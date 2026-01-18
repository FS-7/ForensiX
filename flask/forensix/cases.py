from forensix.shared import *
from forensix.threat import extraction

cases = Blueprint('cases', __name__, url_prefix='/cases')

@cases.route('/', methods=["GET"])
def get_cases():
    print("Request to access all Cases")

    results = []
    sql = "SELECT * FROM CRIME_CASES;"
    values = {}
    
    try:
        conn = get_conn("Forensix.db")
        cursor = conn.cursor()
        
        evidences = defaultdict(list)
        keys = []
        
        for i in cursor.execute("SELECT * FROM EVIDENCES;", values).fetchall():
            keys.append(i[0])
        
        for i in set(keys):
            for j in cursor.execute("SELECT rowid, case_id, type FROM EVIDENCES;", values).fetchall():    
                if i == j[1]:
                    evidences[i].append((j[0], j[2]))
        
        for id, i in enumerate(cursor.execute(sql, values).fetchall()):
            results.append(
                {
                    "id": str(id), "caseNumber": i[0], "title": i[1], "description": i[2], "type": i[3], "status": i[4], "severity": i[5], "location": i[6], "dateOccured": (int(i[7]) * 1000), "dateReported": (int(i[8]) * 1000), "assignedOfficer": i[9], "witnesses": i[10], "evidences": evidences[i[0]], "notes": i[11]
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
        conn = get_conn("Forensix.db")
        cursor = conn.cursor()
        
        cursor.execute(sql, values)
        
        cursor.close()
        conn.commit()
        conn.close()
        
    data = request.form
    print(data)
    
    title = data['title']
    description = data['description']
    type = data['type']
    status = 'open'
    severity = data['severity']
    location = data['location']
    dateOccurred = data['dateOccurred']
    dateReported = datetime.now().timestamp()
    assignedOfficer = data['assignedOfficer']
    witnesses = data['witnesses']
    notes = ""
    
    dateOccurred = int(dateOccurred) // 1000
    sql = "INSERT INTO CRIME_CASES(CASE_ID, TITLE, DESCRIPTION, TYPE, STATUS, SEVERITY, LOCATION, DATE_OCCURED, DATE_REPORTED, ASSIGNED_OFFICER, WITNESSES, NOTES) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    
    inserted = False
    while inserted != True:
        try:
            case_id = "CC-" + datetime.now().strftime("%Y") + "-" + str(random.randint(0, 999)).zfill(3)
            
            values = [case_id, title, description, type, status, severity, location, dateOccurred, dateReported, assignedOfficer, witnesses, notes]
    
            temp(sql, values)
            inserted = True
            print("Case Added Successfully")
            
            documents.insert_one({
                "page_content": f"Case ID {case_id}, titled “{title},” is a {type} case currently marked as {status} with a {severity} severity level. The incident occurred at {location} on {dateOccurred} and was officially reported on {dateReported}. The case description states that {description}. The matter has been assigned to {assignedOfficer}, and the following witnesses were identified in relation to the incident: {witnesses}.".lower(), 
                "metadata": {
                    "Case ID": case_id,
                    "Title": title,
                    "Description": description,
                    "Type": type,
                    "Status": status,
                    "Severity": severity,
                    "Location": location,
                    "Date_Occurred": datetime.fromtimestamp(int(dateOccurred) // 1000).isoformat(),
                    "Date_Reported": datetime.fromtimestamp(int(dateReported) // 1000).isoformat(),
                    "Assigned_Officer": assignedOfficer,
                    "Witnesses": witnesses                    
                }
            })
            
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
    print("Removing Case")
    data = request.form
    id = data['id']
    
    sql = "DELETE FROM CRIME_CASE WHERE ID=?;"
    values = [id]
    
    try:
        conn = get_conn("Forensix.db")
        cursor = conn.cursor()
        cursor.execute(sql, values)
        print("Case Removed Successfully")
        return make_response("", 200)
    
    except Exception as e:
        print(e)
    except:
        print("Error")
        
    return make_response("Error", 200)

@cases.route('/evidence', methods=["POST"])
def post_evidence():
    print("Adding Evidence...")
    
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    data = request.form
    case_number = data['caseNumber']
    type = data['type']
    filename = ""

    try:
        for i in request.files:
            file = request.files[i]
            filename = secure_filename(f"{case_number}_{file.filename}")
            file.save(os.path.join(UPLOAD_FOLDER, filename))
    except Exception as e:
        print(e)
    except:
        print("Error")
        
    try:
        sql = "INSERT INTO EVIDENCES(CASE_ID, TYPE, REFERENCE) VALUES (?, ?, ?);"
        values = [case_number, type, filename]
        conn = get_conn(f"{DB_LOCATION}/Forensix.db")
        cursor = conn.cursor()
        cursor.execute(sql, values)
        last_id = str(cursor.lastrowid)
        cursor.close()
        conn.commit()
        conn.close()
        print("Evidence Added Successfully")
        
        extraction(last_id, filename, case_number)
        
        return make_response("", 200)
        
    except sqlite3.IntegrityError as e:
        return make_response("Integrity Error", 400)
    except Exception as e:
        print(e)
    except:
        print("Error")
    
    return make_response("", 400)

@cases.route('/evidence', methods=["DELETE"])
def delete_evidence():
    print("Removing Evidence...")
    
    data = request.form
    id = data['id']
    
    try:
        sql = "DELETE FROM EVIDENCES WHERE ID=?;"
        values = [id]
        conn = get_conn("Forensix.db")
        cursor = conn.cursor()
        cursor.execute(sql, values)
        cursor.close()
        conn.commit()
        conn.close()
        print("Evidence Removed Successfully")
        
        return make_response("Evidence Removed", 200)
    
    except sqlite3.IntegrityError as e:
        return make_response("Integrity Error", 400)
    except Exception as e:
        print(e)
    except:
        print("Error")
    
    return make_response("Error", 400)
