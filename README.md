# nam-synthetic

> **Generate custom Neural Amp Modeler profiles from text descriptions using AI**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-gray)

Generate `.nam` guitar amplifier profiles on-demand based on plain text descriptions. Train an AI to understand the semantic space of guitar tones and synthesize new profiles that match user descriptions.

## Vision

Instead of hunting through pre-recorded amp profiles, describe your ideal tone in words:

> *"Warm, bluesy Marshall-style crunch with natural breakup and a tight low-end. Responsive to pick attack."*

The system generates a trained `.nam` file that captures that sonic character.

## Data & Licensing

This project is designed to be trained on a **collection of NAM captures that you create and own yourself**, or on captures you have explicit permission and a compatible license to use for training and redistribution.

Training an embedding space or a generative hypernetwork on someone else's captures — and distributing the resulting model — is a form of re-distribution and can violate the license under which those captures were shared. **Do not use this project to scrape, train on, or redistribute third-party tone libraries** (including TONE3000) without permission. The repository ships only with a generic `.nam` format parser; you supply your own curated dataset.

## How It Works

**4-Phase Pipeline:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: Dataset Assembly                                       │
│ • Parse your own curated collection of .nam files               │
│ • Attach text descriptions (authored or AI-assisted)           │
│ └─ Builds (text, .nam) training pairs                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────────┐
│ Phase 2: Tone Encoding                                          │
│ • Train autoencoder: .nam weights → compact 256-d "tone vector"│
│ • Reduces ~500KB file to efficient latent representation        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────────┐
│ Phase 3: Text → Tone Mapping                                    │
│ • Train model: user description → tone vector                  │
│ • Learns semantic space of guitar tones                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────────┐
│ Phase 4: Generative Synthesis                                   │
│ • Train hypernetwork decoder: tone vector → .nam weights        │
│ • Generates realistic NAM profiles from vectors                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    ┌──────┴──────────────┐
                    │                     │
                User Input           Generated Profile
                (text)                    (.nam file)
                    │                     │
                    └──────────┬──────────┘
                         │
                 Use in DAW or Amp Modeler
```

**At Inference:**
```
User describes tone → Text Encoder → Tone Vector → Hypernetwork → .nam file
```

## Quick Start

### Prerequisites
- Python 3.10+
- A collection of `.nam` files that you own or are licensed to train on, placed under `data/raw/`

### Setup

```bash
# Clone and setup
git clone <repo>
cd nam-synthetic
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies (only needed once you reach the ML training phases)
pip install -r requirements.txt
```

## Project Structure

```
nam-synthetic/
├── data/
│   ├── raw/                    your own .nam files + metadata
│   └── processed/              cleaned datasets ready for training
│
├── src/
│   ├── dataset/                Phase 1: Data Preparation
│   │   └── nam_parser.py        .nam file format parser & validator
│   │
│   ├── encoder/                Phase 2: Tone Autoencoder (coming soon)
│   ├── mapper/                 Phase 3: Text → Tone (coming soon)
│   └── hypernetwork/           Phase 4: Synthesis (coming soon)
│
└── README.md
```

## The .nam Parser

`src/dataset/nam_parser.py` reads and validates `.nam` files (multiple text encodings supported) and exposes them as structured `NamProfile` objects:

```python
from src.dataset import load_nam, summarise

profile = load_nam("data/raw/my_capture.nam")
print(summarise(profile))
```

## Current Status

| Phase | Status | Notes |
|-------|--------|-------|
| **Phase 1** | In progress | `.nam` parser complete; bring your own curated dataset |
| **Phase 2** | Pending | Awaiting phase 1 dataset completion |
| **Phase 3** | Pending | Design complete, awaiting phase 2 |
| **Phase 4** | Pending | Architecture designed, implementation pending |

## License

MIT

---

Questions? Open an issue.
