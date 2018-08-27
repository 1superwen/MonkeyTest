import os
import types

import io , sys


#connectfile = os.popen('adb install C:\\Users\\lenovo\\Desktop\\sany_serialport.apk')
#connectfile1 = os.popen('adb uninstall com.aerozhonghuan.serialporttool')
connectfile = os.popen('aapt dump badging C:\\Users\\lenovo\\Desktop\\sany_serialport.apk','r',encoding='utf-8')
#aapt v[ersion]
#connectfile = os.popen('aapt v[ersion]','r')

list = connectfile.read()
print(list)
'''
#list1 = connectfile1.read()
for line in list.splitlines():
    #print (line)
    if 'Success' in line:
        print('成功')
#print(list)
#print(list1)
#types(list)
'''
