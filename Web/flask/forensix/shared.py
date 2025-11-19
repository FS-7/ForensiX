from flask import Flask, Blueprint, request, make_response, session
from mysql import connector
import hashlib, uuid, json, os

cnx = connector.connect(
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME")
)
