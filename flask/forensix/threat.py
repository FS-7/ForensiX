from forensix.shared import *
from forensix.parser import parseContactsCSV, parseSMS_SQL, parseLogsSQL, scan_files
import zipfile

content = []

def init(id):
    print("Initializing Evidence Database")
    os.makedirs(EXT_DB_LOCATION, exist_ok=True)

    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS MESSAGES;")
        cur.execute("DROP TABLE IF EXISTS CALL_LOGS;")
        cur.execute("DROP TABLE IF EXISTS CONTACTS;")
        cur.execute("DROP TABLE IF EXISTS FILES;")
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS MESSAGES(
                ADDRESS VARCHAR(100) NOT NULL,
                BODY VARCHAR(512) NOT NULL,
                DATE_SENT DATETIME NOT NULL,
                DATE_RECEIVED DATETIME NOT NULL,
                TYPE VARCHAR(10) NOT NULL
            );
            '''
        )
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS CALL_LOGS(
                NUMBER VARCHAR(10) NOT NULL,
                DATE DATETIME NOT NULL,
                DURATION INT NOT NULL,
                TYPE VARCHAR(10) NOT NULL
            );
            '''
        ) 
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS CONTACTS(
                NAME VARCHAR(50) NOT NULL,
                NUMBER VARCHAR(10) NOT NULL,
                GROUP_ID INT NOT NULL,
                EMAIL VARCHAR(255) NOT NULL
            );
            '''
        )
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS FILES(
                PATH VARCHAR(260) NOT NULL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                DIRECTORY VARCHAR(255) NOT NULL,
                SIZE INT NOT NULL,
                C_DATETIME DATETIME NOT NULL,
                M_DATETIME DATETIME NOT NULL,
                EXT VARCHAR(5) NOT NULL
            );
            '''    
        ) 
        conn.commit()
        cur.close()
        conn.close()
        print("Evidence Database Created")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    except:
        print(e)

