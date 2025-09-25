# src/environment.py
class GridCell:
    def __init__(self, terrain_cost=1, is_obstacle=False, dynamic_obstacle=None):
        self.terrain_cost = terrain_cost
        self.is_obstacle = is_obstacle
        self.dynamic_obstacle = dynamic_obstacle  # Moving obstacle schedule
    
    def get_cost(self, time_step):
        if self.is_obstacle:
            return float('inf')
        if self.dynamic_obstacle and self.dynamic_obstacle.is_occupied(time_step):
            return float('inf')
        return self.terrain_cost

class DynamicObstacle:
    def __init__(self, path, speed=1):
        self.path = path  # List of (x,y) positions over time
        self.speed = speed
        self.current_step = 0
    
    def is_occupied(self, time_step):
        if time_step >= len(self.path):
            # Loop or stay at final position
            final_pos = self.path[-1]
            return self.path[time_step % len(self.path)] == final_pos
        return self.path[time_step] if time_step < len(self.path) else self.path[-1]

class CityGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[GridCell() for _ in range(width)] for _ in range(height)]
        self.packages = []
        self.agent_start = (0, 0)
        self.depot = (width-1, height-1)
    
    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == 'X':  # Static obstacle
                    self.grid[y][x].is_obstacle = True
                elif char.isdigit():  # Terrain cost
                    self.grid[y][x].terrain_cost = int(char)
                elif char == 'S':  # Start
                    self.agent_start = (x, y)
                elif char == 'D':  # Depot
                    self.depot = (x, y)
    
    def is_valid_position(self, x, y, time_step=0):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return self.grid[y][x].get_cost(time_step) < float('inf')
    
    def get_neighbors(self, x, y, time_step=0):
        neighbors = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:  # 4-connected
            nx, ny = x + dx, y + dy
            if self.is_valid_position(nx, ny, time_step):
                cost = self.grid[ny][nx].get_cost(time_step)
                neighbors.append(((nx, ny), cost))
        return neighbors
