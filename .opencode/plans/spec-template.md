# Specification: {Project/Feature Name}

> Version: {v1, v2, ...}
> Date: {YYYY-MM-DD}
> Author: {Agent-Writer}
> Status: {Draft | In Review | Approved}

---

## 1. Problem Statement

**What problem are we solving?**
{Clear description of the problem — state the pain point independently from the solution}

**Who is affected?**
{Target users, systems, or stakeholders}

**Why now?**
{Context, urgency, business drivers}

---

## 2. Goals & Non-Goals

### Goals
- {Goal 1 — must be measurable}
- {Goal 2 — must be measurable}
- {Goal 3 — must be measurable}

### Non-Goals
- {What is explicitly out of scope}
- {What we are NOT building in this iteration}

---

## 3. Requirements

### 3.1 Functional Requirements
| ID | Requirement | Priority | Testable? |
|---|---|---|---|
| FR-001 | {Description} | {Must/Should/Could} | {Yes — how to test} |
| FR-002 | {Description} | {Must/Should/Could} | {Yes — how to test} |

### 3.2 Non-Functional Requirements
| ID | Requirement | Metric | Target |
|---|---|---|---|
| NFR-001 | {Performance} | {e.g., response time} | {e.g., < 200ms p95} |
| NFR-002 | {Scalability} | {e.g., concurrent users} | {e.g., 1000+} |
| NFR-003 | {Security} | {e.g., auth method} | {e.g., OAuth2} |

---

## 4. User Stories / Use Cases

### UC-001: {Use Case Name}
- **Actor:** {Who}
- **Scenario:** {Step-by-step flow}
- **Expected Outcome:** {Specific, observable result}
- **Error Paths:**
  - {Error 1} -> {Handling}
  - {Error 2} -> {Handling}

### UC-002: {Use Case Name}
...

---

## 5. Architecture / Design

### 5.1 High-Level Architecture
{Description of components and their interactions}

```
{ASCII diagram or description}
```

### 5.2 Components
| Component | Responsibility | Format/Technology | Dependencies |
|---|---|---|---|
| {Name} | {What it does} | {Stack} | {What it depends on} |

### 5.3 Data Flow
{Description of how data moves through the system}

---

## 6. Data Model

### 6.1 Entities
{For software: database entities, types, schemas}
{For non-software: key concepts, definitions, taxonomies}
{If N/A for this spec type, mark as N/A and explain}

### 6.2 Data Formats
{API request/response schemas, config formats, file structures, etc.}
{If N/A, mark as N/A and explain}

---

## 7. API / Interfaces

### 7.1 External APIs
{For software: REST/GraphQL endpoints}
{For non-software: integration points, handoff procedures}
{If N/A, mark as N/A and explain}

### 7.2 Internal Interfaces
{Function signatures, class interfaces, event contracts, or process interfaces}

---

## 8. Edge Cases

| ID | Scenario | Expected Behavior |
|---|---|---|
| EC-001 | {Edge case description} | {How system handles it} |
| EC-002 | {Edge case description} | {How system handles it} |
| EC-003 | {Edge case description} | {How system handles it} |
| EC-004 | {Edge case description} | {How system handles it} |
| EC-005 | {Edge case description} | {How system handles it} |

---

## 9. Acceptance Criteria

| ID | Criterion | Verification Method |
|---|---|---|
| AC-001 | {Specific, measurable condition} | {Test / Review / Demo} |
| AC-002 | {Specific, measurable condition} | {Test / Review / Demo} |

---

## 10. Risks & Trade-offs

### 10.1 Risks
| ID | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R-001 | {Description} | {High/Med/Low} | {High/Med/Low} | {Plan B} |

### 10.2 Trade-offs
| Decision | Alternative | Why This Choice |
|---|---|---|
| {Choice made} | {What was rejected} | {Reasoning} |

---

## 11. Open Questions

| ID | Question | Owner | Status |
|---|---|---|---|
| OQ-001 | {Unresolved question} | {Who decides} | {Open/Resolved} |

---

## 12. Changelog

| Version | Date | Changes | Author |
|---|---|---|---|
| v1 | {date} | Initial draft | {name} |
| v2 | {date} | {What changed} | {name} |