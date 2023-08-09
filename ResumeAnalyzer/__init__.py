from flask import Flask, render_template, request, session, redirect, url_for
from package.interviewbot import generate_recruitment_question, validate_answer,send_email

from azure.storage.blob import BlobServiceClient
from io import StringIO,BytesIO
from flask_cors import CORS
from dotenv.main import load_dotenv
from langchain.llms import OpenAI
from langchain.llms import OpenAIChat
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain import LLMChain, PromptTemplate
import tempfile
import random
load_dotenv()
import fitz
import os
import re
app = Flask(__name__)
connection_str= os.getenv('AZURE_STORAGE_CONNECTION_STRING')

print(connection_str)

container_name = "csv"
blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_str)
try:
    container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored
    container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
except Exception as e:
    print(e)
    print("Creating container...")
    container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist
container_client.get_container_properties() #
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def extract_text_from_pdf(pdf_path):
    resume_text = ""
    pdf_document = fitz.open(pdf_path)
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        resume_text += page.get_text("text")
    pdf_document.close()
    return resume_text
@app.route('/')
def index():
    return render_template('main.html')
@app.route('/analyze_cv')
def analyseCv():
    return render_template('analyzeCV.html')
@app.route('/analyze_job')
def analyseJob():
    return render_template('analyzeJob.html')
@app.route('/analyze_job', methods=['POST'])
def upload_job():
    if request.method == 'POST':
        if 'file' in request.files:  # User chose the file upload option
            file = request.files['file']
            filenames=""
            if file:
                try:
                    container_client.upload_blob(f"{file.filename}", file,overwrite=True) # upload the file to the container using the filename as the blob name
                    filenames += file.filename + "<br /> "
                except Exception as e:
                    print(e)
                    print("Ignoring duplicate filenames") # ignore duplicate filenames
                blob_client = container_client.get_blob_client(file.filename) # get blob client to interact with the blob and get blob url
                with BytesIO() as input_blob:
                    blob_client.download_blob().download_to_stream(input_blob)
                    input_blob.seek(0)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                        temp_file.write(input_blob.read())
                        temp_file_path = temp_file.name
                    resume_text = extract_text_from_pdf(temp_file_path)
                    os.remove(temp_file_path)
            
                template = """
                For the following job description pdf, extract the following: company name, job description, company description, 
                job requirements. Start each group following this pattern: [<GROUP NAME>], e.g. for 'Skills' do '[SKILLS]'. 
                Return the information as detailed as possible
    

                {chat_history}
                {human_input}"""
            
                prompt = PromptTemplate(
                    input_variables=["chat_history", "human_input"],
                    template=template
                )

                memory = ConversationBufferMemory(memory_key="chat_history")

                llm_chain = LLMChain(
                    llm=OpenAIChat(model="gpt-3.5-turbo"),
                    prompt=prompt,
                    verbose=True,
                    memory=memory,
                )

                res = llm_chain.predict(human_input=resume_text)
                print(res)
                return render_template('analyzeJob.html', parsed_resume=res, error=None)
            else:
                return render_template('analyzeJob.html', parsed_resume=None, error='Error uploading file. Only PDFs are allowed.')
        elif 'job_description' in request.form:  # User chose the textarea option
            job_description = request.form['job_description']
            template = """
                For the following job description text, extract the following: company name, job description, company description, 
                job requirements. Start each group following this pattern: [<GROUP NAME>], e.g. for 'Skills' do '[SKILLS]'. 
                Return the information as detailed as possible
    

                {chat_history}
                {human_input}"""
            
            prompt = PromptTemplate(
                    input_variables=["chat_history", "human_input"],
                    template=template
                )

            memory = ConversationBufferMemory(memory_key="chat_history")

            llm_chain = LLMChain(
                    llm=OpenAIChat(model="gpt-3.5-turbo"),
                    prompt=prompt,
                    verbose=True,
                    memory=memory,
                )

            res = llm_chain.predict(human_input=job_description)

            return render_template('analyzeJob.html', parsed_resume=res, error=None)
    return render_template('analyzeJob.html', parsed_resume=None, error='Error uploading file.')

@app.route('/analyze_cv', methods=['POST'])
def upload_cv():
    if request.method == 'POST':
        file = request.files['file']
        filenames=""
        if file:
            try:
                container_client.upload_blob(f"{file.filename}", file,overwrite=True) # upload the file to the container using the filename as the blob name
                filenames += file.filename + "<br /> "
            except Exception as e:
                print(e)
                print("Ignoring duplicate filenames") # ignore duplicate filenames
            blob_client = container_client.get_blob_client(file.filename) # get blob client to interact with the blob and get blob url
            with BytesIO() as input_blob:
                blob_client.download_blob().download_to_stream(input_blob)
                input_blob.seek(0)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(input_blob.read())
                    temp_file_path = temp_file.name
                resume_text = extract_text_from_pdf(temp_file_path)
                os.remove(temp_file_path)
           
            template = """
        Extract information from the CV provided. Return the information grouped under the following: Contact, 
            Academic Background, Professional Experience, Skills, Other. Start each group following this pattern: 
            [<GROUP NAME>], e.g. for 'Skills' do '[SKILLS]'. Return the information as detailed as possible.
            CV:
   

    {chat_history}
    {human_input}"""
           
            prompt = PromptTemplate(
                input_variables=["chat_history", "human_input"],
                template=template
            )

            memory = ConversationBufferMemory(memory_key="chat_history")

            llm_chain = LLMChain(
                llm=OpenAIChat(model="gpt-3.5-turbo"),
                prompt=prompt,
                verbose=True,
                memory=memory,
            )

            res = llm_chain.predict(human_input=resume_text)
            print(res)
            return render_template('analyzeCV.html', parsed_resume=res, error=None)
        else:
            return render_template('analyzeCV.html', parsed_resume=None, error='Error uploading file. Only PDFs are allowed.')
    return render_template('analyzeCV.html', parsed_resume=None, error='Error uploading file.')

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "pdf"

