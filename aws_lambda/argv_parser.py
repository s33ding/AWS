import sys

def get_input(message='Please enter a value: '):
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return input(message)
