import random
import heapq
import math

# Constants
IDLE = 0
BUSY = 1
Q_LIMIT = 100  # Maximum queue length

# Input Parameters (to be read from a file in real use)
mean_interarrival = 1.0  # Mean time between arrivals
mean_service = 0.5       # Mean service time
num_delays_required = 10  # Number of customers to process

# Simulation variables
sim_time = 0.0
server_status = IDLE
num_in_q = 0
num_custs_delayed = 0
total_of_delays = 0.0
area_num_in_q = 0.0
area_server_status = 0.0
time_last_event = 0.0

# Event list (priority queue)
event_list = []

# Queue (FIFO)
queue = []

# Exponential distribution function
def expon(mean):
    return -mean * math.log(1.0 - random.random())

# Schedule the first arrival
heapq.heappush(event_list, (sim_time + expon(mean_interarrival), "arrival"))

def timing():
    """Determines the next event."""
    global sim_time
    if not event_list:
        print(f"Event list empty at time {sim_time}")
        exit(1)

    # Get the next event from priority queue
    event_time, event_type = heapq.heappop(event_list)
    sim_time = event_time
    return event_type

def arrive():
    """Handles arrival events."""
    global server_status, num_in_q, num_custs_delayed, total_of_delays

    # Schedule next arrival
    heapq.heappush(event_list, (sim_time + expon(mean_interarrival), "arrival"))

    if server_status == BUSY:
        if num_in_q >= Q_LIMIT:
            print(f"Queue overflow at time {sim_time}")
            exit(2)
        queue.append(sim_time)  # Store arrival time
        num_in_q += 1
    else:
        # Server is idle, process immediately
        delay = 0.0
        total_of_delays += delay
        num_custs_delayed += 1
        server_status = BUSY

        # Schedule departure
        heapq.heappush(event_list, (sim_time + expon(mean_service), "departure"))

def depart():
    """Handles departure events."""
    global server_status, num_in_q, num_custs_delayed, total_of_delays

    if num_in_q == 0:
        server_status = IDLE  # No customers in queue
    else:
        num_in_q -= 1
        arrival_time = queue.pop(0)
        delay = sim_time - arrival_time
        total_of_delays += delay
        num_custs_delayed += 1

        # Schedule next departure
        heapq.heappush(event_list, (sim_time + expon(mean_service), "departure"))

def update_time_avg_stats():
    """Updates time-average statistics."""
    global area_num_in_q, area_server_status, time_last_event
    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    area_num_in_q += num_in_q * time_since_last_event
    area_server_status += server_status * time_since_last_event

def report():
    """Prints the simulation report."""
    print(f"\nSimulation results after {num_custs_delayed} customers:")
    print(f"Average delay in queue: {total_of_delays / num_custs_delayed:.4f}")
    print(f"Average number in queue: {area_num_in_q / sim_time:.4f}")
    print(f"Server utilization: {area_server_status / sim_time:.4f}")
    print(f"Simulation ended at time: {sim_time:.4f}")

# Main simulation loop
while num_custs_delayed < num_delays_required:
    next_event = timing()
    update_time_avg_stats()

    if next_event == "arrival":
        arrive()
    elif next_event == "departure":
        depart()

# Output results
report()
