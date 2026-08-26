from brain.manager import BrainManager
from tools.git_sync import GitSync

def main():
    brain = BrainManager()
    git = GitSync()

    print("==================================================")
    print("        RAAGHU BRAIN HARNESS (Meta-Manager)       ")
    print("==================================================")
    print("Brain initialized. Ready for objectives.\n")

    while True:
        try:
            objective = input("raaghu (brain)> ").strip()
            if not objective:
                continue
            if objective.lower() in ["exit", "quit"]:
                break

            print("\n[BRAIN: MANAGER] Deconstructing objective & formulating execution plan...")
            plan = brain.plan_objective(objective)
            print(f"[BRAIN: PLAN] Task: {plan.get('task_name')} | Target: {plan.get('target_file')}")
            for i, step in enumerate(plan.get('steps', []), 1):
                print(f"  {i}. {step}")

            print("\n[BRAIN: WORKER] Executing task...")
            content = brain.supervise_and_generate(plan)

            target_file = plan.get("target_file", "output.txt")
            git.sync_file(target_file, content)

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
