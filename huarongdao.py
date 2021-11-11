#!/usr/bin/python3

import argparse
import copy
import heapq
import sys
import time

# parse arguments
parser = argparse.ArgumentParser()

parser.add_argument('--id', type = int, default = 1,
                    help='Input file, 1 for puzzle1.txt and 2 for puzzle2.txt')

parser.add_argument('--algorithm', type = str, default = "astar", 
                    help='Search algorithms, options: astar, dfs')

args = parser.parse_args()

output_file = open('puzzle'+str(args.id)+'sol_'+args.algorithm+'.txt', 'w')
# end of parse arguments

def read_puzzle(id):
    with open('puzzle'+str(id)+'.txt') as input:
        return list(map(list, input.read().splitlines()))

def is_goal(state):
    return state.heuristic == 0

def get_cost(state):
    return state.cost

def get_heuristic(state):
    return state.heuristic

def get_successors(state):
    return state.generate_successors()

def a_star(initial_state):
    frontier = Priorityq()
    search(initial_state, frontier)

def dfs(initial_state):
    frontier = Stack()
    search(initial_state, frontier)

def generate_blocks_list(state):
    blocks = []
    explored = [[False] * 4 for i in range(5)]
    for row in range(5):
        for col in range(4):
            c = state[row][col]
            if c == '0' or explored[row][col] == True:
                continue
            width = 1
            height = 1
            if c != '7':
                width = 1 + ((col + 1 in range(4)) and (state[row][col+1] == c))
                height = 1 + ((row + 1 in range(5)) and (state[row+1][col] == c))
            for brow in range(height):
                for bcol in range(width):
                    explored[row+brow][col+bcol] = True
            b = [row, col, width, height, c]
            blocks.append(b)
    return blocks

def search(initial_state, frontier):
    explored = set()
    goal_state = None

    frontier.add(initial_state)
    while not frontier.empty():
        state = frontier.pop()
        if state.key in explored:
            continue
        explored.add(state.key)
        if is_goal(state):
            goal_state = state
            break
        else:
            for s in get_successors(state):
                frontier.add(s)

    print('Cost of the solution: ' + str(get_cost(goal_state)), file=output_file)
    print('', file=output_file)
    print('Number of states expanded: ' + str(len(explored)), file=output_file)
    print('', file=output_file)
    print('Solution:', file = output_file)
    print('', file=output_file)
    goal_state.print_path()

class Priorityq:
    def __init__(self):
        self.pqueue = []
        self.keys = set()
        self.count = 0
    def add(self, state):
        if state.key not in self.keys:
            heapq.heappush(self.pqueue, (get_heuristic(state) + state.cost, state))
            self.keys.add(state.key)
            self.count += 1
    def pop(self):
        cost, state = heapq.heappop(self.pqueue)
        self.keys.remove(state.key)
        return state
    def empty(self):
        return len(self.pqueue) == 0

class Stack:
    def __init__(self):
        self.stack = []
        self.keys = set()
        self.count = 0
    def add(self, state):
        if state.key not in self.keys:
            self.stack.append(state)
            self.keys.add(state.key)
            self.count += 1
    def pop(self):
        state = self.stack.pop()
        self.keys.remove(state.key)
        return state
    def empty(self):
        return len(self.stack) == 0

# row, col, width, height, char

class State:
    def __init__(self, state, blocks, parent=None):
        self.state = [ele[:] for ele in state] # list of list, containing state layout
        self.parent = parent # parent state, passed by reference
        self.cost = 0 if parent is None else (parent.cost + 1) # f(n)
        self.blocks = [x[:] for x in blocks] # list of list, containing info
        if parent is None:
            self.calc_key()
            self.calc_heu()

    def __eq__(self, other):
        return other != None and self.state == other.state

    def __lt__(self, other):
        return self.heuristic < other.heuristic

    def __str__(self):
        return str(self.cost) + '\n' + \
                str.join('\n', [str.join('', e) for e in self.state]) + '\n'
    
    # print current state to the console
    def print(self):
        print(self, file=output_file)

    def print_path(self):
        path = []
        state = self
        while state is not None:
            path.append(str(state))
            state = state.parent
        for s in reversed(path):
            print(s, file=output_file)
    
    def update_puzzle(self, p_old, p_new):
        self.blocks.remove(p_old)
        self.blocks.append(p_new)

        # row col width height char
        for h in range(p_old[3]):
            for w in range(p_old[2]):
                self.state[p_old[0] + h][p_old[1] + w] = '0'

        for h in range(p_new[3]):
            for w in range(p_new[2]):
                self.state[p_new[0] + h][p_new[1] + w] = p_new[4]
        self.calc_key()
        self.calc_heu()
    
    def calc_heu(self):
        for block in self.blocks:
            if block[4] == '1':
                row = block[0]
                col = block[1]
        self.heuristic = abs(row - 3) + abs(col - 1)
        # kinds = set()
        # count = 0
        # for i in range(3,5):
        #     for j in range(1,3):
        #         c = self.state[i][j]
        #         if  c == '7':
        #             if '7' in kinds:
        #                 count += 1
        #             else:
        #                 kinds.add('7')
        #         elif c != '1' and c != '0':
        #             kinds.add(c)
        # self.heuristic = len(kinds) + count + self.heuristic
    
    def calc_key(self):
        types = [['0'] * 4 for i in range(5)]
        for block in self.blocks:
            b_type = str((2 - block[2]) * 2 + (2 - block[3]) + 1)
            for h in range(block[3]):
                for w in range(block[2]):
                    types[block[0] + h][block[1] + w] = b_type
        self.key = int(str.join('', [str.join('', e) for e in types]))

    # return list of successors
    def generate_successors(self):
        successors = []
        for b in self.blocks:
            for direction in ["up", "down", "left", "right"]:
                successor = self.move_one_block(b, direction)
                if successor != None:
                    successors.append(successor)
        return successors
    # return new state if moved success, return None otherwise
    def move_one_block(self, b, direction):
        if direction in ["up", "down"]:
            if direction == "up":
                r = b[0] - 1
            elif direction == "down":
                r = b[0] + b[3]
            if r not in range(5):
                return None
            for c in range(b[2]):
                if self.state[r][b[1]+c] != '0':
                    return None
            new_block = [b[0] - 1 if direction == "up" else b[0] + 1, b[1], b[2], b[3], b[4]]

        if direction in ["left", "right"]:
            if direction == "left":
                c = b[1] - 1
            elif direction == "right":
                c = b[1] + b[2]
            if c not in range(4):
                return None
            for r in range(b[3]):
                if self.state[b[0]+r][c] != '0':
                    return None
            new_block = [b[0], b[1] - 1 if direction == "left" else b[1] + 1, b[2], b[3], b[4]]
        new_state = State(self.state, self.blocks, self)
        new_state.update_puzzle(b, new_block)
        return new_state

if __name__ == '__main__':
    method = {"astar": a_star, "dfs": dfs}

    state = read_puzzle(args.id)
    blocks = generate_blocks_list(state)
    initial_state = State(state, blocks)

    print('Initial state:', file=output_file)
    print(str(str.join('\n', [str.join('', e) for e in initial_state.state]) + '\n'), file=output_file)

    method[args.algorithm](initial_state)