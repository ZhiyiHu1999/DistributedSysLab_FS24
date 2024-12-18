import argparse
import os
import json
import math
import sqlite3
import re

from collections import defaultdict
from queue import Queue

#### Postprocessing npkit files
def parse_npkit_event_header(npkit_event_header_path):
    npkit_event_def = {'id_to_type': {}, 'type_to_id': {}}
    with open(npkit_event_header_path, 'r') as f:
        lines = [x.strip() for x in f.readlines() if len(x.strip()) != 0]
        line_idx = 0
        while line_idx < len(lines):
            if lines[line_idx].startswith('#define NPKIT_EVENT_'):
                fields = lines[line_idx].split()
                if len(fields) == 3:
                    event_type = fields[1]
                    event_id = int(fields[2], 0)
                    npkit_event_def['type_to_id'][event_type] = event_id
                    npkit_event_def['id_to_type'][event_id] = event_type
            line_idx += 1
    return npkit_event_def
    
def parse_gpu_event(event_bytes):
    return {
        'id': int.from_bytes(event_bytes[0:1], byteorder='little', signed=False),
        'size': int.from_bytes(event_bytes[1:5], byteorder='little', signed=False),
        'rsvd': int.from_bytes(event_bytes[5:8], byteorder='little', signed=False),
        'timestamp': int.from_bytes(event_bytes[8:16], byteorder='little', signed=False)
    }

def parse_gpu_event_file(npkit_dump_dir, npkit_event_def, rank, buf_idx, gpu_clock_scale):
    gpu_event_file_path = os.path.join(npkit_dump_dir, 'gpu_events_rank_%d_buf_%d' % (rank, buf_idx))
    raw_event_size = 16
    gpu_events = []
    event_type_to_seq = {}
    with open(gpu_event_file_path, 'rb') as f:
        raw_content = f.read()
        raw_content_size = len(raw_content)
        raw_content_idx = 0
        while raw_content_idx < raw_content_size:
            parsed_gpu_event = parse_gpu_event(raw_content[raw_content_idx : raw_content_idx + raw_event_size])
            event_type = npkit_event_def['id_to_type'][parsed_gpu_event['id']]
            phase = 'B' if event_type.endswith('_ENTRY') else 'E'
            gpu_events.append({
                'ph': phase,
                'ts': parsed_gpu_event['timestamp'] / gpu_clock_scale,
                'pid': rank,
                'tid': buf_idx
            })
            if phase == 'B':
                if event_type not in event_type_to_seq:
                    event_type_to_seq[event_type] = 0
                
                if event_type.startswith('NPKIT_EVENT_NCCLKERNEL'):
                    gpu_events[-1].update({
                        'name': event_type,
                        'cat': 'GPU',
                        'args': {
                            'rank': rank,
                            'buf_idx': buf_idx,
                            'seq': event_type_to_seq[event_type],
                            'peer_rank': parsed_gpu_event['rsvd'],  ## Time Unit: ns
                            'data_size': parsed_gpu_event['size'],
                            'loopsize': parsed_gpu_event['rsvd']
                        }
                    })
                else:
                    gpu_events[-1].update({
                    'name': event_type,
                    'cat': 'GPU',
                    'args': {
                        'rank': rank,
                        'buf_idx': buf_idx,
                        'seq': event_type_to_seq[event_type],
                        'DataProcessTotalTime': parsed_gpu_event['rsvd'] * 1e3 // gpu_clock_scale,  ## Time Unit: ns
                        'data_size': parsed_gpu_event['size']
                    }
                    })

                event_type_to_seq[event_type] += 1

            else:
                if event_type not in event_type_to_seq:
                    event_type_to_seq[event_type] = 0
                
                if event_type.startswith('NPKIT_EVENT_NCCLKERNEL'):
                    gpu_events[-1].update({
                        'name': event_type,
                        'cat': 'GPU',
                        'args': {
                            'rank': rank,
                            'buf_idx': buf_idx,
                            'seq': event_type_to_seq[event_type],
                            'peer_rank': parsed_gpu_event['rsvd'],  ## Time Unit: ns
                            'data_size': parsed_gpu_event['size'],
                            'loopsize': parsed_gpu_event['rsvd']
                        }
                    })
                else:
                    gpu_events[-1].update({
                    'name': event_type,
                    'cat': 'GPU',
                    'args': {
                        'rank': rank,
                        'buf_idx': buf_idx,
                        'seq': event_type_to_seq[event_type],
                        'DataProcessTotalTime': parsed_gpu_event['rsvd'] * 1e3 // gpu_clock_scale,  ## Time Unit: ns
                        'data_size': parsed_gpu_event['size']
                    }
                    })

                event_type_to_seq[event_type] += 1

            raw_content_idx += raw_event_size

    return gpu_events

def parse_gpu_clock_scale(gpu_clock_file_path):
    with open(gpu_clock_file_path, 'r') as f:
        freq_in_khz = f.read()
        return float(freq_in_khz) * 1e3 / 1e6  ## The value in the trace must be time unit of 'microsecond', regardless of 'displayTimeUnit'

def convert_npkit_dump_to_trace(npkit_dump_dir, output_dir, npkit_event_def):
    files_in_dump_dir = next(os.walk(npkit_dump_dir))[2]
    gpu_event_files = [x for x in files_in_dump_dir if x.startswith('gpu_events_rank_')]

    ranks = list(set([int(x.split('_rank_')[1].split('_')[0]) for x in gpu_event_files]))
    buf_indices = list(set([int(x.split('_buf_')[1].split('_')[0]) for x in gpu_event_files]))

    trace = {'traceEvents': []}

    for rank in ranks:
        gpu_clock_file_path = os.path.join(npkit_dump_dir, 'gpu_clock_rate_rank_%d' % rank)
        gpu_clock_scale = parse_gpu_clock_scale(gpu_clock_file_path)

        for buf_idx in buf_indices:
            gpu_events = parse_gpu_event_file(npkit_dump_dir, npkit_event_def, rank, buf_idx, gpu_clock_scale)
            trace['traceEvents'].extend(gpu_events)


    trace['traceEvents'].sort(key=lambda x : x['ts'])
    trace['displayTimeUnit'] = 'ns'

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'npkit_event_trace.json'), 'w') as f:
        json.dump(trace, f)

    return trace

