# Spec Refinement Workflow v3

## Overview

An iterative system for improving specification quality. Supports two coordination protocols:

- **Sequential Self-Organizing** (v3, default for strong models) — agents in fixed order, autonomous role choice
- **Writer/Critic** (v2, fallback for weaker models) — two fixed roles in review-fix loop

Protocol selection is automatic via capability detection test.

Based on:
- Self-Refine framework (Madaan et al., NeurIPS 2023)
- Probabilistic convergence theory (Yang et al., EMNLP 2025)
- Self-organizing multi-agent systems (Dochkina, arXiv 2026) — Sequential protocol outperforms centralized by 14%, fully autonomous by 44%

---

## Protocol Selection: Capability Detection

### Step 0a: Check Cache

Check `.opencode/plans/.capability-cache.json`:
- If exists and < 30 days old → use cached protocol
- If missing, expired, or model changed → run capability test

### Step 0b: Run Capability Test

Load `capability-test.md` and present the 3-task test to the model:
1. **Self-Reflection** (30%) — identify weaknesses, rate confidence
2. **Deep Reasoning** (40%) — resolve contradictory requirements
3. **Instruction Following** (30%) — exact format compliance

Score each task 0-1. Calculate:
```
overall = (task1 * 0.30) + (task2 * 0.40) + (task3 * 0.30)
```

### Decision

```
IF overall >= 0.70:
    protocol = "sequential"
    assessment = "STRONG MODEL — self-organizing capable"
ELSE:
    protocol = "writer-critic"
    assessment = "FALLBACK — structured protocol needed"
```

Cache result in `.opencode/plans/.capability-cache.json`.

---

## Protocol A: Sequential Self-Organizing (v3)

### Architecture

```
User Idea
    |
    v
[Agent 1] ── chooses role: WRITE / CRITIQUE / REVISE / ABSTAIN
    |            sees: previous round's final spec
    v
[Agent 2] ── chooses role autonomously
    |            sees: Agent 1 output + previous spec
    v
[Agent 3] ── chooses role autonomously
    |            sees: Agent 1 + 2 outputs + previous spec
    v
[Agent 4] ── chooses role autonomously
    |            sees: Agent 1 + 2 + 3 outputs + previous spec
    v
[Exit Check]
```

**Key principle (Dochkina, 2026):** Each agent sees **completed outputs** of predecessors (factual results), not **intentions** (plans). This informational advantage enables spontaneous role differentiation without central coordination.

### Execution Protocol

#### Step 1: First Draft
1. Load `agent-prompt.md` as system prompt for Agent 1
2. Load `spec-template.md` as template
3. Load `examples/good-spec.md` as quality reference
4. Conduct hybrid interview if needed (max 3-5 questions, max 2 rounds)
5. Agent 1 produces `spec_v1.md` (role: WRITE)

#### Step 2: Sequential Round
For each agent (2, 3, 4) in order:
1. Load `agent-prompt.md` as system prompt
2. Feed ALL predecessor outputs from current round + previous round's final spec
3. Agent autonomously chooses role (WRITE / CRITIQUE / REVISE / ABSTAIN)
4. Agent produces output in chosen role's format

After all 4 agents complete:
- Aggregate outputs into `spec_v{N}.md`
- Run critic scoring if enabled

#### Step 3: Exit Check
```
IF all_agents_abstained:
    STOP (CEILING)

IF composite_score >= 4.5:
    STOP (APPROVED)

IF consecutive_no_improvement >= 2:
    STOP (CONVERGED)

IF round >= MAX_ROUNDS:
    STOP (MAX_ROUNDS_REACHED)

Otherwise: round += 1, continue
```

---

## Protocol B: Writer/Critic (v2 Fallback)

### Architecture

```
User Idea -> [Writer] -> spec_v1 -> [Critic] -> score + findings
                                      |
                            improved? ──No──> STOP
                                    Yes
                                      |
                                      v
                            [Writer] -> spec_v2 -> [Critic] -> ...
```

### Execution Protocol

#### Step 1: Writer Creates v1
1. Load `agent-writer.md` as system prompt
2. Load `examples/good-spec.md` as few-shot reference
3. Conduct hybrid interview (if needed)
4. Produce `spec_v1.md`

#### Step 2: Critic Reviews
1. Load `agent-critic.md` as system prompt
2. Feed current spec to Critic
3. Critic returns: scores (5 dimensions), composite, findings, verdict

#### Step 3: Exit Check
```
IF composite_score >= 4.5: STOP (APPROVED)
IF total_findings == 0: STOP (APPROVED)
IF consecutive_no_improvement >= 2: STOP (CEILING)
IF iteration >= 5: STOP (MAX_ITERATIONS)
Otherwise: continue
```

#### Step 4: Writer Incorporates Feedback
1. Feed findings to Writer with current spec
2. Writer addresses each finding, increments version, updates changelog
3. Go to Step 2

---

## Scoring Rubric (used by Critic)

5 dimensions, each 1-5:

| Dimension | What it evaluates |
|---|---|
| **Completeness** | All sections filled, edge cases covered, acceptance criteria present |
| **Consistency** | No contradictions, valid cross-references, uniform terminology |
| **Concreteness** | Measurable requirements, specific metrics, zero vague language |
| **Implementability** | Clear architecture, complete API contracts, ready for implementation |
| **Risk Coverage** | Risks identified with mitigation, trade-offs justified, open questions tracked |

**Composite >= 4.5** — APPROVED
**Composite 3.5-4.49** — NEEDS_REVISION
**Composite < 3.5** — FUNDAMENTAL_REWORK

---

## Quick Start

### Automatic (recommended)

```
-start
Start the spec refinement workflow.

User idea: {describe your idea}

Follow the workflow in .opencode/plans/workflow.md:
1. Run capability detection (capability-test.md)
2. Use the recommended protocol
3. Loop until exit conditions are met
4. Return the best version with workflow log
```

### Force Sequential (v3)

```
-start
Start the spec refinement workflow using Sequential Self-Organizing protocol (v3).

User idea: {describe your idea}

Follow Protocol A (Sequential). Skip capability test.
```

### Force Writer/Critic (v2)

```
-start
Start the spec refinement workflow using Writer/Critic protocol (v2).

User idea: {describe your idea}

Follow Protocol B (Writer/Critic).
```

---

## File Structure

```
.opencode/plans/
├── spec-template.md
├── agent-writer.md
├── agent-critic.md
├── agent-prompt.md
├── capability-test.md
├── workflow.md
├── examples/
│   └── good-spec.md
└── specs/
    └── {project-slug}/
        ├── spec_v1.md
        ├── spec_v2.md
        ├── spec_final.md
        └── workflow_log.md
```