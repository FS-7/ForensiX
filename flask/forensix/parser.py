from forensix.shared import *
from datetime import datetime
from pathlib import Path

import pandas as pd 
import re, sqlite3

def parseSMS_CSV(loc):
    try:
        sms = pd.read_csv(loc+"sms.csv", header=None)
        if sms.iat[0, 0] == "No result found.":
            return pd.DataFrame()
        sms = sms.loc[:, [2, 12, 4, 5, 9, 18]]
        sms.columns = ["Address", "Body", "Date Sent", "Date Received", "Type", "Seen"]
        for i in sms[1:]:
            sms[i] = sms[i].transform(lambda x: x.split("=")[1])
        
        sms["Address"] = sms["Address"].replace(regex="^\\+1", value="")
        sms["Date Sent"] = sms["Date Sent"].transform(lambda x: datetime.fromtimestamp(int(x)//1000).isoformat())
        sms["Type"] = sms["Type"].transform(lambda x: "Received" if x == "1" else "Sent")
        sms["Seen"] = sms["Seen"].transform(lambda x: "True" if x == "1" else "False")
    
        for i in sms.index:
            sms.at[i, "Date Received"] = sms.at[i, "Date Sent"] if sms.at[i, "Type"] == "Sent" else datetime.fromtimestamp(int(sms.at[i, "Date Received"])//1000).isoformat()
        
        return sms
    
    except Exception as e:
        print(f"Error: {e}")
    except:
        print("Unknown Error")
        
def parseLogsCSV(loc):
    try:
        call_logs = pd.read_csv(loc+"call_logs.csv", header=None)
        if call_logs.iat[0, 0] == "No result found.":
            return pd.DataFrame()
        
        call_logs = call_logs.iloc[: , [9, 24, 1, 26]]
        call_logs.columns = ["Number", "Time", "Duration", "Type"]

        for i in call_logs:
            call_logs[i] = call_logs[i].transform(lambda x: x.split("=")[1])
            
        call_logs["Time"] = call_logs["Time"].transform(lambda x: datetime.fromtimestamp(int(x)//1000).strftime("%d-%m-%Y %H:%M:%S"))
        call_logs["Type"] = call_logs["Type"].transform(lambda x: "INCOMING" if x == "1" else "OUTGOING" if x == "2" else "MISSED" if x == "3" else "REJECTED")

        return call_logs
    
    except Exception as e:
        print(f"Error: {e}")
    except:
        print("Unknown Error")
        
def parseContactsCSV(loc):
    try:
        contacts = pd.read_csv(loc+"contacts.csv", header=None)
        if contacts.iat[0, 0] == "No result found." or contacts.empty:
            return pd.DataFrame()
        contacts = contacts.iloc[:, [16, 1, 2, 8]]
        contacts.columns = ["Name", "Number", "Group", "Email"]

        for i in contacts:
            contacts[i] = contacts[i].transform(lambda x: x.split("=")[1])
            
        contacts["Email"] = contacts["Email"].transform(lambda x: "No Email" if x == "NULL" else x)
        contacts["Number"] = contacts["Number"].transform(lambda x: re.sub(r'[^0-9]', '', x)[-10:])

        return contacts
    
    except pd.errors.EmptyDataError as e:
        print("Khali hai", e)
    except Exception as e:
        print(f"Error: {e}")
    except:
        print("Unknown Error")

def parseSMS_SQL(loc):
    sms = sqlite3.connect(loc + "mmssms.db")
    sms_cursor = sms.cursor()

    sms_documents = pd.DataFrame(columns = ["Address", "Body", "Date Sent", "Date Received", "Type"])
    for i, c in enumerate(sms_cursor.execute("SELECT * FROM SMS").fetchall()):
        sms_documents.loc[i] = [ c[2], c[12], c[5] if c[9] == 1 else int(c[4]), int(c[4]), "Received" if c[9] == 1 else "Sent" ]

    return sms_documents
    
def parseLogsSQL(loc):    
    call_logs = sqlite3.connect(loc + "calllog.db")
    call_logs_cursor = call_logs.cursor()

    call_log_documents = pd.DataFrame(columns=[["Number", "Time", "Duration", "Type"]])
    for i, c in enumerate(call_logs_cursor.execute("SELECT * FROM CALLS;").fetchall()):
        call_log_documents.loc[i] = [ c[1], int(c[5]), c[6], "INCOMING" if c[8]==1 else "OUTGOING" if c[8] == 2 else "MISSED" if c[8] == 3 else "REJECTED"]
    
    return call_log_documents
    
def scan_files(root, id):
    entries = []
    for p in Path(root).rglob("*"):
        if p.is_file():
            stat = p.stat()
            entries.append({
                "path": str(p).removeprefix(f"..\\files\\files\\{id}\\storage\\0"),
                "name": p.name,
                "parent": str(p.parent),
                "size": stat.st_size,
                "ctime_readable": int(stat.st_birthtime)*1000,
                "mtime_readable": int(stat.st_mtime)*1000,
                "ext": p.suffix.lower(),
            })
    return entries
                