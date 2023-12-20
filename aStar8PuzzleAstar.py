class PuzzleNode:
    def __init__(self, state, parent=None, move=None, g_cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g_cost = g_cost
        self.h_cost = self.calculate_h_cost()
        self.f_cost = self.g_cost + self.h_cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def calculate_h_cost(self):
        h_cost = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:
                    goal_i, goal_j = divmod(self.state[i][j] - 1, 3)
                    h_cost += abs(i - goal_i) + abs(j - goal_j)
        return h_cost

def get_blank_pos(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def is_valid_move(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def get_neighbors(node):
    x, y = get_blank_pos(node.state)
    neighbors = []

#                  down,     up,   left,     right.
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = x + dx, y + dy
        if is_valid_move(new_x, new_y):
            new_state = [row[:] for row in node.state]
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            neighbors.append(PuzzleNode(new_state, node, (new_x, new_y), node.g_cost + 1))

    return neighbors

def a_star(initial_state, goal_state):
    start_node = PuzzleNode(initial_state)
    goal_node = PuzzleNode(goal_state)
    visited = set()
    priority_queue = []

    heapq.heappush(priority_queue, start_node)

    while priority_queue:
        current_node = heapq.heappop(priority_queue)

        if current_node.state == goal_node.state:
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            return path[::-1]

        if tuple(map(tuple, current_node.state)) not in visited:
            visited.add(tuple(map(tuple, current_node.state)))

            for neighbor in get_neighbors(current_node):
                if tuple(map(tuple, neighbor.state)) not in visited:
                    heapq.heappush(priority_queue, neighbor)

    return None  # No solution found
