from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_path = Path(__file__).parent / "nodejs.pdf"

#Loading
loader = PyPDFLoader(pdf_path)
docs = loader.load() #Read PDF File

#Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size =1000,
    chunk_overlap =400
)
split_text = text_splitter.split_documents(documents =docs)

#Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

#Using embedding_model create embedding of split_text and store it in DB
vector_store = QdrantVectorStore.from_documents(
    documents=split_text,
    url ="http://localhost:6333",
    collection_name ="learning_vectors",
    embedding=embedding_model
)

print("Indexing of Document Done....")