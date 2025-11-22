# MCP Server Setup

## Local Configuration (Used in This Project)

In this project, the MCP server is configured via the **`.mcp.json`** file in the project root.

### Advantages of Local Configuration

✅ **No need to edit global settings** - configuration is stored in the project
✅ **Automatic activation** - when opening the project in Claude Code
✅ **Relative paths** - project can be moved without changing configuration
✅ **Portability** - easy to share the project with colleagues
✅ **Isolation** - MCP server runs only for this project

### How It Works

1. When opening the project folder in Claude Code
2. Claude Code automatically detects the `.mcp.json` file
3. On first launch, requests permission to use the "document-search" MCP server
4. After approval, the server automatically activates

### Contents of .mcp.json

```json
{
  "mcpServers": {
    "document-search": {
      "command": "python",
      "args": ["mcp_server.py"],
      "env": {
        "DOCS_PATH": "./documents",
        "CHROMA_DB_PATH": "./chroma_db",
        "EMBEDDING_MODEL": "intfloat/multilingual-e5-large",
        "CHUNK_SIZE": "1000",
        "CHUNK_OVERLAP": "200"
      }
    }
  }
}
```

Note the use of relative paths (`./documents`, `./chroma_db`), which makes the configuration independent of the project location on disk.

---

## Global Configuration (Alternative Method)

If you want to use this MCP server **in all projects**, not just this one, you can add it to Claude Code's global configuration.

### Global Configuration File Location

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Global Configuration Example

See the `mcp_config_example.json` file in the project. You will need to:

1. Replace relative paths with absolute paths
2. Copy the `mcpServers` section to the global configuration file
3. Restart Claude Code

### When to Use Global Configuration

- When you need access to documents from any project
- When working with a single knowledge base for all tasks
- When frequently switching between projects but needing access to the same documents

### Note

⚠️ **It's recommended to use local configuration** (`.mcp.json`), as it's simpler to set up and doesn't require changing global system settings.

---

## Verifying MCP Server Operation

After setup, verify the server is working:

1. Open the project in Claude Code
2. Enter the query: "Use the get_database_stats tool"
3. If the MCP server is working, you'll see statistics about indexed documents

Or try a search:

```
Find information about vector embeddings in the documents
```

If the server doesn't start, check:
- Are all dependencies installed: `pip install -r requirements.txt`
- Is the database created: `python indexer.py`
- Did you approve the MCP server on first Claude Code launch

## Disabling the MCP Server

If you want to temporarily disable the MCP server:

### For Local Configuration
Rename or delete the `.mcp.json` file

### For Global Configuration
Delete the `"document-search"` section from the global configuration file

After making changes, restart Claude Code.
