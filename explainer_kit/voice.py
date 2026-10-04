"""Local speech services for manim-voiceover.

KokoroService: high-quality local TTS (Kokoro-82M via ONNX). No API keys.
SilentService: silent audio with estimated timing, for fast layout drafts.

Bookmarks (<bookmark mark='x'/>) get exact times without Whisper: the text is
split at each bookmark and at each sentence end, each segment is synthesized
separately, and a boundary is recorded at every segment start. So bookmark
times and sentence start times (used for captions) are exact sample offsets.
Put bookmarks at clause or sentence boundaries so the split does not break
the prosody. Word-level timing inside a sentence is not available: the ONNX
Kokoro model returns audio only, without phoneme durations.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import numpy as np
import soundfile as sf
from manim import logger
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService, initialize_speech_service, path_to_string
from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

from explainer_kit.paths import model_dir

MODEL_DIR = model_dir()
MODEL_FILE = MODEL_DIR / "kokoro-v1.0.onnx"
VOICES_FILE = MODEL_DIR / "voices-v1.0.bin"
DEFAULT_VOICE = os.environ.get("EXPLAINER_VOICE", "af_heart")

BOOKMARK_SPLIT = re.compile(r"(<bookmark\s*mark\s*=[\'\"]\w*[\"\']\s*/>)")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=\S)")
SENTENCE_END = (".", "!", "?", ":")
CLAUSE_END = (",", ";", "—", "-")


def split_segments(text: str) -> list[tuple[str, int]]:
    """Split text at bookmarks and sentence ends. Return (segment, text_offset) pairs.

    text_offset is measured in the bookmark-free text, which is the space
    that VoiceoverTracker uses to place bookmarks.
    """
    segments: list[tuple[str, int]] = []
    offset = 0
    for part in BOOKMARK_SPLIT.split(text):
        if BOOKMARK_SPLIT.fullmatch(part):
            continue
        start = 0
        for m in [*SENTENCE_SPLIT.finditer(part), None]:
            end = m.start() if m else len(part)
            piece = part[start:end]
            if piece.strip():
                lead = len(piece) - len(piece.lstrip())
                segments.append((piece.strip(), offset + start + lead))
            if m:
                start = m.end()
        offset += len(part)
    return segments


def gap_after(segment: str, sentence_pause: float, clause_pause: float) -> float:
    tail = segment.rstrip()
    if tail.endswith(SENTENCE_END):
        return sentence_pause
    if tail.endswith(CLAUSE_END):
        return clause_pause
    return 0.03


def apply_lexicon(text: str, lexicon: dict[str, str]) -> str:
    """Replace written forms with spoken forms. Captions keep the written form."""
    for written, spoken in lexicon.items():
        text = re.sub(rf"(?<!\w){re.escape(written)}(?!\w)", spoken, text)
    return text


class _SegmentedService(SpeechService):
    """Shared logic: synthesize per bookmark segment, then record boundaries."""

    service_name = "segmented"
    sample_rate = 24_000

    def __init__(self, lexicon: dict[str, str] | None = None, sentence_pause: float = 0.35,
                 clause_pause: float = 0.12, **kwargs: object) -> None:
        initialize_speech_service(self, kwargs)
        self.lexicon = lexicon or {}
        self.sentence_pause = sentence_pause
        self.clause_pause = clause_pause

    def _input_data(self, text: str) -> dict:
        return {"input_text": text, "service": self.service_name, "lexicon": self.lexicon, "segmenter": 2,
                "sentence_pause": self.sentence_pause, "clause_pause": self.clause_pause}

    def synthesize(self, text: str) -> np.ndarray:
        raise NotImplementedError

    def generate_from_text(self, text, cache_dir=None, path=None, **kwargs):
        cache_dir = Path(cache_dir or self.cache_dir)
        input_data = self._input_data(text)
        cached = self.get_cached_result(input_data, cache_dir)
        if cached is not None:
            return cached

        audio_path = path_to_string(path) if path else self.get_audio_basename(input_data) + ".wav"

        chunks: list[np.ndarray] = []
        boundaries = []
        n_samples = 0
        segments = split_segments(text)
        for i, (segment, text_offset) in enumerate(segments):
            boundaries.append({
                "audio_offset": int(n_samples / self.sample_rate * AUDIO_OFFSET_RESOLUTION),
                "text_offset": text_offset,
                "word_length": len(segment),
                "text": segment.strip(),
                "boundary_type": "Word",
            })
            audio = self.synthesize(apply_lexicon(segment.strip(), self.lexicon))
            chunks.append(audio)
            n_samples += len(audio)
            if i < len(segments) - 1:
                pause = np.zeros(int(gap_after(segment, self.sentence_pause, self.clause_pause) * self.sample_rate),
                                 dtype=np.float32)
                chunks.append(pause)
                n_samples += len(pause)

        boundaries.append({
            "audio_offset": int(n_samples / self.sample_rate * AUDIO_OFFSET_RESOLUTION),
            "text_offset": len(remove_bookmarks(text)),
            "word_length": 0,
            "text": "",
            "boundary_type": "Word",
        })

        audio = np.concatenate(chunks) if chunks else np.zeros(self.sample_rate // 4, dtype=np.float32)
        sf.write(cache_dir / audio_path, audio, self.sample_rate)
        return {"input_text": text, "input_data": input_data, "original_audio": audio_path,
                "word_boundaries": boundaries}


class KokoroService(_SegmentedService):
    """Kokoro-82M local TTS. Voices: af_heart, af_bella, am_michael, am_fenrir, bm_george, …"""

    service_name = "kokoro"
    _engine = None  # shared across scenes: loading the model takes about a second

    def __init__(self, voice: str = DEFAULT_VOICE, speed: float = 1.0, lang: str = "en-us", **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.voice = voice
        self.speed = speed
        self.lang = lang

    def _input_data(self, text: str) -> dict:
        return super()._input_data(text) | {"voice": self.voice, "speed": self.speed, "lang": self.lang}

    @classmethod
    def engine(cls):
        if cls._engine is None:
            from kokoro_onnx import Kokoro

            if not MODEL_FILE.exists() or not VOICES_FILE.exists():
                raise FileNotFoundError(
                    f"Kokoro model files are missing in {MODEL_DIR}. Run: uv run explainer setup"
                )
            cls._engine = Kokoro(str(MODEL_FILE), str(VOICES_FILE))
        return cls._engine

    def synthesize(self, text: str) -> np.ndarray:
        samples, sr = self.engine().create(text, voice=self.voice, speed=self.speed, lang=self.lang)
        assert sr == self.sample_rate, f"unexpected Kokoro sample rate {sr}"
        return samples.astype(np.float32)


class SilentService(_SegmentedService):
    """Silent audio. Duration is estimated at about 2.6 words per second."""

    service_name = "silent"
    words_per_second = 2.6

    def synthesize(self, text: str) -> np.ndarray:
        seconds = max(len(text.split()) / self.words_per_second, 0.3)
        return np.zeros(int(seconds * self.sample_rate), dtype=np.float32)


def make_speech_service(voice: str | None = None, **kwargs: object) -> SpeechService:
    """Select the service from EXPLAINER_TTS (kokoro | silent). Default: kokoro."""
    choice = os.environ.get("EXPLAINER_TTS", "kokoro").lower()
    if choice == "kokoro" and not MODEL_FILE.exists():
        logger.warning(f"Kokoro model not found in {MODEL_DIR}; using silent narration. Run: uv run explainer setup")
        choice = "silent"
    if choice == "silent":
        return SilentService(**kwargs)
    return KokoroService(voice=voice or DEFAULT_VOICE, **kwargs)
