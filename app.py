from flask import Flask, render_template, request, jsonify
from customer import Customer
from agent import Agent
import time
import threading
from queue import Queue
app = Flask(__name__)
class Scheduler:
    def __init__(self, num_agents=3, max_wait_time=20, time_slice=5):
        self.agents = [Agent(i) for i in range(num_agents)]  # Create agents
        self.customers = Queue()  # Queue for incoming customers
        self.waiting_queue = Queue()  # Queue for waiting customers
        self.customer_counter = 0  # Track customer IDs
        self.max_wait_time = max_wait_time  # Maximum wait time for customers
        self.time_slice = time_slice  # Fixed time slice for Round Robin (in seconds)
        self.max_customers = 5  # Fixed number of customers to generate
        self.customer_waiting_times = {}  # Track waiting time for each customer
        self.agent_working_time = [0] * num_agents  # Track working time for each agent
        self.start_time = time.time()  # Track the start time of the simulation

    def generate_customer(self):
        # Simulate customer arrivals
        while self.customer_counter < self.max_customers:
            self.customer_counter += 1
            new_customer = Customer(self.customer_counter)
            self.customers.put(new_customer)  # Add customer to the incoming queue
            self.customer_waiting_times[new_customer.customer_id] = time.time()  # Record arrival time
            print(f"New Customer {new_customer.customer_id} arrived with service time {new_customer.service_time} mins.")
            time.sleep(5)  # Simulate 5 seconds between customer arrivals
        print("All customers have been generated.")

    def assign_customer(self, customer, algorithm):
        # Assign customer based on the selected algorithm
        if algorithm == "FCFS":
            self.assign_fcfs(customer)
        elif algorithm == "Round Robin":
            self.assign_round_robin(customer)
        elif algorithm == "Priority":
            self.assign_priority(customer)
        elif algorithm == "SJN":
            self.assign_sjn(customer)
        else:
            print("Invalid algorithm selected.")

    def assign_fcfs(self, customer):
        # Assign to the first available agent
        available_agents = [agent for agent in self.agents if agent.is_free]
        if available_agents:
            assigned_agent = available_agents[0]
            assigned_agent.assign_task(customer)
            self.customer_waiting_times[customer.customer_id] = time.time() - self.customer_waiting_times[customer.customer_id]  # Calculate waiting time
            threading.Thread(target=self.simulate_task_completion, args=(assigned_agent, customer.service_time)).start()
        else:
            print(f"No agents available. Customer {customer.customer_id} added to the waiting queue.")
            self.waiting_queue.put(customer)  # Add customer to the waiting queue

    def assign_round_robin(self, customer):
        # Assign tasks to agents in a round-robin fashion with time slicing
        available_agents = [agent for agent in self.agents if agent.is_free]
        if available_agents:
            assigned_agent = available_agents[0]
            assigned_agent.assign_task(customer)
            self.customer_waiting_times[customer.customer_id] = time.time() - self.customer_waiting_times[customer.customer_id]  # Calculate waiting time
            threading.Thread(target=self.simulate_round_robin_task, args=(assigned_agent, customer)).start()
        else:
            print(f"No agents available. Customer {customer.customer_id} added to the waiting queue.")
            self.waiting_queue.put(customer)  # Add customer to the waiting queue

    def simulate_round_robin_task(self, agent, customer):
        # Simulate the time taken to complete the task with time slicing
        print(f"Agent {agent.agent_id} is working on Customer {customer.customer_id} for {self.time_slice} seconds...")
        time.sleep(self.time_slice * 10)  # Convert seconds to seconds
        self.agent_working_time[agent.agent_id] += self.time_slice  # Track working time

        # Check if the task is completed
        if customer.service_time <= self.time_slice:
            print(f"Customer {customer.customer_id} has completed their task.")
            agent.finish_task()
        else:
            # Preempt the task and add it back to the waiting queue
            customer.service_time -= self.time_slice
            print(f"Customer {customer.customer_id} has been preempted. Remaining service time: {customer.service_time} mins.")
            self.waiting_queue.put(customer)
            agent.finish_task()

        # Process the waiting queue after task completion
        self.process_waiting_queue()

    def assign_priority(self, customer):
        # Assign tasks based on customer priority (VIP > Corporate > Normal)
        available_agents = [agent for agent in self.agents if agent.is_free]
        if available_agents:
            assigned_agent = available_agents[0]
            assigned_agent.assign_task(customer)
            self.customer_waiting_times[customer.customer_id] = time.time() - self.customer_waiting_times[customer.customer_id]  # Calculate waiting time
            threading.Thread(target=self.simulate_task_completion, args=(assigned_agent, customer.service_time)).start()
        else:
            print(f"No agents available. Customer {customer.customer_id} added to the waiting queue.")
            self.waiting_queue.put(customer)  # Add customer to the waiting queue

    def assign_sjn(self, customer=None): #customer is now optional
        # Assign tasks with the shortest service time first
        available_agents = [agent for agent in self.agents if agent.is_free]

        if customer:
            self.customer_waiting_times[customer.customer_id] = time.time()  # Record arrival time
            self.customers.put(customer)

        if available_agents:
            all_customers = list(self.customers.queue) + list(self.waiting_queue.queue)

            if all_customers:
                shortest_customer = min(all_customers, key=lambda x: x.service_time)

                if shortest_customer in list(self.customers.queue):
                    self.customers.queue.remove(shortest_customer)
                elif shortest_customer in list(self.waiting_queue.queue):
                    self.waiting_queue.queue.remove(shortest_customer)

                assigned_agent = available_agents[0]
                assigned_agent.assign_task(shortest_customer)
                self.customer_waiting_times[shortest_customer.customer_id] = time.time() - self.customer_waiting_times[shortest_customer.customer_id]  # Calculate waiting time
                threading.Thread(target=self.simulate_task_completion_sjn, args=(assigned_agent, shortest_customer.service_time)).start()
            else:
                pass # no customers to assign
        else:
            self.process_waiting_queue_sjn() # check for jobs after task completion
    def simulate_task_completion_sjn(self, agent, service_time):
        # Simulate the time taken to complete the task
        print(f"Agent {agent.agent_id} is working on a task for {service_time} seconds...")
        time.sleep(service_time * 10)  # Convert seconds to seconds
        self.agent_working_time[agent.agent_id] += service_time  # Track working time
        agent.finish_task()
        self.assign_sjn() # Re-trigger SJN after task completion
    def simulate_task_completion(self, agent, service_time):
        # Simulate the time taken to complete the task
        print(f"Agent {agent.agent_id} is working on a task for {service_time} seconds...")
        time.sleep(service_time * 5)  # Convert seconds to seconds
        self.agent_working_time[agent.agent_id] += service_time  # Track working time
        agent.finish_task()
        self.process_waiting_queue()  # Check for waiting customers after task completion

    def process_waiting_queue_sjn(self):
        # Assign waiting customers to available agents using SJN
        available_agents = [agent for agent in self.agents if agent.is_free]
        all_customers = list(self.customers.queue) + list(self.waiting_queue.queue)
        if all_customers and available_agents: #Only run if there are available agents.
            self.assign_sjn() #re-run sjn to check for next shortest job.    def process_waiting_queue(self):
        # Assign waiting customers to available agents
        while not self.waiting_queue.empty():
            available_agents = [agent for agent in self.agents if agent.is_free]
            if available_agents:
                next_customer = self.waiting_queue.get()
                print(f"Assigning waiting Customer {next_customer.customer_id} to an agent.")
                self.assign_customer(next_customer, algorithm="FCFS")  # Use FCFS for waiting queue
            else:
                break
    def process_waiting_queue(self):
        # Assign waiting customers to available agents
        while not self.waiting_queue.empty():
            available_agents = [agent for agent in self.agents if agent.is_free]
            if available_agents:
                next_customer = self.waiting_queue.get()
                print(f"Assigning waiting Customer {next_customer.customer_id} to an agent.")
                self.assign_customer(next_customer, algorithm="FCFS")  # Use FCFS for waiting queue
            else:
                break

    def calculate_performance_metrics(self):
        # Calculate average waiting time
        total_waiting_time = sum(self.customer_waiting_times.values())
        average_waiting_time = total_waiting_time / self.max_customers

        # Calculate agent utilization rate
        total_simulation_time = time.time() - self.start_time
        agent_utilization_rate = [working_time / total_simulation_time * 100 for working_time in self.agent_working_time]

        # Print performance metrics
        print("\nPerformance Metrics:")
        print(f"Average Customer Waiting Time: {average_waiting_time:.2f} seconds")
        print("Agent Utilization Rates:")
        for i, rate in enumerate(agent_utilization_rate):
            print(f"Agent {i}: {rate:.2f}%")

    def run_scheduler(self, algorithm="FCFS"):
        # Start customer generation in a separate thread
        threading.Thread(target=self.generate_customer, daemon=True).start()

        # Continuously assign customers to agents
        while True:
            if not self.customers.empty():
                current_customer = self.customers.get()
                self.assign_customer(current_customer, algorithm)
            elif self.customer_counter >= self.max_customers and self.customers.empty() and self.waiting_queue.empty():
                # Check if all agents are free
                all_agents_free = all(agent.is_free for agent in self.agents)
                if all_agents_free:
                    print("All tasks completed. Exiting scheduler.")
                    self.calculate_performance_metrics()  # Calculate and print performance metrics
                    break
            time.sleep(1)  # Reduce sleep time for better responsiveness
scheduler = Scheduler()  # Create a single instance of the scheduler
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        algorithm = request.form['algorithm']
        threading.Thread(target=scheduler.run_scheduler, args=(algorithm,)).start()
        return render_template('index.html', message="Scheduler started with " + algorithm + " algorithm.")
    return render_template('index.html')

@app.route('/status')
def status():
    agent_status = []
    for agent in scheduler.agents:
        if agent.current_task:
            task_id = agent.current_task.customer_id
        else:
            task_id = None
        agent_status.append({"id": agent.agent_id, "free": agent.is_free, "task": task_id})

    customer_queues = {
        "customers": [customer.customer_id for customer in scheduler.customers.queue],
        "waiting_queue": [customer.customer_id for customer in scheduler.waiting_queue.queue]
    }
    performance = {
      "customer_waiting_times": scheduler.customer_waiting_times,
      "agent_working_times": scheduler.agent_working_time,
      "start_time": scheduler.start_time,
      "max_customers": scheduler.max_customers
    }
    return jsonify({"agents": agent_status, "queues": customer_queues, "performance": performance})

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=8080, debug=True)
