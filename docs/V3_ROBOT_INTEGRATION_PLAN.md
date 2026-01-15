# JARVIS V3: Robot Integration Plan
## Open Duck Mini as Peripheral Client

**Version**: 1.0 | **Date**: 2025-01-10 | **Status**: Planning (Future V3)
**Author**: Agent G - Robot Integration Planner

---

## Executive Summary

This document outlines the integration architecture for connecting a physical robot (Open Duck Mini or alternatives) to JARVIS Core as a "dumb terminal" peripheral. The robot handles I/O (mic, speaker, camera, LEDs, motion) while all processing occurs on the JARVIS Core server over Wi-Fi.

**Key Decisions:**
- Protocol: WebSocket with JSON messages (primary) + binary audio streaming
- Privacy: Push-to-talk default, LED indicators, camera on-demand only
- Architecture: Plugin-based device abstraction layer for multiple robot types
- Estimated Cost: EUR 350-550 (self-build) or EUR 300-400 (kit)
- Build Time: 2-4 weeks for experienced maker

---

## 1. Open Duck Mini Assessment

### 1.1 Project Status (January 2025)

| Aspect | Status | Notes |
|--------|--------|-------|
| Mechanical Design | Finalized | V2 design stable, minimal changes expected |
| Locomotion | Working | Sim2real RL policies demonstrated walking |
| Expression Features | Planned | LEDs, camera, mic, speaker NOT yet implemented |
| Documentation | Incomplete | Assembly guide partial, BOM available |
| Community | Active | Discord server, HuggingFace sponsorship |

