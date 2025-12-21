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
        files = scan_files(f"{EXTRACTED_FILES_LOCATION}/{id}/data/")
        
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

def extraction(last_id, filename):
    init(last_id)
    extract(filename, last_id)
    add_to_database(last_id)
    print("Data Extracted and inserted into database")

def analyze(id):
    text_outputs = analyze_text(id)
    #images_outputs = analyze_images(id)
    audio_outputs = analyze_audios(id)
    contacts_output = analyze_contacts(id)
    return {"text": text_outputs, "contacts": contacts_output, "audio": audio_outputs}#, "images": images_outputs}

def analyze_text(id):
    print("Analyzing Text messages")
    
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        sms = cur.execute(
            '''
                SELECT * FROM MESSAGES;
            '''
        ).fetchall()
        
        candidate_labels = [
            "Normal", "Threat", "Identity Attack", "Sexually Explicit", "Extremism", "Scam"
        ]
        
        res = defaultdict(str)
        output = defaultdict(str)
        
        for i in sms:
            res[i[0]] = res[i[0]] + ("Sender: " if i[4] == "Sent" else "Receiver: ") + i[1] + " "    
        
        for k in res.keys():
            print(k)
            messages = f"""
                Text: {res[k]}.
                Query: In one word classify the text into one of the following categories: {', '.join(candidate_labels)}. No explaination.
            """
            output[k] = ask_gemma(messages)
        
        print("Done")
        return output
        
    except Exception as e:
        print(e)
    return 
    
def analyze_images(id):
    print("Analyzing Images")
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        print("Analyzed Images")
       
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

def analyze_contacts(id):
    print("Analyzing Images")
    try:
        conn = sqlite3.connect(f"{EXT_DB_LOCATION}/{id}.db")
        cur = conn.cursor()
        results = cur.execute(
            '''
                SELECT NUMBER FROM CALL_LOGS ORDER BY DATE LIMIT 5;
            '''
        ).fetchall()
        print("Analyzed Contacts")
        return results
    except Exception as e:
        print(e)
    return 
    
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
    