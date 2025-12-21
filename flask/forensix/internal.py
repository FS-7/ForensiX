from forensix.shared import *
from forensix.threat import analyze, generate_query, run_query, convert_to_nlp

internal = Blueprint('internal', __name__, url_prefix='/internal')

@internal.route('/', methods=["GET"])
def internal_index():
    return make_response("Internal", 200)

@internal.route('/generateReport/<int:id>', methods=["GET"])
def generate_report(id):
    print("Generating Report...")
    response = analyze(id)
    print(response)
    print("Report Generated")
    return make_response(response, 200)

@internal.route('/nlp', methods=["POST"])
def nlp_query():
    print("User Query...")
    
    data = request.form
    id = data["id"]
    query = data['query']
    
    print(query)
    
    print("Query to SQL...")
    sql_query = generate_query(query)
    print("SQL:", sql_query)
    
    if sql_query in [None, ""]:
        return make_response("Error", 200)
    
    print("Executing SQL Query")
    results = run_query(sql_query, id)
    
    if results in [None, ""]:
        return make_response("Error", 200)
    
    tabbed_results = ""
    val = []
    for res in results:
        val.append(' | '.join(res))
    tabbed_results = ' \n'.join(val)
    
    print(tabbed_results)
    
    print("SQL to Table...")
    output = ""#convert_to_nlp(tabbed_results)
    print("Output: ", output)
    return make_response(output, 200)