def extract(filename, id):
    print("Extracting Data")
    
    zipfile_path = f"{UPLOAD_FOLDER}/{filename}"
    os.makedirs(f"{EXTRACTED_FILES_LOCATION}/{id}", exist_ok=True)
    
    try:
        with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
            zip_ref.extractall(f"{EXTRACTED_FILES_LOCATION}/{id}")
        print("Data Extracted") 

    except zipfile.BadZipFile:
        print(f"Error: '{zipfile_path}' is not a valid zip file.")
    except FileNotFoundError:
        print(f"Error: Zip file '{zipfile_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    return

def add_to_database(id):
    print("Adding evidence data into database")
    try:
        sms = parseSMS_SQL(f"{EXTRACTED_FILES_LOCATION}/{id}/data/")
        call_logs = parseLogsSQL(f"{EXTRACTED_FILES_LOCATION}/{id}/data/")
        contacts = parseContactsCSV(f"{EXTRACTED_FILES_LOCATION}/{id}/data/")
        files = scan_files(f"{EXTRACTED_FILES_LOCATION}/{id}/storage/", id)
        
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        
        cur.executemany(
            '''
                INSERT INTO MESSAGES(ADDRESS, BODY, DATE_SENT, DATE_RECEIVED, TYPE) VALUES(?, ?, ?, ?, ?);
            ''',
            sms.values
        )
        conn.commit()
        
        cur.executemany(
            '''
                INSERT INTO CALL_LOGS(NUMBER, DATE, DURATION, TYPE) VALUES(?, ?, ?, ?);
            ''',
            call_logs.values
        )
        conn.commit()
        
        cur.executemany(
            '''
                INSERT INTO CONTACTS(NAME, NUMBER, GROUP_ID, EMAIL) VALUES(?, ?, ?, ?);
            ''',
            contacts.values
        )
        conn.commit()
        
        for file in files:
            cur.execute(
            '''
                INSERT INTO FILES(PATH, NAME, DIRECTORY, SIZE, C_DATETIME, M_DATETIME, EXT) VALUES(?, ?, ?, ?, ?, ?, ?);
            ''',
            [file['path'], file['name'], file['parent'], file['size'], file['ctime_readable'], file['mtime_readable'], file['ext']]
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Added evidence data into database")
        
    except Exception as e:
        print(e)
    return

def extraction(last_id, filename, case_id):
    init(last_id)
    extract(filename, last_id)
    add_to_database(last_id)
    analyze(last_id, case_id)
    send_data_to_nlp(case_id, last_id)
    print("Data Extracted and inserted into database")

def analyze(id, case_id):
    document = {
        "Case_id": case_id, "Evidence": id, 
        "Messages": analyze_text_messages(id),
        "Contacts": analyze_contacts(id),
        "Call_logs": analyze_call_logs(id),
        "Files": None,#analyze_files(id),
        "Images": None,#analyze_images(id, case_id),
        "Audios": None,#analyze_audios(id)
    }
    try:
        client["Evidence_report"].insert_one(document)
    except Exception as e:
        print(e)
        
def analyze_text_messages(id):
    print("Analyzing Text messages")
    
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        results = cur.execute(
            '''
                SELECT * FROM MESSAGES;
            '''
        ).fetchall()
        
        candidate_labels = [
            "Normal", "Threat", "Identity Attack", "Sexually Explicit", "Extremism", "Scam"
        ]
        
        output = []
        for i in set(r[0] for r in results):
            temp = []
            for res in results:
                if res[0] == i:
                    temp.append({"Content": res[1], "DateSent": res[2], "DateReceived": res[3], "Type": res[4]})
            output.append({"Number": i, "Messages": temp, "Tags": []})
        
        for k in output:
            msg = ""
            for i in k["Messages"]:
                msg += ("Sender: " if i["Type"] == "Sent" else "Receiver: ") + i["Content"] + " "
                
            messages = [{
                "role":"user", "content": f"""Text: {msg}. Query: In one word classify the text into one of the following categories: {', '.join(candidate_labels)}. No explaination."""
            }]
            
            k["Tags"].append(ask_gemma(messages, 64))
            
        print("Done")
        return output
        
    except Exception as e:
        print(e)
    return 
    
def analyze_contacts(id):
    print("Analyzing Contacts")
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        results = cur.execute(
            '''
                SELECT * FROM CONTACTS;
            '''
        ).fetchall()
        
        output = [] 
        for i in set(r[2] for r in results):
            temp = []
            for res in results:    
                if i==res[2]:
                    temp.append({"Name": res[0], "Number": res[1], "Email": res[3]})
            output.append({ "Group": i, "Contacts": temp, "Tags": []})
            
        print("Analyzed Contacts")
        return output
    except Exception as e:
        print(e)
    return 

def analyze_call_logs(id):
    print("Analyzing Call Logs")
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        results = cur.execute(
            '''
                SELECT * FROM CALL_LOGS;
            '''
        ).fetchall()
        
        output = []
        for i in set(r[0] for r in results):
            temp = []
            for res in results:
                if i == res[0]:
                    temp.append({"Datetime": res[1], "Duration": res[2], "Type": res[3]})
            output.append({"Number": i, "Call_logs": temp, "Tags": []})
        
        print("Analyzed Call Logs")
        return output
    except Exception as e:
        print(e)
    return 

def analyze_files(id):
    try: 
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        results = cur.execute("SELECT * FROM FILES;").fetchall()
        
        output = []
        for i in results:
            output.append({"Path": i[0], "Name": i[1], "Directory": i[2], "Size": i[3], "C_TIME": i[4], "M_TIME": i[5], "EXT": i[6], "Summary": ""})
        return output

    except Exception as e:
        print(e)
    except:
        print("Error") 
    return

def analyze_images(id, case_id):
    print("Analyzing Images")
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        
        output = []
        results = cur.execute('SELECT PATH FROM FILES WHERE EXT IN (".jpg", ".jpeg", ".png");').fetchall()
        for res in results:
            output.append((res[0], ask_fr_get_enc(res[0], id, case_id)))
            
        #similarities = ask_fr_compare_list(, encodings[1])
        print("Analyzed Images")
        return output
       
    except Exception as e:
        print(e)
    return
 
def analyze_audios(id):
    print("Analyzing Audio files")
    
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        audios = cur.execute(
            '''
                SELECT path FROM FILES WHERE EXT='mp3' or EXT='m4a' or EXT='obb' or EXT='mpeg';
            '''
        ).fetchall()
        print(audios)
        results = defaultdict(list)
        for audio_path in audios:
            results[audio_path] = ask_whisperx(audio_path)
        
        print("Analyzed Audio files")
        return results
    
    except Exception as e:
        print(e)
    return 
    
def send_data_to_nlp(case_id, id):
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        messages = cur.execute("SELECT * FROM MESSAGES;").fetchall()
        logs = cur.execute("SELECT * FROM CALL_LOGS;").fetchall()
        contacts = cur.execute("SELECT * FROM CONTACTS;").fetchall()
        files = cur.execute("SELECT * FROM FILES;").fetchall()
        
        for sms in messages:
            content.append(f"Case ID {case_id}, Evidence Number {id}: Message {'to' if sms[4] == 'Sent' else 'from'} {sms[0]} ({sms[4]}) on {sms[3]}: {sms[1]}".lower()) 
        
        for log in logs:
            content.append(f"Case: {case_id}, Evidence: {id}: Call log {log[3]} call, {log[0]} on {log[1]} lasting {log[2]}.".lower())
        
        for contact in contacts:
            content.append(f"Case: {case_id}, Evidence: {id}: Contact: {contact[0]}. Phone number: {contact[1]}{"" if contact[3] == "No Email" else f", Email: {contact[3]}."}.".lower(),
        )
            
        for file in files:
            content.append(f"")
        
        print('\n'.join(content))
    
    except Exception as e:
        print(e)
    except:
        print("Error")
    

def generate_query(query):
    try:
        messages = f"""
Context: You are a SQL generator. 
Given the following database schema:
Table: Messages
Columns: id (integer) - Address (text) - Date Sent (date) - Date Received (date) - Type (text) - Body (text)
Table: Contacts
Columns: id (integer) - name (text) - number (number) - email (text)
Table: Call Logs
Columns: id (integer) - Owner (text) - Date Time (number) - Duration (number) - Type (text)
Table: Files
Columns: - path (text) - name (text) - parent (text) - size (number) - datetime (datetime) - ext (text) alias type
Convert the following user question into a correct, safe SQL query. 
Return only SQL, no explanations.
Query: {query}
        """
        return ask_gemma(messages, 128)
    
    except Exception as e:
        print(e)
        
    return 

def run_query(query, id):
    query = query[6:-3]
    if str(query).lower().startswith("select"):
        return
    conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
    cur = conn.cursor()
    output = cur.execute(
        query,
        []
    ).fetchall()
    print(output)
    return output
    
def convert_to_nlp(results):
    messages = f"""
Structure this data into a table
Data: {results}
No Explaination
    """
    print(len(results)*len(results[0]))
    return ask_gemma(messages, 500)
    