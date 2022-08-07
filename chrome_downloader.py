import sys
import os
import requests
import zipfile

class Downloader:
    def __init__(self, os_type="Linux_x64"):
        self.position_lookup_url = "https://omahaproxy.appspot.com/deps.json"
        self.download_url = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o"
        self.os = os_type
        self.base = "chrome"

        if not os.path.exists(self.base):
            os.makedirs(self.base)

    def get_position(self, version):
        url = self.position_lookup_url + f"?version={version}"
        payload={}
        headers = {}
        r = requests.request("GET", url, headers=headers, data=payload)
        try:
            return r.json()["chromium_base_position"]
        except:
            return None


    def download(self, url, name):
        r = requests.request("GET", url)

        try:
            r.raise_for_status()
            with open(name, "wb") as f:
                for chunk in r:
                    f.write(chunk)
            return True
        except:
            return False

    def unzip_and_rename(self, file_path, name):
        os.system(f"cd {self.base} && unzip {file_path} > /dev/null")
        source = "chrome-linux"       
        os.rename(os.path.join(self.base, source), os.path.join(self.base, name))

    def driver_unzip_and_rename(self, file_path, name):
        os.system(f"cd {self.base} && unzip {file_path} > /dev/null")
        source = "chromedriver_linux64"
        driver = "chromedriver"
        
        os.system(f"cd {self.base} && mv {source}/{driver} {name} && rmdir {source}")

    def download_binary(self, version):
        prefix = "Linux_x64"
        postfix = "chrome-linux.zip"
        driver = "chromedriver_linux64.zip"

        print(f"[+] start download chrome binary")
        print(f"[+] get position - {version}")
        position = self.get_position(version)

        if position is None:
            print(f"[-] fail to get position {version}")
            return None   

        print(f"[+] find position - {position}")

        base_url = f"{self.download_url}/{prefix}%2F"
        download_flag = False
        found = 0

        for i in range(100):
            url = f"{base_url}{int(position)+i}%2F{postfix}?alt=media"
            name = f"{version}_{int(position)+i}"
            zip_name = f"{name}.zip"
            if self.download(url, os.path.join(self.base, zip_name)):
                download_flag = True
                found = int(position)+i
                break
        if download_flag:
            print(f"[+] download success - {os.path.join(self.base, zip_name)}")
        else:
            print(f"[-] download fail")
            return None

        self.unzip_and_rename(zip_name, name)

        driver_url = f"{base_url}{found}%2F{driver}?alt=media"
        driver_name = f"{name}_driver.zip"
        self.download(driver_url, os.path.join(self.base, driver_name))

        print(f"[+] download success - {os.path.join(self.base, driver)}")
        self.driver_unzip_and_rename(driver_name, name)

        print(f"[+] chrome is ready - {os.path.join(self.base, name)}")

def main(argv):
    downloader = Downloader(os_type="Linux_x64")
    downloader.download_binary(argv[1])

if __name__ == "__main__":
    main(sys.argv)