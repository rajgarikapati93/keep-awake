import os, re, sys
from playwright.sync_api import sync_playwright

URLS = os.environ["APP_URLS"].split()
failed = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    for url in URLS:
        page = browser.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(8000)
            btn = page.get_by_role("button", name=re.compile("get this app back up", re.I))
            if btn.count():
                print(f"{url}: asleep, clicking wake button")
                btn.first.click()
                page.wait_for_timeout(90000)
            else:
                page.wait_for_timeout(20000)
            if page.locator("iframe").count() == 0:
                failed.append(url)
                print(f"{url}: app did not load")
            else:
                print(f"{url}: awake")
        except Exception as e:
            failed.append(url)
            print(f"{url}: error {e}")
        finally:
            page.close()
    browser.close()

sys.exit(1 if failed else 0)
