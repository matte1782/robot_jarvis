"""
JARVIS LLM Router
Routes requests between Claude (cloud) and Ollama (local) based on task and availability.

Features:
- Automatic provider detection and health checks
- Task-based routing (simple->local, complex->cloud)
- Privacy-based routing (sensitive data->local only)
- Fallback handling when primary is unavailable
- OpenAI-compatible API for both providers

Usage:
    router = LLMRouter()
    response = await router.complete("Write a Python function to sort a list")

Configuration:
    Set environment variables:
    - OLLAMA_BASE_URL: Ollama API URL (default: http://localhost:11434)
    - OLLAMA_MODEL: Default Ollama model (default: qwen2.5:7b)
    - ANTHROPIC_API_KEY: Claude API key (for cloud routing)
"""
import os
import asyncio
import time
from enum import Enum
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import logging

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    print("WARNING: httpx not installed. Install with: pip install httpx")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jarvis.router")


class RoutingDecision(Enum):
    """Where to route the LLM request"""
    CLAUDE = "claude"
    OLLAMA = "ollama"


class TaskComplexity(Enum):
    """Estimated task complexity"""
    SIMPLE = "simple"       # Quick Q&A, translations
    MODERATE = "moderate"   # Code completion, summarization
    COMPLEX = "complex"     # Multi-step reasoning, debugging


@dataclass
class RouterConfig:
    """Configuration for the LLM router"""
    # Ollama settings
    ollama_base_url: str = field(
        default_factory=lambda: os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    )
    ollama_model: str = field(
        default_factory=lambda: os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
    )
    ollama_timeout: float = 120.0

    # Claude settings
    claude_base_url: str = "https://api.anthropic.com"
    claude_model: str = "claude-3-5-sonnet-20241022"
    claude_timeout: float = 60.0
    claude_api_key: str = field(
        default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY", "")
    )

    # Routing preferences
    prefer_local_for_simple: bool = True
    privacy_mode: bool = False  # When True, always use local

    # Health check settings
    health_check_interval: float = 30.0  # Seconds between health checks


@dataclass
class RouterStats:
    """Statistics for monitoring"""
    ollama_requests: int = 0
    claude_requests: int = 0
    ollama_failures: int = 0
    claude_failures: int = 0
    total_tokens_local: int = 0
    total_tokens_cloud: int = 0


