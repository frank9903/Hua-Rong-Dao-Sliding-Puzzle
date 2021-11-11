from queue import PriorityQueue # retrived from: https://dbader.org/blog/priority-queues-in-python
import copy


class Node:
    def __init__(self, state, parent, cost, h):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.h = h
    
    def __gt__(self, node1):
        return False

def read_puzzle(id):
    if (id == 1):
        with open("puzzle1.txt", "r") as input:
            return list(map(list, input.read().splitlines()))
    
    if (id == 2):
        with open("puzzle2.txt", "r") as input:
            return list(map(list, input.read().splitlines()))

def is_goal(state):
    return state[3][1] == "1" and state[3][2] == "1" and state[4][1] == "1" and state[4][2] == "1"

def get_successors(state):
    idx1 = []
    idx2 = []
    successors = []

    for i in range(5):
        for j in range(4):
            if state[i][j] == "0":
                if (len(idx1) == 0):
                    idx1 = [i ,j]
                else:
                    idx2 = [i ,j]
                    break
        if (len(idx2) != 0):
            break

    # special cases 
    if (idx1[0] == idx2[0] and abs(idx1[1]-idx2[1]) == 1): # 00 horizontal
        if (idx1[0] - 1 > -1 and state[idx1[0]-1][idx1[1]] == "6" and state[idx1[0]-1][idx2[1]] == "6"):
            new_state = copy.deepcopy(state)
            new_state[idx1[0]][idx1[1]] = "6"
            new_state[idx2[0]][idx2[1]] = "6"
            new_state[idx1[0]-1][idx1[1]] = "0"
            new_state[idx1[0]-1][idx2[1]] = "0"
            successors.append(new_state)
        if (idx1[0] + 1 < 5 and state[idx1[0]+1][idx1[1]] == "6" and state[idx1[0]+1][idx2[1]] == "6"):
            new_state = copy.deepcopy(state)
            new_state[idx1[0]][idx1[1]] = "6"
            new_state[idx2[0]][idx2[1]] = "6"
            new_state[idx1[0]+1][idx1[1]] = "0"
            new_state[idx1[0]+1][idx2[1]] = "0"
            successors.append(new_state)
        if (idx1[0] - 1 > -1 and state[idx1[0]-1][idx1[1]] == "1" and state[idx1[0]-1][idx2[1]] == "1"):
            new_state = copy.deepcopy(state)
            new_state[idx1[0]][idx1[1]] = "1"
            new_state[idx2[0]][idx2[1]] = "1"
            new_state[idx1[0]-2][idx1[1]] = "0"
            new_state[idx1[0]-2][idx2[1]] = "0"
            successors.append(new_state)
        if (idx1[0] + 1 < 5 and state[idx1[0]+1][idx1[1]] == "1" and state[idx1[0]+1][idx2[1]] == "1"):
            new_state = copy.deepcopy(state)
            new_state[idx1[0]][idx1[1]] = "1"
            new_state[idx2[0]][idx2[1]] = "1"
            new_state[idx1[0]+2][idx1[1]] = "0"
            new_state[idx1[0]+2][idx2[1]] = "0"
            successors.append(new_state)
    elif (idx1[1] == idx2[1] and abs(idx1[0]-idx2[0]) == 1): # vertical
        if (idx1[1] - 1 > -1 and state[idx1[0]][idx1[1]-1] in list("2345") and state[idx2[0]][idx1[1]-1]==state[idx1[0]][idx1[1]-1]):
            new_state = copy.deepcopy(state)
            new_state[idx1[0]][idx1[1]] = state[idx1[0]][idx1[1]-1]
            new_state[idx2[0]][idx2[1]] = state[idx1[0]][idx1[1]-1]
            new_state[idx1[0]][idx1[1]-1] = "0"
            new_state[idx2[0]][idx1[1]-1] = "0"
            successors.append(new_state)
        if (idx1[1] + 1 < 4 and state[idx1[0]][idx1[1]+1] in list("2345") and state[idx2[0]][idx1[1]+1]==state[idx1[0]][idx1[1]+1]):
            new_state = copy.deepcopy(state)
            new_state[idx1[0]][idx1[1]] = state[idx1[0]][idx1[1]+1]
            new_state[idx2[0]][idx2[1]] = state[idx1[0]][idx1[1]+1]
            new_state[idx1[0]][idx1[1]+1] = "0"
            new_state[idx2[0]][idx1[1]+1] = "0"
            successors.append(new_state)
        if (idx1[1] - 1 > -1 and state[idx1[0]][idx1[1]-1] == "1" and state[idx2[0]][idx1[1]-1] == "1"):
            new_state = copy.deepcopy(state)
            new_state[idx1[0]][idx1[1]] = "1"
            new_state[idx2[0]][idx2[1]] = "1"
            new_state[idx1[0]][idx1[1]-2] = "0"
            new_state[idx2[0]][idx1[1]-2] = "0"
            successors.append(new_state)
        if (idx1[1] + 1 < 4 and state[idx1[0]][idx1[1]+1] == "1" and state[idx2[0]][idx1[1]+1] == "1"):
            new_state = copy.deepcopy(state)
            new_state[idx1[0]][idx1[1]] = "1"
            new_state[idx2[0]][idx2[1]] = "1"
            new_state[idx1[0]][idx1[1]+2] = "0"
            new_state[idx2[0]][idx1[1]+2] = "0"
            successors.append(new_state)
    
    # normal cases
    if (idx1[0]-1 > -1 and state[idx1[0]-1][idx1[1]] == "7"):
        new_state = copy.deepcopy(state)
        new_state[idx1[0]][idx1[1]] = "7"
        new_state[idx1[0]-1][idx1[1]] = "0"
        successors.append(new_state)
    if (idx2[0]-1 > -1 and state[idx2[0]-1][idx2[1]] == "7"):
        new_state = copy.deepcopy(state)
        new_state[idx2[0]][idx2[1]] = "7"
        new_state[idx2[0]-1][idx2[1]] = "0"
        successors.append(new_state)
    if (idx1[0]+1 < 5 and state[idx1[0]+1][idx1[1]] == "7"):
        new_state = copy.deepcopy(state)
        new_state[idx1[0]][idx1[1]] = "7"
        new_state[idx1[0]+1][idx1[1]] = "0"
        successors.append(new_state)
    if (idx2[0]+1 < 5 and state[idx2[0]+1][idx2[1]] == "7"):
        new_state = copy.deepcopy(state)
        new_state[idx2[0]][idx2[1]] = "7"
        new_state[idx2[0]+1][idx2[1]] = "0"
        successors.append(new_state)
    if (idx1[1]-1 > -1 and state[idx1[0]][idx1[1]-1] == "7"):
        new_state = copy.deepcopy(state)
        new_state[idx1[0]][idx1[1]] = "7"
        new_state[idx1[0]][idx1[1]-1] = "0"
        successors.append(new_state)
    if (idx2[1]-1 > -1 and state[idx2[0]][idx2[1]-1] == "7"):
        new_state = copy.deepcopy(state)
        new_state[idx2[0]][idx2[1]] = "7"
        new_state[idx2[0]][idx2[1]-1] = "0"
        successors.append(new_state)
    if (idx1[1]+1 < 4 and state[idx1[0]][idx1[1]+1] == "7"):
        new_state = copy.deepcopy(state)
        new_state[idx1[0]][idx1[1]] = "7"
        new_state[idx1[0]][idx1[1]+1] = "0"
        successors.append(new_state)
    if (idx2[1]+1 < 4 and state[idx2[0]][idx2[1]+1] == "7"):
        new_state = copy.deepcopy(state)
        new_state[idx2[0]][idx2[1]] = "7"
        new_state[idx2[0]][idx2[1]+1] = "0"
        successors.append(new_state)

    if (idx1[1]-1 > -1 and state[idx1[0]][idx1[1]-1] == "6"):
        new_state = copy.deepcopy(state)
        new_state[idx1[0]][idx1[1]] = "6"
        new_state[idx1[0]][idx1[1]-2] = "0"
        successors.append(new_state)
    if (idx2[1]-1 > -1 and state[idx2[0]][idx2[1]-1] == "6"):
        new_state = copy.deepcopy(state)
        new_state[idx2[0]][idx2[1]] = "6"
        new_state[idx2[0]][idx2[1]-2] = "0"
        successors.append(new_state)
    if (idx1[1]+1 < 4 and state[idx1[0]][idx1[1]+1] == "6"):
        new_state = copy.deepcopy(state)
        new_state[idx1[0]][idx1[1]] = "6"
        new_state[idx1[0]][idx1[1]+2] = "0"
        successors.append(new_state)
    if (idx2[1]+1 < 4 and state[idx2[0]][idx2[1]+1] == "6"):
        new_state = copy.deepcopy(state)
        new_state[idx2[0]][idx2[1]] = "6"
        new_state[idx2[0]][idx2[1]+2] = "0"
        successors.append(new_state)

    if (idx1[0]-1 > -1 and state[idx1[0]-1][idx1[1]] in list("2345")):
        new_state = copy.deepcopy(state)
        new_state[idx1[0]][idx1[1]] = state[idx1[0]-1][idx1[1]]
        new_state[idx1[0]-2][idx1[1]] = "0"
        successors.append(new_state)
    if (idx2[0]-1 > -1 and state[idx2[0]-1][idx2[1]] in list("2345")):
        new_state = copy.deepcopy(state)
        new_state[idx2[0]][idx2[1]] = state[idx2[0]-1][idx2[1]]
        new_state[idx2[0]-2][idx2[1]] = "0"
        successors.append(new_state)
    if (idx1[0]+1 < 5 and state[idx1[0]+1][idx1[1]] in list("2345")):
        new_state = copy.deepcopy(state)
        new_state[idx1[0]][idx1[1]] = state[idx1[0]+1][idx1[1]]
        new_state[idx1[0]+2][idx1[1]] = "0"
        successors.append(new_state)
    if (idx2[0]+1 < 5 and state[idx2[0]+1][idx2[1]] in list("2345")):
        new_state = copy.deepcopy(state)
        new_state[idx2[0]][idx2[1]] = state[idx2[0]+1][idx2[1]]
        new_state[idx2[0]+2][idx2[1]] = "0"
        successors.append(new_state)
    
    return successors

