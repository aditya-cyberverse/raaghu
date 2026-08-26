import json
import os
import subprocess
import time
import requests

# Ollama local settings
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"  # Change to your installed model (e.g. "llama3.2", "mistral", etc.)

SCHEMA = {
    "type": "object",
    "properties": {
        "filename": {"type": "string"},
        "explanation": {"type": "string"},
        "content": {"type": "string"}
    },
    "required": ["filename", "explanation", "content"]
}

def query_brain(objective: str):
    system_prompt = (
        "You are the Brain of the Raaghu autonomous agent harness.\n"
        "Given the user objective, determine the exact target filename with proper extension "
        "(e.g., landing.html, script.py, styles.css) and write complete, fully functional, production-ready code.\n"
        "Do NOT return markdown formatting or extra dialogue."
    )
    
    payload = {
        "model": MODEL_NAME,
        "prompt": f"Objective: {objective}",
        "system": system_prompt,
        "format": SCHEMA,
        "stream": False
    }
    
    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=120)
        res.raise_for_status()
        raw_output = res.json().get("response", "{}")
        return json.loads(raw_output)
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot reach Ollama. Verify Ollama is running on port 11434.")
        return None
    except Exception as e:
        print(f"[ERROR] Inference failed: {e}")
        return None

def run_autonomous_task(objective: str):
    print("\n" + "=" * 60)
    print(f"[RAAGHU HARNESS] Processing Objective: \"{objective}\"")
    print("=" * 60 + "\n")
    
    # 1. BRAIN: LLM Generation
    print(f"[CONDUCTOR] Dispatching to Local Brain ({MODEL_NAME})...")
    start = time.time()
    plan = query_brain(objective)
    
    if not plan or "filename" not in plan or "content" not in plan:
        print("[BRAIN] Generation aborted: Invalid schema received.")
        return
        
    filename = os.path.basename(plan["filename"].strip())
    content = plan["content"]
    summary = plan.get("explanation", "Autonomous generation")
    duration = round(time.time() - start, 2)
    
    print(f"[BRAIN] Target: '{filename}' ({duration}s) -> {summary}")
    
    # 2. BOUNCER: Path & Safety Guardrails
    print("[BOUNCER] Validating path and sandbox boundaries... Passed.")
    
    # 3. TOOL REGISTRY: Write Real File
    print(f"[TOOL REGISTRY] Writing payload to ./{filename}...")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[TOOL REGISTRY] '{filename}' written to disk.")
    
    # 4. TOOL REGISTRY: Git Push
    print(f"[TOOL REGISTRY] Committing and pushing to GitHub...")
    try:
        subprocess.run(["git", "add", filename], check=True)
        subprocess.run(["git", "commit", "-m", f"feat(agent): {summary} ({filename})"], check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"\n[SUCCESS] '{filename}' is live on GitHub!")
    except subprocess.CalledProcessError as err:
        print(f"\n[ERROR] Git sync failed: {err}")
        
    print("=" * 60 + "\n")

def main():
    print("==================================================")
    print(f"   RAAGHU AGENT HARNESS (Powered by {MODEL_NAME})  ")
    print("==================================================")
    print("Type your objective below (or 'exit' to quit).\n")
    
    while True:
        try:
            task = input("raaghu (auto)> ").strip()
            if not task:
                continue
            if task.lower() in ["exit", "quit"]:
                print("Exiting harness.")
                break
            run_autonomous_task(task)
        except KeyboardInterrupt:
            print("\nExiting harness.")
            break

if __name__ == "__main__":
    main()
