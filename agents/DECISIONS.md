# Decisions Log

Key architectural and design decisions made during development.

## 2026-04-04

### Γ£à Tech Stack

**Decision:** Python + SQLite + Ollama (local)

**Rationale:**
- Python: Good AI ecosystem, fast development
- SQLite: Simple, no server needed, good for single-user
- Ollama: Local models, privacy, free, fast

**Alternatives considered:**
- Node.js: Less mature AI libraries
- PostgreSQL: Overkill for single-user
- Cloud APIs: Privacy concerns, costs

---

### Γ£à AI Providers

**Decision:** Ollama (local) ΓåÆ Cloud APIs (when needed)

**Order of preference:**
1. Ollama local (free, private, fast)
2. Chinese APIs (if accessible in ╨á╨ñ)
3. Western APIs (if payment possible)

**Providers to test:**
- SiliconFlow (free, Chinese)
- Zhipu AI (free, Chinese)
- DeepSeek (cheap, Chinese)
- Groq (free tier, Western)

---

### Γ£à Video Analysis Flow

**Decision:** yt-dlp + youtube-transcript-api + AI summary

**Components:**
1. `yt_dlp` - video metadata (title, channel, duration, chapters)
2. `youtube_transcript_api` - transcript fetching
3. AI model - summary generation

**Previous attempt:** pytube (failed due to API changes)

---

### Γ£à Summary Format

**Decision:** Structured format with 4 sections

**English format:**
```
What it's about:
[1 sentence]

Key points:
[3-5 bullets]

Tools/Solutions:
[Names + descriptions + key differences]

Conclusion:
[Takeaway]
```

**Russian format:** Same structure, Russian headings

**Rationale:**
- Structured > free-form
- Key differences for comparisons
- Language-aware (transcript language ΓåÆ summary language)

---

### Γ£à Tags Format

**Decision:** English only, lowercase, deduplicated

**Format:** `ai, youtube, summarizer, tools, productivity`

**Constraints:**
- Max 16 tags
- Lowercase only
- 1-3 words per tag
- No duplicates

**Previous attempt:** Categorized tags (removed - too noisy)

---

### Γ£à Proxy Auto-Detection

**Decision:** Read from Obsidian vault settings file

**Source:** `Obsidian/Work/Idea proxy settings.md`

**Format in file:** `127.0.0.1 12334` (space-separated)

**Implementation:**
- Auto-detects on startup
- Sets environment variables
- Used by yt-dlp, transcript API

---

### Γ£à Repository Structure

**Decision:** Separate repo from Obsidian vault

**Structure:**
```
ai-secretary/
Γö£ΓöÇΓöÇ src/secretary/           # Python package
Γö£ΓöÇΓöÇ docs/research/           # Research documents
Γö£ΓöÇΓöÇ agents/                  # Agent context
Γö£ΓöÇΓöÇ pyproject.toml
ΓööΓöÇΓöÇ README.md
```

**Rationale:**
- Cleaner git history
- Can be pip-installed
- Doesn't pollute Obsidian vault

---

### Γ£à CLI Framework

**Decision:** Typer + Rich

**Rationale:**
- Typer: Type hints, easy commands
- Rich: Pretty output, tables, panels

**Commands:**
- `add` - add material
- `analyze` - analyze material
- `learn` - mark as learned
- `status` - show details
- `sync` - sync to Obsidian

---

### Γ£à Database Schema

**Decision:** SQLite with SQLAlchemy ORM

**Tables:**
- `materials` - main table
- `learning_history` - audit log

**Key fields:**
- id, title, type, status
- source_url, summary, tags
- novelty_score, video_metadata
- timestamps

---

## Backlog Decisions (Not Yet Made)

### ΓÅ│ Agentic Chain for Summarization

**Question:** Should we use multiple small prompts instead of one?

**Status:** Research needed

**Factors:**
- Quality improvement potential
- Latency cost
- Implementation complexity

---

### ΓÅ│ Brotab vs Browser Extension

**Question:** How to parse browser tabs?

**Options:**
- Brotab (CLI-based)
- Browser extension
- Manual URL list

**Status:** Not implemented

---

### ΓÅ│ Novelty Scoring

**Question:** How to compute novelty accurately?

**Current:** Embeddings + cosine similarity

**Issues:**
- Quality depends on embedding model
- Threshold tuning needed

---

### ΓÅ│ Embeddings Provider

**Question:** Which embedding model to use?

**Options:**
- Ollama (nomic-embed-text) - local, free
- OpenAI (text-embedding-3-small) - paid
- Cohere (embed-multilingual) - free tier

**Status:** Using Ollama nomic-embed-text

---

## Decision Reviews

These decisions should be revisited periodically:

| Decision | Review Date | Status |
|----------|-------------|--------|
| Ollama as primary | 2026-05-04 | Γ£à Still valid |
| Typer + Rich | 2026-05-04 | Γ£à Still valid |
| Summary format | 2026-04-11 | ΓÅ│ Need user feedback |
| Tags format | 2026-04-11 | ΓÅ│ Need user feedback |
