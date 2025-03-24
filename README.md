# ➡️ browser-use mcp server

[browser-use](https://github.com/browser-use/browser-use) MCP Server with SSE + stdio
transport

### requirements

- uv
- mcp-proxy (for stdio)

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### quickstart

Starting in SSE mode:
```bash
uv sync
uv pip install playwright
uv run playwright install --with-deps --no-shell chromium
uv run server --port 8000
```

With stdio mode (for terminal-based clients):
```bash
# Run with stdio mode and specify a proxy port
uv run server --stdio --proxy-port 8001

# Or just stdio mode (random proxy port)
uv run server --stdio
```

- the .env requires the following:

```
OPENAI_API_KEY=[your api key]
CHROME_PATH=[only change this if you have a custom chrome build]
```

When building the docker image, you can use Docker secrets for VNC password:

```bash
# With Docker secrets (recommended for production)
echo "your-secure-password" > vnc_password.txt
docker run -v $(pwd)/vnc_password.txt:/run/secrets/vnc_password your-image-name

# Or during development with the default password
docker build .
```

### tools

- [x] SSE transport
- [x] stdio transport (via mcp-proxy)
- [x] browser_use - Initiates browser tasks with URL and action
- [x] browser_get_result - Retrieves results of async browser tasks

### supported clients

- cursor.ai
- claude desktop
- claude code
- windsurf ([windsurf](https://codeium.com/windsurf) doesn't support SSE, only stdio)

#### SSE Mode

After running the server in SSE mode, add http://localhost:8000/sse to your client UI, or in a mcp.json file:

```json
{
  "mcpServers": {
    "browser-use-mcp-server": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

#### stdio Mode

When running in stdio mode, the server will automatically start both the SSE server and mcp-proxy. The proxy handles the conversion between stdio and SSE protocols. No additional configuration is needed - just start your terminal-based client and it will communicate with the server through stdin/stdout.

Install the cli

```bash
uv pip install -e .  
```

And then e.g., in Windsurf, paste:

```json
{
  "mcpServers": {
    "browser-server": {
        "command": "browser-use-mcp-server",
        "args": ["run", "server", "--port", "8000", "--stdio", "--proxy-port", "9000"]
    }
  }
}
```

### client configuration paths

#### cursor

- `./.cursor/mcp.json`

#### windsurf

- `~/.codeium/windsurf/mcp_config.json`

#### claude

- `~/Library/Application Support/Claude/claude_desktop_config.json`
- `%APPDATA%\Claude\claude_desktop_config.json`

### example usage

Try asking your LLM the following:

`open https://news.ycombinator.com and return the top ranked article`

### help

for issues or interest reach out @ https://cobrowser.xyz

# stars

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=co-browser/browser-use-mcp-server&type=Date&theme=dark" />
  <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=co-browser/browser-use-mcp-server&type=Date" />
  <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=co-browser/browser-use-mcp-server&type=Date" />
</picture>
