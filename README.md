# FuzzOrigin

## Paper
[FuzzOrigin: Detecting UXSS vulnerabilities in Browsers through Origin Fuzzing](https://www.usenix.org/conference/usenixsecurity22/presentation/kim)

## Server Setting
```
$ sudo apt-get install docker-compose
$ cd servers
$ sudo docker-compose up -d
$ sudo chown -R $(id -nu):$(id -ng) .
```

## Download chrome
```
$ python3 chrome_downloader.py [version]
```
Visit [OmahaProxy](https://omahaproxy.appspot.com/) to check chrome version.

## Run fuzzer
python3 -m src.fuzzer.fuzzer [browser type] [browser binary] [idx]
- browser type: chrome, firefox, edge
- browser binary: browser binary path
- idx: test idx
```
$ python3 -m src.fuzzer.fuzzer chrome chrome/103.0.5042.0_999146/chrome 0
```

## Result
tests/output_[idx]
```
$ ls tests/output_0
```

## Citation
```
@inproceedings {281314,
    author = {Sunwoo Kim and Young Min Kim and Jaewon Hur and Suhwan Song and Gwangmu Lee and Byoungyoung Lee},
    title = {{FuzzOrigin}: Detecting {UXSS} vulnerabilities in Browsers through Origin Fuzzing},
    booktitle = {31st USENIX Security Symposium (USENIX Security 22)},
    year = {2022},
    isbn = {978-1-939133-31-1},
    address = {Boston, MA},
    pages = {1008--1023},
    url = {https://www.usenix.org/conference/usenixsecurity22/presentation/kim},
    publisher = {USENIX Association},
    month = aug,
}
```