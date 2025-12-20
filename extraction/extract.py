from ppadb.client import Client
import shutil
import os

client = Client(host="127.0.0.1", port=5037)
devices = client.devices()

for i, device in enumerate(devices):
    print(f"{i}: {device.serial}")
    
i = int(input("Select a device: "))
device = devices[i]

device.shell("mkdir /storage/emulated/0/data")

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
        
if(check_root_status(device)):
    try:
        for file in files:
            device.shell(f"cp /data/data/{file} /storage/emulated/0/data")
    except Exception as e:
        print(e)

device.shell("content query --uri content://sms > /storage/emulated/0/data/sms.csv")
device.shell("content query --uri content://call_log/calls > /storage/emulated/0/data/call_logs.csv")
device.shell("content query --uri content://contacts/phones/ > /storage/emulated/0/data/contacts.csv")

os.makedirs("output", exist_ok=True)
os.system("adb\\adb pull storage/emulated/0/ output/device/")

shutil.make_archive('output/zip/device', 'zip', 'output/device/0') 