from app.config import LOADING_DIRECTORY
from app.prompts.agenda_prompt import (
    AGENDA_DOCUMENT_QUERY,
    AGENDA_SYSTEM_PROMPT,
    agenda_user_prompt,
)
from app.utils.document_chunking import chunk_and_embed_documents
from app.utils.document_parsing import document_parser
from app.utils.llm_completion import get_chat_completion
from app.utils.pinecone_upsert import upsert_vectors
from app.utils.query_index import query_data


def gen_agenda(discussion_data, index_name, namespace):
    try:
        query = AGENDA_DOCUMENT_QUERY
        system_prompt = AGENDA_SYSTEM_PROMPT

        documents = document_parser(directory_path=LOADING_DIRECTORY)

        vectors = chunk_and_embed_documents(documents=documents)

        upsert_vectors(
            index_name=index_name, namespace=namespace, vectors=vectors
        )

        nodes = query_data(
            index_name=index_name, namespace=namespace, query=query
        )

        node_content = ""
        for node in nodes:
            node_content += f"\n{node.text}"

        discussion_content = ""
        for discussion_point in discussion_data:
            discussion_point = f"""
            Name: {discussion_point.name}
            Department: {discussion_point.department}
            Discussion Points: {discussion_point.discussion_points}\n
            """
            discussion_content += discussion_point

        user_prompt = agenda_user_prompt(
            discussion_data=discussion_content, node_content=node_content
        )

        response = get_chat_completion(
            user_prompt=user_prompt, system_prompt=system_prompt
        )

        return response

    except Exception as e:
        raise e
