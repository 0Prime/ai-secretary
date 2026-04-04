# Research Index

Collection of research documents for the ai-secretary project.

## Documents

### free-llm-apis-2026.md
Comprehensive list of LLM APIs with free tiers.

**Topics covered:**
- Provider APIs (Cohere, Gemini, Mistral, Zhipu)
- Inference providers (Groq, HuggingFace, Cerebras, etc.)
- For Russia section
- DeepSeek details (registration, payment, API)
- Zhipu AI, SiliconFlow, GigaChat

**Key findings:**
- Many free options available
- DeepSeek works in Russia (needs Alipay for payment)
- Chinese providers (Zhipu, SiliconFlow) need testing

### youtube-summarizers-research.md
Best practices and prompts for YouTube video summarization.

**Topics covered:**
- Tools overview (Apify, video-lens, Glasp, NoteGPT)
- Best practices from each tool
- Prompt templates (English, Russian, Educational)
- Agentic chain approach
- Quality comparison

**Key findings:**
- Structured output > free-form
- For comparisons: always include key differences
- Agentic chain may improve quality with small models
- Language-aware summarization works

### chinese-ai-for-russia.md
Guide to using Chinese AI services from Russia.

**Topics covered:**
- DeepSeek: status Γ£à, registration Γ£à, payment ΓÜá∩╕Å
- Zhipu AI: status Γ¥ô, needs testing
- SiliconFlow: status Γ£à (likely)
- API details and Python examples

**Key findings:**
- DeepSeek confirmed working in Russia
- Payment requires Alipay (complicated but possible)
- Quality comparable to GPT-4

## Quick Reference

| Provider | Free | Works in ╨á╨ñ | Payment | Quality |
|----------|------|-------------|---------|---------|
| Ollama local | Γ£à | Γ£à | Γ£à | Γ¡ÉΓ¡ÉΓ¡É |
| DeepSeek | Γ¥î | Γ£à | ΓÜá∩╕Å Alipay | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡É |
| Zhipu AI | Γ£à | Γ¥ô | Γ¥ô | Γ¥ô |
| SiliconFlow | Γ£à | Γ¥ô | Γ¥ô | Γ¥ô |

## Research Needed

- [ ] Test Zhipu AI from Russia
- [ ] Test SiliconFlow from Russia
- [ ] Compare agentic chain vs single prompt
- [ ] Chinese model quality for summarization
- [ ] Cost/quality tradeoff analysis
