# Structured CoT Evaluation Pipeline

This repository contains a single-goal evaluation pipeline with configurable
OpenAI-compatible model providers.

## Setup

```bash
pip install -r requirements.txt
cp config.example.json config.json
```

Edit `config.json` and set the API keys, base URLs, model names, generation
limits, and evolution parameters.

## Run

```bash
python run_single_attack.py --goal "Your goal text here"
```

You can also load the goal from a file:

```bash
python run_single_attack.py --goal-file goal.txt
```

To skip the final judge call:

```bash
python run_single_attack.py --goal "Your goal text here" --skip-judge
```

`config.json` is ignored by git so local credentials are not committed.
