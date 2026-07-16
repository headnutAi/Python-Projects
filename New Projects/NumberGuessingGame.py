import random



if __name__ == '__main__':

    upper = input("Gib das obere ende ein:")
    lower = input("Gib das untere ende ein:")

    flag = random.randint(int(lower), int(upper))
    print(flag)
    chances = 7

    while chances >= 1:
        guess = input("Rate eine zahl zwischen " + upper + " und " + lower + ": ")

        match guess:
            case guess if int(guess) < flag:
                print("Die geratene Zahl ist kleiner als die gesuchte Zahl")
                chances -= 1
            case guess if int(guess) > flag:
                print("Die geratene Zahl ist groeßer als die gesuchte Zahl")
                chances -= 1
            case guess if int(guess) == flag:
                print("Du hast die Zahl erraten") 
                temp = 0

    print("Du hast verloren!")
    print("Die gesuchte zahl war: " + str(flag))

