import random
import numpy as np

name = input("Was ist dein Name? : ")
print("Viel Glück, " + name)

words = ['rainbow', 'computer', 'science', 'programming',
         'python', 'mathematics', 'player', 'condition',
         'reverse', 'water', 'board', 'geeks']
word = random.choice(words)
print(word)

tries = 12

guesses = np.full(len(word), "_", dtype='<U1')

print(guesses)

while tries > 0:
    guess = input("Guess a letter: ")

    if guess not in word:
        tries -= 1


    for index, c in enumerate(word):
        if c == guess:
            guesses[index] = c

    if "_" not in guesses:
        print("Du hast gewonnen!")

    print(guesses)

if tries == 0:
    print("Du hast verloren!")
