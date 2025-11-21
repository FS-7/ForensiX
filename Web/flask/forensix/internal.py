from forensix.shared import *
from forensix import threat, parser

internal = Blueprint('internal', __name__, url_prefix='/internal')
internal.register_blueprint(threat.threat)
internal.register_blueprint(parser.parser)

@internal.route('/', methods=["Get"])
def internal_index():
    return make_response("", 200)

@internal.route('/preprocess')
def preprocessing():
    Normalize()
    GenerateEmbeddings()
    return

@internal.route('/classify')
def classify():
    
    return 

@internal.route('/llm_safety', methods=["POST"])
def llm_safety():
    data = request.data
    query = json.loads(data)
    return make_response(text_gen(query), 200)

def text_gen(query):
    device = "cpu"
    model_path = "ibm-granite/granite-4.0-h-1b"

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    model.eval()
        
    embedding_manager=EmbeddingManager()
    vectorstore = VectorStore('txt_messages', '../Data/vector_store')
    rag_retriever=RAGRetriever(vectorstore,embedding_manager)
    
    sms_documents = parser.parseSMS_CSV(loc="../../AI/Extraction/Data/")
    
    chunks = split_documents(sms_documents)
    texts = [doc.page_content for doc in chunks]
    embeddings = embedding_manager.generate_embeddings(texts)
    vectorstore.add_documents(sms_documents, embeddings)

    results = rag_retriever.retrieve(query=query)
    context="\n\n".join([doc['content'] for doc in results]) if results else ""
    if not context:
        output = ["No relevant context found to answer the question."]
    else:
        chat = [
            { 
            "role": "user", 
            "content": f"""Use the following context to answer the question concisely. Context: {context}, Question: {query}."""
            }
        ]

        chat = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

        input_tokens = tokenizer(chat, return_tensors="pt").to(device)
        output = model.generate(**input_tokens, max_new_tokens=50)
        output = tokenizer.batch_decode(output)

    return output[0]

def Normalize():
    return

def GenerateEmbeddings():
    return