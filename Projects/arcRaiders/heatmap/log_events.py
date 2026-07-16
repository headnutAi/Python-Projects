import matplotlib.pyplot as plt
import csv
import os

MAP_IMAGE = "DamBattlegrounds.png"
OUTPUT_FILE = "events.csv"

# Ensure CSV exists
if not os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y", "event"])

print("Controls:")
print("Left click  = fight")
print("Right click = loot")
print("Middle click = death")
print("Close window to exit")

def onclick(event):
    if event.xdata is None or event.ydata is None:
        return

    x, y = int(event.xdata), int(event.ydata)

    if event.button == 1:
        event_type = "fight"
    elif event.button == 3:
        event_type = "loot"
    elif event.button == 2:
        event_type = "death"
    else:
        return

    with open(OUTPUT_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([x, y, event_type])

    print(f"Logged {event_type} at ({x}, {y})")

img = plt.imread(MAP_IMAGE)
plt.imshow(img)
plt.title("DAM Battlegrounds – Click to Log Events")
plt.axis("off")
plt.connect("button_press_event", onclick)
plt.show()
