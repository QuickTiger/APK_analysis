import os
s="/tmp/apks"
for x in os.listdir(s):
	os.system("python apk_tmp.py "+s+x)
