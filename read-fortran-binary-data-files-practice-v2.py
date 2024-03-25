import struct
import numpy as np
import matplotlib.pyplot as plt

def read_binary_file(file_path, format_string, grid_size):
    data = []
    with open(file_path, 'rb') as f:
        while True:
            day_data = []
            for _ in range(grid_size):
                chunk = f.read(struct.calcsize(format_string))
                if not chunk:
                    break
                record = struct.unpack(format_string, chunk)
                day_data.append(record)
            if not day_data:
                break
            data.append(day_data)
    return data

def print_data_for_each_day(data, grid_size):
    for day, grid in enumerate(data):
        print(f"Data for day {day + 1}: ")
        #for row in grid:
        #    print(row)
        #print()
        for row_index in range(grid_size[0]):
            row_data = grid[row_index*grid_size[1] : (row_index + 1) * grid_size[1]]
            print(" ".join(f"({cell[0]})" for cell in row_data))
        print()

def find_largest_value_for_day(data, day_index):
    day_data = data[day_index]
    largest_value = None
    for row in day_data:
        for value in row:
            if largest_value is None or value > largest_value:
                largest_value = value
    return largest_value

def compute_summary_statistics_for_day(data, day_index):
    day_data = data[day_index] 
    flattened_data = np.array(day_data).flatten() #Transforms grid values into 1D array
    summary_statistics = {
        'Mean: ': np.mean(flattened_data),
        'Median: ': np.median(flattened_data),
        'Standard Deviation: ': np.std(flattened_data),
        'Minimum: ': np.min(flattened_data),
        'Maximum: ': np.max(flattened_data),
    }
    #Another way of calculating summary stats and returning the values
    #mean = np.mean(flattened_data)
    #median = np.median(flattened_data)
    #std_dev = np.std(flattened_data)
    #min = np.min(flattened_data)
    #max = np.max(flattened_data)
    #print(mean)
    #print(median)
    #print(std_dev)
    #print(min)
    #print(max)
    return summary_statistics

def calculate_max_values_per_day(data):
    max_values_per_day = []
    for day_data in data:
        flattened_data = np.array(day_data).flatten()
        max_value = np.max(flattened_data)
        max_values_per_day.append(max_value)
    return max_values_per_day

file_path = 'C:\\cygwin64\\snowmodel\\snowmodel-fraserexperimental-test1\\outputs\\wo_assim\\swed.gdat'
format_string = 'f'
grid_size = (60,41)

data = read_binary_file(file_path, format_string, grid_size[0] * grid_size[1])
#print_data_for_each_day(data, grid_size)

selected_day_index = 284 #Python indexing starts at 0, so to check the largest value of day 285, we use selected_day_index = 284
largest_value_for_selected_day = find_largest_value_for_day(data, selected_day_index)
print(f"Largest value for day {selected_day_index + 1}: {largest_value_for_selected_day}")

summary_stats_for_selected_day = compute_summary_statistics_for_day(data, selected_day_index)
print(f"Summary Statistics for Day {selected_day_index + 1}: ")
for stat, value in summary_stats_for_selected_day.items():
    print(f"{stat}: {value}")

max_values_per_day = calculate_max_values_per_day(data)
plt.figure(figsize=(10,6))
plt.plot(range(1, len(max_values_per_day) + 1), max_values_per_day, marker='o', linestyle='-')
plt.title('Change in max SWE per day from 2017-09-01 to 2018-08-31')
plt.xlabel('Day')
plt.ylabel('Max SWE')
plt.grid(True)
plt.show()