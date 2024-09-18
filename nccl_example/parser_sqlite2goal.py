import sqlite3
import os
import re
import json

def get_sqlite_events(dir_path):
    traced_events = {}
    FileRank_To_GoalRank  = {}
    HostName_To_GoalRank = {}
    pattern_HostName = r'nsys_report_([^.]+)\.'

    for file_name in os.listdir(dir_path):  ## each file represents a rank
        nvtx_events_data = {}
        cupti_kernel_data = []

        if file_name.endswith('.sqlite'):
            file_path = os.path.join(dir_path, file_name)
            file_rank = -1

            match = re.search(pattern_HostName, file_name)
            if match:
                host_name = match.group(1)
                print(f"Host Name: {host_name}")

            if host_name in HostName_To_GoalRank:
                goal_rank = HostName_To_GoalRank[host_name]
            else:
                goal_rank = len(HostName_To_GoalRank)
                HostName_To_GoalRank[host_name] = goal_rank
            
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()

            cursor.execute("SELECT text, start, end FROM NVTX_EVENTS")
            nvtx_events_results = cursor.fetchall()

            pattern_isend = r"ncclNetIsend\(\): Data_Size: (\d+), Sender_Rank: (\d+), Receiver_Rank: (\d+), Channel_ID: (\d+), Sequence: (\d+)"
            pattern_irecv = r"ncclNetIrecv\(\): Data_Size: (\d+), Sender_Rank: (\d+), Receiver_Rank: (\d+), Channel_ID: (\d+), Sequence: (\d+)"
            pattern_send_test = r"ncclNetSendTest\(\): Data_Size: (\d+), Sender_Rank: (\d+), Receiver_Rank: (\d+), Channel_ID: (\d+), Sequence: (\d+)"
            pattern_recv_test = r"ncclNetRecvTest\(\): Data_Size: (\d+), Sender_Rank: (\d+), Receiver_Rank: (\d+), Channel_ID: (\d+), Sequence: (\d+)"

            for row in nvtx_events_results:
                if row[0]:
                    match_isend = re.search(pattern_isend, row[0])
                    match_irecv = re.search(pattern_irecv, row[0])
                    match_send_test = re.search(pattern_send_test, row[0])
                    match_recv_test = re.search(pattern_recv_test, row[0])
                    if match_isend:
                        if not nvtx_events_data.get(match_isend.group(4)):
                            nvtx_events_data[match_isend.group(4)] = {
                                "NVTX_EVENT_NET_ISEND": [],
                                "NVTX_EVENT_NET_IRECV": [],
                                "NVTX_EVENT_NET_SEND_TEST": [],
                                "NVTX_EVENT_NET_RECV_TEST": []
                                }

                        nvtx_events_data[match_isend.group(4)]["NVTX_EVENT_NET_ISEND"].append({
                            "ts_start": row[1] // 1000, 
                            "ts_end": row[2] // 1000,
                            "sender_rank": match_isend.group(2),
                            "receiver_rank": match_isend.group(3),
                            "data_size": match_isend.group(1),
                            "channel_id": match_isend.group(4),
                            "sequence_num": match_isend.group(5)
                            })

                        if file_rank == -1:
                            file_rank = nvtx_events_data[match_isend.group(4)]["NVTX_EVENT_NET_ISEND"][0]["sender_rank"]
                            traced_events[file_rank] = []
                        
                    elif match_irecv:
                        if not nvtx_events_data.get(match_irecv.group(4)):
                            nvtx_events_data[match_irecv.group(4)] = {
                                "NVTX_EVENT_NET_ISEND": [],
                                "NVTX_EVENT_NET_IRECV": [],
                                "NVTX_EVENT_NET_SEND_TEST": [],
                                "NVTX_EVENT_NET_RECV_TEST": []
                                }
                            
                        nvtx_events_data[match_irecv.group(4)]["NVTX_EVENT_NET_IRECV"].append({
                            "ts_start": last_row[1] // 1000, 
                            "ts_end": last_row[2] // 1000,
                            "sender_rank": match_irecv.group(2),
                            "receiver_rank": match_irecv.group(3),
                            "data_size": match_irecv.group(1),
                            "channel_id": match_irecv.group(4),
                            "sequence_num": match_irecv.group(5)
                            })
                        
                        if file_rank == -1:
                            file_rank = nvtx_events_data[match_irecv.group(4)]["NVTX_EVENT_NET_IRECV"][0]["receiver_rank"]
                            traced_events[file_rank] = []
                        
                    elif match_send_test:
                        nvtx_events_data[match_send_test.group(4)]["NVTX_EVENT_NET_SEND_TEST"].append({
                            "ts_start": last_row[1] // 1000, 
                            "ts_end": last_row[2] // 1000,
                            "sender_rank": match_send_test.group(2),
                            "receiver_rank": match_send_test.group(3),
                            "data_size": match_send_test.group(1),
                            "channel_id": match_send_test.group(4),
                            "sequence_num": match_send_test.group(5)
                            })
                        
                    elif match_recv_test:
                        nvtx_events_data[match_recv_test.group(4)]["NVTX_EVENT_NET_RECV_TEST"].append({
                            "ts_start": last_row[1] // 1000, 
                            "ts_end": last_row[2] // 1000,
                            "sender_rank": match_recv_test.group(2),
                            "receiver_rank": match_recv_test.group(3),
                            "data_size": match_recv_test.group(1),
                            "channel_id": match_recv_test.group(4),
                            "sequence_num": match_recv_test.group(5)
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
        for cupti_event_seq, cupti_event in enumerate(cupti_kernel_data):
            # paired_nvtx_events_data = {
            #     "NVTX_EVENT_NET_ISEND": [],
            #     "NVTX_EVENT_NET_IRECV": [],
            #     "NVTX_EVENT_NET_SEND_TEST": [],
            #     "NVTX_EVENT_NET_RECV_TEST": []
            #     }
            paired_nvtx_events_data = {}

            cupti_event_name = cupti_event["event_name"]
            cupti_event_timestamp_start = cupti_event["timestamp_start"]
            cupti_event_timestamp_end = cupti_event["timestamp_end"]
            if cupti_event_seq + 1 < len(cupti_kernel_data):
                next_cupti_event_timestamp_start = cupti_kernel_data[cupti_event_seq + 1]["timestamp_start"]
            else:
                next_cupti_event_timestamp_start = 1e31

            
            for channel, nvtx_events_channel_data in nvtx_events_data.items():
                if not paired_nvtx_events_data.get(channel):
                    paired_nvtx_events_data[channel] = {
                        "NVTX_EVENT_NET_ISEND": [],
                        "NVTX_EVENT_NET_IRECV": [],
                        "NVTX_EVENT_NET_SEND_TEST": [],
                        "NVTX_EVENT_NET_RECV_TEST": []
                        }

                seq_paired = 0
                if len(nvtx_events_channel_data["NVTX_EVENT_NET_ISEND"]) > 0:
                    for seq, nvtx_event in enumerate(nvtx_events_channel_data["NVTX_EVENT_NET_ISEND"]):
                        if seq >= seq_paired and nvtx_event["ts_start"] > cupti_event_timestamp_start and nvtx_event["ts_start"] < next_cupti_event_timestamp_start:
                            paired_nvtx_events_data[channel]["NVTX_EVENT_NET_ISEND"].append(nvtx_events_channel_data["NVTX_EVENT_NET_ISEND"][seq])
                            paired_nvtx_events_data[channel]["NVTX_EVENT_NET_SEND_TEST"].append(nvtx_events_channel_data["NVTX_EVENT_NET_SEND_TEST"][seq])
                            seq_paired += 1
                            cupti_event_timestamp_start = min(nvtx_events_channel_data["NVTX_EVENT_NET_ISEND"][seq]["ts_start"], cupti_event_timestamp_start)
                            cupti_event_timestamp_end = max(nvtx_events_channel_data["NVTX_EVENT_NET_SEND_TEST"][seq]["ts_end"], cupti_event_timestamp_end)

                seq_paired = 0
                if len(nvtx_events_channel_data["NVTX_EVENT_NET_IRECV"]) > 0:
                    for seq, nvtx_event in enumerate(nvtx_events_channel_data["NVTX_EVENT_NET_IRECV"]):
                        if seq >= seq_paired and nvtx_event["ts_start"] > cupti_event_timestamp_start and nvtx_event["ts_end"] < next_cupti_event_timestamp_start:
                            paired_nvtx_events_data[channel]["NVTX_EVENT_NET_IRECV"].append(nvtx_events_channel_data["NVTX_EVENT_NET_IRECV"][seq])
                            paired_nvtx_events_data[channel]["NVTX_EVENT_NET_RECV_TEST"].append(nvtx_events_channel_data["NVTX_EVENT_NET_RECV_TEST"][seq])
                            seq_paired += 1
                            cupti_event_timestamp_start = min(nvtx_events_channel_data["NVTX_EVENT_NET_IRECV"][seq]["ts_start"], cupti_event_timestamp_start)
                            cupti_event_timestamp_end = max(nvtx_events_channel_data["NVTX_EVENT_NET_RECV_TEST"][seq]["ts_end"], cupti_event_timestamp_end)

            if file_rank != -1:  ## No net events happens if file_rank == -1
                traced_events[file_rank].append({
                    "event_name": cupti_event_name,
                    "timestamp_start": cupti_event_timestamp_start,
                    "timestamp_end": cupti_event_timestamp_end,
                    "net_events": paired_nvtx_events_data
                })

                FileRank_To_GoalRank[file_rank] = goal_rank

    # print(f"traced_events: {json.dumps(traced_events, indent=4)}")

    return traced_events, FileRank_To_GoalRank, HostName_To_GoalRank


def merge_nsys_events(traced_events, FileRank_To_GoalRank, HostName_To_GoalRank):
    num_ranks = len(HostName_To_GoalRank)
    merged_events = {}
    for goal_rank in range(num_ranks):
        merged_events[goal_rank] = []

        for file_rank_, nccl_kernel_events_ in traced_events.items():
            nccl_kernel_event_num = len(nccl_kernel_events_)
            num_channels = len(nccl_kernel_events_[0]["net_events"])
            break

        for nccl_kernel_event_id in range(nccl_kernel_event_num):
            merged_events[goal_rank].append({})
            merged_events[goal_rank][nccl_kernel_event_id]["net_events"] = {}
            merged_events[goal_rank][nccl_kernel_event_id]["timestamp_start"] = None
            merged_events[goal_rank][nccl_kernel_event_id]["timestamp_end"] = None

            for file_rank, nccl_kernel_events in traced_events.items():
                if FileRank_To_GoalRank[file_rank] == goal_rank:
                    merged_events[goal_rank][nccl_kernel_event_id]["event_name"] =  nccl_kernel_events[nccl_kernel_event_id]["event_name"]
                    
                    if merged_events[goal_rank][nccl_kernel_event_id]["timestamp_start"]:
                        merged_events[goal_rank][nccl_kernel_event_id]["timestamp_start"] = min(merged_events[goal_rank][nccl_kernel_event_id]["timestamp_start"], nccl_kernel_events[nccl_kernel_event_id]["timestamp_start"])
                    else:
                        merged_events[goal_rank][nccl_kernel_event_id]["timestamp_start"] = nccl_kernel_events[nccl_kernel_event_id]["timestamp_start"]

                    if merged_events[goal_rank][nccl_kernel_event_id]["timestamp_end"]:
                        merged_events[goal_rank][nccl_kernel_event_id]["timestamp_end"] = max(merged_events[goal_rank][nccl_kernel_event_id]["timestamp_end"], nccl_kernel_events[nccl_kernel_event_id]["timestamp_end"])
                    else:
                        merged_events[goal_rank][nccl_kernel_event_id]["timestamp_end"] = nccl_kernel_events[nccl_kernel_event_id]["timestamp_end"]

                    nvtx_net_events = nccl_kernel_events[nccl_kernel_event_id]["net_events"]
                    for channel_id, nvtx_net_channel_events in nvtx_net_events.items():
                        if not merged_events[goal_rank][nccl_kernel_event_id]["net_events"].get(channel_id):
                            merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id] = {
                                "NVTX_EVENT_NET_ISEND": [],
                                "NVTX_EVENT_NET_IRECV": [],
                                "NVTX_EVENT_NET_SEND_TEST": [],
                                "NVTX_EVENT_NET_RECV_TEST": []
                                }

                        if len(nvtx_net_channel_events["NVTX_EVENT_NET_ISEND"]) > 0:
                            for net_event in nvtx_net_channel_events["NVTX_EVENT_NET_ISEND"]:
                                net_event_goal = net_event
                                net_event_goal["sender_rank"] = FileRank_To_GoalRank[net_event_goal["sender_rank"]]
                                net_event_goal["receiver_rank"] = FileRank_To_GoalRank[net_event_goal["receiver_rank"]]
                                merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"].append(net_event_goal)

                            for net_event in nvtx_net_channel_events["NVTX_EVENT_NET_SEND_TEST"]:
                                net_event_goal = net_event
                                net_event_goal["sender_rank"] = FileRank_To_GoalRank[net_event_goal["sender_rank"]]
                                net_event_goal["receiver_rank"] = FileRank_To_GoalRank[net_event_goal["receiver_rank"]]
                                merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_SEND_TEST"].append(net_event_goal)

                        if len(nvtx_net_channel_events["NVTX_EVENT_NET_IRECV"]) > 0:
                            for net_event in nvtx_net_channel_events["NVTX_EVENT_NET_IRECV"]:
                                net_event_goal = net_event
                                net_event_goal["sender_rank"] = FileRank_To_GoalRank[net_event_goal["sender_rank"]]
                                net_event_goal["receiver_rank"] = FileRank_To_GoalRank[net_event_goal["receiver_rank"]]
                                merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_IRECV"].append(net_event_goal)

                            for net_event in nvtx_net_channel_events["NVTX_EVENT_NET_RECV_TEST"]:
                                net_event_goal = net_event
                                net_event_goal["sender_rank"] = FileRank_To_GoalRank[net_event_goal["sender_rank"]]
                                net_event_goal["receiver_rank"] = FileRank_To_GoalRank[net_event_goal["receiver_rank"]]
                                merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"].append(net_event_goal)
    
    return merged_events


def get_intermediate_goal_file(events, goal_file_name):
    num_ranks = len(events)
    # goal_rank = 0
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
                # file.write(f"\nrank {goal_rank}")
                file.write(f"\nrank {real_rank}")
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
                        if len(gpu_event["net_events"]["NVTX_EVENT_NET_ISEND"]) > 0:
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

                        if len(gpu_event["net_events"]["NVTX_EVENT_NET_IRECV"]) > 0:
                            ####
                            net_event = gpu_event["net_events"]["NVTX_EVENT_NET_IRECV"][i]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{start_calc_id}\n")
                            ts_net_irecv_start = net_event["ts_start"]

                            ####
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

            # goal_rank += 1

            file.write("}\n")

def get_goal_file(events, goal_file_name):
    num_ranks = len(events)
    task_counter = 0
    with open(goal_file_name, 'w') as file:
        file.write(f"num_ranks {num_ranks}\n")

        for goal_rank in range(num_ranks):
            nccl_kernel_events = events[goal_rank]
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
                        if len(gpu_event["net_events"]["NVTX_EVENT_NET_ISEND"]) > 0:
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

                        if len(gpu_event["net_events"]["NVTX_EVENT_NET_IRECV"]) > 0:
                            ####
                            net_event = gpu_event["net_events"]["NVTX_EVENT_NET_IRECV"][i]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{start_calc_id}\n")
                            ts_net_irecv_start = net_event["ts_start"]

                            ####
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

            # goal_rank += 1

            file.write("}\n")


def main():
    Dir_Path = './results/nsys_reports'
    Nsys_Events, FileRank_2_GoalRank, HostName_2_GoalRank  = get_sqlite_events(Dir_Path)

    with open("./results/nsys_events_intermediate_output.json", "w") as json_file:
        json.dump(FileRank_2_GoalRank, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(HostName_2_GoalRank, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(Nsys_Events, json_file, indent=4)
    print("Nsys_Events has been exported to nsys_events_intermediate_output.json")

    # Intermediate_Goal_File_Path = './results/example_2_intermediate.goal'
    # get_intermediate_goal_file(Nsys_Events, Intermediate_Goal_File_Path)
    # print("Intermediate goal file has been generated")

    Merged_Nsys_merged_Events = merge_nsys_events(Nsys_Events, FileRank_2_GoalRank, HostName_2_GoalRank)
    with open("./results/nsys_events_merged_output.json", "w") as json_file:
        json.dump(Merged_Nsys_merged_Events, json_file, indent=4)
    print("Merged_Nsys_Events has been exported to nsys_events_merged_output.json")

    # Goal_File_Path = './results/example_2.goal'
    # get_intermediate_goal_file(Merged_Nsys_Events, Goal_File_Path)
    # print("Final goal file has been generated")
                
if __name__ == '__main__':
    main()