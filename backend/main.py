import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
import json
from .knowledge_base import documents as docs
# --- (APP and CORS setup remains the same) ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# --- (RAG CHAIN setup remains the same) ---
embeddings = OllamaEmbeddings(model="gemma:2b")
llm = Ollama(model="gemma:2b")
vector = FAISS.from_documents(docs, embeddings)#/
# ... (imports and other code remain the same)

# --- REFINED PROMPT ---
# This prompt encourages more listening and less direct instruction
prompt = ChatPromptTemplate.from_template("""
You are MindScribe, a compassionate and empathetic AI wellness companion. Your primary role is to be a supportive listener.
- Validate the user's feelings and acknowledge what they are sharing.
- Do not give unsolicited advice or mention therapeutic techniques like CBT unless the user explicitly asks for help or coping strategies.
- Keep your responses concise, gentle, and encouraging.
- Ask open-ended questions to help the user explore their thoughts and feelings.
- The user has not mentioned a presentation, so do not ask about one.

Use the following retrieved context ONLY if the user asks for specific information or techniques. Otherwise, ignore it.

<context>
{context}
</context>

User's message: {input}
Your supportive response:
""")


document_chain = create_stuff_documents_chain(llm, prompt)
retriever = vector.as_retriever()


# --- API ENDPOINT ---
class ChatRequest(BaseModel):
    message: str

async def stream_generator(request: ChatRequest):
    # 1. Retrieve documents first
    retrieved_docs = retriever.invoke(request.message)

    # 2. Stream the LLM response
    stream = document_chain.stream({
        "input": request.message,
        "context": retrieved_docs
    })

    # Yield the chunks of the response as they come in
    for chunk in stream:
        yield chunk

    # 3. After the stream is done, yield the sources
    # We use a special separator to distinguish sources from the main content
    separator = "\n\n---SOURCES---\n\n"
    sources = [doc.metadata for doc in retrieved_docs]
    yield separator + json.dumps(sources)


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return StreamingResponse(stream_generator(request), media_type="text/event-stream")