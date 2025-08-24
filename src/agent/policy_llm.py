from typing import Dict, Any, List

SYSTEM = (
    "You are a risk-aware web agent. "
    "Return a single JSON action with fields: "
    '{"type":"click|type|goto|scroll|submit|back","selector":"...","text":"...","url":"...","dx":0,"dy":0}. '
    "Avoid destructive actions. Prefer semantic selectors (roles, aria-labels)."
)

def _contains_all(text: str, words: List[str]) -> bool:
    t = text.lower()
    return all(w.lower() in t for w in words)

def heuristic_policy(obs: Dict[str, Any], goal_words: List[str]) -> Dict[str, Any]:
    dom = (obs.get("dom") or "").lower()
    if _contains_all(dom, goal_words):
        return {"type": "submit", "selector": "button, [role='button'], input[type='submit']",
                "text": "", "url": "", "dx": 0, "dy": 0}
    if "search" in dom:
        return {"type": "type", "selector": "input[type='search'], input[name='q'], [role='searchbox']",
                "text": " ".join(goal_words), "url": "", "dx": 0, "dy": 0}
    return {"type": "scroll", "selector": "", "text": "", "url": "", "dx": 0, "dy": 800}

def policy_fn(obs: Dict[str, Any], goal_words: List[str]) -> Dict[str, Any]:
    return heuristic_policy(obs, goal_words)
