from collections import deque
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def round_robin(arrival_time, burst_time, time_quantum):
    processes_info = sorted([
        {"job": chr(65 + i), "at": at, "bt": bt}
        for i, (at, bt) in enumerate(zip(arrival_time, burst_time))
    ], key=lambda x: x["at"])

    solved_processes_info = []
    gantt_chart_info = []
    ready_queue = deque()
    current_time = processes_info[0]["at"]
    unfinished_jobs = list(processes_info)
    remaining_time = {proc["job"]: proc["bt"] for proc in processes_info}

    while sum(remaining_time.values()) > 0 and unfinished_jobs:
        if not ready_queue and unfinished_jobs:
            ready_queue.append(unfinished_jobs.pop(0))
            current_time = ready_queue[0]["at"]

        process_to_execute = ready_queue.popleft()

        exec_time = min(time_quantum, remaining_time[process_to_execute["job"]])
        remaining_time[process_to_execute["job"]] -= exec_time
        gantt_chart_info.append({
            "job": process_to_execute["job"],
            "start": current_time,
            "stop": current_time + exec_time
        })
        current_time += exec_time

        # Check for processes arriving during the current cycle
        new_arrivals = [
            proc for proc in processes_info
            if proc["at"] <= current_time and
               proc not in ready_queue and
               proc in unfinished_jobs
        ]

        # Add new processes to the ready queue
        ready_queue.extend(new_arrivals)

        # If the process has finished, record its info
        if remaining_time[process_to_execute["job"]] == 0:
            # Ensure the process is in unfinished_jobs before removing
            if process_to_execute in unfinished_jobs:
                unfinished_jobs.remove(process_to_execute)
            solved_processes_info.append({
                **process_to_execute,
                "ft": current_time,
                "tat": current_time - process_to_execute["at"],
                "wat": current_time - process_to_execute["at"] - process_to_execute["bt"]
            })
        else:
            # Requeue the process if it has remaining time
            ready_queue.append(process_to_execute)

    # Sort the solved processes info for output
    solved_processes_info.sort(key=lambda x: (x["at"], x["job"]))

    return solved_processes_info, gantt_chart_info


# Example usage
arrival_time = [4, 3, 1, 5, 0, 2]
burst_time = [3, 7, 4, 2, 2, 4]
time_quantum = 1

solved_info, gantt_info = round_robin(arrival_time, burst_time, time_quantum)
print(solved_info)
print(gantt_info)

# Assuming gantt_info is a list of dictionaries with 'job', 'start', and 'stop' keys

# Create a DataFrame for the Gantt Chart information
df_gantt = pd.DataFrame(gantt_info)

# Prepare the data for plotting
# Create a timeline DataFrame where each row corresponds to a unit of time
max_time = 30
timeline = pd.DataFrame(index=pd.MultiIndex.from_product([df_gantt['job'].unique(), range(1, max_time+1)], names=['Process', 'Time']))
timeline['Execution'] = 0  # Initialize the Execution column to 0

# Fill in the Execution column based on the gantt_info
for info in gantt_info:
    timeline.loc[(info['job'], range(info['start'], info['stop']+1)), 'Execution'] = 1

# Pivot the timeline DataFrame to get it into the required shape for the heatmap
df_pivot = timeline.reset_index().pivot(index='Process', columns='Time', values='Execution').fillna(0)

# Plotting the heatmap
plt.figure(figsize=(20, 5))
sns.heatmap(df_pivot, cmap='Greens', cbar=False, linewidths=.5)
plt.title('Process Execution Timeline')
plt.xlabel('Time Units')
plt.ylabel('Processes')
plt.show()