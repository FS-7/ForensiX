from pathlib import Path
from forensix.shared import *
from forensix.parser import parseSMS_CSV, parseLogsCSV, parseContactsCSV, parseSMS_SQL, parseLogsSQL
import zipfile

DB_LOCATION = "../db/"

def init(id):
    try:
        conn = sqlite3.connect(DB_LOCATION + id)
        cur = conn.cursor()
        cur.execute(
            '''
            DROP TABLE IF EXISTS MESSAGES;
            DROP TABLE IF EXISTS CALL_LOGS;
            DROP TABLE IF EXISTS CONTACTS;
            DROP TABLE IF EXISTS FILES;
            
            CREATE TABLE IF NOT EXISTS MESSAGES(
                ADDRESS VARCHAR(100) NOT NULL,
                BODY VARCHAR(512) NOT NULL,
                DATE_SENT DATETIME NOT NULL,
                DATE_RECEIVED DATETIME NOT NULL,
                TYPE VARCHAR(10) NOT NULL,
                SEEN VARCHAR(4) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS CALL_LOGS(
                NUMBER VARCHAR(10) NOT NULL,
                DATE DATETIME NOT NULL,
                DURATION INT NOT NULL,
                TYPE VARCHAR(10) NOT NULL,
            );
            
            CREATE TABLE IF NOT EXISTS CONTACTS(
                NAME VARCHAR(50) NOT NULL,
                NUMBER VARCHAR(10) NOT NULL,
                GROUP INT NOT NULL,
                EMAIL VARCHAR(255) NOT NULL,
            );
            
            CREATE TABLE IF NOT EXISTS FILES(
                PATH VARCHAR(260) NOT NULL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                DIRECTORY VARCHAR(255) NOT NULL,
                SIZE INT NOT NULL,
                DATETIME DATETIME NOT NULL,
                EXT VARCHAR(5) NOT NULL
            );
            '''    
        )
        conn.commit()
        cur.close()
        conn.close()
    
    except Exception as e:
        print(e)
        
    return 

