import math

from matplotlib import pyplot as plt
from py4j.java_gateway import JavaGateway
import numpy as np
import pyswarms as ps
from pyswarms.utils.plotters import plot_cost_history

gateway = JavaGateway()

cloud_sim_runner = gateway.entry_point.getCloudSimRunner()

def fitness_function(x):
    fitness = []
    max_execution_time = 1

    for i, vm_config in enumerate(x):
        cpus = round(vm_config[0])
        ram = round(vm_config[1]*1000)

        try:
            execution_time = cloud_sim_runner.runSimulation(cpus, ram)
            if np.isnan(execution_time):
                execution_time = np.inf
        except Exception as e:
            print(f"Error in simulation: {e}")
            execution_time = np.inf

        if max_execution_time < execution_time:
            max_execution_time = execution_time

        # Normalize execution time
        normalized_execution_time = execution_time / math.sqrt(max_execution_time)
        # Calculate total resource usage
        total_resource_usage = cpus + ram / 1000
        fitness_value = (0.7 * normalized_execution_time) + (0.3 * total_resource_usage)
        fitness.append(fitness_value)

    return np.array(fitness)


# Define the bounds for vmPes and ram
options = {'c1': 0.5, 'c2': 0.4, 'w': 0.9}
max_bound = 20 * np.ones(2)
min_bound = 1 * np.ones(2)
bounds = (min_bound, max_bound)

# Initialize the PSO
optimizer = ps.single.GlobalBestPSO(n_particles=120, dimensions=2, options=options, bounds=bounds)

# Perform the optimization
cost, pos = optimizer.optimize(fitness_function, iters=500)
gateway.close()
optimal_cpus = round(pos[0])
optimal_ram = round(pos[1])*1000

# Run the simulation with the optimal configuration to get the execution time
try:
    final_execution_time = cloud_sim_runner.runSimulation(optimal_cpus, optimal_ram)
except Exception as e:
    print(f"Error in final simulation: {e}")
    final_execution_time = None

print("Optimal VM configuration: vCPUs =", optimal_cpus, ", Memory =", optimal_ram, "MB")
print("Minimum execution time:", cost)
print("Final execution time with optimal configuration:", final_execution_time)

# Plot the cost
plot_cost_history(optimizer.cost_history)
plt.show()
