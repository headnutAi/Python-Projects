import mss
import cv2
import numpy as np
import pytesseract
from rapidfuzz import process, utils
import pygame
import win32gui
import win32con
import win32api
import time
import traceback

# ==============================
# CONFIGURATION
# ==============================

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Headnut\AppData\Local\Tesseract-OCR\tesseract.exe"

CAPTURE_REGION = {
    "left": 62,
    "top": 158,
    "width": 813,
    "height": 1149,
}

ITEM_VALUES = {
    "FADED PHOTO": 640,
    "TORN BOOK": 1000,
    "BLOATED TUNA": 1000,
    "CAT BED": 1000,
    "COFFEE POT": 1000,
    "WINE BOTTLE": 1000,
    "EXPIRED PASTA": 1000,
    "RUBBER DUCK": 1000,
    "AIR FRESHENER": 2000,
    "LIGHT BULB": 2000,
    "DART BOARD": 2000,
    "FILM REEL": 2000,
    "NATURAL WONDERS POSTER": 2000,
    "PAINTED BOX": 2000,
    "POTTERY": 2000,
    "ROSARY": 2000,
    "COMFORTABLE PILLOW": 2000,
    "WRISTWATCH": 3000,
    "MUSIC ALBUM": 3000,
    "SILVER TEASPOON SET": 3000,
    "STATUETTE": 3000,
    "VASE": 3000,
    "MUSIC BOX": 5000,
    "PLAYING CARDS": 5000,
    "CORAL JEWELRY": 5000,
    "SNOW GLOBE": 7000,
    "LANCE MIXTAPE": 10000
}

# Advanced Config: --oem 3 uses the LSTM neural engine for better character recognition
OCR_CONFIG = r'--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 '
TRANSPARENCY_COLOR = (15, 15, 15)

# ==============================
# SCREEN CAPTURE & REFINED PREPROCESSING
# ==============================

sct = mss.mss()


def capture_region():
    return np.array(sct.grab(CAPTURE_REGION))


def preprocess_ultra(img):
    # 1. Convert to Gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    # 2. Upscale 3x (Crucial for high-accuracy on small game fonts)
    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_LANCZOS4)

    # 3. Bilateral Filter: Removes noise while keeping letter edges sharp
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # 4. Adaptive Thresholding: Handles varying light levels in game world
    # We use BINARY_INV assuming light text on dark background
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # 5. Morphological Opening: Removes tiny "speckles"
    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    return thresh


# ==============================
# OCR + ITEM EXTRACTION
# ==============================

def extract_items(img):
    try:
        text = pytesseract.image_to_string(img, config=OCR_CONFIG)
    except:
        return []

    items = []
    for line in text.splitlines():
        # clean_line removes weird symbols and normalizes case
        clean_line = utils.default_process(line)
        if len(clean_line) < 3:
            continue

        # Fuzzy match with higher score_cutoff for accuracy in large lists
        match = process.extractOne(
            clean_line,
            list(ITEM_VALUES.keys()),
            processor=utils.default_process,
            score_cutoff=75
        )
        if match:
            items.append(match[0])
    return items


# ==============================
# OVERLAY HELPERS
# ==============================

def set_window_transparency(hwnd):
    styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    styles |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
    colorkey = win32api.RGB(*TRANSPARENCY_COLOR)
    win32gui.SetLayeredWindowAttributes(hwnd, colorkey, 0, win32con.LWA_COLORKEY)


# ==============================
# MAIN OVERLAY LOOP
# ==============================

def run_overlay():
    pygame.init()

    # Window Dimensions
    WIDTH, HEIGHT = 550, 120
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    hwnd = pygame.display.get_wm_info()["window"]

    # POSITION: Change X and Y to move the actual window on your monitor
    # (X=10, Y=940 puts it near the bottom-left of a 1080p screen)
    WINDOW_X = 10
    WINDOW_Y = 940

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, WINDOW_X, WINDOW_Y, WIDTH, HEIGHT,
                          win32con.SWP_NOACTIVATE | win32con.SWP_NOSIZE)
    set_window_transparency(hwnd)

    font = pygame.font.SysFont("Verdana", 32, bold=True)
    clock = pygame.time.Clock()

    # LOGIC VARIABLES
    running_total = 0
    items_currently_on_screen = set()

    print("Overlay active. Press F9 to reset.")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # F9 Reset Keybind
        if win32api.GetAsyncKeyState(0x78) & 0x8000:
            running_total = 0
            items_currently_on_screen = set()

        try:
            img_raw = capture_region()
            img_processed = preprocess_ultra(img_raw)

            # Optional: Uncomment to see the cleaned image for debugging
            # cv2.imshow("Debug View", img_processed)
            # cv2.waitKey(1)

            detected_this_frame = extract_items(img_processed)
            found_set = set(detected_this_frame)

            # Persistent Addition Logic
            for item in found_set:
                if item not in items_currently_on_screen:
                    running_total += ITEM_VALUES[item]

            # Remember what we are looking at so we don't count it twice
            items_currently_on_screen = found_set

        except Exception:
            traceback.print_exc()

        # --- DRAWING ---
        screen.fill(TRANSPARENCY_COLOR)
        display_text = f"Loot Total: ${running_total:,}"

        shadow_surf = font.render(display_text, True, (0, 0, 0))
        text_surf = font.render(display_text, True, (0, 255, 100))  # Green text

        # Position text at the BOTTOM-LEFT of the overlay window
        text_x = 10
        text_y = HEIGHT - text_surf.get_height() - 10

        screen.blit(shadow_surf, (text_x + 2, text_y + 2))
        screen.blit(text_surf, (text_x, text_y))

        pygame.display.update()
        clock.tick(2)

    pygame.quit()


if __name__ == "__main__":
    run_overlay()