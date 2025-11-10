from flask import Flask, request, make_response, Blueprint
from flask_cors import CORS
from mysql import connector
import hashlib, uuid, os, json

app = Flask(__name__)
CORS(app)

cnx = connector.connect(
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME")
)

@app.route('/')
def main():
    return make_response("Hello", 200)

@app.route('/register', methods=["POST"])
def register():
    salt = uuid.uuid4().hex
    data = request.form
    name = data["name"]
    email = data["email"]
    phone = data["phone"]
    password = hashlib.sha512((data["password"] + salt).encode('utf-8')).hexdigest()
    
    try:
        cursor = cnx.cursor()
        sql = "INSERT INTO USER(NAME, EMAIL, PHONE, PASSWORD, SALT) VALUES(%(name)s, %(email)s, %(phone)s, %(password)s, %(salt)s);"
        params = {"name": name, "email": email, "phone": phone, "password": password, "salt": salt}
        cursor.execute(sql, params=params)
    except connector.OperationalError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except connector.InternalError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except connector.ProgrammingError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except:
        print(email, password)
        return make_response("Internal Server Error", 500)
    finally:
        cursor.close()
        cnx.commit()
    
    return make_response(data, 200)
    

@app.route('/login', methods=["POST"])
def login():
    data = request.form
    email = data["email"]
    try:
        cursor = cnx.cursor()
        sql = "SELECT SALT FROM USER WHERE EMAIL=%(email)s"
        params = {"email": email}
        cursor.execute(sql, params=params)
    except connector.OperationalError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except connector.InternalError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except connector.ProgrammingError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except:
        print(email, password)  
        return make_response("Internal Server Error", 500)
    
    salt = cursor.fetchone()[0]
    password = hashlib.sha512((data["password"] + salt).encode('utf-8')).hexdigest()
    
    try:
        cursor = cnx.cursor(buffered=True)
        sql = "SELECT COUNT(ID) FROM USER WHERE EMAIL=%(email)s AND PASSWORD=%(password)s;"
        params = {"email": email, "password": password}
        cursor.execute(sql, params=params)
    except connector.OperationalError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except connector.InternalError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except connector.ProgrammingError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except:
        print(email, password)
        return make_response("Internal Server Error", 500)
    finally:
        cursor.close()    
        
    return make_response(data, 200)

@app.errorhandler(404)
def page_not_found():
    return make_response("The requested URL does not exist", 404)

@app.route("/query", methods=["POST"])
def query():
    data = json.loads(request.data) 
    query = data["query"]
    
    return make_response(query, 200)