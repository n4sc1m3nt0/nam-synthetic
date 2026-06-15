"""
src/dataset/nam_parser.py

Reads a .nam file and extracts everything useful from it.

A .nam file is just JSON. It contains:
  - metadata (name, version, loudness, sample_rate)
  - model_type ("LSTM", "WaveNet", "WaveNet-LSTM", etc.)
  - architecture (hyperparameters: hidden_size, num_layers, etc.)
  - weights (a flat list of floats — the actual neural network parameters)

We care about the weights because that's what encodes the amp's character.
"""

import json
import os
from dataclasses import dataclass, field


@dataclass
class NamProfile:
    """Everything we extract from a .nam file."""
    source_path: str

    # Metadata
    name: str = ""
    version: str = ""
    model_type: str = ""        # "LSTM", "WaveNet", etc.
    sample_rate: int = 48000
    loudness: float = -18.0

    # Architecture hyperparameters (varies by model_type)
    architecture: dict = field(default_factory=dict)

    # The actual neural network weights (flat list of floats)
    weights: list[float] = field(default_factory=list)

    @property
    def num_weights(self) -> int:
        return len(self.weights)

    @property
    def is_lstm(self) -> bool:
        return "LSTM" in self.model_type.upper()

    @property
    def is_wavenet(self) -> bool:
        return "WAVENET" in self.model_type.upper()

    def __repr__(self):
        return (
            f"NamProfile(name={self.name!r}, "
            f"model_type={self.model_type!r}, "
            f"num_weights={self.num_weights})"
        )


def load_nam(path: str) -> NamProfile:
    """
    Parse a .nam file and return a NamProfile.

    Raises ValueError if the file doesn't look like a valid .nam file.
    Raises FileNotFoundError if the path doesn't exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    encodings = ["utf-8", "latin-1", "utf-8-sig"]
    data = None
    last_error = None

    for encoding in encodings:
        try:
            with open(path, "r", encoding=encoding) as f:
                data = json.load(f)
            break
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            last_error = e
            continue

    if data is None:
        raise ValueError(f"Cannot parse as JSON (tried {encodings}): {path}") from last_error

    # Validate — every real .nam file has these keys
    if "weights" not in data:
        raise ValueError(f"Missing 'weights' key — not a .nam file: {path}")
    if "model_type" not in data:
        raise ValueError(f"Missing 'model_type' key — not a .nam file: {path}")

    metadata = data.get("metadata", {})

    return NamProfile(
        source_path=path,
        name=metadata.get("name", os.path.basename(path)),
        version=data.get("version", ""),
        model_type=data.get("model_type", ""),
        sample_rate=data.get("sample_rate", 48000),
        loudness=metadata.get("loudness", -18.0),
        architecture=data.get("architecture", {}),
        weights=data.get("weights", []),
    )


def load_nam_weights_only(path: str) -> list[float]:
    """
    Fast path: load only the weights array from a .nam file.
    Avoids building a full NamProfile object — useful in tight training loops.
    """
    encodings = ["utf-8", "latin-1", "utf-8-sig"]
    for encoding in encodings:
        try:
            with open(path, "r", encoding=encoding) as f:
                data = json.load(f)
            return data["weights"]
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
    raise ValueError(f"Cannot parse weights from {path}")


def summarise(profile: NamProfile) -> dict:
    """
    Return a small dict of key facts about a profile — useful for logging.
    Does not include the weights (too large to log).
    """
    return {
        "name": profile.name,
        "model_type": profile.model_type,
        "num_weights": profile.num_weights,
        "sample_rate": profile.sample_rate,
        "loudness": profile.loudness,
        "architecture": profile.architecture,
    }
