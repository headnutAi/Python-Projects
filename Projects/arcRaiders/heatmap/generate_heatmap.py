import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import Normalize
from scipy.ndimage import gaussian_filter

# ======================
# CONFIG
# ======================
MAP_IMAGE = "DamBattlegrounds.png"
DATA_FILE = "events.csv"
ACTIVE_EVENT = "loot"   # "loot", "fight", or "death"

# Adjust SIGMA to change how "blurry" or "spread out" the heat is
# Higher = smoother/larger glows. Lower = more precise/sharper spots.
SIGMA = 5
BINS = 300 # Keep high for smooth detail
ALPHA = 0.7

EVENT_CMAPS = {
    "loot": "YlGn",
    "fight": "Oranges",
    "death": "Reds",
}

# ======================
# DATA PROCESSING
# ======================
data = pd.read_csv(DATA_FILE)
img = plt.imread(MAP_IMAGE)
img_h, img_w = img.shape[:2]

subset = data[data["event"] == ACTIVE_EVENT]

# Create the 2D Histogram
heatmap, xedges, yedges = np.histogram2d(
    subset["x"],
    subset["y"],
    bins=[np.linspace(0, img_w, BINS), np.linspace(0, img_h, BINS)]
)

# APPLY GAUSSIAN BLUR (This creates the "Heat" look)
# We transpose it now so the math matches the image axes
heatmap_smooth = gaussian_filter(heatmap.T, sigma=SIGMA)

# Mask the areas with no activity so the map is visible
heatmap_smooth = np.ma.masked_where(heatmap_smooth < 0.01, heatmap_smooth)

# ======================
# RENDER
# ======================
plt.figure(figsize=(12, 12), dpi=150)

# 1. Background Map
plt.imshow(img)

# 2. Heatmap Overlay
plt.imshow(
    heatmap_smooth,
    extent=[0, img_w, img_h, 0], # Matches top-left origin
    cmap=EVENT_CMAPS.get(ACTIVE_EVENT, "viridis"),
    alpha=ALPHA,
    origin='upper',
    aspect='equal'
)

plt.axis("off")
plt.title(f"DAM Battlegrounds – {ACTIVE_EVENT.upper()} Intensity", fontsize=16, pad=20)
plt.tight_layout()
plt.show()