# Free LLM APIs 2026

A comprehensive list of LLM APIs with free tiers or permanent free access.

## Table of Contents
- [Provider APIs](#provider-apis)
- [Inference Providers](#inference-providers)
- [For Russia (╨á╨ñ)](#for-russia-)

## Provider APIs

APIs run by the companies that train or fine-tune the models themselves.

| Provider | Models | Free Tier | OpenAI Compatible | Region |
|---------|--------|-----------|------------------|--------|
| **Cohere** | Command A, Command R+, Aya Expanse 32B | 20 RPM, 1K/mo | Γ£à | ≡ƒç║≡ƒç╕ |
| **Google Gemini** | Gemini 2.5 Pro, Flash, Flash-Lite | 5-15 RPM, 100-1K RPD | Γ£à | ΓÜá∩╕Å EU/UK/CH blocked |
| **Mistral AI** | Mistral Large 3, Small 3.1 | 1 req/s, 1B tok/mo | Γ£à | ≡ƒç¬≡ƒç║ |
| **Zhipu AI** | GLM-4.7-Flash, GLM-4.5-Flash | Unknown limits | Γ£à | ≡ƒç¿≡ƒç│ |

## Inference Providers

Third-party platforms that host open-weight models.

| Provider | Models | Free Tier | OpenAI Compatible | Notes |
|---------|--------|-----------|------------------|-------|
| **Cerebras** | Llama 3.3 70B, Qwen3 235B | 30 RPM, 14,400 RPD | Γ£à | Fast inference |
| **Cloudflare Workers AI** | Llama 3.3 70B, Qwen QwQ 32B | 10K neurons/day | Γ£à | Edge computing |
| **GitHub Models** | GPT-4o, Llama 3.3 70B, DeepSeek-R1 | 10-15 RPM, 50-150 RPD | Γ£à | Requires GitHub account |
| **Groq** | Llama 3.3 70B, Llama 4 Scout, Kimi K2 | 30 RPM, 1K RPD | Γ£à | Lightning fast |
| **Hugging Face** | Llama 3.3 70B, Qwen2.5 72B | $0.10/mo credits | Γ£à | Many models |
| **Kluster AI** | DeepSeek-R1, Llama 4 Maverick | Unknown | Γ£à | - |
| **LLM7.io** | DeepSeek R1, Flash-Lite, Qwen2.5 | 30 RPM (120 with token) | Γ£à | - |
| **NVIDIA NIM** | Llama 3.3 70B, Mistral Large | 40 RPM | Γ£à | - |
| **Ollama Cloud** | DeepSeek-V3.2, Qwen3.5 | Light usage | Γ¥î | Uses Ollama API |
| **OpenRouter** | DeepSeek R1, Llama 3.3 70B | 20 RPM, 50 RPD (1K with $10) | Γ£à | Has free router |
| **SiliconFlow** | Qwen3-8B, DeepSeek-R1-Distill | 1K RPM, 50K TPM | Γ£à | ≡ƒç¿≡ƒç│ Chinese |

## For Russia (╨á╨ñ)

### DeepSeek

**Status:** Γ£à Works without VPN in Russia

**Registration:** platform.deepseek.com
- Email + password
- No VPN required

**Payment:** 
- Cards in yuan/dollars not available
- UnionPay cards don't work
- **Solution:** Alipay (Chinese phone number OK)
  - Need international passport
  - Or find people on Avito with Alipay balance

**API Details:**
```
Base URL: https://api.deepseek.com
Models: deepseek-chat, deepseek-coder
Prices: $0.27/1M input, $1.10/1M output
        (50% off: 16:30-00:30 UTC)
```

**Pros:**
- Works in Russia without VPN
- Cheaper than ChatGPT
- OpenAI-compatible
- Good quality

**Cons:**
- Payment requires Alipay
- Slightly slower than local models

**Resources:**
- [Habr article (RU)](https://habr.com/ru/articles/895864/)
- [GitHub example](https://github.com/mihailgok/deepseek)

### Zhipu AI (BigModel)

**Status:** Γ£à Works in China, unknown for Russia

**Registration:** open.bigmodel.cn

**Models:**
- GLM-4.7-Flash
- GLM-4.5-Flash
- GLM-4.6V-Flash

**Free Tier:** Claims "unlimited" usage (needs verification)

**API Details:**
```
Base URL: https://open.bigmodel.cn
Format: OpenAI compatible
```

**Resources:**
- [Documentation](https://open.bigmodel.cn/dev/api)
- [Free API article (RU)](https://jimo.studio/blog/zhipu-big-model-has-its-first-free-api/)

### SiliconFlow

**Status:** Γ£à Chinese provider, should work

**Registration:** cloud.siliconflow.cn

**Models:**
- Qwen3-8B
- DeepSeek-R1-Distill-Qwen-7B
- GLM-4.1V-9B-Thinking

**Free Tier:** 1K RPM, 50K TPM

**API Details:**
```
Base URL: https://api.siliconflow.cn
Format: OpenAI compatible
```

### GigaChat (╨á╨ñ)

**Status:** Γ£à Russian provider

**Registration:** developers.sber.ru

**Models:**
- GigaChat
- GigaChat Pro
- GigaChat Lite

**Free Tier:** Yes, with limits

**API:** Not OpenAI compatible (uses own format)

## Quick Comparison for Russia

| Provider | Free | Works in ╨á╨ñ | Easy Payment | Quality | Speed |
|----------|------|-------------|--------------|---------|-------|
| DeepSeek | Γ¥î (cheap) | Γ£à | ΓÜá∩╕Å Alipay | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡É | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡É |
| Zhipu AI | Γ£à | Γ¥ô | Γ¥ô | Γ¡ÉΓ¡ÉΓ¡É | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡É |
| SiliconFlow | Γ£à | Γ¥ô | Γ¥ô | Γ¡ÉΓ¡ÉΓ¡É | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡É |
| GigaChat | Γ£à | Γ£à | Γ£à | Γ¡ÉΓ¡ÉΓ¡É | Γ¡ÉΓ¡É |
| Ollama (local) | Γ£à | Γ£à | Γ£à | Γ¡ÉΓ¡ÉΓ¡É | Γ¡ÉΓ¡ÉΓ¡ÉΓ¡ÉΓ¡É |

## Recommendations

### For Development/Testing
1. **Ollama local** - free, fast, private
2. **SiliconFlow** - free Chinese models
3. **DeepSeek** - if payment is possible

### For Production
1. **DeepSeek** - best quality/price ratio
2. **SiliconFlow** - if DeepSeek payment fails
3. **GigaChat** - if Russian compliance needed

## Notes

- **RPM** = Requests per minute
- **RPD** = Requests per day
- **TPM** = Tokens per minute
- All endpoints are OpenAI SDK-compatible unless noted
- Trial credits and promos don't count as "permanent free"

## Links

- [awesome-free-llm-apis](https://github.com/mnfst/awesome-free-llm-apis) - Maintained list
- [DeepSeek GitHub](https://github.com/mihailgok/deepseek) - Russian examples