def extract(case, title, id):
    zipfile_path = f"./upload/{case}_{title}"
    extraction_directory = f"../data/{id}"
    os.mkdir(f"../data/{id}/")
    
    try:
        with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
            zip_ref.extractall(extraction_directory)

    except zipfile.BadZipFile:
        print(f"Error: '{zipfile_path}' is not a valid zip file.")
    except FileNotFoundError:
        print(f"Error: Zip file '{zipfile_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    return

def add_to_database(id):
    try:
        sms = parseSMS_CSV(f"../data/{id}/")
        call_logs = parseLogsCSV(f"../data/{id}/")
        contacts = parseContactsCSV(f"../data/{id}/")
        files = scan_files(f"../data/{id}/")
        
        conn = sqlite3.connect(DB_LOCATION + id)
        cur = conn.cursor()
        cur.executemany(
            '''
                INSERT INTO MESSAGES(ADDRESS, BODY, DATE_SENT, DATE_RECEIVED, TYPE, SEEN) VALUES(?, ?, ?, ?, ?, ?);
            ''',
            [sms]
        )
        cur.executemany(
            '''
                INSERT INTO CALL_LOGS(NUMBER, TIME, DURATION, TYPE) VALUES(?, ?, ?, ?);
            ''',
            [call_logs]
        )
        cur.executemany(
            '''
                INSERT INTO CONTACTS(NAME, NUMBER, GROUP, EMAIL) VALUES(?, ?, ?, ?);
            ''',
            [contacts]
        )
        cur.executemany(
            '''
                INSERT INTO FILES(PATH, NAME, DIRECTORY, SIZE, DATETIME, EXT) VALUES(?, ?, ?, ?, ?, ?);
            ''',
            [files]
        )
        conn.commit()
        cur.close()
        conn.close()
        
    except Exception as e:
        print(e)
    return

def analyze_text(id):
    try:
        conn = sqlite3.connect(DB_LOCATION + id)
        cur = conn.cursor()
        sms = cur.execute(
            '''
                SELECT * FROM MESSAGES;
            '''
        ).fetchall()
        
        candidate_labels = [
            "identity_attack",
            "sexual_explicit",
            "threat",
            "toxicity",
            "normal",
            "extremism"
        ]

        res = defaultdict(str)
        output = defaultdict(dict)
        
        keys = set([i[0] for i in reversed(sms)])

        for k in keys:
            for i in sms:
                if k == i[0]:
                    res[k] = res[k] + i[1] + " "

        for k in res.keys():
            output[k] = zsc_model(res[k], candidate_labels)
            
        conn.commit()
        cur.close()
        conn.close()
        
        return output
        
    except Exception as e:
        print(e)
    return 

def analyze_images():
    
    return
 
def analyze_audios(id):
    try:
        conn = sqlite3.connect(DB_LOCATION + id)
        cur = conn.cursor()
        audios = cur.execute(
            '''
                SELECT path FROM FILES WHERE EXT IN (mp3, m4a, obb);
            '''
        ).fetchall()
        
        results = defaultdict(list)
        for audio_path in audios:
            audio = asr_model.load_audio(audio_path)
            results[audio_path] = asr_model.transcribe(audio, batch_size=batch_size, language='en')
        
    except Exception as e:
        print(e)
    return

def analyze(id):
    text_outputs = analyze_text(id)
    images_outputs = analyze_images(id)
    audio_outputs = analyze_audios(id)
    return {"text": text_outputs, "images": images_outputs, "audio": audio_outputs}

def generate(id):    
    
    return 

def scan_files(root="."):
    entries = []
    for p in Path(root).rglob("*"):
        if p.is_file():
            stat = p.stat()
            entries.append({
                "path": str(p),
                "name": p.name,
                "parent": str(p.parent),
                "size": stat.st_size,
                "mtime": stat.st_mtime,
                "mtime_readable": datetime.fromtimestamp(int(stat.st_mtime)//1000).strftime("%d-%m-%Y %H:%M:%S"),
                "ext": p.suffix.lower(),
            })
    return entries

def generate_query(query):
    try:
        messages = [
            {
                "role": "user", "content": 
                f"""
                Context: You are a SQL generator. 
                Given the following database schema:
                    Table: Messages
                    Columns:
                    - id (integer)
                    - Address (text)
                    - Date Sent (date)
                    - Date Received (date)
                    - Type (text)
                    - Body (text)
                    - Seen (boolean)
                    
                    Table: Contacts
                    Columns:
                    - id (integer)
                    - name (text)
                    - number (number)
                    - email (text)
                    
                    Table: Call Logs
                    Columns:
                    - id (integer)
                    - Owner (text)
                    - Date Time (number)
                    - Duration (number)
                    - Type (text)
                    
                    Table: Files
                    Columns:
                    - path (text)
                    - name (text)
                    - parent (text)
                    - size (number)
                    - datetime (datetime)
                    - ext (text) alias type
                Convert the following user question into a correct, safe SQL query. 
                Return only SQL, no explanations.
                Query: {query}
                """
            }
        ]

        outputs = nlp_model(messages, max_new_tokens=128)
        assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
        return assistant_response
    
    except Exception as e:
        print(e)
        
    return 

def run_query(query):
    if str(query).lower().startswith("select"):
        return
    conn = sqlite3.connect("./data/sms.db")
    cur = conn.cursor()
    output = cur.execute(
        query,
        []
    ).fetchall()
    return output
    
def convert_to_nlp(results):
    messages = [
        {
            "role": "user", "content": 
            f"""
            Data: {results}
            Convert the following data in human readable format
            """
        }
    ]
    try:
        outputs = nlp_model(messages, max_new_tokens=256)
        assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
        return assistant_response
        
    except Exception as e:
        print(e)