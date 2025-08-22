import asyncio
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import logging

# Use the newer, recommended packages, with a fallback for compatibility
try:
    from langchain_ollama import OllamaLLM, OllamaEmbeddings
except ImportError:
    from langchain_community.llms import Ollama as OllamaLLM
    from langchain_community.embeddings import OllamaEmbeddings

from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Import knowledge base
try:
    from .knowledge_base import documents as docs
except ImportError:
    from knowledge_base import documents as docs

# --- Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global RAG Components ---
llm = None
retriever = None
document_chain = None
initialization_complete = False

# --- Application Startup Logic ---
@app.on_event("startup")
async def startup_event():
    global llm, retriever, document_chain, initialization_complete
    
    try:
        logger.info("Starting component initialization...")
        
        # 1. Initialize the Language Model
        llm = OllamaLLM(model="gemma:2b")
        logger.info("LLM initialized.")
        
        # 2. Initialize Embeddings (without the problematic timeout parameter)
        embeddings = OllamaEmbeddings(model="gemma:2b")
        logger.info("Embeddings initialized.")
        
        # 3. Create the Vector Store from documents
        logger.info(f"Creating vector store from {len(docs)} documents...")
        vector = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: FAISS.from_documents(docs, embeddings)
        )
        retriever = vector.as_retriever(search_kwargs={"k": 3})
        logger.info("Vector store and retriever created successfully.")
        
        # 4. Create the Prompt Template
        prompt = ChatPromptTemplate.from_template("""
You are MindScribe, a compassionate and empathetic AI wellness companion. Your primary role is to be a supportive listener.
- Validate the user's feelings and acknowledge what they are sharing.
- Do not give unsolicited advice or mention therapeutic techniques like CBT unless the user explicitly asks for help or coping strategies.
- Keep your responses concise, gentle, and encouraging.
- Ask open-ended questions to help the user explore their thoughts and feelings.

Use the following retrieved context ONLY if the user asks for specific information or techniques. Otherwise, ignore it.

<context>
{context}
</context>

User's message: {input}
Your supportive response:
""")
        
        # 5. Create the RAG Chain
        document_chain = create_stuff_documents_chain(llm, prompt)
        logger.info("RAG chain created.")
        
        initialization_complete = True
        logger.info("All components initialized successfully!")
        
    except Exception as e:
        logger.error(f"FATAL: Error during application startup: {e}")
        initialization_complete = False
        # Optionally, you can re-raise the exception to stop the server completely
        # raise e

# --- API Endpoint ---
class ChatRequest(BaseModel):
    message: str

async def stream_generator(request: ChatRequest) -> AsyncGenerator[str, None]:
    if not initialization_complete:
        yield "I'm sorry, the system is still starting up. Please try again in a moment."
        return

    try:
        # Retrieve documents and generate the response in the background
        retrieved_docs = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: retriever.invoke(request.message)
        )
        
        full_response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: document_chain.invoke({
                "input": request.message,
                "context": retrieved_docs
            })
        )

        # Stream the text response
        yield full_response

        # Stream the sources
        separator = "\n\n---SOURCES---\n\n"
        sources = [doc.metadata for doc in retrieved_docs]
        yield separator + json.dumps(sources)

    except Exception as e:
        logger.error(f"Error during response generation: {e}")
        yield "I'm sorry, I encountered an error. Please try again."

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return StreamingResponse(stream_generator(request), media_type="text/plain")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if initialization_complete else "initializing",
    }
