import json
import math
from collections import defaultdict

def get_npkit_events(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    npkit_events = data.get("traceEvents", [])
    ncclkernel_events = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    prim_events = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for event in npkit_events:
        rank = event['args']['rank']
        tid = event['tid']
        event_name = event['name']
        event_info = {
            'event_name': event_name,
            'DataProcessTotalTime': math.ceil(event['args'].get('DataProcessTotalTime') / 1000),  ## ns to us
            'ts': int(event['ts'] // 1),  ## us to us
            }

        if event_name.startswith('NPKIT_EVENT_NCCLKERNEL'):
            if event_name.endswith('ENTRY'):
                ncclkernel_events[rank][tid]["entry_events"].append(event_info)
            elif event_name.endswith('EXIT'):
                ncclkernel_events[rank][tid]["exit_events"].append(event_info)
        elif event_name.startswith('NPKIT_EVENT_PRIM'):
            if event_name.endswith('ENTRY'):
                prim_events[rank][tid]["entry_events"].append(event_info)
            elif event_name.endswith('EXIT'):
                prim_events[rank][tid]["exit_events"].append(event_info)
    
    return ncclkernel_events, prim_events

def pair_npkit_events(ncclkernel_events, prim_events):
    npkit_paired_events = {}

    for rank in ncclkernel_events.keys():
        npkit_paired_events[rank] = {}
        for tid in ncclkernel_events[rank].keys():
            npkit_paired_events[rank][tid] = []

    for rank in ncclkernel_events.keys():
        for tid in ncclkernel_events[rank].keys():
            for i in range(len(ncclkernel_events[rank][tid]["entry_events"])):
                npkit_paired_event = {}
                npkit_paired_event["prim_events"] = []
                npkit_paired_event["event_name"] = ncclkernel_events[rank][tid]["entry_events"][i]["event_name"].replace("_ENTRY", "")
                npkit_paired_event["ts_start"] = ncclkernel_events[rank][tid]["entry_events"][i]["ts"]
                npkit_paired_event["ts_end"] = ncclkernel_events[rank][tid]["exit_events"][i]["ts"]

                for j in range(len(prim_events[rank][tid]["entry_events"])):
                    npkit_prim_event = {}
                    npkit_prim_event["event_name"] = prim_events[rank][tid]["entry_events"][j]["event_name"].replace("_ENTRY", "")

                    if "protocol" not in npkit_paired_event:
                        prim_event_name_splits = npkit_prim_event["event_name"].split("_")
                        npkit_paired_event["protocol"] = prim_event_name_splits[3]

                    npkit_prim_event["ts_start"] = prim_events[rank][tid]["entry_events"][j]["ts"]
                    npkit_prim_event["ts_end"] = prim_events[rank][tid]["exit_events"][j]["ts"]
                    npkit_prim_event["data_process_duration"] = prim_events[rank][tid]["exit_events"][j]["DataProcessTotalTime"]
                    npkit_prim_event["seq"] = len(npkit_paired_event["prim_events"])

                    if npkit_prim_event["ts_start"] >= npkit_paired_event["ts_start"] and npkit_prim_event["ts_end"] <= npkit_paired_event["ts_end"]:
                        npkit_paired_event["prim_events"].append(npkit_prim_event)

                npkit_paired_events[rank][tid].append(npkit_paired_event)

    return npkit_paired_events 

def main():
    json_file = './example_allreduce/results/npkit_run/npkit_trace/job_example_allreduce/npkit_event_trace.json'
    ncclkernel_events, prim_events = get_npkit_events(json_file)

    npkit_events_intermediate_file = "./example_allreduce/results/npkit_events_intermediate_output.json"
    with open(npkit_events_intermediate_file, "w") as json_file:
        json.dump(ncclkernel_events, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(prim_events, json_file, indent=4)
        json_file.write('\n\n')
    print("Npkit_Events has been exported to npkit_events_intermediate_output.json")

    npkit_paired_events = pair_npkit_events(ncclkernel_events, prim_events)

    npkit_paired_events_file = "./example_allreduce/results/npkit_paired_events_output.json"
    with open(npkit_paired_events_file, "w") as json_file:
        json.dump(npkit_paired_events, json_file, indent=4)
        json_file.write('\n\n')
    print("Npkit_Events has been exported to npkit_paired_events_output.json")

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