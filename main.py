import os
from scheduler import Scheduler  # Assuming you have a Scheduler class

def get_user_choice():
    """Get scheduling choice from environment variable or user input."""
    choice = os.getenv("SCHEDULING_ALGORITHM")  # Read from environment variable

    if choice is None:  # If no environment variable, ask for input (only in interactive mode)
        try:
            print("Select a scheduling algorithm:")
            print("1. First-Come-First-Serve (FCFS)")
            print("2. Round Robin")
            print("3. Priority Scheduling")
            print("4. Shortest Job Next (SJN)")
            choice = input("Enter your choice (1-4): ")
        except EOFError:
            print("\nNo input detected. Defaulting to First-Come-First-Serve (FCFS).")
            choice = "1"  # Default to FCFS

    algorithms = {
        "1": "FCFS",
        "2": "Round Robin",
        "3": "Priority",
        "4": "SJN"
    }

    if choice not in algorithms:
        print("Invalid choice! Defaulting to First-Come-First-Serve (FCFS).")
        choice = "1"

    return algorithms[choice]

if __name__ == "__main__":
    algorithms_keys = ["1", "2", "3", "4"]
    algorithms_map = {
        "1": "FCFS",
        "2": "Round Robin",
        "3": "Priority",
        "4": "SJN"
    }

    for choice in algorithms_keys:
        algorithm = algorithms_map[choice]
        print(f"Running {algorithm} scheduling algorithm...\n")

        # Create the scheduler with 3 agents
        scheduler = Scheduler(num_agents=3)
        scheduler.run_scheduler(algorithm=algorithm)
        print("-" * 40) #seperator for each run