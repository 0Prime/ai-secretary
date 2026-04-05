# AI Secretary Plugin for Obsidian

Obsidian plugin that integrates with the AI Secretary CLI tool to provide AI-powered knowledge management directly from Obsidian.

## Features

### Quick Actions (Ribbon Icon)
- Click the brain icon to access quick actions menu
- Ask AI, Query Knowledge Base, Get Recommendations, Research Topic

### Commands (Command Palette)

| Command | Description |
|---------|-------------|
| `Ask AI Agent` | Ask AI any question (uses selected text or prompt) |
| `Add Current Note to Knowledge Base` | Add current note URL to Secretary database |
| `Analyze Current Note` | Analyze and summarize current note |
| `Query Knowledge Base` | Search your learned materials |
| `Get Learning Recommendations` | Get recommended materials to learn |
| `Compare Two Items` | Compare any two items (tools, concepts, etc.) |
| `Research Topic` | Research any topic with AI |

## Installation

### Prerequisites

1. **Install AI Secretary CLI:**
```bash
git clone https://github.com/0Prime/ai-secretary.git
cd ai-secretary
pip install -e .
```

2. **Ensure `secretary` command works:**
```bash
secretary --help
```

### Install Plugin

#### Option 1: Manual Installation
1. Clone this repository or download the `obsidian-plugin` folder
2. Copy the folder to your Obsidian plugins directory:
   - Windows: `%appdata%\obsidian\plugins\ai-secretary`
   - Mac: `~/Library/Application Support/obsidian/plugins/ai-secretary`
   - Linux: `~/.config/obsidian/plugins/ai-secretary`
3. Enable the plugin in Obsidian Settings > Plugins

#### Option 2: From Source (for development)
```bash
npm install
npm run build
```

## Configuration

1. Set your AI providers in `.env`:
```
# .env file in ai-secretary directory
ZHIPU_API_KEY=your_zhipu_key
SILICONFLOW_API_KEY=your_sf_key
```

2. Or use local Ollama (default, no config needed)

## Usage

1. **Click the brain icon** (ribbon) for quick actions
2. **Press Ctrl+P** for Command Palette, then search "AI Secretary"
3. **Right-click** for context menu options

## Commands

### AI Agent Commands
- `ask <question>` - Ask AI anything
- `compare <a> <b>` - Compare two items
- `research <topic>` - Research a topic (brief/medium/detailed)

### Knowledge Base Commands
- `query <text>` - Search learned materials
- `recommend` - Get learning recommendations
- `related <id>` - Find related materials

### Provider Management
- `providers` - Show available AI providers
- `providers --all` - Show all configured providers

## Requirements

- Obsidian v0.15.0+
- AI Secretary CLI installed and in PATH
- Node.js (for building from source)

## License

MIT
