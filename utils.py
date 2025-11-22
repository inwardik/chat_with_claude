"""
Utility functions for working with documents
"""
import os
from pathlib import Path
from typing import List, Tuple


def read_file(file_path: str) -> str:
    """Reads file content with auto-encoding detection"""
    encodings = ['utf-8', 'windows-1251', 'cp1251', 'utf-16']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue

    # If all attempts failed, use utf-8 with error ignoring
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def split_text_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Splits text into chunks with overlap

    Args:
        text: Source text
        chunk_size: Chunk size in characters
        overlap: Overlap size between chunks

    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]

        # If not the last chunk, try to split at sentence or paragraph boundary
        if end < text_length:
            # Look for the last period, exclamation or question mark
            last_period = max(
                chunk.rfind('. '),
                chunk.rfind('! '),
                chunk.rfind('? '),
                chunk.rfind('\n\n')
            )
            if last_period > chunk_size * 0.5:  # If found separator not too early
                chunk = chunk[:last_period + 1]
                end = start + last_period + 1

        chunks.append(chunk.strip())
        start = end - overlap if end < text_length else end

    return [c for c in chunks if c]  # Remove empty chunks


def get_all_documents(docs_path: str, extensions: List[str] = ['.txt', '.md']) -> List[str]:
    """
    Gets a list of all documents in the specified folder

    Args:
        docs_path: Path to documents folder
        extensions: List of file extensions to process

    Returns:
        List of file paths
    """
    documents = []
    docs_path = Path(docs_path)

    if not docs_path.exists():
        raise ValueError(f"Path {docs_path} does not exist")

    for ext in extensions:
        documents.extend(docs_path.rglob(f'*{ext}'))

    return [str(doc) for doc in documents]


def get_relative_path(file_path: str, base_path: str) -> str:
    """Returns relative path of file relative to base folder"""
    return str(Path(file_path).relative_to(Path(base_path)))
