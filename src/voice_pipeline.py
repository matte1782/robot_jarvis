"""
Jarvis Voice Pipeline
Push-to-talk voice interface using faster-whisper (STT) and edge-tts (TTS)

SECURITY: Uses pynput instead of keyboard library (no admin required)

Usage:
    python voice_pipeline.py

Controls:
    F9 (hold): Push-to-talk (record while held)
    Ctrl+C:    Exit

Requirements:
    pip install faster-whisper edge-tts sounddevice numpy pynput
"""
import asyncio
import io
import subprocess
import sys
import wave
import tempfile
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable

import numpy as np
import sounddevice as sd
from pynput import keyboard

# Optional imports with graceful fallback
try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("WARNING: faster-whisper not installed. STT disabled.")
    print("Install with: pip install faster-whisper")

try:
    import edge_tts
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("WARNING: edge-tts not installed. TTS disabled.")
    print("Install with: pip install edge-tts")


# =============================================================================
# CONFIGURATION
# =============================================================================

# Audio settings
SAMPLE_RATE = 16000          # Whisper expects 16kHz
CHANNELS = 1                 # Mono
DTYPE = 'int16'              # 16-bit audio

# Whisper settings - use environment variables for customization
WHISPER_MODEL = "base"
WHISPER_DEVICE = "cpu"  # or "cuda" for GPU
WHISPER_COMPUTE = "int8"

# TTS settings
TTS_VOICE = "en-US-GuyNeural"
# Italian: "it-IT-DiegoNeural", "it-IT-ElsaNeural"
# English: "en-US-GuyNeural", "en-GB-RyanNeural"

# Hotkey (F9 for push-to-talk)
PUSH_TO_TALK_KEY = keyboard.Key.f9


# =============================================================================
# SPEECH-TO-TEXT (faster-whisper)
# =============================================================================

class SpeechToText:
    """Speech-to-text using faster-whisper"""

    def __init__(self, model_size: str = WHISPER_MODEL,
                 device: str = WHISPER_DEVICE,
                 compute_type: str = WHISPER_COMPUTE):
        self.model = None
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type

        if WHISPER_AVAILABLE:
            self._load_model()

    def _load_model(self):
        """Load Whisper model"""
        print(f"Loading Whisper model: {self.model_size} ({self.device}, {self.compute_type})...")
        try:
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type
            )
            print("Whisper model loaded successfully")
        except Exception as e:
            print(f"ERROR: Failed to load Whisper model: {e}")
            self.model = None

    def transcribe(self, audio_data: np.ndarray) -> str:
        """
        Transcribe audio data to text.

        Args:
            audio_data: NumPy array of audio samples (16kHz, mono, int16)

        Returns:
            Transcribed text
        """
        if self.model is None:
            return "[STT not available]"

        try:
            # Convert int16 to float32 for Whisper
            audio_float = audio_data.astype(np.float32) / 32768.0

            # Transcribe
            segments, info = self.model.transcribe(
                audio_float,
                beam_size=5,
                language=None,  # Auto-detect
                vad_filter=True,  # Voice activity detection
                vad_parameters=dict(
                    min_silence_duration_ms=500,
                    speech_pad_ms=400
                )
            )

            # Collect text
            text = " ".join(segment.text.strip() for segment in segments)
            return text.strip()

        except Exception as e:
            print(f"ERROR: Transcription failed: {e}")
            return ""


# =============================================================================
# TEXT-TO-SPEECH (edge-tts)
# =============================================================================

class TextToSpeech:
    """Text-to-speech using Microsoft Edge TTS"""

    def __init__(self, voice: str = TTS_VOICE):
        self.voice = voice

    async def speak_async(self, text: str) -> Optional[bytes]:
        """
        Convert text to speech audio.

        Args:
            text: Text to speak

        Returns:
            MP3 audio data as bytes, or None on error
        """
        if not TTS_AVAILABLE:
            print("[TTS not available]")
            return None

        try:
            communicate = edge_tts.Communicate(text, self.voice)
            audio_data = b""

            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]

            return audio_data

        except Exception as e:
            print(f"ERROR: TTS failed: {e}")
            return None

    def speak(self, text: str) -> Optional[bytes]:
        """Synchronous wrapper for speak_async"""
        return asyncio.run(self.speak_async(text))

    async def save_async(self, text: str, filepath: str) -> bool:
        """Save speech to file"""
        if not TTS_AVAILABLE:
            return False

        try:
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(filepath)
            return True
        except Exception as e:
            print(f"ERROR: Failed to save TTS: {e}")
            return False


# =============================================================================
# AUDIO RECORDER
# =============================================================================

class AudioRecorder:
    """Audio recorder with push-to-talk support"""

    def __init__(self, sample_rate: int = SAMPLE_RATE,
                 channels: int = CHANNELS):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_buffer = []
        self._stream = None

    def start_recording(self):
        """Start recording audio"""
        if self.recording:
            return

        self.audio_buffer = []
        self.recording = True

        def callback(indata, frames, time_info, status):
            if status:
                print(f"Audio status: {status}")
            if self.recording:
                self.audio_buffer.append(indata.copy())

        try:
            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=DTYPE,
                callback=callback
            )
            self._stream.start()
            print("[Recording...]")
        except Exception as e:
            print(f"ERROR: Failed to start recording: {e}")
            self.recording = False

    def stop_recording(self) -> Optional[np.ndarray]:
        """Stop recording and return audio data"""
        if not self.recording:
            return None

        self.recording = False

        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None

        if not self.audio_buffer:
            return None

        # Concatenate all audio chunks
        audio_data = np.concatenate(self.audio_buffer, axis=0)
        self.audio_buffer = []

        print(f"[Recorded {len(audio_data) / self.sample_rate:.1f}s]")
        return audio_data.flatten()


