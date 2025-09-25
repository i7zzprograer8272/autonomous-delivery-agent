# src/utils.py
import json
import time
from datetime import datetime

def save_results(algorithm, map_name, path_cost, nodes_expanded, planning_time, 
                 delivered_packages, fuel_remaining, time_steps):
    """Save experimental results to JSON file"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'algorithm': algorithm,
        'map_name': map_name,
        'path_cost': path_cost,
        'nodes_expanded': nodes_expanded,
        'planning_time': planning_time,
        'delivered_packages': delivered_packages,
        'fuel_remaining': fuel_remaining,
        'time_steps': time_steps
    }
    
    filename = f"results_{algorithm}_{map_name}_{int(time.time())}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    return filename

def load_map_template(width, height, obstacle_density=0.2):
    """Generate random map template"""
    import random
    
    grid = []
    for y in range(height):
        row = []
        for x in range(height):
            if random.random() < obstacle_density:
                row.append('X')  # Obstacle
            else:
                # Random terrain cost 1-3
                row.append(str(random.randint(1, 3)))
        grid.append(''.join(row))
    
    # Set start and depot
    grid[0] = 'S' + grid[0][1:]
    grid[-1] = grid[-1][:-1] + 'D'
    
    return grid

def visualize_path(grid, path, current_pos):
    """Visualize the grid with agent path"""
    visualization = []
    path_set = set(path)
    
    for y, row in enumerate(grid):
        vis_row = []
        for x, cell in enumerate(row):
            if (x, y) == current_pos:
                vis_row.append('A')  # Agent
            elif (x, y) in path_set:
                vis_row.append('*')  # Path
            else:
                vis_row.append(cell)
        visualization.append(''.join(vis_row))
    
    return '\n'.join(visualization)

def compare_algorithms(results):
    """Compare multiple algorithm results"""
    print("\n" + "="*80)
    print("ALGORITHM COMPARISON")
    print("="*80)
    print(f"{'Algorithm':<12} {'Cost':<8} {'Nodes':<8} {'Time(s)':<10} {'Packages':<10} {'Fuel':<8}")
    print("-"*80)
    
    for result in results:
        print(f"{result['algorithm']:<12} {result['path_cost']:<8} "
              f"{result['nodes_expanded']:<8} {result['planning_time']:<10.4f} "
              f"{result['delivered_packages']:<10} {result['fuel_remaining']:<8}")

def create_dynamic_obstacle_schedule(width, height, steps=20):
    """Create a moving obstacle schedule"""
    # Simple horizontal movement pattern
    path = []
    for step in range(steps):
        x = step % width
        y = height // 2
        path.append((x, y))
    return path
