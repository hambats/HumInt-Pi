"""Simple Flask server providing a modern web UI for HUMINT-Pi.

This server exposes a dashboard showing the most recent audio capture
and a dynamically generated spectrogram.  It is intentionally lightweight
and does not require the full BirdNET-Pi PHP stack.

Run with:
    python scripts/ui_server.py

The server expects recorded audio files to be stored in ``recordings/``
at the project root.  Spectrograms are generated on demand using
``librosa`` and ``matplotlib``.
"""

from __future__ import annotations

import io
from datetime import datetime
from pathlib import Path

import librosa
import librosa.display  # noqa: F401  - needed for specshow
import numpy as np
from flask import Flask, abort, jsonify, send_file, send_from_directory
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent.parent
RECORDINGS_DIR = BASE_DIR / "recordings"


app = Flask(
    __name__,
    static_folder=str(BASE_DIR / "homepage"),
    template_folder=str(BASE_DIR / "homepage"),
)


@app.route("/")
def index() -> object:
    """Return the dashboard page."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/recent")
def recent_capture() -> object:
    """Return metadata for the most recent recording.

    Returns an empty 404 JSON response if no recordings are present.
    """

    if not RECORDINGS_DIR.exists():
        return jsonify({}), 404

    wavs = sorted(
        RECORDINGS_DIR.glob("*.wav"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not wavs:
        return jsonify({}), 404

    latest = wavs[0]
    return jsonify(
        {
            "filename": latest.name,
            "timestamp": datetime.fromtimestamp(latest.stat().st_mtime).isoformat(),
        }
    )


@app.route("/api/audio/<path:filename>")
def serve_audio(filename: str):
    """Serve a raw audio file for playback."""
    file_path = RECORDINGS_DIR / filename
    if not file_path.exists():
        abort(404)
    return send_file(file_path, mimetype="audio/wav")


@app.route("/api/spectrogram/<path:filename>")
def spectrogram(filename: str):
    """Generate and return a PNG spectrogram for ``filename``."""

    file_path = RECORDINGS_DIR / filename
    if not file_path.exists():
        abort(404)

    y, sr = librosa.load(file_path, sr=None)
    spec = librosa.stft(y)
    spec_db = librosa.amplitude_to_db(np.abs(spec), ref=np.max)

    fig, ax = plt.subplots(figsize=(10, 4))
    librosa.display.specshow(spec_db, sr=sr, x_axis="time", y_axis="hz", ax=ax)
    ax.set(title="Spectrogram")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    return send_file(buf, mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)

