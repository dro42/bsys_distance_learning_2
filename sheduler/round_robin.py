from collections import deque

import pandas as pd
from IPython.display import display


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


def display_round_robin_results(processes, time_quantum):
    """
    Display the timeline of RR
    :param processes:
    :param time_quantum:
    :return:
    """
    timeline, waiting_time, turnaround_time, _, _ = round_robin_scheduling(processes, time_quantum)

    # Set pandas display options
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Create DataFrames for visualization
    df_timeline = pd.DataFrame(timeline, columns=["ProcessID", "StartTime", "EndTime"])
    df_waiting_turnaround = pd.DataFrame(list(waiting_time.items()), columns=["ProcessID", "WaitingTime"])
    df_waiting_turnaround["TurnaroundTime"] = df_waiting_turnaround["ProcessID"].map(turnaround_time)

    # Define the maximum time units for the table
    max_time_units = timeline[-1][2]

    # Initialize the table with empty strings
    execution_table = {process_id: [" " for _ in range(max_time_units)] for process_id in waiting_time}

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

    # Extract unique process IDs from timeline in the order they first appear
    ordered_process_ids = []
    for process_id, _, _ in timeline:
        if process_id not in ordered_process_ids:
            ordered_process_ids.append(process_id)
    ordered_process_ids = sorted(ordered_process_ids)
    # Reordering the DataFrame to display processes in the order they appear in timeline
    df_execution_ordered = df_execution_transposed.reindex(ordered_process_ids)

    # Styling and displaying the DataFrame directly
    df_execution_ordered.style.map(
        lambda x: 'background-color: lightgreen' if x == 'X' else 'background-color: white')
    display(df_execution_ordered)


def main():
    # User input for processes and time quantum
    processes = [("A", 4, 3), ("B", 3, 7), ("C", 1, 4), ("D", 5, 2), ("E", 0, 2), ("F", 2, 4)]  # example
    processes_exe = [("A", 4, 4), ("B", 3, 3), ("C", 0, 2), ("D", 2, 7), ("E", 5, 2), ("F", 1, 4)]  # exercise
    # processes = [("A", 4, 4), ("B", 3, 3), ("C", 0, 2), ("D", 2, 7), ("E", 5, 2), ("F", 1, 4)] #test
    display_round_robin_results(processes, 1)
    display_round_robin_results(processes_exe, 1)


if __name__ == '__main__':
    main()
