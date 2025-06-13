import sys

# Import your modules
from page_replacement.fifo import FIFO
from page_replacement.lru import LRU
from page_replacement.optimal import Optimal
from page_replacement.visualize import visualize_page_replacement

from scheduling.fcfs import FCFS
from scheduling.sjf import SJF
from scheduling.round_robin import RoundRobin
from scheduling.visualize import visualize_scheduling

from memory_management.first_fit import FirstFit
from memory_management.best_fit import BestFit
from memory_management.visualize import visualize_memory_allocation

from deadlock.detection import DeadlockDetection
from deadlock.visualize import visualize_resource_allocation_graph


# -------------------- INPUT HELPERS --------------------

def get_pages_from_user():
    while True:
        try:
            user_input = input("Enter page numbers separated by spaces: ").strip()
            pages = list(map(int, user_input.split()))
            if pages:
                return pages
            else:
                print("Please enter at least one number.")
        except ValueError:
            print("Invalid input. Please enter integers only.")


def get_scheduling_processes():
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        print(f"\nProcess P{i+1}")
        at = int(input("  Arrival Time: "))
        bt = int(input("  Burst Time: "))
        processes.append({'name': f'P{i+1}', 'arrival_time': at, 'burst_time': bt})
    return processes


def get_memory_blocks_and_processes():
    m = int(input("Enter number of memory blocks: "))
    memory_blocks = []
    for i in range(m):
        size = int(input(f"  Size of block {i+1}: "))
        memory_blocks.append(size)

    p = int(input("\nEnter number of processes: "))
    processes = {}
    for i in range(p):
        name = f'P{i+1}'
        size = int(input(f"  Memory required for {name}: "))
        processes[name] = size

    return memory_blocks, processes


def get_deadlock_input():
    r = int(input("Enter number of resource types: "))
    p = int(input("Enter number of processes: "))
    resource_names = [f'R{i+1}' for i in range(r)]
    processes = [f'P{i+1}' for i in range(p)]

    print("\nEnter total instances of each resource:")
    total_resources = [int(input(f"  Total {name}: ")) for name in resource_names]

    print("\nEnter Allocation matrix:")
    allocation = []
    for i in range(p):
        row = list(map(int, input(f"  Allocation for {processes[i]}: ").split()))
        allocation.append(row)

    print("\nEnter Request matrix:")
    request = []
    for i in range(p):
        row = list(map(int, input(f"  Request for {processes[i]}: ").split()))
        request.append(row)

    return processes, resource_names, total_resources, allocation, request

# -------------------- DEMO RUNNERS --------------------

def run_page_replacement_demo(pages):
    capacity = int(input("Enter frame capacity: "))

    fifo = FIFO(capacity)
    for i, page in enumerate(pages):
        fifo.access_page(page, i)
    faults, hits, frames = fifo.get_results()
    visualize_page_replacement("FIFO", faults, hits, frames, pages)

    lru = LRU(capacity)
    for i, page in enumerate(pages):
        lru.access_page(page, i)
    faults, hits, frames = lru.get_results()
    visualize_page_replacement("LRU", faults, hits, frames, pages)

    optimal = Optimal(capacity)
    optimal.run_simulation(pages)
    faults, hits, frames = optimal.get_results()
    visualize_page_replacement("Optimal", faults, hits, frames, pages)


def run_scheduling_demo():
    processes = get_scheduling_processes()

    fcfs = FCFS(processes)
    fcfs.run()
    visualize_scheduling("FCFS", *fcfs.get_results())

    sjf = SJF(processes)
    sjf.run()
    visualize_scheduling("SJF", *sjf.get_results())

    tq = int(input("Enter time quantum for Round Robin: "))
    rr = RoundRobin(processes, time_quantum=tq)
    rr.run()
    visualize_scheduling("Round Robin", *rr.get_results())


def run_memory_management_demo():
    memory_blocks, processes = get_memory_blocks_and_processes()
    original_blocks = memory_blocks[:]  # <-- Copy of original memory blocks

    # First Fit Allocation
    first_fit = FirstFit(memory_blocks[:])  # fresh copy
    for process, size in processes.items():
        first_fit.allocate(process, size)
    visualize_memory_allocation("First Fit", first_fit.get_memory_blocks(), first_fit.get_allocation(), original_blocks=original_blocks)

    # Best Fit Allocation
    best_fit = BestFit(memory_blocks[:])  # fresh copy again
    for process, size in processes.items():
        best_fit.allocate(process, size)
    visualize_memory_allocation("Best Fit", best_fit.get_memory_blocks(), best_fit.get_allocation(), original_blocks=original_blocks)



def run_deadlock_demo():
    processes, resource_names, total, allocation, request = get_deadlock_input()

    print("\n--- Deadlock Detection ---")
    detection = DeadlockDetection(processes, total, allocation, request)
    print(detection.detect_deadlock())
    visualize_resource_allocation_graph(processes, resource_names, allocation, request)


# -------------------- MAIN MENU --------------------

def print_menu():
    print("\nOperating System Concepts Demo")
    print("1. Page Replacement Algorithms")
    print("2. Scheduling Algorithms")
    print("3. Memory Management Algorithms")
    print("4. Deadlock Handling")
    print("5. Exit")


def main():
    while True:
        print_menu()
        choice = input("Select an option (1-5): ").strip()
        if choice == '1':
            pages = get_pages_from_user()
            run_page_replacement_demo(pages)
        elif choice == '2':
            run_scheduling_demo()
        elif choice == '3':
            run_memory_management_demo()
        elif choice == '4':
            run_deadlock_demo()
        elif choice == '5':
            print("Exiting. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main() 