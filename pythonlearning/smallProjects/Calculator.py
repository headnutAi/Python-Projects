import math
from typing import Any

user_input: str = input("Please enter a number 1 : ")
first_number: int = int(user_input)
user_input: str = input("Please enter a number 2 : ")
second_number: int = int(user_input)

user_input: str = input("Do you want to add,subtract,multiply or divide? : ")
user_wish: str = user_input

result : int


def calculating(x : int, y : int, case : str) -> Any | None:
    match case:
        case "add":
            return x + y
        case "subtract":
            return x - y
        case "multiply":
            return x * y
        case "divide":

            if x or y == 0:
                return 'dont use 0 when you divide'
            else:
                return x / y
    return 'Wrong input'

print(calculating(first_number, second_number, user_wish))