import random
import simpy
import matplotlib.pyplot as plt

# Lists to store data for plotting
arrival_times = []
wait_times = []
service_times = []
total_times = []

def customer(env, name, counter):
    arrival_time = env.now
    arrival_times.append(arrival_time)
    with counter.request() as request:
        yield request
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        service_time = random.expovariate(1.0 / 40)
        service_times.append(service_time)
        yield env.timeout(service_time)
        total_time = wait_time + service_time
        total_times.append(total_time)

def setup(env, num_counters, arrival_rate):
    counter = simpy.Resource(env, num_counters)
    i = 0
    while i < 10000:
        inter_arrival_time = max(0, random.normalvariate(1/arrival_rate, 1))  # Normal distribution with mean 1/arrival_rate and std deviation 1
        yield env.timeout(inter_arrival_time)
        i += 1
        env.process(customer(env, f'Customer {i}', counter))

# Run the simulation
random.seed(42)
env = simpy.Environment()
env.process(setup(env, num_counters=3, arrival_rate=1/20))
env.run(until=env.now + 10000)

# Calculate averages
average_wait_time = sum(wait_times) / len(wait_times)
average_service_time = sum(service_times) / len(service_times)
average_total_time = sum(total_times) / len(total_times)

print(f'Average wait time: {average_wait_time}')
print(f'Average service time: {average_service_time}')
print(f'Average total time (from queuing to receiving package): {average_total_time}')

# Plot all 3 averages on the same graph
plt.figure(figsize=(10, 6))
plt.bar(['Average Total Time', 'Average Wait Time', 'Average Service Time'], 
    [average_total_time, average_wait_time, average_service_time], 
    color=['blue', 'orange', 'green'])
plt.ylabel('Time')
plt.title('Average Times')
plt.show()

# Plot the results
plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.plot(arrival_times, label='Arrival Times')
plt.xlabel('Customer')
plt.ylabel('Time')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(wait_times, label='Wait Times', color='orange')
plt.xlabel('Customer')
plt.ylabel('Time')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(service_times, label='Service Times', color='green')
plt.xlabel('Customer')
plt.ylabel('Time')
plt.legend()

plt.tight_layout()
plt.show()
