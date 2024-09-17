from py4j.java_gateway import JavaGateway


def linear_normalizer(x, min_of_x, range_of_x):
    normalized_value = (x - min_of_x) / range_of_x

    return normalized_value


def resource_normalizer(min_ram_in_mb, max_ram_in_mb, min_vcpus, max_vcpus, current_):
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

# Fixed normalization parameters
min_vcpus = 1
min_ram_in_mb = 1000
max_bound = 20
max_ram_in_mb = max_bound * 1000
max_vcpus = max_bound

# Current resource utilization
current_vcpus = 3
current_ram_in_mb = 4300

# Execution Time Normalizer
max_execution_time = cloud_sim_runner.runSimulation(min_vcpus, min_ram_in_mb)
min_execution_time = cloud_sim_runner.runSimulation(max_vcpus, max_ram_in_mb)

range_of_execution_time = max_execution_time - min_execution_time

execution_time = cloud_sim_runner.runSimulation(current_vcpus, current_ram_in_mb)

execution_time_normalized = (execution_time - min_execution_time) / range_of_execution_time
print("max_execution_time=" + str(max_execution_time))
print("min_execution_time=" + str(min_execution_time))

print("execution_time=" + str(execution_time))
print("min=" + str(min_execution_time))
print("max=" + str(max_execution_time))
print("normalized=" + str(execution_time_normalized))

print("------------------------------------------")

# Ressource Normalizer
max_resources = (max_ram_in_mb / 1000) + max_vcpus
min_resources = (min_ram_in_mb / 1000) + min_vcpus
range_resources = max_resources - min_resources
resources = (current_ram_in_mb / 1000) + current_vcpus

resources_normalized = (resources - min_resources) / range_resources
print("max_resources=" + str(max_resources))
print("min_resources=" + str(min_resources))
print("range_resources=" + str(range_resources))
print("resources=" + str(resources))
print("resources_normalized=" + str(resources_normalized))




