# test_runner.py
import subprocess
import json
import glob
from src.utils import compare_algorithms

def run_comprehensive_tests():
    """Run all algorithms on all maps and compare results"""
    maps = ['small.map', 'medium.map', 'large.map', 'dynamic.map']
    algorithms = ['bfs', 'ucs', 'astar', 'sa']
    
    all_results = []
    
    for map_name in maps:
        print(f"\n{'='*60}")
        print(f"TESTING MAP: {map_name}")
        print(f"{'='*60}")
        
        map_results = []
        for algorithm in algorithms:
            print(f"\nRunning {algorithm} on {map_name}...")
            
            # Run the algorithm
            result = subprocess.run([
                'python', 'run.py', 
                f'maps/{map_name}', 
                '--algorithm', algorithm,
                '--fuel', '200'
            ], capture_output=True, text=True)
            
            # Parse output
            output = result.stdout
            print(output)
            
            # Extract metrics (you'd need to modify run.py to return structured data)
            metrics = {
                'algorithm': algorithm,
                'map_name': map_name,
                'path_cost': extract_metric(output, 'Path cost:'),
                'nodes_expanded': extract_metric(output, 'Nodes expanded:'),
                'planning_time': extract_metric(output, 'Planning time:'),
                'delivered_packages': extract_metric(output, 'Packages delivered:'),
                'fuel_remaining': extract_metric(output, 'Fuel remaining:')
            }
            
            map_results.append(metrics)
            all_results.append(metrics)
        
        compare_algorithms(map_results)
    
    return all_results

def extract_metric(output, keyword):
    """Extract numeric value from output line"""
    for line in output.split('\n'):
        if keyword in line:
            try:
                return float(line.split(':')[-1].strip())
            except:
                return 0
    return 0

if __name__ == "__main__":
    results = run_comprehensive_tests()
    
    # Save comprehensive results
    with open('comprehensive_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nAll tests completed! Results saved to comprehensive_results.json")
