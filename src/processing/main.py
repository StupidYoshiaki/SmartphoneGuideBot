import glob
import json
import os
import tempfile

from google.cloud import storage
from google.cloud.functions_v1.context import Context
from langchain.chat_models import ChatOpenAI
from llama_index import (
    GPTVectorStoreIndex,
    LLMPredictor,
    ServiceContext,
    StorageContext,
    download_loader,
)


SOURCE_BUCKET_NAME = "sgb-pdf-store"
TARGET_BUCKET_NAME = "sgb-vector-store"


def download_all_pdf_from_bucket(
    bucket: storage.Bucket, dir_name: str, dir_path: str
) -> None:
    # バケットからPDFをダウンロード
    blobs = bucket.list_blobs()
    for blob in blobs:
        file_path = os.path.join(dir_path, blob.name)
        blob.download_to_filename(file_path)


def vectorize_pdf_from_directory(directory: str, vector_filepath: str) -> None:
    # pdfをベクトル化し、一時ディレクトリに保存
    CJKPDFReader = download_loader("CJKPDFReader")
    loader = CJKPDFReader()
    documents = loader.load_data(directory=directory)
    service_context = ServiceContext.from_defaults(
        llm_predictor=LLMPredictor(
            llm=ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=0)
        )
    )
    index = GPTVectorStoreIndex.from_documents(
        documents, service_context=service_context
    )
    index.storage_context.persist(persist_dir=vector_filepath)


def upload_to_bucket(bucket: storage.Bucket, directory: str) -> None:
    # 一時ディレクトリに保存したベクトルをバケットにアップロード
    files = glob.glob(os.path.join(directory, "*.json"))
    for file_name in files:
        blob = bucket.blob(os.path.basename(file_name))
        blob.upload_from_filename(file_name)


###################


def main(event: dict, context: Context) -> str:
    client = storage.Client()
    source_bucket = client.get_bucket(SOURCE_BUCKET_NAME)

    # 一時ディレクトリを作成
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_dir_name = "pdf"
        pdf_dir_path = os.path.join(temp_dir, pdf_dir_name)
        vector_filepath = os.path.join(temp_dir, "storage")

        # 一時ディレクトリにPDFをダウンロード・ベクトル化
        download_all_pdf_from_bucket(source_bucket, pdf_dir_name, pdf_dir_path)
        vectorize_pdf_from_directory(pdf_dir_path, vector_filepath)

        # ベクトルをターゲットバケットにアップロード
        target_bucket = client.get_bucket(TARGET_BUCKET_NAME)
        upload_to_bucket(target_bucket, os.path.join(temp_dir, "storage"))

    return "OK"
