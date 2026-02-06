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
from langchain_openai import ChatOpenAI
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

# Import knowledge base
try:
    from .knowledge_base import documents as docs
except ImportError:
    from knowledge_base import documents as docs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

# CORS middleware
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
        "https://synapse-mindscribe.netlify.app/",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
llm = None
retriever = None
prompt_template = None
initialization_complete = False
initialization_error = None

# Store conversation history
conversation_history = {}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request completed in {process_time:.2f}s with status {response.status_code}")
    return response

@app.on_event("startup")
async def startup_event():
    global llm, retriever, prompt_template, initialization_complete, initialization_error
    
    try:
        logger.info("Starting component initialization...")
        initialization_complete = False
        initialization_error = None
        
        # Get API keys
        groq_api_key = os.getenv("GOOGLE_API_KEY")  # Using same env var as before
        cohere_api_key = os.getenv("COHERE_API_KEY")
        
        if not groq_api_key:
            logger.error("GOOGLE_API_KEY environment variable is not set!")
            initialization_error = "GOOGLE_API_KEY environment variable is required"
            return
            
        if not cohere_api_key:
            logger.error("COHERE_API_KEY environment variable is not set!")
            initialization_error = "COHERE_API_KEY environment variable is required for embeddings"
            return
        
        # Initialize LLM with Groq
        try:
            llm = ChatOpenAI(
                model="openai/gpt-oss-120b",
                temperature=0.7,
                api_key=groq_api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            test_response = await llm.ainvoke("Hello")
            logger.info(f"Groq LLM initialized successfully: {test_response.content[:50]}...")
        except Exception as e:
            logger.error(f"Failed to initialize Groq LLM: {e}")
            initialization_error = f"Groq LLM initialization failed: {str(e)}"
            return
        
        # Initialize Cohere Embeddings (cloud-based, lightweight!)
        try:
            embeddings = CohereEmbeddings(
                cohere_api_key=cohere_api_key,
                model="embed-english-v3.0"
            )
            # Test embeddings
            test_embedding = embeddings.embed_query("test")
            logger.info(f"Cohere Embeddings initialized successfully (dimension: {len(test_embedding)})")
        except Exception as e:
            logger.error(f"Failed to initialize Cohere embeddings: {e}")
            initialization_error = f"Cohere embeddings initialization failed: {str(e)}"
            return
        
        # Create vector store from knowledge base
        try:
            logger.info(f"Creating vector store from {len(docs)} documents...")
            if not docs or len(docs) == 0:
                logger.warning("No documents found in knowledge base")
                initialization_error = "No documents found in knowledge base"
                return
            
            vector = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: FAISS.from_documents(docs, embeddings)
            )
            retriever = vector.as_retriever(search_kwargs={"k": 5})
            
            # Test retriever
            test_docs = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: retriever.invoke("test query")
            )
            logger.info(f"Vector store created successfully, retrieved {len(test_docs)} test documents")
        except Exception as e:
            logger.error(f"Failed to create vector store: {e}")
            initialization_error = f"Vector store creation failed: {str(e)}"
            return
        
        # Create prompt template
        try:
            prompt_template = ChatPromptTemplate.from_template("""
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
            logger.info("Prompt template created successfully")
        except Exception as e:
            logger.error(f"Failed to create prompt template: {e}")
            initialization_error = f"Prompt template creation failed: {str(e)}"
            return
        
        initialization_complete = True
        logger.info("All components initialized successfully with Groq LLM + Cohere Embeddings!")
        
    except Exception as e:
        logger.error(f"FATAL: Error during application startup: {e}")
        initialization_complete = False
        initialization_error = str(e)

# Conversation history functions
def get_conversation_context(user_id: str, current_message: str) -> str:
    if not user_id or user_id not in conversation_history:
        return ""
    
    history = conversation_history[user_id]
    recent_history = history[-6:] if len(history) > 6 else history
    
    context_string = ""
    for msg in recent_history:
        role = "User" if msg["is_user"] else "MindScribe"
        context_string += f"{role}: {msg['message']}\n"
    
    return context_string

def add_to_conversation_history(user_id: str, message: str, is_user: bool):
    if not user_id:
        return
    
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    conversation_history[user_id].append({
        "message": message,
        "is_user": is_user,
        "timestamp": time.time()
    })
    
    if len(conversation_history[user_id]) > 20:
        conversation_history[user_id] = conversation_history[user_id][-20:]

# API Endpoint
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

async def stream_generator(request: ChatRequest) -> AsyncGenerator[str, None]:
    try:
        if request.user_id:
            logger.info(f"Processing message from user: {request.user_id}")
        else:
            logger.info("Processing message from anonymous user")

        if not request.message or not request.message.strip():
            yield "I'd love to hear what's on your mind. Please share something with me so I can help you better."
            return

        greeting_pattern = r'^\s*(hi|hello|hey|heya|yo|whatsup|wassup|good\s+(morning|afternoon|evening)|greetings)\s*[!.]*\s*$'
        if re.match(greeting_pattern, request.message, re.IGNORECASE):
            yield "Hello! I'm here to provide you with evidence-based therapeutic support. How are you feeling today, and what would you like to work on together?"
            return

        if not initialization_complete:
            if initialization_error:
                yield f"I'm sorry, there was an error starting up the system: {initialization_error}. Please contact support."
            else:
                yield "I'm sorry, the system is still starting up. Please try again in a moment."
            return

        if not all([llm, retriever, prompt_template]):
            yield "I'm sorry, some components are not properly initialized. Please try again later."
            return

        # Get conversation context
        conversation_context = get_conversation_context(request.user_id or "anonymous", request.message)
        add_to_conversation_history(request.user_id or "anonymous", request.message, True)

        logger.info(f"Processing message: {request.message[:100]}...")
        
        # RAG: Retrieve relevant documents
        try:
            retrieved_docs = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: retriever.invoke(request.message)
            )
            logger.info(f"Retrieved {len(retrieved_docs)} documents")
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            retrieved_docs = []

        # Generate response with RAG context
        try:
            context_text = "\n\n".join([doc.page_content for doc in retrieved_docs]) if retrieved_docs else ""
            
            formatted_prompt = prompt_template.format_messages(
                input=request.message,
                context=context_text,
                conversation_history=conversation_context
            )
            
            response_obj = await llm.ainvoke(formatted_prompt)
            full_response = response_obj.content
            
            if not full_response or not full_response.strip():
                full_response = "I understand you're reaching out for support. Could you tell me more about what you're experiencing right now? I'm here to help you with evidence-based therapeutic techniques."
                
            logger.info(f"Generated response: {full_response[:100]}...")
            add_to_conversation_history(request.user_id or "anonymous", full_response, False)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            full_response = "I'm having trouble processing your message right now, but I'm here to help. Could you try rephrasing what you'd like to work on therapeutically?"

        yield full_response

    except Exception as e:
        logger.error(f"Critical error in stream_generator: {e}")
        yield "I'm sorry, I encountered an unexpected error. Please try again, and if the problem persists, please contact support."

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
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
            "prompt_template": prompt_template is not None,
            "documents_loaded": len(docs) if docs else 0
        },
        "ai_provider": "Groq/OpenAI Compatible (openai/gpt-oss-120b)",
        "embeddings_provider": "Cohere (embed-english-v3.0)",
        "mode": "RAG with Cloud Embeddings",
        "timestamp": time.time(),
        "active_conversations": len(conversation_history)
    }

@app.get("/ping")
def ping():
    return "OK"

@app.get("/")
async def root():
    return {"message": "MindScribe Therapeutic AI with RAG is running", "version": "2.2.0"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {exc}")
    return HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