def get_cost(node):
    return node.cost

def get_heuristic(state):
    idx1 = []

    for i in range(5):
        for j in range(4):
            if state[i][j] == "1":
                idx1 = [i ,j]
                break
        if (len(idx1) != 0):
            break
    
    return abs(idx1[0] - 3) + abs(idx1[1] - 1)

def transform(state):
    new_state = copy.deepcopy(state)
    for i in range(5):
        for j in range(4):
            if new_state[i][j] in list("2345"):
                new_state[i][j] = "9"
    return new_state

def a_star(initial_state):
    frontier = PriorityQueue()
    visited = []
    goal_node = 0

    cur_state = initial_state
    cost = 0
    h = get_heuristic(cur_state)
    successors = get_successors(cur_state)
    cur_node = Node(cur_state, "NULL", cost, h)
    frontier.put((h+cost, cur_node))
    while not frontier.empty():
        cur_node = frontier.get()[1]
        # for i in cur_node.state:
        #     print(i)
        # print("-------------------------------")
        cur_state = cur_node.state
        transformed = transform(cur_state)
        if transformed in visited:
            continue
        visited.append(transformed)
        if is_goal(cur_state):
            goal_node = cur_node
            break
        else:
            for s in get_successors(cur_state):
                # for i in s:
                #     print(i)
                temp = Node(s, cur_node, cur_node.cost+1, get_heuristic(s))
                # print(temp.cost)
                # print(temp.h)
                frontier.put((temp.cost+temp.h, temp))
    
    return goal_node, len(visited)

