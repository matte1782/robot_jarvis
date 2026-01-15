"""
JARVIS Web Dashboard
Provides status monitoring and basic control interface.

Run: python -m src.dashboard
Access: http://localhost:5000
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

try:
    from flask import Flask, render_template, jsonify, request
except ImportError:
    print("Flask not installed. Run: pip install flask")
    sys.exit(1)

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm_router import LLMRouter
from src.memory import get_memory


app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent.parent / 'templates')
)

# Global state
router = LLMRouter()
start_time = datetime.now()


@app.route('/')
def index():
    """Serve main dashboard"""
    return render_template('index.html')


@app.route('/api/status')
def status():
    """Get system status"""
    uptime = (datetime.now() - start_time).total_seconds()

    # Check Ollama
    ollama_status = "unknown"
    try:
        import httpx
        resp = httpx.get("http://localhost:11434/api/tags", timeout=2)
        if resp.status_code == 200:
            ollama_status = "online"
        else:
            ollama_status = "error"
    except:
        ollama_status = "offline"

    return jsonify({
        "status": "running",
        "uptime_seconds": int(uptime),
        "ollama": ollama_status,
        "model": router.local_model,
        "offline_mode": router.force_offline,
        "memory_messages": len(get_memory().messages)
    })


@app.route('/api/memory')
def memory():
    """Get conversation history"""
    return jsonify({
        "messages": get_memory().get_history()
    })


@app.route('/api/memory/clear', methods=['POST'])
def clear_memory():
    """Clear conversation history"""
    get_memory().clear()
    return jsonify({"status": "cleared"})


@app.route('/api/mode', methods=['POST'])
def set_mode():
    """Toggle offline mode"""
    data = request.get_json() or {}
    offline = data.get('offline', False)
    router.force_offline = offline
    return jsonify({
        "offline_mode": router.force_offline
    })


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({"healthy": True})


def main():
    """Run dashboard server"""
    port = int(os.environ.get('JARVIS_DASHBOARD_PORT', 5000))
    debug = os.environ.get('JARVIS_DEBUG', 'false').lower() == 'true'

    print(f"JARVIS Dashboard starting on http://localhost:{port}")
    print("Press Ctrl+C to stop")

    app.run(
        host='127.0.0.1',
        port=port,
        debug=debug
    )


if __name__ == '__main__':
    main()
