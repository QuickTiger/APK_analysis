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
    """
    Convert a string hex byte values into a byte string
    """

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
print("文件访问情况如下")
print accessfiles

dexclasses=[]

for item in a["dexclass"]:
    dex=(a["dexclass"][item]["path"])
    if not dex in dexclasses:
            dexclasses.append(dex)
print dexclasses


recvnets= []

for item in a["recvnet"]:
    ip=(a["recvnet"][item]["host"])
    port=(a["recvnet"][item]["port"])
    data=(a["recvnet"][item]["data"])
    data_decoded=a["recvnet"][item]["data"].decode("hex")
    if not [ip,port,data,data_decoded] in recvnets:
            recvnets.append([ip,port,data,data_decoded])
print recvnets

recvsactions=[]

for item in a["recvsaction"]:
    action=(a["recvsaction"][item])
    if not [item,action] in recvsactions:
            recvsactions.append([item,action])
print recvsactions




services=[]
for item in a["servicestart"]:
    service=(a["servicestart"][item]["name"])
    if not service in services:
            services.append(service)
print services


sendnets=[]

for item in a["sendnet"]:
    ip=(a["sendnet"][item]["desthost"])
    port=(a["sendnet"][item]["destport"])
    data=(a["sendnet"][item]["data"])
    data_decoded=a["sendnet"][item]["data"].decode("hex")
    if not [ip,port,data,data_decoded] in sendnets:
            sendnets.append([ip,port,data,data_decoded])
print sendnets

opennets=[]
for item in a["opennet"]:
    ip=(a["opennet"][item]["desthost"])
    port=(a["opennet"][item]["destport"])
    if not [ip,port] in opennets:
            opennets.append([ip,port])
print opennets


smss=[]
for item in a["sendsms"]:
    message=(a["sendsms"][item]["message"])
    number=(a["sendsms"][item]["number"])
    if not [message,number] in smss:
            smss.append([message,number])
print smss
print("世界你好")
