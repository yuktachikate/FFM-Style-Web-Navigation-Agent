from typing import Dict, Any
from playwright.sync_api import Page

def observe(page: Page) -> Dict[str, Any]:
    """Capture the current browser observation (trimmed DOM for speed)."""
    dom = page.content()[:200_000]
    url = page.url
    try:
        a11y = page.accessibility.snapshot()
    except Exception:
        a11y = None
    screenshot = None
    return {"url": url, "dom": dom, "a11y": a11y, "image": screenshot}
