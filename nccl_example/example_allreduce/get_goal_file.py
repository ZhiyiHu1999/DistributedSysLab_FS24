import sqlite3
import os
import re
import json
import argparse

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
                last_gpu_event_ts_end = gpu_event["timestamp_all_end"]
                last_gpu_event_end_calc_id = task_counter

                if gpu_event["event_name"].startswith("ncclKernel_AllReduce_RING") or gpu_event["event_name"].startswith("ncclDevKernel_AllReduce_RING") or gpu_event["event_name"].startswith("ncclKernel_AllGather_RING") or gpu_event["event_name"].startswith("ncclDevKernel_AllGather_RING"):
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
                            offset = int(GoalRank_To_NumOfRanks[goal_rank] * 2)
                            # offset = int(GoalRank_To_NumOfRanks[goal_rank] * 2) if num_slots == 4 else int(GoalRank_To_NumOfRanks[goal_rank])
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
                            tag = net_event["sequence_num"] + channel_id.zfill(2)
                            file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                                file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                            tag = net_event["sequence_num"] + channel_id.zfill(2)
                            file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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
                                file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

                elif gpu_event["event_name"].startswith("ncclKernel_AllReduce_TREE") or gpu_event["event_name"].startswith("ncclDevKernel_AllReduce_Sum_f32_TREE"):
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                                    tag = net_event["sequence_num"] + channel_id.zfill(2)
                                    file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                                        file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                                    tag = net_event["sequence_num"] + channel_id.zfill(2)
                                    file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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
                                        file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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
                                    file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                                    file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                    file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

            file.write("}\n")

