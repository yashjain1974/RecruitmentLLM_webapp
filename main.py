import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pickle
from langchain import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI
import pylibmagic
from langchain.document_loaders import SeleniumURLLoader,PlaywrightURLLoader
from langchain.document_loaders import PlaywrightURLLoader

import os
os.environ["OPENAI_API_KEY"]


def extract_urls(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Create BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all anchor tags (a) in the HTML
    anchor_tags = soup.find_all('a')

    # Extract the URLs from the anchor tags
    urls = []
    for tag in anchor_tags:
        href = tag.get('href')
        if href:
            absolute_url = urljoin(url, href)  # Make relative URLs absolute
            urls.append(absolute_url)

    return urls


website_url = 'https://brainlox.com/'  # Replace with your desired website URL
urls = extract_urls(website_url)
for url in urls:
    print(url)
#
loaders = SeleniumURLLoader(urls=urls)
data = loaders.load()


text_splitter = CharacterTextSplitter(separator='\n',
                                      chunk_size=2000,
                                      chunk_overlap=200)


docs = text_splitter.split_documents(data)

embeddings = OpenAIEmbeddings()
vectorStore_openAI = FAISS.from_documents(docs, embeddings)

with open("brainlox_embeddings.pkl", "wb") as f:
    pickle.dump(vectorStore_openAI, f)

# with open("brainlox_embeddings.pkl", "rb") as f:
#     VectorStore = pickle.load(f)
#
# llm = ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo')
#
# chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=VectorStore.as_retriever())
#
# print(chain({"question": "Tell me about Brainlox"}, return_only_outputs=True))