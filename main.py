import math
from matplotlib import pyplot as plt
import numpy as np
import pyswarms as ps
from pyswarms.utils.plotters import plot_cost_history
from py4j.java_gateway import JavaGateway


def linear_normalizer(x, min_of_x, range_of_x):
    normalized_value = (x - min_of_x) / range_of_x

    return normalized_value


def resource_normalizer(min_ram_in_mb, max_ram_in_mb, current_ram_in_mb, min_vcpus, max_vcpus, current_vcpus):
    max_resources = (max_ram_in_mb / 1000) + max_vcpus
    min_resources = (min_ram_in_mb / 1000) + min_vcpus
    range_resources = max_resources - min_resources
    resources = (current_ram_in_mb / 1000) + current_vcpus
    resources_normalized = linear_normalizer(resources, min_resources, range_resources)

    return resources_normalized


def execution_time_normalizer(min_ram_in_mb, max_ram_in_mb, min_vcpus, max_vcpus, current_vcpus, current_ram_in_mb):
    max_execution_time = cloud_sim_runner.runSimulation(min_vcpus, min_ram_in_mb)
    min_execution_time = cloud_sim_runner.runSimulation(max_vcpus, max_ram_in_mb)
    range_of_execution_time = max_execution_time - min_execution_time
    execution_time = cloud_sim_runner.runSimulation(current_vcpus, current_ram_in_mb)
    execution_time_normalized = linear_normalizer(execution_time, min_execution_time, range_of_execution_time)

    return execution_time_normalized


gateway = JavaGateway()

cloud_sim_runner = gateway.entry_point.getCloudSimRunner()
min_vcpus = 1
min_ram_in_mb = 1
max_bound = 20
max_ram_in_mb = max_bound*1000
max_vcpus = max_bound

max_execution_time = cloud_sim_runner.runSimulation(min_vcpus, min_ram_in_mb)

def fitness_function(x):
    fitness = []

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

        # Normalize execution time
        normalized_execution_time = execution_time / math.sqrt(max_execution_time)
        # Calculate total resource usage
        total_resource_usage = cpus + ram / 1000
        fitness_value = (1.7 * normalized_execution_time) + (0.3 * total_resource_usage)
        fitness.append(fitness_value)

    return np.array(fitness)


# Define the bounds for vmPes and ram
options = {'c1': 0.5, 'c2': 0.5, 'w': 0.9}
max_bound = 20 * np.ones(2)
min_bound = 1 * np.ones(2)
bounds = (min_bound, max_bound)

# Initialize the PSO
optimizer = ps.single.GlobalBestPSO(n_particles=120, dimensions=2, options=options, bounds=bounds)

# Perform the optimization
cost, pos = optimizer.optimize(fitness_function, iters=200)
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
