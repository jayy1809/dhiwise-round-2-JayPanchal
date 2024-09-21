## Get API keys from here 

To get started, you will need API keys from the following platforms:

- [Groq Console](https://console.groq.com/keys)
- [LlamaIndex](https://cloud.llamaindex.ai/api-key)
- [AssemblyAI](https://www.assemblyai.com/app/)
- [Pinecone](https://docs.pinecone.io/guides/get-started/quickstart)
- [OpenAI](https://platform.openai.com/api-keys)



## Setup

1. Clone the repository:
   ```
   git clone https://github.com/jayy1809/dhiwise-round-2-JayPanchal
   cd dhiwise-round-2-JayPanchal
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

once the repository is successfully cloned create a .env file and add api keys as shown in .env.example

### Starting the FastAPI Backend

1. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

### Starting the Streamlit Frontend

1. Open a new terminal window and activate the virtual environment (if not already activated).
    - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```



3. Start the Streamlit app:
   ```
   streamlit run meeting_frontend.py
   ```
