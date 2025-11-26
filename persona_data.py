"""Persona metadata loader for the Friend Connection System."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

# JSON data file that stores all persona information.
DATA_FILE = Path(__file__).with_suffix(".json")


def load_personas() -> Dict[str, Any]:
    """Load personas from the JSON file; returns an empty dict on failure."""
    if not DATA_FILE.exists():
        print(f"[persona_data] Missing data file: {DATA_FILE}")
        return {}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as exc:  # pragma: no cover - defensive guardrail
        print(f"[persona_data] Failed to load {DATA_FILE}: {exc}")
        return {}


# Cache personas at import so existing imports keep working.
PERSONAS: Dict[str, Any] = load_personas()


def get_persona(name: str):
    """Return persona data for a given name if it exists."""
    if not name:
        return None
    return PERSONAS.get(name)


def get_all_personas() -> Dict[str, Any]:
    """Return the entire persona mapping."""
    return PERSONAS
