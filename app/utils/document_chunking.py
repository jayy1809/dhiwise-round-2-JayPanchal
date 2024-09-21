from datetime import datetime

from openai import OpenAI

from app.config import OPENAI_API_KEY

openai_client = OpenAI(api_key=OPENAI_API_KEY)


def embeddings(text, model="text-embedding-3-small", dimensions=1536):
    try:
        response = openai_client.embeddings.create(
            input=text, model=model, dimensions=dimensions
        )
        return response.data[0].embedding

    except Exception as e:
        error_message = (
            f"Failed to create embeddings for text: {text}. Error: {str(e)}"
        )
        raise RuntimeError(error_message) from e


def chunk_and_embed_documents(documents, chunk_size=100):
    results = []

    for document in documents:
        try:
            file_name = document["file_name"]
            text = document["text"]
        except KeyError as e:
            error_message = f"Missing key in document: {str(e)}"
            raise KeyError(error_message) from e

        words = text.split()
        chunk_index = 1

        for i in range(0, len(words), chunk_size):
            word_chunk = words[i : i + chunk_size]
            chunk = " ".join(word_chunk)

            try:
                values = embeddings(chunk)
                result = {
                    "id": f"{file_name}#{chunk_index}",
                    "metadata": {
                        "text": chunk,
                        "filename": file_name,
                        "created_at": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    },
                    "values": values,
                }

                results.append(result)
                chunk_index += 1

            except RuntimeError as e:
                error_message = (
                    f"An error occurred while generating embeddings: {str(e)}"
                )
                raise RuntimeError(error_message) from e

    return results


def chunk_and_embed(text, chunk_size=100):
    words = text.split()
    chunk_index = 1
    results = []

    for i in range(0, len(words), chunk_size):
        word_chunk = words[i : i + chunk_size]
        chunk = " ".join(word_chunk)

        try:
            values = embeddings(chunk)
            result = {
                "id": f"transcript#{chunk_index}",
                "metadata": {
                    "text": chunk,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
                "values": values,
            }

            results.append(result)
            chunk_index += 1

        except RuntimeError as e:
            error_message = (
                f"An error occurred while generating embeddings: {str(e)}"
            )
            raise RuntimeError(error_message) from e

    return results
