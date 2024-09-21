import os

from dotenv import load_dotenv

load_dotenv(override=True)

INDEX_NAME = "meeting-management"
MEETING_DATA_NAMESPACE = "discussion-data"
TRANSCRIPT_DATA_NAMESPACE = "transcript"
LOADING_DIRECTORY = "./data"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
