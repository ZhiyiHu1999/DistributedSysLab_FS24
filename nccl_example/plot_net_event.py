import re
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

file_path = sys.argv[1]

send_entries = defaultdict(list)
send_exits = defaultdict(list)
recv_entries = defaultdict(list)
recv_exits = defaultdict(list)

with open(file_path, 'r') as file:
    for line in file:
        send_entry_match = re.search(r'NET SEND ENTRY INFO: \(Sender_Global_Rank:(\d+), Receiver_Global_Rank:(\d+), Size:\d+, Timestamp:(\d+)\)', line)
        send_exit_match = re.search(r'NET SEND EXIT INFO: \(Sender_Global_Rank:(\d+), Receiver_Global_Rank:(\d+), Size:\d+, Timestamp:(\d+)\)', line)
        recv_entry_match = re.search(r'NET RECV ENTRY INFO: \(Receiver_Global_Rank:(\d+), Sender_Global_Rank:(\d+), Size:\d+, Timestamp:(\d+)\)', line)
        recv_exit_match = re.search(r'NET RECV EXIT INFO: \(Receiver_Global_Rank:(\d+), Sender_Global_Rank:(\d+), Size:\d+, Timestamp:(\d+)\)', line)

        if send_entry_match:
            sender_rank = int(send_entry_match.group(1))
            receiver_rank = int(send_entry_match.group(2))
            timestamp = int(send_entry_match.group(3))
            send_entries[(sender_rank, receiver_rank)].append(timestamp)

        elif send_exit_match:
            sender_rank = int(send_exit_match.group(1))
            receiver_rank = int(send_exit_match.group(2))
            timestamp = int(send_exit_match.group(3))
            send_exits[(sender_rank, receiver_rank)].append(timestamp)

        elif recv_entry_match:
            receiver_rank = int(recv_entry_match.group(1))
            sender_rank = int(recv_entry_match.group(2))
            timestamp = int(recv_entry_match.group(3))
            recv_entries[(receiver_rank, sender_rank)].append(timestamp)

        elif recv_exit_match:
            receiver_rank = int(recv_exit_match.group(1))
            sender_rank = int(recv_exit_match.group(2))
            timestamp = int(recv_exit_match.group(3))
            recv_exits[(receiver_rank, sender_rank)].append(timestamp)


paired_send_events = {}
paired_recv_events = {}

for key in send_entries:
    send_entries[key].sort()
    send_exits[key].sort()
    paired_send_events[key] = list(zip(send_entries[key], send_exits[key]))

for key in recv_entries:
    recv_entries[key].sort()
    recv_exits[key].sort()
    paired_recv_events[key] = list(zip(recv_entries[key], recv_exits[key]))

fig, axs = plt.subplots(len(paired_send_events) + len(paired_recv_events), 1, figsize=(10, 5 * (len(paired_send_events) + len(paired_recv_events))))
fig.tight_layout(pad=5.0)

for i, (key, events) in enumerate(paired_send_events.items()):
    ax = axs[i] if len(paired_send_events) + len(paired_recv_events) > 1 else axs
    for event in events:
        ax.plot([event[0], event[1]], [i, i], label=f'{key} Send', marker='o')
    ax.set_title(f'NET SEND EVENTS (Sender: {key[0]}, Receiver: {key[1]})')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Event Index')
    ax.legend()

for i, (key, events) in enumerate(paired_recv_events.items(), start=len(paired_send_events)):
    ax = axs[i] if len(paired_send_events) + len(paired_recv_events) > 1 else axs
    for event in events:
        ax.plot([event[0], event[1]], [i, i], label=f'{key} Receive', marker='o')
    ax.set_title(f'NET RECV EVENTS (Receiver: {key[0]}, Sender: {key[1]})')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Event Index')
    ax.legend()

plt.show()
