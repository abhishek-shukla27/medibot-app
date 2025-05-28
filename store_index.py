from src.helper import load_pdf, text_split, download_hugging_face_embeddings
#from langchain.vectorstores import Pinecone
import pinecone
from dotenv import load_dotenv
import os
from pinecone import ServerlessSpec,Pinecone
from langchain_pinecone import PineconeVectorStore

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

print(PINECONE_API_KEY)
print(PINECONE_API_ENV)

extracted_data = load_pdf("C:\\Users\\Abhishek SHUKLA\\OneDrive\\Documents\\medibot\\End-to-end-Medical-Chatbot-using-Llama2-main\\data")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


#Initializing the Pinecone
pc=Pinecone(api_key="pcsk_EC9bZ_4bYKxBvtNskx9PC7xw8HkyfThrBVm7rbguQgAsKcm7dKYzKhXHgAif6vNPvyFkS")

index_name = "medicalbot"

pc.create_index(
    name=index_name,
    dimension=384, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

