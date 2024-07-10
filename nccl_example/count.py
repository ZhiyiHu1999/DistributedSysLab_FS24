# import re
# import sys
# from collections import defaultdict

# entry_types = ["NET SEND ENTRY", "NET SEND EXIT", "NET RECV ENTRY", "NET RECV EXIT"]
# size_counts = {entry: defaultdict(int) for entry in entry_types}

# file_path = sys.argv[1]

# with open(file_path, 'r') as file:
#     for line in file:
#         for entry in entry_types:
#             if entry in line:
#                 size_match = re.search(r'Size:(\d+)', line)
#                 if size_match:
#                     size = int(size_match.group(1))
#                     size_counts[entry][size] += 1

# for entry, counts in size_counts.items():
#     print(f"{entry}:")
#     for size, count in counts.items():
#         print(f"  Size: {size}, Count: {count}")


# send_entry_counts = defaultdict(int)
# send_exit_counts = defaultdict(int)
# recv_entry_counts = defaultdict(int)
# recv_exit_counts = defaultdict(int)

# with open(file_path, 'r') as file:
#     for line in file:
#         if "NET SEND ENTRY" in line:
#             match = re.search(r'Sender_Global_Rank:(\d+), Receiver_Global_Rank:(\d+)', line)
#             if match:
#                 sender_rank = int(match.group(1))
#                 receiver_rank = int(match.group(2))
#                 send_entry_counts[(sender_rank, receiver_rank)] += 1
#         elif "NET SEND EXIT" in line:
#             match = re.search(r'Sender_Global_Rank:(\d+), Receiver_Global_Rank:(\d+)', line)
#             if match:
#                 sender_rank = int(match.group(1))
#                 receiver_rank = int(match.group(2))
#                 send_exit_counts[(sender_rank, receiver_rank)] += 1
#         elif "NET RECV ENTRY" in line:
#             match = re.search(r'Receiver_Global_Rank:(\d+), Sender_Global_Rank:(\d+)', line)
#             if match:
#                 receiver_rank = int(match.group(1))
#                 sender_rank = int(match.group(2))
#                 recv_entry_counts[(receiver_rank, sender_rank)] += 1
#         elif "NET RECV EXIT" in line:
#             match = re.search(r'Receiver_Global_Rank:(\d+), Sender_Global_Rank:(\d+)', line)
#             if match:
#                 receiver_rank = int(match.group(1))
#                 sender_rank = int(match.group(2))
#                 recv_exit_counts[(receiver_rank, sender_rank)] += 1

# print("NET SEND ENTRY (Sender_Global_Rank, Receiver_Global_Rank):")
# for pair, count in send_entry_counts.items():
#     print(f"  {pair}: {count}")

# print("\nNET SEND EXIT (Sender_Global_Rank, Receiver_Global_Rank):")
# for pair, count in send_exit_counts.items():
#     print(f"  {pair}: {count}")

# print("\nNET RECV ENTRY (Receiver_Global_Rank, Sender_Global_Rank):")
# for pair, count in recv_entry_counts.items():
#     print(f"  {pair}: {count}")

# print("\nNET RECV EXIT (Receiver_Global_Rank, Sender_Global_Rank):")
# for pair, count in recv_exit_counts.items():
#     print(f"  {pair}: {count}")


# import re
# import sys
# from collections import defaultdict

# entry_types = ["NET SEND ENTRY", "NET SEND EXIT", "NET RECV ENTRY", "NET RECV EXIT"]
# size_counts = {entry: defaultdict(lambda: defaultdict(int)) for entry in entry_types}

# file_path = sys.argv[1]

# with open(file_path, 'r') as file:
#     for line in file:
#         for entry in entry_types:
#             if entry in line:
#                 size_match = re.search(r'Size:(\d+)', line)
#                 channel_match = re.search(r'Channel_Id:(\d+)', line)
#                 if size_match and channel_match:
#                     size = int(size_match.group(1))
#                     channel_id = int(channel_match.group(1))
#                     size_counts[entry][channel_id][size] += 1

# for entry, channels in size_counts.items():
#     print(f"{entry}:")
#     for channel, counts in channels.items():
#         print(f"  Channel_Id: {channel}")
#         for size, count in counts.items():
#             print(f"    Size: {size}, Count: {count}")


# send_entry_counts = defaultdict(lambda: defaultdict(int))
# send_exit_counts = defaultdict(lambda: defaultdict(int))
# recv_entry_counts = defaultdict(lambda: defaultdict(int))
# recv_exit_counts = defaultdict(lambda: defaultdict(int))

