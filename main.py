x = 0
for x in range(0, 4):
    print(" ")
    for x in range(-1, x):
        print("*", end= ' ', flush=True)
        x = x + 1