from forensix.shared import *
from forensix.parser import parseContactsCSV, parseSMS_SQL, parseLogsSQL, scan_files
import zipfile

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
    print("Data Extracted and inserted into database")

def analyze(id, case_id):
    images = analyze_images(case_id, id)
    files = analyze_text(case_id, id) + analyze_pdf(case_id, id) + analyze_audios(case_id, id) + images
    document = {
        "Case_id": case_id, "Evidence": id, 
        "Messages": analyze_text_messages(case_id, id),
        "Contacts": analyze_contacts(case_id, id),
        "Call_logs": analyze_call_logs(case_id, id),
        "Files": files,    
        "Images": images,
    }
    try:
        report.insert_one(document)
    except Exception as e:
        print(e)
        
def analyze_text_messages(case_id, id):
    print("Analyzing Text messages")
    
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        results = cur.execute(
            '''
                SELECT * FROM MESSAGES;
            '''
        ).fetchall()
        
        for r in results:
            documents.insert_one({
                "page_content": f"Case ID: {case_id}, Evidence Number: {id}; Message {'to' if r[4] == 'Sent' else 'from'} {r[0]} {r[4]} on {datetime.fromtimestamp(int(r[3]) // 1000).isoformat()}: {r[1]}.".lower(), 
                "metadata": {
                    "Case ID": case_id,
                    "Evidence": id,
                    "Number": r[0],
                    "Message": r[1],
                    "Datetime Sent": r[2],
                    "Datetime Received": r[3],
                    "Type": r[4],
                }
            })
        
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
        
            k["Tags"].append(ask_gemma(messages, 10))
        
            
        print("Done")
        return output
        
    except Exception as e:
        print(e)
    return 
    
def analyze_contacts(case_id, id):
    print("Analyzing Contacts")
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        results = cur.execute(
            '''
                SELECT * FROM CONTACTS;
            '''
        ).fetchall()
        
        for r in results:
            documents.insert_one({
                "page_content": f"Case ID: {case_id}, Evidence Number: {id}; Contact: {r[0]}, Phone number: {r[1]}, Email: {r[3]}.".lower(),
                "metadata": {
                    "Case ID": case_id,
                    "Evidence": id,
                    "Name": r[0],
                    "Number": r[1],
                    "Group": r[2],
                    "Email": r[3],
                }
            })
        
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

def analyze_call_logs(case_id, id):
    print("Analyzing Call Logs")
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        results = cur.execute(
            '''
                SELECT * FROM CALL_LOGS;
            '''
        ).fetchall()
        
        for r in results:
            documents.insert_one({
                "page_content": f"Case ID: {case_id}, Evidence Number: {id}; Call log: {r[3]} call, {r[0]} on {datetime.fromtimestamp(int(r[1]) // 1000).isoformat()} lasting {r[2]} seconds.".lower(),
                "metadata": {
                    "Case ID": case_id,
                    "Evidence": id,
                    "Number": r[0],
                    "Date": r[1],
                    "Duration": r[2],
                    "Type": r[3],
                }
            })
        
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

def analyze_pdf(case_id, id):
    try: 
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        results = cur.execute("SELECT * FROM FILES WHERE EXT='.pdf';").fetchall()
        
        output = []
        for i in results:
            content = ""
            reader = PdfReader(f"..\\files\\files\\{id}\\storage\\0{i[0]}")
            for page in reader.pages:
                content += page.extract_text()
            
            output.append({"Path": i[0], "Name": i[1], "Directory": i[2], "Size": i[3], "C_TIME": i[4], "M_TIME": i[5], "EXT": i[6], "CONTENT": content})
            documents.insert_one({
                "page_content": f"Case ID: {case_id}, Evidence Number: {id}; File, Type: PDF, Path: {i[0]}, Size: {i[3]}, Creation Time: {datetime(int(i[4]) // 1000).isoformat(sep=" ")}, Modified Time: {datetime(int(i[5]) // 1000).isoformat(sep=" ")} Content: {content}",
                "metadata": {   
                    "Case ID": case_id,
                    "Evidence": id,
                    "Path": i[0], 
                    "Name": i[1], 
                    "Directory": i[2], 
                    "Size": i[3],
                    "C_TIME": i[4], 
                    "M_TIME": i[5], 
                    "EXT": i[6]
                }
            })
        
        return output

    except Exception as e:
        print(e)
    except:
        print("Error") 
    return

