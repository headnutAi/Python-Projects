import random
from collections import Counter


import numpy as np
from websockets.cli import send_outgoing_messages

someWords = '''apple banana mango strawberry 
orange grape pineapple apricot lemon coconut watermelon 
cherry papaya berry peach lychee muskmelon'''

someWords = someWords.split(' ')

word = random.choice(someWords)

stages = [
'''
  -----
  |   |
      |
      |
      |
      |
---------
''',
'''
  -----
  |   |
  O   |
      |
      |
      |
---------
''',
'''
  -----
  |   |
  O   |
  |   |
      |
      |
---------
''',
'''
  -----
  |   |
  O   |
 /|   |
      |
      |
---------
''',
'''
  -----
  |   |
  O   |
 /|\\  |
      |
      |
---------
''',
'''
  -----
  |   |
  O   |
 /|\\  |
 /    |
      |
---------
''',
'''
  -----
  |   |
  O   |
 /|\\  |
 / \\  |
      |
---------
'''
]

guesses = np.full(len(word), "_", dtype='<U1')
print(word)
if __name__ == '__main__':

    tries = len(stages)
    flag = 0
    stagecounter = 0

    while tries > 0 and flag == 0:
        print(guesses)

        userinput = input("Rate einen Buchstaben: ")

        if userinput not in word:
            tries -= 1
            print(stages[stagecounter])
            stagecounter += 1
        else:
            for index, char in enumerate(word):
                if char == userinput:
                    guesses[index] = char

        if "_" not in guesses:
            flag = 1
            print("Du hast gewonnen")

    if tries == 0:
        print(f"Du hast verloren das wort war : {word}")













