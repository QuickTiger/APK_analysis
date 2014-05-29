import os
s="/home/tiger/APKvir/"
for x in os.listdir(s):
	os.system("python apk_process.py "+s+x)
