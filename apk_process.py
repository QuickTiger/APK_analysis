#coding=utf-8
import sys
import re
import os
import shutil
import time
import argparse
from androguard.core.bytecodes import apk
from apkil import smali, monitor, logger



mani_info=[["访问登记属性","android.permission.ACCESS_CHECKIN_PROPERTIES ","读取或写入登记check-in数据库属性表的权限","3"],["获取错略位置","android.permission.ACCESS_COARSE_LOCATION","通过WiFi或移动基站的方式获取用户错略的经纬度信息，定位精度大概误差在30~1500米","3"],["获取精确位置","android.permission.ACCESS_FINE_LOCATION","通过GPS芯片接收卫星的定位信息，定位精度达10米以内","3"],["访问定位额外命令","android.permission.ACCESS_LOCATION_EXTRA_COMMANDS","允许程序访问额外的定位提供者指令","6"],["获取模拟定位信息","android.permission.ACCESS_MOCK_LOCATION","获取模拟定位信息，一般用于帮助开发者调试应用","5"],["获取网络状态","android.permission.ACCESS_NETWORK_STATE","获取网络信息状态，如当前的网络连接是否有效","5"],["访问Surface Flinger","android.permission.ACCESS_SURFACE_FLINGER","Android平台上底层的图形显示支持，一般用于游戏或照相机预览界面和底层模式的屏幕截图","1"],["获取WiFi状态","android.permission.ACCESS_WIFI_STATE","获取当前WiFi接入的状态以及WLAN热点的信息","3"],["账户管理","android.permission.ACCOUNT_MANAGER","获取账户验证信息，主要为GMail账户信息","3"],["验证账户","android.permission.AUTHENTICATE_ACCOUNTS","允许一个程序通过账户验证方式访问账户管理ACCOUNT_MANAGER相关信息","3"],["电量统计","android.permission.BATTERY_STATS","获取电池电量统计信息","1"],["绑定小插件","android.permission.BIND_APPWIDGET","允许一个程序告诉appWidget服务需要访问小插件的数据库，只有非常少的应用才用到此权限","1"],["绑定设备管理","android.permission.BIND_DEVICE_ADMIN","请求系统管理员接收者receiver，只有系统才能使用","10"],["绑定输入法","android.permission.BIND_INPUT_METHOD ","请求InputMethodService服务，只有系统才能使用","10"],["绑定RemoteView","android.permission.BIND_REMOTEVIEWS","必须通过RemoteViewsService服务来请求，只有系统才能用","10"],["绑定壁纸","android.permission.BIND_WALLPAPER","必须通过WallpaperService服务来请求，只有系统才能用","10"],["使用蓝牙","android.permission.BLUETOOTH","允许程序连接配对过的蓝牙设备","1"],["蓝牙管理","android.permission.BLUETOOTH_ADMIN","允许程序进行发现和配对新的蓝牙设备","5"],["变成砖头","android.permission.BRICK","能够禁用手机，非常危险","10"],["应用删除时广播","android.permission.BROADCAST_PACKAGE_REMOVED","当一个应用在删除时触发一个广播","7"],["收到短信时广播","android.permission.BROADCAST_SMS","当收到短信时触发一个广播","7"],["连续广播","android.permission.BROADCAST_STICKY","允许一个程序收到广播后快速收到下一个广播","1"],["WAP PUSH广播","android.permission.BROADCAST_WAP_PUSH","WAP PUSH服务收到后触发一个广播","1"],["拨打电话","android.permission.CALL_PHONE","允许程序从非系统拨号器里输入电话号码","7"],["通话权限","android.permission.CALL_PRIVILEGED","允许程序拨打电话，替换系统的拨号器界面","7"],["拍照权限","android.permission.CAMERA","允许访问摄像头进行拍照","3"],["改变组件状态","android.permission.CHANGE_COMPONENT_ENABLED_STATE","改变组件是否启用状态","6"],["改变配置","android.permission.CHANGE_CONFIGURATION","允许当前应用改变配置，如定位","8"],["改变网络状态","android.permission.CHANGE_NETWORK_STATE","改变网络状态如是否能联网","8"],["改变WiFi多播状态","android.permission.CHANGE_WIFI_MULTICAST_STATE","改变WiFi多播状态","3"],["改变WiFi状态","android.permission.CHANGE_WIFI_STATE","改变WiFi状态","6"],["清除应用缓存","android.permission.CLEAR_APP_CACHE","清除应用缓存","8"],["清除用户数据","android.permission.CLEAR_APP_USER_DATA","清除应用的用户数据","8"],["底层访问权限","android.permission.CWJ_GROUP","允许CWJ账户组访问底层信息","3"],["手机优化大师扩展权限","android.permission.CELL_PHONE_MASTER_EX","手机优化大师扩展权限","0"],["控制定位更新","android.permission.CONTROL_LOCATION_UPDATES","允许获得移动网络定位信息改变","8"],["删除缓存文件","android.permission.DELETE_CACHE_FILES","允许应用删除缓存文件","8"],["删除应用","android.permission.DELETE_PACKAGES","允许程序删除应用","9"],["电源管理","android.permission.DEVICE_POWER","允许访问底层电源管理","6"],["应用诊断","android.permission.DIAGNOSTIC","允许程序到RW到诊断资源","0"],["禁用键盘锁","android.permission.DISABLE_KEYGUARD","允许程序禁用键盘锁","9"],["转存系统信息","android.permission.DUMP","允许程序获取系统dump信息从系统服务","9"],["状态栏控制","android.permission.EXPAND_STATUS_BAR","允许程序扩展或收缩状态栏","0"],["工厂测试模式","android.permission.FACTORY_TEST","允许程序运行工厂测试模式","10"],["使用闪光灯","android.permission.FLASHLIGHT","允许访问闪光灯","0"],["强制后退","android.permission.FORCE_BACK","允许程序强制使用back后退按键，无论Activity是否在顶层","8"],["访问账户Gmail列表","android.permission.GET_ACCOUNTS","访问GMail账户列表","3"],["获取应用大小","android.permission.GET_PACKAGE_SIZE","获取应用的文件大小","1"],["获取任务信息","android.permission.GET_TASKS","允许程序获取当前或最近运行的应用","3"],["允许全局搜索","android.permission.GLOBAL_SEARCH","允许程序使用全局搜索功能","1"],["硬件测试","android.permission.HARDWARE_TEST","访问硬件辅助设备，用于硬件测试","1"],["注射事件","android.permission.INJECT_EVENTS","允许访问本程序的底层事件，获取按键、轨迹球的事件流","8"],["安装定位提供","android.permission.INSTALL_LOCATION_PROVIDER","安装定位提供","0"],["安装应用程序","android.permission.INSTALL_PACKAGES","允许程序安装应用","5"],["内部系统窗口","android.permission.INTERNAL_SYSTEM_WINDOW","允许程序打开内部窗口，不对第三方应用程序开放此权限","0"],["访问网络","android.permission.INTERNET","访问网络连接，可能产生GPRS流量","3"],["结束后台进程","android.permission.KILL_BACKGROUND_PROCESSES","允许程序调用killBackgroundProcesses(String).方法结束后台进程","3"],["管理账户","android.permission.MANAGE_ACCOUNTS","允许程序管理AccountManager中的账户列表","1"],["管理程序引用","android.permission.MANAGE_APP_TOKENS","管理创建、摧毁、Z轴顺序，仅用于系统","2"],["高级权限","android.permission.MTWEAK_USER","允许mTweak用户访问高级系统权限","1"],["社区权限","android.permission.MTWEAK_FORUM","允许使用mTweak社区权限","1"],["软格式化","android.permission.MASTER_CLEAR","允许程序执行软格式化，删除系统配置信息","9"],["修改声音设置","android.permission.MODIFY_AUDIO_SETTINGS","修改声音设置信息","1"],["修改电话状态","android.permission.MODIFY_PHONE_STATE","修改电话状态，如飞行模式","7"],["格式化文件系统","android.permission.MOUNT_FORMAT_FILESYSTEMS","格式化可移动文件系统，比如格式化清空SD卡","10"],["挂载文件系统","android.permission.MOUNT_UNMOUNT_FILESYSTEMS","挂载、反挂载外部文件系统","10"],["允许NFC通讯","android.permission.NFC","允许程序执行NFC近距离通讯操作，用于移动支持","1"],["永久Activity","android.permission.PERSISTENT_ACTIVITY","创建一个永久的Activity，该功能标记为将来将被移除","1"],["处理拨出电话","android.permission.PROCESS_OUTGOING_CALLS","允许程序监视，修改或放弃播出电话","10"],["读取日程提醒","android.permission.READ_CALENDAR","允许程序读取用户的日程信息","5"],["读取联系人","android.permission.READ_CONTACTS","允许应用访问联系人通讯录信息","7"],["屏幕截图","android.permission.READ_FRAME_BUFFER","读取帧缓存用于屏幕截图","7"],["读取收藏夹和历史记录","com.android.browser.permission.READ_HISTORY_BOOKMARKS","读取浏览器收藏夹和历史记录","8"],["读取输入状态","android.permission.READ_INPUT_STATE","读取当前键的输入状态，仅用于系统","5"],["读取系统日志","android.permission.READ_LOGS","读取系统底层日志","5"],["读取电话状态","android.permission.READ_PHONE_STATE","访问电话状态","3"],["读取短信内容","android.permission.READ_SMS","读取短信内容","9"],["读取同步设置","android.permission.READ_SYNC_SETTINGS","读取同步设置，读取Google在线同步设置","1"],["读取同步状态","android.permission.READ_SYNC_STATS","读取同步状态，获得Google在线同步状态","1"],["重启设备","android.permission.REBOOT","允许程序重新启动设备","3"],["开机自动允许","android.permission.RECEIVE_BOOT_COMPLETED","允许程序开机自动运行","6"],["接收彩信","android.permission.RECEIVE_MMS","接收彩信","7"],["接收短信","android.permission.RECEIVE_SMS","接收短信","8"],["接收Wap Push","android.permission.RECEIVE_WAP_PUSH","接收WAP PUSH信息","8"],["录音","android.permission.RECORD_AUDIO","录制声音通过手机或耳机的麦克","6"],["排序系统任务","android.permission.REORDER_TASKS","重新排序系统Z轴运行中的任务","5"],["结束系统任务","android.permission.RESTART_PACKAGES","结束任务通过restartPackage(String)方法，该方式将在外来放弃","0"],["发送短信","android.permission.SEND_SMS","发送短信","9"],["设置Activity观察其","android.permission.SET_ACTIVITY_WATCHER","设置Activity观察器一般用于monkey测试","0"],["设置闹铃提醒","com.android.alarm.permission.SET_ALARM","设置闹铃提醒","0"],["设置总是退出","android.permission.SET_ALWAYS_FINISH","设置程序在后台是否总是退出","0"],["设置动画缩放","android.permission.SET_ANIMATION_SCALE","设置全局动画缩放","0"],["设置调试程序","android.permission.SET_DEBUG_APP","设置调试程序，一般用于开发","3"],["设置屏幕方向","android.permission.SET_ORIENTATION","设置屏幕方向为横屏或标准方式显示，不用于普通应用","0"],["设置应用参数","android.permission.SET_PREFERRED_APPLICATIONS","设置应用的参数，已不再工作具体查看addPackageToPreferred(String) 介绍","1"],["设置进程限制","android.permission.SET_PROCESS_LIMIT","允许程序设置最大的进程数量的限制","1"],["设置系统时间","android.permission.SET_TIME","设置系统时间","1"],["设置系统时区","android.permission.SET_TIME_ZONE","设置系统时区","1"],["设置桌面壁纸","android.permission.SET_WALLPAPER","设置桌面壁纸","0"],["设置壁纸建议","android.permission.SET_WALLPAPER_HINTS","设置壁纸建议","0"],["发送永久进程信号","android.permission.SIGNAL_PERSISTENT_PROCESSES","发送一个永久的进程信号","4"],["状态栏控制","android.permission.STATUS_BAR","允许程序打开、关闭、禁用状态栏","3"],["访问订阅内容","android.permission.SUBSCRIBED_FEEDS_READ","访问订阅信息的数据库","3"],["写入订阅内容","android.permission.SUBSCRIBED_FEEDS_WRITE","写入或修改订阅内容的数据库","3"],["显示系统窗口","android.permission.SYSTEM_ALERT_WINDOW","显示系统窗口","7"],["更新设备状态","android.permission.UPDATE_DEVICE_STATS","更新设备状态","7"],["使用证书","android.permission.USE_CREDENTIALS","允许程序请求验证从AccountManager","0"],["使用SIP视频","android.permission.USE_SIP","允许程序使用SIP视频服务","0"],["使用振动","android.permission.VIBRATE","允许振动","0"],["唤醒锁定","android.permission.WAKE_LOCK","允许程序在手机屏幕关闭后后台进程仍然运行","8"],["写入GPRS接入点设置","android.permission.WRITE_APN_SETTINGS","写入网络GPRS接入点设置","3"],["写入日程提醒","android.permission.WRITE_CALENDAR","写入日程，但不可读取","0"],["写入联系人","android.permission.WRITE_CONTACTS","写入联系人，但不可读取","3"],["写入外部存储","android.permission.WRITE_EXTERNAL_STORAGE","允许程序写入外部存储，如SD卡上写文件","2"],["写入Google地图数据","android.permission.WRITE_GSERVICES","允许程序写入Google Map服务数据","1"],["写入收藏夹和历史记录","com.android.browser.permission.WRITE_HISTORY_BOOKMARKS","写入浏览器历史记录或收藏夹，但不可读取","1"],["读写系统敏感设置","android.permission.WRITE_SECURE_SETTINGS","允许程序读写系统安全敏感的设置项","7"],["读写系统设置","android.permission.WRITE_SETTINGS","允许读写系统设置项","3"],["编写短信","android.permission.WRITE_SMS","允许编写短信","9"],["写入在线同步设置","android.permission.WRITE_SYNC_SETTINGS","写入Google在线同步设置","1"]]
api_score=[["Landroid/content/Intent;-><init>","0"],["Landroid/content/ContextWrapper;->sendBroadcast","0"],["Landroid/content/ContextWrapper;->sendOrderedBroadcast","0"],["Landroid/content/ContextWrapper;->sendStickyBroadcast","0"],["Landroid/content/ContextWrapper;->sendStickyOrderedBroadcast","0"],["Landroid/content/ContextWrapper;->startActivity","0"],["Landroid/content/ContextWrapper;->startActivities","0"],["Landroid/net/Uri;->parse(Ljava/lang/String;)","0"],["Landroid/content/ContextWrapper;->openFileInput","0"],["Landroid/content/ContextWrapper;->openFileOutput","0"],["Ljava/io/FileReader;-><init>","0"],["Ljava/io/FileWriter;-><init>","0"],["Ljava/net/URL;-><init>","0"],["Ljava/net/URL;->openConnection","0"],["Ljava/net/URL;->openStream","0"],["Ljava/io/Reader;->read","0"],["Ljava/io/Writer;->write","0"],["Ljava/io/BufferedReader;->read","0"],["Ljava/io/BufferedReader;->readLine","0"],["Ljava/io/BufferedWriter;->write","0"],["Ljava/io/BufferedWriter;->newLine","0"],["Ljava/io/InputStreamReader;->read","0"],["Ljava/io/OutputStreamWriter;->write","0"],["Ljava/io/CharArrayReader;->read","0"],["Ljava/io/CharArrayWriter;->write","0"],["Ljava/io/CharArrayWriter;->writeTo","0"],["Ljava/io/FilterReader;->read","0"],["Ljava/io/FilterWriter;->write","0"],["Ljava/io/StringReader;->read","0"],["Ljava/io/StringWriter;->write","0"],["Ljava/io/PrintWriter;->append","0"],["Ljava/io/PrintWriter;->format","0"],["Ljava/io/PrintWriter;->print","0"],["Ljava/io/PrintWriter;->printf","0"],["Ljava/io/PrintWriter;->println","0"],["Ljava/io/PrintWriter;->write","0"],["Landroid/content/ContextWrapper;->openOrCreateDatabase","0"],["Landroid/database/sqlite/SQLiteDatabase;->openDatabase","0"],["Landroid/database/sqlite/SQLiteDatabase;->openOrCreateDatabase","0"],["Landroid/database/sqlite/SQLiteDatabase;->query","0"],["Landroid/database/sqlite/SQLiteDatabase;->rawQuery","0"],["Landroid/database/sqlite/SQLiteDatabase;->queryWithFactory","0"],["Landroid/database/sqlite/SQLiteDatabase;->rawQueryWithFactory","0"],["Landroid/content/ContentResolver;","0"],["Landroid/telephony/SmsManager;->sendTextMessage","6"],["Landroid/telephony/SmsManager;->sendDataMessage","6"],["Landroid/telephony/SmsManager;->sendMultipartTextMessage","6"],["Landroid/content/pm/PackageManager;->getInstalledApplications","3"],["Landroid/telephony/TelephonyManager;->getDeviceId","3"],["Landroid/telephony/TelephonyManager;->getSubscriberId","5"],["Landroid/telephony/TelephonyManager;->getCallState","5"],["Landroid/telephony/TelephonyManager;->getCellLocation","5"],["Ljava/security/MessageDigest;->getInstance","0"],["Ljava/security/MessageDigest;->update","0"],["Ljava/security/MessageDigest;->digest","0"],["Ljavax/crypto/Cipher;->getInstance","0"],["Ljavax/crypto/spec/SecretKeySpec;-><init>","0"],["Ljavax/crypto/Cipher;->init","0"],["Ljavax/crypto/Cipher;->doFinal","0"],["Landroid/telephony/TelephonyManager;->getLine1Number","5"]]
working_dir = sys.path[0]

