from dotenv.main import load_dotenv
import os
load_dotenv()
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
def generate_recruitment_question(prompt):
    # Set the temperature to control the randomness of the generated text
    temperature = 0.5

    # Set the probability threshold for top-p (nucleus) sampling
    top_p = 0.9

    # Set the maximum number of tokens in the response
    max_tokens = 150

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use GPT-3.5-turbo engine
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p
        )
        question = response['choices'][0]['text'].strip()
        return question
    except Exception as e:
        print(f"Error: {e}")
        return None

def validate_answer(question, candidate_answer):
    # Combine the question and candidate's answer as the new prompt
    prompt = f"Question:{question}\ncandidate_Answer: {candidate_answer}\n. Please provide a numerical rating on a scale of 1 to 10 to evaluate the quality and helpfulness of the Answer. 1 being the lowest. 10 be the highest. \nGive me only rating nothing else "

    # Set the temperature and max tokens for the response
    temperature = 1
    max_tokens = 150

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        validation_response = response['choices'][0]['text'].strip()
        print(validation_response)
        return validation_response
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    prompt = "You are the hiring manager for a growing tech company. Please generate a quiz based question for a python developer position. the question should be one word type and knowldege based."

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