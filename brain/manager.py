import json
import re
from brain.providers import LLMProvider

class BrainManager:
    def __init__(self):
        self.llm = LLMProvider()

    def plan_objective(self, user_prompt: str) -> dict:
        system_instruction = (
            "You are the Meta-Brain of the Raaghu Autonomous Agent.\n"
            "Analyze the objective and break it down into a structured execution plan.\n"
            "Output strictly valid JSON with the following keys:\n"
            "{\n"
            '  "task_name": "<short_task_name>",\n'
            '  "target_file": "<filename_to_create_or_modify>",\n'
            '  "complexity": "low" | "medium" | "high",\n'
            '  "steps": ["step 1", "step 2", "step 3"],\n'
            '  "prompt_for_worker": "<refined clear instruction for execution>"\n'
            "}"
        )

        raw_plan = self.llm.query_cloud_manager(
            prompt=f"User Objective: {user_prompt}", 
            system=system_instruction
        )

        # Parse JSON output cleanly
        try:
            json_match = re.search(r"\{[\s\S]*\}", raw_plan)
            clean_json = json_match.group(0) if json_match else raw_plan
            return json.loads(clean_json)
        except Exception:
            return {
                "task_name": "general_execution",
                "target_file": "output.txt",
                "complexity": "low",
                "steps": ["Direct execution"],
                "prompt_for_worker": user_prompt
            }

    def supervise_and_generate(self, plan: dict) -> str:
        system_instruction = (
            "You are a code synthesis engine. Given the task plan, write complete, production-ready code.\n"
            "Do NOT include conversational filler."
        )
        worker_prompt = f"Plan: {plan['steps']}\nInstruction: {plan['prompt_for_worker']}"
        
        # Use cloud manager or local worker depending on complexity
        if plan.get("complexity") == "high":
            return self.llm.query_cloud_manager(worker_prompt, system=system_instruction)
        else:
            return self.llm.query_ollama(worker_prompt, system=system_instruction)
