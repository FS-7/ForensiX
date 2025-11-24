from forensix.shared import *
from forensix.threat import analyze, generate_query, run_query, convert_to_nlp

internal = Blueprint('internal', __name__, url_prefix='/internal')

@internal.route('/', methods=["GET"])
def internal_index():
    return make_response("Internal", 200)

@internal.route('/generateReport/<int:id>', methods=["GET"])
def generate_report(id):
    response = analyze(id)
    print(response)
    return make_response(response, 200)

@internal.route('/nlp', methods=["POST"])
def nlp_query():
    data = request.form
    query = data['query']
    
    print(query)
    
    sql_query = generate_query(query)
    print("SQL:", sql_query)
    
    results = run_query(sql_query)
    print("Results: ", results)
    
    output = convert_to_nlp(results)
    print("Output: ", output)
    return make_response(output, 200)

