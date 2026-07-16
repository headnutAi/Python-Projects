import pyautogui
import keyboard
import time
import random
from PIL import ImageGrab

# ==================== KONFIGURATION ====================
# Trag hier deine ermittelte RGB-Farbe aus dem Kalibrierungsmodus ein
TARGET_COLOR = (255, 85, 85)

# Wie stark darf die Farbe abweichen?
COLOR_TOLERANCE = 10

# Suchbereich (Mittleres Drittel des Bildschirms)
screen_width, screen_height = pyautogui.size()
SEARCH_REGION = (int(screen_width / 3), int(screen_height / 3), int(screen_width / 3), int(screen_height / 3))


# =======================================================

def check_for_color():
    """Scannt den Bereich nach der Ziel-Farbe ab."""
    bbox = (SEARCH_REGION[0], SEARCH_REGION[1], SEARCH_REGION[0] + SEARCH_REGION[2],
            SEARCH_REGION[1] + SEARCH_REGION[3])
    screenshot = ImageGrab.grab(bbox=bbox)
    img_rgb = screenshot.convert('RGB')

    for x in range(0, img_rgb.width, 3):
        for y in range(0, img_rgb.height, 3):
            r, g, b = img_rgb.getpixel((x, y))
            if (abs(r - TARGET_COLOR[0]) <= COLOR_TOLERANCE and
                    abs(g - TARGET_COLOR[1]) <= COLOR_TOLERANCE and
                    abs(b - TARGET_COLOR[2]) <= COLOR_TOLERANCE):
                return True
    return False


def calibrate_color():
    """Hilfsfunktion: Gibt die RGB-Farbe unter der Maus aus."""
    print("\n🎨 --- KALIBRIERUNGS-MODUS ---")
    print("Bewege deine Maus auf den Mod-Text und drücke 'F10'.")
    print("Drücke 'ESC' um die Kalibrierung zu beenden.")
    while True:
        if keyboard.is_pressed('f10'):
            x, y = pyautogui.position()
            color = pyautogui.pixel(x, y)
            print(f"📍 Position: {x}, {y} -> RGB-Farbe: {color}")
            time.sleep(0.5)
        if keyboard.is_pressed('esc'):
            print("Kalibrierung beendet.\n")
            break


def skyblock_fish_bot():
    print(f" 🦾 Hypixel Stealth-Fisher aktiviert.")
    print("-> 'F7' = Farbkallibrierung | 'F9' = Start/Pause | 'q' = Beenden")

    running = False

    while True:
        if keyboard.is_pressed('q'):
            print("Skript beendet.")
            break

        if keyboard.is_pressed('f7'):
            calibrate_color()

        if keyboard.is_pressed('f9'):
            running = not running
            print(f"{'▶️ BOT GESTARTET' if running else '⏸️ BOT PAUSIERT'}")
            time.sleep(1)

        if running:
            print("\n[INFO] Werfe Angel aus...")
            pyautogui.click(button='right')

            # Leicht zufällige Zeit, bis die Angel im Wasser landet
            time.sleep(random.uniform(1.5, 1.9))

            print("[INFO] Scanne Bildschirm nach Mod-Text...")
            start_time = time.time()
            bite_detected = False

            while (time.time() - start_time) < 35:
                if keyboard.is_pressed('q') or keyboard.is_pressed('f9'):
                    running = False
                    break

                if check_for_color():
                    print("✨ MOD-TEXT ERKANNT!")
                    bite_detected = True
                    break

                time.sleep(0.03)

                # ================= NEUE REAKTIONSZEIT-LOGIK =================
            if bite_detected:
                # Generiert eine minimale Verzögerung zwischen 40ms und 170ms
                reaktions_zeit = random.uniform(0.022, 0.032)
                print(f"⏱️ Pro-Gamer-Reaktion simuliert: +{reaktions_zeit:.3f}s")
                time.sleep(reaktions_zeit)

                # Jetzt erst einholen
                pyautogui.click(button='right')
                print("🐟 Fisch/Monster am Haken!")
            else:
                # Falls Timeout: Einfach direkt einholen
                pyautogui.click(button='right')
                print("⏳ Zeitüberschreitung.")
            # ============================================================

            # Variable Wartezeit vor dem nächsten Wurf (50/50-Chance)
            if random.random() < 0.5:
                wartezeit = random.uniform(0.2, 0.35)
                print(f"⚡ [Variante A] Fast-Cast aktiv. Wartezeit: {wartezeit:.2f}s")
            else:
                wartezeit = random.uniform(0.2, 0.35)
                print(f"⏳ [Variante B] Human-Delay aktiv. Wartezeit: {wartezeit:.2f}s")

            time.sleep(wartezeit)


if __name__ == "__main__":
    skyblock_fish_bot()