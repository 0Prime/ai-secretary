# YouTube Video Summarizers Research

Research on best practices, tools, and prompts for YouTube video summarization.

## Table of Contents
- [Tools Overview](#tools-overview)
- [Best Practices](#best-practices)
- [Prompt Templates](#prompt-templates)
- [Agentic Approaches](#agentic-approaches)
- [Quality Comparison](#quality-comparison)

## Tools Overview

### Apify YouTube Summarizer
**URL:** apify.com/quotidian_vulture/youtube-summarizer

**Features:**
- Summarize any YouTube video with AI
- Timestamped key points with clickable links
- Supports 40+ languages
- **Free AI providers:** Gemini, Groq, OpenAI

**Pros:**
- Ready-to-use
- Multiple AI backends
- Handles long videos

**Cons:**
- Requires API keys for AI providers
- Cloud-dependent

### video-lens
**URL:** github.com/kar2phi/video-lens

**Features:**
- Generates structured HTML report
- Executive summary
- Key points with analysis
- Timestamped outline
- In-page YouTube player
- Markdown export

**Output Structure:**
```
1. Executive Summary ΓÇö 3-5 sentence TL;DR
2. Takeaway ΓÇö single most important insight (1-3 sentences)
3. Key Points ΓÇö bulleted, scannable insights with detail
4. Timestamped Outline ΓÇö clickable topics
5. In-page Player ΓÇö synced with content
```

**Pros:**
- No API keys needed (uses coding agent)
- Beautiful HTML output
- Interactive features

**Cons:**
- Requires coding agent (Claude, Copilot)
- HTML output, not markdown

### Glasp
**URL:** glasp.co

**Features:**
- Chrome extension
- YouTube Summary with ChatGPT/Claude
- Transcript highlighting
- Export to note-taking apps

**Pros:**
- Browser-based
- Good integration

**Cons:**
- Extension required
- Not CLI-friendly

### NoteGPT
**URL:** notegpt.io

**Features:**
- YouTube summarizer
- Transcript export
- Mind maps
- Notes organization

**Pros:**
- Feature-rich
- Multiple export formats

**Cons:**
- Free tier limits
- Cloud-dependent

## Best Practices

### From video-lens

1. **Separation of concerns**
   - Don't try to do everything in one prompt
   - Extract facts ΓåÆ Group themes ΓåÆ Generate insights ΓåÆ Create summary

2. **Takeaway-first approach**
   - Lead with the single most important insight
   - Then expand to supporting points

3. **Specific over generic**
   - "Deck App: fastest extraction, exports to PDF" 
   - NOT "A useful tool for videos"

4. **Timestamps for navigation**
   - Users should be able to jump to relevant parts

5. **Structured output**
   - Clear sections
   - Bullet points over paragraphs
   - Consistent formatting

### From SummaryAI Blog

**Prompt Types That Work:**

1. **Simple Summary**
   ```
   "Summarize the following YouTube video transcript in 5 clear bullet points."
   ```

2. **Key Insights**
   ```
   "Read the transcript and summarize the key insights and main lessons from this video."
   ```

3. **Structured Summary**
   ```
   "Create a summary with:
   - Main topic
   - Key points explained
   - Important examples
   - Final takeaway"
   ```

4. **Learning Notes**
   ```
   "Convert to study notes with:
   - Main topic
   - Key concepts
   - Important tips
   - Short summary"
   ```

### For Comparisons

When summarizing comparison videos, include:
- What is being compared
- Key criteria
- How they differ from each other
- Recommendation/verdict

**Bad:**
```
"The video compares 5 AI tools."
```

**Good:**
```
"5 AI summarizers compared:
- Deck App: fastest, PDF export
- 85: bullet-point summaries, 8 key points
- Glasp: ChatGPT integration, custom prompts
- NoGPTI: mind maps, presentations
- Yin Video: multi-speaker support

Best for quick scan: 85
Best for depth: Glasp
Best for visuals: NoGPTI"
```

## Prompt Templates

### English Summary (Tested)

```markdown
Analyze this transcript and create a structured summary.

Format:
1. **What it's about:** (1 sentence - no "video"/"video")
2. **Key points:** (3-5 bullet points - specific ideas, facts)
3. **Tools/Solutions:** (names + brief description + key difference from others)
4. **Conclusion:** (takeaway)

Be specific. If this is a comparison - describe key differences between items.

Transcript:
{transcript}

Summary:
```

### Russian Summary

```markdown
╨ƒ╤Ç╨╛╨░╨╜╨░╨╗╨╕╨╖╨╕╤Ç╤â╨╣ ╤é╤Ç╨░╨╜╤ü╨║╤Ç╨╕╨┐╤é ╨╕ ╤ü╨╛╨╖╨┤╨░╨╣ ╤ü╤é╤Ç╤â╨║╤é╤â╤Ç╨╕╤Ç╨╛╨▓╨░╨╜╨╜╤â╤Ä ╨▓╤ï╨╢╨╕╨╝╨║╤â.

╨ñ╨╛╤Ç╨╝╨░╤é:
1. **╨₧ ╤ç╤æ╨╝:** (1 ╨┐╤Ç╨╡╨┤╨╗╨╛╨╢╨╡╨╜╨╕╨╡ - ╨▒╨╡╨╖ "╨▓╨╕╨┤╨╡╨╛"/"video")
2. **╨Ü╨╗╤Ä╤ç╨╡╨▓╤ï╨╡ ╨╝╤ï╤ü╨╗╨╕:** (3-5 ╨┐╤â╨╜╨║╤é╨╛╨▓ - ╨║╨╛╨╜╨║╤Ç╨╡╤é╨╜╤ï╨╡ ╨╕╨┤╨╡╨╕, ╤ä╨░╨║╤é╤ï)
3. **╨ÿ╨╜╤ü╤é╤Ç╤â╨╝╨╡╨╜╤é╤ï/╨á╨╡╤ê╨╡╨╜╨╕╤Å:** (╨╜╨░╨╖╨▓╨░╨╜╨╕╤Å + ╨║╤Ç╨░╤é╨║╨╛╨╡ ╨╛╨┐╨╕╤ü╨░╨╜╨╕╨╡ + ╨║╨╗╤Ä╤ç╨╡╨▓╨╛╨╡ ╨╛╤é╨╗╨╕╤ç╨╕╨╡ ╨╛╤é ╨┤╤Ç╤â╨│╨╕╤à)
4. **╨ÿ╤é╨╛╨│:** (╨▓╤ï╨▓╨╛╨┤)

╨æ╤â╨┤╤î ╨║╨╛╨╜╨║╤Ç╨╡╤é╨╜╤ï╨╝. ╨ò╤ü╨╗╨╕ ╤ì╤é╨╛ ╤ü╤Ç╨░╨▓╨╜╨╡╨╜╨╕╨╡ - ╨╛╨┐╨╕╤ê╨╕ ╨║╨╗╤Ä╤ç╨╡╨▓╤ï╨╡ ╨╛╤é╨╗╨╕╤ç╨╕╤Å ╤ü╤Ç╨░╨▓╨╜╨╕╨▓╨░╨╡╨╝╤ï╤à ╤ê╤é╤â╨║.

╨ó╤Ç╨░╨╜╤ü╨║╤Ç╨╕╨┐╤é:
{transcript}

╨Æ╤ï╨╢╨╕╨╝╨║╨░:
```

### Educational Summary

```markdown
You will be provided with a YouTube video link. Your task is to analyze the video and create a summary suitable as an educational lesson.

Format:
1. **Lesson Reading Material:** (120-150 words summary)
2. **Learning Objectives:** (3 clear objectives)
3. **Quiz:** (3 multiple-choice questions with answers)
4. **Practical Exercise:** (1-2 hands-on activities)
5. **Slug:** (lowercase, hyphenated title)

Transcript:
{transcript}
```

## Agentic Approaches

### Hypothesis
Using a chain of smaller prompts instead of one large prompt can improve quality, especially with smaller models.

### Chain: Summarize Video

```
Step 1: Extract Facts
---
Prompt: "Extract ALL specific facts from this transcript. List each fact on a new line. Be exhaustive."
Output: ["fact 1", "fact 2", ...]

Step 2: Group by Themes
---
Prompt: "Group these facts into 3-5 themes. Return: Theme: [name], Facts: [indices]"
Output: ["Theme: Tool A, Facts: 1,3,5", ...]

Step 3: Generate Insights
---
Prompt: "For each theme, write 1-2 sentence insight. What does this mean? Why is it important?"
Output: ["Tool A is best for quick summaries because...", ...]

Step 4: Create Summary
---
Prompt: "Create a structured summary using these insights. Format: What, Key Points, Tools/Comparison, Conclusion"
Output: final structured summary
```

### Advantages of Chain

1. **Debugging** - Can see where quality breaks down
2. **Model flexibility** - Can use different models for different steps
3. **Less hallucinations** - Each step is simpler
4. **Caching** - Can cache intermediate results

### Disadvantages

1. **Latency** - Multiple API calls
2. **Complexity** - More code to maintain
3. **Cost** - More tokens overall

## Quality Comparison

| Aspect | Single Prompt | Agentic Chain | Hybrid |
|--------|---------------|---------------|--------|
| Speed | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡ÉΓ¡É | Γ¡ÉΓ¡É | Γ¡ÉΓ¡ÉΓ¡É |
| Quality (small model) | Γ¡ÉΓ¡É | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡É | Γ¡ÉΓ¡ÉΓ¡É |
| Quality (large model) | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡É | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡ÉΓ¡É | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡ÉΓ¡É |
| Cost | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡É | Γ¡ÉΓ¡É | Γ¡ÉΓ¡ÉΓ¡É |
| Debugging | Γ¡É | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡ÉΓ¡É | Γ¡ÉΓ¡ÉΓ¡É |
| Implementation | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡ÉΓ¡É | Γ¡É | Γ¡ÉΓ¡É |

## Recommendations

### For Small Models (llama3.2:1b, phi3)
Use agentic chain with focus on structure:
1. Extract facts (no creativity)
2. Group by themes (simple categorization)
3. Generate insights (guided format)
4. Final summary (follow template strictly)

### For Large Models (llama3.3:70b, GPT-4)
Single well-crafted prompt can work:
- Clear format specification
- Examples in prompt
- Constraints on output

### For Comparison Videos
Always include:
- What is compared
- Key differentiators
- Verdict/recommendation

### For Educational Videos
Consider:
- Learning objectives
- Quiz questions
- Practical exercises

## Open Questions / Research Needed

- [x] Test agentic chain vs single prompt with same model
- [ ] Optimal number of steps in chain
- [ ] Best models for each chain step
- [ ] Caching strategies for intermediate results
- [x] Chinese model quality for summarization (✅ Good: Zhipu GLM-4-flash tested)
- [ ] Cost/quality tradeoff analysis

### Test Results (2026-04-05)

**Tested with:** Zhipu GLM-4-flash on 3Blue1Brown neural networks video

**Single Prompt:**
- ✅ More structured output
- ✅ Follows format better
- ⚠️ May miss detailed facts
- Speed: ~3s

**Agentic Chain:**
- ✅ Better fact extraction
- ✅ Organized by themes
- ⚠️ Final output verbose, needs strict format
- Speed: ~9s (3 steps)

**Recommendation:**
- Large models (GPT-4, GLM-4): Single prompt is sufficient
- Small models (llama3.2:1b): Agentic chain may help
- For comparisons: Always include key differences

## Resources

- [video-lens GitHub](https://github.com/kar2phi/video-lens)
- [SummaryAI Blog](https://summaryai.app/blog/best-youtube-video-summary-prompts/)
- [AGENTVSAI Guide](https://agentvsai.com/how-to-summarize-youtube-videos-with-ai-ultimate-guide-2026/)
- [DocsBot Prompts](https://docsbot.ai/prompts/education/structured-video-summary)
