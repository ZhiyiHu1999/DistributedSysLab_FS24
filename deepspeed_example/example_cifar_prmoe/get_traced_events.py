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
    nccl_events = {}
    cupti_kernel_results = {}
    HostName_To_GoalRank = {}
    GoalRank_To_NumOfGPUs = {}
    comm_to_commId = {}
    stream_to_streamId = {}
    comm_init_events = {}
    gpuId = -1

    for file_name in os.listdir(dir_path):  ## each file represents a process(GPU)
        if file_name.endswith('.sqlite'):
            P2P_state = 0  ## awaiting P2P or Group operations
            file_path = os.path.join(dir_path, file_name)
            
            gpuId += 1
            comm_to_commId[gpuId] = {}
            stream_to_streamId[gpuId] = {}

            pattern_HostName = r'nsys_report_([^.]+)\.'

            match = re.search(pattern_HostName, file_name)
            if match:
                host_name = match.group(1)
                print(f"Host Name: {host_name}")

            if host_name in HostName_To_GoalRank:
                goal_rank = HostName_To_GoalRank[host_name]
                GoalRank_To_NumOfGPUs[goal_rank] += 1
            else:
                goal_rank = len(HostName_To_GoalRank)
                HostName_To_GoalRank[host_name] = goal_rank
                GoalRank_To_NumOfGPUs[goal_rank] = 1
                nccl_events[goal_rank] = {}
                cupti_kernel_results[goal_rank] = {}
                comm_init_events[goal_rank] = {}

            nccl_events[goal_rank][gpuId] = {}    
            cupti_kernel_results[goal_rank][gpuId] = {}
            
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()
            cursor.execute("SELECT text, start, end FROM NVTX_EVENTS")  ## row[0]: text, row[1]: ts_start, row[2]: ts_end
            nvtx_events_results = cursor.fetchall()

            pattern_Comm_Info = r"comm (\S+) commId (\S+) rank (\d+) nranks (\d+)"
            pattern_Comm_NumOfChannels = r"(\d+) coll channels, (\d+) nvls channels, (\d+) p2p channels, (\d+) p2p channels per peer"

            pattern_Ring = r"comm (\S+) commHash (\S+) Rings \[(\d+)\] (\d+)->(\d+)->(\d+)"
            pattern_Tree = r"comm (\S+) commHash (\S+) Trees \[(\d+)\] (-?\d+)/(-?\d+)/(-?\d+)->(-?\d+)->(-?\d+)"

            pattern_nccl_AllReduce = r"ncclAllReduce\(\): comm (\S+), stream (\S+), data_size (\d+), red_op (\d+)"
            pattern_nccl_Broadcast = r"ncclBroadcast\(\): comm (\S+), stream (\S+), data_size (\d+), root (\d+)"

            pattern_nccl_Send = r"ncclSend\(\): comm (\S+), stream (\S+), data_size (\d+), receiver_rank: (\d+)"
            pattern_nccl_Recv = r"ncclRecv\(\): comm (\S+), stream (\S+), data_size: (\d+), sender_rank (\d+)"

            pattern_nccl_GroupStart = r"ncclGroupStart\(\)"
            pattern_nccl_GroupEnd = r"ncclGroupEnd\(\)"

            pattern_Coll_Algo_Proto = r"(\d+) Bytes -> Algo (\d+) proto (\d+) nThreads (\d+)"
            pattern_Coll_Elem = r"nWarps (\d+) count (\d+) redOpArg (\d+) chunkCount (\d+) workCount (\d+) lastChunkCount (\d+) workOffset (\d+)"
            pattern_P2P_Elem = r"Bytes (\d+) nWarps (\d+) peer (\d+) proto (\d+) countHi32 (\d+) countLo32 (\d+) chunkSize (\d+)"

            pattern_ncclKernel_Elem = r"ncclLaunchKernel()"

            for row in nvtx_events_results:
                if row[0]:
                    match_Comm_Info = re.search(pattern_Comm_Info, row[0])
                    match_Comm_NumOfChannels = re.search(pattern_Comm_NumOfChannels, row[0])

                    match_Ring = re.search(pattern_Ring, row[0])
                    match_Tree = re.search(pattern_Tree, row[0])

                    match_nccl_AllReduce = re.search(pattern_nccl_AllReduce, row[0])
                    match_nccl_Broadcast = re.search(pattern_nccl_Broadcast, row[0])

                    match_nccl_Send = re.search(pattern_nccl_Send, row[0])
                    match_nccl_Recv = re.search(pattern_nccl_Recv, row[0])

                    match_nccl_GroupStart = re.search(pattern_nccl_GroupStart, row[0])
                    match_nccl_GroupEnd = re.search(pattern_nccl_GroupEnd, row[0])

                    match_Coll_Algo_Proto = re.search(pattern_Coll_Algo_Proto, row[0])
                    match_Coll_Elem = re.search(pattern_Coll_Elem, row[0])
                    match_P2P_Elem = re.search(pattern_P2P_Elem, row[0])

                    match_ncclLaunchKernel = re.search(pattern_ncclKernel_Elem, row[0])

                    if match_Comm_Info:
                        comm = match_Comm_Info.group(1)
                        commId = match_Comm_Info.group(2)
                        my_rank = match_Comm_Info.group(3)
                        nranks = match_Comm_Info.group(4)

                        ts_init_start = row[1] // 1000  ## ns to us
                        ts_init_end = row[2] // 1000  ## ns to us

                        if commId not in comm_info:
                            comm_info[commId] = {}
                            comm_info[commId]["nranks"] = int(nranks)
                            comm_info[commId]["gpuId_To_rank"] = {}
                            comm_info[commId]["rank_To_rankInfo"] = {}
                            comm_info[commId]["comm_index"] = len(comm_info) - 1

                        comm_info[commId]["gpuId_To_rank"][gpuId] = my_rank
                        comm_info[commId]["rank_To_rankInfo"][my_rank] = {
                            "gpuId": gpuId,
                            "goal_rank": goal_rank,
                            "host_name": host_name,
                            "channel_info": {
                                "Ring": [],
                                "Tree": []
                            }
                        }

                        comm_to_commId[gpuId][comm] = commId
                        last_commId = commId

                        if gpuId not in comm_init_events[goal_rank]:
                            comm_init_events[goal_rank][gpuId] = {}
                            comm_init_events[goal_rank][gpuId]["ts_init_start"] = ts_init_start
                            comm_init_events[goal_rank][gpuId]["ts_init_end"] = ts_init_end

                    elif match_Comm_NumOfChannels:
                        num_P2P_channels_per_peer = match_Comm_NumOfChannels.group(4)
                        comm_info[last_commId]["NumOfP2PChannelsPerPeer"] = num_P2P_channels_per_peer

                    elif match_Ring:
                        comm = match_Ring.group(1)
                        channel_Id = match_Ring.group(3)
                        previous_rank = match_Ring.group(4)
                        my_rank = match_Ring.group(5)
                        next_rank = match_Ring.group(6)

                        commId = comm_to_commId[gpuId][comm]
                        comm_info[commId]["rank_To_rankInfo"][my_rank]["channel_info"]["Ring"].append(
                            {
                                "previous_rank": previous_rank,
                                "my_rank": my_rank,
                                "next_rank": next_rank,
                                "channel_Id": channel_Id
                            }
                        )

                    elif match_Tree:
                        comm = match_Tree.group(1)
                        channel_Id = match_Tree.group(3)
                        child_1_rank = match_Tree.group(4)
                        child_2_rank = match_Tree.group(5)
                        child_3_rank = match_Tree.group(6)
                        my_rank = match_Tree.group(7)
                        parent_rank = match_Tree.group(8)

                        commId = comm_to_commId[gpuId][comm]
                        
                        comm_info[commId]["rank_To_rankInfo"][my_rank]["channel_info"]["Tree"].append(
                            {
                                "child_1_rank": child_1_rank,
                                "child_2_rank": child_2_rank,
                                "child_3_rank": child_3_rank,
                                "my_rank": my_rank,
                                "parent_rank": parent_rank,
                                "channel_Id": channel_Id
                            }
                        )

                    elif match_nccl_AllReduce:  ## "ncclAllReduce\(\): comm (\S+), stream (\S+), data_size (\d+), red_op (\d+)"
                        comm = match_nccl_AllReduce.group(1)
                        stream = match_nccl_AllReduce.group(2)
                        data_size = int(match_nccl_AllReduce.group(3))
                        red_op = match_nccl_AllReduce.group(4)

                        ts_start = row[1] // 1000  ## ns to us
                        ts_end = row[2] // 1000  ## ns to us

                        commId = comm_to_commId[gpuId][comm]
                        my_rank = comm_info[commId]["gpuId_To_rank"][gpuId]

                        if comm_info[commId]["nranks"] > 1:
                            if stream not in stream_to_streamId[gpuId]:
                                stream_to_streamId[gpuId][stream] = len(stream_to_streamId[gpuId])

                            streamId = stream_to_streamId[gpuId][stream]
                            if streamId not in nccl_events[goal_rank][gpuId]:
                                nccl_events[goal_rank][gpuId][streamId] = []

                            nccl_events[goal_rank][gpuId][streamId].append(
                                {
                                    "event_type": "AllReduce",
                                    "commId": commId,
                                    "comm_index": comm_info[commId]["comm_index"],
                                    "streamId": streamId,
                                    "my_rank": my_rank,
                                    "gpuId": gpuId,
                                    "data_size": data_size,
                                    "red_op": red_op,
                                    "ts_start": ts_start,
                                    "ts_end": ts_end
                                }
                        )    

                            last_Coll_goal_rank = goal_rank
                            last_Coll_gpuId = gpuId
                            last_Coll_streamId = streamId
                            last_update = "Coll"

                    elif match_nccl_Broadcast:  ## "ncclBroadcast\(\): comm (\S+), stream (\S+), data_size (\d+), root (\d+)"
                        comm = match_nccl_Broadcast.group(1)
                        stream = match_nccl_Broadcast.group(2)
                        data_size = int(match_nccl_Broadcast.group(3))
                        root_rank = match_nccl_Broadcast.group(4)

                        ts_start = row[1] // 1000  ## ns to us
                        ts_end = row[2] // 1000  ## ns to us

                        commId = comm_to_commId[gpuId][comm]
                        my_rank = comm_info[commId]["gpuId_To_rank"][gpuId]

                        if comm_info[commId]["nranks"] > 1:
                            if stream not in stream_to_streamId[gpuId]:
                                stream_to_streamId[gpuId][stream] = len(stream_to_streamId[gpuId])

                            streamId = stream_to_streamId[gpuId][stream]
                            if streamId not in nccl_events[goal_rank][gpuId]:
                                nccl_events[goal_rank][gpuId][streamId] = []

                            nccl_events[goal_rank][gpuId][streamId].append(
                                {
                                    "event_type": "Broadcast",
                                    "commId": commId,
                                    "comm_index": comm_info[commId]["comm_index"],
                                    "streamId": streamId,
                                    "my_rank": my_rank,
                                    "gpuId": gpuId,
                                    "data_size": data_size,
                                    "root_rank": root_rank,
                                    "ts_start": ts_start,
                                    "ts_end": ts_end
                                }
                        ) 

                            last_Coll_goal_rank = goal_rank
                            last_Coll_gpuId = gpuId
                            last_Coll_streamId = streamId
                            last_update = "Coll"

                    elif match_Coll_Algo_Proto:  ## r"(\d+) Bytes -> Algo (\d+) proto (\d+) nThreads (\d+)"
                        nBytes = int(match_Coll_Algo_Proto.group(1))
                        algo = match_Coll_Algo_Proto.group(2)
                        proto = match_Coll_Algo_Proto.group(3)
                        nthreads = int(match_Coll_Algo_Proto.group(4))

                        assert nBytes == nccl_events[last_Coll_goal_rank][last_Coll_gpuId][last_Coll_streamId][-1]["data_size"], "nBytes not equal to data_size"
                        nccl_events[last_Coll_goal_rank][last_Coll_gpuId][last_Coll_streamId][-1]["algorithm"] = algo
                        nccl_events[last_Coll_goal_rank][last_Coll_gpuId][last_Coll_streamId][-1]["protocol"] = proto
                        nccl_events[last_Coll_goal_rank][last_Coll_gpuId][last_Coll_streamId][-1]["nthreads"] = nthreads

                    elif match_Coll_Elem: ## "nWarps (\d+) count (\d+) redOpArg (\d+) chunkCount (\d+) workCount (\d+) lastChunkCount (\d+) workOffset (\d+)"
                        nWarps = int(match_Coll_Elem.group(1))
                        count = int(match_Coll_Elem.group(2))
                        chunkCount = int(match_Coll_Elem.group(4))
                        workCount = int(match_Coll_Elem.group(5))
                        lastChunkCount = int(match_Coll_Elem.group(6))
                        workOffset = int(match_Coll_Elem.group(7))

                        assert nWarps * 32 == nccl_events[last_Coll_goal_rank][last_Coll_gpuId][last_Coll_streamId][-1]["nthreads"], "nWarps * 32 not equal to nthreads"
                        nccl_events[last_Coll_goal_rank][last_Coll_gpuId][last_Coll_streamId][-1]["count"] = count
                        nccl_events[last_Coll_goal_rank][last_Coll_gpuId][last_Coll_streamId][-1]["chunkCount"] = chunkCount
                        nccl_events[last_Coll_goal_rank][last_Coll_gpuId][last_Coll_streamId][-1]["workCount"] = workCount
                        nccl_events[last_Coll_goal_rank][last_Coll_gpuId][last_Coll_streamId][-1]["lastChunkCount"] = lastChunkCount
                        nccl_events[last_Coll_goal_rank][last_Coll_gpuId][last_Coll_streamId][-1]["workOffset"] = workOffset

                    elif match_nccl_GroupStart:
                        if P2P_state == 0:
                            ts_group_start = row[1] // 1000  ## ns to us
                            P2P_state = 1  ## awaiting ncclSend/ncclRecv, ignore ncclGroupStart/ncclGroupEnd in between

                        elif P2P_state == 2:
                            P2P_state = 3

                    elif match_nccl_GroupEnd:
                        if P2P_state == 3:
                            P2P_state = 2

                        elif P2P_state == 2:
                            ts_group_end = row[2] // 1000  ## ns to us
                            nccl_events[last_P2P_goal_rank][last_P2P_gpuId][last_P2P_streamId][-1]["ts_end"] = ts_group_end
                            next_P2P_elem_id = 0

                            P2P_state = 4

                    elif match_nccl_Send:
                        if P2P_state == 1:  ## "ncclSend\(\): comm (\S+), stream (\S+) data_size (\d+), receiver_rank: (\d+)"
                            comm = match_nccl_Send.group(1)
                            stream = match_nccl_Send.group(2)
                            data_size = int(match_nccl_Send.group(3))
                            peer_rank = match_nccl_Send.group(4)

                            commId = comm_to_commId[gpuId][comm]
                            my_rank = comm_info[commId]["gpuId_To_rank"][gpuId]

                            if comm_info[commId]["nranks"] > 1:
                                if stream not in stream_to_streamId[gpuId]:
                                    stream_to_streamId[gpuId][stream] = len(stream_to_streamId[gpuId])

                                streamId = stream_to_streamId[gpuId][stream]
                                if streamId not in nccl_events[goal_rank][gpuId]:
                                    nccl_events[goal_rank][gpuId][streamId] = []

                                nccl_events[goal_rank][gpuId][streamId].append(
                                    {
                                        "event_type": "GroupP2P",
                                        "commId": commId,
                                        "comm_index": comm_info[commId]["comm_index"],
                                        "streamId": streamId,
                                        "my_rank": my_rank,
                                        "gpuId": gpuId,
                                        "ts_start": ts_group_start,
                                        "P2P_events": [
                                            {
                                                "event_type": "Send",
                                                "data_size": data_size,
                                                "peer_rank": peer_rank
                                            }
                                        ]
                                    }
                            ) 
                                
                            P2P_state = 2

                        elif P2P_state == 2:
                            comm = match_nccl_Send.group(1)
                            stream = match_nccl_Send.group(2)
                            data_size = int(match_nccl_Send.group(3))
                            peer_rank = match_nccl_Send.group(4)

                            commId = comm_to_commId[gpuId][comm]
                            my_rank = comm_info[commId]["gpuId_To_rank"][gpuId]
                            streamId = stream_to_streamId[gpuId][stream]

                            nccl_events[goal_rank][gpuId][streamId][-1]["P2P_events"].append(
                                {
                                    "event_type": "Send",
                                    "data_size": data_size,
                                    "peer_rank": peer_rank
                                }
                            )

                            P2P_state = 2

                        last_P2P_goal_rank = goal_rank
                        last_P2P_gpuId = gpuId
                        last_P2P_streamId = streamId    
                        last_update = "P2P"

                    elif match_nccl_Recv:
                        if P2P_state == 1:  ## "ncclRecv\(\): comm (\S+), stream (\S+) data_size (\d+), sender_rank: (\d+)"
                            comm = match_nccl_Recv.group(1)
                            stream = match_nccl_Recv.group(2)
                            data_size = int(match_nccl_Recv.group(3))
                            peer_rank = match_nccl_Recv.group(4)

                            commId = comm_to_commId[gpuId][comm]
                            my_rank = comm_info[commId]["gpuId_To_rank"][gpuId]

                            if comm_info[commId]["nranks"] > 1:
                                if stream not in stream_to_streamId[gpuId]:
                                    stream_to_streamId[gpuId][stream] = len(stream_to_streamId[gpuId])

                                streamId = stream_to_streamId[gpuId][stream]
                                if streamId not in nccl_events[goal_rank][gpuId]:
                                    nccl_events[goal_rank][gpuId][streamId] = []

                                nccl_events[goal_rank][gpuId][streamId].append(
                                    {
                                        "event_type": "GroupP2P",
                                        "commId": commId,
                                        "comm_index": comm_info[commId]["comm_index"],
                                        "streamId": streamId,
                                        "my_rank": my_rank,
                                        "gpuId": gpuId,
                                        "ts_start": ts_group_start,
                                        "P2P_events": [
                                            {
                                                "event_type": "Recv",
                                                "data_size": data_size,
                                                "peer_rank": peer_rank
                                            }
                                        ]
                                    }
                            ) 
                                
                            P2P_state = 2

                        elif P2P_state == 2:
                            comm = match_nccl_Recv.group(1)
                            stream = match_nccl_Recv.group(2)
                            data_size = int(match_nccl_Recv.group(3))
                            peer_rank = match_nccl_Recv.group(4)

                            commId = comm_to_commId[gpuId][comm]
                            my_rank = comm_info[commId]["gpuId_To_rank"][gpuId]
                            streamId = stream_to_streamId[gpuId][stream]

                            nccl_events[goal_rank][gpuId][streamId][-1]["P2P_events"].append(
                                {
                                    "event_type": "Recv",
                                    "data_size": data_size,
                                    "peer_rank": peer_rank
                                }
                            )

                            P2P_state = 2

                        last_P2P_goal_rank = goal_rank
                        last_P2P_gpuId = gpuId
                        last_P2P_streamId = streamId
                        last_update = "P2P"

                    elif match_P2P_Elem:  ## "Bytes (\d+) nWarps (\d+) peer (\d+) proto (\d+) countHi32 (\d+) countLo32 (\d+) chunkSize (\d+)"
                        nWarps = int(match_P2P_Elem.group(2))
                        proto = match_P2P_Elem.group(4)
                        countHi32 = int(match_P2P_Elem.group(5))
                        countLo32 = int(match_P2P_Elem.group(6))
                        chunkSize = int(match_P2P_Elem.group(7))

                        nthreads = nWarps * 32

                        if P2P_state == 4:
                            group_event = nccl_events[last_P2P_goal_rank][last_P2P_gpuId][last_P2P_streamId][-1]
                            group_event["P2P_events"][next_P2P_elem_id]["nthreads"] = nthreads
                            group_event["P2P_events"][next_P2P_elem_id]["protocol"] = proto
                            group_event["P2P_events"][next_P2P_elem_id]["countHi32"] = countHi32
                            group_event["P2P_events"][next_P2P_elem_id]["countLo32"] = countLo32
                            group_event["P2P_events"][next_P2P_elem_id]["chunkSize"] = chunkSize
                            nccl_events[last_P2P_goal_rank][last_P2P_gpuId][last_P2P_streamId][-1] = group_event
                            next_P2P_elem_id += 1

                            if next_P2P_elem_id == len(group_event["P2P_events"]):
                                P2P_state = 0

                    elif match_ncclLaunchKernel:
                        ts_kernel = row[2] // 1000 ## ns to us

                        if last_update == "Coll":
                            nccl_events[last_Coll_goal_rank][last_Coll_gpuId][last_Coll_streamId][-1]["ts_kernel"] = ts_kernel

                        elif last_update == "P2P":
                            nccl_events[last_P2P_goal_rank][last_P2P_gpuId][last_P2P_streamId][-1]["ts_kernel"] = ts_kernel
            
            cursor.execute("SELECT id, value FROM StringIds")
            string_ids = cursor.fetchall()
            string_dict = {row[0]: row[1] for row in string_ids}
            
            cursor.execute("SELECT start, end, streamId, demangledName FROM CUPTI_ACTIVITY_KIND_KERNEL")
            cupti_kernel_events = cursor.fetchall()
            for row in cupti_kernel_events:
                start, end, streamId, demangled_name = row
                if string_dict[demangled_name].startswith("ncclKernel") or string_dict[demangled_name].startswith("ncclDevKernel"):
                    fields = string_dict[demangled_name].replace('(', '_').replace(')', '_').split('_')
                    if streamId not in cupti_kernel_results[goal_rank][gpuId]:
                        cupti_kernel_results[goal_rank][gpuId][streamId] = [] 

                    cupti_kernel_results[goal_rank][gpuId][streamId].append({
                        "gpu_event_type": fields[1],
                        "ts_gpu_start": start // 1000,
                        "ts_gpu_end": end // 1000,
                    })

            conn.close()
        
    return comm_init_events, nccl_events, cupti_kernel_results, comm_info, HostName_To_GoalRank

