# AI Secretary — Specification

> Version: v2
> Date: 2026-04-05
> Status: In Review

---

## 1. Problem Statement

**What problem are we solving?**
Users want to efficiently manage their knowledge base in Obsidian by:
- Finding and summarizing educational videos from YouTube
- Tracking what they've learned and identifying new content
- Avoiding duplicate information across multiple sources
- Getting AI assistance for research and comparisons

**Who is affected?**
- Knowledge workers using Obsidian for personal knowledge management
- Learners who consume大量 YouTube educational content
- Researchers tracking multiple information sources

**Why now?**
- YouTube contains vast educational content but no native Obsidian integration exists
- Local AI models (Ollama) now provide free, private inference
- Chinese AI APIs (Zhipu, SiliconFlow) provide free tiers accessible from Russia

---

## 2. Goals & Non-Goals

### Goals
- [ ] CLI tool for adding YouTube videos to knowledge base with one command
- [ ] Automatic video analysis: transcript → structured summary → tags
- [ ] Novelty scoring: compare new content against learned materials
- [ ] Direct AI agent queries for research, comparison, and Q&A
- [ ] Intelligent AI provider auto-selection (free first: Ollama → Zhipu → SiliconFlow)
- [ ] Obsidian plugin for quick actions from within Obsidian
- [ ] API server for external integrations

### Non-Goals
- [ ] Mobile app or web interface (CLI-first approach)
- [ ] Paid AI API integration (free providers only)
- [ ] Real-time YouTube streaming or live detection
- [ ] Social features, sharing, or collaboration

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Testable? |
|----|-------------|----------|-----------|
| FR-001 | `secretary add <url>` adds material to database | Must | Yes — run command, check DB |
| FR-002 | `secretary analyze <id>` extracts summary + tags | Must | Yes — check material fields |
| FR-003 | `secretary learn <id>` marks material as learned | Must | Yes — check status change |
| FR-004 | `secretary query <text>` searches learned materials | Must | Yes — run query, verify results |
| FR-005 | `secretary recommend` returns materials sorted by novelty | Must | Yes — check sorting |
| FR-006 | `secretary ask <question>` queries AI with auto-select | Must | Yes — verify response |
| FR-007 | `secretary compare <a> <b>` compares two items | Should | Yes — verify comparison |
| FR-008 | `secretary research <topic>` generates research summary | Should | Yes — verify output |
| FR-009 | `secretary add-from-tabs` imports YouTube from browser | Should | Yes — check imported URLs |
| FR-010 | Auto-proxy detection from Obsidian settings | Should | Yes — verify proxy usage |
| FR-011 | Zhipu AI integration (free tier) | Must | Yes — test API call |
| FR-012 | SiliconFlow integration (free tier) | Could | Yes — test API call |
| FR-013 | Obsidian plugin with ribbon icon + commands | Should | Yes — test in Obsidian |

### 3.2 Non-Functional Requirements

| ID | Requirement | Metric | Target |
|----|-------------|--------|--------|
| NFR-001 | Video analysis speed | Response time | < 30s for 10-min video |
| NFR-001 | AI query response | Response time | < 10s for simple queries |
| NFR-002 | Database size | Materials supported | 10,000+ |
| NFR-003 | Privacy | Data stays local | Ollama + local DB |
| NFR-004 | Provider fallback | Auto-switch on failure | 100% uptime |

---

## 4. User Stories / Use Cases

### UC-001: Add and Analyze YouTube Video
- **Actor:** User with CLI access
- **Scenario:**
  1. User runs `secretary add https://youtube.com/watch?v=...`
  2. System fetches video metadata
  3. User runs `secretary analyze <id>`
  4. System gets transcript, generates summary + tags
- **Expected Outcome:** Material has summary, tags, novelty_score
- **Error Paths:**
  - No transcript → use title + metadata only

