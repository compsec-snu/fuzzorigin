from platform import platform
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from msedge.selenium_tools import Edge
from msedge.selenium_tools import EdgeOptions

import sys
import os
import time
import urllib3
import subprocess
import json


class EdgeHandler:
    def __init__(self, binary_path, name="default", output="."):
        self.name = name
        self.binary_path = os.path.abspath(binary_path)
        self.driver_home = os.path.dirname(self.binary_path)
        self.driver_path = os.path.join(self.driver_home, "msedgedriver")
        self.remote_url = "127.0.0.1:8888"
        self.driver_log_dir = os.path.join(output, "logs/driver")
        self.exception_log_dir = os.path.join(output, "logs/exception")
        self.check_log_dir = os.path.join(output, "logs/check")
        self.driver_log = None
        self.browser_log = []
        self.alert_log = []
        self.check_text = []

        self.driver = None
        self.driver_log_fd = None
        self.main_window = None

        self.reset_flag = 0
        self.crash_flag = False

        self.cur_url = self.name
        self.origin = []
        self.last_origin = ""
        self.origin_change = 0

        if "ASAN_OPTIONS" not in os.environ:
            os.environ["ASAN_OPTIONS"] = "detect_odr_violation=1"

        if self.driver_home not in os.environ["PATH"]:
            os.environ["PATH"] = f'{os.environ["PATH"]}:{self.driver_home}'

        os.environ["webdriver.chrome.driver"] = self.driver_path

        if not os.path.exists(self.driver_log_dir):
            os.makedirs(self.driver_log_dir)

        if not os.path.exists(self.exception_log_dir):
            os.makedirs(self.exception_log_dir)

        if not os.path.exists(self.check_log_dir):
            os.makedirs(self.check_log_dir)

    def open(self, cur_time=0):
        print(f"[+] open new driver {cur_time}")
        self.crash_flag = False

        options = EdgeOptions()
        options.use_chromium = True
        options.set_headless()
        options.add_argument("--log-level=0")
        options._caps["platform"] = "ANY"
        options.binary_location = self.binary_path

        d = DesiredCapabilities.EDGE
        
        # low version logging
        d['loggingPrefs'] = { 'browser':'ALL' }

        # high version logging
        d['goog:loggingPrefs'] = { 'browser':'ALL', 'performance': 'ALL'}
        d['edg:loggingPrefs'] = { 'browser':'ALL', 'performance': 'ALL'}

        self.driver_log = os.path.join(self.driver_log_dir, f"{self.name}_{cur_time}.text")

        try:
            # self.driver = webdriver.Edge(self.driver_path, service_args=["--verbose", f"--log-path={self.driver_log}"], desired_capabilities=d, chrome_options=options)
            self.driver = Edge(service_args=["--verbose", f"--log-path={self.driver_log}"], options=options)
            self.driver.set_page_load_timeout(2)
            self.driver.set_script_timeout(10)
            self.main_window = self.driver.window_handles[0]
            self.driver_log_fd = open(self.driver_log)
        except Exception as e:
            print(f"[-] {str(e)}")
            return -2

    def click_item(self, item):
        try:
            # print(f"[+] try to click {item.get_attribute('outerHTML')}")
            item.click()
        except selenium.common.exceptions.UnexpectedAlertPresentException as e:
            print(f"[+] UnexpectedAlertPresentException : {e}")
            try:
                # result = True
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                self.alert_log.append(alert_text)
                alert.accept()
            except selenium.common.exceptions.WebDriverException as e:
                pass
        except selenium.common.exceptions.ElementNotInteractableException as e:
            pass
        except selenium.common.exceptions.WebDriverException as e:
            pass
        # except Exception as e:
        #     print(f"[+] click Exception : {e}")
        #     pass
        # time.sleep(0.1)

    def check_alert(self, wait_time=0.01):
        try:
            WebDriverWait(self.driver, wait_time).until (EC.alert_is_present())
            alert_count = 0
            
            while True:
                if alert_count > 20:
                    break
                if len(self.driver.window_handles) == 1:
                    break
                try:
                    alert = self.driver.switch_to.alert
                    alert_text = alert.text
                    self.alert_log.append(alert_text)
                    alert.accept()
                    # print(f"alert Exists in page - {alert_text}")
                except selenium.common.exceptions.WebDriverException as e:
                    pass
                alert_count = alert_count + 1
        except selenium.common.exceptions.TimeoutException as e:
            # print("alert does not Exist in page")
            pass

    def run(self, url, idx=None):
        if idx is None:
            idx = self.name

        self.cur_url = url.rsplit("/", 1)[1]
        exception_log = os.path.join(self.exception_log_dir, f"{idx}.txt")
        self.origin = []
        
        try:
            try:
                self.reset_flag = 0
                driver = self.driver
                self.browser_log = []
                self.alert_log = []
                self.check_text = []

                driver.execute_script(f'window.open("{url}");')
                driver.switch_to.window(self.driver.window_handles[1])
                self.check_alert()

                item = driver.find_element_by_tag_name("body")
                if item:
                    self.click_item(item)

                arr = driver.find_elements_by_name("click_me")
                for item in arr:
                    self.click_item(item)

                frames = driver.find_elements_by_tag_name("iframe")
                for frame in frames:
                    try:
                        driver.switch_to_frame(frame)
                    except selenium.common.exceptions.WebDriverException as e:
                        continue

                    arr = driver.find_elements_by_name("click_me")
                    for item in arr:
                        self.click_item(item)

                self.check_alert()

                for handler in driver.window_handles:
                    if handler == self.main_window:
                        continue
                    try:
                        driver.switch_to.window(handler)
                    # except Exception as e:
                    except selenium.common.exceptions.WebDriverException as e:
                        continue
                    for entry in driver.get_log('browser'):
                        try:
                            if entry['source'] == 'console-api':
                                self.browser_log.append(entry)
                        except KeyError as e:
                            pass

                driver.switch_to.window(driver.window_handles[1])

            except selenium.common.exceptions.UnexpectedAlertPresentException as e:
                print(f"[+] UnexpectedAlertPresentException : {e}")
                try:
                    alert = driver.switch_to.alert
                    alert_text = alert.text
                    self.alert_log.append(alert_text)
                    alert.accept()
                except selenium.common.exceptions.WebDriverException as e:
                    pass
            except selenium.common.exceptions.TimeoutException as e:
                print(f"[-] TimeoutException : {e}")
                driver.execute_script("window.stop();")
                with open(exception_log, "w") as f:
                    f.write(str(e))
                self.reset_flag = 1
            except selenium.common.exceptions.WebDriverException as e:
                print(f"[-] WebDriverException : {e}")
                with open(exception_log, "w") as f:
                    f.write(str(e))

                if "window already closed" in str(e):
                    for entry in driver.get_log('browser'):
                        if entry['source'] == 'console-api':
                            self.browser_log.append(entry)
                else:
                    self.reset_flag = 1

            for handler in driver.window_handles:
                if handler == self.main_window:
                    continue
                try:
                    driver.switch_to.window(handler)
                    driver.close()
                except selenium.common.exceptions.WebDriverException as e:
                    continue

            driver.switch_to.window(self.main_window)

        except Exception as e:
            print(f"[-] [{e.__class__.__name__}] {e}")
            self.reset_flag = 2
            # raise e

    def ret(self):
        check_result = self.check()
        origin = list(set(self.origin))
        origin_cnt = len(origin)
        return check_result, self.reset_flag, origin_cnt, self.origin_change

    def quit(self, remove=False):
        try:
            print("[+] try to press ESC")
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        except selenium.common.exceptions.WebDriverException as e:
            pass
        except ConnectionRefusedError as e:
            pass
        except AttributeError as e:
            pass
        except urllib3.exceptions.MaxRetryError as e:
            pass
        except urllib3.exceptions.ProtocolError as e:
            pass
        try:
            print("[+] try to quit driver")
            self.driver.quit()
            self.driver = None
        except AttributeError as e:
            print(e)
            pass
        self.main_window = None

        try:
            print("[+] try to close log fd")
            self.driver_log_fd.close()
            self.driver_log_fd = None
        except AttributeError as e:
            print(e)
            pass

        if remove:
            try:
                os.remove(self.driver_log)
            except FileNotFoundError as e:
                print(e)
                pass

    def quit_force(self, remove=False):
        ps = 'ps -ef'.split()
        ret = subprocess.check_output(ps)

        arr = ret.decode().split("\n")
        for item in arr:
            cmd = " ".join(item.split()[7:])
            if self.driver_log in cmd:
                pid = item.split()[1]

                for item2 in arr:
                    if len(item2.split()) < 2:
                        continue
                    parent_pid = item2.split()[2]
                    if pid == parent_pid:
                        child_pid = item2.split()[1]
                        child_cmd = " ".join(item2.split()[7:])
                        print(f'[+] kill {child_pid} {child_cmd}')
                        os.system(f"kill -9 {child_pid} 2> /dev/null")
                print(f'[+] kill {pid} {cmd}')
                os.system(f"kill -9 {pid}  2> /dev/null")

        self.driver = None
        self.main_window = None

        try:
            print("[+] try to close log fd")
            self.driver_log_fd.close()
            self.driver_log_fd = None
        except AttributeError as e:
            print(e)
            pass

        if remove:
            try:
                os.remove(self.driver_log)
            except FileNotFoundError as e:
                print(e)
                pass

    def check(self):
        self.last_origin = ""
        self.origin_change = 0
        
        for entry in self.browser_log:
            message = entry["message"]
            text = " ".join(message.split(" ")[2:])
            if message.startswith('"'):
                text = text[1:-1]

            lines = text.split("\n")
            for line in lines:
                if self.check_log(line.strip()):
                    self.write_raw_log()
                    self.crash_flag = True
                    return True

            lines = text.split("\\n")
            for line in lines:
                if self.check_log(line.strip()):
                    self.write_raw_log()
                    self.crash_flag = True
                    return True

        for text in self.alert_log:
            if not text:
                continue
            lines = text.split('\n')
            for line in lines:
                try:
                    if self.check_log(line.strip()):
                        self.write_raw_log()
                        self.crash_flag = True
                        return True
                except:
                    pass

        try:
            lines = self.driver_log_fd.readlines()
        except:
            return False

        for i, line in enumerate(lines):
            try:
                if 'INFO:CONSOLE' in line:
                    text = line.split("\"")[1]
                    if self.check_log(text):
                        self.write_raw_log()
                        self.crash_flag = True
                        return True
            except:
                pass
            if "Runtime.consoleAPICalled" in line:
                try:
                    text = lines[i+3].split("\"")[3]
                    if self.check_log(text):
                        self.write_raw_log()
                        self.crash_flag = True
                        return True
                except:
                    pass
        return False

    def check_log(self, message):
        if message.startswith("\"") and message.endswith("\""):
            message = message[1:-1]
        if message.startswith("\'") and message.endswith("\'"):
            message = message[1:-1]

        if "[UXSS]" in message:
            return True
        
        text = message.split(" ")
        try:
            idx = text[0]
            gt = text[1]
            result = text[2]

            if result.endswith('/'):
                result = result[:-1]


            self.check_text.append([idx, gt, result])
            self.origin.append(result)

            if result != self.last_origin:
                self.origin_change += 1
                self.last_origin = result

            if result == "null":
                return False

            hostname = result.split(":")[1][2:]

            if gt != result:
                if hostname == "0.0.0.0":
                    return False
                return True

        except:
            pass
        return False

    def write_check_log(self):
        dest = os.path.join(self.check_log_dir, f"check_{self.cur_url}.text")
        with open(dest, "w") as f:
            for item in self.check_text:
                f.write(" ".join(item) + "\n")

    def write_raw_log(self):
        dest = os.path.join(self.check_log_dir, f"raw_{self.cur_url}.json")
        with open(dest, "w") as f:
            data = {
                "console": self.browser_log,
                "alert": self.alert_log
            }
            json.dump(data, f)

        self.write_check_log()

import signal

def handler(signum, frame):
    print('\n\n[-] Signal handler called with signal', signum)
    print("[+] Fuzzer will be terminated")
    os._exit(1)

def main():
    testcase_name = sys.argv[1]

    signal.signal(signal.SIGINT, handler)

    edge_path = "/home/shelling/edge/microsoft-edge"

    base_url = "http://127.0.0.1:7000"
    url = f"{base_url}/{testcase_name}"
    edge_handler = EdgeHandler(edge_path, name=testcase_name)
    
    print("[+] end init")
    count = 1
    ret = edge_handler.open(cur_time=count)
    print("[+] end open")
    while True:
        
        edge_handler.run(url)
        ret, reset, origin, origin_update = edge_handler.ret()
        print(f"[+] end run - {ret, reset, origin}")
        if ret:
            # chrome_handler.write_check_log()
            break

        if count % 100 == 0:
            print("[+] reset")
            edge_handler.quit()
            edge_handler.open(cur_time=count)

        count += 1
        break
    
    edge_handler.quit()
    return ret


if __name__ == "__main__":
    main()