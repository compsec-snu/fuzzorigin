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
        self.fuzzer_idx = int(fuzzer_idx)
        self.binary = binary
        self.target = target
        self.cur_input = None
        self.src1 = None
        self.src2 = None
        self.op = None
        self.queue_idx = 0

        # self.origins = 5
        # self.pages = 10

        self.origins = 2
        self.pages = 2

        self.base_url = "http://127.0.0.1:70"
        self.base_data = "servers/data"

        if not os.path.exists(self.base_data):
            os.makedirs(self.base_data)

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

        self.testcase_generator = TestcaseGenerator(self.origins, self.pages)
        self.lift_skip = False

        self.start_time = time.time()

        self.crash_path = os.path.join(self.report_path, "crash")
        self.queue_path = os.path.join(self.report_path, "queue")
        self.origin_path = os.path.join(self.report_path, "eval")
        
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
        self.cross_origin = 0
        self.origin_change = 0

    
    def get_base_url(self, origin_idx):
        if origin_idx < 10:
            return  f"{self.base_url}0{origin_idx}"
        else:
            return  f"{self.base_url}{origin_idx}"
    
    def get_url(self, origin_idx, page_idx):
        return f"{self.get_base_url(origin_idx)}/{self.get_name(origin_idx, page_idx)}"

    def get_name(self, name, origin_idx, page_idx):
        return f"{name}_{origin_idx}_{page_idx}.html"

    def save_eval(self, origin, origin_change, violation, eventhandler, event_handler_uni, e_time, e_count):
        if origin == 0:
            return
        # cur = int(time.time() - self.start_time)
        cur = self.idx
        with open(self.origin_path, "a") as f:
            f.write(f"{cur} {origin} {origin_change} {violation} {eventhandler} {event_handler_uni} {e_time} {e_count}\n")

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
            self.execute_handler.quit(remove=(not self.execute_handler.crash_flag))
            
        except TestcaseTimeout as e:
            print("[-] reset timeout, retry quit force")
            self.execute_handler.quit_force(remove=(not self.execute_handler.crash_flag))
            # self.execute_handler.quit(remove=(not self.crash_flag))
        signal.alarm(0)
        self.execute_handler.open(cur_time=int(time.time()-self.start_time))
        self.reset_count += 1
        self.reset_signal = 0
        self.crash_flag = False
        print("[+] FUZZER reset done")

    def quit(self):
        print("[+] FUZZER quit")
        
        signal.alarm(self.timeout)
        try:
            print("[+] try to quit chrome driver ...")
            self.execute_handler.quit(remove=(not self.execute_handler.crash_flag))
            
        except TestcaseTimeout as e:
            print("[-] reset timeout, retry quit force")
            self.execute_handler.quit_force(remove=(not self.execute_handler.crash_flag))
            # self.execute_handler.quit(remove=(not self.crash_flag))
        signal.alarm(0)
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
        print(f"[origin change]     {self.origin_change}")
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
            f.write(f"[origin change]     {self.origin_change}" + "\n")
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

    def generate_testcase(self):
        self.cur_input = self.testcase_generator.generate(self.get_html_name(self.idx))

    def get_html_name(self, idx):
        return f"fuzz-{self.fuzzer_idx}-{idx}"

    def to_server(self):
        tc = self.cur_input

        for origin in range(tc.origins):
            for page in range(tc.pages):
                print(f"[+] write {origin},{page}/{tc.origins},{tc.pages}")
                name = self.get_name(tc.name, origin, page)
                dest = os.path.join(self.base_data, f"idx_{origin}")

                if not os.path.exists(dest):
                    os.makedirs(dest)

                code = tc.get(origin, page).to_string()

                with open(os.path.join(dest, name), "w") as f:
                    f.write(code)
        return self.get_name(tc.name, 0, 0)

    def remove_server(self):
        tc = self.cur_input
        for origin in range(tc.origins):
            for page in range(tc.pages):
                name = self.get_name(tc.name, origin, page)
                dest = os.path.join(self.base_data, f"idx_{origin}", name)
                os.remove(dest)

    def run(self):
        self.reset_signal = 0

        while True:
            self.idx = self.idx + 1
            self.generate_testcase()
            testcase_name = self.to_server()
            print(f"[+] run {testcase_name}")

            url = f"{self.get_base_url(0)}/{testcase_name}"

            if self.execute_handler.driver is None:
                self.initialize()

            start = time.time()

            signal.alarm(self.timeout)

            try:
                self.execute_handler.run(url, idx=testcase_name)
                signal.alarm(0)
            except TestcaseTimeout as e:
                self.execute_handler.reset_flag = 2

            ret, reset, origin, origin_change = self.execute_handler.ret()

            end = time.time()
            exec_time = end - start

            self.origin_change += origin_change

            print(f"[ret] {ret, reset, origin, origin_change}")
            print(f"[+] elapsed time is {exec_time}")

            # self.quit()

            if reset == 2 or self.idx % 100 == 0:
                self.quit()

            # elif reset == 1:
            #     self.reset_signal += 1
            #     if self.reset_signal > 100:
            #         self.reset()

            # self.reset()

            self.exec_count += 1
            self.total_exec_time += exec_time

            if ret == 1:
                self.save_crash()
                self.crash_count += 1
                self.crash_flag = True
                self.quit()

            # else:
            #     self.remove_server()

            if ret == -1:
                self.timeout_count += 1

            if origin > 1:
                self.cross_origin += 1


            if self.idx % 10 == 0:
                self.print_summary()

    def parse_seed_name(self, name):
        splited = name.split(",")
        fuzzer_idx = int(splited[0][7:])
        idx = int(splited[1][3:])
        tmp = splited[2][4:].split("+")
        src = []
        for item in tmp:
            try:
                src.append(int(item))
            except:
                src.append(None)
        time = splited[3][5:]
        reason = splited[4]
        return (fuzzer_idx, idx, src, time, reason)

    def make_seed_name(self, fuzzer_idx, idx, src1, src2, time, reason):
        return "fuzzer:{:03d},id:{:05d},src:{:05d}+{:05d},time:{},{}".format(fuzzer_idx, idx, src1, src2, time, reason)

    def save_crash(self):
        tc = self.cur_input
        for origin in range(tc.origins):
            for page in range(tc.pages):
                name = self.get_name(tc.name, origin, page)
                src = os.path.join(self.base_data, f"idx_{origin}", name)
                dest = os.path.join(self.crash_path, name)
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

    # DISPLAY=:0
    target = sys.argv[1]
    binary = sys.argv[2]
    idx = sys.argv[3]

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGALRM, handler)

    fuzzer = Fuzzer(target, binary, fuzzer_idx=idx)
    fuzzer.run()
    fuzzer.finalize()

if __name__ == "__main__":
    main()