### UC-002: Query Knowledge Base
- **Actor:** User asking research question
- **Scenario:**
  1. User runs `secretary query "neural networks"`
  2. System searches learned materials
  3. System returns relevant materials with summaries
- **Expected Outcome:** List of related materials

### UC-003: Get Learning Recommendations
- **Actor:** User wanting to learn
- **Scenario:**
  1. User runs `secretary recommend`
  2. System sorts pending materials by novelty
  3. User receives prioritized learning list
- **Expected Outcome:** Ranked list of materials

---

## 5. Architecture / Design

### 5.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
├─────────────────┬─────────────────┬─────────────────────────┤
│  Obsidian       │      CLI        │   API Server            │
│  Plugin         │   (Typer)       │   (HTTP)                │
└────────┬────────┴────────┬────────┴────────┬────────────────┘
         │                  │                 │
         v                  v                 v
┌─────────────────────────────────────────────────────────────┐
│                     CORE (Python)                            │
├─────────────────────────────────────────────────────────────┤
│  AI Router ─────────────► Material Manager ─────────────► DB │
│  (Ollama/Zhipu/SF)       (CRUD + novelty)      (SQLite)    │
│         │                        │                          │
│         v                        v                          │
│  Video Analyzer ◄───────── Knowledge Base                   │
│  (yt-dlp + transcript)     (ChromaDB - future)             │
└─────────────────────────────────────────────────────────────┘
         │                  │                 │
         v                  v                 v
┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐
│  Obsidian   │  │   Vector DB  │  │   Browser History       │
│  Vault      │  │  (ChromaDB)  │  │   (Opera/Chrome)        │
└─────────────┘  └─────────────┘  └─────────────────────────┘
```

### 5.2 Components

| Component | Responsibility | Format/Technology |
|-----------|----------------|-------------------|
| ai_router.py | AI provider abstraction + auto-select | Python class |
| material_manager.py | CRUD + novelty scoring | Python class |
| video_analyzer.py | YouTube parsing + summarization | Python class |
| database.py | SQLite operations | SQLAlchemy |
| cli/main.py | CLI commands | Typer + Rich |
| obsidian.py | Obsidian vault sync | Python + Obsidian API |
| api.py | HTTP API server | Flask/FastAPI |

### 5.3 Data Flow

1. **Add Material:** `add` → normalize URL → check duplicates → save to DB
2. **Analyze:** `analyze` → fetch transcript → generate summary → extract tags → compute novelty
3. **Learn:** `learn` → update status → trigger re-index of pending materials
4. **Query:** `query` → search DB → return ranked results

---

## 6. Data Model

### 6.1 Entities

```python
class Material:
    id: str                      # UUID
    obsidian_path: str | None   # Path in vault
    type: str                    # "video", "article"
    source_url: str | None       # YouTube URL
    title: str                   # Material title
    status: str                  # "pending", "analyzing", "learned", "skipped"
    novelty_score: float | None  # 0-1, higher = more novel
    tags: list[str]              # Extracted tags
    summary: str | None          # Generated summary
    added_at: datetime           # When added
    analyzed_at: datetime | None # When analyzed
    learned_at: datetime | None  # When marked learned
    video_metadata: VideoMetadata | None
    related_materials: list[str] # IDs of related

class VideoMetadata:
    channel: str | None
    views: int | None
    likes: int | None
    transcript: str | None
    chapters: list[VideoChapter]
    duration: int | None
```

### 6.2 Data Formats

**SQLite Schema:**
```sql
CREATE TABLE materials (
  id TEXT PRIMARY KEY,
  obsidian_path TEXT,
  type TEXT,
  source_url TEXT,
  title TEXT,
  status TEXT DEFAULT 'pending',
  novelty_score REAL,
  tags_json TEXT,
  summary TEXT,
  added_at TIMESTAMP,
  analyzed_at TIMESTAMP,
  learned_at TIMESTAMP,
  video_metadata_json TEXT,
  related_materials_json TEXT
);
```

**Obsidian Frontmatter:**
```yaml
---
created: 2026-04-04
type: video
status: learned
source_url: https://youtube.com/watch?v=...
tags: [ai, youtube, summarizer]
summary: |
  **What it's about:** ...
  **Key points:** ...
