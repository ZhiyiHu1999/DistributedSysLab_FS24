import sqlite3
import os
import re
import json

def get_sqlite_events(dir_path):
    traced_events = {}

    for file_name in os.listdir(dir_path):
        nvtx_events_data = {
            "NVTX_EVENT_NET_ISEND": [],
            "NVTX_EVENT_NET_IRECV": [],
            "NVTX_EVENT_NET_SEND_TEST": [],
            "NVTX_EVENT_NET_RECV_TEST": []
            }

        cupti_kernel_data = []

        if file_name.endswith('.sqlite'):
            file_path = os.path.join(dir_path, file_name)
            file_rank = -1
            
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT text, start, end FROM NVTX_EVENTS")
            nvtx_events_results = cursor.fetchall()

            pattern_isend = r"ncclNetIsend\(\): Data_Size: (\d+), Sender_Rank: (\d+), Receiver_Rank: (\d+), Channel_ID: (\d+)"
            pattern_irecv = r"ncclNetIrecv\(\): Data_Size: (\d+), Sender_Rank: (\d+), Receiver_Rank: (\d+), Channel_ID: (\d+)"
            pattern_send_test = r"ncclNetSendTest\(\): Data_Size: (\d+), Sender_Rank: (\d+), Receiver_Rank: (\d+), Channel_ID: (\d+)"
            pattern_recv_test = r"ncclNetRecvTest\(\): Data_Size: (\d+), Sender_Rank: (\d+), Receiver_Rank: (\d+), Channel_ID: (\d+)"

            for row in nvtx_events_results:
                if row[0]:
                    match_isend = re.search(pattern_isend, row[0])
                    match_irecv = re.search(pattern_irecv, row[0])
                    match_send_test = re.search(pattern_send_test, row[0])
                    match_recv_test = re.search(pattern_recv_test, row[0])
                    if match_isend:
                        nvtx_events_data["NVTX_EVENT_NET_ISEND"].append({
                            "ts_start": row[1] // 1000, 
                            "ts_end": row[2] // 1000,
                            "sender_rank": match_isend.group(2),
                            "receiver_rank": match_isend.group(3),
                            "data_size": match_isend.group(1),
                            "channel_id": match_isend.group(4)
                            })

                        if file_rank == -1:
                            file_rank = nvtx_events_data["NVTX_EVENT_NET_ISEND"][0]["sender_rank"]
                            traced_events[file_rank] = []
                        
                    elif match_irecv:
                        nvtx_events_data["NVTX_EVENT_NET_IRECV"].append({
                            "ts_start": last_row[1] // 1000, 
                            "ts_end": last_row[2] // 1000,
                            "sender_rank": match_irecv.group(2),
                            "receiver_rank": match_irecv.group(3),
                            "data_size": match_irecv.group(1),
                            "channel_id": match_irecv.group(4)
                            })
                        
                        if file_rank == -1:
                            file_rank = nvtx_events_data["NVTX_EVENT_NET_IRECV"][0]["receiver_rank"]
                            traced_events[file_rank] = []
                        
                    elif match_send_test:
                        nvtx_events_data["NVTX_EVENT_NET_SEND_TEST"].append({
                            "ts_start": last_row[1] // 1000, 
                            "ts_end": last_row[2] // 1000,
                            "sender_rank": match_send_test.group(2),
                            "receiver_rank": match_send_test.group(3),
                            "data_size": match_send_test.group(1),
                            "channel_id": match_send_test.group(4)
                            })
                        
                    elif match_recv_test:
                        nvtx_events_data["NVTX_EVENT_NET_RECV_TEST"].append({
                            "ts_start": last_row[1] // 1000, 
                            "ts_end": last_row[2] // 1000,
                            "sender_rank": match_recv_test.group(2),
                            "receiver_rank": match_recv_test.group(3),
                            "data_size": match_recv_test.group(1),
                            "channel_id": match_recv_test.group(4)
                            })
                        
                    last_row = row
            
            cursor.execute("SELECT id, value FROM StringIds")
            string_ids = cursor.fetchall()
            string_dict = {row[0]: row[1] for row in string_ids}
            
            cursor.execute("SELECT start, end, demangledName FROM CUPTI_ACTIVITY_KIND_KERNEL")
            cupti_kernel_results = cursor.fetchall()
            for row in cupti_kernel_results:
                start, end, demangled_name = row
                if string_dict[demangled_name].startswith("ncclKernel"):
                    cupti_kernel_data.append({
                        "event_name": string_dict[demangled_name],
                        "timestamp_start": start // 1000,
                        "timestamp_end": end // 1000
                    })

            conn.close()

            # print(f"file_rank: {file_rank}")
            # print("    NVTX_EVENTS Data:")
            # print(json.dumps(nvtx_events_data, indent=8))
            
            # print("\n    CUPTI_ACTIVITY_KIND_KERNEL Data:")
            # print(json.dumps(cupti_kernel_data, indent=8))

        # Fill in traced_events[file_rank]
        for cupti_event in cupti_kernel_data:
            paired_nvtx_events_data = {
                "NVTX_EVENT_NET_ISEND": [],
                "NVTX_EVENT_NET_IRECV": [],
                "NVTX_EVENT_NET_SEND_TEST": [],
                "NVTX_EVENT_NET_RECV_TEST": []
                }

            cupti_event_name = cupti_event["event_name"]
            cupti_event_timestamp_start = cupti_event["timestamp_start"]
            cupti_event_timestamp_end = cupti_event["timestamp_end"]

            seq_paired = 0
            for seq, nvtx_event in enumerate(nvtx_events_data["NVTX_EVENT_NET_RECV_TEST"]):
                if seq >= seq_paired and nvtx_event["ts_start"] > cupti_event_timestamp_start and nvtx_event["ts_end"] < cupti_event_timestamp_end:
                    paired_nvtx_events_data["NVTX_EVENT_NET_ISEND"].append(nvtx_events_data["NVTX_EVENT_NET_ISEND"][seq])
                    paired_nvtx_events_data["NVTX_EVENT_NET_IRECV"].append(nvtx_events_data["NVTX_EVENT_NET_IRECV"][seq])
                    paired_nvtx_events_data["NVTX_EVENT_NET_SEND_TEST"].append(nvtx_events_data["NVTX_EVENT_NET_SEND_TEST"][seq])
                    paired_nvtx_events_data["NVTX_EVENT_NET_RECV_TEST"].append(nvtx_events_data["NVTX_EVENT_NET_RECV_TEST"][seq])
                    seq_paired += 1

            # seq_paired = 0
            # if len(nvtx_events_data["NVTX_EVENT_NET_ISEND"]) > 0:
            #     for seq, nvtx_event in enumerate(nvtx_events_data["NVTX_EVENT_NET_ISEND"]):
            #         if seq >= seq_paired and nvtx_event["ts_start"] > cupti_event_timestamp_start and nvtx_event["ts_end"] < cupti_event_timestamp_end:
            #             paired_nvtx_events_data["NVTX_EVENT_NET_ISEND"].append(nvtx_events_data["NVTX_EVENT_NET_ISEND"][seq])
            #             paired_nvtx_events_data["NVTX_EVENT_NET_SEND_TEST"].append(nvtx_events_data["NVTX_EVENT_NET_SEND_TEST"][seq])
            #             seq_paired += 1

            # seq_paired = 0
            # if len(nvtx_events_data["NVTX_EVENT_NET_IRECV"]) > 0:
            #     for seq, nvtx_event in enumerate(nvtx_events_data["NVTX_EVENT_NET_IRECV"]):
            #         if seq >= seq_paired and nvtx_event["ts_start"] > cupti_event_timestamp_start and nvtx_event["ts_end"] < cupti_event_timestamp_end:
            #             paired_nvtx_events_data["NVTX_EVENT_NET_IRECV"].append(nvtx_events_data["NVTX_EVENT_NET_IRECV"][seq])
            #             paired_nvtx_events_data["NVTX_EVENT_NET_RECV_TEST"].append(nvtx_events_data["NVTX_EVENT_NET_RECV_TEST"][seq])
            #             seq_paired += 1

            traced_events[file_rank].append({
                "event_name": cupti_event_name,
                "timestamp_start": cupti_event_timestamp_start,
                "timestamp_end": cupti_event_timestamp_end,
                "net_events": paired_nvtx_events_data
            })

    # print(f"traced_events: {json.dumps(traced_events, indent=4)}")

    return traced_events


