from openai import OpenAI

from judge import get_judge_client
from structured_evolution import run_structured_evolution
from templates import malicious_teacher_suffix, teacher_template


def _make_client(model_config):
    return OpenAI(
        api_key=model_config["api_key"],
        base_url=model_config["base_url"],
    )


def malicious_teacher(input_text: str, config: dict) -> str:
    attack_config = config["attack_model"]
    target_config = config["target_model"]
    judge_config = config["judge_model"]
    generation_config = config["generation"]
    evolution_config = config["evolution"]

    target_client = _make_client(target_config)
    attack_client = _make_client(attack_config)
    judge_client, judge_model_name = get_judge_client(
        api_key=judge_config["api_key"],
        base_url=judge_config["base_url"],
        model_name=judge_config["model"],
    )

    print("Step 1: Generating initial rewritten prompt...")
    response = attack_client.chat.completions.create(
        model=attack_config["model"],
        messages=[
            {"role": "user", "content": teacher_template.format(goal=input_text)},
        ],
        stream=False,
        temperature=generation_config["temperature"],
    )
    malicious_teacher_main = response.choices[0].message.content
    print("Step 1 complete.")

    print("Step 2: Starting structured CoT evolution process...")
    best_evolved_cot_text = run_structured_evolution(
        malicious_teacher_main=malicious_teacher_main,
        malicious_teacher_suffix=malicious_teacher_suffix,
        target_model_client=target_client,
        target_model_name=target_config["model"],
        judge_model_client=judge_client,
        judge_model_name=judge_model_name,
        target_max_tokens=generation_config["target_max_tokens"],
        judge_max_tokens=generation_config["judge_max_tokens"],
        population_size=evolution_config["population_size"],
        max_generations=evolution_config["max_generations"],
        initial_mutation_rate=evolution_config["initial_mutation_rate"],
        min_mutation_rate=evolution_config["min_mutation_rate"],
        max_mutation_rate=evolution_config["max_mutation_rate"],
        mutation_rate_step=evolution_config["mutation_rate_step"],
        crossover_rate=evolution_config["crossover_rate"],
        tournament_size=evolution_config["tournament_size"],
    )
    print("Step 2 complete.\n")

    print("Step 3: Assembling final query with evolved CoT...")
    final_query_evolved = malicious_teacher_main + malicious_teacher_suffix + best_evolved_cot_text
    print("Step 3 complete.\n")

    return final_query_evolved
