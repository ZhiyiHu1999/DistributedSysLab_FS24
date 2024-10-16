import json
from collections import defaultdict

def get_npkit_events(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    trace_events = data.get("traceEvents", [])
    gpu_events_type_1 = defaultdict(lambda: defaultdict(list))
    gpu_events_type_2 = defaultdict(lambda: defaultdict(list))
    gpu_events_op = defaultdict(lambda: defaultdict(list))
    gpu_events_prim = defaultdict(lambda: defaultdict(list))
    cpu_events_net = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    cpu_events_npkit_init = defaultdict(lambda: defaultdict(list))

    for event in trace_events:
        if event['cat'] == 'CPU':
            rank = event['args']['rank']
            event_name = event['name']

            if event_name.startswith('NPKIT_EVENT_NET'):
                channel = event['args']['channel']
                event_info = {
                    'seq': event['args'].get('seq'),  ## useless
                    'step': event['args'].get('step'),
                    'ts': int(event['ts'] // 1),  ## event['ts'] is in time unit of microsecond
                    'sender_rank': event['args'].get('sender_rank'),
                    'receiver_rank': event['args'].get('receiver_rank'),
                    'size': event['args'].get('size_0')
                    }
                cpu_events_net[rank][channel][event_name].append(event_info)
            
            elif event_name.startswith('NPKIT_EVENT_NPKIT_INIT'):
                event_info = {
                    'ts': int(event['ts'] // 1),  ## event['ts'] is in time unit of microsecond
                    }
                cpu_events_npkit_init[rank][event_name].append(event_info)

        elif event['cat'] == 'GPU':
            rank = event['args']['rank']
            tid = event['tid']
            event_name = event['name']
            event_info = {
                'event_name': event_name,
                'seq': event['args'].get('seq'),  ## useless
                'ts': int(event['ts'] // 1),  ## event['ts'] is in time unit of microsecond
                }

            if event_name.startswith('NPKIT_EVENT_GPU_1'):
                gpu_events_type_1[rank][tid].append(event_info)
            elif event_name.startswith('NPKIT_EVENT_GPU_2'):
                gpu_events_type_2[rank][tid].append(event_info)
            elif event_name.startswith('NPKIT_EVENT_GPU_OP'):
                gpu_events_op[rank][tid].append(event_info)
            elif event_name.startswith('NPKIT_EVENT_PRIM'):
                gpu_events_prim[rank][tid].append(event_info)
    
    return gpu_events_type_1, gpu_events_type_2, gpu_events_op, gpu_events_prim, cpu_events_net, cpu_events_npkit_init

# num_ranks = 0

# for rank, channels in tracing_result.items():  ## rank is the key, channels is the corresponding value
#     num_ranks += 1
#     print(f"Rank: {rank}")
#     for channel, events in channels.items():
#         print(f"  Channel: {channel}")
#         for event_name, infos in events.items():
#             print(f"    Event: {event_name}")
#             if event_name != 'NPKIT_EVENT_NPKIT_INIT_ENTRY' and event_name != 'NPKIT_EVENT_NPKIT_INIT_EXIT':
#                 for info in infos:  ## 'infos' is a list containing dictionaries 'info'
#                     # print(f"      {info}")
#                     info['ts'] -= channels[0]['NPKIT_EVENT_NPKIT_INIT_EXIT'][0]['ts']
#                     print(f"      {info}")

def main():
    json_file = './results/npkit_run/npkit_trace/job_example_2/npkit_event_trace.json'
    Gpu_Events_Type_1, Gpu_Events_Type_2, Gpu_Events_Op, Gpu_Events_Prim, Cpu_Events_Net, Cpu_Events_Npkit_Init = get_npkit_events(json_file)

    with open("./results/npkit_events_intermediate_output.json", "w") as json_file:
        json.dump(Gpu_Events_Type_1, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(Gpu_Events_Type_2, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(Gpu_Events_Op, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(Gpu_Events_Prim, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(Cpu_Events_Net, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(Cpu_Events_Npkit_Init, json_file, indent=4)
    print("Npkit_Events has been exported to npkit_events_intermediate_output.json")

    # goal_filename = './example_2.goal'
    # with open(goal_filename, 'w') as file:
    #     file.write(f"num_ranks {num_ranks}\n")
    #     # for rank, channels in tracing_result.items():
    #     for rank in range(num_ranks):
    #         channels = tracing_result[rank]
    #         task_counter = 0
    #         file.write(f"\nrank {rank}")
    #         file.write(" {\n")
    #         for channel, events in channels.items():
    #             if len(events['NPKIT_EVENT_NET_SEND_ENTRY']) > 0:
    #                 task_counter += 1
    #                 task_counter_init = task_counter
    #                 for i in range(len(events['NPKIT_EVENT_NET_SEND_ENTRY'])):
    #                     event = events['NPKIT_EVENT_NET_SEND_EXIT'][i]
    #                     task_counter += 1
    #                     file.write(f"l{task_counter}: send {event['size']}b to {event['receiver_rank']} tag {channel}\n")
    #                     ts_net_send_exit = event['ts']
    #                     if task_counter - task_counter_init == 1:
    #                         file.write(f"l{task_counter_init}: calc 0\n")

    #                     event = events['NPKIT_EVENT_NET_SEND_ENTRY'][i]
    #                     task_counter += 1
    #                     file.write(f"l{task_counter}: calc {event['ts']}\n")
    #                     file.write(f"l{task_counter - 1} requires l{task_counter}\n")
    #                     file.write(f"l{task_counter} requires l{task_counter_init}\n")

    #                     event = events["NPKIT_EVENT_NET_SEND_TEST_ENTRY"][i]
    #                     task_counter += 1
    #                     file.write(f"l{task_counter}: calc {event['ts'] - ts_net_send_exit}\n")
    #                     file.write(f"l{task_counter} requires l{task_counter - 1}\n")
    #                     file.write(f"l{task_counter} irequires l{task_counter - 2}\n")

    #             if len(events['NPKIT_EVENT_NET_RECV_ENTRY']) > 0:
    #                 for i in range(len(events['NPKIT_EVENT_NET_RECV_ENTRY'])):
    #                     event = events["NPKIT_EVENT_NET_RECV_ENTRY"][i]
    #                     ts_net_recv_entry = event['ts']

    #                     event = events["NPKIT_EVENT_NET_RECV_TEST_ENTRY"][i]
    #                     task_counter += 1
    #                     file.write(f"l{task_counter}: recv {event['size']}b from {event['sender_rank']} tag {channel}\n")  ## In "NPKIT_EVENT_NET_RECV_TEST_ENTRY" & "NPKIT_EVENT_NET_RECV_TEST_EXIT", we have the real size received
    #                     task_counter += 1
    #                     file.write(f"l{task_counter}: calc {event['ts'] - ts_net_recv_entry}\n")

    #                     event = events["NPKIT_EVENT_NET_RECV_ENTRY"][i]
    #                     task_counter += 1
    #                     file.write(f"l{task_counter}: calc {event['ts']}\n")
    #                     file.write(f"l{task_counter - 2} requires l{task_counter}\n")
    #                     file.write(f"l{task_counter - 1} requires l{task_counter}\n")
    #                     file.write(f"l{task_counter - 1} irequires l{task_counter - 2}\n")
    #                     file.write(f"l{task_counter} requires l{task_counter_init}\n")
                
    #         file.write("}\n")
                
if __name__ == '__main__':
    main()