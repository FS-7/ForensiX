from ai.shared import *

internal = Blueprint('internal', __name__, url_prefix='/internal')

@internal.route('/', methods=["GET"])
def internal_index():
    return make_response("Internal", 200)

@internal.route('/generateReport/<int: id>', methods=["GET"])
def generate_report(id):
    #analyze()
    #generate()
    return make_response("", 200)

@internal.route('/nlp', methods=["POST"])
def nlp_query():
    data = request.data
    generate_query()
    return make_response("", 200)

def generate_query(query):
    try:
        messages = [
            {"role": "user", "content": 
                f"""
                Context: You are a SQL generator. 
                Given the following database schema:
                    Table: Messages
                    Columns:
                    - id (integer)
                    - Address (text)
                    - Date Sent (date)
                    - Date Received (date)
                    - Type (text)
                    - Body (text)
                    - Seen (boolean)
                    
                    Table: Contacts
                    Columns:
                    - id (integer)
                    - name (text)
                    - number (number)
                    - email (text)
                    
                    Table: Call Logs
                    Columns:
                    - id (integer)
                    - Owner (text)
                    - Date Time (number)
                    - Duration (number)
                    - Type (text)
                    
                    Table: Files
                    Columns:
                    - path (text)
                    - name (text)
                    - parent (text)
                    - size (number)
                    - datetime (datetime)
                    - ext (text) alias type
                Convert the following user question into a correct, safe SQL query. 
                Return only SQL, no explanations.
                Query: {query}
                """}
        ]

        outputs = nlp_model(messages, max_new_tokens=128)
        assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
        return assistant_response
    
    except Exception as e:
        print(e)
        
    return 
