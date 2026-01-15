"""
Jarvis Rate Limiter Module
Shared rate limiting for all Jarvis services

Features:
- Per-client rate limiting
- Configurable windows and limits
- Thread-safe implementation
- Memory-efficient (auto-cleanup of old entries)

Usage:
    from rate_limiter import RateLimiter

    limiter = RateLimiter(max_requests=100, window_seconds=60)

    if limiter.check("client_id"):
        # Process request
    else:
        # Return 429 Too Many Requests
"""
import threading
import logging
from datetime import datetime
from collections import defaultdict
from typing import Optional, Dict, List

logger = logging.getLogger("jarvis.rate_limiter")


# =============================================================================
# RATE LIMITER
# =============================================================================

class RateLimiter:
    """
    Thread-safe sliding window rate limiter.

    Tracks requests per client within a configurable time window.
    """

    def __init__(self, max_requests: int = 100,
                 window_seconds: int = 60,
                 cleanup_interval: int = 300):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum requests allowed per window
            window_seconds: Time window in seconds
            cleanup_interval: How often to clean up old entries (seconds)
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.cleanup_interval = cleanup_interval

        self._requests: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.RLock()
        self._last_cleanup = datetime.now().timestamp()

    def check(self, client_id: str = "default") -> bool:
        """
        Check if a request should be allowed.

        Args:
            client_id: Identifier for the client (IP, user ID, etc.)

        Returns:
            True if request is allowed, False if rate limited
        """
        now = datetime.now().timestamp()
        cutoff = now - self.window_seconds

        with self._lock:
            # Periodic cleanup
            if now - self._last_cleanup > self.cleanup_interval:
                self._cleanup(cutoff)
                self._last_cleanup = now

            # Remove old requests for this client
            self._requests[client_id] = [
                ts for ts in self._requests[client_id] if ts > cutoff
            ]

            # Check limit
            if len(self._requests[client_id]) >= self.max_requests:
                logger.warning(f"Rate limit exceeded for {client_id}")
                return False

            # Record this request
            self._requests[client_id].append(now)
            return True

    def get_remaining(self, client_id: str = "default") -> int:
        """
        Get remaining requests for a client.

        Args:
            client_id: Identifier for the client

        Returns:
            Number of remaining requests in current window
        """
        now = datetime.now().timestamp()
        cutoff = now - self.window_seconds

        with self._lock:
            # Count valid requests
            valid_requests = [
                ts for ts in self._requests[client_id] if ts > cutoff
            ]
            return max(0, self.max_requests - len(valid_requests))

    def get_reset_time(self, client_id: str = "default") -> Optional[float]:
        """
        Get time until rate limit resets.

        Args:
            client_id: Identifier for the client

        Returns:
            Seconds until reset, or None if not rate limited
        """
        now = datetime.now().timestamp()
        cutoff = now - self.window_seconds

        with self._lock:
            valid_requests = [
                ts for ts in self._requests[client_id] if ts > cutoff
            ]

            if len(valid_requests) < self.max_requests:
                return None

            # Oldest request determines reset time
            oldest = min(valid_requests)
            return max(0, (oldest + self.window_seconds) - now)

    def reset(self, client_id: str = "default"):
        """
        Reset rate limit for a client.

        Args:
            client_id: Identifier for the client
        """
        with self._lock:
            self._requests[client_id] = []
            logger.info(f"Rate limit reset for {client_id}")

    def _cleanup(self, cutoff: float):
        """
        Clean up old entries to prevent memory growth.

        Args:
            cutoff: Timestamp before which entries are removed
        """
        empty_clients = []

        for client_id, timestamps in self._requests.items():
            self._requests[client_id] = [
                ts for ts in timestamps if ts > cutoff
            ]
            if not self._requests[client_id]:
                empty_clients.append(client_id)

        # Remove empty entries
        for client_id in empty_clients:
            del self._requests[client_id]

        if empty_clients:
            logger.debug(f"Cleaned up {len(empty_clients)} inactive clients")

    def get_stats(self) -> dict:
        """
        Get rate limiter statistics.

        Returns:
            Dict with limiter stats
        """
        now = datetime.now().timestamp()
        cutoff = now - self.window_seconds

        with self._lock:
            active_clients = sum(
                1 for timestamps in self._requests.values()
                if any(ts > cutoff for ts in timestamps)
            )
            total_requests = sum(
                len([ts for ts in timestamps if ts > cutoff])
                for timestamps in self._requests.values()
            )

            return {
                "max_requests": self.max_requests,
                "window_seconds": self.window_seconds,
                "active_clients": active_clients,
                "total_requests_in_window": total_requests
            }


# =============================================================================
# PRESET CONFIGURATIONS
# =============================================================================

def create_standard_limiter() -> RateLimiter:
    """Create rate limiter with standard settings (100 req/min)"""
    return RateLimiter(max_requests=100, window_seconds=60)


def create_strict_limiter() -> RateLimiter:
    """Create rate limiter with strict settings (30 req/min)"""
    return RateLimiter(max_requests=30, window_seconds=60)


def create_relaxed_limiter() -> RateLimiter:
    """Create rate limiter with relaxed settings (500 req/min)"""
    return RateLimiter(max_requests=500, window_seconds=60)


# =============================================================================
# CLI / TESTING
# =============================================================================

def main():
    """Simple CLI for testing rate limiter"""
    import time

    print("Rate Limiter Test")
    print("-" * 40)

    # Create limiter with low threshold for testing
    limiter = RateLimiter(max_requests=5, window_seconds=10)

    print(f"Config: {limiter.max_requests} requests per {limiter.window_seconds}s")
    print()

    for i in range(8):
        allowed = limiter.check("test_client")
        remaining = limiter.get_remaining("test_client")
        reset = limiter.get_reset_time("test_client")

        status = "ALLOWED" if allowed else "BLOCKED"
        print(f"Request {i + 1}: {status} | Remaining: {remaining} | Reset in: {reset or 'N/A'}s")

        if not allowed:
            print(f"\nWaiting for reset...")
            time.sleep(reset + 0.1 if reset else 1)
            print("Retrying...")
            allowed = limiter.check("test_client")
            print(f"After wait: {'ALLOWED' if allowed else 'BLOCKED'}")

        time.sleep(0.5)

    print()
    print("Stats:", limiter.get_stats())


if __name__ == "__main__":
    main()
