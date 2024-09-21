from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

from app.config import OPENAI_API_KEY, PINECONE_API_KEY

pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
embed_model = OpenAIEmbedding(
    model="text-embedding-3-small", dimensions=1536, api_key=OPENAI_API_KEY
)


def query_data(index_name, namespace, query, k_value=10):
    try:
        pinecone_index = pinecone_client.Index(index_name)
    except Exception as e:
        error_message = (
            f"Error initializing Pinecone index '{index_name}': {str(e)}"
        )
        raise RuntimeError(error_message) from e

    try:
        vector_store = PineconeVectorStore(
            pinecone_index=pinecone_index, namespace=namespace
        )
        index = VectorStoreIndex.from_vector_store(vector_store)
    except Exception as e:
        error_message = f"Error setting up vector store with namespace '{namespace}': {str(e)}"
        raise RuntimeError(error_message) from e

    try:
        retriever = VectorIndexRetriever(
            index=index, similarity_top_k=k_value, embed_model=embed_model
        )
        nodes = retriever.retrieve(query)
    except Exception as e:
        error_message = f"Error retrieving data with query '{query}': {str(e)}"
        raise RuntimeError(error_message) from e

    return nodes
