import random
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

        if goal not in came_from:
            print(f"No valid path from {start} to {goal}.")
            return []

        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def get_direction(self, from_pos, to_pos):
        if to_pos[0] < from_pos[0]:
            return 'up'
        elif to_pos[0] > from_pos[0]:
            return 'down'
        elif to_pos[1] < from_pos[1]:
            return 'left'
        elif to_pos[1] > from_pos[1]:
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
            self.commands.append("Wait()")
            return self.commands

        for i in range(len(path)):
            if i == 0:
                continue  # Skip the starting position
            prev_pos = path[i - 1]
            curr_pos = path[i]
            desired_direction = self.get_direction(prev_pos, curr_pos)
            
            turn_command = self.turn_bot(desired_direction)
            if turn_command:
                self.commands.append(turn_command)
            
            self.commands.append("Forward()")
            
            if i % 2 == 0 or self.grid[curr_pos[0]][curr_pos[1]] in ['B1', 'B2']:
                self.commands.append("Wait()")

        return self.commands

# Function to generate a random grid
def generate_random_grid(rows, cols, obstacle_prob=0.2):
    grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if random.random() < obstacle_prob:
                row.append('X')  # Obstacle
            else:
                row.append('.')  # Empty space
        grid.append(row)
    return grid

# Function to create autobots and set their positions based on user input
def create_autobots(num_autobots, grid):
    autobots = []
    for i in range(1, num_autobots + 1):
        print(f"\nEnter start and end positions for Autobot {i}:")
        start_x = int(input(f"Start row for Autobot {i} (0 to {len(grid)-1}): "))
        start_y = int(input(f"Start column for Autobot {i} (0 to {len(grid[0])-1}): "))
        end_x = int(input(f"End row for Autobot {i} (0 to {len(grid)-1}): "))
        end_y = int(input(f"End column for Autobot {i} (0 to {len(grid[0])-1}): "))
        
        start = (start_x, start_y)
        end = (end_x, end_y)
        grid[start_x][start_y] = f'A{i}'
        grid[end_x][end_y] = f'B{i}'
        autobots.append(Autobot(start=start, end=end, grid=grid))
    return autobots

# Get user input for grid size and number of Autobots
rows = int(input("Enter the number of rows for the grid: "))
cols = int(input("Enter the number of columns for the grid: "))
num_autobots = int(input("Enter the number of Autobots: "))

# Generate the grid and Autobots
random_grid = generate_random_grid(rows, cols)
autobots = create_autobots(num_autobots, random_grid)

# Print the generated grid
print("\nGenerated Grid:")
for row in random_grid:
    print(' '.join(row))

# Simulate movements for each Autobot
for i, autobot in enumerate(autobots, 1):
    print(f"\nAutobot {i} commands:")
    commands = autobot.move()
    print(commands)
