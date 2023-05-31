import pickle

from flask import Flask, request, jsonify, render_template, send_from_directory
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.callbacks import get_openai_callback
from flask_cors import CORS
from waitress import serve
from langchain.chat_models import ChatOpenAI
import os

app = Flask(__name__)
CORS(app)

os.environ["OPENAI_API_KEY"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    # Get the file link and question from the request
    data = request.get_json()
    question = data['question']
    #embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    with get_openai_callback() as cb:
        with open("brainlox_embeddings.pkl", "rb") as f:
            VectorStore = pickle.load(f)

        #RESULT WITH SOURCES
        llm = ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo')
        chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=VectorStore.as_retriever())

        answer = chain({"question": question}, return_only_outputs=True)

        # llm = ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo')
        # chain = load_qa_chain(llm, chain_type="stuff")
        #
        # # Perform the question answering
        # docs = VectorStore.similarity_search(question)
        # answer = chain.run(input_documents=docs, question=question)

        print(answer)
        print(cb)
    # Return the answer as a JSON response
    #return jsonify ({'answer': answer})
    return answer

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.',
                               'ai-plugin.json',
                               mimetype='application/json')


@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=80)
