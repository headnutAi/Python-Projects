from seleniumbase import SB
import time

with SB(uc=True) as sb:
    sb.uc_open_with_reconnect("https://chatgpt.com", 6)

    assert "No results found." not in sb.get_page_source(), "Fehler: Text wurde gefunden!"

    sb.click('//button[contains(normalize-space(.), "Anmelden") and not(contains(@style, "display: none"))]')
    time.sleep(3)

    sb.type("#email", "dropshippingshop2023@gmail.com")
    sb.click('//button[contains(normalize-space(.), "Weiter") and not(contains(@style, "display: none"))]')
    time.sleep(3)

    sb.click('//button[contains(normalize-space(.), "Weiter") and not(contains(@style, "display: none"))]')
    sb.type("#password", "...")

    time.sleep(10)
