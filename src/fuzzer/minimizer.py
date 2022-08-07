import sys
import os
import signal
import shutil
import secrets
import random

from bs4 import BeautifulSoup

from src.fuzzer.exception import TestcaseTimeout
from src.fuzzer.reproducer import Fuzzer

from tools.lithium.src.lithium.testcases import TestcaseLine
from tools.lithium.src.lithium.strategies import Minimize

fuzzer = None

class Minimizer:
    def __init__(self, target, binary, testcase):
        self.target = target
        self.binary = binary
        self.testcase = testcase
        self.testcase_name = ""
        self.sub_name = ""
        self.child_name = ""
        self.child_sub_name = ""

        self.limit_try = 30
        self.max_try = 0
        self.best_try = self.limit_try
        

        self.base_url = "http://127.0.0.1:70"
        self.base_data = "new_servers/data"

        self.idx = secrets.token_hex(4)
        self.working_dir = os.path.join("minimize", self.idx)
        self.original_dir = os.path.join(self.working_dir, "original")
        self.best_dir = os.path.join(self.working_dir, "best")
        self.cur_dir = os.path.join(self.working_dir, "cur")
        self.raw_dir = os.path.join(self.working_dir, "raw")
        
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)

        if not os.path.exists(self.original_dir):
            os.makedirs(self.original_dir)

        if not os.path.exists(self.best_dir):
            os.makedirs(self.best_dir)

        if not os.path.exists(self.cur_dir):
            os.makedirs(self.cur_dir)

        if not os.path.exists(self.raw_dir):
            os.makedirs(self.raw_dir)

        self.origins = 0
        self.pages = 0

        self.get_origins_pages(self.testcase)

        self.testcase_copy(self.testcase, self.original_dir)
        self.testcase_copy(self.testcase, self.best_dir)

    def get_origins_pages(self, src):
        arr = os.listdir(src)
        self.testcase_name = arr[0].split("_")[0]

        for item in arr:
            origin = int(item.split("_")[1])
            page = int(item.split("_")[2].split(".")[0])

            if origin > self.origins:
                self.origins = origin
            if page > self.pages:
                self.pages = page


    def testcase_copy(self, src, dest):
        arr = os.listdir(src)

        for item in arr:
            shutil.copyfile(os.path.join(src, item), os.path.join(dest, item))

    def testcase_to_server(self):
        arr = os.listdir(self.cur_dir)

        for item in arr:
            origin = item.split("_")[1]

            src = os.path.join(self.cur_dir, item)
            dest = os.path.join(self.base_data, f"idx_{origin}", item)
            print(f'[+] copy {src} -> {dest}')
            shutil.copyfile(src, dest)


    def fuzzer_run(self, init=False, count=0):
        global fuzzer

        self.testcase_to_server()

        print('debug')
        print(f'init:{init}, count:{count}')

        fuzzer = Fuzzer(self.target, self.binary, fuzzer_idx=999)
        fuzzer.initialize()
        fuzzer.testcase_name = f"{self.testcase_name}_0_0.html"
        ret = fuzzer.run(count=count)
        fuzzer.finalize()

        if init and (ret == -1):
            print("[-] reproduce fail :(")
            exit(-1)

        if ret >= 0:
            if ret > self.max_try:
                self.max_try = ret
            if ret < self.best_try:
                self.best_try = ret

        if ret == -1:
            print('[-] fuzzer_run: FAIL')
            return False
        else:
            print('[+] fuzzer_run: SUCCESS')
            return True

    def dry_run(self):
        self.testcase_copy(self.best_dir, self.cur_dir)
        self.fuzzer_run(init=True, count=self.limit_try)

    def fuzzer_test(self, idx, name, count=0):
        if count > self.limit_try:
            count = self.limit_try
        count = 1
        ret = self.fuzzer_run(count=count)
        src = os.path.join(self.cur_dir, name)
        dest = os.path.join(self.raw_dir, f"{idx}_{name}_{ret}")
        shutil.copyfile(src, dest)
        return ret

    def run(self):
        print("[+] start reproduce dry run")
        self.dry_run()
        print("[+] finish reproduce dry run")

        round = 1
        for i in range(round):
            print(f"[+] {i+1} round")
            for origin in range(self.origins+1):
                for page in range(self.pages+1):
                    self.minimize_html(origin, page)

        print("[+] finish minimize")
        print('[+] done')

    def minimize_html(self, origin, page):
        name = f"{self.testcase_name}_{origin}_{page}.html"

        self.testcase_copy(self.best_dir, self.cur_dir)
        src = os.path.join(self.best_dir, name)
        dest = os.path.join(self.cur_dir, name)

        tc = TestcaseLine()
        tc.load(src)

        st = Minimize()
        reduction = st.reduce(tc)

        for i, attempt in enumerate(reduction):
            if i > 1000:
                break
            attempt.dump(dest)
            ret = self.fuzzer_test(i, name, count=self.max_try * 2)

            if ret:
                attempt.dump(src)
            reduction.feedback(ret)

        testcase = reduction.testcase
        testcase.dump(src)





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

    target = sys.argv[1]
    binary = sys.argv[2]
    testcase = sys.argv[3]
    idx = 999

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGALRM, handler)

    mininizer = Minimizer(target, binary, testcase)
    mininizer.run()


if __name__ == "__main__":
    main()
