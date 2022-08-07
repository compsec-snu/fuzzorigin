import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

import sys
import os
import time
import urllib3
import subprocess
import json


class FirefoxHandler:
    def __init__(self, firefox_path, name="default", output="."):
        self.name = name
        self.firefox_path = os.path.abspath(firefox_path)
        self.driver_home = os.path.dirname(self.firefox_path)
        self.driver_path = os.path.join(self.driver_home, "geckodriver")
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
        self.pid = -1

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

        options = webdriver.FirefoxOptions()
        options.set_headless()
        options.set_preference('devtools.console.stdout.content', True)
        
        d = DesiredCapabilities.FIREFOX
        
        # low version logging
        d['loggingPrefs'] = { 'browser':'ALL' }

        # # high version logging
        # d['goog:loggingPrefs'] = { 'browser':'ALL', 'performance': 'ALL'}
        # caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        self.driver_log = os.path.join(self.driver_log_dir, f"{self.name}_{cur_time}.text")

        if os.path.isfile(self.driver_log):
            os.remove(self.driver_log)
        binary = FirefoxBinary(self.firefox_path)

        try:
            self.driver = webdriver.Firefox(firefox_binary=binary, log_path=self.driver_log, capabilities=d, firefox_options=options)
            self.driver.set_page_load_timeout(2)
            self.driver.set_script_timeout(10)
            self.main_window = self.driver.window_handles[0]
            self.driver_log_fd = open(self.driver_log)
            self.pid = self.driver.capabilities['moz:processID']
        except Exception as e:
            print(f"[-] {str(e)}")
            return -2

    def click_item(self, item):
        try:
            # print(f"[+] try to click {item.get_attribute('outerHTML')}")
            # item.click()
            pass
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

    def alert_check(self, wait_time=0.01):
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
                driver.switch_to_window(self.driver.window_handles[1])

                self.alert_check(wait_time=1)

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

                self.alert_check(wait_time=0.5)

                for handler in driver.window_handles:
                    if handler == self.main_window:
                        continue
                    try:
                        driver.switch_to_window(handler)
                    # except Exception as e:
                    except selenium.common.exceptions.WebDriverException as e:
                        continue

                driver.switch_to_window(driver.window_handles[1])

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
                    driver.switch_to_window(handler)
                    driver.close()
                except selenium.common.exceptions.WebDriverException as e:
                    continue

            driver.switch_to_window(self.main_window)

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
        if self.pid > 1:
            os.system(f"kill -9 {self.pid} 2> /dev/null")
            self.pid = -1

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
                if 'console.log' in line:
                    self.browser_log.append(line)
                    text = line.split(": ")[1].strip()
                    if self.check_log(text):
                        self.write_raw_log()
                        self.crash_flag = True
                        return True
                else:
                    self.check_log(text)
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
            
        # reduce false positive
        if message.startswith("\""):
            return False

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

    firefox_path = "firefox/firefox-91.0b9/firefox"

    base_url = "http://127.0.0.1:7000"
    url = f"{base_url}/{testcase_name}"
    firefox_handler = FirefoxHandler(firefox_path, name=testcase_name)
    
    print("[+] end init")
    count = 0
    ret = firefox_handler.open(cur_time=count)
    print("[+] end open")
    while True:
        
        firefox_handler.run(url)
        ret, reset, origin, origin_update = firefox_handler.ret()
        print(f"[+] end run - {ret, reset, origin}")
        if ret:
            # firefox_handler.write_check_log()
            break

        if count % 100 == 0:
            print("[+] reset")
            firefox_handler.quit()
            firefox_handler.open(cur_time=count)

        count += 1
        break
    
    firefox_handler.quit()
    # firefox_handler.quit_force()
    return ret

if __name__ == "__main__":
    main()