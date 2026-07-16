import mss
import cv2
import numpy as np
import pygame
import win32gui
import win32con
import win32api
import os
import traceback

# ==============================
# CONFIGURATION
# ==============================
ICON_FOLDER = "icons"
ITEM_VALUES = {
    "FadedPhotograph": 640,
    "TornBook": 1000,
    "BloatedTunaCan": 1000,
    "CatBed": 1000,
    "CoffeePot": 1000,
    "EmptyWineBottle": 1000,
    "ExpiredPasta": 1000,
    "RubberDuck": 1000,
    "AirFreshener": 2000,
    "LightBulb": 2000,
    "DartBoard": 2000,
    "FilmReel": 2000,
    "PosterOfNaturalWonders": 2000,
    "PaintedBox": 2000,
    "Pottery": 2000,
    "Rosary": 2000,
    "VeryComfortablePillow": 2000,
    "FineWristwatch": 3000,
    "MusicAlbum": 3000,
    "SilverTeaspoonSet": 3000,
    "Statuette": 3000,
    "Vase": 3000,
    "MusicBox": 5000,
    "PlayingCards": 5000,
    "RedCoralJewelry": 5000,
    "BreathtakingSnowGlobe": 7000,
    "Lance'sMixtape(5thEdition)": 10000


}

CAPTURE_REGION = {
    "left": 62, "top": 158, "width": 813, "height": 1149,
}

# Obsidian & Emerald Theme
TRANSPARENCY_COLOR = (15, 15, 15)
EMERALD_GREEN = (0, 200, 100)
WHITE_TEXT = (240, 240, 240)
GHOST_GREY = (140, 140, 140)
SHADOW_BLACK = (0, 0, 0)

# ==============================
# LOGIC
# ==============================
sct = mss.mss()
templates = {}


def load_templates():
    if not os.path.exists(ICON_FOLDER): os.makedirs(ICON_FOLDER)
    for filename in os.listdir(ICON_FOLDER):
        if filename.endswith(".png"):
            item_key = os.path.splitext(filename)[0]
            img = cv2.imread(os.path.join(ICON_FOLDER, filename), cv2.IMREAD_GRAYSCALE)
            if img is not None: templates[item_key] = img


def find_items_in_capture(screen_bgra):
    screen_gray = cv2.cvtColor(screen_bgra, cv2.COLOR_BGRA2GRAY)
    detected = []
    for name, template in templates.items():
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        if max_val >= 0.90:
            detected.append(name)
    return detected


def set_window_transparency(hwnd):
    styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    styles |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
    colorkey = win32api.RGB(*TRANSPARENCY_COLOR)
    win32gui.SetLayeredWindowAttributes(hwnd, colorkey, 0, win32con.LWA_COLORKEY)


# ==============================
# MAIN LOOP
# ==============================
def run_overlay():
    pygame.init()
    load_templates()

    # WIDER WINDOW: Increased from 450 to 600
    WIDTH, HEIGHT = 600, 350
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    hwnd = pygame.display.get_wm_info()["window"]

    # Position: Bottom Left
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 30, 700, WIDTH, HEIGHT, win32con.SWP_SHOWWINDOW)
    set_window_transparency(hwnd)

    # Fonts - Slightly larger for visibility
    header_font = pygame.font.SysFont("Courier New", 18, bold=True)
    total_font = pygame.font.SysFont("Verdana", 52, bold=True)
    list_font = pygame.font.SysFont("Verdana", 22, bold=False)

    running_total = 0
    items_on_screen_last_frame = set()
    manifest_history = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        tab_pressed = win32api.GetAsyncKeyState(0x09) & 0x8000
        f9_pressed = win32api.GetAsyncKeyState(0x78) & 0x8000

        if tab_pressed or f9_pressed:
            running_total = 0
            items_on_screen_last_frame = set()
            manifest_history = []
            win32api.Sleep(100)

        try:
            screenshot = np.array(sct.grab(CAPTURE_REGION))
            current_detected = set(find_items_in_capture(screenshot))

            for item in current_detected:
                if item not in items_on_screen_last_frame:
                    val = ITEM_VALUES.get(item, 0)
                    running_total += val
                    # Cleaner list format
                    manifest_history.insert(0, f"> {item:<25} +${val:,}")
                    if len(manifest_history) > 6: manifest_history.pop()

            items_on_screen_last_frame = current_detected
        except:
            pass

        # --- DRAWING ---
        screen.fill(TRANSPARENCY_COLOR)

        # Optional: Draw a dark "Backplate" for readability
        # Remove these lines if you want it strictly floating
        backdrop_rect = pygame.Rect(5, 5, 550, 320)
        pygame.draw.rect(screen, (30, 30, 30), backdrop_rect, border_radius=10)  # Dark grey background
        pygame.draw.rect(screen, EMERALD_GREEN, backdrop_rect, 2, border_radius=10)  # Emerald border

        # 1. Header
        header_surf = header_font.render("BETTER RAIDER v.1.0", True, EMERALD_GREEN)
        screen.blit(header_surf, (25, 20))

        # 2. Total Value
        total_str = f"${running_total:,}"
        # Thick shadow for contrast
        for offset in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
            shadow = total_font.render(total_str, True, SHADOW_BLACK)
            screen.blit(shadow, (25 + offset[0], 55 + offset[1]))

        total_surf = total_font.render(total_str, True, WHITE_TEXT)
        screen.blit(total_surf, (25, 55))

        # 3. Line
        pygame.draw.line(screen, EMERALD_GREEN, (25, 125), (530, 125), 3)

        # 4. History
        y_pos = 140
        for entry in manifest_history:
            entry_surf = list_font.render(entry, True, GHOST_GREY)
            screen.blit(entry_surf, (30, y_pos))
            y_pos += 30

        pygame.display.update()
        win32api.Sleep(150)

    pygame.quit()


if __name__ == "__main__":
    run_overlay()