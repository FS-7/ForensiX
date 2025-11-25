@echo off

set SEVENZIP_PATH="C:\Program Files\7-Zip\7z.exe"

SET PWD=""
FOR /F "tokens=*" %%a in ('cd') do SET PWD=%%a

SET ADB_LOCATION="D:\ForensiX\platform-tools"
cd /D %ADB_LOCATION%

SET DEVICE="/storage/emulated/0"
SET CALL_RECORDING_LOCATION="%DEVICE%/CallRecordings"
SET IMAGES_LOCATION="%DEVICE%/DCIM"

SET /P CALL_RECORDING_LOCATION="Enter Call Recording Location: "
SET /P IMAGES_LOCATION="Enter Images Location: "

adb devices
adb root

adb shell "cd %DEVICE%"
adb shell "mkdir data -p"
adb shell "cd data"

SET ROOT=%errorlevel%
if %ROOT% == 0 (
    adb shell "cp /data/data/com.android.providers.telephony/databases/mmssms.db %DEVICE%/data/sms.db"
    adb shell "cp /data/data/com.android.providers.contacts/databases/calllog.db %DEVICE%/data/call_log.db"
    adb shell "cp /data/data/com.android.providers.contacts/databases/contacts2.db %DEVICE%/data/contacts.db"
    adb shell "cp /data/data/com.google.android.apps.maps/databases/gmm_storage.db %DEVICE%/data/gps.db"
)

adb shell "content query --uri content://sms > %DEVICE%/data/sms.csv"
adb shell "content query --uri content://call_log/calls > %DEVICE%/data/call_logs.csv"
adb shell "content query --uri content://contacts/phones/ > %DEVICE%/data/contacts.csv"

mkdir -p "output"
adb pull "%DEVICE%/" "%PWD%/output"

cd /D %PWD%
%SEVENZIP_PATH% a -tzip "device.zip" "%PWD%/output/0/*"