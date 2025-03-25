# ➡️ browser-use mcp server

[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/cobrowser.svg?style=social&label=Follow%20%40cobrowser)](https://x.com/cobrowser)
[![PyPI version](https://badge.fury.io/py/browser-use-mcp-server.svg)](https://pypi.org/project/browser-use-mcp-server/)

[browser-use](https://github.com/browser-use/browser-use) MCP Server with SSE +
stdio transport

### Requirements

- [uv](https://github.com/astral-sh/uv)
- [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) (for stdio)

```
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# 2. Install mcp-proxy pypi package via uv
uv tool install mcp-proxy
```

### Quickstart

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

### Tools

- [x] SSE transport
- [x] stdio transport (via mcp-proxy)
- [x] browser_use - Initiates browser tasks with URL and action
- [x] browser_get_result - Retrieves results of async browser tasks

### Supported Clients

- cursor.ai
- claude desktop
- claude code
- windsurf ([windsurf](https://codeium.com/windsurf) doesn't support SSE, only
  stdio)

#### SSE Mode

After running the server in SSE mode, add http://localhost:8000/sse to your
client UI, or in a mcp.json file:

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

When running in stdio mode, the server will automatically start both the SSE
server and mcp-proxy. The proxy handles the conversion between stdio and SSE
protocols. No additional configuration is needed - just start your
terminal-based client and it will communicate with the server through
stdin/stdout.

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
      "args": [
        "run",
        "server",
        "--port",
        "8000",
        "--stdio",
        "--proxy-port",
        "9000"
      ]
    }
  }
}
```

### Client Configuration Paths

#### Cursor

- `./.cursor/mcp.json`

#### Windsurf

- `~/.codeium/windsurf/mcp_config.json`

#### Claude

- `~/Library/Application Support/Claude/claude_desktop_config.json`
- `%APPDATA%\Claude\claude_desktop_config.json`

### Example Usage

Try asking your LLM the following:

`open https://news.ycombinator.com and return the top ranked article`

### Help

for issues or interest reach out @ https://cobrowser.xyz

# Stars

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=co-browser/browser-use-mcp-server&type=Date&theme=dark" />
  <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=co-browser/browser-use-mcp-server&type=Date" />
  <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=co-browser/browser-use-mcp-server&type=Date" />
</picture>
