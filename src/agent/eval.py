from typing import List, Dict, Any
from .runner import run_task

def evaluate(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    results = []
    for t in tasks:
        r = run_task(t["start_url"], t["goal"], t.get("max_steps", 40))
        results.append({"name": t.get("name", "task"), **r})
    success_rate = sum(1 for r in results if r["success"]) / max(1, len(results))
    avg_steps = sum(r["steps"] for r in results) / max(1, len(results))
    total_viol = sum(r["violations"] for r in results)
    return {"success_rate": success_rate, "avg_steps": avg_steps, "violations": total_viol, "details": results}
