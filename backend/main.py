import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

# --- 1. SET UP THE FASTAPI APP ---
app = FastAPI()

# Allow all origins for CORS (important for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. LOAD YOUR KNOWLEDGE BASE (EXAMPLE) ---
# In a real app, you would load your CBT/Mindfulness documents here.
# For this example, we'll use a simple string as our knowledge base.
knowledge_base_text = """
Cognitive Behavioral Therapy (CBT) is a type of psychotherapy that helps people to change unhelpful thinking and behavior patterns.
One key technique is cognitive restructuring, where you identify, challenge, and reframe negative automatic thoughts.
For example, if a user feels they failed a presentation, a helpful reframe is to focus on what they learned from the experience and what they did well, rather than just the negative aspects.
Another technique is mindfulness, which involves paying attention to the present moment without judgment. A simple mindfulness exercise is to focus on your breath, noticing the sensation of inhalation and exhalation.
"""

# Split the text into manageable chunks
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_text(knowledge_base_text)

# Create Document objects
docs = [Document(page_content=t) for t in documents]

# --- 3. CREATE THE RAG CHAIN ---
# Initialize Ollama embeddings and the main LLM
embeddings = OllamaEmbeddings(model="gemma:2b")
llm = Ollama(model="gemma:2b")

# Create a FAISS vector store from the documents
vector = FAISS.from_documents(docs, embeddings)

# Create the prompt template
prompt = ChatPromptTemplate.from_template("""
You are MindScribe, a compassionate AI wellness companion.
Use the following retrieved context to inform your response in a caring, conversational tone.
Do not mention the context directly. If it's not relevant, ignore it.

<context>
{context}
</context>

Question: {input}
""")

# Create the main chain that combines the documents and the prompt
document_chain = create_stuff_documents_chain(llm, prompt)

# Create the retriever from the vector store
retriever = vector.as_retriever()

# --- 4. DEFINE THE API ENDPOINT ---
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Create a simple chain to pass the input to the retriever
        retrieval_chain = retriever | document_chain
        
        # Invoke the chain with the user's message
        response = await retrieval_chain.ainvoke({"input": request.message})
        
        return {"reply": response}
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return {"error": "Internal server error"}

# --- 5. DEFINE A ROOT ENDPOINT FOR HEALTH CHECKS ---
@app.get("/")
def read_root():
    return {"Hello": "MindScribe Backend"}