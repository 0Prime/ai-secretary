# Chinese AI APIs for Russia (╨á╨ñ)

Guide to using Chinese AI services from Russia, including registration, payment, and setup.

## Overview

| Provider | Status | Free Tier | Registration | Payment |
|----------|--------|-----------|--------------|---------|
| **DeepSeek** | Γ£à Works | Γ¥î (cheap) | Easy | ΓÜá∩╕Å Alipay |
| **Zhipu AI** | Γ¥ô Unknown | Γ£à | Easy | Γ¥ô |
| **SiliconFlow** | Γ£à Likely | Γ£à | Easy | Γ¥ô |
| **Baidu ERNIE** | Γ¥ô Unknown | Γ£à | Γ¥ô | Γ¥ô |

## DeepSeek

### Status
Γ£à **Confirmed working in Russia** - no VPN required

### Registration
1. Go to https://platform.deepseek.com
2. Click "Sign Up"
3. Enter email and password
4. Verify via email

### Payment from Russia

#### Problem
- Russian cards (rubles) don't work
- UnionPay cards don't work (tested by community)

#### Solution 1: Alipay
1. Register Alipay with Russian phone number
2. Need international passport (with NFC chip - better for Android)
3. Link UnionPay card to Alipay (some users report it doesn't work)
4. Alternative: Find people on Avito with Alipay balance

**Steps for Alipay registration (RU article):**
- Article on VC.ru: https://vc.ru/life/1342398

#### Solution 2: Use friends in China
- Find someone who can help top up

#### Solution 3: Use Alipay in stores
- Load cash to Alipay via payment terminals

### API Details

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
)

print(response.choices[0].message.content)
```

### Models

| Model | Description | Context | Use Case |
|-------|-------------|---------|----------|
| `deepseek-chat` | General chat | 8K | General tasks |
| `deepseek-coder` | Code-specific | 8K | Programming |

### Pricing

| Time | Input | Output |
|------|-------|--------|
| Standard (00:30-16:30 UTC) | $0.27/1M | $1.10/1M |
| Discount (16:30-00:30 UTC) | $0.135/1M | $0.55/1M |

**Comparison:**
- GPT-4o mini: ~$0.15/1M input
- DeepSeek is ~2x more expensive than GPT-4o mini

### Quality

From community tests:
- Slightly slower than local Ollama
- Quality comparable to GPT-4
- Good for Russian language
- Good coding abilities

### Resources

- **Habr article (RU):** https://habr.com/ru/articles/895864/
- **GitHub examples:** https://github.com/mihailgok/deepseek
- **Documentation:** https://api-docs.deepseek.com/

## Zhipu AI (BigModel)

### Status
Γ¥ô **Not confirmed for Russia** - needs testing

### Registration
1. Go to https://open.bigmodel.cn
2. Sign up with email
3. Get API key

### Models

| Model | Description | Context |
|-------|-------------|---------|
| `GLM-4.7-Flash` | Latest flagship | Long |
| `GLM-4.5-Flash` | Fast, capable | Medium |
| `GLM-4.6V-Flash` | Vision model | - |

### Free Tier
Claims "unlimited free usage" but limits are undocumented.

### API Details

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://open.bigmodel.cn"
)

response = client.chat.completions.create(
    model="glm-4-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
)
```

### Resources
- **Documentation:** https://open.bigmodel.cn/dev/api
- **Article (RU):** https://jimo.studio/blog/zhipu-big-model-has-its-first-free-api/

## SiliconFlow

### Status
Γ£à **Should work** - Chinese provider

### Registration
1. Go to https://cloud.siliconflow.cn
2. Sign up
3. Get API key

### Models

| Model | Description |
|-------|-------------|
| `Qwen/Qwen3-8B` | Alibaba's latest |
| `Qwen/Qwen2.5-32B-Instruct` | Larger, faster |
| `DeepSeek-R1-Distill-Qwen-7B` | Reasoning model |
| `GLM-4.1V-9B-Thinking` | Vision + reasoning |

### Free Tier
- 1,000 requests per minute (RPM)
- 50,000 tokens per minute (TPM)

### API Details

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.siliconflow.cn"
)

response = client.chat.completions.create(
    model="Qwen/Qwen3-8B",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
)
```

### Resources
- **Website:** https://www.siliconflow.com/
- **Models:** https://www.siliconflow.com/models

## Testing Checklist

When testing from Russia:

- [ ] Can register without VPN
- [ ] Can get API key
- [ ] API responds to requests
- [ ] Quality is acceptable
- [ ] Latency is acceptable
- [ ] Payment works (if applicable)

## Alternative: Ollama (Local)

For completely free and private AI:

```bash
# Install Ollama
# Download models
ollama pull llama3.2:1b
ollama pull phi3:latest

# Use with OpenAI-compatible API
ollama serve
```

**Pros:**
- 100% free
- No data leaves your machine
- Fast with good GPU
- No registration/payment

**Cons:**
- Requires local GPU (8GB+ VRAM recommended)
- Model quality limited by size

## Recommendations

### For Testing (Priority Order)
1. **SiliconFlow** - free, Chinese, easy to test
2. **Zhipu AI** - free, Chinese, needs verification
3. **DeepSeek** - best quality, needs Alipay

### For Production
1. **DeepSeek** - if payment is possible
2. **SiliconFlow** - if DeepSeek fails
3. **Ollama local** - if cloud fails

### For Privacy
- **Ollama local** - only option that doesn't send data

## Open Questions

- [x] Does Zhipu AI work from Russia? ✅ Yes (GLM-4, GLM-4-flash)
- [x] Does SiliconFlow work from Russia? ✅ Yes, but no balance
- [ ] Can DeepSeek be paid with crypto?
- [ ] Are there other Chinese providers?
- [x] What's the quality of Chinese summarization? ✅ Good (tested)

## Contributing

If you've tested any of these services from Russia, please contribute your findings!
