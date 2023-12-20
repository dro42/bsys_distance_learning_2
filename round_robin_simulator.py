# Improved Round Robin scheduling implementation

from collections import deque
import pandas as pd
from IPython.display import display


def simulate_round_robin(processes, time_quantum=1, max_time_units=30):
    """
    Improved simulation of Round Robin scheduling for given processes.

    Parameters:
    processes (list of tuples): Each tuple contains (ProcessID, ArrivalTime, BurstTime).
    time_quantum (int): The time quantum for the Round Robin scheduling.
    max_time_units (int): The maximum number of time units for the execution table.

    Returns:
    pd.DataFrame: DataFrame representing the execution timeline of processes.
    """
    # Sort processes by their arrival time
    processes.sort(key=lambda x: x[1])

    # Initialize variables
    queue = deque()
    current_time = 0
    timeline = []
    waiting_time = {process[0]: 0 for process in processes}
    turnaround_time = {process[0]: 0 for process in processes}
    remaining_burst_time = {process[0]: process[2] for process in processes}

    # Start the round-robin scheduling
    while processes or queue:
        # Add processes to the queue that have arrived
        while processes and processes[0][1] <= current_time:
            queue.append(processes.pop(0))

        if queue:
            current_process = queue.popleft()
            process_id, arrival_time, burst_time = current_process

            # Calculate execution time
            exec_time = min(time_quantum, remaining_burst_time[process_id])
            remaining_burst_time[process_id] -= exec_time

            # Record the timeline
            timeline.append((process_id, current_time, current_time + exec_time))
            current_time += exec_time

            # If the process is not finished, put it back in the queue
            if remaining_burst_time[process_id] > 0:
                queue.append(current_process)
            else:
                # Process is finished, calculate turnaround time
                turnaround_time[process_id] = current_time - arrival_time
                waiting_time[process_id] = turnaround_time[process_id] - burst_time + exec_time

        else:
            # Increment current time if no process is ready to execute
            current_time += 1

    # Create the execution table
    execution_table = {process_id: [" " for _ in range(max_time_units)] for process_id in waiting_time}
    for process_id, start, end in timeline:
        for time_unit in range(start, min(end, max_time_units)):
            execution_table[process_id][time_unit] = "X"

    # Convert the table to a DataFrame and transpose
    df_execution_table = pd.DataFrame(execution_table)
    df_execution_table.index += 1  # Adjusting index to start from 1
    df_execution_transposed = df_execution_table.transpose()

    # Reorder the DataFrame for process order
    ordered_processes = ['A', 'B', 'C', 'D', 'E', 'F']
    return df_execution_transposed.loc[ordered_processes]


def main():
    # Example usage
    processes_example = [("A", 4, 3), ("B", 3, 7), ("C", 1, 4), ("D", 5, 2), ("E", 0, 2), ("F", 2, 4)]
    df_execution_ordered = simulate_round_robin(processes_example)
    df_execution_ordered.head(30)  # Displaying first 30 units of time
    display(df_execution_ordered)


if __name__ == "__main__":
    main()