def dfs(initial_state):
    frontier = []
    visited = []
    goal_node = 0

    cur_state = initial_state
    cost = 0
    h = get_heuristic(cur_state)
    successors = get_successors(cur_state)
    cur_node = Node(cur_state, "NULL", cost, h)
    frontier.append(cur_node)
    while not (len(frontier) == 0):
        cur_node = frontier.pop()
        # for i in cur_node.state:
        #     print(i)
        # print("-------------------------------")
        cur_state = cur_node.state
        transformed = transform(cur_state)
        if transformed in visited:
            continue
        visited.append(transformed)
        if is_goal(cur_state):
            goal_node = cur_node
            break
        else:
            for s in get_successors(cur_state):
                # for i in s:
                #     print(i)
                temp = Node(s, cur_node, cur_node.cost+1, get_heuristic(s))
                # print(temp.cost)
                # print(temp.h)
                frontier.append(temp)
    
    return goal_node, len(visited)
        

if __name__ == "__main__":
    initial_state1 = read_puzzle(1)
    initial_state2 = read_puzzle(2)
    goal1, num1 = a_star(initial_state1)
    goal2, num2 = a_star(initial_state2)
    output_file1 = open("puzzle1sol_astar.txt", "w")
    output_file2 = open("puzzle2sol_astar.txt", "w")
    print("Initial state:", file=output_file1)
    print(str("\n".join(["".join(i) for i in initial_state1]) + "\n"), file=output_file1)
    print("Cost of the solution: " + str(goal1.cost) + "\n", file=output_file1)
    print("Number of states expanded: " + str(num1) + "\n", file=output_file1)
    print("Solution: \n", file=output_file1)
    path = []
    cur_node = goal1
    while (cur_node != "NULL"):
        string = str(cur_node.cost) + "\n" + str("\n".join(["".join(i) for i in cur_node.state])) + "\n"
        path.insert(0, string)
        cur_node = cur_node.parent
    print("\n".join(path), file=output_file1)

    print("Initial state:", file=output_file2)
    print(str("\n".join(["".join(i) for i in initial_state2]) + "\n"), file=output_file2)
    print("Cost of the solution: " + str(goal2.cost) + "\n", file=output_file2)
    print("Number of states expanded: " + str(num2) + "\n", file=output_file2)
    print("Solution: \n", file=output_file2)
    path = []
    cur_node = goal2
    while (cur_node != "NULL"):
        string = str(cur_node.cost) + "\n" + str("\n".join(["".join(i) for i in cur_node.state])) + "\n"
        path.insert(0, string)
        cur_node = cur_node.parent
    print("\n".join(path), file=output_file2)

    goal3, num3 = dfs(initial_state1)
    goal4, num4 = dfs(initial_state2)
    output_file3 = open("puzzle1sol_dfs.txt", "w")
    output_file4 = open("puzzle2sol_dfs.txt", "w")
    print("Initial state:", file=output_file3)
    print(str("\n".join(["".join(i) for i in initial_state1]) + "\n"), file=output_file3)
    print("Cost of the solution: " + str(goal3.cost) + "\n", file=output_file3)
    print("Number of states expanded: " + str(num3) + "\n", file=output_file3)
    print("Solution: \n", file=output_file3)
    path = []
    cur_node = goal3
    while (cur_node != "NULL"):
        string = str(cur_node.cost) + "\n" + str("\n".join(["".join(i) for i in cur_node.state])) + "\n"
        path.insert(0, string)
        cur_node = cur_node.parent
    print("\n".join(path), file=output_file3)

    print("Initial state:", file=output_file4)
    print(str("\n".join(["".join(i) for i in initial_state2]) + "\n"), file=output_file4)
    print("Cost of the solution: " + str(goal4.cost) + "\n", file=output_file4)
    print("Number of states expanded: " + str(num4) + "\n", file=output_file4)
    print("Solution: \n", file=output_file4)
    path = []
    cur_node = goal4
    while (cur_node != "NULL"):
        string = str(cur_node.cost) + "\n" + str("\n".join(["".join(i) for i in cur_node.state])) + "\n"
        path.insert(0, string)
        cur_node = cur_node.parent
    print("\n".join(path), file=output_file4)