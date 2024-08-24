# HR Recruitment Automation System

![image](https://github.com/yashjain1974/SIH_HR-recruitmet_webapp/assets/69360295/546252d5-4813-455b-9e39-327d534cada0)
*Automated HR recruitment process overview*

## Project Description

This Flask application automates key aspects of the HR recruitment process, particularly for evaluating Python developer candidates. The application dynamically generates random programming questions from a list of topics using a language model (LLM) and allows candidates to answer them. Their responses are validated and scored, streamlining the recruitment workflow.

## Demo Video

[Demo Video](https://www.youtube.com/watch?v=Gd2wnMj4fBQ)

## Features

- **Random Question Generation:** Uses LLM to dynamically generate random programming questions.
- **PDF Parsing and Analysis:** Extracts and processes text from uploaded PDFs (job descriptions, resumes).
- **Context Management:** Maintains session state to track candidate progress and scores using Python cookie sessions.
- **Azure Blob Storage Integration:** Securely manages file uploads for scalable storage solutions.
- **Dynamic Content Generation:** Utilizes `LLMChain` and `PromptTemplate` for generating and evaluating questions.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yashjain1974/RecruitmentLLM_webapp.git
    cd RecruitmentLLM_webapp
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**
    Create a `.env` file in the root directory and add your Azure Storage connection string and OpenAI API key:
    ```env
    AZURE_STORAGE_CONNECTION_STRING="your_azure_storage_connection_string"
    OPENAI_API_KEY="your_openai_api_key"
    ```

4. **Run the application:**
    ```bash
    python app.py
    ```

## Usage

1. **Navigate to the main page:**
    Open your browser and go to `http://127.0.0.1:5000/`.

2. **Analyze Job Descriptions and Resumes:**
    - Upload PDFs or enter text to analyze job descriptions and resumes.
    - Extract detailed information and insights.

3. **Conduct Interviews:**
    - Generate random programming questions for candidates.
    - Validate and score candidate responses.

4. **Session Management:**
    - Track progress and scores across multiple sessions.

## Screenshots

![image](https://github.com/yashjain1974/SIH_HR-recruitmet_webapp/assets/69360295/712e1c8e-3288-4abd-b3a6-e3fdb41551c3)
![image](https://github.com/yashjain1974/SIH_HR-recruitmet_webapp/assets/69360295/691fd57b-c626-4c4d-99f8-6da5f1389fbc)
*Main page of the HR recruitment automation system.*

![image](https://github.com/yashjain1974/SIH_HR-recruitmet_webapp/assets/69360295/acbd652a-0b1c-40c2-8845-1cfe5fee000a)
*Analyze CV page where users can upload candidate resumes.*

![image](https://github.com/yashjain1974/SIH_HR-recruitmet_webapp/assets/69360295/82bed4bf-f6cd-498f-a69e-8ed92694c31f)
*Technical assessment Page *

![image](https://github.com/yashjain1974/SIH_HR-recruitmet_webapp/assets/69360295/fbc00b01-6f4e-41c9-b9e2-e4a3c5711fb0)
*Interview page with dynamically generated questions.*

![image](https://github.com/yashjain1974/SIH_HR-recruitmet_webapp/assets/69360295/323a4358-3fc8-48e3-8e9a-3dbf76f5a969)
*Thank you page showing the total score after completing the interview Quiz*

![image](https://github.com/yashjain1974/SIH_HR-recruitmet_webapp/assets/69360295/52ee32b4-f4d7-4545-bcf3-a9703270d2de)
*Final assessment Page*

![image](https://github.com/yashjain1974/SIH_HR-recruitmet_webapp/assets/69360295/e35efb3e-da84-4694-9cfc-7c61a9c0e0f8)
*Final Assessment page with dynamically generated questions. Question s generated from pdf*

![image](https://github.com/yashjain1974/SIH_HR-recruitmet_webapp/assets/69360295/cb60a7ab-d2ba-4b86-a4c9-4ce45cd96ef7)
*Validation page for score generated for each question* 

![image](https://github.com/yashjain1974/SIH_HR-recruitmet_webapp/assets/69360295/20af21d1-dc0e-4d62-a05a-443b93feb596)
*Automatic Email generation for Interview result to candidate*





## Challenges Faced

1. **Maintaining Context Across Sessions:**
   - **Solution:** Implemented Python cookie sessions to track questions answered and scores.

2. **PDF Parsing and Information Extraction:**
   - **Solution:** Used `PyMuPDF` for text extraction and LLMs for structured information processing.

3. **File Storage and Management:**
   - **Solution:** Integrated Azure Blob Storage for secure and scalable file handling.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, please contact [yash191174@gmail.com](yash191174@gmail.com).

---

*This project automates significant parts of the HR recruitment process, making it more efficient and effective.*

