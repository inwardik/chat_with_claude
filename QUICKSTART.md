# Quick Start

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Add Your Documents

Place your .txt or .md files in the `documents/` folder

## Step 3: Index Documents

```bash
python indexer.py
```

## Step 4: Open Project in Claude Code

The MCP server is already configured via the `.mcp.json` file in the project root.

1. Open the project folder in Claude Code
2. On first launch, approve the use of the "document-search" MCP server
3. Done! No additional setup is required

## Step 5: Start Using!

Now you can ask questions about your documents in Claude Code:

```
Find information about authentication in my documents
```

```
What is written about database setup?
```

## Re-indexing

If you added new documents:

```bash
python indexer.py
```

Done!
