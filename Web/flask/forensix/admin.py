from forensix.shared import * 

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/register', methods=["POST"])
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
    

@admin.route('/login', methods=["POST"])
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