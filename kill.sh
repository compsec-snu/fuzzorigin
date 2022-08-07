ps -ef | grep fuzzer.fuzzer | awk -F" " '{print "kill -9 " $2}' | sh
ps -ef | grep chrome | grep /home/shelling/chromium | awk -F" " '{print "kill -9 " $2}' | sh
ps -ef | grep geckodriver  | awk -F" " '{print "kill -9 " $2}' | sh
ps -ef | grep firefox-bin  | awk -F" " '{print "kill -9 " $2}' | sh
ps -ef | grep msedgedriver  | awk -F" " '{print "kill -9 " $2}' | sh
ps -ef | grep msedge  | awk -F" " '{print "kill -9 " $2}' | sh
ps -ef | grep firefox  | awk -F" " '{print "kill -9 " $2}' | sh
ps -ef | grep chrome  | awk -F" " '{print "kill -9 " $2}' | sh
