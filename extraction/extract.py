from ppadb.client import Client
import shutil
import os

client = Client(host="127.0.0.1", port=5037)
devices = client.devices()

for i, device in enumerate(devices):
    print(f"{i}: {device.serial}")
    
i = int(input("Select a device: "))
device = devices[i]

files = [
    "com.android.providers.telephony/databases/mmssms.db", 
    "com.android.providers.contacts/databases/calllog.db", 
    "com.android.providers.contacts/databases/contacts2.db", 
    "com.google.android.apps.maps/databases/gmm_storage.db"
]

def check_root_status(device):
    try:
        result = device.shell("su 0 id -u")
        if "0" in result:
            return True
        else:
            device.root()
            return False
    except Exception as e:
        error_message = str(e).lower()
        if "su: not found" in error_message or "permission denied" in error_message:
            return False
        else:
            print(f"An unexpected error occurred: {e}")
            return False
     
os.makedirs("output\\device", exist_ok=True)
os.makedirs("output\\device\\data", exist_ok=True)
os.makedirs("output\\device\\storage", exist_ok=True)

os.system(f"adb\\adb shell content query --uri content://sms > output/device/data/sms.csv")
os.system(f"adb\\adb shell content query --uri content://call_log/calls > output/device/data/call_logs.csv")
os.system(f"adb\\adb shell content query --uri content://contacts/phones/ > output/device/data/contacts.csv")

if(check_root_status(device)):
    try:
        for file in files:
            os.system(f"adb\\adb pull /data/data/{file} output/device/data")
            #device.shell(f"cp /data/data/{file} /storage/emulated/0/data")
    except Exception as e:
        print(e)

os.system("adb\\adb pull storage/emulated/0/ output/device/storage")

shutil.make_archive('output/device', 'zip', 'output/device/') 