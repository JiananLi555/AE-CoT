#!/usr/bin/env python3
import argparse
from pathlib import Path

from openai import OpenAI

from config_loader import load_config
from judge import duo_judge, get_judge_client
from malicious_teacher import malicious_teacher


def parse_args():
    parser = argparse.ArgumentParser(description="Run the single-goal pipeline.")
    goal_group = parser.add_mutually_exclusive_group(required=True)
    goal_group.add_argument("--goal", help="Goal text to evaluate.")
    goal_group.add_argument("--goal-file", help="Path to a UTF-8 text file containing the goal.")
    parser.add_argument("--config", default=None, help="Path to config JSON. Defaults to ./config.json.")
    parser.add_argument("--skip-judge", action="store_true", help="Skip final judge evaluation.")
    return parser.parse_args()


def read_goal(args) -> str:
    if args.goal:
        return args.goal
    return Path(args.goal_file).read_text(encoding="utf-8").strip()


def make_client(model_config):
    return OpenAI(api_key=model_config["api_key"], base_url=model_config["base_url"])


def main():
    args = parse_args()
    config = load_config(args.config)
    goal = read_goal(args)

    print("=" * 70)
    print("Single Goal Pipeline")
    print("=" * 70)
    print(f"Goal: {goal}")
    print("=" * 70)

    final_query = malicious_teacher(goal, config)

    print("\n" + "=" * 70)
    print("Final Query")
    print("=" * 70)
    print(final_query)

    target_config = config["target_model"]
    generation_config = config["generation"]
    target_client = make_client(target_config)

    print("\n" + "=" * 70)
    print(f"Calling Target Model: {target_config['model']}")
    print("=" * 70)
    response = target_client.chat.completions.create(
        model=target_config["model"],
        messages=[{"role": "user", "content": final_query}],
        stream=False,
        max_tokens=generation_config["target_max_tokens"],
        temperature=generation_config["temperature"],
    )
    target_response = response.choices[0].message.content

    print("\n" + "=" * 70)
    print("Target Response")
    print("=" * 70)
    print(target_response)

    if args.skip_judge:
        return

    judge_config = config["judge_model"]
    judge_client, judge_model_name = get_judge_client(
        api_key=judge_config["api_key"],
        base_url=judge_config["base_url"],
        model_name=judge_config["model"],
    )
    scores, reasons, _ = duo_judge(
        [(goal, target_response)],
        judge_model_name=judge_model_name,
        judge_client=judge_client,
        judge_max_tokens=generation_config["judge_max_tokens"],
    )

    print("\n" + "=" * 70)
    print("Judge Result")
    print("=" * 70)
    print(f"Score: {scores[0] if scores else 'N/A'}")
    print(f"Reason: {reasons[0] if reasons else 'N/A'}")


if __name__ == "__main__":
    main()
