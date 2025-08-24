import argparse, json, time
from pathlib import Path
from typing import List, Dict, Any
from playwright.sync_api import sync_playwright
from .observe import observe
from .policy_llm import policy_fn
from .safety import safety_gate

def done_heuristic(obs: Dict[str, Any], goal_words: List[str]) -> bool:
    text = (obs.get("dom") or "").lower()
    return all(w.lower() in text for w in goal_words)

def act(page, action: Dict[str, Any]):
    t = action.get("type")
    try:
        if t == "click":
            page.click(action["selector"], timeout=5000)
        elif t == "type":
            page.fill(action["selector"], action.get("text", ""), timeout=5000)
        elif t == "goto":
            page.goto(action["url"], wait_until="domcontentloaded", timeout=10000)
        elif t == "scroll":
            page.mouse.wheel(action.get("dx", 0), action.get("dy", 800))
        elif t == "submit":
            page.click(action.get("selector", "button, [role='button'], input[type='submit']"))
        elif t == "back":
            page.go_back()
        else:
            return False, f"Unknown action type: {t}"
    except Exception as e:
        return False, str(e)
    return True, ""

def run_task(start_url: str, goal: str, budget: int = 40, out_dir: str = "replays") -> Dict[str, Any]:
    goal_words = [w.strip() for w in goal.split() if w.strip()]
    run_id = time.strftime("%Y%m%d-%H%M%S")
    out_path = Path(out_dir) / run_id
    out_path.mkdir(parents=True, exist_ok=True)
    log_file = out_path / "traj.jsonl"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(start_url)

        success = False
        steps = 0
        violations = 0

        with open(log_file, "w") as f:
            for step in range(budget):
                steps += 1
                obs = observe(page)

                if done_heuristic(obs, goal_words):
                    success = True
                    f.write(json.dumps({"event": "done", "step": step, "obs_url": obs["url"]}) + "\n")
                    break

                action = policy_fn(obs, goal_words)
                ok, reason = safety_gate(obs, action)
                if not ok:
                    violations += 1
                    f.write(json.dumps({"event": "safety_block", "step": step, "reason": reason, "action": action}) + "\n")
                    action = {"type": "scroll", "selector": "", "text": "", "url": "", "dx": 0, "dy": 600}

                ok, err = act(page, action)
                f.write(json.dumps({"event": "step", "step": step, "action": action, "ok": ok, "err": err, "url": page.url}) + "\n")
                if not ok:
                    page.reload()

        browser.close()

    return {"success": success, "steps": steps, "violations": violations, "log_dir": str(out_path)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start_url", required=True)
    ap.add_argument("--goal", required=True)
    ap.add_argument("--budget", type=int, default=40)
    args = ap.parse_args()
    res = run_task(args.start_url, args.goal, args.budget)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