def events_list_equal(events_list_1, events_list_2):
    if len(events_list_1) != len(events_list_2):
        return 0
    
    else:
        num_events = len(events_list_1)
        for i in range(num_events):
            if events_list_1[i]["event_type"] != events_list_2[i]["gpu_event_type"]:
                if events_list_1[i]["event_type"] != "GroupP2P" and events_list_2[i]["gpu_event_type"] != "SendRecv":
                    return 0
                
        return 1        

def merge_nsys_events(nccl_events, cupti_kernel_results, comm_info):
    merged_events = {}
    for goal_rank, nccl_node_events in nccl_events.items():
        merged_events[goal_rank] = {}
        for gpuId, nccl_gpu_events in nccl_node_events.items():
            merged_events[goal_rank][gpuId] = {}
            for streamId, nccl_stream_events in nccl_gpu_events.items():
                merged_events[goal_rank][gpuId][streamId] = nccl_stream_events
                for gpu_streamId, cupti_stream_events in cupti_kernel_results[goal_rank][gpuId].items():
                    if events_list_equal(nccl_stream_events, cupti_stream_events):
                        for i in range(len(nccl_stream_events)):
                            merged_events[goal_rank][gpuId][streamId][i]["ts_gpu_start"] = cupti_stream_events[i]["ts_gpu_start"]
                            merged_events[goal_rank][gpuId][streamId][i]["ts_gpu_end"] = cupti_stream_events[i]["ts_gpu_end"]
                        
                        print(f"goal_rank: {goal_rank}, gpuId: {gpuId}, streamId: {streamId}, num_events: {len(merged_events[goal_rank][gpuId][streamId])}")

    return merged_events

