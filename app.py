from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
from langchain.llms import OpenAI
from bot_app import BabyAGI
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore import InMemoryDocstore
from typing import Dict, List, Optional, Any
from dotenv.main import load_dotenv
app = Flask(__name__)
CORS(app)
load_dotenv()


embeddings_model = OpenAIEmbeddings()
embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_pdf', methods=['POST'])
def process_pdf():

    
    embeddings_model = OpenAIEmbeddings()
    # Initialize the vectorstore as empty
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})


    
    llm = OpenAI(temperature=0)
    # Logging of LLMChains
    verbose = False
    # Get the file link and question from the request

    data = request.get_json()
    question = data['question']
    
   
    # If None, will keep on going forever
    max_iterations: Optional[int] = 3
    try:
        baby_agi = BabyAGI.from_llm(
            llm=llm, vectorstore=vectorstore, verbose=verbose, max_iterations=max_iterations
        )
        # baby_agi({"objective": question})
    
        output = baby_agi._call(data)
        print(output)
        print(output["final_result"])
        response = {
                    'question': question,
                    
                'task_list': output['task_list'],       # Replace with the actual task list
                'next_task': output['next_task'],       # Replace with the actual next task
                'task_result': output['task_result'],     # Replace with the actual task result
                'task_ending': output['task_ending']  ,  # Replace with the actual task ending
                'final_result': output['final_result']    # Replace with the actual task ending
        
                }
        return jsonify(response)
    except Exception as e:
        error_response = {
                'error': str(e)
            }
        response = {
                'question': question,
                'final_result': error_response
            }
        return jsonify(error_response)  # Return HTTP 500 status code for error

        

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.',
                               'ai-plugin.json',
                               mimetype='application/json')


@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')


if __name__ == '__main__':
    # serve(app, host="0.0.0.0", port=80)
    app.run(host='0.0.0.0', port=80)

