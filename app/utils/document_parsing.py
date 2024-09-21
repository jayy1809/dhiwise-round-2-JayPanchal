import os
from collections import defaultdict
from datetime import datetime

from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse

from app.config import LLAMA_CLOUD_API_KEY

parser = LlamaParse(result_type="markdown", api_key=LLAMA_CLOUD_API_KEY)


def document_parser(directory_path):
    try:
        pdf_in_directory, txt_in_directory, md_in_directory = [], [], []

        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            file_ext = file.lower().endswith
            if file_ext(".pdf"):
                pdf_in_directory.append(file_path)
            elif file_ext(".txt"):
                txt_in_directory.append(file_path)
            elif file_ext(".md"):
                md_in_directory.append(file_path)

        file_extractor = {".pdf": parser}

        documents = []
        if pdf_in_directory:
            try:
                documents = SimpleDirectoryReader(
                    input_files=pdf_in_directory,
                    file_extractor=file_extractor,
                    filename_as_id=True,
                ).load_data()
            except Exception as e:
                error_message = f"Error reading PDF documents: {str(e)}"
                raise RuntimeError(error_message) from e

        grouped_documents = defaultdict(list)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for document in documents:
            try:
                file_name = document.metadata.get("file_name", "")
                text = document.text
                grouped_documents[file_name].append(text)
            except AttributeError as e:
                error_message = (
                    f"Error processing document attributes: {str(e)}"
                )
                raise AttributeError(error_message) from e

        for file_path in txt_in_directory + md_in_directory:
            try:
                file_name = os.path.basename(file_path)
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()
                    grouped_documents[file_name].append(text)
            except RuntimeError as e:
                error_message = f"Error reading file {file_path}: {str(e)}"
                raise RuntimeError(error_message) from e

        results = [
            {
                "file_name": file_name,
                "text": "\n".join(texts),
                "created_at": current_time,
            }
            for file_name, texts in grouped_documents.items()
        ]

        [
            os.remove(os.path.join(directory_path, f))
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f))
        ]

        return results

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        raise RuntimeError(error_message) from e
