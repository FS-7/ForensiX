import os
from datetime import datetime

def insertSMS(adb_loc):
    address = "+1111111111"
    messages = [
        { "id": 1, "sender": "+1111111111", "timestamp": "2025-11-19T09:00:01Z", "text": "Morning Bob! You awake?" },
        { "id": 2, "sender": "Me", "timestamp": "2025-11-19T09:00:27Z", "text": "Barely. Need coffee first." },
        { "id": 3, "sender": "+1111111111", "timestamp": "2025-11-19T09:01:03Z", "text": "Same. Rough night?" },
        { "id": 4, "sender": "Me", "timestamp": "2025-11-19T09:01:40Z", "text": "I stayed up fixing that server issue." },
        { "id": 5, "sender": "+1111111111", "timestamp": "2025-11-19T09:02:11Z", "text": "Oh wow. Did it finally work?" },
        { "id": 6, "sender": "Me", "timestamp": "2025-11-19T09:02:48Z", "text": "Yeah. Took forever though." },
        { "id": 7, "sender": "+1111111111", "timestamp": "2025-11-19T09:03:20Z", "text": "You're a hero lol." },
        { "id": 8, "sender": "Me", "timestamp": "2025-11-19T09:03:55Z", "text": "I accept praise in the form of pastries." },
        { "id": 9, "sender": "+1111111111", "timestamp": "2025-11-19T09:04:32Z", "text": "I'll see if there's donuts in the break room." },
        { "id": 10, "sender": "Me", "timestamp": "2025-11-19T09:04:59Z", "text": "Bless you." },
    ]
    
    for message in messages:
        print(str(message["text"]).replace(" ", "\\ "))
    
    print(os.system(f"{adb_loc}\\adb devices"))
    for i in messages:
        type = 2 if i["sender"] == "Me" else 1
        print(
            os.system(
                f"""
                {adb_loc}\\adb shell "content insert --uri content://sms --bind address:s:{address} --bind date:l:{int(datetime.strptime(i["timestamp"], "%Y-%m-%dT%H:%M:%SZ").timestamp())*1000} --bind body:s:"{i["text"]}" --bind type:i:{type}"
                """
            )
        )
    
adb_loc = input("ADB Location: ")
insertSMS(adb_loc)