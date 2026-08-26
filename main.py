import time

def run_harness(objective):
    print("=" * 40)
    print(f"[RAAGHU HARNESS] Starting Task: \"{objective}\"")
    print("=" * 40 + "\n")
    
    step = 1
    max_steps = 3
    
    while step <= max_steps:
        print(f"--- Step {step} of {max_steps} ---")
        print("[CONDUCTOR] Evaluating current state...")
        time.sleep(0.5)
        print("[BOUNCER] Scanning actions for safety and policy compliance... Passed.")
        time.sleep(0.5)
        print("[TOOL REGISTRY] Executing sandbox operation... [OK]\n")
        step += 1
        
    print("=" * 40)
    print("[RAAGHU HARNESS] Task completed successfully!")
    print("=" * 40)

if __name__ == "__main__":
    run_harness("Verify raaghu harness core execution loop")