def get_npkit_events(npkit_trace):
    # with open(json_file, 'r') as f:
    #     data = json.load(f)

    npkit_events = npkit_trace.get("traceEvents", [])
    ncclkernel_events = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    prim_events = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for event in npkit_events:
        rank = event['args']['rank']
        tid = event['tid']
        event_name = event['name']

        if event_name.startswith('NPKIT_EVENT_NCCLKERNEL'):
            event_info = {
            'event_name': event_name,
            'peer_rank': event['args'].get('peer_rank'),
            'ts': int(event['ts'] // 1),  ## us to us
            'data_size': event['args'].get('data_size')
            }

            if event_name.endswith('ENTRY'):
                ncclkernel_events[rank][tid]["entry_events"].append(event_info)
            elif event_name.endswith('EXIT'):
                ncclkernel_events[rank][tid]["exit_events"].append(event_info)

        elif event_name.startswith('NPKIT_EVENT_PRIM'):
            event_info = {
            'event_name': event_name,
            'DataProcessTotalTime': event['args'].get('DataProcessTotalTime') // 1000,  ## ns to us
            'ts': int(event['ts'] // 1),  ## us to us
            'data_size': event['args'].get('data_size')
            }

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
            if tid < 32:
                channel_id = tid
            elif tid < 96:
                channel_id = (tid - 32) // 2 + 32
            else:
                channel_id = (tid - 96) // 16 + 64  ## A global channel_id for Ring/Tree/P2P 

            if channel_id not in npkit_paired_events[rank]:
                npkit_paired_events[rank][channel_id] = {}
            npkit_paired_events[rank][channel_id][tid] = []

    for rank in ncclkernel_events.keys():
        for tid in ncclkernel_events[rank].keys():
            if tid < 32:
                channel_id = tid
            elif tid < 96:
                channel_id = (tid - 32) // 2 + 32
            else:
                channel_id = (tid - 96) // 16 + 64

            for i in range(len(ncclkernel_events[rank][tid]["entry_events"])):
                npkit_paired_event = {}
                npkit_paired_event["prim_events"] = []
                npkit_paired_event["event_name"] = ncclkernel_events[rank][tid]["entry_events"][i]["event_name"].replace("_ENTRY", "")
                npkit_paired_event["peer_rank"] = ncclkernel_events[rank][tid]["entry_events"][i]["peer_rank"]
                npkit_paired_event["ts_start"] = ncclkernel_events[rank][tid]["entry_events"][i]["ts"]
                npkit_paired_event["ts_end"] = ncclkernel_events[rank][tid]["exit_events"][i]["ts"]

                if "algorithm" not in npkit_paired_event:
                    ncclkernel_event_name_splits = ncclkernel_events[rank][tid]["entry_events"][i]["event_name"].split("_")
                    npkit_paired_event["algorithm"] = ncclkernel_event_name_splits[-2]

                for j in range(len(prim_events[rank][tid]["entry_events"])):
                    npkit_prim_event = {}
                    npkit_prim_event["event_name"] = prim_events[rank][tid]["entry_events"][j]["event_name"].replace("_ENTRY", "")

                    if "protocol" not in npkit_paired_event:
                        prim_event_name_splits = npkit_prim_event["event_name"].split("_")
                        npkit_paired_event["protocol"] = prim_event_name_splits[3]

                    npkit_prim_event["ts_start"] = prim_events[rank][tid]["entry_events"][j]["ts"]
                    npkit_prim_event["ts_end"] = prim_events[rank][tid]["exit_events"][j]["ts"]
                    npkit_prim_event["data_process_duration"] = int(prim_events[rank][tid]["exit_events"][j]["DataProcessTotalTime"])
                    npkit_prim_event["seq"] = len(npkit_paired_event["prim_events"])  ## Seq num of the prim event within the kernel event
                    npkit_prim_event["data_size"] = prim_events[rank][tid]["exit_events"][j]["data_size"]

                    if npkit_prim_event["ts_start"] >= npkit_paired_event["ts_start"] and npkit_prim_event["ts_end"] <= npkit_paired_event["ts_end"]:
                        npkit_paired_event["prim_events"].append(npkit_prim_event)

                npkit_paired_events[rank][channel_id][tid].append(npkit_paired_event)

    return npkit_paired_events 

#### Postprocessing nsys files
def get_nsys_events(dir_path):
    comm_info = {}
    nccl_api_events = {}
    HostName_To_GoalRank = {}
    Comm_GoalRank_To_FileRank = {}
    Comm_FileRank_To_GoalRank = {}
    pattern_HostName = r'nsys_report_([^.]+)\.'

    for file_name in os.listdir(dir_path):  ## each file represents a rank
        if file_name.endswith('.sqlite'):
            file_path = os.path.join(dir_path, file_name)
            comm_to_file_rank = {}
            comm_to_commId = {}
            cupti_kernel_events = []

            match = re.search(pattern_HostName, file_name)
            if match:
                host_name = match.group(1)
                print(f"Host Name: {host_name}")

            if host_name in HostName_To_GoalRank:
                goal_rank = HostName_To_GoalRank[host_name]
                # GoalRank_To_NumOfRanks[goal_rank] += 1
            else:
                goal_rank = len(HostName_To_GoalRank)
                HostName_To_GoalRank[host_name] = goal_rank
                # GoalRank_To_NumOfRanks[goal_rank] = 1
            
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()

            cursor.execute("SELECT text, start, end FROM NVTX_EVENTS")  ## row[0]: text, row[1]: ts_start, row[2]: ts_end
            nvtx_events_results = cursor.fetchall()

            pattern_ring = r"comm (\S+) commHash (\S+) Rings \[(\d+)\] (\d+)->(\d+)->(\d+)"
            pattern_tree = r"comm (\S+) commHash (\S+) Trees \[(\d+)\] (-?\d+)/(-?\d+)/(-?\d+)->(-?\d+)->(-?\d+)"

            pattern_nccl_AllReduce = r"ncclAllReduce\(\): comm (\S+), data_size: (\d+)"

            for row in nvtx_events_results:
                if row[0]:
                    match_ring = re.search(pattern_ring, row[0])
                    match_tree = re.search(pattern_tree, row[0])
                    match_nccl_AllReduce = re.search(pattern_nccl_AllReduce, row[0])

                    if match_ring:
                        if not comm_info.get(match_ring.group(2)):
                            comm_info[match_ring.group(2)] = {}

                        if not comm_info[match_ring.group(2)].get(goal_rank):
                            comm_info[match_ring.group(2)][goal_rank] = {}

                        if not comm_info[match_ring.group(2)][goal_rank].get(match_ring.group(5)):
                            comm_info[match_ring.group(2)][goal_rank][match_ring.group(5)] = {
                                        "comm": match_ring.group(1),
                                        "Ring": [],
                                        "Tree": [],
                                        "HostName": host_name,
                                        "goal_rank": goal_rank
                            }    

                        Ring_channel = {
                            "prev_rank": match_ring.group(4),
                            "my_rank": match_ring.group(5),
                            "next_rank": match_ring.group(6),
                            "channel_id": match_ring.group(3)
                        }
                        comm_info[match_ring.group(2)][goal_rank][match_ring.group(5)]["Ring"].append(Ring_channel)

                        if not comm_to_file_rank.get(match_ring.group(1)):
                            comm_to_file_rank[match_ring.group(1)] = match_ring.group(5)

                        if not comm_to_commId.get(match_ring.group(1)):
                            comm_to_commId[match_ring.group(1)] = match_ring.group(2)

                        if not Comm_GoalRank_To_FileRank.get(match_ring.group(2)):
                            Comm_GoalRank_To_FileRank[match_ring.group(2)] = {}

                        if not Comm_GoalRank_To_FileRank[match_ring.group(2)].get(goal_rank):
                            Comm_GoalRank_To_FileRank[match_ring.group(2)][goal_rank] = []

                        if match_ring.group(5) not in Comm_GoalRank_To_FileRank[match_ring.group(2)][goal_rank]:
                            Comm_GoalRank_To_FileRank[match_ring.group(2)][goal_rank].append(match_ring.group(5))

                        if not Comm_FileRank_To_GoalRank.get(match_ring.group(2)):
                            Comm_FileRank_To_GoalRank[match_ring.group(2)] = {}

                        if not Comm_FileRank_To_GoalRank[match_ring.group(2)].get(match_ring.group(5)):
                            Comm_FileRank_To_GoalRank[match_ring.group(2)][match_ring.group(5)] = goal_rank

                    elif match_tree:
                        if not comm_info.get(match_tree.group(2)):
                            comm_info[match_tree.group(2)] = {}

                        if not comm_info[match_tree.group(2)].get(goal_rank):
                            comm_info[match_tree.group(2)][goal_rank] = {}

                        if not comm_info[match_tree.group(2)][goal_rank].get(match_tree.group(7)):
                            comm_info[match_tree.group(2)][match_tree.group(7)] = {
                                        "comm": match_tree.group(1),
                                        "Ring": [],
                                        "Tree": [],
                                        "HostName": host_name,
                                        "goal_rank": goal_rank
                            }                            

                        Tree_channel = {
                            "child_1_rank": match_tree.group(4),
                            "child_2_rank": match_tree.group(5),
                            "child_3_rank": match_tree.group(6),
                            "my_rank": match_tree.group(7),
                            "parent_rank": match_tree.group(8),
                            "channel_id": match_tree.group(3)
                        }
                        comm_info[match_tree.group(2)][goal_rank][match_tree.group(7)]["Tree"].append(Tree_channel)

                        if not comm_to_file_rank.get(match_tree.group(1)):
                            comm_to_file_rank[match_tree.group(1)] = match_tree.group(7)

                        if not comm_to_commId.get(match_tree.group(1)):
                            comm_to_commId[match_tree.group(1)] = match_tree.group(2)

                    elif match_nccl_AllReduce:
                        commId = comm_to_commId[match_nccl_AllReduce.group(1)]
                        if not nccl_api_events.get(commId):
                            nccl_api_events[commId] = {}

                        if not nccl_api_events[commId].get(goal_rank):
                            nccl_api_events[commId][goal_rank] = {}

                        if not nccl_api_events[commId][goal_rank].get(comm_to_file_rank[match_nccl_AllReduce.group(1)]):
                            nccl_api_events[commId][goal_rank][comm_to_file_rank[match_nccl_AllReduce.group(1)]] = []

                        nccl_api_event = {
                            "event_type": "AllReduce",
                            "ts_start": row[1] // 1000,  ## ns to us
                            "ts_end": row[2] // 1000,  ## ns to us
                            "comm": match_nccl_AllReduce.group(1),
                            "my_rank": comm_to_file_rank[match_nccl_AllReduce.group(1)]
                        }

                        nccl_api_events[commId][goal_rank][comm_to_file_rank[match_nccl_AllReduce.group(1)]].append(nccl_api_event)
            
            cursor.execute("SELECT id, value FROM StringIds")
            string_ids = cursor.fetchall()
            string_dict = {row[0]: row[1] for row in string_ids}
            
            cursor.execute("SELECT start, end, demangledName FROM CUPTI_ACTIVITY_KIND_KERNEL")
            cupti_kernel_results = cursor.fetchall()
            for row in cupti_kernel_results:
                start, end, demangled_name = row
                if string_dict[demangled_name].startswith("ncclKernel") or string_dict[demangled_name].startswith("ncclDevKernel"):
                    cupti_kernel_events.append({
                        "event_name": string_dict[demangled_name],
                        "timestamp_start": start // 1000,
                        "timestamp_end": end // 1000
                    })

            conn.close()
        
    # return comm_info, nccl_api_events, FileRank_To_GoalRank, HostName_To_GoalRank, GoalRank_To_NumOfRanks
    return comm_info, nccl_api_events, HostName_To_GoalRank, Comm_GoalRank_To_FileRank, Comm_FileRank_To_GoalRank

def merge_npkit_events(Npkit_Paired_Events, GoalRank_To_FileRank):
    for GoalRank_to_FileRank in GoalRank_To_FileRank.values():
        Merged_Npkit_Events = {}
        for goal_rank, file_rank_list in GoalRank_to_FileRank.items():
            Merged_Npkit_Events[goal_rank] = {}
            for file_rank in file_rank_list:
                Merged_Npkit_Events[goal_rank][file_rank] = Npkit_Paired_Events[int(file_rank)]

    return Merged_Npkit_Events       

def transform_nsys_events(npkit_paired_events, nsys_events):
    transformed_nsys_events = {}
    for rank, rank_nsys_events in nsys_events.items():
        transformed_nsys_events[rank] = []
        for nsys_event_id, rank_nsys_event in enumerate(rank_nsys_events):
            transformed_nsys_events[rank].append({})
            transformed_nsys_events[rank][nsys_event_id]["event_name"] = rank_nsys_event["event_name"]

            fields = transformed_nsys_events[rank][nsys_event_id]["event_name"].split("_")
            transformed_nsys_events[rank][nsys_event_id]["event_type"] = fields[1]
            for field in fields:
                if field.lower() == "ring":
                    transformed_nsys_events[rank][nsys_event_id]["event_algo"] = "Ring"
                    break
                elif field.lower() == "tree":
                    transformed_nsys_events[rank][nsys_event_id]["event_algo"] = "Tree"
                    break

            for field in fields:
                if field.lower() == "sendrecv":
                    transformed_nsys_events[rank][nsys_event_id]["event_algo"] = "P2P"

            # if not transformed_nsys_events[rank][nsys_event_id].get("event_protocol"):
            #     transformed_nsys_events[rank][nsys_event_id]["event_protocol"] = npkit_paired_events[int(rank)][0][0][nsys_event_id]["protocol"]  ## bid and tid is not string

            transformed_nsys_events[rank][nsys_event_id]["timestamp_start"] = rank_nsys_event["timestamp_start"]
            transformed_nsys_events[rank][nsys_event_id]["timestamp_end"] = rank_nsys_event["timestamp_end"]

            transformed_net_events = {}

            for channel_id, channel_net_events in rank_nsys_event["net_events"].items():
                transformed_net_events[channel_id] = {
                    "NVTX_EVENT_NET_ISEND": {},
                    "NVTX_EVENT_NET_IRECV": {},
                    # "NVTX_EVENT_NET_SEND_TEST": {},
                    # "NVTX_EVENT_NET_RECV_TEST": {}
                    }
                
                if len(channel_net_events["NVTX_EVENT_NET_ISEND"]) > 0:
                    for net_event in channel_net_events["NVTX_EVENT_NET_ISEND"]:
                        receiver_rank = net_event["receiver_rank"]
                        if receiver_rank not in transformed_net_events[channel_id]["NVTX_EVENT_NET_ISEND"]:
                            transformed_net_events[channel_id]["NVTX_EVENT_NET_ISEND"][receiver_rank] = []
                        transformed_net_events[channel_id]["NVTX_EVENT_NET_ISEND"][receiver_rank].append(net_event)

                # if len(channel_net_events["NVTX_EVENT_NET_SEND_TEST"]) > 0:
                #     for net_event in channel_net_events["NVTX_EVENT_NET_SEND_TEST"]:
                #         receiver_rank = net_event["receiver_rank"]
                #         if receiver_rank not in transformed_net_events[channel_id]["NVTX_EVENT_NET_SEND_TEST"]:
                #             transformed_net_events[channel_id]["NVTX_EVENT_NET_SEND_TEST"][receiver_rank] = []
                #         transformed_net_events[channel_id]["NVTX_EVENT_NET_SEND_TEST"][receiver_rank].append(net_event)

                if len(channel_net_events["NVTX_EVENT_NET_IRECV"]) > 0:
                    for net_event in channel_net_events["NVTX_EVENT_NET_IRECV"]:
                        sender_rank = net_event["sender_rank"]
                        if sender_rank not in transformed_net_events[channel_id]["NVTX_EVENT_NET_IRECV"]:
                            transformed_net_events[channel_id]["NVTX_EVENT_NET_IRECV"][sender_rank] = []
                        transformed_net_events[channel_id]["NVTX_EVENT_NET_IRECV"][sender_rank].append(net_event)

                # if len(channel_net_events["NVTX_EVENT_NET_RECV_TEST"]) > 0:
                #     for net_event in channel_net_events["NVTX_EVENT_NET_RECV_TEST"]:
                #         sender_rank = net_event["sender_rank"]
                #         if sender_rank not in transformed_net_events[channel_id]["NVTX_EVENT_NET_RECV_TEST"]:
                #             transformed_net_events[channel_id]["NVTX_EVENT_NET_RECV_TEST"][sender_rank] = []
                #         transformed_net_events[channel_id]["NVTX_EVENT_NET_RECV_TEST"][sender_rank].append(net_event)

            transformed_nsys_events[rank][nsys_event_id]["net_events"] = transformed_net_events

    return transformed_nsys_events


def map_npkit_to_nsys(npkit_paired_events, transformed_nsys_events, FileRank_to_GoalRank):
    next_npkit_event_id = {}
    for rank, rank_npkit_events in npkit_paired_events.items():
        next_npkit_event_id[rank] = {}
        for channel, channel_npkit_events in rank_npkit_events.items():
            next_npkit_event_id[rank][channel] = {}
            for tid in channel_npkit_events.keys():
                next_npkit_event_id[rank][channel][tid] = 0

    print(next_npkit_event_id)

    for rank, channel_gpu_prim_events in npkit_paired_events.items():
        if str(rank) in FileRank_to_GoalRank:
            nsys_rank_events = transformed_nsys_events[str(rank)]
            for i in range(len(nsys_rank_events)):
                nsys_nccl_kernel_ts_start = nsys_rank_events[i]["timestamp_start"]
                nsys_nccl_kernel_ts_end = nsys_rank_events[i]["timestamp_end"]

                if nsys_rank_events[i]["event_algo"] == "Tree":
                    for channel, tid_gpu_prim_events in channel_gpu_prim_events.items():
                        if (channel * 2 + 1) in tid_gpu_prim_events:
                            npkit_gpu_event_id = next_npkit_event_id[rank][channel][(channel * 2 + 1)]
                            gpu_prim_event = tid_gpu_prim_events[(channel * 2 + 1)][npkit_gpu_event_id]
                        else:
                            npkit_gpu_event_id = next_npkit_event_id[rank][channel][(channel * 2)]
                            gpu_prim_event = tid_gpu_prim_events[(channel * 2)][npkit_gpu_event_id]

                        gpu_prim_event_ts_start = gpu_prim_event["ts_start"]
                        gpu_prim_event_ts_end = gpu_prim_event["ts_end"]

                        for tid, gpu_prim_events in tid_gpu_prim_events.items():
                            npkit_gpu_event_id = next_npkit_event_id[rank][channel][tid]
                            gpu_prim_event = gpu_prim_events[npkit_gpu_event_id]
                            gpu_prim_event["ts_start"] = nsys_nccl_kernel_ts_start
                            gpu_prim_event["ts_end"] = nsys_nccl_kernel_ts_end

                            for j in range(len(gpu_prim_event["prim_events"])):
                                gpu_prim_event["prim_events"][j]["ts_start"] = map_p_to_t(gpu_prim_event["prim_events"][j]["ts_start"], gpu_prim_event_ts_start, gpu_prim_event_ts_end, nsys_nccl_kernel_ts_start, nsys_nccl_kernel_ts_end)
                                gpu_prim_event["prim_events"][j]["ts_end"] = map_p_to_t(gpu_prim_event["prim_events"][j]["ts_end"], gpu_prim_event_ts_start, gpu_prim_event_ts_end, nsys_nccl_kernel_ts_start, nsys_nccl_kernel_ts_end)
                                gpu_prim_event["prim_events"][j]["ts_calc"] = map_p_to_t(gpu_prim_event["prim_events"][j]["ts_calc"], gpu_prim_event_ts_start, gpu_prim_event_ts_end, nsys_nccl_kernel_ts_start, nsys_nccl_kernel_ts_end)

                        next_npkit_event_id[rank][channel][(channel * 2)] += 1
                        if (channel * 2 + 1) in tid_gpu_prim_events:
                            next_npkit_event_id[rank][channel][(channel * 2 + 1)] += 1

                else:
                    for channel, tid_gpu_prim_events in channel_gpu_prim_events.items():
                        npkit_gpu_event_id = next_npkit_event_id[rank][channel][(channel * 2)]
                        gpu_prim_event = tid_gpu_prim_events[(channel * 2)][npkit_gpu_event_id]

                        gpu_prim_event_ts_start = gpu_prim_event["ts_start"]
                        gpu_prim_event_ts_end = gpu_prim_event["ts_end"]

                        for tid, gpu_prim_events in tid_gpu_prim_events.items():
                            npkit_gpu_event_id = next_npkit_event_id[rank][channel][tid]
                            gpu_prim_event = gpu_prim_events[npkit_gpu_event_id]
                            gpu_prim_event["ts_start"] = nsys_nccl_kernel_ts_start
                            gpu_prim_event["ts_end"] = nsys_nccl_kernel_ts_end

                            for j in range(len(gpu_prim_event["prim_events"])):
                                gpu_prim_event["prim_events"][j]["ts_start"] = map_p_to_t(gpu_prim_event["prim_events"][j]["ts_start"], gpu_prim_event_ts_start, gpu_prim_event_ts_end, nsys_nccl_kernel_ts_start, nsys_nccl_kernel_ts_end)
                                gpu_prim_event["prim_events"][j]["ts_end"] = map_p_to_t(gpu_prim_event["prim_events"][j]["ts_end"], gpu_prim_event_ts_start, gpu_prim_event_ts_end, nsys_nccl_kernel_ts_start, nsys_nccl_kernel_ts_end)
                                gpu_prim_event["prim_events"][j]["ts_calc"] = map_p_to_t(gpu_prim_event["prim_events"][j]["ts_calc"], gpu_prim_event_ts_start, gpu_prim_event_ts_end, nsys_nccl_kernel_ts_start, nsys_nccl_kernel_ts_end)

                        next_npkit_event_id[rank][channel][(channel * 2)] += 1

    mapped_npkit_events = {}
    for rank, channel_gpu_prim_events in npkit_paired_events.items():
        file_rank = str(rank)
        if file_rank in FileRank_to_GoalRank:
            mapped_npkit_events[file_rank] = channel_gpu_prim_events

    print(next_npkit_event_id)

    return mapped_npkit_events

def map_p_to_t(p0, p1, p2, t1, t2):
    return (t1 - t2) * p0 // (p1 - p2) + (t2* p1 - t1 * p2) // (p1 - p2)

def combine_npkit_nsys_events(mapped_npkit_events, transformed_nsys_events):
    next_npkit_event_id = {}
    for rank, rank_npkit_events in mapped_npkit_events.items():
        next_npkit_event_id[rank] = {}
        for channel, channel_npkit_events in rank_npkit_events.items():
            next_npkit_event_id[rank][channel] = {}
            for tid in channel_npkit_events.keys():
                next_npkit_event_id[rank][channel][tid] = 0

    print(next_npkit_event_id)

    combined_events = {}
    for rank, rank_nsys_events in transformed_nsys_events.items():
        combined_events[rank] = []
        for nsys_event_id, rank_nsys_event in enumerate(rank_nsys_events):
            combined_events[rank].append({})
            combined_events[rank][nsys_event_id]["event_name"] = rank_nsys_event["event_name"]
            combined_events[rank][nsys_event_id]["event_type"] = rank_nsys_event["event_type"]
            combined_events[rank][nsys_event_id]["event_algo"] = rank_nsys_event["event_algo"]
            combined_events[rank][nsys_event_id]["event_protocol"] = rank_nsys_event["event_protocol"]
            combined_events[rank][nsys_event_id]["timestamp_start"] = rank_nsys_event["timestamp_start"]
            combined_events[rank][nsys_event_id]["timestamp_end"] = rank_nsys_event["timestamp_end"]
            combined_events[rank][nsys_event_id]["timestamp_all_end"] = rank_nsys_event["timestamp_all_end"]

            combined_events[rank][nsys_event_id]["net_events"] = rank_nsys_event["net_events"]

            if combined_events[rank][nsys_event_id]["event_algo"] == "Simple":
                for channel_id, channel_next_npkit_event_id in next_npkit_event_id[rank].items():
                    channel = int(channel_id)
                    channel_next_npkit_event_id[channel * 2] += 1
                    if combined_events[rank][nsys_event_id]["event_algo"] == "Tree" and (channel * 2 + 1) in channel_next_npkit_event_id:
                        channel_next_npkit_event_id[channel * 2 + 1] += 1

            elif combined_events[rank][nsys_event_id]["event_algo"] == "LL" or "LL128":
                for channel_id, channel_net_events in rank_nsys_event["net_events"].items():
                    channel = int(channel_id)

                    if combined_events[rank][nsys_event_id]["event_algo"] == "Tree":
                        if len(combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"]) == 1: ## The rank is a middle rank and only has one sender and one receiver
                            if (channel * 2 + 1) in next_npkit_event_id[rank][channel]:
                                npkit_id_up = next_npkit_event_id[rank][channel][channel * 2]
                                npkit_id_down = next_npkit_event_id[rank][channel][channel * 2 + 1]
                                ts_calc_up = mapped_npkit_events[rank][channel][channel * 2][npkit_id_up]["prim_events"][0]["ts_calc"]
                                ts_calc_down = mapped_npkit_events[rank][channel][channel * 2 + 1][npkit_id_down]["prim_events"][0]["ts_calc"]

                                for recv_rank in rank_nsys_event["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"].keys():
                                    ts_isend_start = rank_nsys_event["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"][recv_rank][0]["ts_start"]

                                if ts_isend_start < ts_calc_down:  ## Net Recv corresponds to ts_calc_down
                                    for send_rank in rank_nsys_event["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"].keys():
                                        for i in range(len(combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank])):
                                            combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank][i]["ts_calc"] = mapped_npkit_events[rank][channel][channel * 2 + 1][npkit_id_down]["prim_events"][i]["ts_calc"]
                                            if combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank][i]["ts_calc"] < combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"][send_rank][i]["ts_start"]:
                                                print(f"rank: {rank}, peer_rank: {send_rank}, sqeuence_num: {i}")

                                else:  ## Net Recv corresponds to ts_calc_up
                                    for send_rank in rank_nsys_event["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"].keys():
                                        for i in range(len(combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank])):
                                            combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank][i]["ts_calc"] = mapped_npkit_events[rank][channel][channel * 2][npkit_id_up]["prim_events"][i]["ts_calc"]
                                            # if combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank][i]["ts_calc"] > combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"][send_rank][i]["ts_start"]:
                                            #     print(f"rank: {rank}, sqeuence_num: {i}")

                            else:  ## Top-most rank and has net events
                                npkit_id_up = next_npkit_event_id[rank][channel][channel * 2]
                                ts_calc_up = mapped_npkit_events[rank][channel][channel * 2][npkit_id_up]["prim_events"][0]["ts_calc"]
                                for send_rank in rank_nsys_event["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"].keys():
                                    for i in range(len(combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank])):
                                        combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank][i]["ts_calc"] = mapped_npkit_events[rank][channel][channel * 2][npkit_id_up]["prim_events"][i]["ts_calc"]
                                        # if combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank][i]["ts_calc"] > combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"][send_rank][i]["ts_start"]:
                                        #     print(f"rank: {rank}, peer_rank: {send_rank}, sqeuence_num: {i}")

                        else:
                            npkit_id_up = next_npkit_event_id[rank][channel][channel * 2]
                            npkit_id_down = next_npkit_event_id[rank][channel][channel * 2 + 1]
                            ts_calc_up = mapped_npkit_events[rank][channel][channel * 2][npkit_id_up]["prim_events"][0]["ts_calc"]
                            ts_calc_down = mapped_npkit_events[rank][channel][channel * 2 + 1][npkit_id_down]["prim_events"][0]["ts_calc"]

                            for recv_rank in rank_nsys_event["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"].keys():
                                ts_isend_start = rank_nsys_event["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"][recv_rank][0]["ts_start"]

                                if ts_isend_start < ts_calc_down:  ## recv_rank is parent
                                    for send_rank in rank_nsys_event["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"].keys():
                                        if send_rank != recv_rank:  ## send_rank is child
                                            for i in range(len(combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank])):
                                                combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank][i]["ts_calc"] = mapped_npkit_events[rank][channel][channel * 2][npkit_id_up]["prim_events"][i]["ts_calc"]
                                                # if combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank][i]["ts_calc"] > combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"][send_rank][i]["ts_start"]:
                                                #     print(f"rank: {rank}, peer_rank: {send_rank}, sqeuence_num: {i}")

                                        else:  ## send_rank is parent
                                            for i in range(len(combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank])):
                                                combined_events[rank][nsys_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][send_rank][i]["ts_calc"] = mapped_npkit_events[rank][channel][channel * 2 + 1][npkit_id_down]["prim_events"][i]["ts_calc"]


                    next_npkit_event_id[rank][channel][channel * 2] += 1
                    if combined_events[rank][nsys_event_id]["event_algo"] == "Tree" and (channel * 2 + 1) in next_npkit_event_id[rank][channel]:
                        next_npkit_event_id[rank][channel][channel * 2 + 1] += 1
                    
            
    # return transformed_nsys_events
    return combined_events

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
            merged_events[goal_rank][nccl_kernel_event_id]["timestamp_all_end"] = None

            for file_rank, nccl_kernel_events in traced_events.items():
                if FileRank_To_GoalRank[file_rank] == goal_rank:
                    merged_events[goal_rank][nccl_kernel_event_id]["event_name"] =  nccl_kernel_events[nccl_kernel_event_id]["event_name"]
                    merged_events[goal_rank][nccl_kernel_event_id]["event_type"] =  nccl_kernel_events[nccl_kernel_event_id]["event_type"]
                    merged_events[goal_rank][nccl_kernel_event_id]["event_algo"] =  nccl_kernel_events[nccl_kernel_event_id]["event_algo"]
                    merged_events[goal_rank][nccl_kernel_event_id]["event_protocol"] =  nccl_kernel_events[nccl_kernel_event_id]["event_protocol"]
                    
                    if merged_events[goal_rank][nccl_kernel_event_id]["timestamp_start"]:
                        merged_events[goal_rank][nccl_kernel_event_id]["timestamp_start"] = min(merged_events[goal_rank][nccl_kernel_event_id]["timestamp_start"], nccl_kernel_events[nccl_kernel_event_id]["timestamp_start"])
                    else:
                        merged_events[goal_rank][nccl_kernel_event_id]["timestamp_start"] = nccl_kernel_events[nccl_kernel_event_id]["timestamp_start"]

                    if merged_events[goal_rank][nccl_kernel_event_id]["timestamp_end"]:
                        merged_events[goal_rank][nccl_kernel_event_id]["timestamp_end"] = max(merged_events[goal_rank][nccl_kernel_event_id]["timestamp_end"], nccl_kernel_events[nccl_kernel_event_id]["timestamp_end"])
                    else:
                        merged_events[goal_rank][nccl_kernel_event_id]["timestamp_end"] = nccl_kernel_events[nccl_kernel_event_id]["timestamp_end"]

                    if merged_events[goal_rank][nccl_kernel_event_id]["timestamp_all_end"]:
                        merged_events[goal_rank][nccl_kernel_event_id]["timestamp_all_end"] = max(merged_events[goal_rank][nccl_kernel_event_id]["timestamp_all_end"], nccl_kernel_events[nccl_kernel_event_id]["timestamp_all_end"])
                    else:
                        merged_events[goal_rank][nccl_kernel_event_id]["timestamp_all_end"] = nccl_kernel_events[nccl_kernel_event_id]["timestamp_all_end"]

                    net_events = nccl_kernel_events[nccl_kernel_event_id]["net_events"]
                    for channel_id, nvtx_net_channel_events in net_events.items():
                        if not merged_events[goal_rank][nccl_kernel_event_id]["net_events"].get(channel_id):
                            merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id] = {
                                "NVTX_EVENT_NET_ISEND": {},
                                "NVTX_EVENT_NET_IRECV": {},
                                "NVTX_EVENT_NET_SEND_TEST": {},
                                "NVTX_EVENT_NET_RECV_TEST": {}
                                }

                        if len(nvtx_net_channel_events["NVTX_EVENT_NET_ISEND"]) > 0:
                            for recv_rank in nvtx_net_channel_events["NVTX_EVENT_NET_ISEND"].keys():
                                for net_event in nvtx_net_channel_events["NVTX_EVENT_NET_ISEND"][recv_rank]:
                                    net_event_goal = net_event
                                    net_event_goal["sender_rank"] = FileRank_To_GoalRank[net_event_goal["sender_rank"]]
                                    net_event_goal["receiver_rank"] = FileRank_To_GoalRank[net_event_goal["receiver_rank"]]
                                    if not merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"].get(net_event_goal["receiver_rank"]):
                                        merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"][net_event_goal["receiver_rank"]] = []
                                    merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_ISEND"][net_event_goal["receiver_rank"]].append(net_event_goal)

                            for recv_rank in nvtx_net_channel_events["NVTX_EVENT_NET_SEND_TEST"].keys():
                                for net_event in nvtx_net_channel_events["NVTX_EVENT_NET_SEND_TEST"][recv_rank]:
                                    net_event_goal = net_event
                                    net_event_goal["sender_rank"] = FileRank_To_GoalRank[net_event_goal["sender_rank"]]
                                    net_event_goal["receiver_rank"] = FileRank_To_GoalRank[net_event_goal["receiver_rank"]]
                                    if not merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_SEND_TEST"].get(net_event_goal["receiver_rank"]):
                                        merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_SEND_TEST"][net_event_goal["receiver_rank"]] = []
                                    merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_SEND_TEST"][net_event_goal["receiver_rank"]].append(net_event_goal)

                        if len(nvtx_net_channel_events["NVTX_EVENT_NET_IRECV"]) > 0:
                            for send_rank in nvtx_net_channel_events["NVTX_EVENT_NET_IRECV"].keys():
                                for net_event in nvtx_net_channel_events["NVTX_EVENT_NET_IRECV"][send_rank]:
                                    net_event_goal = net_event
                                    net_event_goal["sender_rank"] = FileRank_To_GoalRank[net_event_goal["sender_rank"]]
                                    net_event_goal["receiver_rank"] = FileRank_To_GoalRank[net_event_goal["receiver_rank"]]
                                    if not merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_IRECV"].get(net_event_goal["sender_rank"]):
                                        merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_IRECV"][net_event_goal["sender_rank"]] = []
                                    merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_IRECV"][net_event_goal["sender_rank"]].append(net_event_goal)

                            for send_rank in nvtx_net_channel_events["NVTX_EVENT_NET_RECV_TEST"].keys():
                                for net_event in nvtx_net_channel_events["NVTX_EVENT_NET_RECV_TEST"][send_rank]:
                                    net_event_goal = net_event
                                    net_event_goal["sender_rank"] = FileRank_To_GoalRank[net_event_goal["sender_rank"]]
                                    net_event_goal["receiver_rank"] = FileRank_To_GoalRank[net_event_goal["receiver_rank"]]
                                    if not merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"].get(net_event_goal["sender_rank"]):
                                        merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][net_event_goal["sender_rank"]] = []
                                    merged_events[goal_rank][nccl_kernel_event_id]["net_events"][channel_id]["NVTX_EVENT_NET_RECV_TEST"][net_event_goal["sender_rank"]].append(net_event_goal)
    
    return merged_events

