import sys
import os
import random
import signal
import shutil
import time

from contextlib import contextmanager

from src.script.testcase_generator import TestcaseGenerator
from src.script.testcase import Testcase
from src.executor.chrome_handler import ChromeHandler
from src.executor.firefox_handler import FirefoxHandler
from src.executor.edge_handler import EdgeHandler
from src.executor.safari_handler import SafariHandler
from src.fuzzer.exception import TestcaseTimeout

fuzzer = None

@contextmanager
def timeout(time):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)

class Fuzzer:
    def __init__(self, target, binary, fuzzer_idx=0):
        self.idx = 0
        self.fuzzer_idx = fuzzer_idx
        self.binary = binary
        self.target = target
        self.cur_input = None
        self.src1 = None
        self.src2 = None
        self.op = None
        self.queue_idx = 0

        self.parent_path = "servers/data/parent/"
        self.child_path = "servers/data/child/"

        self.base_url = "http://127.0.0.1:7000"

        self.report_path = f"tests/output_{self.fuzzer_idx}"

        if self.target == "chrome":
            self.execute_handler = ChromeHandler(self.binary, output=self.report_path)
            self.console_log = True
        elif self.target == "firefox":
            self.execute_handler = FirefoxHandler(self.binary, output=self.report_path)
            self.console_log = True
        elif self.target == "edge":
            self.execute_handler = EdgeHandler(self.binary, output=self.report_path)
            self.console_log = True
        elif self.target == "safari":
            self.execute_handler = SafariHandler(self.binary, output=self.report_path)
            self.console_log = False

        self.testcase_generator = TestcaseGenerator()

        self.start_time = time.time()

        self.crash_path = os.path.join(self.report_path, "crash")
        self.queue_path = os.path.join(self.report_path, "queue")
        
        if not os.path.exists(self.crash_path):
            os.makedirs(self.crash_path)

        if not os.path.exists(self.queue_path):
            os.makedirs(self.queue_path)

        self.crash_flag = False

        self.timeout = 3

        self.exec_count = 0
        self.timeout_count = 0
        self.crash_count = 0
        self.total_exec_time = 0
        self.reset_count = 0
        self.reset_signal = 0
        self.testcase_name = ""
        self.cross_origin = 0

    def setup_shm(self, shm_id):
        if os.environ.get("__AFL_SHM_ID") is None:
            os.environ["__AFL_SHM_ID"] = str(shm_id) 
            print('> shm_id is set as {}'.format(shm_id))

    def unset_shm(self):
        del os.environ["__AFL_SHM_ID"]

    def initialize(self):
        print("[+] FUZZER initialize")
        self.execute_handler.open(cur_time=int(time.time()-self.start_time))

    def reset(self):
        print("[+] FUZZER reset")
        
        signal.alarm(self.timeout)
        try:
            print("[+] try to quit chrome driver ...")
            self.execute_handler.quit(remove=(not self.crash_flag))
            
        except TestcaseTimeout as e:
            print("[-] reset timeout, retry quit force")
            self.execute_handler.quit_force(remove=(not self.crash_flag))
            # self.execute_handler.quit(remove=(not self.crash_flag))
        signal.alarm(0)
        self.execute_handler.open(cur_time=int(time.time()-self.start_time))
        self.reset_count += 1
        self.reset_signal = 0
        self.crash_flag = False
        print("[+] FUZZER reset done")

    def print_summary(self):
        execute_time = int(time.time() - self.start_time)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(f"[exec count]       {self.exec_count}  ({self.exec_count/self.idx * 100}%)")
        print(f"[exec time]        {execute_time}")
        print(f"[exec/sec]         {self.exec_count/execute_time}")
        print(f"[avg exec time]    {self.total_exec_time/self.idx}")
        print(f"[crash count]      {self.crash_count}  ({self.crash_count/self.idx * 100}%)")
        print(f"[timeout count]    {self.timeout_count}  ({self.timeout_count/self.idx * 100}%)")
        print(f"[reset count]      {self.reset_count}")
        print(f"[origin count]     {self.cross_origin}")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        summary_path = os.path.join(self.report_path, "summary.txt")

        with open(summary_path, "w") as f:
            f.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
            f.write(f"[exec count]       {self.exec_count}  ({self.exec_count/self.idx * 100}%)" + "\n")
            f.write(f"[exec time]        {execute_time}" + "\n")
            f.write(f"[exec/sec]         {self.exec_count/execute_time}" + "\n")
            f.write(f"[avg exec time]    {self.total_exec_time/self.idx}" + "\n")
            f.write(f"[crash count]      {self.crash_count}  ({self.crash_count/self.idx * 100}%)" + "\n")
            f.write(f"[timeout count]    {self.timeout_count}  ({self.timeout_count/self.idx * 100}%)" + "\n")
            f.write(f"[reset count]      {self.reset_count}" + "\n")
            f.write(f"[origin count]     {self.cross_origin}" + "\n")
            f.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

    def load_queue(self):
        files = os.listdir(self.queue_path)

        try:
            items = random.choices(files, k=2)
            self.src1 = items[0]
            self.src2 = items[1]

        except:
            self.src1 = None
            self.src2 = None


    def get_html_name(self, idx):
        return f"fuzz-{self.fuzzer_idx}-{idx}"

    def to_server(self):
        html_name = self.to_server_target(self.cur_input.main, "main")
        self.to_server_target(self.cur_input.sub, "sub")
        self.to_server_target(self.cur_input.iframe, "iframe")
        return html_name

    def to_server_target(self, web_page, target):
        if target == "main":
            html_name = f"{self.get_html_name(self.idx)}.html"
            dest = os.path.join(self.parent_path, html_name)
        elif target == "sub":
            html_name = f"{self.get_html_name(self.idx)}-sub.html"
            dest = os.path.join(self.parent_path, html_name)
        else:
            html_name = f"{self.get_html_name(self.idx)}.html"
            dest = os.path.join(self.child_path, html_name)

        code = web_page.to_string()

        with open(dest, "w") as f:
            f.write(code)

        return html_name

    def remove_server(self, idx):
        html_name = f"{self.get_html_name(self.idx)}.html"
        dest = os.path.join(self.parent_path, html_name)
        os.remove(dest)

        html_name = f"{self.get_html_name(self.idx)}-sub.html"
        dest = os.path.join(self.parent_path, html_name)
        os.remove(dest)

        html_name = f"{self.get_html_name(self.idx)}.html"
        dest = os.path.join(self.child_path, html_name)
        os.remove(dest)

    def run(self, count=0):
        self.reset_signal = 0
        testcase_name = self.testcase_name

        while True:
            self.idx = self.idx + 1
            if count > 0 and self.idx > count:
                return -1

            print(f"[+] run {testcase_name}")
            
            url = f"{self.base_url}/{testcase_name}"

            start = time.time()

            signal.alarm(self.timeout)
            
            self.execute_handler.run(url, idx=testcase_name)
            signal.alarm(0)

            ret, reset, origin, origin_change, poc_idx = self.execute_handler.ret()
            end = time.time()
            exec_time = end - start

            print(f"[ret] {ret, reset, origin, origin_change, poc_idx}")
            print(f"[+] elapsed time is {exec_time}")

            if reset == 2:
                self.reset()

            elif reset == 1:
                self.reset_signal += 1
                if self.reset_signal > 100:
                    self.reset()

            self.exec_count += 1
            self.total_exec_time += exec_time

            if origin > 1:
                self.cross_origin += 1

            if ret == 1:
                print(f"[+] crash")
                break

            if self.idx % 100 == 0:
                self.reset()

            if self.idx % 10 == 0:
                self.print_summary()
        return self.idx

    def parse_seed_name(self, name):
        splited = name.split(",")
        idx = int(splited[0][3:])
        tmp = splited[1][4:].split("+")
        src = []
        for item in tmp:
            try:
                src.append(int(item))
            except:
                src.append(None)
        time = splited[2][5:]
        reason = splited[3]
        return (idx, src, time, reason)

    def make_seed_name(self, idx, src1, src2, time, reason):
        return "id:{:05d},src:{:05d}+{:05d},time:{},{}".format(idx, src1, src2, time, reason)

    def save_crash(self):
        html_name = f"{self.get_html_name(self.idx)}.html"
        src = os.path.join(self.parent_path, html_name)
        dest = os.path.join(self.crash_path, html_name)
        shutil.copyfile(src, dest)

        html_name = f"{self.get_html_name(self.idx)}-sub.html"
        src = os.path.join(self.parent_path, html_name)
        dest = os.path.join(self.crash_path, html_name)
        shutil.copyfile(src, dest)

        src = os.path.join(self.child_path, f"{self.get_html_name(self.idx)}.html")
        dest = os.path.join(self.crash_path, f"{self.get_html_name(self.idx)}-child.html")
        shutil.copyfile(src, dest)


    def finalize(self):
        print("[+] FUZZER finalize")
        self.execute_handler.quit()


def handler(signum, frame):
    if signum == signal.SIGALRM:
        print('[-] Signal handler called with signal', signum)
        raise TestcaseTimeout("testcase timeout")

    else:
        print('\n\n[-] Signal handler called with signal', signum)
        print("[+] Fuzzer will be terminated")
        if fuzzer:
            fuzzer.finalize()
        print("[+] Fuzzer terminated")
        os._exit(1)


def main():
    global fuzzer

    target = sys.argv[1]
    binary = sys.argv[2]
    testcase_name = sys.argv[3]
    idx = 999

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGALRM, handler)

    fuzzer = Fuzzer(target, binary, fuzzer_idx=idx)
    fuzzer.initialize()
    fuzzer.testcase_name = testcase_name
    fuzzer.run(count=100)

    fuzzer.finalize()


if __name__ == "__main__":
    main()
