# src/agent.py
from abc import ABC, abstractmethod
from collections import deque
import heapq
import random
import time

class DeliveryAgent:
    def __init__(self, environment, fuel_capacity=100, time_limit=1000):
        self.env = environment
        self.fuel = fuel_capacity
        self.time_limit = time_limit
        self.current_position = environment.agent_start
        self.path = []
        self.time_step = 0
        self.delivered_packages = 0
    
    def execute_plan(self, plan):
        """Execute a planned path"""
        for next_pos in plan:
            if self.fuel <= 0 or self.time_step >= self.time_limit:
                break
            self.move_to(next_pos)
    
    def move_to(self, position):
        x, y = position
        if self.env.is_valid_position(x, y, self.time_step):
            cost = self.env.grid[y][x].get_cost(self.time_step)
            self.fuel -= cost
            self.current_position = position
            self.time_step += 1
            self.path.append(position)
            
            # Check if package delivered
            if position == self.env.depot:
                self.delivered_packages += 1
            return True
        return False

class Planner(ABC):
    @abstractmethod
    def plan(self, start, goal, environment, time_step=0):
        pass
