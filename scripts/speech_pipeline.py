"""Speech detection, transcription and classification pipeline."""

from __future__ import annotations

import datetime as _dt
from typing import Iterable

import numpy as np
import webrtcvad
import whisper
from langdetect import detect
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from . import database


vad = webrtcvad.Vad(3)
model = whisper.load_model("small.en")
sentiment_analyser = SentimentIntensityAnalyzer()


def _is_speech(audio_bytes: bytes, sample_rate: int) -> bool:
    """Return True if audio chunk contains speech according to VAD."""

    frame_ms = 30
    frame_len = int(sample_rate * frame_ms / 1000) * 2  # 16-bit samples
    for start in range(0, len(audio_bytes), frame_len):
        frame = audio_bytes[start : start + frame_len]
        if len(frame) < frame_len:
            break
        if vad.is_speech(frame, sample_rate):
            return True
    return False


def _detect_keywords(text: str, keywords: Iterable[str]) -> list[str]:
    return [k for k in keywords if k.lower() in text.lower()]


def process_audio_chunk(
    audio_bytes: bytes,
    sample_rate: int,
    keywords: Iterable[str],
    conn,
):
    """Process a chunk of audio. If speech is detected, transcribe and store it."""

    if not _is_speech(audio_bytes, sample_rate):
        return None

    audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    result = model.transcribe(audio)
    transcript = result["text"].strip()
    language = detect(transcript) if transcript else ""
    found = _detect_keywords(transcript, keywords)
    sentiment = sentiment_analyser.polarity_scores(transcript)["compound"]

    timestamp = _dt.datetime.utcnow().isoformat()
    database.insert_event(conn, timestamp, transcript, language, found, str(sentiment))

    return {
        "timestamp": timestamp,
        "transcript": transcript,
        "language": language,
        "keywords": found,
        "sentiment": sentiment,
    }

