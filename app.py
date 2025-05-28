from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain.vectorstores import Pinecone
import pinecone
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *
import os
from pinecone import ServerlessSpec,Pinecone
from langchain_pinecone import PineconeVectorStore

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')


embeddings = download_hugging_face_embeddings()

#Initializing the Pinecone
pc=Pinecone(api_key=PINECONE_API_KEY,
            environment=PINECONE_API_ENV)

index_name="medicalbot"

#Loading the index
docsearch=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings,
)


PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])

chain_type_kwargs={"prompt": PROMPT}

llm=CTransformers(model="C:\\Users\\Abhishek SHUKLA\\OneDrive\\Documents\\medibot\\End-to-end-Medical-Chatbot-using-Llama2-main\\model",
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.8})


qa=RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs)



@app.route("/")
def index():
    return render_template('chat.html')



@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg.lower().strip()
    print(input)

    greetings=["hello",'hi',"hey","good morning","good evening"]
    if input in greetings:
        return "👋 Hello! I'm MediBot, your medical assistant. How can I help you today?"
    result=qa({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)


