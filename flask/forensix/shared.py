#   FLASK UTILITY
from flask import Flask, Blueprint, request, make_response, session
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from forensix.parser import *

#   GENERAL UTILITY
from collections import defaultdict
from dotenv import load_dotenv, get_key

import os, hashlib, random, requests, uuid

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

UPLOAD_FOLDER = get_key('.env', "UPLOAD_FOLDER")
DB_LOCATION = get_key('.env', "DB_LOCATION")
EXTRACTED_FILES_LOCATION = get_key('.env', "EXTRACTED_FILES_LOCATION")
EXT_DB_LOCATION = get_key('.env', "EXT_DB_LOCATION")

ASR_URL = get_key('.env', "ASR_URL")
FR_URL = get_key('.env', "FR_URL")
NLP_URL = get_key('.env', "NLP_URL")

print("File storage location")
print(UPLOAD_FOLDER)
print(DB_LOCATION)
print(EXTRACTED_FILES_LOCATION)
print(EXT_DB_LOCATION)

print("\nAI URLs")
print(ASR_URL)
print(FR_URL)
print(NLP_URL)

ALLOWED_EXTENSIONS = {'.zip'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    try:
        print("Creating Forensix Database")
        
        conn = sqlite3.connect(DB_LOCATION)
        cur = conn.cursor()
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS CRIME_CASES(
                CASE_ID VARCHAR(32) NOT NULL PRIMARY KEY,
                TITLE VARCHAR(50) NOT NULL,
                DESCRIPTION VARCHAR(255) NOT NULL,
                TYPE VARCHAR(20) NOT NULL,
                STATUS INT NOT NULL,
                SEVERITY INT NOT NULL,
                LOCATION VARCHAR(255) NOT NULL,
                DATE_OCCURED DATETIME NOT NULL,
                DATE_REPORTED DATETIME NOT NULL,
                ASSIGNED_OFFICER VARCHAR(32),
                WITNESSES INT,
                NOTES VARCHAR(100)
            );
            '''    
        )
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS EVIDENCES(
                CASE_ID VARCHAR(32) NOT NULL REFERENCES CRIME_CASES(CASE_ID),
                TITLE VARCHAR(50) NOT NULL UNIQUE,
                REFERENCE VARCHAR(512) NOT NULL
            );
            '''    
        )
            
        conn.commit()
        cur.close()
        conn.close()
        print("Database Created")
    
    except Exception as e:
        print(e)
        
def get_conn():
    return sqlite3.connect(DB_LOCATION)


def ask_whisperx(audio):
    print("Transcribing audio")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'audio': audio}
    
    session = requests.Session()
    res = session.post(f"{ASR_URL}/", headers=headers, data=payload)
    return res.text

def ask_fr(image):
    print("Face recognition")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'image': image}
    
    session = requests.Session()
    res = session.post(f"{FR_URL}/", headers=headers, data=payload)
    return

def ask_gemma(messages, size):
    print("Asking Gemma")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'messages': messages, 'new_token_size': size}
    
    session = requests.Session()
    res = session.post(f"{NLP_URL}/", headers=headers, data=payload)
    
    if res.status_code == 200:
        return res.text
    else:
        return ""