app.secret_key = "12uwnasdfw" 

programming_topics = [
    "Variables and Data Types",
    "Operators and Expressions",
    "Control Flow (if-else, loops)",
    "Functions and Methods",
    "Object-Oriented Programming (OOP)",
    "Classes and Objects",
    "Inheritance and Polymorphism",
    "Encapsulation and Abstraction",
    "File Handling and I/O",
    "Exception Handling",
    "Recursion",
    "Data Structures (Lists, Sets, Tuples, Dictionaries)",
    "Algorithms (Sorting, Searching, etc.)",
    "Regular Expressions",
    "Lambda Functions",
    "Functional Programming",
    "Generators and Iterators",
    "Decorators",
    "Modules and Packages",
    "Namespaces and Scope",
    "Closures",
    "Multithreading and Multiprocessing",
    "Networking and Socket Programming",
    "Web Scraping",
    "JSON and APIs",
    "GUI Programming (Tkinter, PyQt, etc.)",
    "Database Interaction (SQL, SQLite, etc.)",
    "Unit Testing and Test-Driven Development (TDD)",
    "Debugging Techniques",
    "Performance Optimization",
    "Design Patterns",
    "Software Development Life Cycle (SDLC)",
    "Version Control (Git, SVN, etc.)",
    "Continuous Integration and Deployment (CI/CD)",
    "Security Best Practices in Programming",
    "Concurrency and Parallel Programming",
    "Asynchronous Programming (async/await)",
    "Data Serialization (XML, JSON, Pickle, etc.)",
    "Interprocess Communication (IPC)",
    "Code Documentation and Commenting"
]
@app.route('/welcomePage')
def welcome():
    return render_template('welcome.html')

@app.route('/interview',methods=['GET', 'POST'])
def interview():
    

    
    
    
    # Initialize session variable if not present
    if 'email' not in session:
        session['email'] = ""
    if 'name' not in session:
        session['name'] = ""
    
    if request.method == 'POST':
        # Retrieve the email and name from the form
        email = request.form.get('email')
        name = request.form.get('name')
        session['email'] = email
        session['name'] = name
    
   
    if 'question_count' not in session:
        session['question_count'] = 0

    # Check if the user has reached the limit of 10 questions
    if session['question_count'] >= 5:
                total_score = sum(session.get('individual_scores'))
                
        
               
                session.clear()

        # Render the thank you template
                return render_template('thank_you.html',total_score=total_score)

    # Generate a question
    random_topic = random.choice(programming_topics)
    prompt = f"You are the hiring manager for a growing tech company. Please generate a quiz type question for a Java developer position related to  {random_topic}"
    question = generate_recruitment_question(prompt)

    # Increment the question count in the session
    session['question_count'] += 1

    # Render the template with the question
    return render_template('new_index.html',question=question,question_count=session['question_count'])


@app.route('/validate', methods=['POST'])
def validate():
   

    question = request.form['question']
    candidate_answer = request.form['candidate_answer']
    print(question)
    print(candidate_answer)

    # Validate the answer and get the score
   
    def is_integer_string(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    # Assuming you have the 'score' variable as a string
    score = validate_answer(question, candidate_answer)
    print("score=",score)
    # Check if the score is an integer string
    if is_integer_string(score):
        score = int(score)
    else:
        score = 0
    if 'individual_scores' not in session:
        session['individual_scores'] = 0
    print("score2=",score)
    # Append the current score to the list of individual scores
    session['individual_scores']+=score
    print("Individual Scores:", session['individual_scores'])

    # Check if the user has completed 10 questions
    print("Session_question=",session['question_count'])
    if session['question_count'] >= 5:
        # Calculate the total score
        total_score = session['individual_scores']
        print("Total Score:", total_score)
        llm = OpenAI(temperature=0.9)
        prompt = PromptTemplate(
        input_variables=["name","score","cutoff","company_name"],
        template="""
                    You work at a company named {company_name}. 
                    Your job is to write official mails to candidaes informing them if they have passed or failed the hiring test.
                    To pass the test the candidate must score above the cutoff score of {cutoff} out of 100.
                    You only have to write the body of the email and nothing else. 
                    The name of the candidate is {name}. The candidate scored {score} marks out of 100. Write an email to inform them about the result.
                    You only have to write if the candidate passed or failed. Do not reveal their marks under any circumstances.
                    """,
                    )
                
        chain = LLMChain(llm=llm, prompt=prompt)
        cutoff=35
        k=chain.run({
                "name":session['name'],
                "cutoff":cutoff,

                "score":total_score,
                "company_name":"Axis bank Recruitment team",
        })
        send_email(session['email'],k)
        session.clear()  # Clear the session data after calculating the total score

        # Render the thank you template with the total score
        return render_template('thank_you.html', total_score=total_score)


    # Render the template with the score and the next question
    return render_template('score.html', question=question,answer= candidate_answer, score=score)
if __name__ == "__main__":
    app.run(debug=True)
