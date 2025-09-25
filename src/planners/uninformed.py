# src/planners/uninformed.py
from src.agent import Planner
from collections import deque
import heapq

class BFSPlanner(Planner):
    def plan(self, start, goal, environment, time_step=0):
        queue = deque([(start, [start], 0)])  # (position, path, cost)
        visited = set([start])
        nodes_expanded = 0
        
        while queue:
            current, path, cost = queue.popleft()
            nodes_expanded += 1
            
            if current == goal:
                return path[1:], cost, nodes_expanded  # Exclude start position
            
            x, y = current
            for (nx, ny), move_cost in environment.get_neighbors(x, y, time_step + len(path)):
                neighbor = (nx, ny)
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor], cost + move_cost))
        
        return None, float('inf'), nodes_expanded

class UniformCostPlanner(Planner):
    def plan(self, start, goal, environment, time_step=0):
        priority_queue = [(0, start, [start])]  # (cost, position, path)
        visited = {}
        nodes_expanded = 0
        
        while priority_queue:
            cost, current, path = heapq.heappop(priority_queue)
            nodes_expanded += 1
            
            if current == goal:
                return path[1:], cost, nodes_expanded
            
            if current in visited and visited[current] <= cost:
                continue
            visited[current] = cost
            
            x, y = current
            for (nx, ny), move_cost in environment.get_neighbors(x, y, time_step + len(path)):
                neighbor = (nx, ny)
                new_cost = cost + move_cost
                new_path = path + [neighbor]
                
                if neighbor not in visited or new_cost < visited[neighbor]:
                    heapq.heappush(priority_queue, (new_cost, neighbor, new_path))
        
        return None, float('inf'), nodes_expanded
