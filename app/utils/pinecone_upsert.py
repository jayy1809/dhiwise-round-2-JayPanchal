import time

from pinecone import Pinecone,  ServerlessSpec

from app.config import PINECONE_API_KEY

pinecone_client = Pinecone(api_key=PINECONE_API_KEY)


def upsert_vectors(index_name, namespace, vectors, batch_size=15):
    try:
        if index_name not in pinecone_client.list_indexes().names():
            pinecone_client.create_index(
                name=index_name,
                dimension=1536,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                ),
                deletion_protection="disabled"
            )
            while not pinecone_client.describe_index(index_name).status['ready']:
                time.sleep(1)
        index = pinecone_client.Index(index_name)
        time.sleep(2)
    except Exception as e:
        error_message = (
            f"Error initializing Pinecone index '{index_name}': {str(e)}"
        )
        raise RuntimeError(error_message) from e

    for i in range(0, len(vectors), batch_size):
        vectors_chunk = vectors[i : i + batch_size]
        try:
            index.upsert(vectors=vectors_chunk, namespace=namespace)

            time.sleep(5)
        except Exception as e:
            error_message = (
                f"Error upserting vector chunk starting at index {i}: {str(e)}"
            )
            raise RuntimeError(error_message) from e
