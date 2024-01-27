import os
from dotenv import load_dotenv
from pathlib import Path
from llama_index import download_loader
from llama_index import ServiceContext, LLM, VectorStoreIndex
from langchain_openai import ChatOpenAI

# .envファイルの内容を読み込み
load_dotenv()

# APIキーの取得
os.environ["OPENAI_API_KEY"] = os.environ.get("API_KEY")

# PDFファイルの読み込み
PDFReader = download_loader("PDFReader")
loader = PDFReader()
documents = loader.load_data(file=Path("./doc/guide.pdf"))

# indexを作成するための設定
service_context = ServiceContext.from_defaults(
    llm_predictor=LLM(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=0)
    )
)

# indexを作成
index = VectorStoreIndex.from_documents(documents, service_context=service_context)
index.storage_context.persist(persist_dir="./storage/")
