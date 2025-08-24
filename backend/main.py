import asyncio
import os
from typing import AsyncGenerator, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import logging
import re
import time
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
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
        "https://*.netlify.app",  # Add your Netlify domain
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

# Store conversation history (in production, use a proper database)
conversation_history = {}

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
        
       
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise Exception("GOOGLE_API_KEY environment variable is required")
        
        
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",  # Latest and fastest Gemini model
                temperature=0.7,
                google_api_key=google_api_key,
                convert_system_message_to_human=True
            )
            # Test the LLM connection
            test_response = await llm.ainvoke("Hello")
            logger.info(f"Gemini LLM initialized and tested successfully: {test_response.content[:50]}...")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini LLM: {e}")
            raise Exception(f"Gemini LLM initialization failed: {str(e)}")
        
        # Initialize embeddings with Gemini
        try:
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=google_api_key
            )
            # Test embeddings
            test_embedding = await embeddings.aembed_query("test")
            logger.info(f"Gemini Embeddings initialized successfully (dimension: {len(test_embedding)})")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini embeddings: {e}")
            raise Exception(f"Gemini embeddings initialization failed: {str(e)}")
        
        # Create vector store
        try:
            logger.info(f"Creating vector store from {len(docs)} documents...")
            if not docs or len(docs) == 0:
                raise Exception("No documents found in knowledge base")
            
            vector = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: FAISS.from_documents(docs, embeddings)
            )
            retriever = vector.as_retriever(search_kwargs={"k": 5})  # Increased from 3 to 5
            
            # Test retriever
            test_docs = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: retriever.invoke("test query")
            )
            logger.info(f"Vector store created successfully, retrieved {len(test_docs)} test documents")
        except Exception as e:
            logger.error(f"Failed to create vector store: {e}")
            raise Exception(f"Vector store creation failed: {str(e)}")
        
        # Create document chain with UPDATED PROMPT
        try:
            prompt = ChatPromptTemplate.from_template("""
You are MindScribe, a professional AI therapy assistant with expertise in evidence-based therapeutic techniques. Your role is to provide structured, practical therapeutic guidance while being empathetic and supportive.

CONVERSATION HISTORY (for context):
{conversation_history}

RETRIEVED THERAPEUTIC KNOWLEDGE:
{context}

CURRENT USER MESSAGE: {input}

INSTRUCTIONS:
1. ALWAYS acknowledge the user's feelings and validate their experience
2. ALWAYS provide relevant therapeutic techniques, exercises, or insights from the knowledge base when available
3. Structure your response as: [Acknowledgment] → [Therapeutic Insight/Technique] → [Practical Application]
4. Be specific and actionable - give concrete steps, not just general advice
5. If the knowledge base contains relevant information, prioritize it and explain the technique clearly
6. Remember previous context from conversation history to provide continuity
7. If discussing specific conditions (anxiety, depression, stress), provide targeted evidence-based techniques
8. Always maintain a professional yet warm therapeutic tone

RESPONSE FORMAT:
- Start by acknowledging their feelings/situation
- Provide specific therapeutic technique(s) or insights
- Give clear, step-by-step instructions when applicable
- Offer gentle follow-up questions to encourage engagement

Your response:
""")
            
            document_chain = create_stuff_documents_chain(llm, prompt)
            
            # Test the chain
            test_result = await document_chain.ainvoke({
                "input": "Hello",
                "context": [],
                "conversation_history": ""
            })
            logger.info(f"Document chain created and tested successfully: {test_result[:50]}...")
        except Exception as e:
            logger.error(f"Failed to create document chain: {e}")
            raise Exception(f"Document chain creation failed: {str(e)}")
        
        initialization_complete = True
        logger.info("All components initialized successfully with Gemini!")
        
    except Exception as e:
        logger.error(f"FATAL: Error during application startup: {e}")
        initialization_complete = False
        initialization_error = str(e)

# Function to manage conversation history
def get_conversation_context(user_id: str, current_message: str) -> str:
    """Get the last few messages for context"""
    if not user_id or user_id not in conversation_history:
        return ""
    
    history = conversation_history[user_id]
    # Get last 6 messages (3 exchanges) for context
    recent_history = history[-6:] if len(history) > 6 else history
    
    context_string = ""
    for msg in recent_history:
        role = "User" if msg["is_user"] else "MindScribe"
        context_string += f"{role}: {msg['message']}\n"
    
    return context_string

def add_to_conversation_history(user_id: str, message: str, is_user: bool):
    """Add message to conversation history"""
    if not user_id:
        return
    
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    conversation_history[user_id].append({
        "message": message,
        "is_user": is_user,
        "timestamp": time.time()
    })
    
    # Keep only last 20 messages to prevent memory issues
    if len(conversation_history[user_id]) > 20:
        conversation_history[user_id] = conversation_history[user_id][-20:]

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
            yield "I'd love to hear what's on your mind. Please share something with me so I can help you better."
            return

        # Handle simple greetings with more therapeutic approach
        greeting_pattern = r'^\s*(hi|hello|hey|heya|yo|whatsup|wassup|good\s+(morning|afternoon|evening)|greetings)\s*[!.]*\s*$'
        if re.match(greeting_pattern, request.message, re.IGNORECASE):
            yield "Hello! I'm here to provide you with evidence-based therapeutic support. How are you feeling today, and what would you like to work on together?"
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

        # Get conversation context
        conversation_context = get_conversation_context(request.user_id or "anonymous", request.message)
        
        # Add current user message to history
        add_to_conversation_history(request.user_id or "anonymous", request.message, True)

        # Process the message
        logger.info(f"Processing message: {request.message[:100]}...")
        
        # Retrieve documents - always try to get relevant information
        try:
            retrieved_docs = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: retriever.invoke(request.message)
            )
            logger.info(f"Retrieved {len(retrieved_docs)} documents")
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            retrieved_docs = []  # Continue without documents

        # Generate response using async invoke
        try:
            full_response = await document_chain.ainvoke({
                "input": request.message,
                "context": retrieved_docs,
                "conversation_history": conversation_context
            })
            
            if not full_response or not full_response.strip():
                full_response = "I understand you're reaching out for support. Could you tell me more about what you're experiencing right now? I'm here to help you with evidence-based therapeutic techniques."
                
            logger.info(f"Generated response: {full_response[:100]}...")
            
            # Add AI response to history
            add_to_conversation_history(request.user_id or "anonymous", full_response, False)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            full_response = "I'm having trouble processing your message right now, but I'm here to help. Could you try rephrasing what you'd like to work on therapeutically?"

        # Stream the text response
        yield full_response

        # Stream the sources if available
        '''if retrieved_docs:
            try:
                separator = "\n\n---THERAPEUTIC SOURCES---\n\n"
                sources = [doc.metadata for doc in retrieved_docs if hasattr(doc, 'metadata')]
                if sources:
                    yield separator + json.dumps(sources, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"Error processing sources: {e}")'''

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
        "ai_provider": "Google Gemini 2.0 Flash",
        "timestamp": time.time(),
        "active_conversations": len(conversation_history)
    }

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {"message": "MindScribe Therapeutic AI is running with Gemini 2.0 Flash", "version": "2.0.0"}

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