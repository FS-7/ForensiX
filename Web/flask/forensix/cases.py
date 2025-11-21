from forensix.shared import *
from collections import defaultdict

cases = Blueprint('cases', __name__, url_prefix='/cases')

@cases.route('/', methods=["GET"])
def get_cases():
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
            for j in cursor.execute("SELECT * FROM EVIDENCES;", values).fetchall():    
                if i == j[0]:
                    evidences[i].append(j[1])
        
        for id, i in enumerate(cursor.execute(sql, values).fetchall()):
            results.append(
                {
                    "id": str(id), "caseNumber": i[0], "title": i[1], "description": i[2], "type": i[3], "status": i[4], "severity": i[5], "location": i[6], "dateOccured": i[7], "dateReported": i[8], "assignedOfficer": i[9], "witnesses": i[10], "evidence": evidences[i[0]], "notes": i[11]
                }
            )
        return make_response(results, 200)
    
    except Exception as e:
        print(e)
    except:
        print("Error")
    
    return make_response([], 400)
    

@cases.route('/', methods=["POST"])
def post_cases():
    data = request.form
    
    case_id = "CC-" + datetime.now().strftime("%Y") + "-" + str(random.randint(0, 999)).zfill(3)
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
    #evidences = data['evidences']
    notes = ""
    
    sql = "INSERT INTO CRIME_CASES(CASE_ID, TITLE, DESCRIPTION, TYPE, STATUS, SEVERITY, LOCATION, DATE_OCCURED, DATE_REPORTED, ASSIGNED_OFFICER, WITNESSES, NOTES) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    values = [case_id, title, description, type, status,severity, location, dateOccurred, dateReported, assignedOfficer, witnesses, notes]
    
    try:
        conn = get_conn()
        cursor = conn.cursor()
        
        cursor.execute(sql, values)
        
        cursor.close()
        conn.commit()
        conn.close()
        
        return make_response("", 200)
    
    except Exception as e:
        print(e)
    except:
        print("Error")

@cases.route('/', methods=["PUT"])
def put_cases():
    return make_response("", 200)

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






cases_data = [
    {
        "id": "1",
        "caseNumber": "CC-2024-001",
        "title": "Armed Robbery at Downtown Bank",
        "description": "Suspects entered the bank at approximately 2:30 PM, threatening staff and customers with firearms. Escaped with approximately $50,000.",
        "type": "theft",
        "status": "investigating",
        "severity": "critical",
        "location": "First National Bank, 123 Main St",
        "dateReported": "2024-11-15",
        "dateOccurred": "2024-11-15",
        "assignedOfficer": "Det. Sarah Johnson",
        "witnesses": 8,
        "evidence": ["Security footage", "Fingerprints", "Witness statements"],
        "notes": "Suspects wore masks and left in a dark sedan."
    },
    {
        "id": "2",
        "caseNumber": "CC-2024-002",
        "title": "Residential Burglary on Oak Street",
        "description": "Break-in occurred during daytime hours. Electronics, jewelry, and cash were stolen.",
        "type": "theft",
        "status": "open",
        "severity": "medium",
        "location": "456 Oak Street",
        "dateReported": "2024-11-14",
        "dateOccurred": "2024-11-13",
        "assignedOfficer": "Officer Mike Chen",
        "witnesses": 2,
        "evidence": ["Forced entry marks", "Shoe prints"],
        "notes": ""
    },
    {
        "id": "3",
        "caseNumber": "CC-2024-003",
        "title": "Assault at Local Bar",
        "description": "Physical altercation between two patrons resulted in serious injuries to one individual.",
        "type": "assault",
        "status": "pending",
        "severity": "high",
        "location": "The Corner Bar, 789 Elm Ave",
        "dateReported": "2024-11-12",
        "dateOccurred": "2024-11-12",
        "assignedOfficer": "Det. James Martinez",
        "witnesses": 6,
        "evidence": ["Surveillance video", "Medical report", "Witness statements"],
        "notes": ""
    },
    {
        "id": "4",
        "caseNumber": "CC-2024-004",
        "title": "Identity Theft and Credit Card Fraud",
        "description": "Victim's personal information was stolen and used to open multiple credit card accounts.",
        "type": "fraud",
        "status": "investigating",
        "severity": "medium",
        "location": "Online/Multiple Locations",
        "dateReported": "2024-11-10",
        "dateOccurred": "2024-10-28",
        "assignedOfficer": "Det. Lisa Wong",
        "witnesses": 0,
        "evidence": ["Credit reports", "Transaction records", "IP addresses"],
        "notes": ""
    },
    {
        "id": "5",
        "caseNumber": "CC-2024-005",
        "title": "Vandalism at Public Park",
        "description": "Graffiti and property damage to park facilities and playground equipment.",
        "type": "vandalism",
        "status": "solved",
        "severity": "low",
        "location": "Central Park",
        "dateReported": "2024-11-08",
        "dateOccurred": "2024-11-07",
        "assignedOfficer": "Officer Tom Anderson",
        "witnesses": 1,
        "evidence": ["Photos", "Paint samples"],
        "notes": "Suspect identified through witness testimony and arrested."
    },
    {
        "id": "6",
        "caseNumber": "CC-2024-006",
        "title": "Cyber Attack on Local Business",
        "description": "Ransomware attack on local business computer systems, demanding payment for data release.",
        "type": "cybercrime",
        "status": "open",
        "severity": "high",
        "location": "Tech Solutions Inc, 321 Commerce Blvd",
        "dateReported": "2024-11-18",
        "dateOccurred": "2024-11-17",
        "assignedOfficer": "Det. Kevin Park",
        "witnesses": 0,
        "evidence": ["System logs", "Ransom note", "Network forensics"],
        "notes": ""
    }
]

@cases.route('/insertAll', methods=["GET"])
def insertAll():
    sql = "INSERT INTO CRIME_CASES(CASE_ID, TITLE, DESCRIPTION, TYPE, STATUS, SEVERITY, LOCATION, DATE_OCCURED, DATE_REPORTED, ASSIGNED_OFFICER, WITNESSES, NOTES) VALUES(?,?,?,?,?,?,?,?,?,?,?,?);"
    try:
        conn = get_conn()
        for case in cases_data:
            values = [case["caseNumber"], case["title"], case["description"], case["type"], case["status"], case["severity"], case["location"], case["dateOccurred"], case["dateReported"], case["assignedOfficer"], case["witnesses"], case["notes"]]
            cursor = conn.cursor()
            cursor.execute(sql, values)
            for evidence in case["evidence"]:
                cursor.execute("INSERT INTO EVIDENCES(CASE_ID, TITLE, REFERENCE) VALUES (?, ?, ?);", [case["caseNumber"], evidence, ""])
        
        cursor.close()
        conn.commit()
        conn.close()
    
    except Exception as e:
        print(e)
    except:
        print("Error")
    return make_response(cases_data, 200)