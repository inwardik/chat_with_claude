# Document Search System for Claude Code

This project allows you to index your documents into a vector database and use semantic search through an MCP server in Claude Code.

## Features

- Index text documents (.txt, .md) into a ChromaDB vector database
- Semantic search through document content using natural language
- Support for Russian and English languages
- Integration with Claude Code through the MCP protocol
- Local data storage without cloud uploads

## Installation

### 1. Install UV

UV is a modern package manager for Python that automatically manages dependencies.

**Windows:**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or via pip:
```bash
pip install uv
```

### 2. Install Dependencies

UV will automatically install all dependencies on first run. You can also install them in advance:

```bash
uv sync
```

On first run, the embedding model (~1.5 GB) will be automatically downloaded.

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and configure parameters:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Path to the documents folder for indexing
DOCS_PATH=./documents

# Path to the vector database
CHROMA_DB_PATH=./chroma_db

# Model for creating embeddings
EMBEDDING_MODEL=intfloat/multilingual-e5-large

# Text chunk size (in characters)
CHUNK_SIZE=1000

# Overlap between chunks
CHUNK_OVERLAP=200
```

### 4. Prepare Documents

Create a `documents` folder and place your text files (.txt, .md) in it:

```bash
mkdir documents
```

### 5. Run Indexing

```bash
uv run indexer.py
```

This script will:
- Find all .txt and .md files in the `documents` folder
- Split them into chunks
- Create embeddings for each chunk
- Save to ChromaDB

## Claude Code Configuration

### Local Configuration (Recommended)

The MCP server is configured via the `.mcp.json` file in the project root. This means the configuration is automatically applied when opening the project in Claude Code.

**No additional setup required!** On first use, Claude Code will ask for permission to run the MCP server - just approve it.

The `.mcp.json` file is already created and contains the correct configuration with relative paths.

### Restart Claude Code

If the project was already open, restart Claude Code to apply the changes.

---

### Alternative: Global Configuration (Optional)

If you want to use this MCP server in all projects, you can add it to the global configuration:

1. Open Claude Code's configuration file:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Add the `mcpServers` section (see `mcp_config_example.json` for an example)

**Note**: Local configuration via `.mcp.json` is more convenient as it doesn't require changing global settings and automatically works when opening the project.

After changing the configuration, restart Claude Code to apply the changes.

## Usage

After setup, the MCP server will be automatically available in Claude Code.

### Available Tools

1. **search_documents** - Semantic search through documents
   ```
   Find information about database setup
   ```

2. **get_database_stats** - Statistics on indexed documents
   ```
   How many documents are indexed?
   ```

### Usage Examples

**Search for information:**
```
Use the search_documents tool to find information about API keys
```

**Questions about documents:**
```
What is written in the documents about authentication?
```

**Get statistics:**
```
Show me statistics about indexed documents
```

## Re-indexing Documents

If you've added new documents or modified existing ones, run indexing again:

```bash
uv run indexer.py
```

This will add new documents to the database. If you want to clear the database and re-index all documents from scratch:

```python
from indexer import DocumentIndexer
from dotenv import load_dotenv
import os

load_dotenv()
indexer = DocumentIndexer(
    chroma_db_path=os.getenv('CHROMA_DB_PATH', './chroma_db'),
    embedding_model=os.getenv('EMBEDDING_MODEL', 'intfloat/multilingual-e5-large')
)
indexer.clear_collection()  # Clear the database
```

## Project Structure

```
R:\proj\
├── documents/          # Your documents folder
├── chroma_db/         # Vector database
├── utils.py           # Utility functions
├── indexer.py         # Indexing script
├── mcp_server.py      # MCP server
├── requirements.txt   # Python dependencies
├── .env              # Environment variables
└── README.md         # This file
```

## Technical Details

### Technologies Used

- **ChromaDB** - vector database for storing embeddings
- **Sentence Transformers** - text embedding creation
- **MCP (Model Context Protocol)** - protocol for Claude Code integration
- **intfloat/multilingual-e5-large** - embedding model with Russian language support

### How It Works

1. **Indexing**: Documents are split into chunks (~1000 characters with overlap)
2. **Embeddings**: Each chunk gets a vector representation
3. **Storage**: Embeddings are saved in ChromaDB with metadata
4. **Search**: Queries are converted to vectors and similar chunks are found
5. **Results**: The most relevant document fragments are returned

## Troubleshooting

### Error: "Database Not Found"

Make sure you've run `python indexer.py` before running the MCP server.

### Slow Performance

On first run, the model (~1.5 GB) is loaded. Subsequent runs will be faster.

### MCP Server Won't Connect

1. Check that paths in the configuration are correct
2. Ensure Python is available from the command line
3. Verify that all dependencies are installed
4. Restart Claude Code

## Extending Functionality

### Adding Support for New File Formats

Edit `utils.py` and `indexer.py` to add handlers for new file types (.pdf, .docx, etc.).

### Adjusting Chunk Size

Change the `CHUNK_SIZE` and `CHUNK_OVERLAP` parameters in the `.env` file. Smaller chunks give more precise results but require more database space.

### Changing the Embedding Model

You can use other models from Sentence Transformers. For Russian language support, we recommend:
- `intfloat/multilingual-e5-large` (recommended)
- `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
- `cointegrated/rubert-tiny2`

## License

MIT
