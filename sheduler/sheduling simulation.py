from collections import deque

import pandas as pd
from IPython.display import display


def first_come_first_served_scheduling(processes):
    # Sort processes by their arrival time
    processes.sort(key=lambda x: x[1])

    # Initialize variables
    current_time = 0
    timeline = []
    waiting_time = {process[0]: 0 for process in processes}
    turnaround_time = {process[0]: 0 for process in processes}
    processes_queue = processes.copy()

    while processes_queue:
        # Get the first process that has arrived
        current_process = None
        for process in processes_queue:
            if process[1] <= current_time:
                current_process = process
                break

        if current_process:
            process_id, arrival_time, burst_time = current_process
            processes_queue.remove(current_process)

            # Execute the process
            start_time = current_time
            current_time += burst_time
            end_time = current_time
            timeline.append((process_id, start_time, end_time))

            # Update turnaround and waiting times
            turnaround_time[process_id] = end_time - arrival_time
            waiting_time[process_id] = turnaround_time[process_id] - burst_time
        else:
            # No process available, advance time
            current_time += 1

    # Calculate average waiting and turnaround times
    average_waiting_time = sum(waiting_time.values()) / len(waiting_time)
    average_turnaround_time = sum(turnaround_time.values()) / len(turnaround_time)

    return timeline, waiting_time, turnaround_time, average_waiting_time, average_turnaround_time


def shortest_job_first_scheduling(processes):
    # Sort processes by their arrival time
    processes.sort(key=lambda x: x[1])

    # Initialize variables
    current_time = 0
    timeline = []
    waiting_time = {process[0]: 0 for process in processes}
    turnaround_time = {process[0]: 0 for process in processes}
    processes_queue = processes.copy()

    while processes_queue:
        # Filter processes that have arrived
        available_processes = [p for p in processes_queue if p[1] <= current_time]

        if available_processes:
            # Select the process with the shortest burst time
            shortest_process = min(available_processes, key=lambda x: x[2])
            processes_queue.remove(shortest_process)
            process_id, arrival_time, burst_time = shortest_process

            # Execute the process
            start_time = current_time
            current_time += burst_time
            end_time = current_time
            timeline.append((process_id, start_time, end_time))

            # Update turnaround and waiting times
            turnaround_time[process_id] = end_time - arrival_time
            waiting_time[process_id] = turnaround_time[process_id] - burst_time
        else:
            # No process available, advance time
            current_time += 1

    # Calculate average waiting and turnaround times
    average_waiting_time = sum(waiting_time.values()) / len(waiting_time)
    average_turnaround_time = sum(turnaround_time.values()) / len(turnaround_time)

    return timeline, waiting_time, turnaround_time, average_waiting_time, average_turnaround_time


def round_robin_scheduling(processes, time_quantum=1):
    # Sort processes by their arrival time
    processes.sort(key=lambda x: x[1])

    # Initialize variables
    current_time = 1
    queue = deque()
    timeline = []
    waiting_time = {process[0]: 0 for process in processes}
    turnaround_time = {process[0]: 0 for process in processes}
    remaining_burst_time = {process[0]: process[2] for process in processes}
    arrival_time = {process[0]: process[1] for process in processes}

    # Start the round-robin scheduling
    while processes or queue:
        # Add initially arrived processes to the queue
        while processes and processes[0][1] <= current_time:
            process_id, _, _ = processes.pop(0)
            queue.append(process_id)

        if queue:
            process_id = queue.popleft()

            # Execute the process
            exec_time = min(time_quantum, remaining_burst_time[process_id])
            remaining_burst_time[process_id] -= exec_time
            timeline.append((process_id, current_time - exec_time, current_time))
            current_time += exec_time

            # Update waiting time for other processes
            for pid in queue:
                waiting_time[pid] += exec_time

            # Check if the process needs more time
            if remaining_burst_time[process_id] > 0:
                queue.append(process_id)

            # Update turnaround time
            if remaining_burst_time[process_id] == 0:
                turnaround_time[process_id] = current_time - arrival_time[process_id]

        else:
            # If no process is running and processes are pending, advance time
            if processes:
                current_time = processes[0][1]

    # Calculate average waiting and turnaround times
    average_waiting_time = sum(waiting_time.values()) / len(waiting_time) if len(waiting_time) > 0 else 0
    average_turnaround_time = sum(turnaround_time.values()) / len(turnaround_time) if len(turnaround_time) > 0 else 0

    # Return the results
    return timeline, waiting_time, turnaround_time, average_waiting_time, average_turnaround_time


def display_scheduling_results(timeline):
    """
    Display the timeline of the scheduling algorithm
    :param timeline: List of tuples representing the process execution timeline
    :return: None
    """

    # Set pandas display options
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Create DataFrames for visualization
    df_timeline = pd.DataFrame(timeline, columns=["ProcessID", "StartTime", "EndTime"])

    # Define the maximum time units for the table
    max_time_units = timeline[-1][2] if timeline else 0

    # Extract unique process IDs from timeline
    unique_process_ids = sorted(set([process_id for process_id, _, _ in timeline]))

    # Initialize the table with empty strings
    execution_table = {process_id: [" " for _ in range(max_time_units)] for process_id in unique_process_ids}

    # Fill the table with 'X' where processes are executing
    for process_id, start, end in timeline:
        for time_unit in range(start, min(end, max_time_units)):
            execution_table[process_id][time_unit] = "X"

    # Convert the table to a DataFrame for better visualization
    df_execution_table = pd.DataFrame(execution_table)
    df_execution_table.index += 1  # Adjusting index to start from 1
    df_execution_table.columns.name = "ProcessID"

    # Transpose the DataFrame to swap rows and columns
    df_execution_transposed = df_execution_table.transpose()

    print(df_execution_transposed)


def main():
    # User input for processes and time quantum
    processes = [("A", 4, 3), ("B", 3, 7), ("C", 1, 4), ("D", 5, 2), ("E", 0, 2), ("F", 2, 4)]  # example
    processes_exe = [("A", 4, 4), ("B", 3, 3), ("C", 0, 2), ("D", 2, 7), ("E", 5, 2), ("F", 1, 4)]  # exercise
    # processes = [("A", 4, 4), ("B", 3, 3), ("C", 0, 2), ("D", 2, 7), ("E", 5, 2), ("F", 1, 4)] #test
    timeline_sj, _, _, _, _ = shortest_job_first_scheduling(processes)
    timeline_fifo, _, _, _, _ = first_come_first_served_scheduling(processes)
    timeline_rr, _, _, _, _ = round_robin_scheduling(processes)

    display(display_scheduling_results(timeline_fifo))
    display(display_scheduling_results(timeline_sj))
    display(display_scheduling_results(timeline_rr))


if __name__ == '__main__':
    main()
