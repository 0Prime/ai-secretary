# Capability Test: Model Strength Detection

## Purpose

Determine whether the current model is strong enough for Sequential Self-Organizing protocol, or should fall back to Writer/Critic (v2) protocol.

Based on Dochkina (2026), self-organization requires three capabilities:
1. **Self-reflection** — ability to assess one's own competence
2. **Deep reasoning** — multi-step logical chains
3. **Instruction following** — precise adherence to coordination protocols

## Test Procedure

Present the following test to the model. Evaluate responses against the scoring criteria.

---

## Test Input

```
You are about to take a capability assessment. Answer all 3 tasks.

=== TASK 1: Self-Reflection ===

Here is a section from a specification:

---
## 3. Requirements

### 3.1 Functional Requirements
The system should be fast and user-friendly. It should handle all user requests properly and provide good error messages.

### 3.2 Non-Functional Requirements
The system should be scalable and secure.
---

Identify 2 specific weaknesses in this section. For each weakness, rate your confidence that it is a real issue (1-5, where 5 = absolutely certain).

=== TASK 2: Deep Reasoning ===

Here are two requirements from the same specification:

- FR-001: All user data must be stored encrypted at rest using AES-256.
- FR-003: The search feature must return results in under 50ms for queries across all user data.

These requirements may conflict. Explain:
1. What is the contradiction?
2. Why does it exist?
3. Propose a viable resolution.

=== TASK 3: Instruction Following ===

Format the following data as a markdown table with exactly these columns: ID, Name, Priority, Status.

Data:
- Item 1: "Database migration" — it's critical — done
- Item 2: "UI redesign" — should have — in progress
- Item 3: "API documentation" — could wait — not started

Do not add extra columns. Do not change the column names. Do not add commentary outside the table.
```

---

## Scoring Agent

Scoring is performed by a separate evaluation agent (not the test-taker) using the criteria below. The evaluator should be the same model that will be used for the workflow — this ensures the test measures the actual model's capabilities, not a different model's.

## Scoring Criteria

### Task 1: Self-Reflection (Weight: 30%)

| Score | Criteria |
|---|---|
| 0 | No weaknesses identified, or identified things that aren't weaknesses |
| 0.5 | Identified 1 real weakness (e.g., "fast" is vague, no metrics) but missed the other |
| 1.0 | Identified 2+ real weaknesses (e.g., "fast/user-friendly" are vague, no testable criteria, NFRs lack metrics, "all user requests" is ambiguous) |

**Confidence calibration bonus:** If confidence ratings are >= 4 for real weaknesses and <= 3 for uncertain ones, add +0.1 (capped at 1.0 total).

### Task 2: Deep Reasoning (Weight: 40%)

| Score | Criteria |
|---|---|
| 0 | No contradiction identified, or incorrect analysis |
| 0.5 | Identified the contradiction (encryption slows down search) but resolution is superficial or impractical |
| 1.0 | Identified the contradiction AND proposed a viable resolution (e.g., encrypt non-indexed fields, use searchable encryption, cache decrypted search index, separate encrypted storage from search index) |

### Task 3: Instruction Following (Weight: 30%)

| Score | Criteria |
|---|---|
| 0 | Wrong format, wrong columns, or added extra content |
| 0.5 | Correct format but minor deviations (extra whitespace, wrong priority wording) |
| 1.0 | Exact format match: 4 columns (ID, Name, Priority, Status), 3 rows, no extra content |

**Note:** The correct output is:

```markdown
| ID | Name | Priority | Status |
|---|---|---|---|
| 1 | Database migration | critical | done |
| 2 | UI redesign | should have | in progress |
| 3 | API documentation | could wait | not started |
```

---

## Overall Score Calculation

```
overall_score = (task1_score * 0.30) + (task2_score * 0.40) + (task3_score * 0.30)
```

## Decision

```
IF overall_score >= 0.70:
    protocol = "sequential"
    assessment = "STRONG MODEL — capable of self-organizing coordination"
ELSE:
    protocol = "writer-critic"
    assessment = "FALLBACK — use structured Writer/Critic protocol (v2)"
```

## Cache Result

Store in `.opencode/plans/.capability-cache.json`:

```json
{
  "model": "<auto-detected or user-provided model name>",
  "score": <overall_score>,
  "task_scores": {
    "self_reflection": <task1_score>,
    "deep_reasoning": <task2_score>,
    "instruction_following": <task3_score>
  },
  "protocol": "<sequential|writer-critic>",
  "tested_at": "<ISO timestamp>",
  "test_version": "1.0"
}
```

## Re-Test Conditions

Re-run capability test if:
- User explicitly requests it
- Model name changed (detected different model)
- Cache is older than 30 days
- Sequential protocol consistently underperforms (score < 3.5 after 3 rounds)