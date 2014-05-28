#coding=utf-8

import json

def hexToStr(hexStr):
    """
    Convert a string hex byte values into a byte string
    """

    bytes = []
    hexStr = ''.join(hexStr.split(" "))
    for i in range(0, len(hexStr), 2):
        bytes.append(chr(int(hexStr[i:i+2], 16)))
    return unicode(''.join( bytes ), errors='replace')


a=json.loads(open("/tmp/droidbox.dump").read())
for item in json.loads(json.dumps(a["opennet"],sort_keys=True)):
	print(" 建立网络连接 时间:"+str(item)[0:5]+" "+a["opennet"][item]["desthost"]+":"+a["opennet"][item]["destport"])
	

for item in json.loads(json.dumps(a["sendnet"],sort_keys=True)):
	print("发送网络数据 时间:"+str(item)[0:5]+" "+a["sendnet"][item]["desthost"]+":"+a["sendnet"][item]["destport"]+"\t 发送内容："+str(a["sendnet"][item]["data"]).decode("hex"))


for item in json.loads(json.dumps(a["accessedfiles"],sort_keys=True)):
	print("文件访问  fileid: "+str(item)+" "+a["accessedfiles"][item])



for item in json.loads(json.dumps(a["fdaccess"],sort_keys=True)):
#	try:
	print("文件访问 时间: "+str(item)+" "+a["fdaccess"][item]["path"]+" "+a["fdaccess"][item]["operation"]+" "+a["fdaccess"][item]["type"]+" "+str(a["fdaccess"][item]["data"]).decode("hex"))
#	except:
	#	pass

for item in json.loads(json.dumps(a["recvnet"],sort_keys=True)):
	print("接收网络数据  时间: "+str(item)[0:5]+" "+a["recvnet"][item]["type"]+"  "+a["recvnet"][item]["host"]+":"+a["recvnet"][item]["port"]+"\t 接收内容 ："+hexToStr(a["recvnet"][item]["data"]))


for item in json.loads(json.dumps(a["sendsms"],sort_keys=True)):
	print("发送短信: "+str(item)[0:5]+" "+a["sendsms"][item]["type"]+" 送达号码："+a["sendsms"][item]["number"]+" 短信内容："+a["sendsms"][item]["message"])
