import json
import re

NPKIT_TRACE_FILE = "./npkit_run/npkit_trace/job_example_2/npkit_event_trace.json"
INFO_TRACE_FILE = "./example_2.54393168.o"
MERGE_FILE = "./npkit_run/npkit_trace/job_example_2/merged_trace.json"

try:
    import os
    os.remove(MERGE_FILE)
except FileNotFoundError:
    pass

with open(NPKIT_TRACE_FILE, 'r') as f1:
    with open(MERGE_FILE, 'w') as mf:
        mf.write(f1.read())

send_entries = []
recv_entries = []

with open(INFO_TRACE_FILE, 'r') as f2:
    for line in f2:
        send_match = re.search(r"NCCL INFO NET SEND ENTRY INFO: \(Sender_Global_Rank:([0-9]+), Receiver_Global_Rank:([0-9]+), Size:([0-9]+), Timestamp:([0-9]+)\)", line)
        recv_match = re.search(r"NCCL INFO NET RECV ENTRY INFO: \(Receiver_Global_Rank:([0-9]+), Sender_Global_Rank:([0-9]+), Size:([0-9]+), Timestamp:([0-9]+)\)", line)
        if send_match:
            send_entries.append((int(send_match.group(1)), int(send_match.group(2)), int(send_match.group(3)), int(send_match.group(4))))
        elif recv_match:
            recv_entries.append((int(recv_match.group(1)), int(recv_match.group(2)), int(recv_match.group(3)), int(recv_match.group(4))))

with open(MERGE_FILE, 'r') as mf:
    data = json.load(mf)

send_index = 0
recv_index = 0

data["traceEvents"].sort(key=lambda event: event["ts"])

for event in data["traceEvents"]:
    if "name" in event and event["name"] == "NPKIT_EVENT_NET_SEND_ENTRY" and send_index < len(send_entries):
        event["args"]["Sender_Global_Rank"] = send_entries[send_index][0]
        event["args"]["Receiver_Global_Rank"] = send_entries[send_index][1]
        send_index += 1
    elif "name" in event and event["name"] == "NPKIT_EVENT_NET_RECV_ENTRY" and recv_index < len(recv_entries):
        event["args"]["Receiver_Global_Rank"] = recv_entries[recv_index][0]
        event["args"]["Sender_Global_Rank"] = recv_entries[recv_index][1]
        recv_index += 1

with open(MERGE_FILE, 'w') as mf:
    json.dump(data, mf, indent=2)

print("Two trace files have been successfully merged")