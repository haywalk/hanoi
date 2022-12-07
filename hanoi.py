'''
Towers of Hanoi Solver
Hayden Walker (www.haywalk.ca)
2022-12-06
'''

def move(states, stacks, number, stack_from, stack_to):
    # base case: one item to move
    if number == 1:
        stacks[stack_to].append(stacks[stack_from].pop())
        states.append([[j for j in stacks[i]] for i in range(3)])

    # recursive case: more than one item to move
    else:
        aux_stack = 3 - stack_from - stack_to
        move(states, stacks, number - 1, stack_from, aux_stack)
        move(states, stacks, 1, stack_from, stack_to)
        move(states, stacks, number - 1, aux_stack, stack_to)

def hanoi(size):
    # generate the stacks
    stacks = [[] for i in range(3)]
    stacks[0] = [size - i for i in range(size)]

    # save initial state
    states = [[[j for j in stacks[i]] for i in range(3)]]

    # move the stack and return list of states
    move(states, stacks, size, 0, 1)
    return states

if __name__ == '__main__':
    size = int(input('stack size: '))

    for state in hanoi(size):
        print(state)