def get_goal_file(events, goal_file_name):
    num_ranks = len(events)
    goal_rank = 0
    task_counter = 0
    with open(goal_file_name, 'w') as file:
        file.write(f"num_ranks {num_ranks}\n")

        for real_rank, nccl_kernel_events in events.items():
            net_event_pair_num_max = 0
            for gpu_event_id, gpu_event in enumerate(nccl_kernel_events):
                net_event_pair_num = max(len(gpu_event["net_events"]["NVTX_EVENT_NET_ISEND"]), len(gpu_event["net_events"]["NVTX_EVENT_NET_IRECV"]))
                if net_event_pair_num > net_event_pair_num_max:
                    net_event_pair_num_max = net_event_pair_num

            if net_event_pair_num_max > 0:  ## The rank has net events
                file.write(f"\nrank {goal_rank}")
                file.write(" {\n")

                for gpu_event_id, gpu_event in enumerate(nccl_kernel_events):
                    if gpu_event_id == 0:
                        task_counter += 1
                        file.write(f"l{task_counter}: calc 0\n") ## Starting point of the rank
                        last_gpu_event_ts_end = 0
                        end_calc_id = task_counter

                    task_counter += 1
                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_start"] - last_gpu_event_ts_end}\n')  ## Starting point of the gpu event
                    file.write(f"l{task_counter} requires l{end_calc_id}\n")
                    start_calc_id = task_counter

                    task_counter += 1
                    file.write(f"l{task_counter}: calc 0\n")  ## end point of a gpu event
                    end_calc_id = task_counter  ## id of the calc 0 at the end of the last gpu event

                    net_event_pair_num = max(len(gpu_event["net_events"]["NVTX_EVENT_NET_ISEND"]), len(gpu_event["net_events"]["NVTX_EVENT_NET_IRECV"]))
                    for i in range(net_event_pair_num):
                        ####
                        net_event = gpu_event["net_events"]["NVTX_EVENT_NET_ISEND"][i]
                        task_counter += 1
                        file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                        file.write(f"l{task_counter} requires l{start_calc_id}\n")

                        task_counter += 1
                        file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {net_event["channel_id"]}\n')
                        file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                        ts_net_isend_end = net_event["ts_end"]

                        ####
                        net_event = gpu_event["net_events"]["NVTX_EVENT_NET_SEND_TEST"][i]
                        task_counter += 1
                        file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                        file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                        file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                        task_counter +=1
                        file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_start"]}\n')
                        file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                        file.write(f"l{end_calc_id} requires l{task_counter}\n")

                        ####
                        net_event = gpu_event["net_events"]["NVTX_EVENT_NET_IRECV"][i]
                        task_counter += 1
                        file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                        file.write(f"l{task_counter} requires l{start_calc_id}\n")
                        ts_net_irecv_start = net_event["ts_start"]

                        net_event = gpu_event["net_events"]["NVTX_EVENT_NET_RECV_TEST"][i]
                        task_counter += 1
                        file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {net_event["channel_id"]}\n')
                        file.write(f"l{task_counter} requires l{task_counter - 1}\n")

                        task_counter += 1
                        file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                        file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                        file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                        task_counter += 1
                        file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_start"]}\n')
                        file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                        file.write(f"l{end_calc_id} requires l{task_counter}\n")

            goal_rank += 1

            file.write("}\n")


def main():
    Dir_Path = './nsys_reports'
    Nsys_Events = get_sqlite_events(Dir_Path)

    with open("nsys_events_output.json", "w") as json_file:
        json.dump(Nsys_Events, json_file, indent=4)
    print("Nsys_Events has been exported to nsys_events_output.json")

    Goal_File_Path = './example_2.goal'
    get_goal_file(Nsys_Events, Goal_File_Path)
    print("Goal file has been generated")
                
if __name__ == '__main__':
    main()