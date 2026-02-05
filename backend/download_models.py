from sentence_transformers import SentenceTransformer
import os

def download_model():
    print("Pre-downloading SentenceTransformer model...")
    # This matches the model used in main.py: "all-MiniLM-L6-v2"
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Model downloaded successfully.")

if __name__ == "__main__":
    download_model()
