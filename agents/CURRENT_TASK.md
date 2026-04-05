# Current Task

## Project: AI Secretary

**Status:** Active Development  
**Started:** 2026-04-04  
**Last Updated:** 2026-04-04

## Project Overview

AI Secretary for managing a knowledge base in Obsidian. The Secretary should:
- Manage a knowledge base, add tags to materials, track studied materials
- Summarize videos
- Compare with already studied topics and find new content
- Fill knowledge base with studied materials and future study materials
- Study the internet (Google, YouTube) for new knowledge on topics
- Plan learning trajectory
- Find materials for next learning steps
- Reindex all unstudied materials after each studied material
- Index novelty of material considering already studied materials

## Current Sprint

### Goals (Sprint 1)
1. ✅ Basic video analysis working (YouTube video → summary, tags, novelty)
2. ✅ Proxy auto-detection from Obsidian settings
3. ✅ CLI commands: add, analyze, learn, sync, status
4. ✅ Obsidian vault sync
5. ✅ GitHub repository setup on GitHub
6. ✅ Research: Chinese AI APIs for Russia
7. ⏳ SPEC.md review

### Completed This Session
- Video analysis with new structured prompts
- Tags: English only, lowercase, deduplicated
- Summary: Language-aware (ru/en), structured format
- Database fixes for tag persistence
- Proxy auto-detection implemented
- GitHub repository created and pushed
- Added Chinese AI providers (SiliconFlow, Zhipu AI) and tested

### In Progress
- Agentic Chain Research

### Blocked
- None

## Next Steps (Priority Order)

1. ✅ Test Chinese AI APIs (SiliconFlow ✅, Zhipu AI ✅)

2. **Agentic Chain Research**
   - Compare single-prompt vs chain approach
   - Document findings
   - Implement if quality improves

3. **Brotab Integration**
   - Add-from-tabs command
   - Browser tab parsing

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