class LLMRouter:
    """
    Intelligent router for JARVIS LLM requests.

    Routes between Ollama (local) and Claude (cloud) based on:
    - Task complexity
    - Privacy requirements
    - Provider availability
    """

    # Task classification patterns
    SIMPLE_PATTERNS = [
        "what is", "who is", "when was", "where is", "how many",
        "translate", "define", "meaning of",
        "time", "date", "weather",
        "yes or no", "true or false",
        "list the", "name the",
    ]

    COMPLEX_PATTERNS = [
        "explain in detail", "analyze", "compare and contrast",
        "write a complete", "create a", "design", "implement",
        "debug", "review this code", "refactor", "optimize",
        "step by step", "plan", "strategy", "architecture",
        "why does", "how would you", "what if",
        "multi-step", "comprehensive",
    ]

    PRIVACY_PATTERNS = [
        "password", "secret", "private", "confidential",
        "personal", "medical", "financial", "sensitive",
        "api key", "token", "credential", "login",
        "social security", "credit card", "bank",
    ]

    CODING_PATTERNS = [
        "function", "class", "method", "variable",
        "python", "javascript", "typescript", "rust", "go",
        "code", "script", "program", "algorithm",
        "bug", "error", "exception", "fix",
        "import", "export", "async", "await",
    ]

    def __init__(self, config: RouterConfig = None):
        if not HTTPX_AVAILABLE:
            raise ImportError("httpx is required. Install with: pip install httpx")

        self.config = config or RouterConfig()
        self.stats = RouterStats()

        # Cache health status
        self._ollama_healthy: Optional[bool] = None
        self._claude_healthy: Optional[bool] = None
        self._last_health_check: float = 0

        logger.info(f"LLMRouter initialized")
        logger.info(f"  Ollama: {self.config.ollama_base_url} (model: {self.config.ollama_model})")
        logger.info(f"  Privacy mode: {self.config.privacy_mode}")

    async def check_ollama_health(self, force: bool = False) -> bool:
        """Check if Ollama is running and responsive"""
        now = time.time()
        if not force and self._ollama_healthy is not None:
            if now - self._last_health_check < self.config.health_check_interval:
                return self._ollama_healthy

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.config.ollama_base_url}/api/tags",
                    timeout=5.0
                )
                self._ollama_healthy = response.status_code == 200
                self._last_health_check = now

                if self._ollama_healthy:
                    # Check if our model is available
                    data = response.json()
                    models = [m.get("name", "") for m in data.get("models", [])]
                    if not any(self.config.ollama_model in m for m in models):
                        logger.warning(f"Model {self.config.ollama_model} not found in Ollama")

        except Exception as e:
            logger.debug(f"Ollama health check failed: {e}")
            self._ollama_healthy = False

        return self._ollama_healthy

    async def check_claude_health(self, force: bool = False) -> bool:
        """Check if Claude API is reachable"""
        now = time.time()
        if not force and self._claude_healthy is not None:
            if now - self._last_health_check < self.config.health_check_interval:
                return self._claude_healthy

        if not self.config.claude_api_key:
            self._claude_healthy = False
            return False

        try:
            async with httpx.AsyncClient() as client:
                # Simple connectivity check
                response = await client.get(
                    "https://api.anthropic.com",
                    timeout=5.0
                )
                # Any response (including 401) means reachable
                self._claude_healthy = True
                self._last_health_check = now
        except Exception as e:
            logger.debug(f"Claude health check failed: {e}")
            self._claude_healthy = False

        return self._claude_healthy

    def classify_task(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze the prompt to determine task characteristics.

        Returns:
            Dict with keys: complexity, is_private, is_coding, estimated_tokens
        """
        prompt_lower = prompt.lower()

        # Check patterns
        is_simple = any(p in prompt_lower for p in self.SIMPLE_PATTERNS)
        is_complex = any(p in prompt_lower for p in self.COMPLEX_PATTERNS)
        is_private = any(p in prompt_lower for p in self.PRIVACY_PATTERNS)
        is_coding = any(p in prompt_lower for p in self.CODING_PATTERNS)

        # Determine complexity
        if is_complex or (is_coding and len(prompt) > 500):
            complexity = TaskComplexity.COMPLEX
        elif is_simple and not is_complex:
            complexity = TaskComplexity.SIMPLE
        else:
            complexity = TaskComplexity.MODERATE

        # Estimate tokens (rough approximation)
        estimated_tokens = int(len(prompt.split()) * 1.3)

        return {
            "complexity": complexity,
            "is_private": is_private,
            "is_coding": is_coding,
            "estimated_tokens": estimated_tokens,
            "needs_long_context": estimated_tokens > 4000,
        }

    async def route(
        self,
        prompt: str,
        force: Optional[RoutingDecision] = None
    ) -> RoutingDecision:
        """
        Determine which LLM to use for this request.

        Priority:
        1. Forced routing (if specified)
        2. Privacy mode -> Ollama
        3. Private data detected -> Ollama
        4. Task classification
        5. Availability fallback

        Args:
            prompt: The user's prompt
            force: Force a specific routing decision

        Returns:
            RoutingDecision indicating which provider to use

        Raises:
            RuntimeError: If no LLM is available
        """
        # Force override
        if force:
            logger.info(f"Routing forced to: {force.value}")
            return force

        # Check availability
        ollama_ok = await self.check_ollama_health()
        claude_ok = await self.check_claude_health()

        logger.debug(f"Provider status - Ollama: {ollama_ok}, Claude: {claude_ok}")

        # Privacy mode always uses local
        if self.config.privacy_mode:
            if ollama_ok:
                logger.info("Privacy mode: routing to Ollama")
                return RoutingDecision.OLLAMA
            else:
                raise RuntimeError("Privacy mode enabled but Ollama unavailable")

        # Classify task
        task_info = self.classify_task(prompt)
        logger.debug(f"Task classification: {task_info}")

        # Private data -> local only
        if task_info["is_private"]:
            if ollama_ok:
                logger.info("Private data detected: routing to Ollama")
                return RoutingDecision.OLLAMA
            else:
                raise RuntimeError("Private data detected but local LLM unavailable")

        # Complex tasks prefer Claude
        if task_info["complexity"] == TaskComplexity.COMPLEX:
            if claude_ok:
                logger.info("Complex task: routing to Claude")
                return RoutingDecision.CLAUDE
            elif ollama_ok:
                logger.info("Complex task but Claude unavailable: falling back to Ollama")
                return RoutingDecision.OLLAMA

        # Simple tasks can use local
        if task_info["complexity"] == TaskComplexity.SIMPLE:
            if self.config.prefer_local_for_simple and ollama_ok:
                logger.info("Simple task: routing to Ollama (local preference)")
                return RoutingDecision.OLLAMA
            elif claude_ok:
                return RoutingDecision.CLAUDE
            elif ollama_ok:
                return RoutingDecision.OLLAMA

        # Moderate tasks: prefer local for coding, cloud for general
        if task_info["is_coding"] and ollama_ok:
            logger.info("Coding task: routing to Ollama")
            return RoutingDecision.OLLAMA

        # Default: Claude if available, else Ollama
        if claude_ok:
            return RoutingDecision.CLAUDE
        elif ollama_ok:
            return RoutingDecision.OLLAMA
        else:
            raise RuntimeError("No LLM provider available")

    async def call_ollama(
        self,
        prompt: str,
        system: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """
        Call Ollama API using OpenAI-compatible endpoint.

        Args:
            prompt: User prompt (used if messages not provided)
            system: System prompt
            messages: Full message list (overrides prompt/system)
            temperature: Sampling temperature
            max_tokens: Maximum response tokens

        Returns:
            Generated text response
        """
        if messages is None:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.config.ollama_base_url}/v1/chat/completions",
                    json={
                        "model": self.config.ollama_model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "stream": False,
                    },
                    timeout=self.config.ollama_timeout
                )
                response.raise_for_status()
                data = response.json()

                self.stats.ollama_requests += 1

                # Extract usage if available
                if "usage" in data:
                    self.stats.total_tokens_local += data["usage"].get("total_tokens", 0)

                return data["choices"][0]["message"]["content"]

        except httpx.TimeoutException:
            self.stats.ollama_failures += 1
            raise RuntimeError(f"Ollama request timed out after {self.config.ollama_timeout}s")
        except Exception as e:
            self.stats.ollama_failures += 1
            raise RuntimeError(f"Ollama request failed: {e}")

    async def call_claude(
        self,
        prompt: str,
        system: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """
        Call Claude API.

        Note: For full JARVIS integration, Claude is accessed via MCP.
        This is a fallback for direct API calls.
        """
        if not self.config.claude_api_key:
            raise RuntimeError("Claude API key not configured")

        if messages is None:
            messages = [{"role": "user", "content": prompt}]

        try:
            async with httpx.AsyncClient() as client:
                request_body = {
                    "model": self.config.claude_model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }

                if system:
                    request_body["system"] = system

                response = await client.post(
                    f"{self.config.claude_base_url}/v1/messages",
                    headers={
                        "x-api-key": self.config.claude_api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json=request_body,
                    timeout=self.config.claude_timeout
                )
                response.raise_for_status()
                data = response.json()

                self.stats.claude_requests += 1

                # Extract usage
                if "usage" in data:
                    self.stats.total_tokens_cloud += (
                        data["usage"].get("input_tokens", 0) +
                        data["usage"].get("output_tokens", 0)
                    )

                # Extract text from content blocks
                content = data.get("content", [])
                text_parts = [c["text"] for c in content if c["type"] == "text"]
                return "\n".join(text_parts)

        except httpx.TimeoutException:
            self.stats.claude_failures += 1
            raise RuntimeError(f"Claude request timed out after {self.config.claude_timeout}s")
        except Exception as e:
            self.stats.claude_failures += 1
            raise RuntimeError(f"Claude request failed: {e}")

    async def complete(
        self,
        prompt: str,
        system: Optional[str] = None,
        force_provider: Optional[RoutingDecision] = None,
        **kwargs
    ) -> str:
        """
        Main entry point: Route and complete a request.

        Args:
            prompt: The user's prompt
            system: System prompt
            force_provider: Force a specific provider
            **kwargs: Additional arguments passed to the LLM call

        Returns:
            Generated text response
        """
        # Default JARVIS system prompt
        if system is None:
            system = (
                "You are JARVIS, an advanced AI assistant. "
                "Be helpful, accurate, and concise. "
                "For code, include comments and follow best practices."
            )

        # Determine routing
        decision = await self.route(prompt, force=force_provider)

        # Execute request
        if decision == RoutingDecision.OLLAMA:
            return await self.call_ollama(prompt, system=system, **kwargs)
        else:
            return await self.call_claude(prompt, system=system, **kwargs)

    def get_stats(self) -> Dict[str, Any]:
        """Get router statistics"""
        return {
            "ollama_requests": self.stats.ollama_requests,
            "claude_requests": self.stats.claude_requests,
            "ollama_failures": self.stats.ollama_failures,
            "claude_failures": self.stats.claude_failures,
            "total_tokens_local": self.stats.total_tokens_local,
            "total_tokens_cloud": self.stats.total_tokens_cloud,
            "ollama_healthy": self._ollama_healthy,
            "claude_healthy": self._claude_healthy,
        }


# =============================================================================
# CLI for testing
# =============================================================================

async def main():
    """Test the router"""
    print("=" * 50)
    print("JARVIS LLM Router Test")
    print("=" * 50)

    router = LLMRouter()

    # Check health
    print("\nChecking provider health...")
    ollama_ok = await router.check_ollama_health(force=True)
    claude_ok = await router.check_claude_health(force=True)
    print(f"  Ollama: {'OK' if ollama_ok else 'UNAVAILABLE'}")
    print(f"  Claude: {'OK' if claude_ok else 'UNAVAILABLE'}")

    # Test routing decisions
    test_prompts = [
        ("What is the capital of Italy?", "Simple question"),
        ("Debug this code and explain the fix in detail", "Complex task"),
        ("My password is secret123", "Privacy sensitive"),
        ("Write a Python function to sort a list", "Coding task"),
    ]

    print("\nRouting decisions:")
    for prompt, desc in test_prompts:
        try:
            decision = await router.route(prompt)
            print(f"  [{desc}] -> {decision.value}")
        except RuntimeError as e:
            print(f"  [{desc}] -> ERROR: {e}")

    # Test actual completion (if Ollama available)
    if ollama_ok:
        print("\nTesting Ollama completion...")
        try:
            response = await router.complete(
                "Say 'JARVIS online' and nothing else.",
                force_provider=RoutingDecision.OLLAMA
            )
            print(f"  Response: {response[:100]}...")
        except Exception as e:
            print(f"  ERROR: {e}")

    # Show stats
    print("\nRouter stats:", router.get_stats())


if __name__ == "__main__":
    asyncio.run(main())
