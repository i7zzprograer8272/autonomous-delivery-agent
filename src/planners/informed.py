# src/planners/informed.py
from src.agent import Planner
import heapq

class AStarPlanner(Planner):
    def __init__(self, heuristic='manhattan'):
        self.heuristic = heuristic
    
    def calculate_heuristic(self, a, b):
        x1, y1 = a
        x2, y2 = b
        if self.heuristic == 'manhattan':
            return abs(x1 - x2) + abs(y1 - y2)
        elif self.heuristic == 'euclidean':
            return ((x1 - x2)**2 + (y1 - y2)**2)**0.5
        else:
            return 0
    
    def plan(self, start, goal, environment, time_step=0):
        open_set = []
        heapq.heappush(open_set, (0, 0, start, [start]))  # (f, g, position, path)
        
        g_costs = {start: 0}
        visited = set()
        nodes_expanded = 0
        
        while open_set:
            f, g, current, path = heapq.heappop(open_set)
            nodes_expanded += 1
            
            if current == goal:
                return path[1:], g, nodes_expanded
            
            if current in visited:
                continue
            visited.add(current)
            
            x, y = current
            current_time = time_step + len(path) - 1
            
            for (nx, ny), move_cost in environment.get_neighbors(x, y, current_time):
                neighbor = (nx, ny)
                new_g = g + move_cost
                new_path = path + [neighbor]
                
                if neighbor not in g_costs or new_g < g_costs[neighbor]:
                    g_costs[neighbor] = new_g
                    h = self.calculate_heuristic(neighbor, goal)
                    f = new_g + h
                    heapq.heappush(open_set, (f, new_g, neighbor, new_path))
        
        return None, float('inf'), nodes_expanded