**Source**: [GitHub - Open Duck Mini](https://github.com/apirrone/Open_Duck_Mini)

### 1.2 Hardware Specifications

| Component | Specification | Notes |
|-----------|---------------|-------|
| Height | ~42 cm (legs extended) | Desktop-friendly size |
| Compute | Raspberry Pi Zero 2W | Sufficient for I/O, not for AI |
| Servos | 14x Feetech servos | High-torque hobby servos |
| IMU | BNO055 | Absolute orientation sensor |
| Power | LiPo 2S battery | Rechargeable |
| **Planned I/O** | | |
| Microphone | I2S (INMP441) | To be added |
| Speaker | I2S DAC (MAX98357) | To be added |
| Camera | OV5647 / Pi Camera | To be added |
| LEDs | WS2812B (NeoPixel) | For eye expressions |

### 1.3 Bill of Materials (EU Pricing)

| Category | Components | Est. Cost EUR | EU Source |
|----------|------------|---------------|-----------|
| **Mechanical** | 3D printed parts | 20-50 | Self-print or 3D printing service |
| **Electronics Core** | Pi Zero 2W, IMU BNO055, PCB | 60-80 | Melopero, Amazon.it |
| **Servos** | 14x Feetech/MG90S servos | 35-70 | Amazon.it, AliExpress |
| **Audio** | INMP441 mic + MAX98357 amp + speaker | 15-25 | Amazon.it |
| **Vision** | OV5647 camera module | 10-25 | Melopero, Amazon.it |
| **LEDs** | WS2812B strip/ring (10 LEDs) | 8-12 | Amazon.it |
| **Power** | LiPo 2S 1000mAh + charger | 15-25 | Amazon.it |
| **Misc** | Wiring, connectors, screws | 20-30 | Local hardware |
| **TOTAL** | | **EUR 183-317** | Self-build |

**Pre-assembled kit** (when available): ~EUR 300-400 from [AIFITLAB](https://aifitlab.com/products/openduckmini-open-source-version-of-the-bdx-droid)

### 1.4 Build Difficulty Assessment

| Factor | Rating | Details |
|--------|--------|---------|
| 3D Printing | Medium | Requires calibrated printer, ~20+ hours print time |
| Electronics Assembly | Medium | Soldering required for audio/LED connections |
| Servo Calibration | High | Each servo needs individual tuning via BAM tool |
| Software Setup | Medium-High | Linux, Python, RL policy deployment |
| Walking Tuning | High | Sim2real transfer may need environment-specific tuning |
| **Overall** | **Medium-High** | 2-4 weeks for experienced maker |

### 1.5 Feasibility for JARVIS V3

| Requirement | Open Duck Mini | Assessment |
|-------------|----------------|------------|
| Audio I/O | Planned (not built-in) | Need to add components |
| Camera | Planned (not built-in) | Need to add module |
| WiFi connectivity | Yes (Pi Zero 2W) | Native support |
| Expressive indicators | Planned (LED eyes) | Need to add WS2812B |
| Motion/gestures | Yes (14 DOF) | RL policies available |
| Always-on operation | Partial | Battery life ~1-2 hours |
| Quiet operation | Good | Servos quiet at idle |

**Verdict**: Feasible but requires additional hardware integration work for I/O features.

---

## 2. Communication Protocol Specification

### 2.1 Protocol Selection

| Protocol | Pros | Cons | Use Case |
|----------|------|------|----------|
| **WebSocket** | Bi-directional, browser-native, low overhead | Requires persistent connection | Primary protocol |
| MQTT | Pub/sub, QoS levels, IoT standard | Requires broker, more complex | Alternative for multi-robot |
| gRPC | High performance, typed schemas | Overkill for simple I/O, complex setup | Not recommended |

**Recommendation**: WebSocket with JSON messages for commands, binary streaming for audio.

**Sources**:
- [WebSockets vs gRPC comparison](https://ably.com/topic/grpc-vs-websocket)
- [MQTT vs WebSocket for IoT](https://www.emqx.com/en/blog/mqtt-vs-websocket)

### 2.2 Connection Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        JARVIS CORE                               │
│                    (Mini-PC / Main PC)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐    ┌────────────────┐    ┌───────────────┐  │
│  │   LLM Router   │    │   STT Engine   │    │  TTS Engine   │  │
│  │ (Claude/Ollama)│    │(faster-whisper)│    │  (edge-tts)   │  │
│  └───────┬────────┘    └───────┬────────┘    └───────┬───────┘  │
│          │                     │                     │          │
│          └─────────────────────┼─────────────────────┘          │
│                                │                                │
│                    ┌───────────┴───────────┐                    │
│                    │     Robot Bridge      │                    │
│                    │    (WebSocket Hub)    │                    │
│                    │      Port: 8766       │                    │
│                    └───────────┬───────────┘                    │
│                                │                                │
└────────────────────────────────┼────────────────────────────────┘
                                 │
                     WiFi (LAN)  │  WebSocket + Audio Stream
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ROBOT CLIENT                                │
│                  (Open Duck Mini / Alternative)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │   MIC    │  │ SPEAKER  │  │  CAMERA  │  │   LEDs   │        │
│  │  I2S     │  │  I2S     │  │  CSI     │  │ WS2812B  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │             │               │
│       ▼             ▼             ▼             ▼               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                Robot Client Daemon (Python)               │   │
│  │                                                           │   │
│  │  - WebSocket client to JARVIS Core                       │   │
│  │  - Audio capture (I2S → PCM → stream)                    │   │
│  │  - Audio playback (stream → PCM → I2S)                   │   │
│  │  - Camera capture (on-demand JPEG)                       │   │
│  │  - LED control (patterns via PWM)                        │   │
│  │  - Motion control (RL policy inference)                  │   │
│  │  - PTT button handling                                    │   │
│  │  - Status reporting (battery, temp, IMU)                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Latency Requirements

| Operation | Target Latency | Critical | Notes |
|-----------|----------------|----------|-------|
| PTT → Recording start | < 50ms | Yes | Immediate feedback required |
| Audio streaming (mic) | < 100ms chunks | Yes | Real-time feel |
| STT processing | < 1000ms | No | User expects some delay |
| LLM response | < 3000ms | No | Conversational acceptable |
| TTS + playback start | < 500ms | Yes | Responsiveness perception |
| LED state change | < 100ms | Yes | Visual feedback timing |
| Camera frame capture | < 200ms | No | On-demand only |

### 2.4 Reconnection Handling

```python
RECONNECTION_STRATEGY = {
    "initial_delay_ms": 1000,
    "max_delay_ms": 30000,
    "backoff_multiplier": 2.0,
    "max_retries": None,  # Infinite retries
    "heartbeat_interval_ms": 5000,
    "heartbeat_timeout_ms": 15000,
}

# Robot behavior during disconnection:
# 1. LED pattern: slow pulsing amber (disconnected state)
# 2. PTT button: LED flash red (cannot connect)
# 3. Speaker: optional "Connection lost" announcement
# 4. Motion: safe idle pose, no autonomous movement
```

---

## 3. Message Schema Definitions

### 3.1 Transport Layer

```
WebSocket Connection:
  URL: ws://jarvis-core.local:8766/robot
  Subprotocol: jarvis-robot-v1

Binary Audio Channel (separate or multiplexed):
  Format: Raw PCM, 16kHz, 16-bit, mono
  Chunk size: 1600 bytes (100ms @ 16kHz)
```

### 3.2 Message Envelope

```json
{
  "v": 1,
  "id": "uuid-message-id",
  "ts": 1704931200000,
  "type": "command|event|response|stream",
  "payload": { ... }
}
```

### 3.3 Commands (JARVIS Core → Robot)

#### 3.3.1 say(text) - TTS Playback

```json
// Option A: Pre-rendered audio (preferred for low-latency robot)
{
  "type": "command",
  "payload": {
    "cmd": "say",
    "audio": {
      "format": "pcm_16k_16bit_mono",
      "data": "<base64-encoded-pcm>",
      "duration_ms": 2500
    },
    "interrupt": false
  }
}

// Option B: Stream audio chunks (for long responses)
{
  "type": "stream",
  "payload": {
    "stream_id": "tts-12345",
    "cmd": "say_stream",
    "chunk_index": 0,
    "chunk_data": "<base64-encoded-pcm>",
    "is_final": false
  }
}
```

#### 3.3.2 animate(animation_name) - Robot Movement

```json
{
  "type": "command",
  "payload": {
    "cmd": "animate",
    "animation": "wave",  // predefined animation name
    "params": {
      "speed": 1.0,       // 0.5 = half speed, 2.0 = double speed
      "intensity": 0.8    // 0.0-1.0 amplitude multiplier
    },
    "blocking": false     // true = wait for completion before next cmd
  }
}

// Predefined animations (robot implements):
// - "wave": arm wave greeting
// - "nod": head nod (yes)
// - "shake": head shake (no)
// - "think": looking up/around thinking pose
// - "happy": excited bounce/wiggle
// - "sad": slump posture
// - "attention": stand tall, focus forward
// - "idle": subtle breathing/swaying
// - "dance_01", "dance_02": fun dance moves
```

#### 3.3.3 led(pattern) - LED Control

```json
{
  "type": "command",
  "payload": {
    "cmd": "led",
    "pattern": "listening",
    "params": {
      "color": "#00FF88",     // optional override
      "brightness": 0.8,      // 0.0-1.0
      "speed": 1.0            // animation speed
    },
    "duration_ms": 0          // 0 = until next command
  }
}

// Predefined LED patterns:
// - "off": all LEDs off
// - "idle": slow breathing, soft blue
// - "listening": pulsing green (PTT active)
// - "thinking": rotating/chasing cyan
// - "speaking": audio-reactive, voice color
// - "error": red flash
// - "disconnected": slow amber pulse
// - "happy": rainbow sparkle
// - "attention": steady white
```

#### 3.3.4 status() - Get Robot State

```json
// Request
{
  "type": "command",
  "payload": {
    "cmd": "status",
    "include": ["battery", "temperature", "imu", "network", "audio"]
  }
}

// Response
{
  "type": "response",
  "payload": {
    "cmd": "status",
    "data": {
      "battery": {
        "percent": 85,
        "voltage": 7.8,
        "charging": false,
        "time_remaining_min": 45
      },
      "temperature": {
        "cpu_celsius": 52,
        "ambient_celsius": 24
      },
      "imu": {
        "orientation": {"roll": 0.5, "pitch": -2.1, "yaw": 180.3},
        "accel": [0.02, 0.01, 9.81],
        "stable": true
      },
      "network": {
        "wifi_ssid": "HomeNetwork",
        "signal_dbm": -45,
        "latency_ms": 12
      },
      "audio": {
        "mic_active": false,
        "speaker_active": false,
        "volume": 0.7
      },
      "uptime_seconds": 3600,
      "firmware_version": "1.2.0"
    }
  }
}
```

#### 3.3.5 capture_frame() - Camera Snapshot

```json
// Request
{
  "type": "command",
  "payload": {
    "cmd": "capture_frame",
    "params": {
      "resolution": "640x480",  // or "1280x720", "320x240"
      "format": "jpeg",
      "quality": 80             // JPEG quality 1-100
    }
  }
}

// Response
{
  "type": "response",
  "payload": {
    "cmd": "capture_frame",
    "data": {
      "format": "jpeg",
      "width": 640,
      "height": 480,
      "timestamp": 1704931200000,
      "image": "<base64-encoded-jpeg>"
    }
  }
}
```

#### 3.3.6 stream_audio() - Microphone Input Control

```json
// Start streaming
{
  "type": "command",
  "payload": {
    "cmd": "stream_audio",
    "action": "start",
    "params": {
      "sample_rate": 16000,
      "format": "pcm_16bit_mono",
      "chunk_ms": 100,
      "vad_enabled": true       // voice activity detection
    }
  }
}

// Audio data from robot (Robot → JARVIS)
{
  "type": "stream",
  "payload": {
    "stream_id": "mic-session-001",
    "chunk_index": 42,
    "audio_data": "<base64-encoded-pcm>",
    "vad_speech": true,         // VAD detected speech
    "rms_db": -24.5             // audio level
  }
}

// Stop streaming
{
  "type": "command",
  "payload": {
    "cmd": "stream_audio",
    "action": "stop"
  }
}
```

### 3.4 Events (Robot → JARVIS Core)

#### 3.4.1 Button Events

```json
{
  "type": "event",
  "payload": {
    "event": "button",
    "button": "ptt",          // "ptt", "action", "power"
    "action": "pressed",      // "pressed", "released", "long_press"
    "timestamp": 1704931200000
  }
}
```

#### 3.4.2 Motion Events

```json
{
  "type": "event",
  "payload": {
    "event": "motion",
    "detail": "fall_detected", // or "pickup", "shake", "tap"
    "imu_data": {
      "accel": [0.5, 2.3, -8.1],
      "gyro": [45.2, -12.3, 5.6]
    }
  }
}
```

#### 3.4.3 Status Change Events

```json
{
  "type": "event",
  "payload": {
    "event": "status_change",
    "field": "battery",
    "old_value": 20,
    "new_value": 15,
    "warning": "low_battery"
  }
}
```

### 3.5 Error Responses

```json
{
  "type": "response",
  "payload": {
    "cmd": "animate",
    "error": {
      "code": "ANIMATION_NOT_FOUND",
      "message": "Animation 'backflip' is not available",
      "available_animations": ["wave", "nod", "shake", ...]
    }
  }
}
```

---

## 4. Privacy Requirements

### 4.1 Core Privacy Principles

| Principle | Implementation |
|-----------|----------------|
| **Minimal Data Collection** | No continuous recording; PTT-only audio capture |
| **Local Processing First** | STT/TTS on JARVIS Core, not cloud |
| **Explicit Consent** | PTT button = consent to record |
| **Visual Indicators** | LED always shows recording/camera state |
| **Data Ephemerality** | Audio buffers cleared after processing |
| **No Hidden Surveillance** | Camera off by default, requires explicit command |

### 4.2 Camera Privacy

```yaml
camera_policy:
  default_state: "off"
  activation:
    - requires: "explicit_command"  # capture_frame() or start_video()
    - requires: "user_confirmation"  # optional: voice/button confirm
  indicators:
    led_pattern: "camera_active"    # distinct pattern (e.g., red ring)
    led_color: "#FF0000"
    audio_cue: "optional_click"
  auto_disable:
    timeout_seconds: 300            # auto-off after 5 min inactivity
    on_disconnect: true             # off when connection lost
  restrictions:
    - no_continuous_streaming_without_consent
    - no_face_recognition_storage
    - frames_processed_not_stored
```

### 4.3 Microphone Privacy

```yaml
microphone_policy:
  default_state: "off"
  activation:
    mode: "push_to_talk"            # PTT button required
    hotword: "disabled"             # no always-listening hotword
  indicators:
    led_pattern: "listening"
    led_color: "#00FF00"            # green = recording
    audio_cue: "subtle_beep_start"  # optional start/stop sounds
  processing:
    location: "jarvis_core"         # not on robot
    retention: "session_only"       # cleared after response
    transcription_stored: false     # optional: store in memory DB
  restrictions:
    - no_recording_without_ptt
    - audio_buffer_max_seconds: 60
    - no_background_audio_analysis
```

### 4.4 LED Indicator Patterns

| State | LED Pattern | Color | Description |
|-------|-------------|-------|-------------|
| Idle | Slow breathing | Soft blue (#4A90D9) | Robot ready, not active |
| Listening (PTT held) | Pulsing | Green (#00FF88) | Recording audio |
| Processing | Rotating chase | Cyan (#00FFFF) | Thinking/STT/LLM |
| Speaking | Audio-reactive | Purple (#8B5CF6) | TTS playback |
| Camera Active | Solid ring | Red (#FF0000) | Camera capturing |
| Error | Triple flash | Red (#FF0000) | Command failed |
| Disconnected | Slow pulse | Amber (#FFA500) | No connection |
| Charging | Breathing | Orange→Green | Battery state |
| Low Battery | Double flash | Orange (#FF8800) | Below 20% |

### 4.5 Data Flow Audit

```
Audio Flow (Privacy-Safe):
1. User presses PTT button → LED turns green
2. Robot captures audio chunks via I2S
3. Chunks streamed to JARVIS Core via WebSocket
4. JARVIS Core runs STT (faster-whisper, local)
5. Transcription sent to LLM (Claude/Ollama)
6. Response → TTS (edge-tts, local)
7. Audio streamed back to robot
8. Robot plays via speaker
9. All audio buffers cleared

Camera Flow (Privacy-Safe):
1. JARVIS Core sends capture_frame command
2. Robot LED ring turns red
3. Single frame captured
4. JPEG sent to JARVIS Core
5. Frame analyzed (local LLaVA or Claude Vision)
6. Frame discarded after analysis
7. LED ring turns off

NO persistent storage of audio or video by default.
```

---

## 5. Architecture Recommendations for V3 Readiness

### 5.1 Device Abstraction Layer

To support multiple robot types (Open Duck Mini, simpler alternatives, future robots), JARVIS Core should implement a device abstraction layer:

```python
# src/devices/base.py
"""
Device Abstraction Layer for JARVIS V3
Supports multiple robot/peripheral types through common interfaces
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum

class DeviceCapability(Enum):
    AUDIO_INPUT = "audio_input"
    AUDIO_OUTPUT = "audio_output"
    CAMERA = "camera"
    LED_DISPLAY = "led_display"
    MOTION = "motion"
    BUTTON_INPUT = "button_input"
    BATTERY = "battery"
    IMU = "imu"

@dataclass
class DeviceInfo:
    device_id: str
    device_type: str  # "open_duck_mini", "simple_speaker", "esp32_terminal"
    capabilities: list[DeviceCapability]
    firmware_version: str
    battery_percent: Optional[int] = None
    connected: bool = False

class DeviceClient(ABC):
    """Base class for all device clients"""

    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to device"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Gracefully disconnect"""
        pass

    @abstractmethod
    async def get_info(self) -> DeviceInfo:
        """Get device information and capabilities"""
        pass

    @abstractmethod
    async def send_command(self, cmd: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send command to device"""
        pass

    @abstractmethod
    def on_event(self, callback: Callable[[str, Dict[str, Any]], None]) -> None:
        """Register event callback"""
        pass

class AudioCapableDevice(DeviceClient):
    """Mixin for devices with audio I/O"""

    @abstractmethod
    async def start_audio_stream(self, sample_rate: int = 16000) -> str:
        """Start audio capture, return stream_id"""
        pass

    @abstractmethod
    async def stop_audio_stream(self, stream_id: str) -> None:
        """Stop audio capture"""
        pass

    @abstractmethod
    async def play_audio(self, audio_data: bytes, format: str = "pcm") -> None:
        """Play audio on device speaker"""
        pass

class VisualCapableDevice(DeviceClient):
    """Mixin for devices with camera"""

    @abstractmethod
    async def capture_frame(self, resolution: str = "640x480") -> bytes:
        """Capture single camera frame, return JPEG"""
        pass

    @abstractmethod
    async def set_led_pattern(self, pattern: str, color: Optional[str] = None) -> None:
        """Set LED display pattern"""
        pass

class MotionCapableDevice(DeviceClient):
    """Mixin for devices with movement"""

    @abstractmethod
    async def animate(self, animation: str, params: Optional[Dict] = None) -> None:
        """Play animation"""
        pass

    @abstractmethod
    async def get_pose(self) -> Dict[str, float]:
        """Get current pose/orientation"""
        pass
```

### 5.2 Plugin System for Robot Types

```python
# src/devices/registry.py
"""
Device Plugin Registry
Dynamically load and manage device type implementations
"""
from typing import Dict, Type
from pathlib import Path
import importlib

class DeviceRegistry:
    """Registry for device type plugins"""

    _plugins: Dict[str, Type[DeviceClient]] = {}

    @classmethod
    def register(cls, device_type: str, client_class: Type[DeviceClient]):
        """Register a device type implementation"""
        cls._plugins[device_type] = client_class

    @classmethod
    def get_client(cls, device_type: str) -> Type[DeviceClient]:
        """Get client class for device type"""
        if device_type not in cls._plugins:
            raise ValueError(f"Unknown device type: {device_type}")
        return cls._plugins[device_type]

    @classmethod
    def discover_plugins(cls, plugin_dir: Path):
        """Auto-discover device plugins in directory"""
        for py_file in plugin_dir.glob("*.py"):
            if py_file.stem.startswith("_"):
                continue
            module = importlib.import_module(f"devices.plugins.{py_file.stem}")
            if hasattr(module, "register_plugin"):
                module.register_plugin(cls)

# Example plugin: devices/plugins/open_duck_mini.py
"""
Open Duck Mini device plugin
"""
from devices.base import DeviceClient, AudioCapableDevice, VisualCapableDevice, MotionCapableDevice

class OpenDuckMiniClient(AudioCapableDevice, VisualCapableDevice, MotionCapableDevice):
    """Client for Open Duck Mini robot"""

    def __init__(self, host: str, port: int = 8766):
        self.host = host
        self.port = port
        self.ws = None

    async def connect(self) -> bool:
        import websockets
        self.ws = await websockets.connect(f"ws://{self.host}:{self.port}/robot")
        return True

    # ... implement all abstract methods ...

def register_plugin(registry):
    registry.register("open_duck_mini", OpenDuckMiniClient)
```

### 5.3 Robot Bridge Service

```python
# src/services/robot_bridge.py
"""
Robot Bridge Service
WebSocket hub for connected robots/devices
"""
import asyncio
import json
from typing import Dict, Set, Optional
import websockets
from websockets.server import WebSocketServerProtocol

class RobotBridge:
    """WebSocket hub for robot connections"""

    def __init__(self, host: str = "0.0.0.0", port: int = 8766):
        self.host = host
        self.port = port
        self.connections: Dict[str, WebSocketServerProtocol] = {}
        self.device_info: Dict[str, dict] = {}
        self.event_handlers: Dict[str, list] = {}

    async def start(self):
        """Start the WebSocket server"""
        async with websockets.serve(self._handler, self.host, self.port):
            print(f"Robot Bridge listening on ws://{self.host}:{self.port}")
            await asyncio.Future()  # Run forever

    async def _handler(self, ws: WebSocketServerProtocol, path: str):
        """Handle incoming robot connections"""
        device_id = None
        try:
            # Wait for handshake with device info
            handshake = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(handshake)

            if data.get("type") != "handshake":
                await ws.close(1002, "Expected handshake")
                return

            device_id = data["payload"]["device_id"]
            self.connections[device_id] = ws
            self.device_info[device_id] = data["payload"]

            print(f"Robot connected: {device_id} ({data['payload'].get('device_type')})")

            # Send acknowledgment
            await ws.send(json.dumps({
                "type": "handshake_ack",
                "payload": {"status": "connected"}
            }))

            # Handle messages
            async for message in ws:
                await self._handle_message(device_id, message)

        except websockets.ConnectionClosed:
            print(f"Robot disconnected: {device_id}")
        except Exception as e:
            print(f"Error handling robot connection: {e}")
        finally:
            if device_id and device_id in self.connections:
                del self.connections[device_id]
                del self.device_info[device_id]

    async def _handle_message(self, device_id: str, message: str):
        """Process message from robot"""
        data = json.loads(message)
        msg_type = data.get("type")

        if msg_type == "event":
            event_name = data["payload"]["event"]
            for handler in self.event_handlers.get(event_name, []):
                await handler(device_id, data["payload"])
        elif msg_type == "response":
            # Handle command responses
            pass
        elif msg_type == "stream":
            # Handle audio/video streams
            pass

    async def send_command(self, device_id: str, cmd: str, payload: dict) -> Optional[dict]:
        """Send command to specific robot"""
        if device_id not in self.connections:
            raise ValueError(f"Device not connected: {device_id}")

        ws = self.connections[device_id]
        message = json.dumps({
            "type": "command",
            "payload": {"cmd": cmd, **payload}
        })
        await ws.send(message)

        # Wait for response (simplified)
        response = await asyncio.wait_for(ws.recv(), timeout=5)
        return json.loads(response)

    async def broadcast_command(self, cmd: str, payload: dict):
        """Send command to all connected robots"""
        for device_id in self.connections:
            try:
                await self.send_command(device_id, cmd, payload)
            except Exception as e:
                print(f"Failed to send to {device_id}: {e}")

    def on_event(self, event_name: str, handler):
        """Register event handler"""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        self.event_handlers[event_name].append(handler)
```

### 5.4 Configuration Schema

```yaml
# config/devices.yaml
devices:
  robots:
    - id: "duck-01"
      type: "open_duck_mini"
      enabled: true
      connection:
        host: "duck-01.local"  # mDNS or IP
        port: 8766
      capabilities:
        audio: true
        camera: true
        motion: true
        leds: true
      privacy:
        ptt_required: true
        camera_confirmation: false
        led_indicators: true
      audio:
        sample_rate: 16000
        chunk_ms: 100
      motion:
        enabled_animations:
          - "wave"
          - "nod"
          - "shake"
          - "think"
          - "idle"
        restricted_animations: []  # e.g., "dance" if stability concerns

    - id: "simple-terminal"
      type: "esp32_audio"
      enabled: true
      connection:
        host: "192.168.1.50"
        port: 8766
      capabilities:
        audio: true
        camera: false
        motion: false
        leds: true
      privacy:
        ptt_required: true
        led_indicators: true

  bridge:
    host: "0.0.0.0"
    port: 8766
    auth:
      enabled: true
      method: "jwt"
      secret_env: "JARVIS_ROBOT_JWT_SECRET"
    heartbeat:
      interval_ms: 5000
      timeout_ms: 15000
```

### 5.5 Integration with Existing Voice Pipeline

The existing `voice_pipeline.py` should be extended to support robot audio sources:

```python
# Proposed additions to src/voice_pipeline.py

class AudioSource(ABC):
    """Abstract audio source"""
    @abstractmethod
    async def start(self) -> None: pass

    @abstractmethod
    async def stop(self) -> bytes: pass

class LocalMicSource(AudioSource):
    """Local microphone via sounddevice (current implementation)"""
    pass

class RobotMicSource(AudioSource):
    """Remote microphone via Robot Bridge"""

    def __init__(self, bridge: RobotBridge, device_id: str):
        self.bridge = bridge
        self.device_id = device_id
        self.audio_buffer = []
        self.streaming = False

    async def start(self) -> None:
        await self.bridge.send_command(
            self.device_id,
            "stream_audio",
            {"action": "start", "params": {"sample_rate": 16000}}
        )
        self.streaming = True
        # Audio chunks arrive via event handler

    async def stop(self) -> bytes:
        await self.bridge.send_command(
            self.device_id,
            "stream_audio",
            {"action": "stop"}
        )
        self.streaming = False
        return b"".join(self.audio_buffer)

class AudioOutput(ABC):
    """Abstract audio output"""
    @abstractmethod
    async def play(self, audio_data: bytes) -> None: pass

class LocalSpeakerOutput(AudioOutput):
    """Local speaker via sounddevice (current implementation)"""
    pass

class RobotSpeakerOutput(AudioOutput):
    """Remote speaker via Robot Bridge"""

    def __init__(self, bridge: RobotBridge, device_id: str):
        self.bridge = bridge
        self.device_id = device_id

    async def play(self, audio_data: bytes) -> None:
        # Convert to base64 for WebSocket transport
        import base64
        await self.bridge.send_command(
            self.device_id,
            "say",
            {"audio": {
                "format": "pcm_16k_16bit_mono",
                "data": base64.b64encode(audio_data).decode()
            }}
        )
```

---

## 6. Alternative Robot Options (EU Sourcing)

### 6.1 Comparison Matrix

| Robot | Type | Cost EUR | Build Difficulty | Capabilities | EU Availability |
|-------|------|----------|------------------|--------------|-----------------|
| **Open Duck Mini** | Bipedal walker | 350-550 | High | Full (motion, audio, camera, LED) | Self-source parts |
| **Reachy Mini** | Upper-body humanoid | 300-450 | Low (kit) | Arms, camera, LEDs, audio | Pre-order (late 2025) |
| **ESP32 Audio Terminal** | Static speaker | 50-100 | Low | Audio, LEDs only | Easy (Amazon.it) |
| **Raspberry Pi Robot** | Custom build | 100-300 | Medium | Configurable | Easy |
| **Modified Cozmo/Vector** | Desktop companion | 100-200 | Medium | Limited (proprietary) | Second-hand |

### 6.2 Option A: Reachy Mini (Recommended Alternative)

**Description**: Open-source expressive robot from Pollen Robotics / Hugging Face

| Aspect | Details |
|--------|---------|
| **Price** | EUR 299 (Lite) / EUR 449 (Wireless with Pi 5) |
| **Size** | 28 cm tall, 16 cm wide |
| **Features** | 7 DOF arms, camera, speaker, LED display, Python API |
| **Build** | Pre-assembled kit |
| **Shipping** | Late 2025 (EU based company) |
| **Open Source** | Yes, Python/JavaScript APIs |

**Pros**:
- Designed for AI integration
- Pre-built, no 3D printing needed
- Active development by HuggingFace
- EU company (France)

**Cons**:
- Not shipping yet
- Stationary (no legs/walking)
- Limited arm reach

**Source**: [Reachy Mini - Pollen Robotics](https://www.pollen-robotics.com/reachy-mini/)

### 6.3 Option B: ESP32 Audio Terminal (Simplest)

For a minimal V3 proof-of-concept, a simple audio terminal without motion:

```
Components:
- ESP32-S3-Audio-Board (Waveshare): ~EUR 25
- Small speaker (3W): ~EUR 5
- WS2812B LED ring: ~EUR 8
- 3D printed enclosure: ~EUR 10
- Power supply USB-C: ~EUR 10
-----------------------------------------
TOTAL: ~EUR 60
```

**Waveshare ESP32-S3-Audio-Board Features**:
- ESP32-S3 with WiFi + Bluetooth 5
- Dual microphone array
- Built-in speaker driver
- 7x RGB LEDs
- USB-C power

**Source**: [Waveshare ESP32-S3-Audio-Board](https://www.waveshare.com/esp32-s3-audio-board.htm)

This provides:
- Push-to-talk audio capture
- TTS playback
- LED status indicators
- WiFi connection to JARVIS Core

No motion, but functional voice interface for EUR 60.

### 6.4 Option C: DIY Raspberry Pi Terminal

```
Components:
- Raspberry Pi Zero 2W: EUR 18
- ReSpeaker 2-Mic HAT: EUR 15
- Small speaker: EUR 5
- WS2812B LED strip: EUR 8
- Pi Camera Module: EUR 15 (optional)
- Case/enclosure: EUR 10-20
- Power supply: EUR 10
-----------------------------------------
TOTAL: EUR 70-90
```

**Pros**:
- Familiar platform (same as Open Duck Mini compute)
- More processing power than ESP32
- Can run Python directly
- Easy to add camera

**Cons**:
- Requires case design
- More power hungry than ESP32
- Larger form factor

### 6.5 Recommendation

| Use Case | Recommended Option | Why |
|----------|-------------------|-----|
| Full V3 Experience | Open Duck Mini | Complete robot with motion |
| Quick Prototype | ESP32 Audio Terminal | Fast, cheap, functional |
| Future-Proof | Reachy Mini (wait) | Professional design, HuggingFace backed |
| Maximum Flexibility | DIY Raspberry Pi | Familiar, extensible |

**Phased Approach**:
1. **V3 Alpha**: Build ESP32 Audio Terminal (EUR 60, 1 day)
2. **V3 Beta**: Build Open Duck Mini (EUR 400, 3 weeks)
3. **V3 Final**: Evaluate Reachy Mini when available (late 2025)

---

## 7. Implementation Roadmap

### Phase 1: V3 Alpha - Audio Terminal (Week 1-2)

```
Goal: Validate protocol and integration with minimal hardware

Tasks:
[ ] Acquire ESP32-S3-Audio-Board
[ ] Flash firmware with WebSocket client
[ ] Implement basic message handlers (audio, LED)
[ ] Create RobotBridge service in JARVIS Core
[ ] Integrate with existing VoicePipeline
[ ] Test end-to-end voice interaction via robot

Deliverables:
- Working audio terminal connected to JARVIS
- Protocol validation
- Latency measurements
```

### Phase 2: V3 Beta - Full Robot (Week 3-6)

```
Goal: Build and integrate Open Duck Mini

Tasks:
[ ] Order all BOM components
[ ] Print robot parts (or order kit)
[ ] Assemble mechanical structure
[ ] Wire electronics (servos, IMU)
[ ] Add audio components (mic, speaker)
[ ] Add camera and LEDs
[ ] Deploy robot client daemon
[ ] Implement motion commands
[ ] Calibrate walking policies
[ ] Integration testing

Deliverables:
- Walking robot with full I/O
- All commands implemented
- Privacy controls validated
```

### Phase 3: V3 Release (Week 7-8)

```
Goal: Polish and document

Tasks:
[ ] Performance optimization
[ ] Error handling hardening
[ ] Documentation updates
[ ] User testing
[ ] Edge case handling

Deliverables:
- Production-ready robot integration
- Updated JARVIS_BUILD_GUIDE.md
- Demo video
```

---

## 8. Open Questions and Future Considerations

### 8.1 Unresolved Questions

| Question | Options | Decision Needed By |
|----------|---------|-------------------|
| Motion policy licensing | Use provided policies vs train custom | V3 Beta |
| Multi-robot support | Single robot vs fleet | V3 Final |
| Robot autonomy level | Full remote vs hybrid local | V3 Beta |
| Audio codec | Raw PCM vs Opus compression | V3 Alpha |
| Security auth | JWT vs mTLS vs API key | V3 Alpha |

### 8.2 Future Enhancements (Post V3)

- **Multi-robot coordination**: Multiple robots in different rooms
- **Gesture recognition**: Camera-based hand gesture commands
- **Face tracking**: Robot looks at speaker
- **Obstacle avoidance**: Autonomous navigation
- **Charging dock**: Auto-return for charging
- **Emotion display**: More complex LED/screen expressions
- **Local wake word**: Optional "Hey Jarvis" detection on robot

---

## References

### Project Sources
- [Open Duck Mini GitHub](https://github.com/apirrone/Open_Duck_Mini)
- [Open Duck Mini Discord](https://discord.gg/UtJZsgfQGe)
- [Reachy Mini - Pollen Robotics](https://www.pollen-robotics.com/reachy-mini/)
- [AIFITLAB Open Duck Mini Kit](https://aifitlab.com/products/openduckmini-open-source-version-of-the-bdx-droid)

### Technical References
- [WebSocket vs gRPC Comparison](https://ably.com/topic/grpc-vs-websocket)
- [MQTT vs WebSocket for IoT](https://www.emqx.com/en/blog/mqtt-vs-websocket)
- [ESP32 I2S Audio](https://dronebotworkshop.com/esp32-i2s/)
- [Waveshare ESP32-S3-Audio-Board](https://www.waveshare.com/esp32-s3-audio-board.htm)
- [Privacy Patterns for Domestic Robots (USENIX)](https://www.usenix.org/system/files/soups2024-windl.pdf)

### Hardware Suppliers (EU)
- [Amazon.it](https://amazon.it) - General components
- [Melopero](https://melopero.com) - Raspberry Pi, sensors
- [Robot Italy](https://robot-italy.com) - Robotics parts
- [PCBWay](https://www.pcbway.com) - Custom PCBs

---

**Document Version**: 1.0
**Last Updated**: 2025-01-10
**Author**: Agent G - Robot Integration Planner
**Status**: Planning Document for JARVIS V3
