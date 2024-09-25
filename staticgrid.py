import heapq

class Autobot:
    def __init__(self, start, end, grid):
        self.start = start
        self.end = end
        self.grid = grid
        self.position = start
        self.facing = 'up'  # Autobots start facing upward
        self.commands = []
    
    def is_valid_move(self, position):
        x, y = position
        if 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]):
            return self.grid[x][y] != 'X'  # Ensure it's not an obstacle
        return False

    def heuristic(self, a, b):
        # Manhattan distance heuristic for grid-based movement
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(self):
        # A* pathfinding algorithm to find the shortest path from start to end
        start, goal = self.start, self.end
        queue = []
        heapq.heappush(queue, (0, start))  # (priority, position)
        came_from = {start: None}
        cost_so_far = {start: 0}

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

        while queue:
            _, current = heapq.heappop(queue)

            if current == goal:
                break

            for direction in directions:
                next_position = (current[0] + direction[0], current[1] + direction[1])
                if self.is_valid_move(next_position):
                    new_cost = cost_so_far[current] + 1
                    if next_position not in cost_so_far or new_cost < cost_so_far[next_position]:
                        cost_so_far[next_position] = new_cost
                        priority = new_cost + self.heuristic(next_position, goal)
                        heapq.heappush(queue, (priority, next_position))
                        came_from[next_position] = current

        # Check if we reached the goal
        if goal not in came_from:
            print(f"No valid path from {start} to {goal}.")
            return []

        # Reconstruct path
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def get_direction(self, from_pos, to_pos):
        # Determine which direction to move based on two positions
        if to_pos[0] < from_pos[0]:  # Moving up
            return 'up'
        elif to_pos[0] > from_pos[0]:  # Moving down
            return 'down'
        elif to_pos[1] < from_pos[1]:  # Moving left
            return 'left'
        elif to_pos[1] > from_pos[1]:  # Moving right'
            return 'right'

    def turn_bot(self, desired_direction):
        turns = {
            ('up', 'left'): 'Left()',
            ('up', 'right'): 'Right()',
            ('up', 'down'): 'Right(), Right()',
            ('down', 'left'): 'Right()',
            ('down', 'right'): 'Left()',
            ('down', 'up'): 'Right(), Right()',
            ('left', 'up'): 'Right()',
            ('left', 'down'): 'Left()',
            ('left', 'right'): 'Right(), Right()',
            ('right', 'up'): 'Left()',
            ('right', 'down'): 'Right()',
            ('right', 'left'): 'Right(), Right()',
        }
        if self.facing == desired_direction:
            return None  # No turn needed
        command = turns[(self.facing, desired_direction)]
        self.facing = desired_direction  # Update the bot's direction after turning
        return command

    def move(self):
        path = self.a_star()
        if not path:
            self.commands.append("Wait()")  # Wait if no valid path
            return self.commands

        for i in range(len(path)):
            if i == 0:
                continue  # Skip the starting position
            prev_pos = path[i - 1]
            curr_pos = path[i]
            desired_direction = self.get_direction(prev_pos, curr_pos)
            
            # Turn if needed
            turn_command = self.turn_bot(desired_direction)
            if turn_command:
                self.commands.append(turn_command)
            
            # Move forward after turning in the correct direction
            self.commands.append("Forward()")
            
            # Force the bot to wait every two moves or at specific points (e.g., 'B1', 'B2')
            if i % 2 == 0 or self.grid[curr_pos[0]][curr_pos[1]] in ['B1', 'B2']:
                self.commands.append("Wait()")

        return self.commands

# Example grid
grid = [
    ['A1', '.', 'X', '.', 'B1'],
    ['.', 'X', '.', 'X', '.'],
    ['.', '.', '.', '.', '.'],
    ['X', 'X', '.', '.', 'X'],
    ['A2', '.', '.', '.', 'B2']
]

# Create autobots and simulate their movements
autobot1 = Autobot(start=(0, 0), end=(0, 4), grid=grid)
autobot2 = Autobot(start=(4, 0), end=(0, 4), grid=grid)

# Simulate movements
commands1 = autobot1.move()
commands2 = autobot2.move()

# Print results
print("Autobot 1 commands:", commands1)
print("Autobot 2 commands:", commands2)
