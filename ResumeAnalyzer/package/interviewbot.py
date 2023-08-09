from dotenv.main import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import smtplib
import os
load_dotenv()
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
def send_email(customer_email,email_content):
    time_elapsed =5-2
    time_elapsed = format(time_elapsed, ".2f")
    # Read the content of the file
    # content="Once you have created your account, you will be able to access the course and start your Python programming journey. Our instructors will be there to guide you and provide support throughout the course."
    # Load the summarization chain
    # llm = OpenAI(temperature=0)


    # prompt_template = """Summarize the courses and recommend to buy it from the website brainlox.com.
    
    # {text}

    # Course recommendation
    # """

    # PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    # formatted_prompt = PROMPT.format(text=content)
    # llm_result = llm.generate([formatted_prompt])

    # generations = llm_result.generations
    # summary = generations[0][0]

    # Send summary via email
    RECRUITER_EMAIL = customer_email
    # FROM_EMAIL = "brainlox.ai@gmail.com"
    FROM_PASSWORD= os.getenv("FROM_PASSWORD")
    

    # Create a message
    msg = MIMEMultipart()

    # setup the parameters of the message
    msg['From']=" yashyash191174@gmail.com"
    msg['To']=customer_email
    msg['Subject']="Company Interview Result " + ""  #candidate_id

    # add in the message body
    message = """\
        <html>
            <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    color: #333;
                    max-width: 800px;
                    margin: auto;
                }}
                h2 {{
                    font-family: 'Roboto', sans-serif;
                    color: #2d3748;
                }}
                p {{
                    font-size: 14px;
                    line-height: 1.5;
                }}
                strong {{
                    color: #2d3748;
                }}
                em {{
                    color: #718096;
                }}
                .multiline {{
        white-space: pre-line; /* or pre-wrap */
    }}
                </style>
                </head>
            <body>
            <img src="https://www.teamplusindia.in/wp-content/uploads/2023/05/recruitment.jpg" alt="Interview">
                <div class="multiline">{content}</div>
                <hr>
                
    
                
                <p><em>This email was sent automatically by Interview .Kindly reply to this email for further info.</em></p>
            </body>
        </html>
        """.format(content=email_content)
    

    msg.attach(MIMEText(message, 'html'))

    # Setup the server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()

    # Login to the server
    server.login(msg['From'], FROM_PASSWORD)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()
def generate_recruitment_question(prompt):
    # Set the temperature to control the randomness of the generated text
    temperature = 0.5

    # Set the probability threshold for top-p (nucleus) sampling
    top_p = 0.9

    # Set the maximum number of tokens in the response
    max_tokens = 150

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5 Turbo model
            messages=[
                {"role": "system", "content": "You are the hiring manager."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p
        )
        question = response['choices'][0]['message']['content'].strip()
        return question
    except Exception as e:
        print(f"Error: {e}")
        return None

def validate_answer(question, candidate_answer):
    # Combine the question and candidate's answer as the new prompt
    prompt = f"Question: {question}\nCandidate Answer: {candidate_answer}\nPlease provide a numerical rating on a scale of 1 to 10 to evaluate the quality and helpfulness of the Answer. 1 being the lowest. 10 be the highest.\nGive me only rating nothing else."

    # Set the temperature and max tokens for the response
    temperature = 1
    max_tokens = 150

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5 Turbo model
            messages=[
                {"role": "system", "content": "Validation prompt."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        validation_response = response['choices'][0]['message']['content'].strip()
        print(validation_response)
        return validation_response
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    prompt = "You are the hiring manager for a growing tech company. Please generate a quiz based question for a python developer position. The question should be one-word type and knowledge-based."

    num_questions = 10
    generated_questions = set()  # Using a set to store unique questions
    while len(generated_questions) < num_questions:
        question = generate_recruitment_question(prompt)
        if question:
            generated_questions.add(question)

    if generated_questions:
        print("Generated Questions:")
        for idx, question in enumerate(generated_questions, start=1):
            print(f"{idx}. {question}")
            candidate_answer = input("Candidate Answer: ")
            validation_result = validate_answer(question, candidate_answer)
            print("Validation Result:")
            print(validation_result)
    else:
        print("Question generation failed.")