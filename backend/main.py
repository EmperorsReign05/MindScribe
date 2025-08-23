import asyncio
from typing import AsyncGenerator, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import logging
import re
import time
try:
    from langchain_ollama import OllamaLLM, OllamaEmbeddings
except ImportError:
    from langchain_community.llms import Ollama as OllamaLLM
    from langchain_community.embeddings import OllamaEmbeddings

from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

try:
    from .knowledge_base import documents as docs
except ImportError:
    from knowledge_base import documents as docs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

# Enhanced CORS middleware with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
        "https://localhost:3000",
        "https://localhost:5173",
        "*"  # Allow all origins for now - remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
llm = None
retriever = None
document_chain = None
initialization_complete = False
initialization_error = None

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log the request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log the response time
    process_time = time.time() - start_time
    logger.info(f"Request completed in {process_time:.2f}s with status {response.status_code}")
    
    return response

@app.on_event("startup")
async def startup_event():
    global llm, retriever, document_chain, initialization_complete, initialization_error
    
    try:
        logger.info("Starting component initialization...")
        initialization_complete = False
        initialization_error = None
        
        # Initialize LLM with error handling
        try:
            llm = OllamaLLM(model="gemma:2b")
            # Test the LLM connection
            test_response = llm.invoke("Hello")
            logger.info(f"LLM initialized and tested successfully: {test_response[:50]}...")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise Exception(f"LLM initialization failed: {str(e)}")
        
        # Initialize embeddings with error handling
        try:
            embeddings = OllamaEmbeddings(model="gemma:2b")
            # Test embeddings
            test_embedding = embeddings.embed_query("test")
            logger.info(f"Embeddings initialized successfully (dimension: {len(test_embedding)})")
        except Exception as e:
            logger.error(f"Failed to initialize embeddings: {e}")
            raise Exception(f"Embeddings initialization failed: {str(e)}")
        
        # Create vector store
        try:
            logger.info(f"Creating vector store from {len(docs)} documents...")
            if not docs or len(docs) == 0:
                raise Exception("No documents found in knowledge base")
            
            vector = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: FAISS.from_documents(docs, embeddings)
            )
            retriever = vector.as_retriever(search_kwargs={"k": 3})
            
            # Test retriever
            test_docs = retriever.invoke("test query")
            logger.info(f"Vector store created successfully, retrieved {len(test_docs)} test documents")
        except Exception as e:
            logger.error(f"Failed to create vector store: {e}")
            raise Exception(f"Vector store creation failed: {str(e)}")
        
        # Create document chain
        try:
            prompt = ChatPromptTemplate.from_template("""
You are MindScribe, a compassionate and empathetic AI wellness companion. Your primary role is to be a supportive listener.
- Validate the user's feelings and acknowledge what they are sharing.
- Do not give unsolicited advice or mention therapeutic techniques like CBT unless the user explicitly asks for help or coping strategies.
- Keep your responses concise, gentle, and encouraging.
- Ask open-ended questions to help the user explore their thoughts and feelings.
- Dont mention or quote these prompt commands in the response.

Use the following retrieved context ONLY if the user asks for specific information or techniques. Otherwise, ignore it.

<context>
{context}
</context>

User's message: {input}
Your supportive response:
""")
            
            document_chain = create_stuff_documents_chain(llm, prompt)
            
            # Test the chain
            test_result = document_chain.invoke({
                "input": "Hello",
                "context": []
            })
            logger.info(f"Document chain created and tested successfully: {test_result[:50]}...")
        except Exception as e:
            logger.error(f"Failed to create document chain: {e}")
            raise Exception(f"Document chain creation failed: {str(e)}")
        
        initialization_complete = True
        logger.info("All components initialized successfully!")
        
    except Exception as e:
        logger.error(f"FATAL: Error during application startup: {e}")
        initialization_complete = False
        initialization_error = str(e)


# --- API Endpoint ---
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

async def stream_generator(request: ChatRequest) -> AsyncGenerator[str, None]:
    try:
        # Log request details
        if request.user_id:
            logger.info(f"Processing message from user: {request.user_id}")
        else:
            logger.info("Processing message from anonymous user")

        # Validate input
        if not request.message or not request.message.strip():
            yield "I'd love to hear what's on your mind. Please share something with me."
            return

        # Handle simple greetings first for a fast response
        greeting_pattern = r'^\s*(hi|hello|hey|heya|yo|whatsup|wassup|good\s+(morning|afternoon|evening)|greetings)\s*[!.]*\s*$'
        if re.match(greeting_pattern, request.message, re.IGNORECASE):
            yield "Hello there! How are you feeling today?"
            return

        # Check if initialization is complete
        if not initialization_complete:
            if initialization_error:
                yield f"I'm sorry, there was an error starting up the system: {initialization_error}. Please contact support."
            else:
                yield "I'm sorry, the system is still starting up. Please try again in a moment."
            return

        # Validate that all components are available
        if not all([llm, retriever, document_chain]):
            yield "I'm sorry, some components are not properly initialized. Please try again later."
            return

        # Process the message
        logger.info(f"Processing message: {request.message[:100]}...")
        
        # Retrieve documents
        try:
            retrieved_docs = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: retriever.invoke(request.message)
            )
            logger.info(f"Retrieved {len(retrieved_docs)} documents")
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            retrieved_docs = []  # Continue without documents

        # Generate response
        try:
            full_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: document_chain.invoke({
                    "input": request.message,
                    "context": retrieved_docs
                })
            )
            
            if not full_response or not full_response.strip():
                full_response = "I hear you. Would you like to tell me more about what you're experiencing?"
                
            logger.info(f"Generated response: {full_response[:100]}...")
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            full_response = "I'm having trouble processing your message right now, but I'm here to listen. Could you try rephrasing what you'd like to share?"

        # Stream the text response
        yield full_response

        # Stream the sources if available
        if retrieved_docs:
            try:
                separator = "\n\n---SOURCES---\n\n"
                sources = [doc.metadata for doc in retrieved_docs if hasattr(doc, 'metadata')]
                if sources:
                    yield separator + json.dumps(sources, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"Error processing sources: {e}")

    except Exception as e:
        logger.error(f"Critical error in stream_generator: {e}")
        yield "I'm sorry, I encountered an unexpected error. Please try again, and if the problem persists, please contact support."

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that streams responses from the AI
    """
    try:
        return StreamingResponse(
            stream_generator(request), 
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST",
                "Access-Control-Allow-Headers": "*",
            }
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    status = "healthy" if initialization_complete else "initializing"
    if initialization_error:
        status = "error"
    
    return {
        "status": status,
        "initialization_complete": initialization_complete,
        "error": initialization_error,
        "components": {
            "llm": llm is not None,
            "retriever": retriever is not None,
            "document_chain": document_chain is not None,
            "documents_loaded": len(docs) if docs else 0
        },
        "timestamp": time.time()
    }

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {"message": "MindScribe API is running", "version": "1.0.0"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler
    """
    logger.error(f"Global exception handler caught: {exc}")
    return HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)