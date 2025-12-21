from forensix.shared import * 

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/update_password', methods=["POST"])
def UpdatePassword():
    salt = uuid.uuid4().hex
    data = request.form
    password = hashlib.sha512((data["password"] + salt).encode('utf-8')).hexdigest()
    
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "UPDATE ADMIN SET PASSWORD=? AND SALT=?;"
        params = [password, salt]
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
        print(password)
        return make_response("Internal Server Error", 500)
    
    return make_response(data, 200)
    
@admin.route('/login', methods=["POST"])
def login():
    data = request.form
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "SELECT SALT FROM ADMIN"
        cursor.execute(sql)
        
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
        print(password)  
        return make_response("Internal Server Error", 500)
    
    salt = cursor.fetchone()[0]
    password = hashlib.sha512((data["password"] + salt).encode('utf-8')).hexdigest()
    
    try:
        conn = get_conn()
        cursor = conn.cursor()
        sql = "SELECT PASSWORD FROM ADMIN;"
        r = cursor.execute(sql).fetchone()[0]
        cursor.close()
        conn.commit()
            
        if r==password:
            return make_response("Right Password", 200)
        else:
            return make_response("Wrong password", 200) 
        
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
        print(password)
        return make_response("Internal Server Error", 500)