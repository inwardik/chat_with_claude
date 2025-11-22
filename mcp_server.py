"""
MCP server for semantic document search
"""
import os
import sys
import asyncio
from pathlib import Path
from typing import Any, List, Dict
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

# Set UTF-8 encoding for stdout/stderr on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


# Global variables for storing state
embedding_model = None
chroma_client = None
collection = None


def initialize_db():
    """Initializes ChromaDB connection and embedding model"""
    global embedding_model, chroma_client, collection

    # Load environment variables
    load_dotenv()

    chroma_db_path = os.getenv('CHROMA_DB_PATH', './chroma_db')
    model_name = os.getenv('EMBEDDING_MODEL', 'intfloat/multilingual-e5-large')

    # Check if database exists
    if not Path(chroma_db_path).exists():
        raise ValueError(
            f"Database not found at: {chroma_db_path}\n"
            "Run indexing script first: python indexer.py"
        )

    # Load embedding model
    print(f"Loading model: {model_name}", flush=True)
    embedding_model = SentenceTransformer(model_name)

    # Connect to ChromaDB
    print(f"Connecting to ChromaDB: {chroma_db_path}", flush=True)
    chroma_client = chromadb.PersistentClient(
        path=chroma_db_path,
        settings=Settings(anonymized_telemetry=False)
    )

    # Get collection
    collection = chroma_client.get_collection("documents")
    print(f"Ready! Database contains {collection.count()} documents", flush=True)


def search_documents(query: str, n_results: int = 5) -> List[Dict[str, Any]]:
    """
    Performs semantic search through documents

    Args:
        query: Search query
        n_results: Number of results

    Returns:
        List of found documents with metadata
    """
    global embedding_model, collection

    # Create embedding for query
    query_embedding = embedding_model.encode([query])[0].tolist()

    # Search for similar documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    # Format results
    formatted_results = []
    if results['documents'] and results['documents'][0]:
        for i, doc in enumerate(results['documents'][0]):
            formatted_results.append({
                'content': doc,
                'source': results['metadatas'][0][i]['source'],
                'chunk_index': results['metadatas'][0][i]['chunk_index'],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })

    return formatted_results


# Create MCP server
app = Server("document-search")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List of available tools"""
    return [
        Tool(
            name="search_documents",
            description=(
                "Semantic search through indexed documents. "
                "Use this tool to find relevant information in documents by meaning, "
                "not by exact keyword matching."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query in natural language"
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "Number of results to return (default: 5)",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 20
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_database_stats",
            description=(
                "Get statistics on indexed documents. "
                "Shows the number of documents in the database and other information."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Process tool calls"""
    global collection

    if name == "search_documents":
        query = arguments.get("query")
        n_results = arguments.get("n_results", 5)

        if not query:
            return [TextContent(
                type="text",
                text="Error: search query not specified"
            )]

        # Perform search
        results = search_documents(query, n_results)

        if not results:
            return [TextContent(
                type="text",
                text=f"Nothing found for query '{query}'."
            )]

        # Format results
        response = f"Found {len(results)} results for query: '{query}'\n\n"

        for i, result in enumerate(results, 1):
            response += f"--- Result {i} ---\n"
            response += f"Source: {result['source']}\n"
            response += f"Chunk: {result['chunk_index']}\n"
            if result['distance'] is not None:
                response += f"Relevance: {1 - result['distance']:.2%}\n"
            response += f"\nContent:\n{result['content']}\n\n"

        return [TextContent(type="text", text=response)]

    elif name == "get_database_stats":
        count = collection.count()
        response = f"Database statistics:\n"
        response += f"- Total indexed chunks: {count}\n"
        response += f"- Collection: {collection.name}\n"

        return [TextContent(type="text", text=response)]

    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def main():
    """Main function to run server"""
    # Initialize database on startup
    initialize_db()

    # Run MCP server via stdio
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == '__main__':
    asyncio.run(main())
