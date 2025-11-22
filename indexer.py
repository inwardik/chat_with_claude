"""
Script for indexing documents into ChromaDB vector database
"""
import io
import sys
import os
from pathlib import Path
from typing import List

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from utils import read_file, split_text_into_chunks, get_all_documents, get_relative_path


class DocumentIndexer:
    """Indexes documents into ChromaDB"""

    def __init__(
        self,
        chroma_db_path: str,
        embedding_model: str,
        collection_name: str = "documents"
    ):
        """
        Initializes the document indexer

        Args:
            chroma_db_path: Path to ChromaDB database
            embedding_model: Name of model for creating embeddings
            collection_name: Name of collection in ChromaDB
        """
        self.chroma_db_path = chroma_db_path
        self.collection_name = collection_name

        # Create database folder if it doesn't exist
        Path(chroma_db_path).mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=chroma_db_path,
            settings=Settings(anonymized_telemetry=False)
        )

        # Load embedding model
        print(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Indexed documents"}
        )

    def _create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Creates embeddings for list of texts"""
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()

    def index_document(self, file_path: str, docs_base_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Indexes a single document

        Args:
            file_path: Path to file
            docs_base_path: Base path to documents folder (for creating relative paths)
            chunk_size: Chunk size
            chunk_overlap: Overlap between chunks
        """
        print(f"Indexing: {file_path}")

        # Get relative path
        relative_path = get_relative_path(file_path, docs_base_path)

        # Delete old chunks of this document if they exist
        try:
            existing = self.collection.get(
                where={"source": relative_path}
            )
            if existing['ids']:
                self.collection.delete(ids=existing['ids'])
                print(f"  Deleted old chunks: {len(existing['ids'])}")
        except Exception as e:
            print(f"  Warning when deleting old chunks: {e}")

        # Read file
        content = read_file(file_path)

        if not content.strip():
            print(f"  File is empty, skipping")
            return

        # Split into chunks
        chunks = split_text_into_chunks(content, chunk_size, chunk_overlap)
        print(f"  Created {len(chunks)} chunks")

        if not chunks:
            return

        # Create embeddings
        embeddings = self._create_embeddings(chunks)

        # Prepare data for adding to database
        ids = [f"{relative_path}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "source": relative_path,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            for i in range(len(chunks))
        ]

        # Add to ChromaDB
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )

        print(f"  Successfully indexed")

    def index_all_documents(
        self,
        docs_path: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        extensions: List[str] = ['.txt', '.md']
    ):
        """
        Indexes all documents in the specified folder

        Args:
            docs_path: Path to documents folder
            chunk_size: Chunk size
            chunk_overlap: Overlap between chunks
            extensions: List of file extensions to process
        """
        # Get list of all documents
        documents = get_all_documents(docs_path, extensions)

        print(f"\nFound documents: {len(documents)}")
        print(f"Starting indexing...\n")

        # Index each document
        for doc_path in documents:
            try:
                self.index_document(doc_path, docs_path, chunk_size, chunk_overlap)
            except Exception as e:
                print(f"Error indexing {doc_path}: {e}")

        print(f"\nIndexing completed!")
        print(f"Total items in database: {self.collection.count()}")

    def clear_collection(self):
        """Clears collection (deletes all documents)"""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "Indexed documents"}
        )
        print("Collection cleared")


def main():
    """Main function to run indexing"""
    # Load environment variables
    load_dotenv()

    # Get parameters from .env
    docs_path = os.getenv('DOCS_PATH', './documents')
    chroma_db_path = os.getenv('CHROMA_DB_PATH', './chroma_db')
    embedding_model = os.getenv('EMBEDDING_MODEL', 'intfloat/multilingual-e5-large')
    chunk_size = int(os.getenv('CHUNK_SIZE', '1000'))
    chunk_overlap = int(os.getenv('CHUNK_OVERLAP', '200'))

    # Check if documents folder exists
    if not Path(docs_path).exists():
        print(f"Error: Folder {docs_path} does not exist!")
        print(f"Create the folder and place documents in it for indexing.")
        return

    # Create indexer
    indexer = DocumentIndexer(
        chroma_db_path=chroma_db_path,
        embedding_model=embedding_model
    )

    # Index all documents
    indexer.index_all_documents(
        docs_path=docs_path,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        extensions=['.txt', '.md']
    )


if __name__ == '__main__':
    main()
