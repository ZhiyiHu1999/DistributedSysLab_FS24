import json
from collections import Counter

# Load the JSON data
with open('./npkit_run/npkit_trace/job_example_2/merged_trace.json', 'r') as file:
    data = json.load(file)

# Initialize counters for SEND_ENTRY and RECV_ENTRY for ph = 'B'
entry_B = Counter()


# Initialize counter for ph = 'E' with Sender_Global_Rank and Receiver_Global_Rank
count_E_events_with_ranks = 0

# Total count of events with Sender_Global_Rank and Receiver_Global_Rank
total_count_with_ranks = 0

# Iterate over the events
for event in data['traceEvents']:
    if 'args' in event and 'Sender_Global_Rank_merged' in event['args'] and 'Receiver_Global_Rank_merged' in event['args']:
        total_count_with_ranks += 1
        if event['ph'] == 'B':
            if 'name' in event:
                entry_B[event['name']] += 1
        elif event['ph'] == 'E':
            count_E_events_with_ranks += 1

result = {
    'ph_B': {
        'ENTRY': dict(entry_B)
    },
    'ph_E': {
        'count_with_ranks': count_E_events_with_ranks
    },
    'total_count_with_ranks': total_count_with_ranks
}

print(result)