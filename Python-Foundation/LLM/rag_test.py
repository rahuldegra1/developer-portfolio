import chromadb
import requests

# 1. Connect to the permanent memory on your hard drive
# (Since the folder was created inside LLM/, we point the path there)
chroma_client = chromadb.PersistentClient(path="./local_memory_db")
collection = chroma_client.get_collection(name="personal_knowledge")

# 2. Get real input from the user
print("\n--- LOCAL RAG SYSTEM INITIALIZED ---")
user_question = input("Ask a question about your coding journal: ")

# 3. Retrieve the matching context from your actual journal
results = collection.query(query_texts=[user_question], n_results=1)

# Extract the most relevant chunk
retrieved_context = results["documents"][0][0]
print("\n[Found relevant note in memory...]")

# 4. Prompt Injection
rag_prompt = f"""You are a helpful AI assistant. Answer the user's question using ONLY the provided context.

Context: 
{retrieved_context}

User Question: 
{user_question}
"""

# 5. Route to local Qwen model via FastAPI
LOCAL_API_URL = "http://localhost:8000/generate_code"
payload = {"prompt": rag_prompt}

try:
    response = requests.post(LOCAL_API_URL, json=payload)
    response_data = response.json()

    print("\n--- QWEN'S ANSWER ---")
    print(response_data.get("response", response_data))

except requests.exceptions.ConnectionError:
    print("\n[ERROR] Connection refused. Is Uvicorn running?")
