import sqlite3
import os
import re
import json
import argparse

from get_traced_events import *
from get_goal_file import *

def main():
    #### Get npkit events
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

    Goal_File_Path = './results/example_2.goal'
    get_goal_file(Merged_Npkit_Events, NCCL_API_Events, Comm_Info, HostName_To_GoalRank, FileRank_To_GoalRank, Goal_File_Path)
    print("Final goal file has been generated using get_goal_file.")

if __name__ == '__main__':
    main()