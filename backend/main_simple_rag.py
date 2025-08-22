import asyncio
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import logging

# Try to import from the newer package first, fallback to community
try:
    from langchain_ollama import OllamaLLM as Ollama, OllamaEmbeddings
except ImportError:
    from langchain_community.llms import Ollama
    from langchain_community.embeddings import OllamaEmbeddings

from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Import knowledge base
try:
    from .knowledge_base import documents as docs
except ImportError:
    from knowledge_base import documents as docs

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- APP and CORS setup ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
embeddings = None
llm = None
vector = None
document_chain = None
retriever = None
initialization_complete = False

@app.on_event("startup")
async def startup_event():
    global embeddings, llm, vector, document_chain, retriever, initialization_complete
    
    try:
        logger.info("Starting component initialization...")
        
        # Initialize LLM first
        logger.info("Initializing LLM...")
        llm = Ollama(model="gemma:2b")
        
        # Test LLM connection
        logger.info("Testing LLM connection...")
        test_response = llm.invoke("Hello")
        logger.info(f"LLM test successful: {test_response[:50]}...")
        
        # Initialize embeddings (simpler, no timeout)
        logger.info("Initializing embeddings...")
        embeddings = OllamaEmbeddings(model="gemma:2b")
        
        # Create vector store with a smaller subset first
        logger.info(f"Creating vector store with {len(docs)} documents...")
        logger.info("This may take a few minutes for the first time...")
        
        # Create vector store in executor to avoid blocking
        vector = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: FAISS.from_documents(docs, embeddings)
        )
        
        logger.info("Vector store created successfully!")
        
        # Set up prompt
        prompt = ChatPromptTemplate.from_template("""
You are MindScribe, a compassionate and empathetic AI wellness companion. Your primary role is to be a supportive listener.

- Validate the user's feelings and acknowledge what they are sharing
- Keep your responses concise, gentle, and encouraging
- Ask open-ended questions to help the user explore their thoughts and feelings
- Only mention specific techniques from the context if the user explicitly asks for help or coping strategies

Context (use only when relevant):
{context}

User's message: {input}

Your supportive response:""")
        
        # Create document chain
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vector.as_retriever(search_kwargs={"k": 3})
        
        initialization_complete = True
        logger.info("All components initialized successfully!")
        
    except Exception as e:
        logger.error(f"Error during initialization: {e}")
        initialization_complete = False
        raise

class ChatRequest(BaseModel):
    message: str

async def stream_generator(request: ChatRequest) -> AsyncGenerator[str, None]:
    try:
        if not initialization_complete:
            yield "System is still initializing. Please wait a moment and try again."
            return
            
        logger.info(f"Processing message: {request.message}")
        
        # Retrieve relevant documents
        retrieved_docs = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: retriever.invoke(request.message)
        )
        logger.info(f"Retrieved {len(retrieved_docs)} documents")

        # Generate response
        try:
            full_response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: document_chain.invoke({
                    "input": request.message,
                    "context": retrieved_docs
                })
            )
            
            # Stream the response
            words = full_response.split(' ')
            for i, word in enumerate(words):
                if i > 0:
                    yield ' '
                yield word
                await asyncio.sleep(0.05)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            yield "I'm sorry, I encountered an error while processing your message. Please try again."

        # Add sources
        separator = "\n\n---SOURCES---\n\n"
        sources = [doc.metadata for doc in retrieved_docs]
        yield separator + json.dumps(sources)
        
    except Exception as e:
        logger.error(f"Error in stream_generator: {e}")
        yield "I'm sorry, I'm having trouble right now. Please try again in a moment."

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    logger.info(f"Received chat request: {request.message}")
    
    if not initialization_complete:
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
    return {
        "status": "healthy" if initialization_complete else "initializing",
        "message": "MindScribe API is running",
        "initialization_complete": initialization_complete,
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
        "initialization_complete": initialization_complete,
        "total_documents": len(docs) if docs else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)