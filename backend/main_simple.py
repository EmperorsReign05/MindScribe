import os
import asyncio
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
# Try to import from the newer package first, fallback to community
try:
    from langchain_ollama import OllamaLLM as Ollama, OllamaEmbeddings
except ImportError:
    from langchain_community.llms import Ollama
    from langchain_community.embeddings import OllamaEmbeddings

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import knowledge base - adjust path based on your file structure
try:
    from .knowledge_base import documents as docs
except ImportError:
    from knowledge_base import documents as docs

# --- APP and CORS setup ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for components
embeddings = None
llm = None
vector = None
document_chain = None
retriever = None

async def initialize_components():
    global embeddings, llm, vector, document_chain, retriever
    
    try:
        logger.info("Starting component initialization...")
        
        # Test Ollama connection first
        logger.info("Testing Ollama connection...")
        test_llm = Ollama(model="gemma:2b", timeout=10)
        test_response = test_llm.invoke("Hello")
        logger.info(f"Ollama test successful: {test_response[:50]}...")
        
        # Initialize embeddings (no timeout parameter for embeddings)
        logger.info("Initializing embeddings...")
        embeddings = OllamaEmbeddings(model="gemma:2b")
        
        # Initialize LLM
        logger.info("Initializing LLM...")
        llm = Ollama(model="gemma:2b", timeout=30)
        
        # Create vector store with smaller batch size
        logger.info(f"Creating vector store with {len(docs)} documents...")
        
        # Process documents in smaller batches to avoid timeout
        batch_size = 10
        if len(docs) > batch_size:
            logger.info(f"Processing documents in batches of {batch_size}")
            # Take first batch for initial vector store
            initial_docs = docs[:batch_size]
            vector = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: FAISS.from_documents(initial_docs, embeddings)
            )
            
            # Add remaining documents in batches
            for i in range(batch_size, len(docs), batch_size):
                batch_docs = docs[i:i+batch_size]
                logger.info(f"Adding batch {i//batch_size + 1}...")
                temp_vector = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: FAISS.from_documents(batch_docs, embeddings)
                )
                vector.merge_from(temp_vector)
        else:
            vector = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: FAISS.from_documents(docs, embeddings)
            )
        
        logger.info("Vector store created successfully")
        
        # Initialize prompt and chain
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
        
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vector.as_retriever(search_kwargs={"k": 3})  # Limit to top 3 results
        
        logger.info("All components initialized successfully!")
        
    except Exception as e:
        logger.error(f"Error initializing components: {e}")
        raise

# Initialize components at startup
@app.on_event("startup")
async def startup_event():
    await initialize_components()

# --- API ENDPOINT ---
class ChatRequest(BaseModel):
    message: str

async def stream_generator(request: ChatRequest) -> AsyncGenerator[str, None]:
    try:
        if not all([embeddings, llm, vector, document_chain, retriever]):
            yield "System is still initializing. Please wait a moment and try again."
            return
            
        logger.info(f"Processing message: {request.message}")
        
        # 1. Retrieve documents first
        retrieved_docs = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: retriever.invoke(request.message)
        )
        logger.info(f"Retrieved {len(retrieved_docs)} documents")

        # 2. Generate response
        try:
            full_response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: document_chain.invoke({
                    "input": request.message,
                    "context": retrieved_docs
                })
            )
            
            # Stream the response word by word
            words = full_response.split(' ')
            for i, word in enumerate(words):
                if i > 0:
                    yield ' '
                yield word
                await asyncio.sleep(0.03)  # Smaller delay for smoother streaming
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            yield f"I'm sorry, I encountered an error while processing your message. Please try again."

        # 3. Add sources
        separator = "\n\n---SOURCES---\n\n"
        sources = [doc.metadata for doc in retrieved_docs]
        yield separator + json.dumps(sources)
        
    except Exception as e:
        logger.error(f"Error in stream_generator: {e}")
        yield f"I'm sorry, I'm having trouble right now. Please try again in a moment."

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    logger.info(f"Received chat request: {request.message}")
    
    # Check if system is ready
    if not all([embeddings, llm, vector, document_chain, retriever]):
        return {"error": "System is still initializing. Please wait a moment."}
    
    return StreamingResponse(
        stream_generator(request), 
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.get("/health")
async def health_check():
    system_ready = all([embeddings, llm, vector, document_chain, retriever])
    return {
        "status": "healthy" if system_ready else "initializing",
        "message": "MindScribe API is running",
        "components_ready": system_ready,
        "documents_loaded": len(docs) if docs else 0
    }

@app.get("/status")
async def status_check():
    return {
        "embeddings_ready": embeddings is not None,
        "llm_ready": llm is not None,
        "vector_ready": vector is not None,
        "chain_ready": document_chain is not None,
        "retriever_ready": retriever is not None,
        "total_documents": len(docs) if docs else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)