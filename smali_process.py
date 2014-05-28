import re 
import os 

score=[["Landroid/content/Intent;-><init>","0"],["Landroid/content/ContextWrapper;->sendBroadcast","0"],["Landroid/content/ContextWrapper;->sendOrderedBroadcast","0"],["Landroid/content/ContextWrapper;->sendStickyBroadcast","0"],["Landroid/content/ContextWrapper;->sendStickyOrderedBroadcast","0"],["Landroid/content/ContextWrapper;->startActivity","0"],["Landroid/content/ContextWrapper;->startActivities","0"],["Landroid/net/Uri;->parse(Ljava/lang/String;)","0"],["Landroid/content/ContextWrapper;->openFileInput","0"],["Landroid/content/ContextWrapper;->openFileOutput","0"],["Ljava/io/FileReader;-><init>","0"],["Ljava/io/FileWriter;-><init>","0"],["Ljava/net/URL;-><init>","0"],["Ljava/net/URL;->openConnection","0"],["Ljava/net/URL;->openStream","0"],["Ljava/io/Reader;->read","0"],["Ljava/io/Writer;->write","0"],["Ljava/io/BufferedReader;->read","0"],["Ljava/io/BufferedReader;->readLine","0"],["Ljava/io/BufferedWriter;->write","0"],["Ljava/io/BufferedWriter;->newLine","0"],["Ljava/io/InputStreamReader;->read","0"],["Ljava/io/OutputStreamWriter;->write","0"],["Ljava/io/CharArrayReader;->read","0"],["Ljava/io/CharArrayWriter;->write","0"],["Ljava/io/CharArrayWriter;->writeTo","0"],["Ljava/io/FilterReader;->read","0"],["Ljava/io/FilterWriter;->write","0"],["Ljava/io/StringReader;->read","0"],["Ljava/io/StringWriter;->write","0"],["Ljava/io/PrintWriter;->append","0"],["Ljava/io/PrintWriter;->format","0"],["Ljava/io/PrintWriter;->print","0"],["Ljava/io/PrintWriter;->printf","0"],["Ljava/io/PrintWriter;->println","0"],["Ljava/io/PrintWriter;->write","0"],["Landroid/content/ContextWrapper;->openOrCreateDatabase","0"],["Landroid/database/sqlite/SQLiteDatabase;->openDatabase","0"],["Landroid/database/sqlite/SQLiteDatabase;->openOrCreateDatabase","0"],["Landroid/database/sqlite/SQLiteDatabase;->query","0"],["Landroid/database/sqlite/SQLiteDatabase;->rawQuery","0"],["Landroid/database/sqlite/SQLiteDatabase;->queryWithFactory","0"],["Landroid/database/sqlite/SQLiteDatabase;->rawQueryWithFactory","0"],["Landroid/content/ContentResolver;","0"],["Landroid/telephony/SmsManager;->sendTextMessage","6"],["Landroid/telephony/SmsManager;->sendDataMessage","6"],["Landroid/telephony/SmsManager;->sendMultipartTextMessage","6"],["Landroid/content/pm/PackageManager;->getInstalledApplications","3"],["Landroid/telephony/TelephonyManager;->getDeviceId","3"],["Landroid/telephony/TelephonyManager;->getSubscriberId","5"],["Landroid/telephony/TelephonyManager;->getCallState","5"],["Landroid/telephony/TelephonyManager;->getCellLocation","5"],["Ljava/security/MessageDigest;->getInstance","0"],["Ljava/security/MessageDigest;->update","0"],["Ljava/security/MessageDigest;->digest","0"],["Ljavax/crypto/Cipher;->getInstance","0"],["Ljavax/crypto/spec/SecretKeySpec;-><init>","0"],["Ljavax/crypto/Cipher;->init","0"],["Ljavax/crypto/Cipher;->doFinal","0"],["Landroid/telephony/TelephonyManager;->getLine1Number","5"]]


os.system("egrep -r \"http[:s]\" /tmp/smali >/tmp/result.txt")
res_file=open("/tmp/result.txt")
out_put=open("/tmp/result1.txt","w")
pa=re.compile(r"http[s:][:/][^\"^#]+")

for line in res_file:
	if pa.search(line):
		out_put.write(pa.search(line).group()+"\n")
res_file.close()
out_put.close()
os.system("sort /tmp/result1.txt -u >/tmp/url_result.txt")



os.system("rm /tmp/result.txt")
os.system("rm /tmp/result1.txt")

os.system("egrep -r \"[1][0-9]{10}\" /tmp/smali >/tmp/result.txt")

res_file1=open("/tmp/result.txt")
out_put1=open("/tmp/result1.txt","w")
pa1=re.compile(r"1[0-9]{10}")

for line in res_file1:
	if pa1.search(line):
		out_put1.write(pa1.search(line).group()+"\n")
out_put1.close()
os.system("sort /tmp/result1.txt -u >/tmp/num_result.txt")

api_file=open("config/default_api_collection")
api_result=open("/tmp/api.txt","w")
api_result.close()
for line in api_file:
	if not line.startswith("#") and line.find("L")>-1:
		os.system("egrep -n -r \""+line.split("\n")[0]+"\" /tmp/smali |wc -l >>/tmp/api.txt")
		os.system("echo  -n \""+line+"\" >>/tmp/api.txt")
tmpf=open("/tmp/api.txt")
tmpf1=open("/tmp/api_result_tmp.txt","w")
tmpf1.write(tmpf.read().replace("\nL","\tL"))
tmpf.close()
tmpf1.close()

api_result=open("/tmp/api_result_tmp.txt")
risk_score = 0
for line in api_result:
	num=line.split("\t")[0]
	api=line.split("\t")[1]
	for api_info in score:
		if api_info[0]==api.split("\n")[0] and not num=="0":
			risk_score=risk_score+int(api_info[1])
			if int(api_info[1])!=0:
				print(api.split('\n')[0]+"\t"+api_info[1])
print(risk_score)


