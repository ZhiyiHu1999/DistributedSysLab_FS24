import sqlite3
import os
import re
import json
import argparse

def get_sqlite_events(dir_path):
    traced_events = {}
    FileRank_To_GoalRank  = {}
    HostName_To_GoalRank = {}
    GoalRank_To_NumOfRanks = {}
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
                GoalRank_To_NumOfRanks[goal_rank] += 1
            else:
                goal_rank = len(HostName_To_GoalRank)
                HostName_To_GoalRank[host_name] = goal_rank
                GoalRank_To_NumOfRanks[goal_rank] = 1
            
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

                        if nvtx_events_data[match_isend.group(4)]["NVTX_EVENT_NET_ISEND"] == []:
                            nvtx_events_data[match_isend.group(4)]["NVTX_EVENT_NET_ISEND"].append({
                                "ts_start": row[1] // 1000, 
                                "ts_end": row[2] // 1000,
                                "sender_rank": match_isend.group(2),
                                "receiver_rank": match_isend.group(3),
                                "data_size": match_isend.group(1),
                                "channel_id": match_isend.group(4),
                                "sequence_num": match_isend.group(5)
                                })
                        
                        elif int(match_isend.group(5)) > int(nvtx_events_data[match_isend.group(4)]["NVTX_EVENT_NET_ISEND"][-1]["sequence_num"]):
                            nvtx_events_data[match_isend.group(4)]["NVTX_EVENT_NET_ISEND"].append({
                                "ts_start": row[1] // 1000, 
                                "ts_end": row[2] // 1000,
                                "sender_rank": match_isend.group(2),
                                "receiver_rank": match_isend.group(3),
                                "data_size": match_isend.group(1),
                                "channel_id": match_isend.group(4),
                                "sequence_num": match_isend.group(5)
                                })

                        elif int(match_isend.group(5)) == int(nvtx_events_data[match_isend.group(4)]["NVTX_EVENT_NET_ISEND"][-1]["sequence_num"]):  ## For duplicate netIsend() invoked in RDMA
                            nvtx_events_data[match_isend.group(4)]["NVTX_EVENT_NET_ISEND"][-1]["ts_end"] = row[2] // 1000

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
                        if nvtx_events_data[match_send_test.group(4)]["NVTX_EVENT_NET_SEND_TEST"] == []:
                            nvtx_events_data[match_send_test.group(4)]["NVTX_EVENT_NET_SEND_TEST"].append({
                                "ts_start": last_row[1] // 1000, 
                                "ts_end": last_row[2] // 1000,
                                "sender_rank": match_send_test.group(2),
                                "receiver_rank": match_send_test.group(3),
                                "data_size": match_send_test.group(1),
                                "channel_id": match_send_test.group(4),
                                "sequence_num": match_send_test.group(5)
                                })
                        
                        elif int(match_send_test.group(5)) != int(nvtx_events_data[match_send_test.group(4)]["NVTX_EVENT_NET_SEND_TEST"][-1]["sequence_num"]):
                            nvtx_events_data[match_send_test.group(4)]["NVTX_EVENT_NET_SEND_TEST"].append({
                                "ts_start": last_row[1] // 1000, 
                                "ts_end": last_row[2] // 1000,
                                "sender_rank": match_send_test.group(2),
                                "receiver_rank": match_send_test.group(3),
                                "data_size": match_send_test.group(1),
                                "channel_id": match_send_test.group(4),
                                "sequence_num": match_send_test.group(5)
                                })
                        
                        elif int(match_send_test.group(5)) == int(nvtx_events_data[match_send_test.group(4)]["NVTX_EVENT_NET_SEND_TEST"][-1]["sequence_num"]):
                            nvtx_events_data[match_send_test.group(4)]["NVTX_EVENT_NET_SEND_TEST"][-1]["ts_end"] = last_row[2] // 1000
                        
                    elif match_recv_test:
                        if nvtx_events_data[match_recv_test.group(4)]["NVTX_EVENT_NET_RECV_TEST"] == []:
                            nvtx_events_data[match_recv_test.group(4)]["NVTX_EVENT_NET_RECV_TEST"].append({
                                "ts_start": last_row[1] // 1000, 
                                "ts_end": last_row[2] // 1000,
                                "sender_rank": match_recv_test.group(2),
                                "receiver_rank": match_recv_test.group(3),
                                "data_size": match_recv_test.group(1),
                                "channel_id": match_recv_test.group(4),
                                "sequence_num": match_recv_test.group(5)
                                })
                            
                        elif int(match_recv_test.group(5)) != int(nvtx_events_data[match_recv_test.group(4)]["NVTX_EVENT_NET_RECV_TEST"][-1]["sequence_num"]):
                            nvtx_events_data[match_recv_test.group(4)]["NVTX_EVENT_NET_RECV_TEST"].append({
                                "ts_start": last_row[1] // 1000, 
                                "ts_end": last_row[2] // 1000,
                                "sender_rank": match_recv_test.group(2),
                                "receiver_rank": match_recv_test.group(3),
                                "data_size": match_recv_test.group(1),
                                "channel_id": match_recv_test.group(4),
                                "sequence_num": match_recv_test.group(5)
                                })
                            
                        elif int(match_recv_test.group(5)) == int(nvtx_events_data[match_recv_test.group(4)]["NVTX_EVENT_NET_RECV_TEST"][-1]["sequence_num"]):
                            if last_row[2] is not None:
                                nvtx_events_data[match_recv_test.group(4)]["NVTX_EVENT_NET_RECV_TEST"][-1]["ts_end"] = last_row[2] // 1000
                            nvtx_events_data[match_recv_test.group(4)]["NVTX_EVENT_NET_RECV_TEST"][-1]["data_size"] = match_recv_test.group(1)
                        
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

    return traced_events, FileRank_To_GoalRank, HostName_To_GoalRank, GoalRank_To_NumOfRanks


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
                                "NVTX_EVENT_NET_ISEND": {},
                                "NVTX_EVENT_NET_IRECV": {},
                                "NVTX_EVENT_NET_SEND_TEST": {},
                                "NVTX_EVENT_NET_RECV_TEST": {}
                                }

                        if len(nvtx_net_channel_events["NVTX_EVENT_NET_ISEND"]) > 0:
                            for net_event in nvtx_net_channel_events["NVTX_EVENT_NET_ISEND"]:
                                net_event_goal = net_event
                                net_event_goal["sender_rank"] = FileRank_To_GoalRank[net_event_goal["sender_rank"]]
                                net_event_goal["receiver_rank"] = FileRank_To_GoalRank[net_event_goal["receiver_rank"]]
                                if not merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"].get(net_event_goal["receiver_rank"]):
                                    merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"][net_event_goal["receiver_rank"]] = []
                                merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"][net_event_goal["receiver_rank"]].append(net_event_goal)

                            for net_event in nvtx_net_channel_events["NVTX_EVENT_NET_SEND_TEST"]:
                                net_event_goal = net_event
                                net_event_goal["sender_rank"] = FileRank_To_GoalRank[net_event_goal["sender_rank"]]
                                net_event_goal["receiver_rank"] = FileRank_To_GoalRank[net_event_goal["receiver_rank"]]
                                if not merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_SEND_TEST"].get(net_event_goal["receiver_rank"]):
                                    merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_SEND_TEST"][net_event_goal["receiver_rank"]] = []
                                merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_SEND_TEST"][net_event_goal["receiver_rank"]].append(net_event_goal)

                        if len(nvtx_net_channel_events["NVTX_EVENT_NET_IRECV"]) > 0:
                            for net_event in nvtx_net_channel_events["NVTX_EVENT_NET_IRECV"]:
                                net_event_goal = net_event
                                net_event_goal["sender_rank"] = FileRank_To_GoalRank[net_event_goal["sender_rank"]]
                                net_event_goal["receiver_rank"] = FileRank_To_GoalRank[net_event_goal["receiver_rank"]]
                                if not merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_IRECV"].get(net_event_goal["sender_rank"]):
                                    merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_IRECV"][net_event_goal["sender_rank"]] = []
                                merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_IRECV"][net_event_goal["sender_rank"]].append(net_event_goal)

                            for net_event in nvtx_net_channel_events["NVTX_EVENT_NET_RECV_TEST"]:
                                net_event_goal = net_event
                                net_event_goal["sender_rank"] = FileRank_To_GoalRank[net_event_goal["sender_rank"]]
                                net_event_goal["receiver_rank"] = FileRank_To_GoalRank[net_event_goal["receiver_rank"]]
                                if not merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"].get(net_event_goal["sender_rank"]):
                                    merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][net_event_goal["sender_rank"]] = []
                                merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][net_event_goal["sender_rank"]].append(net_event_goal)
    
    return merged_events

