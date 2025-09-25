# run.py
import argparse
from src.environment import CityGrid
from src.agent import DeliveryAgent
from src.planners.uninformed import BFSPlanner, UniformCostPlanner
from src.planners.informed import AStarPlanner
from src.planners.local_search import SimulatedAnnealingPlanner
import time

def main():
    parser = argparse.ArgumentParser(description='Autonomous Delivery Agent')
    parser.add_argument('map_file', help='Path to map file')
    parser.add_argument('--algorithm', choices=['bfs', 'ucs', 'astar', 'sa'], 
                       default='astar', help='Planning algorithm')
    parser.add_argument('--fuel', type=int, default=100, help='Fuel capacity')
    parser.add_argument('--time-limit', type=int, default=1000, help='Time limit')
    
    args = parser.parse_args()
    
    # Load environment
    env = CityGrid(0, 0)  # Dimensions will be set by load_from_file
    env.load_from_file(args.map_file)
    
    # Create agent
    agent = DeliveryAgent(env, args.fuel, args.time_limit)
    
    # Select planner
    if args.algorithm == 'bfs':
        planner = BFSPlanner()
    elif args.algorithm == 'ucs':
        planner = UniformCostPlanner()
    elif args.algorithm == 'astar':
        planner = AStarPlanner()
    elif args.algorithm == 'sa':
        planner = SimulatedAnnealingPlanner()
    
    # Plan and execute
    start_time = time.time()
    path, cost, nodes_expanded = planner.plan(
        agent.current_position, env.depot, env, agent.time_step
    )
    planning_time = time.time() - start_time
    
    print(f"Algorithm: {args.algorithm}")
    print(f"Path cost: {cost}")
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Planning time: {planning_time:.4f}s")
    
    if path:
        agent.execute_plan(path)
        print(f"Packages delivered: {agent.delivered_packages}")
        print(f"Fuel remaining: {agent.fuel}")
        print(f"Time steps used: {agent.time_step}")
    else:
        print("No path found!")

if __name__ == "__main__":
    main()