parser = argparse.ArgumentParser(description=\
'Repackage apk to Process.')
parser.add_argument('filename', type=str,
                    help='path of APK file')
args = parser.parse_args()
a = apk.APK(args.filename)
apk_name = args.filename.split(".apk")[0].replace("/","_")
os.system("mkdir /tmp/"+apk_name)
dex_file = open("/tmp/"+apk_name+"/classes.dex", 'w')
dex_file.write(a.get_dex())
dex_file.close()

os.system("java -jar smali/baksmali.jar -b -o /tmp/"+apk_name+"/smali /tmp/"+apk_name+"/classes.dex")

permissions=a.permissions
permission_count=len(permissions)
permission_sum = 0
print(args.filename+" 的权限申请情况如下：")
for item_permission in permissions:
	for i in mani_info:
		if item_permission==i[1]:
			permission_sum = permission_sum + int(i[3])	
			print(i[0]+'\t'+i[1]+'\t'+i[2])
print(args.filename+" 的权限申请危险指数是："+str(permission_sum*10/permission_count))






os.system("egrep -r \"http[:s]\" /tmp/"+apk_name+"/smali >/tmp/"+apk_name+"/result.txt")
res_file=open("/tmp/"+apk_name+"/result.txt")
out_put=open("/tmp/"+apk_name+"/result1.txt","w")
pa=re.compile(r"http[s:][:/][^\"^#]+")

