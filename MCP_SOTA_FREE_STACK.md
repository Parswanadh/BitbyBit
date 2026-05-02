# SOTA Free MCP Stack for BitbyBit

This setup is optimized for your workspace (RTL + Python simulation + Next.js + Playwright).

## What is configured

The workspace MCP config is in `.vscode/mcp.json`.

Configured servers:
- filesystem
- git
- fetch
- memory
- sequentialThinking
- playwright
- context7
- github (remote HTTP endpoint)
- braveSearch (optional free API key)
- everything

## Why this stack

- **Codebase reasoning**: filesystem + git + memory + sequentialThinking
- **Research quality**: fetch + context7 + braveSearch
- **Web/testing automation**: playwright
- **Repository operations**: github
- **Rapid tool discovery**: everything

## Installed packages

Global npm packages installed:
- @modelcontextprotocol/server-filesystem
- @modelcontextprotocol/server-memory
- @modelcontextprotocol/server-sequential-thinking
- @modelcontextprotocol/server-github
- @modelcontextprotocol/server-brave-search
- @modelcontextprotocol/server-everything
- @playwright/mcp
- @upstash/context7-mcp

Python MCP packages installed into workspace Python environment:
- mcp-server-git
- mcp-server-fetch

## Optional keys

- `braveSearch` uses `BRAVE_API_KEY` via input prompt in `mcp.json`.
- `github` is configured as remote `https://api.githubcopilot.com/mcp`.

## VS Code settings added

`.vscode/settings.json` includes:
- `chat.mcp.autostart: true`
- `chat.mcp.discovery.enabled: true`

## Notes

- MCP ecosystem is very large and changes weekly. Installing every free server globally is not practical and adds heavy noise and security risk.
- This stack is the highest-impact free set for this repository and should produce strong coding + research output quality.
