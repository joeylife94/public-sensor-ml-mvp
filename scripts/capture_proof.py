#!/usr/bin/env python3
"""Capture a deterministic Playwright screenshot from the running dashboard."""
from __future__ import annotations

import argparse
import os
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8000/")
    parser.add_argument("--output", type=Path, default=Path("proof/screenshots/dashboard.png"))
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=1200)
    parser.add_argument(
        "--fetch-html",
        action="store_true",
        help="Fetch the running dashboard HTML with Python, then render it in Playwright. Useful where Chromium localhost navigation is policy-blocked.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    executable = os.getenv("PLAYWRIGHT_CHROMIUM_EXECUTABLE")

    with sync_playwright() as playwright:
        launch_args: dict[str, object] = {"headless": True}
        if executable:
            launch_args["executable_path"] = executable
        browser = playwright.chromium.launch(**launch_args)
        page = browser.new_page(viewport={"width": args.width, "height": args.height})

        if args.fetch_html:
            with urllib.request.urlopen(args.url, timeout=120) as response:
                if response.status != 200:
                    raise RuntimeError(f"Dashboard HTTP status: {response.status}")
                dashboard_html = response.read().decode("utf-8")
            page.set_content(dashboard_html, wait_until="load", timeout=120_000)
            page.wait_for_timeout(1000)
        else:
            page.goto(args.url, wait_until="networkidle", timeout=120_000)

        if page.title() != "Public Sensor ML MVP":
            raise RuntimeError(f"Unexpected dashboard title: {page.title()!r}")
        body = page.locator("body").inner_text()
        for marker in ("Ridge MAE", "Top statistical anomaly candidates", "Source quality"):
            if marker not in body:
                raise RuntimeError(f"Missing proof marker: {marker}")

        page.screenshot(path=str(args.output), full_page=True)
        browser.close()

    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
