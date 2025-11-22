# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Project Rules

**CRITICAL**: For ANY question about myself:
1. ALWAYS call document-search MCP server FIRST
2. Never answer from general knowledge without checking document-search
3. If document-search returns results, use ONLY that information

## When to use document-search
- Questions about me

## Project Overview

This is a document search system that indexes documents into a ChromaDB vector database and provides semantic search capabilities through an MCP server for Claude Code. The system supports Russian and English languages and uses multilingual embeddings for semantic search.

## Development Commands

### Install Dependencies
```bash
uv sync
```
UV automatically manages dependencies from `pyproject.toml`. On first run, the embedding model (~1.5 GB) will be automatically downloaded.

### Index Documents
```bash
uv run indexer.py
```
Indexes all `.txt` and `.md` files from the `documents/` folder into ChromaDB. Creates embeddings and stores them with metadata.

### Test Search (Standalone)
```bash
uv run test_search.py
```
Interactive testing of document search without using the MCP server. Useful for verifying indexing worked correctly.

### Run MCP Server
The MCP server is configured via `.mcp.json` and starts automatically when Claude Code opens the project. The server runs using `uv run mcp_server.py`, eliminating the need for virtual environment management.

### Clear Database
```bash
uv run clear_db.py
```
Completely clears the ChromaDB collection. Use this when you want to start from scratch. The script will ask for confirmation before deleting data.

**Note**: Running `uv run indexer.py` automatically handles incremental updates - it removes old versions of documents before re-indexing them, so a full clear is rarely needed.

## Architecture

### Core Components

**indexer.py** - Document indexation pipeline:
- `DocumentIndexer` class handles reading documents, chunking, embedding creation, and ChromaDB storage
- Uses `SentenceTransformer` with `intfloat/multilingual-e5-large` model for multilingual embeddings
- Chunks are created with overlap to preserve context across boundaries
- Automatically removes old versions of documents before re-indexing (prevents duplicates and stale data)

**clear_db.py** - Database maintenance script:
- Provides interactive way to completely clear the ChromaDB collection
- Asks for confirmation before deleting data
- Useful when starting fresh or troubleshooting

**utils.py** - Utility functions:
- `read_file()`: Multi-encoding file reader (tries utf-8, windows-1251, cp1251, utf-16)
- `split_text_into_chunks()`: Intelligent text chunking with sentence boundary detection
- `get_all_documents()`: Recursively finds documents with specified extensions
- `get_relative_path()`: Converts absolute paths to relative for storage

**mcp_server.py** - MCP server for Claude Code integration:
- Implements two MCP tools: `search_documents` and `get_database_stats`
- Loads ChromaDB and embedding model on startup
- Communicates via stdio protocol
- Handles UTF-8 encoding on Windows platforms

**test_search.py** - Standalone search tester for debugging

### Data Flow

1. **Indexing**: `indexer.py` → reads files → chunks text → creates embeddings → stores in ChromaDB
2. **Search**: Query → embedding → ChromaDB vector similarity search → ranked results
3. **MCP Integration**: Claude Code → calls MCP tool → `mcp_server.py` → ChromaDB → returns formatted results

### Configuration

**Dependencies** are managed in `pyproject.toml`:
- Python >=3.10 required
- Main dependencies: chromadb, sentence-transformers, mcp, python-dotenv
- UV automatically installs and manages these dependencies

**Environment variables** are loaded from `.env` (based on `.env.example`):
- `DOCS_PATH`: Path to documents folder (default: `./documents`)
- `CHROMA_DB_PATH`: Path to ChromaDB storage (default: `./chroma_db`)
- `EMBEDDING_MODEL`: Sentence transformer model (default: `intfloat/multilingual-e5-large`)
- `CHUNK_SIZE`: Text chunk size in characters (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)

### Database Structure

ChromaDB collection named "documents" stores:
- **embeddings**: Vector representations of text chunks
- **documents**: Actual text content
- **metadata**:
  - `source`: Relative path to source file
  - `chunk_index`: Position of chunk in document
  - `total_chunks`: Total chunks in the source document
- **ids**: Formatted as `{relative_path}_chunk_{index}`

### Text Chunking Strategy

Chunks are created with smart boundary detection (`utils.py:25-61`):
1. Attempt to split at sentence boundaries (`. `, `! `, `? `, `\n\n`)
2. Only split at boundaries if found in the latter half of chunk (>50% position)
3. Apply overlap to preserve context across chunk boundaries
4. This ensures semantic coherence and prevents information loss at boundaries

## Platform Considerations

- **Windows**: The code includes Windows-specific UTF-8 configuration (`mcp_server.py:18-20`) and multi-encoding file reading for Cyrillic text
- **Dependency Management**: Uses UV (`uv run`) which eliminates the need for manual virtual environment management. UV automatically creates isolated environments per project.
- **File Encodings**: Documents may be in various encodings (utf-8, windows-1251, cp1251, utf-16) due to Russian language support

## Extending the System

### Adding New File Formats

Modify `indexer.py:182` to include new extensions in the `extensions` parameter. Then add format-specific reading logic to `utils.py:read_file()`.

### Changing Embedding Models

Update `EMBEDDING_MODEL` in `.env`. For Russian language support, recommended models are listed in `README.md:217-220`.

### Adjusting Chunk Size

Modify `CHUNK_SIZE` and `CHUNK_OVERLAP` in `.env`. Smaller chunks provide more precise results but require more storage and may lose context.
