# Specification: URL Shortener API

> Version: v1
> Date: 2026-04-05
> Author: Agent-Writer (Example)
> Status: Approved

---

## 1. Problem Statement

**What problem are we solving?**
Long URLs are inconvenient for sharing on social networks, email, and print materials. Users need a service that transforms long URLs into short, memorable links with click tracking.

**Who is affected?**
Marketers, content creators, regular users who need to share links.

**Why now?**
Growing use of social networks and messengers where character limit and visual cleanliness matter.

---

## 2. Goals & Non-Goals

### Goals
- G-001: Shorten URLs to 6-character codes in < 100ms (p95)
- G-002: Redirect from short URL to original in < 200ms (p95)
- G-003: Track click count for each short link
- G-004: Support 10,000 redirects per second

### Non-Goals
- Custom aliases (user cannot choose their short URL)
- Expiration dates for links
- QR code generation
- User accounts and authentication

---

## 3. Requirements

### 3.1 Functional Requirements
| ID | Requirement | Priority | Testable? |
|---|---|---|---|
| FR-001 | POST /shorten accepts long_url and returns short_code | Must | Yes — send POST, verify 201 + short_code in response |
| FR-002 | GET /{short_code} redirects (301) to original URL | Must | GET /abc123, verify 301 + Location header |
| FR-003 | GET /{short_code}/stats returns click count | Should | GET /abc123/stats, verify JSON with click_count |
| FR-004 | URL validation — reject invalid URLs with 400 | Must | POST with "not-a-url", verify 400 |
| FR-005 | GET /{short_code} for non-existent code returns 404 | Must | GET /zzzzzz, verify 404 |

### 3.2 Non-Functional Requirements
| ID | Requirement | Metric | Target |
|---|---|---|---|
| NFR-001 | Shortening latency | p95 response time | < 100ms |
| NFR-002 | Redirect latency | p95 response time | < 200ms |
| NFR-003 | Throughput | Requests per second | >= 10,000 |
| NFR-004 | Availability | Uptime | >= 99.9% |

---

## 4. User Stories / Use Cases

### UC-001: Shorten URL
- **Actor:** User
- **Scenario:** POST /shorten with body {"long_url": "https://example.com/very/long/path"} -> 201 Created with body {"short_code": "aB3xK9", "short_url": "https://short.link/aB3xK9"}
- **Expected Outcome:** Short_code saved in DB, user receives short link
- **Error Paths:**
  - Invalid URL -> 400 Bad Request with {"error": "Invalid URL format"}
  - URL already exists -> 200 OK with existing short_code (idempotent)

### UC-002: Redirect
- **Actor:** User browser
- **Scenario:** GET /aB3xK9 -> 301 Redirect with Location: https://example.com/very/long/path
- **Expected Outcome:** Browser redirects to original URL, click_count increments
- **Error Paths:**
  - Code not found -> 404 Not Found with {"error": "Short URL not found"}
  - Code expired (if TTL added) -> 410 Gone

---

## 5. Architecture / Design

### 5.1 High-Level Architecture
```
Client -> [API Gateway] -> [URL Shortener Service] -> [Redis Cache]
                                              |
                                              v
                                         [PostgreSQL]
```

### 5.2 Components
| Component | Responsibility | Technology | Dependencies |
|---|---|---|---|
| API Gateway | Rate limiting, routing, TLS | Nginx | None |
| URL Shortener Service | Business logic: shorten, redirect, stats | Go (net/http) | Redis, PostgreSQL |
| Redis Cache | Cache popular redirects | Redis 7.x | None |
| PostgreSQL | Persistent storage URL mappings | PostgreSQL 16 | None |

### 5.3 Data Flow
1. Shorten: Client -> API -> Service -> generate code -> check uniqueness -> save to DB -> return code
2. Redirect: Client -> API -> Service -> check cache -> if miss, query DB -> cache result -> 301 redirect
3. Stats: Client -> API -> Service -> query DB -> return click_count

---

## 6. Data Model

### 6.1 Entities
```
url_mapping
  - id: BIGSERIAL (PK)
  - short_code: VARCHAR(6) (UNIQUE, NOT NULL)
  - long_url: TEXT (NOT NULL)
  - click_count: BIGINT (DEFAULT 0)
  - created_at: TIMESTAMPTZ (NOT NULL, DEFAULT NOW())
  - updated_at: TIMESTAMPTZ (NOT NULL, DEFAULT NOW())
  indexes:
    - idx_short_code: UNIQUE (short_code)
```

