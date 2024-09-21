import os

from app.config import LOADING_DIRECTORY
from app.prompts.summary_prompt import (
    SUMMARY_SYSTEM_PROMPT,
    SUMMARY_TRANSCRIPT_QUERY,
    summary_user_prompt,
)
from app.utils.document_chunking import chunk_and_embed
from app.utils.llm_completion import get_chat_completion
from app.utils.pinecone_upsert import upsert_vectors
from app.utils.query_index import query_data
from app.utils.video_processing import process_video_transcription


def gen_summary(agenda, index_name, namespace):
    
    try:
        query = SUMMARY_TRANSCRIPT_QUERY
        system_prompt = SUMMARY_SYSTEM_PROMPT

        file_name = ""
        for file_name_details in os.listdir(LOADING_DIRECTORY):
            if file_name_details.endswith(".mp4"):
                file_name = file_name_details

        transcript = process_video_transcription(f"./data/{file_name}")

        vectors = chunk_and_embed(text=transcript)

        upsert_vectors(index_name=index_name, namespace=namespace, vectors=vectors)

        nodes = query_data(
            index_name=index_name, namespace=namespace, query=query, k_value=7
        )

        context = "\n".join([node.text for node in nodes])

        user_prompt = summary_user_prompt(transcript_data=context, agenda=agenda)

        summary = get_chat_completion(user_prompt, system_prompt)

        return summary
    
    except Exception as e:
        raise e
