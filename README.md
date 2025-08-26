MindScribe 🧠✨
MindScribe is an AI-powered wellness companion designed to be a supportive and empathetic listener. Built with a powerful RAG (Retrieval-Augmented Generation) pipeline, it provides context-aware, helpful conversations based on a curated knowledge base of therapeutic techniques.

By Team Synapse for IIC 

Features
RAG-Powered Conversations: The AI uses a knowledge base of therapeutic techniques (like CBT and Mindfulness) to provide informed and relevant responses.

Conversational Memory: The AI remembers previous parts of the conversation to provide context-aware and coherent support.

Real-time Streaming: Responses are streamed word-by-word, creating a fast and natural conversational experience.

User Authentication: Secure sign-up and login functionality powered by Supabase.

Persistent Chat History: Users can view and continue their past conversations, which are securely saved to their account.

Sourced Information: When appropriate, the AI provides sources for the information it shares, ensuring transparency and trust.

Modern UI: A clean, soothing, and responsive interface built with React and Tailwind CSS.

Tech Stack
Frontend: React, TypeScript, Vite, Tailwind CSS

Backend: Python, FastAPI

AI & NLP: LangChain, Gemini, FAISS (for vector storage)

Database & Auth: Supabase

Setup and Local Installation
To run this project on your local machine, follow these steps.

Prerequisites
Node.js and npm (or your preferred package manager)

Python 3.10+ and pip

Ollama installed and running with the gemma:2b model (ollama run gemma:2b)

1. Clone the Repository
Bash

git clone https://github.com/your-username/mindscribe.git
cd mindscribe
2. Frontend Setup
The frontend is a standard Vite + React application.

Bash

# Install frontend dependencies
npm install

# Create an environment file
# Create a new file named .env in the root directory
# and add your Supabase keys:
VITE_SUPABASE_PROJECT_URL=YOUR_SUPABASE_PROJECT_URL
VITE_SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY

# Run the frontend development server
npm run dev
The frontend will now be running on http://localhost:5173.

3. Backend Setup
The backend is a Python FastAPI server.

Bash

# Navigate to the backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install backend dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
The backend API will now be running on http://127.0.0.1:8000.

Deployment
The application is designed to be deployed with a service like Render for the backend and Netlify for the frontend.

Backend (Render)
Create a new Web Service on Render and connect your GitHub repository.

Set the Root Directory to backend.

Use the following commands:

Build Command: pip install -r requirements.txt

Start Command: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

Render will provide a URL for your live backend.

Frontend (Netlify)
Create a new site on Netlify and connect it to your GitHub repository.

Set the build settings:

Build command: npm run build

Publish directory: dist

Add an environment variable:

Key: VITE_BACKEND_URL

Value: The URL of your deployed Render backend.

Deploy the site.

Acknowledgments
UI components are based on the excellent shadcn/ui.

The RAG implementation is powered by the LangChain framework.

User authentication and database services are provided by Supabase.