novelty_score: 0.85
learned_at: 2026-04-05
---
```

---

## 7. API / Interfaces

### 7.1 CLI Commands

```bash
# Materials
secretary add <url>                      # Add material
secretary list-materials                 # List all
secretary status <id>                    # Show status
secretary analyze <id>                   # Analyze + summarize
secretary learn <id> --sync              # Mark learned + sync

# Video
secretary video-summarize <url>          # Summarize video
secretary video-chapters <url>           # Get chapters

# AI
secretary ask <question>                 # Query AI
secretary compare <a> <b>                 # Compare items
secretary research <topic>               # Research topic

# Knowledge Base
secretary query <text>                   # Search
secretary recommend                      # Get recommendations

# System
secretary providers                      # Show AI providers
secretary add-from-tabs                  # Import from browser
```

### 7.2 API Server Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /providers | Available AI providers |
| GET | /ask?q=... | Ask AI question |
| GET | /recommend | Learning recommendations |
| GET | /query?q=... | Search knowledge base |
| GET | /materials | List all materials |

---

## 8. Edge Cases

| ID | Scenario | Expected Behavior |
|----|----------|-------------------|
| EC-001 | No transcript available | Use video title + metadata only |
| EC-002 | Duplicate URL | Raise error, don't add |
| EC-003 | Very long transcript | Truncate to 4000 chars |
| EC-004 | AI provider fails | Auto-fallback to next provider |
| EC-005 | Browser history locked | Return empty, show warning |
| EC-006 | Proxy required but not working | Show error, continue without |
| EC-007 | Non-YouTube URL | Accept but skip video-specific features |

---

## 9. Acceptance Criteria

| ID | Criterion | Verification Method |
|----|-----------|---------------------|
| AC-001 | `secretary add <yt_url>` creates material with normalized URL | Run command, verify DB |
| AC-002 | `secretary analyze <id>` populates summary + tags | Run, check fields |
| AC-003 | `secretary query` returns matching learned materials | Add learned material, query by keyword |
| AC-004 | Novelty score distinguishes new from duplicate content | Add similar videos, compare scores |
| AC-005 | `secretary ask` returns response from AI | Run, verify response |
| AC-006 | Provider auto-select chooses working provider | Disable one provider, verify fallback |
| AC-007 | Obsidian sync creates proper markdown file | Run sync, check vault |

---

## 10. Risks & Trade-offs

### 10.1 Risks

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R-001 | Proxy connection flaky | High | Medium | Graceful fallback |
| R-002 | Zhipu API changes | Medium | Low | Config-driven endpoint |
| R-003 | Small models produce template phrases | High | Low | Use larger models (phi3) |

### 10.2 Trade-offs

| Decision | Alternative | Why This Choice |
|----------|-------------|-----------------|
| CLI-first approach | GUI or web UI | Simpler, faster to build |
| Free AI providers only | Paid APIs | Accessibility from Russia |
| SQLite over PostgreSQL | PostgreSQL | Simpler, sufficient for use case |
| Single-file config | Multi-file config | Single source of truth |

---

## 11. Open Questions

| ID | Question | Owner | Status |
|----|----------|-------|--------|
| OQ-001 | How to handle non-video materials (articles)? | Owner | Open |
| OQ-002 | Should we implement real-time YouTube notifications? | Owner | Open |
| OQ-003 | Best strategy for ChromaDB integration? | Owner | Open |

---

## 12. Changelog

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v1 | 2026-04-04 | Initial spec creation | Dev |
| v2 | 2026-04-05 | Refined with spec-template, added all sections | Workflow |