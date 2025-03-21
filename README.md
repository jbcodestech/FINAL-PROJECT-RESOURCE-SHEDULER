Resource Scheduler Documentation
1. Project Overview
The Resource Scheduler is a simulation system designed to optimize the allocation of employees (e.g., bank tellers or call center agents) to customer requests. The system minimizes customer wait times, maximizes resource utilization, and ensures fairness in task distribution. It integrates multiple scheduling algorithms, including:

First-Come-First-Serve (FCFS)

Round Robin (RR)

Priority Scheduling

Shortest Job Next (SJN)

The system simulates customer arrivals with randomized service times and priority levels, dynamically assigning agents to handle requests based on availability and workload capacity.

2. Features
Customer Simulation:

Customers arrive with randomized service times (5–15 minutes) and priority levels (VIP, Corporate, Normal).

Agent Allocation:

Agents are dynamically assigned to customers based on availability and workload capacity.

Scheduling Algorithms:

FCFS: Assigns tasks to the first available agent.

Round Robin: Assigns tasks in a cyclic order with a fixed time slice (e.g., 5 minutes).

Priority Scheduling: Assigns tasks based on customer priority (VIP > Corporate > Normal).

SJN: Assigns tasks with the shortest service time first.

Real-Time Monitoring:

Tracks agent availability and workload, updating status every 5 seconds.

Performance Metrics:

Measures average customer wait time, agent utilization rate, and fairness in task distribution.

3. Project Structure
Copy
resource-scheduler/
├─
│   ├── customer.py          # Customer class and logic
│   ├── agent.py             # Agent class and logic
│   ├── scheduler.py         # Scheduler class and scheduling algorithms
│   ├── app.py               # REST API implementation (optional)
│   └── main.py              # Main entry point for the application
├── tests/                   # Unit tests for the project
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration for containerization
├── docker-compose.yml       # Docker Compose configuration (optional)
├── .github/workflows/       # GitHub Actions CI/CD pipeline
│   └── ci-cd.yml
└── README.md                # Project documentation
4. Setup Instructions
4.1. Prerequisites
Python 3.9 or higher

Docker (optional, for containerization)

Git (optional, for version control)

The system will simulate customer arrivals and assign agents based on the selected algorithm.

5.2. REST API (Optional)
If the REST API is enabled, you can interact with the system using the following endpoints:

Generate a Customer: POST /generate_customer

bash
Copy
curl -X POST http://localhost:5000/generate_customer
Get Waiting Queue: GET /get_waiting_queue

bash
Copy
curl http://localhost:5000/get_waiting_queue
Get Agents Status: GET /get_agents_status


curl http://localhost:5000/get_agents_status
6. Scheduling Algorithms
6.1. First-Come-First-Serve (FCFS)
Tasks are assigned to the first available agent.

Simple and easy to implement.

6.2. Round Robin (RR)
Tasks are assigned in a cyclic order.

Each task is given a fixed time slice (e.g., 5 minutes).

If a task is not completed within the time slice, it is preempted and added back to the queue.

6.3. Priority Scheduling
Tasks are assigned based on customer priority (VIP > Corporate > Normal).

Ensures high-priority customers are served first.

6.4. Shortest Job Next (SJN)
Tasks with the shortest service time are assigned first.

Minimizes average wait time.

7. Performance Metrics
Average Customer Wait Time: Measures the average time customers spend waiting for service.

Agent Utilization Rate: Measures the percentage of time agents spend working versus being idle.

Fairness in Task Distribution: Ensures tasks are evenly distributed among agents.

8. Technical Details
8.1. Classes
Customer:

Attributes: customer_id, service_time, priority

Methods: __str__ (returns a string representation of the customer).

Agent:

Attributes: agent_id, workload_limit, current_workload, is_free

Methods: assign_task, finish_task.

Scheduler:

Attributes: agents, customers, waiting_queue, customer_counter, max_wait_time, time_slice

Methods: generate_customer, assign_customer, simulate_task_completion, process_waiting_queue, run_scheduler.

8.2. Threading
The system uses threading to simulate:

Customer arrivals.

Task execution with time slicing (for Round Robin).

Real-time monitoring of agent status.

8.3. Containerization
The application is containerized using Docker for easy deployment.

A Dockerfile and docker-compose.yml are provided for containerization.

9. CI/CD Pipeline
The project includes a GitHub Actions workflow to automate testing and deployment:

Build and test the application on every commit.

Push Docker images to Docker Hub.

Deploy the application to a cloud platform (e.g., Heroku, AWS).

10. Future Enhancements
GUI: Add a graphical user interface for better visualization.

Database Integration: Store customer and agent data in a database for persistence.

Advanced Metrics: Add more performance metrics (e.g., throughput, turnaround time).

Scalability: Optimize the system for large-scale simulations.

