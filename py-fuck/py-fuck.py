import sys


class State:
    def __init__(self):
        self.array = [0]
        self.pointer = 0

    @property
    def value(self):
        return self.array[self.pointer]

    @value.setter
    def value(self, val):
        self.array[self.pointer] = val % 256

    def __repr__(self):
        return str(self.pointer) + str(self.array)


class Action:
    def __init__(self, function, arg=None):
        self.function = function
        self.arg = arg

    def __call__(self, string, state):
        return self.function(string, state, self.arg)


def split_string(string):
    ''' Splits the string head:tail where head is the first character of the
    string which is in the language and tail is the rest of the string.
    Used to ignore non-language characters such as comments or whitespace '''
    index = 0
    while string[index] not in'<>+-,.[]':
        index += 1
    return string[index], string[index + 1:]

def move_pointer(tail, state, arg):
    ''' Moves the pointer by 'arg' units, resizes the array approprietly. '''
    state.pointer += arg
    if state.pointer < 0:
        raise IndexError('Decremented a pointer of value 0')
    if state.pointer >= len(state.array):
        state.array.append(0)

def change_value(tail, state, arg):
    ''' Adds 'arg' to the value at the current pointer. '''
    state.value += arg

def print_value(tail, state, arg):
    ''' Prints the current value, converting it to a character. '''
    print(chr(state.value), end='')
    
def read_value(tail, state, arg):
    ''' Reads value trough stdin. '''
    state.value = int(input())

def loop(tail, state, arg):
    ''' Loops the string between both [] until the current value becomes 0. '''
    def closing_brace_index(tail):
        ''' Gets the index of the corresponding closing bracket. '''
        depth, index = 1, 0
        while depth > 0:
            if index >= len(tail):
                raise SyntaxError('Mismatched "["')
            current = tail[index]
            if current == '[':
                depth += 1
            elif current == ']':
                depth -= 1
            index += 1
        return index

    index = closing_brace_index(tail)
    while state.value > 0:
       interpret(tail[:index-1], state)
    return tail[index:]

def closing_bracket(string, state, arg):
    pass

ACTIONS = {'>': Action(move_pointer, 1), 
           '<': Action(move_pointer, -1), 
           '+': Action(change_value, 1), 
           '-': Action(change_value, -1), 
           '.': Action(print_value, None), 
           ',': Action(read_value, None), 
           '[': Action(loop, None), 
           ']': Action(closing_bracket, None), }

def interpret(string, state):
    ''' Interprets the string as a brainfuck program, storing the state.
    It uses a dict ACTIONS to emulate a switch-case. '''
    head, tail = split_string(string)
    tail = ACTIONS[head](tail, state) or tail
        
    if tail:
        interpret(tail, state)

if __name__ == '__main__':
    interpret(sys.argv[1], State())
