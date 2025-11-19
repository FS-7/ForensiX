@echo off

SET PWD=""
FOR /F "tokens=*" %%a in ('cd') do SET PWD=%%a

mkdir Data

SET ADB_LOCATION="C:\Users\FS\Desktop\platform-tools"
cd /D %ADB_LOCATION%

SET CALL_RECORDING_LOCATION="/sdcard/CallRecordings"
SET IMAGES_LOCATION="/sdcard/DCIM"
SET ALL_FILES_LOCATION="/sdcard"

SET /P CALL_RECORDING_LOCATION="Enter Call Recording Location: "
SET /P IMAGES_LOCATION="Enter Images Location: "
SET /P ALL_FILES_LOCATION="Enter All Files Location: "

adb devices
adb root

adb shell "content query --uri content://sms" > "%PWD%\Data\sms.csv" 
adb shell "content query --uri content://call_log/calls" > %PWD%"\Data\call_logs.csv"
adb shell "content query --uri content://contacts/phones/" > %PWD%"\Data\contacts.csv"

adb pull "/data/data/com.android.providers.telephony/databases/mmssms.db" %PWD%"\Data\sms.db" || False
adb pull "/data/data/com.android.providers.contacts/databases/calllog.db" %PWD%"\Data\call_log.db" || False
adb pull "/data/data/com.android.providers.contacts/databases/contacts2.db" %PWD%"\Data\contacts.db" || False
adb pull "/data/data/com.google.android.apps.maps/databases/gmm_storage.db" %PWD%"\Data\gps.db" || False

adb pull %CALL_RECORDING_LOCATION% "\Data\CallRecordings"
adb pull %IMAGES_LOCATION% "\Data\DCIM"
adb pull %ALL_FILES_LOCATION% "\Data\"

cd /D %PWD%
