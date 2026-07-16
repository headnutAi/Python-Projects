a, b = 10, 'fifteen'

try:
    print(a+b)
except TypeError as e:
    print(f'something went wrong', {e})
except EOFError as e:
    print(f'something else went wrong', {e})