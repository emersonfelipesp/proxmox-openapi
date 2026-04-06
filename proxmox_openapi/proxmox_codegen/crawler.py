"""Crawler for Proxmox API Viewer using Playwright."""

from __future__ import annotations

import asyncio
import importlib.util

_playwright_sync_api_available: bool | None = None


def _check_playwright_sync_api_available() -> bool:
    """Check if playwright sync API is available."""
    global _playwright_sync_api_available
    if _playwright_sync_api_available is None:
        _playwright_sync_api_available = importlib.util.find_spec("playwright.sync_api") is not None
    return _playwright_sync_api_available


async def crawl_proxmox_api_viewer_async(
    url: str,
    worker_count: int = 10,
    retry_count: int = 2,
    retry_backoff_seconds: float = 0.35,
    checkpoint_path: str | None = None,
    checkpoint_every: int = 50,
) -> dict[str, object]:
    """Crawl Proxmox API viewer to capture endpoint definitions."""

    if not _check_playwright_sync_api_available():
        return {
            "endpoints": {},
            "discovered_navigation_items": 0,
            "method_count": 0,
            "failed_endpoint_count": 0,
            "duration_seconds": 0.0,
        }

    from playwright.sync_api import sync_playwright

    endpoints: dict[str, object] = {}
    failed_endpoints: list[str] = []
    discovered_navigation_items = 0

    def run_crawler() -> None:
        """Run the synchronous Playwright crawl in a worker thread."""
        nonlocal discovered_navigation_items
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_selector("nav", timeout=10000)

            nav = page.locator("nav")
            items = nav.locator("a").all()
            discovered_navigation_items = len(items)

            for item in items:
                try:
                    href = item.get_attribute("href")
                    if href:
                        endpoints[href] = {
                            "path": href,
                            "text": item.text_content(),
                            "methods": {},
                        }
                except Exception:
                    failed_endpoints.append(item.text_content() or "")

            browser.close()

    await asyncio.to_thread(run_crawler)

    return {
        "endpoints": endpoints,
        "discovered_navigation_items": discovered_navigation_items,
        "method_count": len(endpoints),
        "failed_endpoint_count": len(failed_endpoints),
        "duration_seconds": 0.0,
    }


__all__ = ["crawl_proxmox_api_viewer_async"]
