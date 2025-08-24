import re
from typing import Dict, Any
from urllib.parse import urlparse

ALLOWED_DOMAINS = {"example.com", "www.w3schools.com"}
DANGEROUS_SELECTORS = re.compile(r"(delete|remove|purchase|buy|transfer|checkout|logout)", re.I)
PII_REGEX = re.compile(r"(ssn|social\s+security|credit\s*card|password)", re.I)

def is_domain_allowed(url: str) -> bool:
    try:
        netloc = urlparse(url).netloc
        host = netloc.split(":")[0]
        return host in ALLOWED_DOMAINS or any(host.endswith(d) for d in ALLOWED_DOMAINS)
    except Exception:
        return False

def safety_gate(obs: Dict[str, Any], action: Dict[str, Any]) -> (bool, str):
    url = obs.get("url", "")
    if not is_domain_allowed(url):
        return False, f"Domain not allowed: {url}"
    t = action.get("type", "")
    selector = action.get("selector", "") or ""
    text = action.get("text", "") or ""
    if DANGEROUS_SELECTORS.search(selector):
        return False, f"Blocked dangerous selector: {selector}"
    if PII_REGEX.search(text):
        return False, "PII-like content detected in text"
    return True, ""