def get_goal_file_slots(events, goal_file_name, GoalRank_To_NumOfRanks):
    num_ranks = len(events)
    task_counter = 0
    with open(goal_file_name, 'w') as file:
        file.write(f"num_ranks {num_ranks}\n")

        for goal_rank in range(num_ranks):
            file.write(f"\nrank {goal_rank}")
            file.write(" {\n")

            nccl_kernel_events = events[goal_rank]
            for gpu_event_id, gpu_event in enumerate(nccl_kernel_events):
                if gpu_event_id == 0:
                    task_counter += 1
                    file.write(f"l{task_counter}: calc 0\n") ## Starting point of the rank
                    last_gpu_event_ts_end = gpu_event["timestamp_start"]
                    last_gpu_event_end_calc_id = task_counter

                task_counter += 1
                file.write(f'l{task_counter}: calc {gpu_event["timestamp_start"] - last_gpu_event_ts_end}\n')  ## Starting point of the gpu event
                file.write(f"l{task_counter} requires l{last_gpu_event_end_calc_id}\n")
                gpu_event_start_calc_id = task_counter

                task_counter += 1
                file.write(f"l{task_counter}: calc 0\n")  ## end point of a gpu event
                gpu_event_end_calc_id = task_counter  ## id of the calc 0 at the end of the last gpu event
                last_gpu_event_ts_end = gpu_event["timestamp_end"]
                last_gpu_event_end_calc_id = task_counter

                if gpu_event["event_name"].startswith("ncclKernel_AllReduce_RING"):
                    num_slots = -1
                    offset = -1

                    for channel_id, net_channel_events in gpu_event["net_events"].items():
                        for net_channel_rank_events in net_channel_events["NVTX_EVENT_NET_ISEND"].values():
                            net_event_pair_num = len(net_channel_rank_events)  ## to know the number of send/recv pairs, a pair may have multiple send/recv from different node
                            break
                        
                        for net_rank in net_channel_events["NVTX_EVENT_NET_ISEND"].keys():
                            next_rank = net_rank
                        for net_rank in net_channel_events["NVTX_EVENT_NET_IRECV"].keys():
                            previou_rank = net_rank
                        
                        if num_slots == -1:
                            num_slots = 8 // (int(net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][1]["sequence_num"]) - int(net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][0]["sequence_num"]))
                            print(f"num_slots: {num_slots}")

                        if offset == -1:
                            offset = int(GoalRank_To_NumOfRanks[goal_rank] * 2 * num_slots / 4)
                            print(f"offset: {offset}")

                        send_depends_on_send_events = {}
                        recv_depends_on_recv_events = {}
                        send_depends_on_recv_events = {}

                        for i in range(num_slots):
                            send_depends_on_send_events[i] = {}  ## send depends on send as long as slot is available
                            recv_depends_on_recv_events[i] = {}  ## recv depends on recv as long as slot is available       

                        for i in range(net_event_pair_num):
                            send_depends_on_recv_events[i] = {}

                        for i in range(net_event_pair_num):
                            slot = i % num_slots  ## 4 for Ring_Simple and 8 for others(Tree)
                            if send_depends_on_send_events[slot] == {}:
                                send_depends_on_send_events[slot]["ts_end"] = gpu_event["timestamp_start"]
                                send_depends_on_send_events[slot]["task_id"] = gpu_event_start_calc_id

                            if recv_depends_on_recv_events[slot] == {}:
                                recv_depends_on_recv_events[slot]["ts_end"] = gpu_event["timestamp_start"]
                                recv_depends_on_recv_events[slot]["task_id"] = gpu_event_start_calc_id

                            if send_depends_on_recv_events[i] == {}:
                                send_depends_on_recv_events[i]["ts_end"] = gpu_event["timestamp_start"]
                                send_depends_on_recv_events[i]["task_id"] = gpu_event_start_calc_id

                            ####
                            net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][previou_rank][i]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - recv_depends_on_recv_events[slot]["ts_end"]}\n')
                            file.write(f"l{task_counter} requires l{recv_depends_on_recv_events[slot]['task_id']}\n")
                            ts_net_irecv_start = net_event["ts_start"]

                            ####
                            net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][previou_rank][i]
                            task_counter += 1
                            file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {channel_id}\n')
                            file.write(f"l{task_counter} requires l{task_counter - 1}\n")

                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                            file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                            file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                            task_counter += 1
                            file.write(f'l{task_counter}: calc 0\n')  ## End point of a recv 
                            file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                            file.write(f"l{task_counter} requires l{task_counter - 2}\n")

                            recv_depends_on_recv_events[slot]["ts_end"] = net_event["ts_end"]
                            recv_depends_on_recv_events[slot]["task_id"] = task_counter

                            if (i + offset) < net_event_pair_num:
                                send_depends_on_recv_events[i + offset]["ts_end"] = net_event["ts_end"]  ## send(i + offset) depends on recv(i)
                                send_depends_on_recv_events[i + offset]["task_id"] = task_counter

                            if (i + num_slots) >= net_event_pair_num:
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

                            ####
                            net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][i]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc 0\n')  ## Starting point of a send (requires the end point of a previous send, requires a calc and then the end point of a previous recv )
                            net_send_event_start_calc_id = task_counter

                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_recv_events[i]["ts_end"]}\n')
                            file.write(f"l{task_counter} requires l{send_depends_on_recv_events[i]['task_id']}\n")
                            file.write(f"l{net_send_event_start_calc_id} requires l{task_counter}\n")
                            if i >= num_slots:
                                file.write(f"l{net_send_event_start_calc_id} requires l{send_depends_on_send_events[slot]['task_id']}\n")

                            task_counter += 1
                            file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {channel_id}\n')
                            file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                            ts_net_isend_end = net_event["ts_end"]

                            ####
                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][next_rank][i]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                            file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                            file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                            task_counter += 1
                            file.write(f'l{task_counter}: calc 0\n')  ## End point of a send
                            file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                            file.write(f"l{task_counter} requires l{task_counter - 2}\n")

                            send_depends_on_send_events[slot]["ts_end"] = net_event["ts_end"]
                            send_depends_on_send_events[slot]["task_id"] = task_counter

                            if (i + num_slots) >= net_event_pair_num:
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

                elif gpu_event["event_name"].startswith("ncclKernel_AllReduce_TREE"):
                    for channel_id, net_channel_events in gpu_event["net_events"].items():
                        for net_channel_rank_events in net_channel_events["NVTX_EVENT_NET_ISEND"].values():
                            net_event_pair_num = len(net_channel_rank_events)  ## to know the number of send/recv pairs, a pair may have multiple send/recv from different node
                            break

                        node_place = None     
                        parent_rank = None
                        child_1_rank = None
                        child_2_rank = None

                        if len(net_channel_events["NVTX_EVENT_NET_ISEND"]) > 1:  ## the node is in the middle of the tree
                            node_place = "010"
                            for rank, net_channel_send_test_rank_events in net_channel_events["NVTX_EVENT_NET_SEND_TEST"].items():
                                if parent_rank is None:
                                    parent_rank = rank
                                    send_to_parent_test_end = net_channel_send_test_rank_events[0]["ts_end"]
                                elif send_to_parent_test_end < net_channel_send_test_rank_events[0]["ts_end"]:
                                    if child_1_rank is None: 
                                        child_1_rank = rank
                                    else: 
                                        child_2_rank = rank
                                else:
                                    if child_1_rank is None: 
                                        child_1_rank = parent_rank
                                        parent_rank = rank
                                        send_to_parent_test_end = net_channel_send_test_rank_events[0]["ts_end"]
                                    else:
                                        child_2_rank = parent_rank
                                        parent_rank = rank
                                        send_to_parent_test_end = net_channel_send_test_rank_events[0]["ts_end"]

                        else:  ## the node is either top-most or bottom-most
                            for receiver_rank, net_channel_send_test_rank_events in net_channel_events["NVTX_EVENT_NET_SEND_TEST"].items():
                                for sender_rank, net_channel_recv_test_rank_events in net_channel_events["NVTX_EVENT_NET_RECV_TEST"].items():
                                    if net_channel_send_test_rank_events[0]["ts_end"] >= net_channel_recv_test_rank_events[0]["ts_end"]:  ## the node is top-most
                                        node_place = "100"
                                        child_1_rank = receiver_rank  ## either sender_rank or receiver_rank is fine
                                    else:  ## the node is bottom-most
                                        node_place = "001"
                                        parent_rank = receiver_rank

                        if node_place == "001":
                            send_depends_on_events = {}
                            recv_depends_on_events = {}
                            for i in range(8):
                                send_depends_on_events[i] = {}  ## send depends on send as long as slot is available
                                recv_depends_on_events[i] = {}  ## recv depends on recv as long as slot is available       

                            for i in range(net_event_pair_num):
                                slot = i % 8  ## 4 for Ring_Simple and 8 for others(Tree)
                                if send_depends_on_events[slot] == {}:
                                    send_depends_on_events[slot]["ts_end"] = gpu_event["timestamp_start"]
                                    send_depends_on_events[slot]["task_id"] = gpu_event_start_calc_id

                                if recv_depends_on_events[slot] == {}:
                                    recv_depends_on_events[slot]["ts_end"] = gpu_event["timestamp_start"]
                                    recv_depends_on_events[slot]["task_id"] = gpu_event_start_calc_id

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events[slot]["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{send_depends_on_events[slot]['task_id']}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                ts_net_isend_end = net_event["ts_end"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")

                                send_depends_on_events[slot]["ts_end"] = net_event["ts_end"]
                                send_depends_on_events[slot]["task_id"] = task_counter

                                if (i + 8) >= net_event_pair_num:
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - recv_depends_on_events[slot]["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{recv_depends_on_events[slot]['task_id']}\n")
                                ts_net_irecv_start = net_event["ts_start"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")

                                recv_depends_on_events[slot]["ts_end"] = net_event["ts_end"]
                                recv_depends_on_events[slot]["task_id"] = task_counter

                                if (i + 8) >= net_event_pair_num:
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

                        elif node_place == "010":
                            send_depends_on_events_p = {}  ## send to child depends on recv from parent
                            send_depends_on_events_c_1 = {}  ## send to parent depends on recv from child_1
                            send_depends_on_events_c_2 = {}  ## send to parent depends on recv from child_2

                            send_depends_on_events_parent = {}  ## send to parent depends on send to parent as long as the slot is available
                            send_depends_on_events_child_1 = {}  ## send to child_1 depends on send to child_1 as long as the slot is available
                            send_depends_on_events_child_2 = {}  ## send to child_2 depends on send to child_2 as long as the slot is available

                            recv_depends_on_events_parent = {}  ## recv from parent depends on recv from parent as long as the slot is available
                            recv_depends_on_events_child_1 = {}  ## recv from child_1 depends on recv from child_1 as long as the slot is available
                            recv_depends_on_events_child_2 = {}  ## recv drom child_2 depends on recv from child_2 as long as the slot is available
                            
                            for i in range(8):
                                recv_depends_on_events_parent[i] = {}
                                recv_depends_on_events_child_1[i] = {}
                                recv_depends_on_events_child_2[i] = {}  ## recv depends on recv as long as the slot is available

                                send_depends_on_events_parent[i] = {}
                                send_depends_on_events_child_1[i] = {}
                                send_depends_on_events_child_2[i] = {}  ## send depends on send as long as the slot is available
                                
                            for i in range(net_event_pair_num):
                                send_depends_on_events_p[i] = {}  ## send to child 1 and child 2 depends on recv from parent
                                send_depends_on_events_c_1[i] = {}  ## send to parent depends on recv from child 1
                                send_depends_on_events_c_2[i] = {}  ## send to parent depends on recv from child 2

                            for i in range(net_event_pair_num):
                                slot = i % 8  ## 4 for Ring_Simple and 8 for others(Tree)
                                if recv_depends_on_events_parent[slot] == {}:
                                    recv_depends_on_events_parent[slot]["ts_end"] = gpu_event["timestamp_start"]
                                    recv_depends_on_events_parent[slot]["task_id"] = gpu_event_start_calc_id
                                
                                if recv_depends_on_events_child_1[slot] == {}:
                                    recv_depends_on_events_child_1[slot]["ts_end"] = gpu_event["timestamp_start"]
                                    recv_depends_on_events_child_1[slot]["task_id"] = gpu_event_start_calc_id

                                if recv_depends_on_events_child_2[slot] == {}:
                                    recv_depends_on_events_child_2[slot]["ts_end"] = gpu_event["timestamp_start"]
                                    recv_depends_on_events_child_2[slot]["task_id"] = gpu_event_start_calc_id

                                ## recv from parent
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - recv_depends_on_events_parent[slot]["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{recv_depends_on_events_parent[slot]['task_id']}\n")
                                ts_net_irecv_start = net_event["ts_start"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")

                                recv_depends_on_events_parent[slot]["ts_end"] = net_event["ts_end"]
                                recv_depends_on_events_parent[slot]["task_id"] = task_counter

                                send_depends_on_events_p[i]["ts_end"] = net_event["ts_end"]
                                send_depends_on_events_p[i]["task_id"] = task_counter

                                if (i + 8) >= net_event_pair_num:
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                                
                                ## recv from child_1
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - recv_depends_on_events_child_1[slot]["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{recv_depends_on_events_child_1[slot]['task_id']}\n")
                                ts_net_irecv_start = net_event["ts_start"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")

                                recv_depends_on_events_child_1[slot]["ts_end"] = net_event["ts_end"]
                                recv_depends_on_events_child_1[slot]["task_id"] = task_counter

                                send_depends_on_events_c_1[i]["ts_end"] = net_event["ts_end"]
                                send_depends_on_events_c_1[i]["task_id"] = task_counter

                                if (i + 8) >= net_event_pair_num:
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

                                ## recv from child_2
                                if child_2_rank is not None:
                                    ####
                                    net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][child_2_rank][i]
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {net_event["ts_start"] - recv_depends_on_events_child_2[slot]["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{recv_depends_on_events_child_2[slot]['task_id']}\n")
                                    ts_net_irecv_start = net_event["ts_start"]

                                    ####
                                    net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][child_2_rank][i]
                                    task_counter += 1
                                    file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {channel_id}\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")

                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                    file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc 0\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{task_counter} requires l{task_counter - 2}\n")

                                    recv_depends_on_events_child_2[slot]["ts_end"] = net_event["ts_end"]
                                    recv_depends_on_events_child_2[slot]["task_id"] = task_counter

                                    send_depends_on_events_c_2[i]["ts_end"] = net_event["ts_end"]
                                    send_depends_on_events_c_2[i]["task_id"] = task_counter

                                    if (i + 8) >= net_event_pair_num:
                                        task_counter += 1
                                        file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                                        file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                        file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

                                ## send to parent
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                net_send_event_start_calc_id = task_counter

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events_c_1[i]["ts_end"]}\n')
                                # print(f'calc {net_event["ts_start"] - send_depends_on_events_child_1[i]["ts_end"]}')
                                file.write(f"l{task_counter} requires l{send_depends_on_events_c_1[i]['task_id']}\n")
                                file.write(f"l{net_send_event_start_calc_id} requires l{task_counter}\n")

                                if child_2_rank is not None:
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events_c_2[i]["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{send_depends_on_events_c_2[i]['task_id']}\n")
                                    file.write(f"l{net_send_event_start_calc_id} requires l{task_counter}\n")

                                if i >= 8:
                                    file.write(f"l{net_send_event_start_calc_id} requires l{send_depends_on_events_parent[slot]['task_id']}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                ts_net_isend_end = net_event["ts_end"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")

                                send_depends_on_events_parent[slot]["ts_end"] = net_event["ts_end"]
                                send_depends_on_events_parent[slot]['task_id'] = task_counter

                                if (i + 8) >= net_event_pair_num:
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                                
                                ## send to child_1
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                net_send_event_start_calc_id = task_counter

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events_p[i]["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{send_depends_on_events_p[i]['task_id']}\n")
                                file.write(f"l{net_send_event_start_calc_id} requires l{task_counter}\n")
                                
                                if i >= 8:
                                    file.write(f"l{net_send_event_start_calc_id} requires l{send_depends_on_events_child_1[slot]['task_id']}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                ts_net_isend_end = net_event["ts_end"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")

                                send_depends_on_events_child_1[slot]["ts_end"] = net_event["ts_end"]
                                send_depends_on_events_child_1[slot]['task_id'] = task_counter

                                if (i + 8) >= net_event_pair_num:
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

                                ## send to child_2
                                if child_2_rank is not None:
                                    ####
                                    net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][child_2_rank][i]
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc 0\n')
                                    net_send_event_start_calc_id = task_counter

                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events_p[i]["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{send_depends_on_events_p[i]['task_id']}\n")
                                    file.write(f"l{net_send_event_start_calc_id} requires l{task_counter}\n")
                                    
                                    if i >= 8:
                                        file.write(f"l{net_send_event_start_calc_id} requires l{send_depends_on_events_child_2[slot]['task_id']}\n")

                                    task_counter += 1
                                    file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {channel_id}\n')
                                    file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                    ts_net_isend_end = net_event["ts_end"]

                                    ####
                                    net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_2_rank][i]
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                                    file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                    file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc 0\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{task_counter} requires l{task_counter - 2}\n")

                                    send_depends_on_events_child_2[slot]["ts_end"] = net_event["ts_end"]
                                    send_depends_on_events_child_2[slot]['task_id'] = task_counter

                                    if (i + 8) >= net_event_pair_num:
                                        task_counter += 1
                                        file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                                        file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                        file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

                        elif node_place == "100":
                            send_depends_on_events_child = {}  ## send depends on recv from child
                            send_depends_on_events = {}  ## send depends on send as long as the slot is available
                            recv_depends_on_events = {}  ## recv depends on recv as long as the slot is available

                            for i in range(8):
                                send_depends_on_events[i] = {}
                                recv_depends_on_events[i] = {}  

                            for i in range(net_event_pair_num):
                                send_depends_on_events_child[i] = {}  ## send to child depends on recv from child

                            for i in range(net_event_pair_num):
                                slot = i % 8  ## 4 for Ring_Simple and 8 for others(Tree)
                                if recv_depends_on_events[slot] == {}:
                                    recv_depends_on_events[slot]["ts_end"] = gpu_event["timestamp_start"]
                                    recv_depends_on_events[slot]["task_id"] = gpu_event_start_calc_id

                                if send_depends_on_events[slot] == {}:
                                    send_depends_on_events[slot]["ts_end"] = gpu_event["timestamp_start"]
                                    send_depends_on_events[slot]["task_id"] = gpu_event_start_calc_id
                                
                                ## recv from child_1
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - recv_depends_on_events[slot]["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{recv_depends_on_events[slot]['task_id']}\n")
                                ts_net_irecv_start = net_event["ts_start"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")

                                recv_depends_on_events[slot]["ts_end"] = net_event["ts_end"]
                                recv_depends_on_events[slot]["task_id"] = task_counter

                                send_depends_on_events_child[i]["ts_end"] = net_event["ts_end"]
                                send_depends_on_events_child[i]["task_id"] = task_counter

                                if (i + 8) >= net_event_pair_num:
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

                                ## send to child_1
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][child_1_rank][i]

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')  ## Starting point of the send
                                net_send_event_start_calc_id = task_counter

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events_child[i]["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{send_depends_on_events_child[i]['task_id']}\n")
                                file.write(f"l{net_send_event_start_calc_id} requires l{task_counter}\n")
                                if i >= 8:
                                    file.write(f"l{net_send_event_start_calc_id} requires l{send_depends_on_events[slot]['task_id']}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                ts_net_isend_end = net_event["ts_end"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")

                                send_depends_on_events[slot]["ts_end"] = net_event["ts_end"]
                                send_depends_on_events[slot]["task_id"] = task_counter

                                if (i + 8) >= net_event_pair_num:
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

            file.write("}\n")

