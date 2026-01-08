#   FLASK UTILITY
from flask import Flask, Blueprint, request, make_response, session
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from forensix.parser import *
from pymongo import MongoClient

#   GENERAL UTILITY
from collections import defaultdict
from dotenv import load_dotenv, get_key

import os, hashlib, random, requests, uuid, json, asyncio

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

UPLOAD_FOLDER = get_key('.env', "UPLOAD_FOLDER")
DB_LOCATION = get_key('.env', "DB_LOCATION")
EXTRACTED_FILES_LOCATION = get_key('.env', "EXTRACTED_FILES_LOCATION")
EXT_DB_LOCATION = get_key('.env', "EXT_DB_LOCATION")

ASR_URL = get_key('.env', "ASR_URL")
FR_URL = get_key('.env', "FR_URL")
NLP_URL = get_key('.env', "NLP_URL")
MONGO_HOST = get_key('.env', "MONGO_HOST")
MONGO_PORT = get_key('.env', "MONGO_PORT")

print("File storage location")
print(UPLOAD_FOLDER)
print(DB_LOCATION)
print(EXTRACTED_FILES_LOCATION)
print(EXT_DB_LOCATION)
print(MONGO_HOST)
print(MONGO_PORT)

print("\nAI URLs")
print(ASR_URL)
print(FR_URL)
print(NLP_URL)

client = MongoClient(host=MONGO_HOST, port=int(MONGO_PORT))["Forensix"]

ALLOWED_EXTENSIONS = {'.zip'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    try:
        print("Creating Forensix Database")
        
        conn = sqlite3.connect(f"{DB_LOCATION}/Forensix.db")
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
                TYPE VARCHAR(10) NOT NULL,
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
        
def get_conn(file):
    return sqlite3.connect(f"{DB_LOCATION}/{file}")

def ask_whisperx(audio):
    print("Transcribing audio")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'audio': audio}
    
    session = requests.Session()
    res = session.post(f"{ASR_URL}/", headers=headers, data=payload)
    return res.text

def ask_gemma(messages, size):
    print("Asking Gemma")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'messages': messages, 'new_token_size': size}

    session = requests.Session()
    res = session.post(f"{NLP_URL}/", headers=headers, data=json.dumps(payload))
    
    if res.status_code == 200:
        return res.text
    else:
        return ""

def ask_fr_get_enc(image, evidence, case_id):
    print("Face recognition")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'image': image, 'evidence': evidence, 'case_id': case_id}
    
    session = requests.Session()
    res = session.post(f"{FR_URL}/", headers=headers, data=payload)
    
    if res.status_code == 200:
        return res.content
    else:
        print(res.content)
        return ""

def ask_fr_compare(face_known, face_unknown):
    print("Face comparision")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'enc_known': face_known, 'enc_unknown': face_unknown}

    session = requests.Session()
    res = session.post(f"{FR_URL}/similarity", headers=headers, data=payload)
    
    if res.status_code == 200:
        return res.content
    else:
        print(res.content)
        return ""

def ask_fr_compare_list(faces_known, face_unknown):
    print("Face comparision list")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'enc_known': faces_known, 'enc_unknown': face_unknown}
    
    session = requests.Session()
    res = session.post(f"{FR_URL}/similarity_list", headers=headers, data=payload)
    
    if res.status_code == 200:
        return res.content
    else:
        print(res.content)
        return ""
