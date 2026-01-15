# JARVIS Offline LLM Design Document
## Agent D - Offline LLM Engineer

**Version**: 1.0 | **Date**: 2026-01-10 | **Target**: Windows 11
**Hardware Tiers**: Balanced (16GB RAM) | Pro (32GB RAM + GPU)

---

## Executive Summary

This document provides a complete design for offline/local LLM capability in JARVIS, enabling operation when Claude is unavailable or for privacy-sensitive tasks. The design prioritizes:
- Consumer hardware compatibility (16-32GB RAM)
- Windows native support
- Coding assistance, summarization, and Q&A capabilities
- Italian language support

---

## 1. LLM Runners Comparison

### 1.1 Ollama (Recommended for JARVIS)

**Current Version**: Latest stable (auto-updates)
**Installation**: Native Windows installer from [ollama.com](https://ollama.com)

| Aspect | Details |
|--------|---------|
| **Setup Complexity** | Very Low - Single installer, no config needed |
| **Windows Support** | Native (Windows 10/11 64-bit) |
| **GPU Support** | Automatic NVIDIA CUDA detection, AMD ROCm |
| **API** | OpenAI-compatible endpoint at `localhost:11434` |
| **Memory Management** | Automatic model loading/unloading |
| **Model Library** | 100+ pre-quantized models |

**Performance on Windows**:
- Startup time: ~2-3 seconds (model loading)
- RTX 4060 8GB: 40-53 tokens/second (7B models)
- RTX 3060 12GB: 35-45 tokens/second (7B models)
- CPU-only (i9): 12-15 tokens/second (7B models)

**Why Ollama for JARVIS**:
1. OpenAI-compatible API enables easy Claude fallback integration
2. Zero-config GPU acceleration
3. Background service model (always ready)
4. Active development (180% YoY growth)

Sources:
- [Ollama Windows Documentation](https://docs.ollama.com/windows)
- [Ollama Hardware Guide](https://www.arsturn.com/blog/ollama-hardware-guide-what-you-need-to-run-llms-locally)

### 1.2 LM Studio

| Aspect | Details |
|--------|---------|
| **Setup Complexity** | Very Low - GUI-based |
| **Windows Support** | Native with Vulkan out-of-box |
| **Best For** | Beginners, model exploration |
| **Downsides** | 528MB installer, pre-quantized models only |

**When to use instead of Ollama**:
- First-time local LLM users wanting GUI
- Testing/comparing multiple models visually
- Vulkan GPU support needed (AMD older cards)

### 1.3 llama.cpp (Direct)

| Aspect | Details |
|--------|---------|
| **Setup Complexity** | High - Requires compilation |
| **Best For** | Maximum control, custom quantization |
| **Performance** | Slightly faster (no abstraction layer) |

**When to use instead of Ollama**:
- Custom quantization requirements
- Embedded/minimal deployments
- Advanced users needing fine-grained control

### 1.4 vLLM

**Not recommended for JARVIS local deployment**:
- Designed for production serving at scale
- Requires CUDA compute capability 7.0+
- Overkill for single-user local inference
- Better suited for cloud/server deployments

---

## 2. Model Selection by Tier

### 2.1 Balanced Tier (16GB RAM, CPU or 8GB GPU)

#### Recommended Primary Model: **Qwen2.5-7B-Instruct**

| Model | RAM Required | Tokens/sec (CPU) | Tokens/sec (GPU) | Coding | Italian |
|-------|--------------|------------------|------------------|--------|---------|
| **Qwen2.5-7B-Instruct** | 8-10GB | 10-14 t/s | 40-50 t/s | Excellent | Good |
| Llama 3.2 3B | 4-5GB | 20-25 t/s | 60-70 t/s | Good | Limited |
| Mistral 7B Instruct | 8GB | 12-15 t/s | 45-52 t/s | Very Good | Good |
| Phi-3 Mini 3.8B | 4-5GB | 25-30 t/s | 70-80 t/s | Good | Limited |

**Quantization Options**:
- **Q4_K_M** (Recommended): Best quality/size ratio, ~4GB for 7B model
- **Q5_K_M**: Higher quality, ~5GB for 7B model
- **Q8**: Near full precision, ~8GB for 7B model

**Ollama Commands**:
```bash
# Primary recommendation
ollama pull qwen2.5:7b

# For faster responses (lower quality)
ollama pull qwen2.5:3b

# Alternative for pure coding
ollama pull qwen2.5-coder:7b

# Mistral alternative
ollama pull mistral:7b-instruct-v0.3-q4_K_M
```

#### Why Qwen2.5-7B for JARVIS Balanced Tier:

1. **Multilingual Excellence**: Supports 29+ languages including Italian
2. **Coding Performance**: 88.4% HumanEval (competitive with larger models)
3. **128K Context Window**: Handles long conversations
4. **Efficient**: Runs well on 16GB system RAM with Q4 quantization

Sources:
- [Qwen2.5 Official Announcement](https://qwenlm.github.io/blog/qwen2.5/)
- [Qwen Italian Fine-tuning Guide](https://medium.com/@michymarcucci/how-i-fine-tuned-qwen2-5-0-5b-instruct-to-improve-italian-language-performance-b96acd0e0e5c)

### 2.2 Pro Tier (32GB RAM or Dedicated GPU)

#### Primary Recommendation: **Qwen2.5-Coder-32B** (with 24GB+ GPU)

| Model | VRAM Required | Tokens/sec | Coding | Italian |
|-------|---------------|------------|--------|---------|
| **Qwen2.5-Coder-32B Q4** | 20-24GB | 25-35 t/s | Exceptional | Good |
| Mixtral 8x7B Q4 | 24GB+ | 20-30 t/s | Very Good | Excellent |
| Llama 3.1 70B Q4 | 40GB+ | 10-15 t/s | Excellent | Good |
| DeepSeek-Coder-V2-Lite | 16GB | 35-45 t/s | Excellent | Limited |

**GPU-Specific Recommendations**:

| GPU VRAM | Best Model | Command |
|----------|------------|---------|
| 8GB (RTX 4060) | Qwen2.5-7B Q4 | `ollama pull qwen2.5:7b` |
| 12GB (RTX 3060/4070) | Qwen2.5-14B Q4 | `ollama pull qwen2.5:14b` |
| 16GB (RTX 4080) | Qwen2.5-Coder-14B | `ollama pull qwen2.5-coder:14b` |
| 24GB (RTX 4090) | Qwen2.5-32B Q4 | `ollama pull qwen2.5:32b` |

**Important Note on 70B Models**:
Llama 3.1 70B at Q4 requires ~42GB VRAM. With 32GB RAM/VRAM, you'll need:
- Aggressive 3-bit quantization (quality trade-off)
- CPU offloading (severe performance impact: 3-5 t/s)
- Dual GPU setup (2x 24GB)

**Recommendation**: For 32GB RAM systems, use 32B models maximum.

Sources:
- [Best LLMs for 16GB VRAM](https://localllm.in/blog/best-local-llms-16gb-vram)
- [Qwen2.5-Coder Benchmarks](https://deepgram.com/learn/best-local-coding-llm)

### 2.3 Model Comparison Table

| Model | Size | RAM Min | Best Use Case | Coding Score | Italian | Speed |
|-------|------|---------|---------------|--------------|---------|-------|
| Phi-3 Mini | 3.8B | 6GB | Quick tasks, reasoning | 7/10 | 5/10 | Fast |
| Llama 3.2 3B | 3B | 5GB | General assistant | 6/10 | 6/10 | Very Fast |
| Qwen2.5 7B | 7B | 10GB | All-around best | 8/10 | 8/10 | Medium |
| Mistral 7B | 7B | 10GB | European languages | 7/10 | 8/10 | Medium |
| Qwen2.5-Coder 7B | 7B | 10GB | Pure coding | 9/10 | 6/10 | Medium |
| Qwen2.5 14B | 14B | 16GB | Complex tasks | 9/10 | 8/10 | Slower |
| Mixtral 8x7B | 47B | 26GB | MoE reasoning | 8/10 | 9/10 | Variable |
| Qwen2.5 32B | 32B | 24GB | Near-Claude quality | 9/10 | 9/10 | Slower |

---

## 3. Routing Strategy

### 3.1 Routing Decision Matrix

| Condition | Route To | Reason |
|-----------|----------|--------|
| No internet connection | Ollama Local | Only option |
| Privacy-sensitive data | Ollama Local | Data stays local |
| Simple Q&A / chat | Ollama Local | Save Claude usage |
| Code completion (short) | Ollama Local | Low latency needed |
| Complex reasoning | Claude API | Higher quality |
| Long context (>32K tokens) | Claude API | Better context handling |
| Code review / debugging | Claude API | Better analysis |
| Multi-step planning | Claude API | Better coherence |

### 3.2 Automatic Fallback Logic

```python
# src/llm_router.py
"""
JARVIS LLM Router
Routes requests between Claude and Ollama based on task and availability
"""
import httpx
import asyncio
from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass

class RoutingDecision(Enum):
    CLAUDE = "claude"
    OLLAMA = "ollama"

@dataclass
class RouterConfig:
    claude_base_url: str = "https://api.anthropic.com"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b"
    claude_timeout: float = 30.0
    ollama_timeout: float = 60.0
    prefer_local_for_simple: bool = True
    privacy_mode: bool = False

class LLMRouter:
    def __init__(self, config: RouterConfig = None):
        self.config = config or RouterConfig()
        self._claude_available = None
        self._ollama_available = None

    async def check_ollama_health(self) -> bool:
        """Check if Ollama is running and responsive"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.config.ollama_base_url}/api/tags",
                    timeout=5.0
                )
                return response.status_code == 200
        except Exception:
            return False

    async def check_claude_health(self) -> bool:
        """Check if Claude API is reachable"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.anthropic.com/v1/health",
                    timeout=5.0
                )
                return response.status_code in [200, 401]  # 401 = reachable but needs auth
        except Exception:
            return False

    def classify_task(self, prompt: str) -> Dict[str, Any]:
        """Classify task complexity and characteristics"""
        prompt_lower = prompt.lower()

        # Simple task indicators
        simple_patterns = [
            "what is", "who is", "when was", "where is",
            "translate", "summarize briefly", "quick question",
            "time", "date", "weather", "define"
        ]

        # Complex task indicators
        complex_patterns = [
            "explain in detail", "analyze", "compare and contrast",
            "write a", "create a", "design", "implement",
            "debug", "review this code", "refactor",
            "step by step", "plan", "strategy"
        ]

        # Privacy indicators
        privacy_patterns = [
            "password", "secret", "private", "confidential",
            "personal", "medical", "financial", "sensitive"
        ]

        is_simple = any(p in prompt_lower for p in simple_patterns)
        is_complex = any(p in prompt_lower for p in complex_patterns)
        is_private = any(p in prompt_lower for p in privacy_patterns)

        # Token estimation (rough)
        estimated_tokens = len(prompt.split()) * 1.3
        needs_long_context = estimated_tokens > 4000

        return {
            "is_simple": is_simple and not is_complex,
            "is_complex": is_complex,
            "is_private": is_private,
            "needs_long_context": needs_long_context,
            "estimated_tokens": estimated_tokens
        }

    async def route(self, prompt: str, force: Optional[RoutingDecision] = None) -> RoutingDecision:
        """
        Determine which LLM to use for this request.

        Priority:
        1. Forced routing (if specified)
        2. Privacy mode -> Ollama
        3. Task classification
        4. Availability fallback
        """
        # Force override
        if force:
            return force

        # Check availability
        ollama_ok = await self.check_ollama_health()
        claude_ok = await self.check_claude_health()

        # Privacy mode always uses local
        if self.config.privacy_mode:
            if ollama_ok:
                return RoutingDecision.OLLAMA
            else:
                raise RuntimeError("Privacy mode enabled but Ollama unavailable")

        # Classify task
        task_info = self.classify_task(prompt)

        # Private data -> local only
        if task_info["is_private"]:
            if ollama_ok:
                return RoutingDecision.OLLAMA
            else:
                raise RuntimeError("Private data detected but local LLM unavailable")

        # Complex tasks prefer Claude
        if task_info["is_complex"] or task_info["needs_long_context"]:
            if claude_ok:
                return RoutingDecision.CLAUDE
            elif ollama_ok:
                return RoutingDecision.OLLAMA
            else:
                raise RuntimeError("No LLM available")

        # Simple tasks can use local
        if task_info["is_simple"] and self.config.prefer_local_for_simple:
            if ollama_ok:
                return RoutingDecision.OLLAMA
            elif claude_ok:
                return RoutingDecision.CLAUDE
            else:
                raise RuntimeError("No LLM available")

        # Default: Claude if available, else Ollama
        if claude_ok:
            return RoutingDecision.CLAUDE
        elif ollama_ok:
            return RoutingDecision.OLLAMA
        else:
            raise RuntimeError("No LLM available")

    async def call_ollama(self, prompt: str, system: str = None) -> str:
        """Call Ollama API"""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.config.ollama_base_url}/v1/chat/completions",
                json={
                    "model": self.config.ollama_model,
                    "messages": messages,
                    "stream": False
                },
                timeout=self.config.ollama_timeout
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]


# Example usage
async def main():
    router = LLMRouter()

    # Check which LLM to use
    decision = await router.route("What time is it?")
    print(f"Route to: {decision.value}")

    # Force local for privacy
    decision = await router.route(
        "My password is...",
        force=None  # Will auto-detect privacy
    )
    print(f"Private data route: {decision.value}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 3.3 Privacy-Based Routing

**Always Route to Ollama (Local)**:
- Passwords, credentials, API keys
- Personal health information
- Financial data
- Private conversations
- Proprietary business data

**Configure in JARVIS**:
```python
# Enable privacy mode (all traffic local)
router = LLMRouter(RouterConfig(privacy_mode=True))

# Or per-request
decision = await router.route(prompt, force=RoutingDecision.OLLAMA)
```

---

## 4. Integration Architecture

### 4.1 OpenAI-Compatible API

Ollama exposes an OpenAI-compatible endpoint, enabling drop-in replacement:

```python
from openai import OpenAI

# Configure for Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Required but ignored
)

# Use exactly like OpenAI
response = client.chat.completions.create(
    model="qwen2.5:7b",
    messages=[
        {"role": "system", "content": "You are JARVIS, an AI assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
print(response.choices[0].message.content)
```

### 4.2 Integration with Voice Pipeline

Update `src/voice_pipeline.py` to include LLM routing:

```python
# Add to voice_pipeline.py

from llm_router import LLMRouter, RoutingDecision, RouterConfig

class VoicePipelineWithLLM(VoicePipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.router = LLMRouter(RouterConfig(
            ollama_model="qwen2.5:7b",
            prefer_local_for_simple=True
        ))

    async def process_transcription(self, text: str) -> str:
        """Process transcribed text through LLM and return response"""

        # Determine routing
        decision = await self.router.route(text)

        if decision == RoutingDecision.OLLAMA:
            response = await self.router.call_ollama(
                prompt=text,
                system="You are JARVIS, a helpful AI assistant. Respond concisely."
            )
        else:
            # Use Claude via MCP or direct API
            response = await self.call_claude(text)

        return response

    def _process_audio(self, audio_data):
        """Override to include LLM processing"""
        text = self.stt.transcribe(audio_data)

        if text:
            print(f"\n>> {text}\n")

            # Get LLM response
            response = asyncio.run(self.process_transcription(text))

            # Speak response
            self.respond(response)
```

### 4.3 LiteLLM Proxy for Advanced Routing

For more sophisticated routing with observability, use LiteLLM:

```yaml
# litellm_config.yaml
model_list:
  - model_name: jarvis-fast
    litellm_params:
      model: ollama/qwen2.5:7b
      api_base: http://localhost:11434
    model_info:
      mode: completion

  - model_name: jarvis-smart
    litellm_params:
      model: ollama/qwen2.5:14b
      api_base: http://localhost:11434
    model_info:
      mode: completion

  - model_name: jarvis-cloud
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY
    model_info:
      mode: completion

router_settings:
  routing_strategy: latency-based-routing

litellm_settings:
  fallbacks:
    - jarvis-cloud: ["jarvis-smart", "jarvis-fast"]
  context_window_fallbacks:
    - jarvis-fast: ["jarvis-smart", "jarvis-cloud"]
  allowed_fails: 3
```

**Run LiteLLM Proxy**:
```bash
pip install litellm
litellm --config litellm_config.yaml --port 4000
```

### 4.4 Context Management for Local Models

Local models have smaller context windows. Implement context compression:

```python
# src/context_manager.py
"""
Context manager for local LLM token limits
"""
from typing import List, Dict
import tiktoken

class ContextManager:
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))

    def truncate_messages(
        self,
        messages: List[Dict[str, str]],
        reserve_for_response: int = 1000
    ) -> List[Dict[str, str]]:
        """
        Truncate conversation history to fit context window.
        Keeps system message and recent messages.
        """
        available = self.max_tokens - reserve_for_response

        # Always keep system message
        system_msg = None
        other_msgs = []

        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg
            else:
                other_msgs.append(msg)

        # Start with system message tokens
        used = self.count_tokens(system_msg["content"]) if system_msg else 0

        # Add messages from most recent, stop when limit reached
        included = []
        for msg in reversed(other_msgs):
            msg_tokens = self.count_tokens(msg["content"])
            if used + msg_tokens > available:
                break
            included.insert(0, msg)
            used += msg_tokens

        result = []
        if system_msg:
            result.append(system_msg)
        result.extend(included)

        return result

    def summarize_context(self, messages: List[Dict[str, str]]) -> str:
        """Create a summary of older messages for context"""
        older_messages = messages[:-5]  # Keep last 5 as-is

        if not older_messages:
            return ""

        summary_parts = []
        for msg in older_messages:
            role = msg["role"]
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            summary_parts.append(f"{role}: {content}")

        return "Previous conversation summary:\n" + "\n".join(summary_parts)
```

---

## 5. Performance Benchmarks

### 5.1 Tokens per Second by Hardware

| Hardware | Model | Quantization | Tokens/sec | Notes |
|----------|-------|--------------|------------|-------|
| **CPU Only (i9-12900K)** | Qwen2.5-7B | Q4_K_M | 12-15 t/s | Dual-channel RAM helps |
| **CPU Only (Ryzen 9 7900)** | Mistral-7B | Q4_K_M | 12-14 t/s | Memory bandwidth limited |
| **RTX 3060 12GB** | Qwen2.5-7B | Q4_K_M | 40-45 t/s | Sweet spot value GPU |
| **RTX 4060 8GB** | Qwen2.5-7B | Q4_K_M | 45-52 t/s | Efficient for 7B |
| **RTX 4070 12GB** | Qwen2.5-14B | Q4_K_M | 35-40 t/s | Can run 14B comfortably |
| **RTX 4080 16GB** | Qwen2.5-32B | Q4_K_M | 25-30 t/s | Near-Claude quality |
| **RTX 4090 24GB** | Qwen2.5-32B | Q4_K_M | 40-50 t/s | Premium performance |

### 5.2 Quality Comparison for Coding

| Model | HumanEval | MBPP | Aider Benchmark | Real-world Feel |
|-------|-----------|------|-----------------|-----------------|
| GPT-4o | 92.1% | 91.0% | 79.2% | Excellent |
| Claude 3.5 Sonnet | 92.0% | 90.5% | 78.5% | Excellent |
| **Qwen2.5-Coder-32B** | 90.2% | 88.5% | 75.2% | Very Good |
| Qwen2.5-Coder-7B | 88.4% | 85.2% | 70.1% | Good |
| DeepSeek-Coder-V2 | 90.2% | 87.0% | 72.3% | Good |
| Mistral-7B | 81.2% | 78.5% | 62.5% | Moderate |

### 5.3 Memory Usage

| Model | VRAM (Q4) | System RAM (Q4) | Peak Memory |
|-------|-----------|-----------------|-------------|
| Phi-3 Mini 3.8B | 3GB | 5GB | +2GB overhead |
| Llama 3.2 3B | 2.5GB | 4GB | +2GB overhead |
| Qwen2.5-7B | 5GB | 8GB | +3GB overhead |
| Mistral-7B | 5GB | 8GB | +3GB overhead |
| Qwen2.5-14B | 9GB | 14GB | +4GB overhead |
| Qwen2.5-32B | 20GB | 28GB | +6GB overhead |

### 5.4 Startup Times

| Component | Cold Start | Warm Start |
|-----------|------------|------------|
| Ollama service | 2-3 seconds | Instant |
| Model load (7B) | 3-5 seconds | 1-2 seconds |
| Model load (14B) | 5-8 seconds | 2-3 seconds |
| Model load (32B) | 10-15 seconds | 3-5 seconds |
| First token | +1-2 seconds | Instant |

---

## 6. Installation Guide: Ollama on Windows

### 6.1 Prerequisites

- Windows 10/11 64-bit
- 16GB RAM minimum (32GB recommended for larger models)
- 50GB free disk space
- (Optional) NVIDIA GPU with 8GB+ VRAM

### 6.2 Step-by-Step Installation

```powershell
# Step 1: Download Ollama
# Go to https://ollama.com/download/windows
# Or use PowerShell:
Invoke-WebRequest -Uri "https://ollama.com/download/windows" -OutFile "$env:TEMP\OllamaSetup.exe"

# Step 2: Run installer
Start-Process "$env:TEMP\OllamaSetup.exe" -Wait

# Step 3: Verify installation
ollama --version

# Step 4: Pull recommended model
ollama pull qwen2.5:7b

# Step 5: Test the model
ollama run qwen2.5:7b "Hello, I am JARVIS. Say test OK."

# Step 6: (Optional) Pull coding-specific model
ollama pull qwen2.5-coder:7b

# Step 7: Verify API is running
Invoke-RestMethod -Uri "http://localhost:11434/api/tags"
```

### 6.3 Configuration for JARVIS

```powershell
# Set model storage location (if needed)
[Environment]::SetEnvironmentVariable("OLLAMA_MODELS", "D:\OllamaModels", "User")

# Restart Ollama service
Stop-Process -Name ollama -Force -ErrorAction SilentlyContinue
Start-Process ollama -ArgumentList "serve"
```

### 6.4 GPU Optimization (NVIDIA)

```powershell
# Verify CUDA detection
ollama run qwen2.5:7b --verbose

# Check GPU usage during inference
nvidia-smi -l 1
```

### 6.5 Creating Custom JARVIS Model

```powershell
# Create Modelfile for JARVIS persona
@"
FROM qwen2.5:7b

SYSTEM You are JARVIS, an advanced AI assistant for coding and productivity. You help with:
- Code writing, review, and debugging
- File and project management
- System automation tasks
- Research and documentation

Be concise, accurate, and helpful. When writing code, always include comments.
Respond in the same language as the user's query.

PARAMETER temperature 0.7
PARAMETER num_ctx 8192
"@ | Out-File -FilePath "Modelfile" -Encoding UTF8

# Create the custom model
ollama create jarvis -f Modelfile

# Test it
ollama run jarvis "Ciao! Come posso aiutarti oggi?"
```

---

## 7. Recommended Setup Summary

### 7.1 Balanced Tier Setup (16GB RAM)

**Hardware**:
- 16GB System RAM (dual-channel preferred)
- Any modern CPU (AMD Ryzen 5/7 or Intel i5/i7)
- Optional: RTX 3060 12GB or RTX 4060 8GB

**Software Stack**:
```
Ollama (LLM Runtime)
    |
    +-- Primary: qwen2.5:7b (general + Italian)
    +-- Coding: qwen2.5-coder:7b (when needed)
    +-- Fast: phi3:mini (quick responses)
    |
JARVIS LLM Router
    |
    +-- Routes to Ollama (local) or Claude (cloud)
    +-- Privacy detection
    +-- Automatic fallback
```

**Expected Performance**:
- Response time: 3-8 seconds (CPU), 1-3 seconds (GPU)
- Quality: Good for most coding tasks, Italian support works well
- Privacy: Full local operation when needed

### 7.2 Pro Tier Setup (32GB RAM + GPU)

**Hardware**:
- 32GB System RAM
- RTX 4070/4080/4090 (12-24GB VRAM)
- Fast NVMe SSD for model storage

**Software Stack**:
```
Ollama (LLM Runtime)
    |
    +-- Primary: qwen2.5:14b or qwen2.5:32b
    +-- Coding: qwen2.5-coder:14b
    +-- Fast: qwen2.5:7b
    |
LiteLLM Proxy (Optional)
    |
    +-- Load balancing
    +-- Automatic fallbacks
    +-- Observability
    |
JARVIS LLM Router
```

**Expected Performance**:
- Response time: 1-4 seconds
- Quality: Near-Claude for most tasks
- Can handle complex coding and long context

---

## 8. Integration Checklist

### Pre-Integration
- [ ] Ollama installed and running (`ollama --version`)
- [ ] Primary model downloaded (`ollama pull qwen2.5:7b`)
- [ ] API endpoint accessible (`curl http://localhost:11434/api/tags`)
- [ ] GPU detected (if applicable)

### JARVIS Integration
- [ ] `llm_router.py` implemented
- [ ] Voice pipeline updated with LLM calls
- [ ] Context manager for token limits
- [ ] Privacy routing configured
- [ ] Fallback logic tested

### Testing
- [ ] Local-only mode works (disable network)
- [ ] Cloud fallback works (stop Ollama)
- [ ] Privacy detection routes correctly
- [ ] Italian language responses work
- [ ] Coding assistance produces valid code

---

## Sources

### Ollama
- [Ollama Windows Installation](https://localaimaster.com/blog/ollama-windows-installation)
- [Ollama Official Docs](https://docs.ollama.com/windows)
- [Ollama Hardware Guide](https://www.arsturn.com/blog/ollama-hardware-guide-what-you-need-to-run-llms-locally)

### Model Comparisons
- [Local LLM Benchmarks 2025](https://www.practicalwebtools.com/blog/local-llm-benchmarks-consumer-hardware-guide-2025)
- [Best LLMs for 16GB VRAM](https://localllm.in/blog/best-local-llms-16gb-vram)
- [Qwen2.5-Coder vs DeepSeek](https://deepgram.com/learn/best-local-coding-llm)

### Routing and Integration
- [LiteLLM Routing Documentation](https://docs.litellm.ai/docs/routing)
- [Ollama OpenAI Compatibility](https://ollama.com/blog/openai-compatibility)
- [LLM Model Routing Guide](https://medium.com/@michael.hannecke/implementing-llm-model-routing-a-practical-guide-with-ollama-and-litellm-b62c1562f50f)

### Performance Benchmarks
- [GPU Benchmark RTX 4060](https://www.databasemart.com/blog/ollama-gpu-benchmark-rtx4060)
- [RTX 3060 Ti LLM Performance](https://www.databasemart.com/blog/ollama-gpu-benchmark-rtx3060ti)
- [CPU vs GPU Performance Analysis](https://markaicode.com/ollama-cpu-vs-gpu-performance-benchmark-2025/)

### Qwen2.5 and Italian
- [Qwen2.5 Official Blog](https://qwenlm.github.io/blog/qwen2.5/)
- [Qwen2.5 Italian Fine-tuning](https://medium.com/@michymarcucci/how-i-fine-tuned-qwen2-5-0-5b-instruct-to-improve-italian-language-performance-b96acd0e0e5c)
- [Qwen on Ollama](https://ollama.com/library/qwen2.5)

---

**Document Version**: 1.0
**Last Updated**: 2026-01-10
**Author**: Agent D - Offline LLM Engineer
