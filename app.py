from flask import Flask, request, jsonify, render_template, send_from_directory
from langchain.callbacks import get_openai_callback
from flask_cors import CORS
from waitress import serve
from langchain.chat_models import ChatOpenAI
import os
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI


app = Flask(__name__)
CORS(app)

os.environ["OPENAI_API_KEY"] = "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"




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    # Get the file link and question from the request
    data = request.get_json()
    question = data['question']
   
    csvPath="data/Retail_Store.csv"
    with get_openai_callback() as cb:
    
        llm = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo',request_timeout=120)
        
        try:
            agent = create_csv_agent(OpenAI(temperature=0), csvPath)
            # Perform the question answering
            docs = agent.run(question)
            
            response = {
                'question': question,
                'answer': docs
            }
            
            return jsonify(response)
        
        except Exception as e:
            error_response = {
                'error': str(e)
            }
            response = {
                'question': question,
                'answer': error_response
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

