from forensix.shared import *
from forensix.threat import analyze, generate, generate_query, run_query, convert_to_nlp

internal = Blueprint('internal', __name__, url_prefix='/internal')

@internal.route('/', methods=["GET"])
def internal_index():
    return make_response("Internal", 200)

@internal.route('/generateReport/<int: id>', methods=["GET"])
def generate_report(id):
    analyze(id)
    return make_response("", 200)

@internal.route('/nlp', methods=["POST"])
def nlp_query():
    data = request.form
    query = data['query']
    
    sql_query = generate_query(query)
    results = run_query(sql_query)
    output = convert_to_nlp(results)
    return make_response(output, 200)

