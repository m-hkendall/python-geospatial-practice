import struct

#def read_binary_file(file_path, format_string):
#    data_set = []
#    with open(file_path, 'rb') as f:
#        while True:
#            chunk = f.read(struct.calcsize(format_string))
#            if not chunk:
#                break
#            data = struct.unpack(format_string, chunk)
#            data_set.append(data)
#    return data_set

#file_path = 'C:\\cygwin64\\snowmodel\\snowmodel-fraserexperimental-test1\\outputs\\wo_assim\\swed.gdat'
#format_string = 'f'

#data_set = read_binary_file(file_path, format_string)
#print(data_set)

#def read_binary_file(file_path, format_string):
#    data = []
#    with open(file_path, 'rb') as f:
#        while True:
#            chunk = f.read(struct.calcsize(format_string))
#            if not chunk:
#                break
#            record = struct.unpack(format_string, chunk)
#            data.append(record)
#    return data

#def print_data_for_each_day(data):
#    for day, record in enumerate(data):
#        print(f"Data for day {day + 1}: {record}")

#file_path = 'C:\\cygwin64\\snowmodel\\snowmodel-fraserexperimental-test1\\outputs\\wo_assim\\swed.gdat'
#format_string = 'f'

#data = read_binary_file(file_path, format_string)
#print_data_for_each_day(data)

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

file_path = 'C:\\cygwin64\\snowmodel\\snowmodel-fraserexperimental-test1\\outputs\\wo_assim\\swed.gdat'
format_string = 'f'
grid_size = (60,41)

data = read_binary_file(file_path, format_string, grid_size[0] * grid_size[1])
print_data_for_each_day(data, grid_size)

selected_day_index = 284 #Python indexing starts at 0, so to check the largest value of day 285, we use selected_day_index = 284
largest_value_for_selected_day = find_largest_value_for_day(data, selected_day_index)
print(f"Largest value for day {selected_day_index + 1}: {largest_value_for_selected_day}")