def check_events_pair(events):
    events_pair = {}

    for goal_rank, goal_events in events.items():
        events_pair[goal_rank] = {}
        for gpuId, gpu_events in goal_events.items():
            events_pair[goal_rank][gpuId] = {}
            for streamId, stream_events in gpu_events.items():
                for event in stream_events:
                    if event["event_type"] not in events_pair[goal_rank][gpuId]:
                        events_pair[goal_rank][gpuId][event["event_type"]] = {}

                    if event["commId"] not in events_pair[goal_rank][gpuId][event["event_type"]]:
                        events_pair[goal_rank][gpuId][event["event_type"]][event["commId"]] = []

                    if streamId not in events_pair[goal_rank][gpuId][event["event_type"]][event["commId"]]:
                        events_pair[goal_rank][gpuId][event["event_type"]][event["commId"]].append(streamId)

    return events_pair

def get_events_dependency(nccl_events, comm_init_events, comm_info, goal_file_name):
    num_ranks = len(nccl_events)
    task_counter = 0
    with open(goal_file_name, 'w') as file:
        file.write(f"num_ranks {num_ranks}\n")

        for goal_rank in range(num_ranks):
            file.write(f"\nrank {goal_rank}")
            file.write(" {\n")

            goal_events = nccl_events[goal_rank]
            task_counter += 1
            file.write(f"l{task_counter}: calc 0\n") ## Starting point of the node
            node_start_calc_id = task_counter

            file.write(f"l{task_counter}: calc 0\n") ## Starting point of the node
            node_end_calc_id = task_counter

            for gpuId, gpu_events in goal_events.items():
                for streamId, stream_events in gpu_events.items():
                    last_event_end_time =  comm_init_events[goal_rank][gpuId]["ts_init_end"]
                    last_event_end_id = node_start_calc_id
                    for event_index, event in enumerate(stream_events): 
                        task_counter += 1
                        file.write(f"l{task_counter}: calc {event["ts_start"] - last_event_end_time}\n")  ## Calc between last gpu event end and host event start
                        file.write(f"l{task_counter} requires l{last_event_end_id}")

                        task_counter += 1
                        file.write(f"l{task_counter}: calc {event["ts_kernel"] - event["ts_start"]}\n")  ## Calc between gpu event start and host event start
                        file.write(f"l{task_counter} requires l{task_counter - 1}")

                        task_counter += 1
                        file.write(f"l{task_counter}: event_type {event["event_type"]} comm {event["comm_index"]} gpu {gpuId} stream {streamId}\n")  ## gpu event
                        file.write(f"l{task_counter} requires l{task_counter - 1}")
                        last_event_end_time = event["ts_gpu_end"]
                        last_event_end_id = task_counter

                        if event_index == len(stream_events) - 1:
                            file.write(f"l{node_end_calc_id} requires l{last_event_end_id}")

            file.write("}\n")