for line in res_file:
	if pa.search(line):
		out_put.write(pa.search(line).group()+"\n")
res_file.close()
out_put.close()
os.system("sort /tmp/"+apk_name+"/result1.txt -u >/tmp/"+apk_name+"/url_result.txt")



os.system("rm /tmp/"+apk_name+"/result.txt")
os.system("rm /tmp/"+apk_name+"/result1.txt")

os.system("egrep -r \"[1][0-9]{10}\" /tmp/"+apk_name+"/smali >/tmp/"+apk_name+"/result.txt")

res_file1=open("/tmp/"+apk_name+"/result.txt")
out_put1=open("/tmp/"+apk_name+"/result1.txt","w")
pa1=re.compile(r"1[0-9]{10}")

for line in res_file1:
	if pa1.search(line):
		out_put1.write(pa1.search(line).group()+"\n")
out_put1.close()
os.system("sort /tmp/"+apk_name+"/result1.txt -u >/tmp/"+apk_name+"/num_result.txt")

api_file=open("config/default_api_collection")
api_result=open("/tmp/"+apk_name+"/api.txt","w")
api_result.close()
for line in api_file:
	if not line.startswith("#") and line.find("L")>-1:
		os.system("egrep -n -r \""+line.split("\n")[0]+"\" /tmp/"+apk_name+"/smali |wc -l >>/tmp/"+apk_name+"/api.txt")
		os.system("echo  -n \""+line+"\" >>/tmp/"+apk_name+"/api.txt")
tmpf=open("/tmp/"+apk_name+"/api.txt")
tmpf1=open("/tmp/"+apk_name+"/api_result_tmp.txt","w")
tmpf1.write(tmpf.read().replace("\nL","\tL"))
tmpf.close()
tmpf1.close()

api_result=open("/tmp/"+apk_name+"/api_result_tmp.txt")
risk_score = 0
print("--------------------------------------------------           ")
print(args.filename+" 的二进制代码中，危险API调用情况如下 :")
for line in api_result:
	num=line.split("\t")[0]
	api=line.split("\t")[1]
	for api_info in api_score:
		if api_info[0]==api.split("\n")[0] and not num=="0":
			risk_score=risk_score+int(api_info[1])
			if int(api_info[1])!=0:
				print(api.split('\n')[0]+"\t"+api_info[1])
print( args.filename+" 的二进制代码API 调用危险指数是:      "+str(risk_score))