def analyze_text(case_id, id):
    try: 
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        results = cur.execute("SELECT * FROM FILES WHERE EXT='.txt';").fetchall()
        
        output = []
        for i in results:
            content = ""
            with open(f"..\\files\\files\\{id}\\storage\\0{i[0]}", 'r') as file:
                content = file.read()
            output.append({"Path": i[0], "Name": i[1], "Directory": i[2], "Size": i[3], "C_TIME": i[4], "M_TIME": i[5], "EXT": i[6], "CONTENT": content})
            documents.insert_one({
                "page_content": f"Case ID: {case_id}, Evidence Number: {id}; File, Type: Text, Path: {i[0]}, Size: {i[3]}, Creation Time: {datetime.fromtimestamp(int([4]) // 1000).isoformat(sep=" ")}, Modified Time: {datetime.fromtimestamp(int(i[5]) // 1000).isoformat(sep=" ")} Content: {content}",
                "metadata": {   
                    "Case ID": case_id,
                    "Evidence": id,
                    "Path": i[0], 
                    "Name": i[1], 
                    "Directory": i[2], 
                    "Size": i[3],
                    "C_TIME": i[4], 
                    "M_TIME": i[5], 
                    "EXT": i[6]
                }
            })
            
        return output

    except Exception as e:
        print(e)
    except:
        print("Error") 
    return

def analyze_images(case_id, id):
    print("Analyzing Images")
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        
        output = []
        results = cur.execute('SELECT * FROM FILES WHERE EXT IN (".jpg", ".jpeg", ".png");').fetchall()
        for res in results:
            content = ask_ir(f"..\\files\\files\\{id}\\storage\\0{res[0]}", id, case_id).decode('utf-8')
            print(content)
            output.append({"Path": res[0], "Name": res[1], "Directory": res[2], "Size": res[3], "C_TIME": res[4], "M_TIME": res[5], "EXT": res[6], "CONTENT": content})
            documents.insert_one({
                "page_content": f"Case ID: {case_id}, Evidence Number: {id}; File, Type: Image, Path: {res[0]}, Size: {res[3]}, Creation Time: {datetime.fromtimestamp(int(res[4]) // 1000).isoformat(sep=" ")}, Modified Time: {datetime.fromtimestamp(int(res[5]) // 1000).isoformat(sep=" ")} Content: {content}",
                "metadata": {   
                    "Case ID": case_id,
                    "Evidence": id,
                    "Path": res[0], 
                    "Name": res[1], 
                    "Directory": res[2], 
                    "Size": res[3],
                    "C_TIME": res[4], 
                    "M_TIME": res[5], 
                    "EXT": res[6]
                }
            }) 
        
        print("Analyzed Images")
        return output
       
    except Exception as e:
        print(e)
    return
 
def analyze_audios(case_id, id):
    print("Analyzing Audio files")
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        audios = cur.execute(
            '''
                SELECT * FROM FILES WHERE EXT IN ('.mp3', '.m4a', '.obb', '.mpeg', '.mp4');
            '''
        ).fetchall()
        
        output = []
        for res in audios:
            content = ask_whisperx(f"..\\files\\files\\{id}\\storage\\0{res[0]}")
            output.append({"Path": res[0], "Name": res[1], "Directory": res[2], "Size": res[3], "C_TIME": res[4], "M_TIME": res[5], "EXT": res[6], "CONTENT": content})
            documents.insert_one({
                "page_content": f"Case ID: {case_id}, Evidence Number: {id}; File, Type: Audio, Path: {res[0]}, Size: {res[3]}, Creation Time: {datetime.fromtimestamp(int(res[4]) // 1000).isoformat(sep=" ")}, Modified Time: {datetime.fromtimestamp(int(res[5]) // 1000).isoformat(sep=" ")} Content: {content}",
                "metadata": {   
                    "Case ID": case_id,
                    "Evidence": id,
                    "Path": res[0], 
                    "Name": res[1], 
                    "Directory": res[2], 
                    "Size": res[3],
                    "C_TIME": res[4], 
                    "M_TIME": res[5], 
                    "EXT": res[6]
                }
            })
        print("Analyzed Audio files")
        return output
    except Exception as e:
        print(e)
    except:
        print("Error")
    return

    