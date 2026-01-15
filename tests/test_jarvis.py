"""
JARVIS Test Suite - Basic Smoke Tests
Run with: pytest tests/ -v
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestImports:
    """Verify all modules can be imported"""

    def test_import_auth(self):
        """Test auth module imports"""
        from src import auth
        assert hasattr(auth, 'hash_api_key')

    def test_import_rate_limiter(self):
        """Test rate_limiter module imports"""
        from src import rate_limiter
        assert hasattr(rate_limiter, 'RateLimiter')

    def test_import_llm_router(self):
        """Test llm_router module imports"""
        from src import llm_router
        assert hasattr(llm_router, 'LLMRouter')


class TestAuth:
    """Test authentication functions"""

    def test_hash_api_key_deterministic(self):
        """Same input produces same hash"""
        from src.auth import hash_api_key
        key = "test-key-12345"
        hash1 = hash_api_key(key)
        hash2 = hash_api_key(key)
        assert hash1 == hash2

    def test_hash_api_key_different_inputs(self):
        """Different inputs produce different hashes"""
        from src.auth import hash_api_key
        hash1 = hash_api_key("key1")
        hash2 = hash_api_key("key2")
        assert hash1 != hash2

    def test_hash_length(self):
        """Hash is SHA-256 (64 hex chars)"""
        from src.auth import hash_api_key
        h = hash_api_key("test")
        assert len(h) == 64


class TestRateLimiter:
    """Test rate limiting functionality"""

    def test_rate_limiter_allows_requests(self):
        """Rate limiter allows requests under limit"""
        from src.rate_limiter import RateLimiter
        limiter = RateLimiter(requests_per_minute=10)
        assert limiter.is_allowed("test-client") == True

    def test_rate_limiter_blocks_excess(self):
        """Rate limiter blocks after exceeding limit"""
        from src.rate_limiter import RateLimiter
        limiter = RateLimiter(requests_per_minute=2)
        limiter.is_allowed("test-client")
        limiter.is_allowed("test-client")
        # Third request should be blocked
        assert limiter.is_allowed("test-client") == False


class TestLLMRouter:
    """Test LLM routing logic"""

    def test_router_initialization(self):
        """Router initializes with default model"""
        from src.llm_router import LLMRouter
        router = LLMRouter()
        assert router.local_model == "qwen2.5:7b"

    def test_router_offline_mode(self):
        """Router can be set to offline mode"""
        from src.llm_router import LLMRouter
        router = LLMRouter()
        router.force_offline = True
        assert router.force_offline == True


class TestMemory:
    """Test conversation memory"""

    def test_memory_import(self):
        """Memory module imports"""
        from src import memory
        assert hasattr(memory, 'ConversationMemory')

    def test_memory_add_retrieve(self):
        """Can add and retrieve messages"""
        from src.memory import ConversationMemory
        mem = ConversationMemory(max_messages=10)
        mem.add("user", "Hello")
        mem.add("assistant", "Hi there!")
        history = mem.get_history()
        assert len(history) == 2


class TestAudit:
    """Test audit logging"""

    def test_audit_import(self):
        """Audit module imports"""
        from src import audit
        assert hasattr(audit, 'AuditLogger')


# Integration test placeholder
class TestIntegration:
    """Integration tests (require running services)"""

    @pytest.mark.skip(reason="Requires Ollama running")
    def test_ollama_connection(self):
        """Test Ollama connectivity"""
        pass

    @pytest.mark.skip(reason="Requires microphone")
    def test_voice_pipeline(self):
        """Test voice pipeline"""
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
