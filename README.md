# 🤖 Robot Projects Repository

This repository contains the **OpenDuck Mini V3** quadruped robot project.

---

⚠️ **CRITICAL SAFETY WARNING** ⚠️

This project uses **high-capacity Li-ion batteries** that can explode, cause fires, and result in death.

**REQUIRED READING BEFORE ORDERING BATTERIES:**
📖 [Battery Safety Warnings](firmware/docs/SAFETY_WARNINGS.md)

- 🔴 18+ only
- ⚡ Electrical safety training required
- 🧯 Class D fire extinguisher required
- 👨‍🏫 Adult supervision mandatory

**Do NOT order batteries until you have read the safety guide completely.**

---

## 📦 OpenDuck Mini V3 Documentation

The primary project in this repository is **OpenDuck Mini V3**, a quadruped robot project.

| Document | Purpose |
|----------|---------|
| [Firmware Documentation](firmware/README.md) | Technical firmware details |
| [Safety Warnings](firmware/docs/SAFETY_WARNINGS.md) | **REQUIRED READING** - Battery safety |
| [Configuration Guide](firmware/CONFIG_DIRECTORIES_README.md) | Understanding config directories |
| [Contributing](CONTRIBUTING.md) | How to contribute to the project |
| [Security Policy](SECURITY.md) | Reporting vulnerabilities |
| [Day 2 Morning Briefing](firmware/MORNING_BRIEFING_DAY_02.md) | Hardware setup guide |

---

## 🗂️ Legacy Content: JARVIS Desktop Assistant

⚠️ **IMPORTANT:** The content below is **legacy documentation** for a previously planned JARVIS desktop assistant project. This project has been **moved to a separate repository** and is no longer part of the OpenDuck Mini V3 robotics project.

**Status:** The JARVIS assistant code, documentation, and planning materials below are kept for historical reference only. They are NOT maintained and NOT part of the current OpenDuck project.

**Why is this here?** This repository originally planned to include both robotics (OpenDuck) and AI assistant (JARVIS) projects under one umbrella. The projects have since been separated for better focus and maintainability.

---

### JARVIS - AI Desktop Assistant (LEGACY)

> **⚠️ ARCHIVED CONTENT - NOT ACTIVELY MAINTAINED**
>
> The information below is from the original JARVIS planning phase. For the current OpenDuck Mini V3 project, see the documentation links above.

A voice-controlled AI assistant using Claude (via MCP subscription) with local LLM fallback, holographic UI, and future robot integration.

## Quick Start

```bash
# 1. Clone and setup
# Clone this repository
git clone https://github.com/matte1782/robot_jarvis.git
cd robot_jarvis
pip install -r requirements.txt

# 2. Install Ollama + local model
winget install Ollama.Ollama
ollama pull qwen2.5:7b

# 3. Configure Claude Desktop MCP
# Copy config/claude_desktop_config.example.json to %APPDATA%\Claude\claude_desktop_config.json
# Edit paths and restart Claude Desktop

# 4. Run JARVIS
python -m src.voice_pipeline
```

## What This Is

**V1 Desktop Assistant** - Voice in, voice out, with:
- Claude Sonnet via MCP (subscription, not API)
- Ollama Qwen2.5-7B for offline/fallback
- Push-to-talk voice interface
- Secure file operations (sandboxed workspace)
- Safe shell commands (strict allowlist)
- Optional holographic UI (Pepper's Ghost pyramid)

## Documentation

| Document | Purpose |
|----------|---------|
| [Weekly Planning](Planning/Week_01/) | Day-by-day progress tracking |
| [Firmware Documentation](firmware/README.md) | Technical firmware details |
| [docs/HOLOGRAPHIC_UI.md](docs/HOLOGRAPHIC_UI.md) | Holographic display options |
| [bom/bom_totals.md](bom/bom_totals.md) | Hardware costs by tier |
| [bom/vendor_strategy.md](bom/vendor_strategy.md) | EU purchasing guide |

## Hardware Tiers

| Tier | Cost (EUR) | Capabilities |
|------|------------|--------------|
| Budget | ~325 | Voice + 7B LLM |
| Balanced | ~626 | + Pro audio, CV, hologram |
| Pro | ~1295 | + 14B LLM, NPU, UPS |

See [bom/products_eu.csv](bom/products_eu.csv) for complete parts list.

## Project Structure

```
robot_jarvis/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── config/                   # Configuration examples
│   └── claude_desktop_config.example.json
├── docs/                     # Research documents
│   ├── HOLOGRAPHIC_UI.md
│   ├── SECURITY_MODEL.md
│   ├── OFFLINE_LLM_DESIGN.md
│   └── ...
├── bom/                      # Bill of Materials
│   ├── products_eu.csv
│   ├── products_eu.json
│   ├── bom_totals.md
│   └── vendor_strategy.md
├── src/                      # Source code
│   ├── voice_pipeline.py
│   ├── llm_router.py
│   ├── auth.py
│   └── rate_limiter.py
├── mcp_servers/              # MCP server implementations
│   ├── filesystem_server.py
│   ├── shell_server.py
│   ├── notes_server.py
│   └── tasks_server.py
├── tests/                    # Test files
├── logs/                     # Log output
└── workspace/                # Sandboxed file operations
```

## Security Model

- **No admin required** - Uses pynput for hotkeys
- **Sandboxed workspace** - File ops restricted to `~/jarvis/workspace`
- **Shell allowlist** - Only safe commands permitted
- **API key hashing** - SHA-256 with constant-time comparison
- **Rate limiting** - Prevents abuse

See [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md) for threat analysis.

## Requirements

- Windows 11 (primary target)
- Python 3.11+
- Claude Desktop with active subscription
- 16GB RAM minimum (32GB for Pro tier)
- Microphone + Speakers

## License

MIT License - See [LICENSE](LICENSE)

## Roadmap

- [x] V1: Desktop voice assistant
- [ ] V2: Computer vision integration
- [ ] V3: Physical robot (Raspberry Pi Zero 2W)

---

*Built with Claude Code and lots of caffeine*