def get_goal_file(events, goal_file_name, GoalRank_To_NumOfRanks):
    num_ranks = len(events)
    task_counter = 0
    with open(goal_file_name, 'w') as file:
        file.write(f"num_ranks {num_ranks}\n")

        for goal_rank in range(num_ranks):
            file.write(f"\nrank {goal_rank}")
            file.write(" {\n")

            nccl_kernel_events = events[goal_rank]
            for gpu_event_id, gpu_event in enumerate(nccl_kernel_events):
                if gpu_event_id == 0:
                    task_counter += 1
                    file.write(f"l{task_counter}: calc 0\n") ## Starting point of the rank
                    last_gpu_event_ts_end = gpu_event["timestamp_start"]
                    last_gpu_event_end_calc_id = task_counter

                task_counter += 1
                file.write(f'l{task_counter}: calc {gpu_event["timestamp_start"] - last_gpu_event_ts_end}\n')  ## Starting point of the gpu event
                file.write(f"l{task_counter} requires l{last_gpu_event_end_calc_id}\n")
                gpu_event_start_calc_id = task_counter

                task_counter += 1
                file.write(f"l{task_counter}: calc 0\n")  ## end point of a gpu event
                gpu_event_end_calc_id = task_counter  ## id of the calc 0 at the end of the last gpu event
                last_gpu_event_ts_end = gpu_event["timestamp_end"]
                last_gpu_event_end_calc_id = task_counter

                if gpu_event["event_name"].startswith("ncclKernel_AllReduce_RING"):
                    num_slots = -1
                    offset = -1

                    for channel_id, net_channel_events in gpu_event["net_events"].items():
                        for net_channel_rank_events in net_channel_events["NVTX_EVENT_NET_ISEND"].values():
                            net_event_pair_num = len(net_channel_rank_events)  ## to know the number of send/recv pairs, a pair may have multiple send/recv from different node
                            break
                        
                        for net_rank in net_channel_events["NVTX_EVENT_NET_ISEND"].keys():
                            next_rank = net_rank
                        for net_rank in net_channel_events["NVTX_EVENT_NET_IRECV"].keys():
                            previou_rank = net_rank
                        
                        if num_slots == -1:
                            num_slots = 8 // (int(net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][1]["sequence_num"]) - int(net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][0]["sequence_num"]))
                            print(f"num_slots: {num_slots}")

                        if offset == -1:
                            offset = int(GoalRank_To_NumOfRanks[goal_rank] * 2 * num_slots / 4)
                            print(f"offset: {offset}")

                        recv_depends_on_events = {}
                        send_depends_on_events = {}

                        for i in range(net_event_pair_num):
                            send_depends_on_events[i] = {}

                        net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][previou_rank][0]
                        task_counter += 1
                        file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                        file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                        recv_depends_on_events["task_id_start"] = task_counter

                        net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][previou_rank][net_event_pair_num - 1]
                        task_counter += 1
                        file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                        file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                        recv_depends_on_events["task_id_end"] = task_counter

                        net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][next_rank][net_event_pair_num - 1]
                        task_counter += 1
                        file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                        file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                        send_depends_on_events["task_id_end"] = task_counter

                        task_counter += 1
                        file.write(f'l{task_counter}: calc 0\n')
                        recv_depends_on_events["task_id_last"] = task_counter

                        for i in range(net_event_pair_num):
                            if send_depends_on_events[i] == {}:
                                send_depends_on_events[i]["ts_end"] = gpu_event["timestamp_start"]
                                send_depends_on_events[i]["task_id"] = gpu_event_start_calc_id

                            ####
                            net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][previou_rank][i]   
                            task_counter += 1
                            file.write(f'l{task_counter}: calc 0\n')
                            file.write(f"l{task_counter} requires l{recv_depends_on_events['task_id_start']}\n")
                            net_recv_event_start_calc_id = task_counter

                            ts_net_irecv_start = net_event["ts_start"]

                            ####
                            net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][previou_rank][i]
                            task_counter += 1
                            file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {channel_id}\n')
                            file.write(f"l{task_counter} requires l{net_recv_event_start_calc_id}\n")

                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                            file.write(f"l{task_counter} requires l{net_recv_event_start_calc_id}\n")
                            file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                            task_counter += 1
                            file.write(f'l{task_counter}: calc 0\n')  ## End point of a recv 
                            file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                            file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                            file.write(f"l{recv_depends_on_events['task_id_end']} requires l{task_counter}\n")

                            if (i + offset) < net_event_pair_num:
                                send_depends_on_events[i + offset]["ts_end"] = net_event["ts_end"]  ## send(i + offset) depends on recv(i)
                                send_depends_on_events[i + offset]["task_id"] = task_counter
                                file.write(f"l{recv_depends_on_events['task_id_last']} requires l{task_counter}\n")

                            else:
                                file.write(f"l{net_recv_event_start_calc_id} requires l{recv_depends_on_events['task_id_last']}\n")

                            ####
                            net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][i]

                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events[i]["ts_end"]}\n')
                            file.write(f"l{task_counter} requires l{send_depends_on_events[i]['task_id']}\n")

                            task_counter += 1
                            file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {channel_id}\n')
                            file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                            ts_net_isend_end = net_event["ts_end"]

                            ####
                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][next_rank][i]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                            file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                            file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                            task_counter += 1
                            file.write(f'l{task_counter}: calc 0\n')  ## End point of a send
                            file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                            file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                            file.write(f"l{send_depends_on_events['task_id_end']} requires l{task_counter}\n")

                elif gpu_event["event_name"].startswith("ncclKernel_AllReduce_TREE"):
                    for channel_id, net_channel_events in gpu_event["net_events"].items():
                        for net_channel_rank_events in net_channel_events["NVTX_EVENT_NET_ISEND"].values():
                            net_event_pair_num = len(net_channel_rank_events)  ## to know the number of send/recv pairs, a pair may have multiple send/recv from different node
                            break

                        node_place = None     
                        parent_rank = None
                        child_1_rank = None
                        child_2_rank = None

                        if len(net_channel_events["NVTX_EVENT_NET_ISEND"]) > 1:  ## the node is in the middle of the tree
                            node_place = "010"
                            for rank, net_channel_send_test_rank_events in net_channel_events["NVTX_EVENT_NET_SEND_TEST"].items():
                                if parent_rank is None:
                                    parent_rank = rank
                                    send_to_parent_test_end = net_channel_send_test_rank_events[0]["ts_end"]
                                elif send_to_parent_test_end < net_channel_send_test_rank_events[0]["ts_end"]:
                                    if child_1_rank is None: 
                                        child_1_rank = rank
                                    else: 
                                        child_2_rank = rank
                                else:
                                    if child_1_rank is None: 
                                        child_1_rank = parent_rank
                                        parent_rank = rank
                                        send_to_parent_test_end = net_channel_send_test_rank_events[0]["ts_end"]
                                    else:
                                        child_2_rank = parent_rank
                                        parent_rank = rank
                                        send_to_parent_test_end = net_channel_send_test_rank_events[0]["ts_end"]

                        else:  ## the node is either top-most or bottom-most
                            for receiver_rank, net_channel_send_test_rank_events in net_channel_events["NVTX_EVENT_NET_SEND_TEST"].items():
                                for sender_rank, net_channel_recv_test_rank_events in net_channel_events["NVTX_EVENT_NET_RECV_TEST"].items():
                                    if net_channel_send_test_rank_events[0]["ts_end"] >= net_channel_recv_test_rank_events[0]["ts_end"]:  ## the node is top-most
                                        node_place = "100"
                                        child_1_rank = receiver_rank  ## either sender_rank or receiver_rank is fine
                                    else:  ## the node is bottom-most
                                        node_place = "001"
                                        parent_rank = receiver_rank

                        if node_place == "001":
                            recv_depends_on_events = {}
                            send_depends_on_events = {}

                            net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][parent_rank][0]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                            recv_depends_on_events["task_id_start"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][parent_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            recv_depends_on_events["task_id_end"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][parent_rank][0]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                            send_depends_on_events["task_id_start"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][parent_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            send_depends_on_events["task_id_end"] = task_counter      

                            for i in range(net_event_pair_num):
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{send_depends_on_events['task_id_start']}\n")
                                net_send_event_start_calc_id = task_counter

                                task_counter += 1
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                ts_net_isend_end = net_event["ts_end"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{send_depends_on_events['task_id_end']} requires l{task_counter}\n")

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{recv_depends_on_events['task_id_start']}\n")
                                net_recv_event_start_calc_id = task_counter

                                task_counter += 1
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{net_recv_event_start_calc_id}\n")
                                ts_net_irecv_start = net_event["ts_start"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                                file.write(f"l{task_counter} requires l{net_recv_event_start_calc_id}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{recv_depends_on_events['task_id_end']} requires l{task_counter}\n")

                        elif node_place == "010":
                            recv_from_parent_depends_on_events = {}  ## recv from parent
                            recv_from_child_1_depends_on_events = {}
                            recv_from_child_2_depends_on_events = {}
                            send_depends_on_events_parent = {}  ## send to child depends on recv from parent
                            send_depends_on_events_child_1 = {}  ## send to parent depends on recv from child_1
                            send_depends_on_events_child_2 = {}  ## send to parent depends on recv from child_2

                            for i in range(net_event_pair_num):
                                send_depends_on_events_parent[i] = {}
                                send_depends_on_events_child_1[i] = {}
                                send_depends_on_events_child_2[i] = {}
                            
                            #
                            net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][parent_rank][0]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                            recv_from_parent_depends_on_events["task_id_start"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][parent_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            recv_from_parent_depends_on_events["task_id_end"] = task_counter

                            #
                            net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][child_1_rank][0]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                            recv_from_child_1_depends_on_events["task_id_start"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][child_1_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            recv_from_child_1_depends_on_events["task_id_end"] = task_counter

                            #
                            net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][child_2_rank][0]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                            recv_from_child_2_depends_on_events["task_id_start"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][child_2_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            recv_from_child_2_depends_on_events["task_id_end"] = task_counter

                            #
                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][parent_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            send_depends_on_events_parent["task_id_end"] = task_counter

                            #
                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_1_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            send_depends_on_events_child_1["task_id_end"] = task_counter

                            #
                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_2_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            send_depends_on_events_child_2["task_id_end"] = task_counter

                            for i in range(net_event_pair_num):
                                ## recv from parent
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{recv_from_parent_depends_on_events['task_id_start']}\n")
                                net_recv_event_start_calc_id = task_counter

                                ts_net_irecv_start = net_event["ts_start"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{net_recv_event_start_calc_id}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                                file.write(f"l{task_counter} requires l{net_recv_event_start_calc_id}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{recv_from_parent_depends_on_events['task_id_end']} requires l{task_counter}\n")

                                send_depends_on_events_parent[i]["ts_end"] = net_event["ts_end"]
                                send_depends_on_events_parent[i]["task_id"] = task_counter
                                
                                ## recv from child_1
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{recv_from_child_1_depends_on_events['task_id_start']}\n")
                                net_recv_event_start_calc_id = task_counter

                                ts_net_irecv_start = net_event["ts_start"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{net_recv_event_start_calc_id}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                                file.write(f"l{task_counter} requires l{net_recv_event_start_calc_id}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{recv_from_child_1_depends_on_events['task_id_end']} requires l{task_counter}\n")

                                send_depends_on_events_child_1[i]["ts_end"] = net_event["ts_end"]
                                send_depends_on_events_child_1[i]["task_id"] = task_counter

                                ## recv from child_2
                                if child_2_rank is not None:
                                    ####
                                    net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][child_2_rank][i]
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc 0\n')
                                    file.write(f"l{task_counter} requires l{recv_from_child_2_depends_on_events['task_id_start']}\n")
                                    net_recv_event_start_calc_id = task_counter

                                    ts_net_irecv_start = net_event["ts_start"]

                                    ####
                                    net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][child_2_rank][i]
                                    task_counter += 1
                                    file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {channel_id}\n')
                                    file.write(f"l{task_counter} requires l{net_recv_event_start_calc_id}\n")

                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                                    file.write(f"l{task_counter} requires l{net_recv_event_start_calc_id}\n")
                                    file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc 0\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                    file.write(f"l{recv_from_child_2_depends_on_events['task_id_end']} requires l{task_counter}\n")

                                    send_depends_on_events_child_2[i]["ts_end"] = net_event["ts_end"]
                                    send_depends_on_events_child_2[i]["task_id"] = task_counter

                                ## send to parent
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                net_send_event_start_calc_id = task_counter

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events_child_1[i]["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{send_depends_on_events_child_1[i]['task_id']}\n")
                                file.write(f"l{net_send_event_start_calc_id} requires l{task_counter}\n")

                                if child_2_rank is not None:
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events_child_2[i]["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{send_depends_on_events_child_2[i]['task_id']}\n")
                                    file.write(f"l{net_send_event_start_calc_id} requires l{task_counter}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                ts_net_isend_end = net_event["ts_end"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][parent_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{send_depends_on_events_parent['task_id']} requires l{task_counter}\n")
                                
                                ## send to child_1
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                net_send_event_start_calc_id = task_counter

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events_parent[i]["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{send_depends_on_events_parent[i]['task_id']}\n")
                                file.write(f"l{net_send_event_start_calc_id} requires l{task_counter}\n")
                                
                                task_counter += 1
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                ts_net_isend_end = net_event["ts_end"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{send_depends_on_events_child_1['task_id']} requires l{task_counter}\n")
                                
                                ## send to child_2
                                if child_2_rank is not None:
                                    ####
                                    net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][child_2_rank][i]
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc 0\n')
                                    net_send_event_start_calc_id = task_counter

                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events_parent[i]["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{send_depends_on_events_parent[i]['task_id']}\n")
                                    file.write(f"l{net_send_event_start_calc_id} requires l{task_counter}\n")
                                    
                                    task_counter += 1
                                    file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {channel_id}\n')
                                    file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                    ts_net_isend_end = net_event["ts_end"]

                                    ####
                                    net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_2_rank][i]
                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                                    file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                    file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                    task_counter += 1
                                    file.write(f'l{task_counter}: calc 0\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                    file.write(f"l{send_depends_on_events_child_2['task_id']} requires l{task_counter}\n")

                        elif node_place == "100":
                            recv_depends_on_events = {}
                            send_depends_on_events = {}  ## send to child depends on recv from child

                            for i in range(net_event_pair_num):
                                send_depends_on_events[i] = {}
                            
                            #
                            net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][child_1_rank][0]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                            recv_depends_on_events["task_id_start"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][child_1_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            recv_depends_on_events["task_id_end"] = task_counter

                            #
                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_1_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            send_depends_on_events["task_id_end"] = task_counter

                            for i in range(net_event_pair_num):
                                ## recv from child_1
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{recv_depends_on_events['task_id_start']}\n")
                                net_recv_event_start_calc_id = task_counter

                                ts_net_irecv_start = net_event["ts_start"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{net_recv_event_start_calc_id}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_irecv_start}\n')
                                file.write(f"l{task_counter} requires l{net_recv_event_start_calc_id}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{recv_depends_on_events['task_id_end']} requires l{task_counter}\n")

                                send_depends_on_events[i]["ts_end"] = net_event["ts_end"]
                                send_depends_on_events[i]["task_id"] = task_counter

                                ## send to child_1
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                net_send_event_start_calc_id = task_counter

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events[i]["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{send_depends_on_events[i]['task_id']}\n")
                                file.write(f"l{net_send_event_start_calc_id} requires l{task_counter}\n")
                                
                                task_counter += 1
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {channel_id}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                ts_net_isend_end = net_event["ts_end"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_1_rank][i]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - ts_net_isend_end}\n')
                                file.write(f"l{task_counter} requires l{net_send_event_start_calc_id}\n")
                                file.write(f"l{task_counter} irequires l{task_counter - 1}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{task_counter} requires l{task_counter - 2}\n")
                                file.write(f"l{send_depends_on_events['task_id_end']} requires l{task_counter}\n")
                                
            file.write("}\n")


def main():
    parser = argparse.ArgumentParser(description='Process SQLite to Goal file.')
    
    parser.add_argument('-r', '--use-slots', action='store_true',
                        help='Use get_goal_file_slots instead of get_goal_file.')

    args = parser.parse_args()

    Dir_Path = './results/nsys_reports'
    Nsys_Events, FileRank_2_GoalRank, HostName_2_GoalRank, GoalRank_2_NumOfRanks  = get_sqlite_events(Dir_Path)

    with open("./results/nsys_events_intermediate_output.json", "w") as json_file:
        json.dump(GoalRank_2_NumOfRanks, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(FileRank_2_GoalRank, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(HostName_2_GoalRank, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(Nsys_Events, json_file, indent=4)
    print("Nsys_Events has been exported to nsys_events_intermediate_output.json")

    Merged_Nsys_Events = merge_nsys_events(Nsys_Events, FileRank_2_GoalRank, HostName_2_GoalRank)
    with open("./results/nsys_events_merged_output.json", "w") as json_file:
        json.dump(Merged_Nsys_Events, json_file, indent=4)
    print("Merged_Nsys_Events has been exported to nsys_events_merged_output.json")

    Goal_File_Path = './results/example_2.goal'
    if args.use_slots:
        get_goal_file_slots(Merged_Nsys_Events, Goal_File_Path, GoalRank_2_NumOfRanks)
        print("Final goal file has been generated using get_goal_file_slots.")
    else:
        get_goal_file(Merged_Nsys_Events, Goal_File_Path, GoalRank_2_NumOfRanks)
        print("Final goal file has been generated using get_goal_file.")
                
if __name__ == '__main__':
    main()