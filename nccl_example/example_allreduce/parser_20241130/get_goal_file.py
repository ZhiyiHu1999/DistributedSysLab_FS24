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

                if gpu_event["event_type"] == "AllReduce" and gpu_event["event_algo"] == "Ring":
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

                elif gpu_event["event_type"] == "AllReduce" and gpu_event["event_algo"] == "Tree":
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

def get_goal_file(npkit_events, nsys_events, comm_info, HostName_To_GoalRank, FileRank_To_GoalRank, goal_file_name):
    num_ranks = len(HostName_To_GoalRank)
    print(f'num_ranks: {num_ranks}')

    num_gpus = 0
    for goal_rank_npkit_events in npkit_events.items():
        num_gpus += len(goal_rank_npkit_events)
    print(f'num_gpus: {num_gpus}')

    for commId in comm_info.keys():
        comm_id = commId
        channels_info = comm_info[commId]

    for goal_channels in channels_info.values():
        for file_channels in goal_channels.values():
            num_channels = len(file_channels["Ring"])

    channels_in_out_info = {}
    for goal_rank, goal_channels in channels_info.items():
        channels_in_out_info[goal_rank] = {
            "Ring": [],
            "Tree": []
        }

        for i in range(num_channels):
            for file_rank, file_channels in goal_channels.items():
                Ring_channel = file_channels["Ring"][i]
                if FileRank_To_GoalRank[comm_id][Ring_channel["prev_rank"]] != goal_rank:
                    ingress_rank = Ring_channel["my_rank"]
                if FileRank_To_GoalRank[comm_id][Ring_channel["next_rank"]] != goal_rank:
                    egress_rank = Ring_channel["my_rank"]

            channels_in_out_info[goal_rank]["Ring"].append({
                "ingress_rank": ingress_rank,
                "egress_rank": egress_rank
            })
    
    task_counter = 0
    with open(goal_file_name, 'w') as file:
        file.write(f"num_ranks {num_ranks}\n")

        for goal_rank in range(num_ranks):
            file.write(f"\nrank {goal_rank}")
            file.write(" {\n")

            goal_npkit_events = npkit_events[goal_rank]

            task_counter += 1
            file.write(f"l{task_counter}: calc 0\n") ## Starting point of the rank
            last_gpu_event_end_calc_id = task_counter

            task_counter += 1
            file.write(f'l{task_counter}: calc 0\n')  ## Starting point of the gpu event
            file.write(f"l{task_counter} requires l{last_gpu_event_end_calc_id}\n")
            gpu_event_start_calc_id = task_counter

            task_counter += 1
            file.write(f"l{task_counter}: calc 0\n")  ## end point of a gpu event
            gpu_event_end_calc_id = task_counter  ## id of the calc 0 at the end of the gpu event
            last_gpu_event_end_calc_id = task_counter

            for file_rank, file_npkit_events in goal_npkit_events.items():
                for channel, channel_npkit_events in file_npkit_events.items():
                    for tid, tid_npkit_events in channel_npkit_events.items():
                        npkit_protocol = tid_npkit_events[0]["protocol"]
                        npkit_algo = tid_npkit_events[0]["algorithm"]
                        event_type = nsys_events[comm_id][goal_rank][file_rank][0]["event_type"]

            if event_type == "AllReduce" and npkit_algo == "RING":
                for i in range(num_channels):
                    ingress_rank = channels_in_out_info[goal_rank]["Ring"][i]["ingress_rank"]
                    prev_goal_rank = FileRank_To_GoalRank[commId][comm_info[commId][goal_rank][ingress_rank]["Ring"][i]["prev_rank"]]
                    egress_rank = channels_in_out_info[goal_rank]["Ring"][i]["egress_rank"]
                    next_goal_rank = FileRank_To_GoalRank[commId][comm_info[commId][goal_rank][egress_rank]["Ring"][i]["next_rank"]]

                    send_seq = 0
                    recv_seq = 0

                    if npkit_protocol == "SIMPLE":
                        num_gpus_within_node = len(comm_info[comm_id][goal_rank])
                        offset = num_gpus_within_node * 2
                        print(f"offset: {offset}")
                        num_prim_events_per_round = (num_gpus * 2 - 1) * 2
                        print(f"num_prim_events_per_round: {num_prim_events_per_round}")

                        for j in range(len(goal_npkit_events[egress_rank][i][i][0]["prim_events"])):
                            remainder_j = j % num_prim_events_per_round
                            add_count = 0

                            if remainder_j < offset:
                                print(f"case 1 remainder_j: {remainder_j}")
                                file_rank_send = egress_rank
                                file_rank_recv = ingress_rank
                                calc_duration_send = goal_npkit_events[egress_rank][i][i][0]["prim_events"][j]["data_process_duration"]
                                calc_duration_recv = goal_npkit_events[ingress_rank][i][i][0]["prim_events"][j + num_prim_events_per_round - 1 - 2 * remainder_j]["data_process_duration"]
                                while add_count < (remainder_j // 2):  
                                    file_rank_send = comm_info[comm_id][goal_rank][file_rank_send]["Ring"][i]["prev_rank"]
                                    add_count += 1
                                    calc_duration_send += goal_npkit_events[file_rank_send][i][i][0]["prim_events"][j - 2 * add_count]["data_process_duration"]
                                    calc_duration_recv += goal_npkit_events[ingress_rank][i][i][0]["prim_events"][j + num_prim_events_per_round - 1 - 2 * remainder_j + 2 * add_count]["data_process_duration"]

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {calc_duration_send}\n')
                                file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")

                                task_counter += 1
                                data_size = goal_npkit_events[egress_rank][i][i][0]["prim_events"][j]["data_size"]
                                tag = str(send_seq) + str(i).zfill(2)
                                send_seq += 1
                                file.write(f'l{task_counter}: send {data_size}b to {next_goal_rank} tag {tag}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

                                task_counter += 1
                                data_size = goal_npkit_events[ingress_rank][i][i][0]["prim_events"][j + num_prim_events_per_round - 1 - 2 * remainder_j]["data_size"]
                                remainder_send_seq = send_seq % (num_prim_events_per_round - 2)
                                tag = str(send_seq - remainder_send_seq + (num_prim_events_per_round - 2 - remainder_send_seq)) + str(i).zfill(2)
                                file.write(f'l{task_counter}: recv {data_size}b from {prev_goal_rank} tag {tag}\n')
                                file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")

                                task_counter += 1
                                file.write(f'l{task_counter}: calc {calc_duration_recv}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")

                            elif remainder_j + 2 < num_prim_events_per_round:
                                print(f"case 2 remainder_j: {remainder_j}")
                                file_rank = egress_rank
                                calc_duration = goal_npkit_events[egress_rank][i][i][0]["prim_events"][j]["data_process_duration"]
                                while file_rank != ingress_rank:
                                    file_rank = comm_info[comm_id][goal_rank][file_rank]["Ring"][i]["prev_rank"]
                                    add_count += 1
                                    calc_duration += goal_npkit_events[file_rank][i][i][0]["prim_events"][j - 2 * add_count]["data_process_duration"]

                                task_counter += 1
                                data_size = goal_npkit_events[ingress_rank][i][i][0]["prim_events"][j - offset + 2]["data_size"]
                                tag = str(recv_seq) + str(i).zfill(2)
                                recv_seq += 1
                                file.write(f'l{task_counter}: recv {data_size}b from {prev_goal_rank} tag {tag}\n')
                                file.write(f"l{task_counter} requires l{gpu_event_start_calc_id}\n")
                                
                                task_counter += 1
                                file.write(f'l{task_counter}: calc {calc_duration}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")

                                task_counter += 1
                                tag = str(send_seq) + str(i).zfill(2)
                                send_seq += 1
                                file.write(f'l{task_counter}: send {data_size}b to {next_goal_rank} tag {tag}\n')
                                file.write(f"l{task_counter} requires l{task_counter - 1}\n")
                                file.write(f"l{gpu_event_end_calc_id} requires l{task_counter}\n")
                                
            file.write("}\n")