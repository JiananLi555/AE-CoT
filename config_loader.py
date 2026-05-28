import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_CONFIG: Dict[str, Any] = {
    "attack_model": {
        "api_key": "",
        "base_url": "",
        "model": "o3-mini"
    },
    "target_model": {
        "api_key": "",
        "base_url": "",
        "model": "o3-mini"
    },
    "judge_model": {
        "api_key": "",
        "base_url": "",
        "model": "gpt-4o-2024-11-20"
    },
    "generation": {
        "target_max_tokens": 4096,
        "judge_max_tokens": 2048,
        "temperature": 0.0
    },
    "evolution": {
        "population_size": 10,
        "max_generations": 3,
        "initial_mutation_rate": 0.3,
        "min_mutation_rate": 0.1,
        "max_mutation_rate": 0.3,
        "mutation_rate_step": 0.1,
        "crossover_rate": 0.5,
        "tournament_size": 3
    }
}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    path = Path(config_path or os.environ.get("ATTACK_CONFIG", "config.json"))
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found: {path}. Copy config.example.json to config.json "
            "or pass --config /path/to/config.json."
        )

    with path.open("r", encoding="utf-8") as f:
        user_config = json.load(f)

    config = _deep_merge(DEFAULT_CONFIG, user_config)
    _validate_config(config)
    return config


def _validate_config(config: Dict[str, Any]) -> None:
    for section in ("attack_model", "target_model", "judge_model"):
        missing = [key for key in ("api_key", "base_url", "model") if not config[section].get(key)]
        if missing:
            missing_text = ", ".join(missing)
            raise ValueError(f"Missing required config value(s) in {section}: {missing_text}")

        api_key = str(config[section]["api_key"])
        base_url = str(config[section]["base_url"])
        if api_key.startswith("YOUR_") or "YOUR_PROVIDER" in base_url:
            raise ValueError(f"Placeholder values remain in {section}. Please edit config.json.")
