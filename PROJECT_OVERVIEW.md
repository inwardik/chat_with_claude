# Project Overview: Document Search System

## Description

A full-featured system for indexing documents and semantic search with integration into Claude Code via the MCP protocol.

## Created Files

### Main Scripts

- **`utils.py`** - Utility functions for file and text handling
  - File reading with auto-encoding detection
  - Text splitting into chunks with overlap
  - Getting list of documents

- **`indexer.py`** - Document indexing script
  - `DocumentIndexer` class for working with ChromaDB
  - Embedding creation via Sentence Transformers
  - Indexing all documents in a folder
  - Collection cleanup

- **`mcp_server.py`** - MCP server for Claude Code
  - `search_documents` tool - semantic search
  - `get_database_stats` tool - database statistics
  - Asynchronous operation via stdio

- **`test_search.py`** - Interactive testing script
  - Search functionality testing without MCP
  - Interactive mode for testing queries

### Configuration

- **`.env`** / **`.env.example`** - Environment variables
  - Document and database paths
  - Embedding model settings
  - Chunk splitting parameters

- **`requirements.txt`** - Python dependencies
  - chromadb - vector database
  - sentence-transformers - embedding creation
  - mcp - Claude Code protocol
  - python-dotenv - .env file handling

- **`.mcp.json`** - Local MCP server configuration
  - Automatically applied when opening project in Claude Code
  - Uses relative paths

- **`mcp_config_example.json`** - Global configuration example (optional)
  - For using MCP server in all projects

- **`.gitignore`** - Git exclusions
  - Python cache, virtual environments
  - ChromaDB database
  - IDE settings files

### Documentation

- **`README.md`** - Complete documentation
  - Feature description
  - Detailed installation instructions
  - Claude Code setup
  - Usage examples
  - Troubleshooting
  - Technical details

- **`QUICKSTART.md`** - Quick start
  - Brief instructions to get started
  - 5 simple steps

- **`PROJECT_OVERVIEW.md`** - This file
  - Project structure overview

### Setup Scripts

- **`setup.bat`** - Automated installation (Windows)
  - Python checking
  - Virtual environment creation
  - Dependency installation
  - Creation of required files and folders

### Data

- **`documents/`** - Your documents folder
  - `example.md` - Example document for testing

- **`chroma_db/`** - Database (created during indexing)
  - Vector embeddings
  - Document metadata

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Vector DB | ChromaDB | Store embeddings and search |
| Embeddings | Sentence Transformers | Create vector representations |
| Model | multilingual-e5-large | Russian language support |
| Protocol | MCP | Claude Code integration |
| Language | Python 3.8+ | Primary development language |

## Architecture

```
┌─────────────────┐
│  Your documents │
│   (.txt, .md)   │
└────────┬────────┘
         │
         ▼
  ┌──────────────┐
  │  indexer.py  │  ← Split into chunks
  └──────┬───────┘     Create embeddings
         │
         ▼
  ┌──────────────┐
  │  ChromaDB    │  ← Vector storage
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │mcp_server.py │  ← MCP protocol
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │ Claude Code  │  ← Semantic search
  └──────────────┘
```

## Core Features

### Indexing (indexer.py)
1. Scan documents folder
2. Read files with auto-encoding detection
3. Split into chunks ~1000 characters
4. Create vector embeddings
5. Save to ChromaDB with metadata

### Search (mcp_server.py)
1. Receive query from Claude
2. Create query embedding
3. Vector search for similar chunks
4. Rank by relevance
5. Return top-N results

## Quick Start

### Automated Installation (Windows)
```bash
setup.bat
```

### Manual Installation
```bash
# 1. Installation
pip install -r requirements.txt

# 2. Add documents
# Place files in documents/ folder

# 3. Indexing
python indexer.py

# 4. Testing (optional)
python test_search.py

# 5. Open project in Claude Code
# MCP server configured via .mcp.json and auto-activates
```

## Usage

After setup in Claude Code:

```
Find information about authentication
```

```
What is written in the documents about API?
```

```
Show me statistics about indexed documents
```

## Extensions

### Adding New File Formats

Edit `utils.py`:
```python
def read_pdf(file_path):
    # PDF reading implementation
    pass
```

Update `indexer.py`:
```python
extensions=['.txt', '.md', '.pdf']
```

### Changing Model

In `.env`:
```env
EMBEDDING_MODEL=cointegrated/rubert-tiny2
```

### Adjusting Chunk Size

In `.env`:
```env
CHUNK_SIZE=500
CHUNK_OVERLAP=100
```

## Troubleshooting

### Database Not Found
```bash
python indexer.py
```

### MCP Server Won't Connect
1. Check paths in configuration
2. Ensure Python is in PATH
3. Restart Claude Code

### Slow Performance
On first run, the model (~1.5 GB) is loaded. Subsequent runs are faster.

## License

MIT

---

**Author**: Created with Claude Code
**Date**: 2025-11-22
