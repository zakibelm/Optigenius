import os
import pytest
from playwright.sync_api import sync_playwright, expect

BASE_URL = os.getenv("E2E_BASE_URL", "https://api.optigenius.pro")

@pytest.mark.e2e
def test_form_submit_ok():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"{BASE_URL}/web/", wait_until="domcontentloaded")
        page.get_by_label("Nom").fill("E2E Bot")
        page.get_by_label("Téléphone").fill("+33123456789")
        page.get_by_label("Date & heure").fill("2026-01-01T09:00")
        page.get_by_label("Notes").fill("depuis e2e")
        page.get_by_role("button", name="Envoyer").click()
        expect(page.locator("#statusWrap .ok")).to_contain_text("Rendez-vous enregistré", timeout=7000)
        assert '"status":"ok"' in page.locator("#lastResp").inner_text()
        browser.close()
