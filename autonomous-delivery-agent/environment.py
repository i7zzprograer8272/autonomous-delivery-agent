# src/environment.py (enhanced)
class DynamicObstacle:
    def __init__(self, start_pos, movement_pattern, speed=1):
        self.start_pos = start_pos
        self.movement_pattern = movement_pattern  # 'horizontal', 'vertical', 'circular'
        self.speed = speed
        self.positions = self._generate_positions(100)  # Pre-generate 100 steps
    
    def _generate_positions(self, steps):
        positions = []
        x, y = self.start_pos
        
        for step in range(steps):
            if self.movement_pattern == 'horizontal':
                new_x = (x + step) % 20  # Assuming max width 20
                new_y = y
            elif self.movement_pattern == 'vertical':
                new_x = x
                new_y = (y + step) % 20
            elif self.movement_pattern == 'circular':
                radius = 3
                new_x = x + int(radius * math.cos(step * 0.5))
                new_y = y + int(radius * math.sin(step * 0.5))
            else:
                new_x, new_y = x, y
            
            positions.append((new_x, new_y))
        
        return positions
    
    def is_occupied(self, time_step):
        if time_step < len(self.positions):
            return self.positions[time_step]
        return self.positions[-1]  # Stay at last position

class CityGrid:
    # ... existing code ...
    
    def load_dynamic_map(self, filename):
        """Load map with dynamic obstacles marked with 'D'"""
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        self.height = len(lines)
        self.width = len(lines[0])
        self.grid = [[GridCell() for _ in range(self.width)] for _ in range(self.height)]
        self.dynamic_obstacles = []
        
        obstacle_id = 0
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == 'X':
                    self.grid[y][x].is_obstacle = True
                elif char.isdigit():
                    self.grid[y][x].terrain_cost = int(char)
                elif char == 'S':
                    self.agent_start = (x, y)
                elif char == 'D':
                    self.grid[y][x].dynamic_obstacle = DynamicObstacle(
                        (x, y), 'horizontal' if obstacle_id % 2 == 0 else 'vertical'
                    )
                    obstacle_id += 1
