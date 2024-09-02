import json
from collections import defaultdict

def process_trace_events(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    trace_events = data.get("traceEvents", [])
    ranks_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for event in trace_events:
        if event['cat'] == 'CPU':
            rank = event['args']['rank']
            channel = event['args']['channel']
            event_name = event['name']
            event_info = {
                'seq': event['args'].get('seq'),
                'ts': int(event['ts'] // 1),  ## event['ts'] is in time unit of microsecond
                'sender_rank': event['args'].get('sender_rank'),
                'receiver_rank': event['args'].get('receiver_rank'),
                'size': event['args'].get('size_0')
            }

            ranks_data[rank][channel][event_name].append(event_info)
    
    return ranks_data

json_file = './npkit_run/npkit_trace/mnist/npkit_event_trace.json'
tracing_result = process_trace_events(json_file)

num_ranks = 0

for rank, channels in tracing_result.items():  ## rank is the key, channels is the corresponding value
    num_ranks += 1
    print(f"Rank: {rank}")
    for channel, events in channels.items():
        print(f"  Channel: {channel}")
        for event_name, infos in events.items():
            print(f"    Event: {event_name}")
            if event_name != 'NPKIT_EVENT_NPKIT_INIT_ENTRY' and event_name != 'NPKIT_EVENT_NPKIT_INIT_EXIT':
                for info in infos:  ## 'infos' is a list containing dictionaries 'info'
                    # print(f"      {info}")
                    info['ts'] -= channels[0]['NPKIT_EVENT_NPKIT_INIT_EXIT'][0]['ts']
                    print(f"      {info}")

def main():
    goal_filename = './pytorch_example_mnist.goal'
    with open(goal_filename, 'w') as file:
        file.write(f"num_ranks {num_ranks}\n")
        # for rank, channels in tracing_result.items():
        for rank in range(num_ranks):
            channels = tracing_result[rank]
            task_counter = 0
            file.write(f"\nrank {rank}")
            file.write(" {\n")
            for channel, events in channels.items():
                if len(events['NPKIT_EVENT_NET_SEND_ENTRY']) > 0:
                    for i in range(len(events['NPKIT_EVENT_NET_SEND_ENTRY'])):
                        event = events['NPKIT_EVENT_NET_SEND_EXIT'][i]
                        task_counter += 1
                        file.write(f"l{task_counter}: send {event['size']}b to {event['receiver_rank']} tag {channel}\n")
                        ts_net_send_exit = event['ts']

                        event = events['NPKIT_EVENT_NET_SEND_ENTRY'][i]
                        task_counter += 1
                        file.write(f"l{task_counter}: calc {event['ts']}\n")
                        file.write(f"l{task_counter - 1} requires l{task_counter}\n")

                        event = events["NPKIT_EVENT_NET_SEND_TEST_ENTRY"][i]
                        task_counter += 1
                        file.write(f"l{task_counter}: calc {event['ts'] - ts_net_send_exit}\n")
                        file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                        file.write(f"l{task_counter} irequires l{task_counter - 2}\n")

                if len(events['NPKIT_EVENT_NET_RECV_ENTRY']) > 0:
                    for i in range(len(events['NPKIT_EVENT_NET_RECV_ENTRY'])):
                        event = events["NPKIT_EVENT_NET_RECV_ENTRY"][i]
                        ts_net_recv_entry = event['ts']

                        event = events["NPKIT_EVENT_NET_RECV_TEST_ENTRY"][i]
                        task_counter += 1
                        file.write(f"l{task_counter}: recv {event['size']}b from {event['sender_rank']} tag {channel}\n")  ## In "NPKIT_EVENT_NET_RECV_TEST_ENTRY" & "NPKIT_EVENT_NET_RECV_TEST_EXIT", we have the real size received
                        task_counter += 1
                        file.write(f"l{task_counter}: calc {event['ts'] - ts_net_recv_entry}\n")

                        event = events["NPKIT_EVENT_NET_RECV_ENTRY"][i]
                        task_counter += 1
                        file.write(f"l{task_counter}: calc {event['ts']}\n")
                        file.write(f"l{task_counter - 2} requires l{task_counter}\n")
                        file.write(f"l{task_counter - 1} requires l{task_counter}\n")
                        file.write(f"l{task_counter - 1} irequires l{task_counter - 2}\n")
                
            file.write("}\n")
                
if __name__ == '__main__':
    main()