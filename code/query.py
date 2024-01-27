import os
from dotenv import load_dotenv
from llama_index import StorageContext, load_index_from_storage
from langchain_openai import ChatOpenAI
from llama_index import PromptTemplate

PROMPT_TEMPLATE = (
  "下記の情報が与えられています。 \n"
  "---------------------\n"
  "{context_str}"
  "\n---------------------\n"
  "この情報を参照して3個の箇条書きで次の質問に答えてください: {query_str}\n"
  "また、出典となるPDFのページ番号を教えてください。\n"
)
PROMPT = PromptTemplate(PROMPT_TEMPLATE)

  
def query2answer(query_str: str) -> str:
  """
  クエリを投げて回答を返す
  query_str: 質問文
  """
  storage_context = StorageContext.from_defaults(persist_dir="./storage")
  index = load_index_from_storage(storage_context)
  query_engine = index.as_query_engine(text_qa_template=PROMPT)
  response = query_engine.query(query_str)
  return response


if __name__ == "__main__":
  # .envファイルの内容を読み込み
  load_dotenv()

  # APIキーの取得
  os.environ["OPENAI_API_KEY"] = os.environ.get("API_KEY")

  # クエリを投げる
  response = query2answer("LINE Payの使い方を教えてください。")
  
  # 回答を表示
  print(response)