# demo_dynamic.py
from src.environment import CityGrid
from src.agent import DeliveryAgent
from src.planners.informed import AStarPlanner
from src.planners.local_search import SimulatedAnnealingPlanner
import time

def demo_dynamic_obstacles():
    print("DEMONSTRATING DYNAMIC OBSTACLE HANDLING")
    print("="*50)
    
    # Load dynamic map
    env = CityGrid(0, 0)
    env.load_dynamic_map('maps/dynamic.map')
    
    # Create agent
    agent = DeliveryAgent(env, fuel_capacity=200)
    
    # Initial plan with A*
    planner = AStarPlanner()
    path, cost, nodes = planner.plan(agent.current_position, env.depot, env)
    
    print(f"Initial plan: {len(path)} steps, cost: {cost}")
    
    # Simulate execution with dynamic obstacles appearing
    steps_executed = 0
    for i, position in enumerate(path[:10]):  # Execute first 10 steps
        if agent.move_to(position):
            steps_executed += 1
            print(f"Step {i}: Moved to {position}")
            
            # Simulate dynamic obstacle appearing at step 5
            if i == 5:
                print("!!! DYNAMIC OBSTACLE APPEARED !!!")
                # Add a new dynamic obstacle
                env.grid[position[1]][position[0]].dynamic_obstacle = \
                    DynamicObstacle(position, 'circular')
    
    # Replan with local search
    print("\nReplanning with Simulated Annealing...")
    sa_planner = SimulatedAnnealingPlanner()
    new_path, new_cost, new_nodes = sa_planner.plan(
        agent.current_position, env.depot, env, agent.time_step, path[i+1:]
    )
    
    print(f"New plan: {len(new_path)} steps, cost: {new_cost}")
    
    # Continue execution
    agent.execute_plan(new_path)
    print(f"Delivery completed! Packages: {agent.delivered_packages}")

if __name__ == "__main__":
    demo_dynamic_obstacles()
