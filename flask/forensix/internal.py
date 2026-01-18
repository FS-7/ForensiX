from forensix.shared import *

internal = Blueprint('internal', __name__, url_prefix='/internal')

@internal.route('/report/<int:id>', methods=["GET"])
def generate_report(id):
    print("Generating Report...")
    response = report.find({"Evidence": f"{id}"}, {"_id": 0})
    
    print("Report Generated")
    return make_response(response.to_list(), 200)

@internal.route('/nlp', methods=["POST"])
def nlp_query():
    print("User Query...")
    
    data = request.form
    query = data['query']
    
    print(query)
    
    output = ""
    try:
        print("asking query")
        messages = load_input()
        messages.append({"role": "user", "content": f"{query}, just filter them and print them as is, no explaination"})
        output = ask_gemma(messages, 1000)
        messages.append({"role": "assistant", "content": output})
        
        print("Output: ", output)
        return make_response(output, 200)
    except Exception as e:
        print(e)
        return make_response("", 400)
    except:
        print("Error")

def load_input():
    messages = []
    data = load_data()
    print(data)
    query = f"""You are a data retriever model, retrieve data and files info based on the query. This is all the data. Data: {data}"""
    messages.append({"role": "user", "content": f"{query}"})
    messages.append({"role": "assistant", "content": ask_gemma(messages, 10)})
    
    return messages

def load_data():
    res = documents.find({}, {"_id": 0})
    temp = []
    for r in res:
        temp.append(r["page_content"])
    return "\n".join(temp)