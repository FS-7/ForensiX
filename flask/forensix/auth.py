from forensix.shared import * 

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=["POST"])
def register():
    salt = uuid.uuid4().hex
    data = request.form
    name = data["name"]
    email = data["email"]
    phone = data["phone"]
    password = hashlib.sha512((data["password"] + salt).encode('utf-8')).hexdigest()
    
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "INSERT INTO USER(NAME, EMAIL, PHONE, PASSWORD, SALT) VALUES(?, ?, ?, ?, ?);"
        params = [name, email, phone, password, salt]
        cursor.execute(sql, params)
        cursor.close()
        conn.commit()
        
    except sqlite3.OperationalError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except sqlite3.InternalError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except sqlite3.ProgrammingError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except:
        print(email, password)
        return make_response("Internal Server Error", 500)
    
    return make_response(data, 200)
    

@auth.route('/login', methods=["POST"])
def login():
    data = request.form
    email = data["email"]
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "SELECT SALT FROM USER WHERE EMAIL=?;"
        params = [email]
        cursor.execute(sql, params)
    except sqlite3.OperationalError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except sqlite3.InternalError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except sqlite3.ProgrammingError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except:
        print(email, password)  
        return make_response("Internal Server Error", 500)
    
    salt = cursor.fetchone()[0]
    password = hashlib.sha512((data["password"] + salt).encode('utf-8')).hexdigest()
    
    try:
        cursor = conn.cursor()
        sql = "SELECT PASSWORD FROM USER WHERE EMAIL=?;"
        params = [email]
        r = cursor.execute(sql, params).fetchone()[0]
        cursor.close() 
        
        if r==password:
            return make_response("", 200)
        else:
            return make_response("", 200)
        
    except sqlite3.OperationalError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except sqlite3.InternalError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except sqlite3.ProgrammingError as e:
        print(e)
        return make_response("Internal Server Error", 500)
    except:
        print(email, password)
        return make_response("Internal Server Error", 500)
        