#   FLASK UTILITY
from flask import Flask, Blueprint, request, make_response, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from forensix.parser import *

#   GENERAL UTILITY
from datetime import datetime
from collections import defaultdict

import os, hashlib, json, random

#   DATABASE UTILITY
import sqlite3

#   AI UTILITY
import torch
import pandas as pd 
import numpy as np

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
DB_LOCATION = os.getenv("DB_LOCATION")
EXTRACTED_FILES_LOCATION = os.getenv("EXTRACTED_FILES_LOCATION")
EXT_DB_LOCATION = os.getenv("EXT_DB_LOCATION")
AI_URL = os.getenv("AI_URL")

ALLOWED_EXTENSIONS = {'.zip'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    try:
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
    
    except Exception as e:
        print(e)
    
def get_conn():
    return sqlite3.connect(DB_LOCATION)