### 6.2 Data Formats
```
POST /shorten Request:
{
  "long_url": "https://example.com/path"
}

POST /shorten Response (201):
{
  "short_code": "aB3xK9",
  "short_url": "https://short.link/aB3xK9"
}

GET /{code}/stats Response (200):
{
  "short_code": "aB3xK9",
  "long_url": "https://example.com/path",
  "click_count": 42,
  "created_at": "2026-04-05T10:00:00Z"
}
```

---

## 7. API / Interfaces

### 7.1 External APIs
| Method | Endpoint | Input | Output | Error Codes |
|---|---|---|---|---|
| POST | /shorten | {long_url: string} | {short_code, short_url} | 400, 429 |
| GET | /{short_code} | — | 301 Redirect | 404 |
| GET | /{short_code}/stats | — | {short_code, long_url, click_count, created_at} | 404 |

### 7.2 Internal Interfaces
```go
type URLShortener interface {
    Shorten(ctx context.Context, longURL string) (string, error)
    Resolve(ctx context.Context, shortCode string) (string, error)
    IncrementClick(ctx context.Context, shortCode string) error
    GetStats(ctx context.Context, shortCode string) (*URLStats, error)
}
```

---

## 8. Edge Cases

| ID | Scenario | Expected Behavior |
|---|---|---|
| EC-001 | Empty long_url in request | 400 Bad Request with "long_url is required" |
| EC-002 | URL longer than 2048 characters | 400 Bad Request with "URL exceeds maximum length" |
| EC-003 | All 6-character codes used (~56B combinations) | 503 Service Unavailable with "Code space exhausted" |
| EC-004 | Concurrent requests for same long_url | Idempotent: return existing short_code |
| EC-005 | Redis unavailable | Fallback to PostgreSQL directly, no cache |
| EC-006 | Rate limit exceeded (100 req/min per IP) | 429 Too Many Requests with Retry-After header |
| EC-007 | URL with tracking parameters (?utm_source=...) | Store as-is, do not modify |

---

## 9. Acceptance Criteria

| ID | Criterion | Verification Method |
|---|---|---|
| AC-001 | Given valid long_url, when POST /shorten, then 201 with short_code of length 6 | Test |
| AC-002 | Given existing short_code, when GET /{code}, then 301 with Location = original URL | Test |
| AC-003 | Given non-existent short_code, when GET /{code}, then 404 | Test |
| AC-004 | Given 1000 redirects, when GET /stats, then click_count = 1000 | Test |
| AC-005 | Given invalid URL, when POST /shorten, then 400 with error message | Test |
| AC-006 | Given p95 latency, when 10,000 req/s, then shorten < 100ms, redirect < 200ms | Load test |

---

## 10. Risks & Trade-offs

### 10.1 Risks
| ID | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R-001 | Code collision (two URLs get same short_code) | Low | High | Check uniqueness before insert, retry with new code |
| R-002 | Hot key in Redis (one URL gets 90% traffic) | Medium | Medium | Local cache at service level for hot keys |
| R-003 | SQL injection via long_url | Low | High | Parameterized queries, ORM |
| R-004 | PostgreSQL disk full | Low | High | Monitoring, auto-cleanup of old records |

### 10.2 Trade-offs
| Decision | Alternative | Why This Choice |
|---|---|---|
| 6 characters Base62 | 8 characters or Base58 | 6 characters = 56B combinations (enough), Base62 = URL-safe + compact |
| Redis + PostgreSQL | PostgreSQL only | Redis for hot path redirects — critical for < 200ms p95 |
| 301 (permanent) redirect | 302 (temporary) redirect | 302 cached by browser — can't update URL later. 301 gives control. |
| No custom aliases | Support custom aliases | Custom aliases = collision handling, abuse prevention, moderation. Out of scope for v1. |

---

## 11. Open Questions

| ID | Question | Owner | Status |
|---|---|---|---|
| OQ-001 | Is TTL for short links needed? | Product Owner | Open |
| OQ-002 | Which domain to use for short links? | Product Owner | Open |
| OQ-003 | Is per-API-key rate limiting needed (not just per IP)? | Engineering | Open |

---

## 12. Changelog

| Version | Date | Changes | Author |
|---|---|---|---|
| v1 | 2026-04-05 | Initial draft — example spec | Agent-Writer |