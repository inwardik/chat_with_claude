"""
Script for completely clearing ChromaDB database
"""
import os
from dotenv import load_dotenv
from indexer import DocumentIndexer


def main():
    """Clears entire document collection"""
    # Load environment variables
    load_dotenv()

    # Get parameters from .env
    chroma_db_path = os.getenv('CHROMA_DB_PATH', './chroma_db')
    embedding_model = os.getenv('EMBEDDING_MODEL', 'intfloat/multilingual-e5-large')

    print("Initializing...")
    # Create indexer
    indexer = DocumentIndexer(
        chroma_db_path=chroma_db_path,
        embedding_model=embedding_model
    )

    # Show current number of documents
    current_count = indexer.collection.count()
    print(f"Current number of items in database: {current_count}")

    if current_count == 0:
        print("Database is already empty.")
        return

    # Request confirmation
    response = input(f"\nAre you sure you want to delete all {current_count} items? (yes/no): ")

    if response.lower() in ['yes', 'y']:
        print("\nClearing database...")
        indexer.clear_collection()
        print("Database successfully cleared!")
    else:
        print("Operation cancelled.")


if __name__ == '__main__':
    main()
