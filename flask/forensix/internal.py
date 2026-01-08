from forensix.shared import *
from forensix.threat import analyze, generate_query, run_query, convert_to_nlp

internal = Blueprint('internal', __name__, url_prefix='/internal')
        
@internal.route('/', methods=["GET"])
def internal_index():
    return make_response("Internal", 200)

@internal.route('/report/<int:id>', methods=["GET"])
def generate_report(id):
    print("Generating Report...")
    response = client["Evidence_report"].find({"Evidence": f"{id}"}, {"_id": 0})
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
    query = f"""You are a data retriever model, retrieve data and files info based on the query. This is all the data.
Data: {data}
"""
    messages.append({"role": "user", "content": f"{query}"})
    messages.append({"role": "assistant", "content": ask_gemma(messages, 10)})
    
    return messages

def load_data():
    return f"""
case: cc-, evidence: 1: message from +16505551212 (received) on 20-11-2025, 20:15:06: morning bob! you awake?, 
case: cc-, evidence: 1: message to +16505551212 (sent) on 20-11-2025, 20:15:43: barely. need coffee first., 
case: cc-, evidence: 1: message from +16505551212 (received) on 20-11-2025, 20:15:52: same. rough night?, 
case: cc-, evidence: 1: message to +16505551212 (sent) on 20-11-2025, 20:16:14: i stayed up fixing that server issue., 
case: cc-, evidence: 1: message from +16505551212 (received) on 20-11-2025, 20:16:21: oh wow. did it finally work?, 
case: cc-, evidence: 1: message to +16505551212 (sent) on 20-11-2025, 20:16:29: yeah. took forever though., 
case: cc-, evidence: 1: message from +16505551212 (received) on 20-11-2025, 20:16:34: you're a hero lol., 
case: cc-, evidence: 1: message to +16505551212 (sent) on 20-11-2025, 20:16:40: i accept praise in the form of pastries., 
case: cc-, evidence: 1: message from +16505551212 (received) on 20-11-2025, 20:17:00: i'll see if there's donuts in the break room., 
case: cc-, evidence: 1: message to +17899977860 (sent) on 20-11-2025, 22:33:58: youve pushed me for the last time. keep it up and youre going to find out exactly why nobody crosses me twice., 
case: cc-, evidence: 1: message from +17899977860 (received) on 20-11-2025, 22:34:17: good. id hate for you to run when things get messy. lets see if you can handle what you started., 
case: cc-, evidence: 1: message to +17899977860 (sent) on 20-11-2025, 22:34:26: say whatever you want. youre about to learn that i dont back down., 
case: cc-, evidence: 1: message from +19999999999 (received) on 21-11-2025, 00:59:12: your so-called dawn legion is a stain on this realm. our order will reshape the world in shadow, whether your light survives or not., 
case: cc-, evidence: 1: message to +19999999999 (sent) on 21-11-2025, 00:59:24: your shadows are nothing but fear masquerading as strength. the legion will burn away every twisted doctrine your order spreads., 
case: cc-, evidence: 1: message from +19999999999 (received) on 21-11-2025, 00:59:34: you cling to that naive radiance like it protects you. the obsidian orders rise is inevitable. oppose us, and youll be swept aside with the rest of the deluded., 
case: cc-, evidence: 1: message to +19999999999 (sent) on 21-11-2025, 00:59:43: we dont bow to tyrants hiding behind darkness. if its a clash of convictions you want, the legion stands ready. we wont let your corruption swallow the realm., 
case: cc-, evidence: 1: message from +17899977860 (received) on 21-11-2025, 01:01:17: oh im shaking. you talk big but all i see is someone desperate to look tough., 
case: cc-, evidence: 1: contact: fazan. phone number: 7899977860. email: . 
case: cc-, evidence: 1: contact: unk. phone number: 6505551212. email: . 
case: cc-, evidence: 1: contact: fazan. phone number: 7899977861. email: . 
case: cc-, evidence: 1: call log incoming call, 6505551212 on 16-11-2025 23:47:19 lasting 3. 
case: cc-, evidence: 1: call log missed call, 6505551212 on 16-11-2025 23:47:29 lasting 0. 
case: cc-, evidence: 1: call log outgoing call, 6505551212 on 16-11-2025 23:47:37 lasting 2. 
case: cc-, evidence: 1: call log outgoing call, 6505551212 on 16-11-2025 23:47:43 lasting 0. 
case: cc-, evidence: 1: call log rejected call, 7899977860 on 16-11-2025 23:47:54 lasting 0. 
case: cc-, evidence: 1: call log rejected call, 7899977861 on 16-11-2025 23:48:21 lasting 0. 
"""
messages = load_input()
