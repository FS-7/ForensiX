from forensix.shared import *
from forensix.threat import init, extract, add_to_database
from collections import defaultdict

cases = Blueprint('cases', __name__, url_prefix='/cases')

@cases.route('/', methods=["GET"])
def get_cases():
    print("Request to access all Cases")

    results = []
    sql = "SELECT * FROM CRIME_CASES;"
    values = {}
    
    try:
        conn = get_conn()
        cursor = conn.cursor()
        
        evidences = defaultdict(list)
        keys = []
        
        for i in cursor.execute("SELECT * FROM EVIDENCES;", values).fetchall():
            keys.append(i[0])
        
        for i in set(keys):
            for j in cursor.execute("SELECT rowid, case_id, title FROM EVIDENCES;", values).fetchall():    
                if i == j[1]:
                    evidences[i].append((j[0], j[2]))
        
        for id, i in enumerate(cursor.execute(sql, values).fetchall()):
            results.append(
                {
                    "id": str(id), "caseNumber": i[0], "title": i[1], "description": i[2], "type": i[3], "status": i[4], "severity": i[5], "location": i[6], "dateOccured": i[7], "dateReported": i[8], "assignedOfficer": i[9], "witnesses": i[10], "evidences": evidences[i[0]], "notes": i[11]
                }
            )
        print("Request completed")
        
        return make_response(results, 200)
    
    except Exception as e:
        print(e)
    except:
        print("Error")
    
    return make_response([], 400)
    

@cases.route('/', methods=["POST"])
def post_cases():
    print("Adding a case")
    
    def temp(sql, values):
        conn = get_conn()
        cursor = conn.cursor()
        
        cursor.execute(sql, values)
        
        cursor.close()
        conn.commit()
        conn.close()
        
    data = request.form
    
    title = data['title']
    description = data['description']
    type = data['type']
    status = 'open'
    severity = data['severity']
    location = data['location']
    dateOccurred = data['dateOccurred']
    dateReported = datetime.now()
    assignedOfficer = data['assignedOfficer']
    witnesses = data['witnesses']
    notes = ""
    
    dateOccurred = datetime.strptime(dateOccurred, "%Y-%m-%d").strftime("%m %d %Y %H:%M:%S")
    sql = "INSERT INTO CRIME_CASES(CASE_ID, TITLE, DESCRIPTION, TYPE, STATUS, SEVERITY, LOCATION, DATE_OCCURED, DATE_REPORTED, ASSIGNED_OFFICER, WITNESSES, NOTES) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    
    inserted = False
    while inserted != True:
        try:
            case_id = "CC-" + datetime.now().strftime("%Y") + "-" + str(random.randint(0, 999)).zfill(3)
            
            values = [case_id, title, description, type, status, severity, location, dateOccurred, dateReported, assignedOfficer, witnesses, notes]
    
            temp(sql, values)
            inserted = True
            print("Case Added Successfully")
            
            return make_response("", 200)
        
        except sqlite3.IntegrityError:
            inserted = False
            continue
        except Exception as e:
            print(e)
            return make_response("", 500)
        except:
            print("Error")
            return make_response("", 500)

@cases.route('/', methods=["DELETE"])
def delete_cases():
    data = request.form
    id = data['id']
    
    sql = "DELETE FROM CRIME_CASE WHERE ID=%(id)s;"
    values = {"id": id}
    
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        return make_response("", 200)
    
    except Exception as e:
        print(e)
    except:
        print("Error")
        
    return make_response("", 200)

@cases.route('/addEvidence', methods=["POST"])
def post_evidence():
    print("Adding Evidence...")
    
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    data = request.form
    case_number = data['caseNumber']
    title = data['title']
    filename = ""
    
    try:
        for i in request.files:
            file = request.files[i]
            filename = secure_filename(f"{case_number}_{title}_{file.filename}")
            file.save(os.path.join(UPLOAD_FOLDER, filename))
    except Exception as e:
        print(e)
    except:
        print("Error")
    
    try:
        sql = "INSERT INTO EVIDENCES(CASE_ID, TITLE, REFERENCE) VALUES (?, ?, ?);"
        values = [case_number, title, filename]
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        last_id = str(cursor.lastrowid)
        cursor.close()
        conn.commit()
        conn.close()
        print("Evidence Added Successfully")
        
        
        #   CREATE A FUNCTION THAT EXTRACT ZIP FILE 
        #   SEND CASE_NUMBER, TITLE, LAST_ROW_ID 
        init(last_id)
        extract(filename, last_id)
        add_to_database(last_id)
        print("Data Extracted and inserted into database")
        
        return make_response("", 200)
    except sqlite3.IntegrityError as e:
        return make_response("Integrity Error", 400)
    except Exception as e:
        print(e)
    except:
        print("Error")
    
    return make_response("", 400)