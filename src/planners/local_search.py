# src/planners/local_search.py
from src.agent import Planner
import random
import math

class SimulatedAnnealingPlanner(Planner):
    def __init__(self, max_iterations=1000, initial_temp=1000, cooling_rate=0.95):
        self.max_iterations = max_iterations
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
    
    def get_random_neighbor(self, path, environment, time_step):
        """Generate a neighbor by modifying the path"""
        if len(path) < 2:
            return path
        
        # Randomly modify a segment of the path
        new_path = path.copy()
        modification_point = random.randint(0, len(new_path) - 2)
        
        # Try to find an alternative route for a segment
        start = new_path[modification_point]
        goal = new_path[min(modification_point + 2, len(new_path) - 1)]
        
        # Use a simple method to find alternative
        alternatives = []
        x, y = start
        for (nx, ny), cost in environment.get_neighbors(x, y, time_step + modification_point):
            if (nx, ny) != new_path[modification_point + 1]:
                alternatives.append((nx, ny))
        
        if alternatives:
            new_path[modification_point + 1] = random.choice(alternatives)
        
        return new_path
    
    def calculate_path_cost(self, path, environment, time_step):
        total_cost = 0
        for i, (x, y) in enumerate(path):
            current_time = time_step + i
            if not environment.is_valid_position(x, y, current_time):
                return float('inf')
            total_cost += environment.grid[y][x].get_cost(current_time)
        return total_cost
    
    def plan(self, start, goal, environment, time_step=0, initial_path=None):
        # Start with a simple path (straight line or previous best)
        if initial_path is None:
            # Create a simple initial path using greedy approach
            current = start
            path = [start]
            while current != goal and len(path) < environment.width + environment.height:
                x, y = current
                neighbors = environment.get_neighbors(x, y, time_step + len(path))
                if not neighbors:
                    break
                # Choose neighbor closest to goal
                best_neighbor = min(neighbors, 
                                  key=lambda n: abs(n[0][0]-goal[0]) + abs(n[0][1]-goal[1]))
                current = best_neighbor[0]
                path.append(current)
        
        current_path = path
        current_cost = self.calculate_path_cost(current_path, environment, time_step)
        
        temperature = self.initial_temp
        best_path = current_path
        best_cost = current_cost
        nodes_expanded = 1
        
        for iteration in range(self.max_iterations):
            temperature *= self.cooling_rate
            if temperature < 1e-6:
                break
            
            # Generate neighbor
            neighbor_path = self.get_random_neighbor(current_path, environment, time_step)
            neighbor_cost = self.calculate_path_cost(neighbor_path, environment, time_step)
            nodes_expanded += 1
            
            # Accept better solution or worse with probability
            if neighbor_cost < current_cost or \
               random.random() < math.exp((current_cost - neighbor_cost) / temperature):
                current_path = neighbor_path
                current_cost = neighbor_cost
                
                if current_cost < best_cost:
                    best_path = current_path
                    best_cost = current_cost
        
        return best_path[1:], best_cost, nodes_expanded
