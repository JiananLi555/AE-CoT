# Reasoning as an Attack Surface: Adaptive Evolutionary CoT Jailbreaks for LLMs.

Large Reasoning Models (LRMs) have demonstrated remarkable capabilities in reasoning and generation tasks and are increasingly deployed in real-world applications. However, their explicit chain-of-thought (CoT) mechanism introduces new security risks, making them particularly vulnerable to jailbreak attacks. Existing approaches often rely on static CoT templates to elicit harmful outputs, but such fixed designs suffer from limited diversity, adaptability, and effectiveness. To overcome these limitations, we propose an adaptive evolutionary CoT jailbreak framework, called AE-CoT. Specifically, the method first rewrites harmful goals into mild prompts with teacher role-play and decomposes them into semantically coherent reasoning fragments to construct a pool of CoT jailbreak candidates. Then, within a structured representation space, we perform multi-generation evolutionary search, where candidate diversity is expanded through fragment-level crossover and a mutation strategy with an adaptive mutation-rate control mechanism. An independent scoring model provides graded harmfulness evaluations, and high-scoring candidates are further enhanced with a harmful CoT template to induce more destructive generations. Extensive experiments across multiple models and datasets demonstrate the effectiveness of the proposed AE-CoT, consistently outperforming state-of-the-art jailbreak methods.



Our paper is accepted by ICML 2026🚀. Paper link: https://arxiv.org/abs/2605.24497


# AE-CoT Evaluation Pipeline

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
