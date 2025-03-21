class Agent:
    def __init__(self, agent_id, workload_limit=1):  # Add workload_limit as parameter
        self.agent_id = agent_id
        self.is_free = True
        self.current_task = None
        self.current_workload = 0  # Initialize current_workload
        self.workload_limit = workload_limit #set workload limit

    def assign_task(self, customer):
        if self.current_workload < self.workload_limit:
            self.current_task = customer
            self.is_free = False
            self.current_workload += 1
        else:
            print(f"Agent {self.agent_id} is at max workload")

    def finish_task(self):
        self.current_task = None
        self.is_free = True
        self.current_workload -= 1
        if self.current_workload < 0:
            self.current_workload = 0