#coding=utf-8
import re
import json
import sys
import argparse

parser = argparse.ArgumentParser(description=\
'json to Process.')
parser.add_argument('filename', type=str,
                    help='path of json file')
args = parser.parse_args()

def hexToStr(hexStr):

    bytes = []
    hexStr = ''.join(hexStr.split(" "))
    for i in range(0, len(hexStr), 2):
        bytes.append(chr(int(hexStr[i:i+2], 16)))
    return unicode(''.join( bytes ), errors='replace')

a=json.loads(open(args.filename).read())
accessfiles=[]
for item in a["accessedfiles"]:
    filename=(a["accessedfiles"][item])
    if not filename in accessfiles:
            accessfiles.append(filename)
print("程序文件访问情况：")
for x in accessfiles:
	print x


print("\n------------------------------------")


dexclasses=[]

for item in a["dexclass"]:
    dex=(a["dexclass"][item]["path"])
    if not dex in dexclasses:
            dexclasses.append(dex)

print("程序调用情况：")
for x in dexclasses:
	print x
print("\n------------------------------------")



opennets=[]
for item in a["opennet"]:
    ip=(a["opennet"][item]["desthost"])
    port=(a["opennet"][item]["destport"])
    if not [ip,port] in opennets:
            opennets.append([ip,port])
print("程序网络连接情况:")
for x in opennets:
	print("IP: "+x[0]+"\tPort: "+x[1])	
print("\n------------------------------------")	
	






recvnets= []

for item in a["recvnet"]:
    ip=(a["recvnet"][item]["host"])
    port=(a["recvnet"][item]["port"])
    data=(a["recvnet"][item]["data"])
    data_decoded=a["recvnet"][item]["data"].decode("hex")
    if not [ip,port,data,data_decoded] in recvnets:
            recvnets.append([ip,port,data,data_decoded])

print("程序接收网络数据情况：")
for x in recvnets:
	try:
		print("IP: "+x[0]+"\tPort: "+x[1]+"\nData_decoded:\n\n"+x[3]+"\n------------------------")
	except:
		print("IP: "+x[0]+"\tPort: "+x[1]+"\nData:\n\n"+x[2]+"\n----------------------")
print("\n------------------------------------")	


sendnets=[]

for item in a["sendnet"]:
    ip=(a["sendnet"][item]["desthost"])
    port=(a["sendnet"][item]["destport"])
    data=(a["sendnet"][item]["data"])
    data_decoded=a["sendnet"][item]["data"].decode("hex")
    if not [ip,port,data,data_decoded] in sendnets:
            sendnets.append([ip,port,data,data_decoded])
print("程序发送网络数据情况：")
for x in sendnets:
	try:
		print("IP: "+x[0]+"\tPort: "+x[1]+"\nData_decoded:\n\n"+x[3]+"\n----------------------------")
	except:
		
		print("IP: "+x[0]+"\tPort: "+x[1]+"\nData:\n\n"+x[2]+"\n----------------------------")
			
print("\n------------------------------------")				
	
recvsactions=[]

for item in a["recvsaction"]:
    action=(a["recvsaction"][item])
    if not [item,action] in recvsactions:
            recvsactions.append([item,action])
print("程序监听广播情况：")
for x in recvsactions:
	print "广播类型: ",
	print x[0],
	print "\t组件名称: ",
	print x[1]

print("\n------------------------------------")	


services=[]
for item in a["servicestart"]:
    service=(a["servicestart"][item]["name"])
    if not service in services:
            services.append(service)
print("程序启动服务情况：")
for x in services:
	print "服务名称: ",
	print x

print("\n------------------------------------")	




smss=[]
for item in a["sendsms"]:
    message=(a["sendsms"][item]["message"])
    number=(a["sendsms"][item]["number"])
    if not [message,number] in smss:
            smss.append([message,number])
print("程序发送短信情况")
for x in smss:
	print "接收短信号码: ",
	print x[1],
	print "\t短信内容: ",
	print x[0]
