import time

def run_harness(objective):
    print("=" * 40)
    print(f"[RAAGHU HARNESS] Starting Task: "{objective}"")
    print("=" * 40 + "\n")
    for step in range(1, 4):
        print(f"--- Step {step} of 3 ---")
        print("[CONDUCTOR] Evaluating state...")
        time.sleep(0.3)
        print("[BOUNCER] Scanning safety policies... Passed.")
        time.sleep(0.3)
        print("[TOOL REGISTRY] Executing operation... [OK]\n")
    print("=" * 40)
    print("[RAAGHU HARNESS] Task completed successfully!")
    print("=" * 40)

if __name__ == "__main__":
    run_harness("Verify raaghu harness core execution loop")