# with open(file_path, 'r') as file:
#     for line in file:
#         if "NET SEND ENTRY" in line:
#             match = re.search(r'Sender_Global_Rank:(\d+), Receiver_Global_Rank:(\d+), Size:\d+, Channel_Id:(\d+)', line)
#             if match:
#                 sender_rank = int(match.group(1))
#                 receiver_rank = int(match.group(2))
#                 channel_id = int(match.group(3))
#                 send_entry_counts[(sender_rank, receiver_rank)][channel_id] += 1
#         elif "NET SEND EXIT" in line:
#             match = re.search(r'Sender_Global_Rank:(\d+), Receiver_Global_Rank:(\d+), Size:\d+, Channel_Id:(\d+)', line)
#             if match:
#                 sender_rank = int(match.group(1))
#                 receiver_rank = int(match.group(2))
#                 channel_id = int(match.group(3))
#                 send_exit_counts[(sender_rank, receiver_rank)][channel_id] += 1
#         elif "NET RECV ENTRY" in line:
#             match = re.search(r'Receiver_Global_Rank:(\d+), Sender_Global_Rank:(\d+), Size:\d+, Channel_Id:(\d+)', line)
#             if match:
#                 receiver_rank = int(match.group(1))
#                 sender_rank = int(match.group(2))
#                 channel_id = int(match.group(3))
#                 recv_entry_counts[(receiver_rank, sender_rank)][channel_id] += 1
#         elif "NET RECV EXIT" in line:
#             match = re.search(r'Receiver_Global_Rank:(\d+), Sender_Global_Rank:(\d+), Size:\d+, Channel_Id:(\d+)', line)
#             if match:
#                 receiver_rank = int(match.group(1))
#                 sender_rank = int(match.group(2))
#                 channel_id = int(match.group(3))
#                 recv_exit_counts[(receiver_rank, sender_rank)][channel_id] += 1

# print("NET SEND ENTRY (Sender_Global_Rank, Receiver_Global_Rank):")
# for pair, channels in send_entry_counts.items():
#     print(f"  {pair}:")
#     for channel, count in channels.items():
#         print(f"    Channel_Id: {channel}, Count: {count}")

# print("\nNET SEND EXIT (Sender_Global_Rank, Receiver_Global_Rank):")
# for pair, channels in send_exit_counts.items():
#     print(f"  {pair}:")
#     for channel, count in channels.items():
#         print(f"    Channel_Id: {channel}, Count: {count}")

# print("\nNET RECV ENTRY (Receiver_Global_Rank, Sender_Global_Rank):")
# for pair, channels in recv_entry_counts.items():
#     print(f"  {pair}:")
#     for channel, count in channels.items():
#         print(f"    Channel_Id: {channel}, Count: {count}")

# print("\nNET RECV EXIT (Receiver_Global_Rank, Sender_Global_Rank):")
# for pair, channels in recv_exit_counts.items():
#     print(f"  {pair}:")
#     for channel, count in channels.items():
#         print(f"    Channel_Id: {channel}, Count: {count}")


import re
import sys
from collections import defaultdict

if len(sys.argv) != 2:
    print("Usage: python3 count_net_event_pairs.py <file_name>")
    sys.exit(1)

file_path = sys.argv[1]

event_counts = {entry: defaultdict(lambda: defaultdict(lambda: defaultdict(int))) for entry in ["NET SEND ENTRY", "NET SEND EXIT", "NET RECV ENTRY", "NET RECV EXIT"]}

with open(file_path, 'r') as file:
    for line in file:
        if "NET SEND ENTRY" in line:
            match = re.search(r'Sender_Global_Rank:(\d+), Receiver_Global_Rank:(\d+), Size:(\d+), Channel_Id:(\d+)', line)
            if match:
                sender_rank = int(match.group(1))
                receiver_rank = int(match.group(2))
                size = int(match.group(3))
                channel_id = int(match.group(4))
                event_counts["NET SEND ENTRY"][(sender_rank, receiver_rank)][channel_id][size] += 1
        elif "NET SEND EXIT" in line:
            match = re.search(r'Sender_Global_Rank:(\d+), Receiver_Global_Rank:(\d+), Size:(\d+), Channel_Id:(\d+)', line)
            if match:
                sender_rank = int(match.group(1))
                receiver_rank = int(match.group(2))
                size = int(match.group(3))
                channel_id = int(match.group(4))
                event_counts["NET SEND EXIT"][(sender_rank, receiver_rank)][channel_id][size] += 1
        elif "NET RECV ENTRY" in line:
            match = re.search(r'Receiver_Global_Rank:(\d+), Sender_Global_Rank:(\d+), Size:(\d+), Channel_Id:(\d+)', line)
            if match:
                receiver_rank = int(match.group(1))
                sender_rank = int(match.group(2))
                size = int(match.group(3))
                channel_id = int(match.group(4))
                event_counts["NET RECV ENTRY"][(receiver_rank, sender_rank)][channel_id][size] += 1
        elif "NET RECV EXIT" in line:
            match = re.search(r'Receiver_Global_Rank:(\d+), Sender_Global_Rank:(\d+), Size:(\d+), Channel_Id:(\d+)', line)
            if match:
                receiver_rank = int(match.group(1))
                sender_rank = int(match.group(2))
                size = int(match.group(3))
                channel_id = int(match.group(4))
                event_counts["NET RECV EXIT"][(receiver_rank, sender_rank)][channel_id][size] += 1

for event, pairs in event_counts.items():
    print(f"{event}:")
    for pair, channels in pairs.items():
        print(f"  {pair}:")
        for channel, sizes in channels.items():
            print(f"    Channel_Id: {channel}")
            for size, count in sizes.items():
                print(f"      Size: {size}, Count: {count}")