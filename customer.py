import random

class Customer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.service_time = random.randint(5, 15)  # Random service time between 5-15 mins
        self.priority = random.choice(['VIP', 'Corporate', 'Normal'])

    def __str__(self):
        return f"Customer {self.customer_id} | Priority: {self.priority} | Service Time: {self.service_time} mins"