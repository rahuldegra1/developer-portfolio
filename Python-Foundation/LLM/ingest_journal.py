import chromadb
import os

print("Spinning up the Reader...")

# 1. Use PersistentClient to save the vector database directly to a folder
# This ensures the AI's memory survives after the script closes.
chroma_client = chromadb.PersistentClient(path="./local_memory_db")
collection = chroma_client.get_or_create_collection(name="personal_knowledge")

# 2. Check if the journal exists before trying to read it
journal_path = "leetcode/JOURNAL.md"  # Assuming it's in your root folder

if not os.path.exists(journal_path):
    print(f"Error: Could not find {journal_path}. Make sure it exists!")
else:
    # 3. Read the actual Markdown file
    with open(journal_path, "r", encoding="utf-8") as file:
        raw_text = file.read()

    # 4. Split the journal into individual chunks (paragraphs)
    # We split by double newline so each problem/note stays together
    chunks = raw_text.split("\n\n")

    # Clean up any empty chunks
    valid_chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    # Generate unique IDs for each chunk (entry_0, entry_1, etc.)
    ids = [f"journal_entry_{i}" for i in range(len(valid_chunks))]

    print(
        f"Found {len(valid_chunks)} distinct notes. Embedding them into math vectors..."
    )

    # 5. Push the real documents into the permanent database
    collection.add(documents=valid_chunks, ids=ids)

    print("Memory successfully saved to disk! Your AI can now read this file.")