def main():
    #### Get npkit events
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--npkit_dump_dir', type=str, required=True, help='NPKit dump directory.')
    # parser.add_argument('--npkit_event_header_path', type=str, required=True, help='Path to npkit_event.h.')
    # parser.add_argument('--output_dir', type=str, required=True, help='Path to output directory.')
    # args = parser.parse_args()

    # npkit_event_def = parse_npkit_event_header(args.npkit_event_header_path)
    # npkit_trace = convert_npkit_dump_to_trace(args.npkit_dump_dir, args.output_dir, npkit_event_def)

    npkit_event_def = parse_npkit_event_header("/users/zhu/nccl_nvtx_npkit/nccl/src/include/npkit/npkit_event.h")
    npkit_trace = convert_npkit_dump_to_trace("./results/npkit_run/npkit_dump", "./results/npkit_run/npkit_trace", npkit_event_def)

    # json_file = './results/npkit_run/npkit_trace/job_example_sendrecv/npkit_event_trace.json'
    ncclkernel_events, prim_events = get_npkit_events(npkit_trace)

    npkit_events_intermediate_file = "./results/npkit_events_intermediate_output.json"
    with open(npkit_events_intermediate_file, "w") as json_file:
        json.dump(ncclkernel_events, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(prim_events, json_file, indent=4)
        json_file.write('\n\n')
    print("Npkit_Events has been exported to npkit_events_intermediate_output.json")

    Npkit_Paired_Events = pair_npkit_events(ncclkernel_events, prim_events)
    npkit_paired_events_file = "./results/npkit_paired_events_output.json"
    with open(npkit_paired_events_file, "w") as json_file:
        json.dump(Npkit_Paired_Events, json_file, indent=4)
        json_file.write('\n\n')
    print("Npkit_Events has been exported to npkit_paired_events_output.json")

    #### Get nsys events
    if os.path.exists("./results/nsys_events_initial_output.json"):
        os.remove("./results/nsys_events_initial_output.json")

    Dir_Path = './results/nsys_reports'
    Comm_Info, NCCL_API_Events, HostName_To_GoalRank, GoalRank_To_FileRank, FileRank_To_GoalRank = get_nsys_events(Dir_Path)
    with open("./results/nsys_events_intermediate_output.json", "w") as json_file:
        json.dump(FileRank_To_GoalRank, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(GoalRank_To_FileRank, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(HostName_To_GoalRank, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(NCCL_API_Events, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(Comm_Info, json_file, indent=4)
    print("Nsys_Events has been exported to nsys_events_intermediate_output.json")

    Merged_Npkit_Events = merge_npkit_events(Npkit_Paired_Events, GoalRank_To_FileRank)
    with open("./results/npkit_merged_events_output.json", "w") as json_file:
        json.dump(Merged_Npkit_Events, json_file, indent=4)
        json_file.write('\n\n')
    print("Merged_Npkit_Events has been exported to npkit_merged_events_output.json")

    # Transformed_Nsys_Events = transform_nsys_events(Npkit_Paired_Events, Nsys_Events)
    # with open("./results/transformed_nsys_events_output.json", "w") as json_file:
    #     json.dump(Transformed_Nsys_Events, json_file, indent=4)
    # print("Transformed_Nsys_Events has been exported to transformed_nsys_events_output.json")

    # Mapped_Npkit_Events = map_npkit_to_nsys(Npkit_Paired_Events, Transformed_Nsys_Events, FileRank_2_GoalRank)
    # with open("./results/npkit_mapped_events_output.json", "w") as json_file:
    #     json.dump(Mapped_Npkit_Events, json_file, indent=4)
    #     json_file.write('\n\n')
    # print("Mapped_Npkit_Events has been exported to npkit_mapped_events_output.json")

    # Combined_Events = combine_npkit_nsys_events(Mapped_Npkit_Events, Transformed_Nsys_Events)
    # with open("./results/combined_events_output.json", "w") as json_file:
    #     json.dump(Combined_Events, json_file, indent=4)
    # print("Combined_Events has been exported to combined_events_output.json")

    # Merged_Nsys_Events = merge_nsys_events(Combined_Events, FileRank_2_GoalRank, HostName_2_GoalRank)
    # with open("./results/merged_events_output.json", "w") as json_file:
    #     json.dump(Merged_Nsys_Events, json_file, indent=4)
    # print("Merged_Nsys_Events has been exported to merged_events_output.json")

if __name__ == '__main__':
    main()