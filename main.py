import json
import os
import re
import subprocess
import time
import requests

# Ollama local endpoint and default model
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"  # Replace with your installed model if different (e.g., "llama3.2", "mistral")

SYSTEM_PROMPT = """
You are the Brain brick of the Raaghu autonomous agent harness.
Given a user objective, decide on the best filename (with proper extension) and write clean, complete, production-ready code.

You MUST respond strictly in valid JSON format with no additional conversational text:
{
  "filename": "exact_name_with_extension",
  "explanation": "1-sentence summary of what was generated",
  "content": "raw code or document content here"
}
"""

def query_ollama(objective: str) -> dict:
    """Sends the objective to the local Ollama instance and parses the structured response."""
    payload = {
        "model": MODEL_NAME,
        "prompt": f"User Objective: {objective}",
        "system": SYSTEM_PROMPT,
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        res_json = response.json()
        raw_text = res_json.get("response", "{}")
        return json.loads(raw_text)
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to Ollama. Make sure the Ollama app is running locally on port 11434.")
        return None
    except Exception as err:
        print(f"\n[ERROR] Failed during LLM inference: {err}")
        return None

def run_autonomous_task(objective: str):
    print("\n" + "=" * 60)
    print(f"[RAAGHU HARNESS] Starting Task: \"{objective}\"")
    print("=" * 60 + "\n")
    
    # 1. CONDUCTOR & BRAIN: Query Local Model
    print(f"[CONDUCTOR] Dispatching objective to Local Brain ({MODEL_NAME})...")
    start_time = time.time()
    plan = query_ollama(objective)
    
    if not plan or "filename" not in plan or "content" not in plan:
        print("[BRAIN] Failed to generate a valid file plan. Task aborted.")
        return
        
    filename = plan["filename"].strip()
    file_content = plan["content"]
    explanation = plan.get("explanation", "Autonomous generation")
    duration = round(time.time() - start_time, 2)
    
    print(f"[BRAIN] Generated '{filename}' in {duration}s -> {explanation}")
    
    # 2. BOUNCER: Guardrail Checks
    print("[BOUNCER] Scanning generated file path and safety policies...")
    if os.path.isabs(filename) or ".." in filename:
        print("[BOUNCER] Rejected: Path traversal attempt detected. Task aborted.")
        return
    print("[BOUNCER] Policy check passed.")
    
    # 3. TOOL REGISTRY: Write File
    print(f"[TOOL REGISTRY] Writing payload to ./{filename}...")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(file_content)
    print(f"[TOOL REGISTRY] File '{filename}' created successfully.")
    
    # 4. TOOL REGISTRY: Git Push Pipeline
    print(f"[TOOL REGISTRY] Executing Git pipeline to sync with GitHub...")
    try:
        subprocess.run(["git", "add", filename], check=True)
        subprocess.run(["git", "commit", "-m", f"feat(agent): {explanation} ({filename})"], check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"\n[SUCCESS] '{filename}' successfully deployed to GitHub repository!")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Git sync failed: {e}")
        
    print("=" * 60 + "\n")

def main():
    print("==================================================")
    print("   RAAGHU AI AGENT HARNESS (Ollama Powered)       ")
    print("==================================================")
    print(f"Engine: Local Ollama ({MODEL_NAME})")
    print("Type your objective below (e.g., 'build landing.html with dark mode hero section')")
    print("Type 'exit' or 'quit' to close.\n")
    
    while True:
        try:
            user_input = input("raaghu (ollama)> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Shutting down raaghu harness. Goodbye!")
                break
            run_autonomous_task(user_input)
        except KeyboardInterrupt:
            print("\nShutting down raaghu harness. Goodbye!")
            break

if __name__ == "__main__":
    main()
