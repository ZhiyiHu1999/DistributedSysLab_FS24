from collections import Counter

operation_counter = Counter()

with open('./results/nsys_events_initial_output.json', 'r') as file:
    for line in file:
        line = line.strip()
        if "nccl" in line:
            if "Broadcast" in line:
                operation_counter["Broadcast"] += 1
            elif "AllReduce" in line:
                operation_counter["AllReduce"] += 1
            elif "AllGather" in line:
                operation_counter["AllGather"] += 1
            elif "ReduceScatter" in line:
                operation_counter["ReduceScatter"] += 1
            elif "Reduce" in line:
                operation_counter["Reduce"] += 1
            elif "Send" in line:
                operation_counter["Send"] += 1
            elif "Recv" in line:
                operation_counter["Recv"] += 1

with open('./results/collectives_statistics.txt', 'w') as output_file:
    for operation, count in operation_counter.items():
        output_file.write(f"{operation}: {count}\n")
        print(f"{operation}: {count}")
    