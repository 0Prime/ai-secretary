# Current Task

## Project: AI Secretary

**Status:** Active Development  
**Started:** 2026-04-04  
**Last Updated:** 2026-04-05

## Video Analysis: ZProger - AI Secretary Concept

**Video:** https://www.youtube.com/watch?v=6BW4lo7f71I
**Channel:** ZProger [ IT ]
**Duration:** 13 min (801 sec)

### Key Insights from Video

**3 Problems Solved:**
1. **Duplicate content** - 20 videos = same 20% info → extract only unique
2. **Book redundancy** - 5-10 books/year contain known info → AI checks what you know
3. **Product research** - weeks to compare products → AI does in 15 min

**Tools Mentioned:**
- Obsidian - knowledge base
- Gemini - AI for search/processing
- LM (Local Model) - local AI for checking knowledge

### New Architecture Vision

**Hybrid Approach:**
1. **Button functionality** - quick actions (mark watched, add material)
2. **AI Agents** - handle complex queries, research, comparisons
3. **Code only for** - token-heavy operations (parsing, embeddings, novelty scoring)

**Agent Requirements:**
- **Free** - no paid API calls
- **Open source CLI** - Ollama, local models
- **Intelligent routing** - automatically select best available provider:
  1. Ollama local (free, private, fast)
  2. Zhipu AI (free tier, Chinese)
  3. SiliconFlow (free tier, if has balance)
  4. Fallback: nearest working provider

**No-code path:** User → AI Agent → Obsidian (via API)

### Current Sprint

### Goals (Sprint 1)
1. ✅ Basic video analysis working (YouTube video → summary, tags, novelty)
2. ✅ Proxy auto-detection from Obsidian settings
3. ✅ CLI commands: add, analyze, learn, sync, status
4. ✅ Obsidian vault sync
5. ✅ GitHub repository setup on GitHub
6. ✅ Research: Chinese AI APIs for Russia
7. ✅ SPEC.md review

### Completed This Session
- Video analysis with new structured prompts
- Tags: English only, lowercase, deduplicated
- Summary: Language-aware (ru/en), structured format
- Database fixes for tag persistence
- Proxy auto-detection implemented
- GitHub repository created and pushed
- Added Chinese AI providers (SiliconFlow, Zhipu AI) and tested
- Analyzed video that inspired the project (ZProger)

### In Progress
- Define next phase based on new vision

### Blocked
- None

## Next Steps (Priority Order)

### New Architecture (Based on ZProger Video)

1. **Button Functionality**
   - Quick "mark watched" - from Obsidian UI or hotkey
   - Quick add from clipboard
   - Quick analyze current note
   - Implemented via: Obsidian plugin OR hotkeys

2. **AI Agent Layer**
   - Direct queries to AI (natural language)
   - Research tasks (find materials on topic)
   - Comparison tasks (X vs Y)
   - Implemented via: Claude/GPT API or local Ollama

3. **Code for Token-Heavy Ops**
   - Video parsing (yt-dlp)
   - Transcript fetching
   - Embeddings + novelty scoring
   - Database operations

### Research Tasks

- [x] Obsidian plugin development (button functionality)
- [x] AI agent prompt engineering
- [x] Intelligent provider auto-selection with fallback
- [x] Knowledge base queries (query, recommend, related commands)
- [x] AI agent commands (ask, compare, research)
- [ ] Obsidian API integration

## CLI Commands Available

| Command | Description |
|---------|-------------|
| `ask <question>` | Ask AI agent (auto-selects provider) |
| `compare <a> <b>` | Compare two items |
| `research <topic>` | Research a topic |
| `query <text>` | Search knowledge base |
| `recommend` | Get learning recommendations |
| `providers` | Show available AI providers |
| `add <url>` | Add material |
| `analyze <id>` | Analyze material |
| `learn <id>` | Mark as learned |

## Known Issues

- Proxy connection is flaky (Hiddify)
- llm3.2:1b produces some template phrases
- Larger models needed for better quality

## Hardware Context

- CPU: i5-13400F (10C/16T)
- RAM: 32 GB
- GPU: RTX 3070 (8 GB VRAM)
- Free disk: 130 GB on C:

## Models Available (Ollama)

- `phi3:latest` (2.2 GB) - tested, ~7-21 seconds
- `llama3.2:1b` (1.3 GB) - current default, ~2.8 seconds
- `llama3.2:3b` (2.0 GB) - downloaded
- `nomic-embed-text` (274 MB) - for embeddings