def main():
    # Get nsys events
    Dir_Path = './results/nsys_reports'
    Comm_Init_Events, NCCL_Events, CUPTI_Kernel_Results, Comm_Info, HostName_To_GoalRank = get_nsys_events(Dir_Path)  ## nccl_events, cupti_kernel_results, comm_info, HostName_To_GoalRank
    with open("./results/nsys_events_intermediate_output.json", "w") as json_file:
        json.dump(HostName_To_GoalRank, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(Comm_Info, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(CUPTI_Kernel_Results, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(NCCL_Events, json_file, indent=4)
        json_file.write('\n\n')
        json.dump(Comm_Init_Events, json_file, indent=4)
    print("Nsys_Events has been exported to nsys_events_intermediate_output.json")

    Merged_Events = merge_nsys_events(NCCL_Events, CUPTI_Kernel_Results, Comm_Info)
    with open("./results/nsys_events_merged_output.json", "w") as json_file:
        json.dump(Merged_Events, json_file, indent=4)
        json_file.write('\n\n')
    print("Merged_Events has been exported to nsys_events_merged_output.json")

    Events_Pair = check_events_pair(Merged_Events)
    with open("./results/nsys_events_pair_output.json", "w") as json_file:
        json.dump(Events_Pair, json_file, indent=4)
        json_file.write('\n\n')

    Goal_File_Name = "./results/Events_Dependency.goal"
    get_events_dependency(Merged_Events, Comm_Init_Events, Comm_Info, Goal_File_Name)

    # Merged_Npkit_Events = merge_npkit_events(Npkit_Paired_Events, GoalRank_To_FileRank)
    # with open("./results/npkit_merged_events_output.json", "w") as json_file:
    #     json.dump(Merged_Npkit_Events, json_file, indent=4)
    #     json_file.write('\n\n')
    # print("Merged_Npkit_Events has been exported to npkit_merged_events_output.json")

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