# =============================================================================
# AUDIO PLAYBACK (safe implementation)
# =============================================================================

def play_audio_file(filepath: str) -> bool:
    """
    Play an audio file using system default player.

    SECURITY: Uses subprocess with shell=False for safety.

    Args:
        filepath: Path to audio file

    Returns:
        True if playback started successfully
    """
    filepath = str(filepath)

    try:
        if sys.platform == 'win32':
            # Windows: Use Windows Media Player via COM or powershell
            # Using powershell's Add-Type for safe media playback
            subprocess.Popen(
                ['powershell', '-WindowStyle', 'Hidden', '-Command',
                 f'(New-Object Media.SoundPlayer "{filepath}").PlaySync()'],
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        elif sys.platform == 'darwin':
            # macOS: afplay
            subprocess.Popen(
                ['afplay', filepath],
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            # Linux: try mpv, then aplay, then paplay
            for player in [['mpv', '--no-terminal'], ['aplay'], ['paplay']]:
                try:
                    subprocess.Popen(
                        player + [filepath],
                        shell=False,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    break
                except FileNotFoundError:
                    continue
        return True
    except Exception as e:
        print(f"ERROR: Failed to play audio: {e}")
        return False


# =============================================================================
# VOICE PIPELINE
# =============================================================================

class VoicePipeline:
    """
    Complete voice pipeline with push-to-talk.

    Uses pynput for keyboard handling (no admin required).
    """

    def __init__(self, on_transcription: Optional[Callable[[str], None]] = None):
        """
        Initialize voice pipeline.

        Args:
            on_transcription: Callback function called with transcribed text
        """
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.recorder = AudioRecorder()
        self.on_transcription = on_transcription
        self._listener = None
        self._running = False

    def _on_press(self, key):
        """Handle key press"""
        try:
            if key == PUSH_TO_TALK_KEY:
                self.recorder.start_recording()
        except AttributeError:
            pass

    def _on_release(self, key):
        """Handle key release"""
        try:
            if key == PUSH_TO_TALK_KEY:
                audio_data = self.recorder.stop_recording()

                if audio_data is not None and len(audio_data) > 0:
                    # Transcribe in background thread
                    threading.Thread(
                        target=self._process_audio,
                        args=(audio_data,),
                        daemon=True
                    ).start()

            # Stop on Escape
            if key == keyboard.Key.esc:
                print("\n[Stopping...]")
                return False

        except AttributeError:
            pass

    def _process_audio(self, audio_data: np.ndarray):
        """Process recorded audio (runs in background thread)"""
        print("[Transcribing...]")

        text = self.stt.transcribe(audio_data)

        if text:
            print(f"\n>> {text}\n")

            if self.on_transcription:
                try:
                    self.on_transcription(text)
                except Exception as e:
                    print(f"ERROR: Callback failed: {e}")
        else:
            print("[No speech detected]")

    def respond(self, text: str):
        """Speak a response using TTS"""
        if not text:
            return

        print(f"<< {text}")
        audio_data = self.tts.speak(text)

        if audio_data:
            # Save to temp file and play
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                f.write(audio_data)
                temp_path = f.name

            try:
                play_audio_file(temp_path)
            finally:
                # Cleanup after delay
                def cleanup():
                    try:
                        Path(temp_path).unlink(missing_ok=True)
                    except Exception:
                        pass
                threading.Timer(10.0, cleanup).start()

    def start(self):
        """Start the voice pipeline"""
        print("=" * 50)
        print("JARVIS Voice Pipeline")
        print("=" * 50)
        print(f"STT: {'faster-whisper (' + self.stt.model_size + ')' if WHISPER_AVAILABLE else 'disabled'}")
        print(f"TTS: {'edge-tts (' + self.tts.voice + ')' if TTS_AVAILABLE else 'disabled'}")
        print(f"Push-to-talk: {PUSH_TO_TALK_KEY}")
        print("-" * 50)
        print("Hold F9 to speak, release to transcribe")
        print("Press Escape to exit")
        print("=" * 50)

        self._running = True

        # Start keyboard listener (pynput - no admin required)
        with keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        ) as listener:
            self._listener = listener
            listener.join()

        self._running = False
        print("Voice pipeline stopped")

    def stop(self):
        """Stop the voice pipeline"""
        self._running = False
        if self._listener:
            self._listener.stop()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point"""

    def handle_transcription(text: str):
        """Handle transcribed text - integrate with your LLM here"""
        # Example: Echo back using TTS
        # In production, send to Claude/Ollama and speak the response
        if text.lower().startswith("hello"):
            pipeline.respond("Hello! How can I help you?")
        elif text.lower().startswith("time"):
            now = datetime.now().strftime("%I:%M %p")
            pipeline.respond(f"The time is {now}")
        else:
            # Default: just acknowledge
            print("[Received, processing...]")
            # TODO: Send to LLM and get response
            # response = await call_llm(text)
            # pipeline.respond(response)

    pipeline = VoicePipeline(on_transcription=handle_transcription)

    try:
        pipeline.start()
    except KeyboardInterrupt:
        print("\n[Interrupted]")
        pipeline.stop()


if __name__ == "__main__":
    main()
