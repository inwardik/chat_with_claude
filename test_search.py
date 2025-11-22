"""
Script for testing document search (without MCP)
Use to verify indexing works correctly
"""
import os
from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv


def test_search():
    """Tests search through indexed documents"""
    # Load environment variables
    load_dotenv()

    chroma_db_path = os.getenv('CHROMA_DB_PATH', './chroma_db')
    model_name = os.getenv('EMBEDDING_MODEL', 'intfloat/multilingual-e5-large')

    # Check if database exists
    if not Path(chroma_db_path).exists():
        print("❌ Database not found!")
        print(f"Run first: python indexer.py")
        return

    print("Loading embedding model...")
    embedding_model = SentenceTransformer(model_name)

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(
        path=chroma_db_path,
        settings=Settings(anonymized_telemetry=False)
    )

    collection = client.get_collection("documents")
    print(f"✓ Database contains {collection.count()} documents\n")

    # Interactive search
    print("Enter search query (or 'exit' to quit):")
    print("-" * 60)

    while True:
        query = input("\n🔍 Query: ").strip()

        if query.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        if not query:
            continue

        # Create embedding for query
        query_embedding = embedding_model.encode([query])[0].tolist()

        # Search for similar documents
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        # Display results
        if results['documents'] and results['documents'][0]:
            print(f"\n📚 Found {len(results['documents'][0])} results:\n")

            for i, doc in enumerate(results['documents'][0], 1):
                metadata = results['metadatas'][0][i-1]
                distance = results['distances'][0][i-1]
                relevance = 1 - distance

                print(f"--- Result {i} ---")
                print(f"Source: {metadata['source']}")
                print(f"Relevance: {relevance:.1%}")
                print(f"\nText:\n{doc[:300]}...")
                if len(doc) > 300:
                    print(f"[...{len(doc) - 300} more characters]")
                print()
        else:
            print("❌ Nothing found")


if __name__ == '__main__':
    test_search()