def get_goal_file(events, goal_file_name, GoalRank_To_NumOfRanks):
    num_ranks = len(events)

    num_gpus = 0
    for gpu_amount in GoalRank_To_NumOfRanks.values():
        num_gpus += gpu_amount
    print(f'num_gpus: {num_gpus}')
    
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
                last_gpu_event_ts_end = gpu_event["timestamp_all_end"]
                last_gpu_event_end_calc_id = task_counter

                if gpu_event["event_name"].startswith("ncclKernel_AllReduce_RING") or gpu_event["event_name"].startswith("ncclDevKernel_AllReduce_RING"):
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
                            offset = int(GoalRank_To_NumOfRanks[goal_rank] * 2)
                            # offset = int(GoalRank_To_NumOfRanks[goal_rank] * 2 * num_slots / 4) if num_slots == 4 else int(GoalRank_To_NumOfRanks[goal_rank])
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
                        file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                        file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                        recv_depends_on_events["task_id_end"] = task_counter

                        net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][next_rank][net_event_pair_num - 1]
                        task_counter += 1
                        file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                        file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                        send_depends_on_events["task_id_end"] = task_counter

                        # task_counter += 1
                        # file.write(f'l{task_counter}: calc 0\n')
                        # recv_depends_on_events["task_id_last"] = task_counter

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
                            tag = net_event["sequence_num"] + channel_id.zfill(2)
                            file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                                if (i + offset) % ((num_gpus - 1) * 2 * 2) >= GoalRank_To_NumOfRanks[goal_rank] * 2:
                                    send_depends_on_events[i + offset]["task_id"] = task_counter
                                else:
                                    send_depends_on_events[i + offset]["task_id"] = gpu_event_start_calc_id
                            #     file.write(f"l{recv_depends_on_events['task_id_last']} requires l{task_counter}\n")

                            # else:
                            #     file.write(f"l{net_recv_event_start_calc_id} requires l{recv_depends_on_events['task_id_last']}\n")

                            ####
                            net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][i]

                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events[i]["ts_end"]}\n')
                            file.write(f"l{task_counter} requires l{send_depends_on_events[i]['task_id']}\n")

                            task_counter += 1
                            tag = net_event["sequence_num"] + channel_id.zfill(2)
                            file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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

                elif gpu_event["event_name"].startswith("ncclKernel_AllReduce_TREE") or gpu_event["event_name"].startswith("ncclDevKernel_AllReduce_Sum_f32_TREE"):
                    # num_slots = 8
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
                                    # # if net_channel_send_test_rank_events[0]["ts_end"] >= net_channel_recv_test_rank_events[0]["ts_end"]:  ## the node is top-most
                                    # if net_channel_send_test_rank_events[-1]["ts_end"] >= net_channel_recv_test_rank_events[-1]["ts_end"]:  ## the node is top-most
                                    #     node_place = "100"
                                    #     child_1_rank = receiver_rank  ## either sender_rank or receiver_rank is fine
                                    # else:  ## the node is bottom-most
                                    #     node_place = "001"
                                    #     parent_rank = receiver_rank
                                    node_place = "100"
                                    for i in range(len(net_channel_send_test_rank_events)):
                                        if net_channel_send_test_rank_events[i]["ts_end"] < net_channel_recv_test_rank_events[i]["ts_end"]:
                                            node_place = "001"

                                    if node_place == "100":
                                        child_1_rank = receiver_rank  ## either sender_rank or receiver_rank is fine
                                    elif node_place == "001":
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
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            recv_depends_on_events["task_id_end"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][parent_rank][0]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                            send_depends_on_events["task_id_start"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][parent_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            recv_from_child_1_depends_on_events["task_id_end"] = task_counter

                            #
                            if child_2_rank is not None:
                                net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][child_2_rank][0]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                                file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                                recv_from_child_2_depends_on_events["task_id_start"] = task_counter

                                net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][child_2_rank][net_event_pair_num - 1]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                                file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                                recv_from_child_2_depends_on_events["task_id_end"] = task_counter

                            #
                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][parent_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            send_depends_on_events_parent["task_id_end"] = task_counter

                            #
                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_1_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            send_depends_on_events_child_1["task_id_end"] = task_counter

                            #
                            if child_2_rank is not None:
                                net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_2_rank][net_event_pair_num - 1]
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                                    tag = net_event["sequence_num"] + channel_id.zfill(2)
                                    file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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
                                file.write(f"l{send_depends_on_events_parent['task_id_end']} requires l{task_counter}\n")
                                
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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
                                file.write(f"l{send_depends_on_events_child_1['task_id_end']} requires l{task_counter}\n")
                                
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
                                    tag = net_event["sequence_num"] + channel_id.zfill(2)
                                    file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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
                                    file.write(f"l{send_depends_on_events_child_2['task_id_end']} requires l{task_counter}\n")

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
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            recv_depends_on_events["task_id_end"] = task_counter

                            #
                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_1_rank][net_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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

                elif gpu_event["event_name"].startswith("ncclKernel_AllGather_RING") or gpu_event["event_name"].startswith("ncclDevKernel_AllGather_RING"):
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
                            offset = int(GoalRank_To_NumOfRanks[goal_rank] * 2)
                            # offset = int(GoalRank_To_NumOfRanks[goal_rank] * 2 * num_slots / 4) if num_slots == 4 else int(GoalRank_To_NumOfRanks[goal_rank])
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
                        file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                        file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                        recv_depends_on_events["task_id_end"] = task_counter

                        net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][next_rank][net_event_pair_num - 1]
                        task_counter += 1
                        file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                        file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                        send_depends_on_events["task_id_end"] = task_counter

                        # task_counter += 1
                        # file.write(f'l{task_counter}: calc 0\n')
                        # recv_depends_on_events["task_id_last"] = task_counter

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
                            tag = net_event["sequence_num"] + channel_id.zfill(2)
                            file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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
                                if (i + offset) % ((num_gpus - 1) * 2) >= GoalRank_To_NumOfRanks[goal_rank] * 2:
                                    send_depends_on_events[i + offset]["task_id"] = task_counter
                                else:
                                    send_depends_on_events[i + offset]["task_id"] = gpu_event_start_calc_id
                            #     file.write(f"l{recv_depends_on_events['task_id_last']} requires l{task_counter}\n")

                            # else:
                            #     file.write(f"l{net_recv_event_start_calc_id} requires l{recv_depends_on_events['task_id_last']}\n")

                            ####
                            net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][i]

                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events[i]["ts_end"]}\n')
                            file.write(f"l{task_counter} requires l{send_depends_on_events[i]['task_id']}\n")

                            task_counter += 1
                            tag = net_event["sequence_num"] + channel_id.zfill(2)
                            file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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

                elif gpu_event["event_name"].startswith("ncclKernel_Broadcast_RING") or gpu_event["event_name"].startswith("ncclDevKernel_Broadcast_RING"):
                    # num_slots = 8
                    for channel_id, net_channel_events in gpu_event["net_events"].items():
                        net_send_event_pair_num = -1
                        net_recv_event_pair_num = -1

                        for net_channel_rank_events in net_channel_events["NVTX_EVENT_NET_ISEND"].values():
                            net_send_event_pair_num = len(net_channel_rank_events)  
                            print(f'net_send_event_pair_num: {net_send_event_pair_num}')

                        for net_channel_rank_events in net_channel_events["NVTX_EVENT_NET_IRECV"].values():
                            net_recv_event_pair_num = len(net_channel_rank_events)
                            print(f'net_recv_event_pair_num: {net_recv_event_pair_num}')

                        node_place = None     
                        previous_rank = None
                        next_rank = None

                        if net_send_event_pair_num > 0 and net_recv_event_pair_num == -1:  ## the node is at the start of the Ring
                            node_place = "001"
                            for rank, net_channel_send_test_rank_events in net_channel_events["NVTX_EVENT_NET_SEND_TEST"].items():
                                if next_rank is None:
                                    next_rank = rank

                        elif net_send_event_pair_num == -1 and net_recv_event_pair_num > 0:  ## the node is at the end of the Ring
                            node_place = "100"
                            for rank, net_channel_send_test_rank_events in net_channel_events["NVTX_EVENT_NET_RECV_TEST"].items():
                                if previous_rank is None:
                                    previous_rank = rank

                        elif net_send_event_pair_num > 0 and net_recv_event_pair_num > 0:  ## the node is in the middle of the Ring or contains both the start and the end of the Ring
                            for receiver_rank, net_channel_send_test_rank_events in net_channel_events["NVTX_EVENT_NET_SEND_TEST"].items():
                                for sender_rank, net_channel_recv_test_rank_events in net_channel_events["NVTX_EVENT_NET_RECV_TEST"].items():
                                    if net_channel_send_test_rank_events[0]["ts_end"] >= net_channel_recv_test_rank_events[0]["ts_end"]:  ## the node is in the middle of the Ring
                                        node_place = "010"
                                    else:  ## the node contains both the start and the end of the Ring
                                        node_place = "101"

                                    if previous_rank is None:
                                        previous_rank = sender_rank
                                    if next_rank is None:
                                        next_rank = receiver_rank
                        
                        ##
                        if node_place == "001":
                            send_depends_on_events = {}

                            net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][0]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                            send_depends_on_events["task_id_start"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][next_rank][net_send_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            send_depends_on_events["task_id_end"] = task_counter

                            for i in range(net_send_event_pair_num):
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][i]

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{send_depends_on_events['task_id_start']}\n")

                                task_counter += 1
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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

                        elif node_place == "100":
                            recv_depends_on_events = {}

                            net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][previous_rank][0]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                            recv_depends_on_events["task_id_start"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][previous_rank][net_recv_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            recv_depends_on_events["task_id_end"] = task_counter

                            for i in range(net_recv_event_pair_num):
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][previous_rank][i]   
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{recv_depends_on_events['task_id_start']}\n")
                                net_recv_event_start_calc_id = task_counter
                                ts_net_irecv_start = net_event["ts_start"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][previous_rank][i]
                                task_counter += 1
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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

                        elif node_place == "101":
                            recv_depends_on_events = {}
                            send_depends_on_events = {}

                            net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][previous_rank][0]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                            recv_depends_on_events["task_id_start"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][previous_rank][net_recv_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            recv_depends_on_events["task_id_end"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][0]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                            send_depends_on_events["task_id_start"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][next_rank][net_send_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            send_depends_on_events["task_id_end"] = task_counter

                            for i in range(net_recv_event_pair_num):
                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][previous_rank][i]   
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{recv_depends_on_events['task_id_start']}\n")
                                net_recv_event_start_calc_id = task_counter
                                ts_net_irecv_start = net_event["ts_start"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][previous_rank][i]
                                task_counter += 1
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][i]

                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{send_depends_on_events['task_id_start']}\n")

                                task_counter += 1
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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

                        elif node_place == "010":
                            recv_depends_on_events = {}
                            send_depends_on_events = {}

                            for i in range(net_send_event_pair_num):
                                send_depends_on_events[i] = {}

                            net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][previous_rank][0]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {net_event["ts_start"] - gpu_event["timestamp_start"]}\n')
                            file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                            recv_depends_on_events["task_id_start"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][previous_rank][net_recv_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            recv_depends_on_events["task_id_end"] = task_counter

                            net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][next_rank][net_send_event_pair_num - 1]
                            task_counter += 1
                            file.write(f'l{task_counter}: calc {gpu_event["timestamp_all_end"] - net_event["ts_end"]}\n')
                            file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                            send_depends_on_events["task_id_end"] = task_counter

                            for i in range(net_recv_event_pair_num):
                                if send_depends_on_events[i] == {}:
                                    send_depends_on_events[i]["ts_end"] = gpu_event["timestamp_start"]
                                    send_depends_on_events[i]["task_id"] = gpu_event_start_calc_id

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_IRECV"][previous_rank][i]   
                                task_counter += 1
                                file.write(f'l{task_counter}: calc 0\n')
                                file.write(f"l{task_counter} requires l{recv_depends_on_events['task_id_start']}\n")
                                net_recv_event_start_calc_id = task_counter
                                ts_net_irecv_start = net_event["ts_start"]

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_RECV_TEST"][previous_rank][i]
                                task_counter += 1
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: recv {net_event["data_size"]}b from {net_event["sender_rank"]} tag {tag}\n')
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

                                send_depends_on_events[i]["ts_end"] = net_event["ts_end"]  ## send(i) depends on recv(i)
                                send_depends_on_events[i]["task_id"] = task_counter

                                ####
                                net_event = net_channel_events["NVTX_EVENT_NET_ISEND"][next_rank][i]

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {net_event["ts_start"] - send_depends_on_events[i]["ts_end"]}\n')
                                file.write(f"l{task_counter} requires l{send_depends_on_events[i]['task_id']}\n")

                                task_counter += 1
                                tag = net_event["sequence_num"] + channel_id.zfill(2)
                                file.write(f'l{task_counter}: send {net_event["data_size"]}b to {net_event["receiver_rank"]} tag {tag}\n')
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
                                
            file.write("}\n")