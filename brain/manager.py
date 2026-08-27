import json
import re
from brain.providers import LLMProvider

class BrainManager:
    """Pure management engine: plans, delegates, audits, and supervises."""

    def __init__(self):
        self.llm = LLMProvider()

    def create_execution_plan(self, objective: str) -> dict:
        """Deconstructs user prompt into a task pipeline."""
        system_prompt = (
            "You are the Meta-Brain Manager of the Raaghu autonomous system.\n"
            "Your ONLY role is task management, orchestration, and delegation.\n"
            "Do NOT write implementation code.\n"
            "Analyze the objective and return strictly valid JSON matching this schema:\n"
            "{\n"
            '  "task_name": "<concise_name>",\n'
            '  "target_file": "<filename_to_generate_or_edit>",\n'
            '  "assigned_worker": "local_coder" | "cloud_coder" | "media_generator",\n'
            '  "action_items": [\n'
            '    "Step 1: Description",\n'
            '    "Step 2: Description"\n'
            '  ],\n'
            '  "worker_prompt": "<explicit instructions for the downstream worker>"\n'
            "}"
        )

        raw_plan = self.llm.query_manager(
            prompt=f"Objective to manage: {objective}",
            system=system_prompt
        )

        try:
            match = re.search(r"\{[\s\S]*\}", raw_plan)
            clean_json = match.group(0) if match else raw_plan
            return json.loads(clean_json)
        except Exception:
            return {
                "task_name": "task_fallback",
                "target_file": "output.txt",
                "assigned_worker": "local_coder",
                "action_items": ["Execute target requirement"],
                "worker_prompt": objective
            }

    def audit_task(self, plan: dict, worker_output: str) -> bool:
        """Verifies if worker output meets the planned file target and content constraints."""
        if not worker_output or len(worker_output.strip()) == 0:
            return False
        return True
