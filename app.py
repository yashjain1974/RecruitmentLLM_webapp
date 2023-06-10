from flask import Flask, request, jsonify, render_template, send_from_directory
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.callbacks import get_openai_callback
from flask_cors import CORS
from waitress import serve
from langchain.chat_models import ChatOpenAI
import os
import pickle
from langchain.document_loaders import StripeLoader
from langchain.indexes import VectorstoreIndexCreator
print("hello")
app = Flask(__name__)
CORS(app)

os.environ["OPENAI_API_KEY"] = "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"

#it is trial access token
os.environ["STRIPE_ACCESS_TOKEN"] = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"  # here strip"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    # Get the file link and question from the request
    data = request.get_json()
    question = data['question']
    #embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    stripe_loader = StripeLoader("charges")
    # index = VectorstoreIndexCreator().from_loaders([stripe_loader])
    with get_openai_callback() as cb:
        with open("vectorstore.pkl", "rb") as f:
            VectorStore = pickle.load(f)

        #RESULT WITH SOURCES
        llm = ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo')
        chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=VectorStore.as_retriever())
        #using stripe 
        #chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=index.vectorstore.as_retriever()) 

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
    # serve(app, host="0.0.0.0", port=80)
    app.run(host='0.0.0.0', port=80)

