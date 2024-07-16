import json
import re
import sys

NPKIT_TRACE_FILE = "./npkit_run/npkit_trace/job_example_2/npkit_event_trace.json"
INFO_TRACE_FILE = sys.argv[1]
# INFO_TRACE_FILE = "./example_2.54409157.o"
MERGE_FILE = "./npkit_run/npkit_trace/job_example_2/merged_trace.json"

try:
    import os
    os.remove(MERGE_FILE)
except FileNotFoundError:
    pass

with open(NPKIT_TRACE_FILE, 'r') as file:
    data1 = json.load(file)

entries = []

with open(INFO_TRACE_FILE, 'r') as f2:
    for line in f2:
        send_entry_match = re.search(r"NCCL INFO NET SEND ENTRY INFO: \(Sender_Global_Rank:([0-9]+), Receiver_Global_Rank:([0-9]+), Size:([0-9]+), Channel_Id:([0-9]+), Timestamp:([0-9]+)\)", line)
        send_exit_match = re.search(r"NCCL INFO NET SEND EXIT INFO: \(Sender_Global_Rank:([0-9]+), Receiver_Global_Rank:([0-9]+), Size:([0-9]+), Channel_Id:([0-9]+), Timestamp:([0-9]+)\)", line)
        recv_entry_match = re.search(r"NCCL INFO NET RECV ENTRY INFO: \(Receiver_Global_Rank:([0-9]+), Sender_Global_Rank:([0-9]+), Size:([0-9]+), Channel_Id:([0-9]+), Timestamp:([0-9]+)\)", line)
        recv_exit_match = re.search(r"NCCL INFO NET RECV EXIT INFO: \(Receiver_Global_Rank:([0-9]+), Sender_Global_Rank:([0-9]+), Size:([0-9]+), Channel_Id:([0-9]+), Timestamp:([0-9]+)\)", line)
        if send_entry_match:
            entry = {
                'Sender_Global_Rank': int(send_entry_match.group(1)),
                'Receiver_Global_Rank': int(send_entry_match.group(2)),
                'Size': int(send_entry_match.group(3)),
                'Channel_Id': int(send_entry_match.group(4)),
                'Timestamp': int(send_entry_match.group(5)) / 1000.0
            }
            entries.append(entry)

        elif send_exit_match:
            entry = {
                'Sender_Global_Rank': int(send_exit_match.group(1)),
                'Receiver_Global_Rank': int(send_exit_match.group(2)),
                'Size': int(send_exit_match.group(3)),
                'Channel_Id': int(send_exit_match.group(4)),
                'Timestamp': int(send_exit_match.group(5)) / 1000.0
            }
            entries.append(entry)

        elif recv_entry_match:
            entry = {
                'Receiver_Global_Rank': int(recv_entry_match.group(1)),
                'Sender_Global_Rank': int(recv_entry_match.group(2)),
                'Size': int(recv_entry_match.group(3)),
                'Channel_Id': int(recv_entry_match.group(4)),
                'Timestamp': int(recv_entry_match.group(5)) / 1000.0
            }
            entries.append(entry)

        elif recv_exit_match:
            entry = {
                'Receiver_Global_Rank': int(recv_exit_match.group(1)),
                'Sender_Global_Rank': int(recv_exit_match.group(2)),
                'Size': int(recv_exit_match.group(3)),
                'Channel_Id': int(recv_exit_match.group(4)),
                'Timestamp': int(recv_exit_match.group(5)) / 1000.0
            }
            entries.append(entry)
            
# print(entries)

for event in data1['traceEvents']:
    for entry in entries:
        if event['ts'] == entry['Timestamp']: 
            event['args'].update({
                'Sender_Global_Rank_merged': entry['Sender_Global_Rank'],
                'Receiver_Global_Rank_merged': entry['Receiver_Global_Rank'],
                'Size_merged': entry['Size'],
                'Channel_Id_merged': entry['Channel_Id'],
                'Timestamp_merged': entry['Timestamp']
            })
            break

with open(MERGE_FILE, 'w') as file:
    json.dump(data1, file, indent=4)

print("Two trace files have been successfully merged")