from forensix.shared import *
from datetime import datetime
from langchain_core.documents import Document
from sqlite3 import connect
import re
import pandas as pd
    
parser = Blueprint('parser', __name__, url_prefix='/parser')

loc = os.getenv('DATA')

def parseCSV():
    try:
        sms = pd.read_csv(loc+"sms.csv", header=None)
        sms = sms.loc[:, [2, 4, 5, 9, 12, 18]]
        sms.columns = ["Address", "Date Sent", "Date Received", "Type", "Body", "Seen"]
        for i in sms[1:]:
            sms[i] = sms[i].transform(lambda x: x.split("=")[1])
        
        sms["Address"] = sms["Address"].replace(regex="^\\+1", value="")
        sms["Date Sent"] = sms["Date Sent"].transform(lambda x: datetime.fromtimestamp(int(x)//1000).strftime("%d-%m-%Y %H:%M:%S"))
        sms["Type"] = sms["Type"].transform(lambda x: "Received" if x == "1" else "Sent")
        sms["Seen"] = sms["Seen"].transform(lambda x: "True" if x == "1" else "False")
    
        for i in sms.index:
            sms.at[i, "Date Received"] = sms.at[i, "Date Sent"] if sms.at[i, "Type"] == "Sent" else datetime.fromtimestamp(int(sms.at[i, "Date Received"])//1000).strftime("%d-%m-%Y %H:%M:%S")
        
        sms_documents = []
        for i in sms.index:
            sms_documents.append(
                Document(
                    page_content=sms.at[i, "Body"],
                    metadata={
                        "Sender": sms.at[i, "Address"],
                        "Date Time Sent": sms.at[i, "Date Sent"],
                        "Date Time Received": sms.at[i, "Date Received"],
                        "Type": sms.at[i, "Type"],
                        "Seen": sms.at[i, "Seen"]
                    }
                )
            )
        
        print(sms_documents)
        
    except Exception as e:
        print(f"Error: {e}")
    except:
        print("Unknown Error")
        
    try:
        call_logs = pd.read_csv(loc+"call_logs.csv", header=None)
        call_logs = call_logs.iloc[: , [9, 32, 24, 1, 26, 10]]
        call_logs.columns = ["Number", "Owner", "Time", "Duration", "Type", "CountryISO",]

        for i in call_logs:
            call_logs[i] = call_logs[i].transform(lambda x: x.split("=")[1])
            
        call_logs["Time"] = call_logs["Time"].transform(lambda x: datetime.fromtimestamp(int(x)//1000).strftime("%d-%m-%Y %H:%M:%S"))
        call_logs["Type"] = call_logs["Type"].transform(lambda x: "INCOMING" if x == "1" else "OUTGOING" if x == "2" else "MISSED" if x == "3" else "REJECTED")

        call_logs_documents = []
        for c in call_logs.index:
            call_logs_documents.append(
                Document(
                    page_content="",
                    metadata={
                        "Number": call_logs.at[c, "Number"],
                        "Owner": call_logs.at[c, "Owner"],
                        "Time": call_logs.at[c, "Time"],
                        "Duration": call_logs.at[c, "Duration"],
                        "Type": call_logs.at[c, "Type"],
                        "CountryISO": call_logs.at[c, "CountryISO"],
                    }
                )
            )
            
        print(call_logs_documents)
        
    except Exception as e:
        print(f"Error: {e}")
    except:
        print("Unknown Error")
        
    try:
        contacts = pd.read_csv(loc+"contacts.csv", header=None)
        contacts = contacts.iloc[:, [16, 1, 2, 8]]
        contacts.columns = ["Name", "Number", "Group", "Email"]

        for i in contacts:
            contacts[i] = contacts[i].transform(lambda x: x.split("=")[1])
            
        contacts["Email"] = contacts["Email"].transform(lambda x: "No Email" if x == "NULL" else x)
        contacts["Number"] = contacts["Number"].transform(lambda x: re.sub(r'[^0-9]', '', x)[-10:])

        contacts_documents = []
        for c in contacts.index:
            contacts_documents.append(
                Document(
                    page_content="",
                    metadata={
                        "Name": contacts.at[c, "Name"],
                        "Number": contacts.at[c, "Number"],
                        "Group": contacts.at[c, "Group"],
                        "Email": contacts.at[c, "Email"],
                    }
                )
            )
        
        print(contacts_documents)
        
    except Exception as e:
        print(f"Error: {e}")
    except:
        print("Unknown Error")
        
def parseSQL():
    loc = "./Data/"
    sms = connect(loc + "sms.db")
    contacts = connect(loc + "contacts2.db")
    call_logs = connect(loc + "call_log.db")

    sms_cursor = sms.cursor()
    sms_documents = []
    for c in sms_cursor.execute("SELECT * FROM SMS"):
        sms_documents.append(
            Document(
                page_content=c[12],
                metadata={
                    "Sender": c[2],
                    "Date Time Sent": datetime.fromtimestamp(int(c[5])/1000).strftime("%d-%m-%Y, %H:%M:%S") if c[9] == 1 else datetime.fromtimestamp(int(c[4])/1000).strftime("%d-%m-%Y, %H:%M:%S"),
                    "Date Time Received": datetime.fromtimestamp(int(c[4])/1000).strftime("%d-%m-%Y, %H:%M:%S"),
                    "Type": "Received" if c[9] == 1 else "Sent",
                    "Seen": "True" if c[18] == 1 else "False"
                }
            )
        )
        
    call_logs_cursor = call_logs.cursor()
    call_logs_documents = []
    for c in call_logs_cursor.execute("SELECT * FROM CALLS"):
        call_logs_documents.append(
            Document(
                page_content="",
                metadata={
                    "Number": c[1],
                    "Owner": c[12],
                    "Time": datetime.fromtimestamp(int(c[5])//1000).strftime("%d-%m-%Y %H:%M:%S"),
                    "Duration": c[6],
                    "Type": "INCOMING" if c[8]==1 else "OUTGOING" if c[8] == 2 else "MISSED" if c[8] == 3 else "REJECTED",
                    "CountryISO": c[19],
                }
            )
        )
        
    for d in sms_documents:
        print(d)
        
    for d in call_logs_documents:
        print(d)
        