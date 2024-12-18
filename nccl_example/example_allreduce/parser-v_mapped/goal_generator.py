import sqlite3
import os
import re
import json
import argparse

from get_traced_events import *
from get_goal_file import *

def main():
    parser = argparse.ArgumentParser(description='Process SQLite to Goal file.')
    
    parser.add_argument('-r', '--use-slots', action='store_true',
                        help='Use get_goal_file_slots instead of get_goal_file.')

    args = parser.parse_args()

    npkit_event_def = parse_npkit_event_header("/users/zhu/nccl_nvtx_npkit/nccl/src/include/npkit/npkit_event.h")
    npkit_trace = convert_npkit_dump_to_trace("./results/npkit_run/npkit_dump", "./results/npkit_run/npkit_trace", npkit_event_def)

    # json_file = './results/npkit_run/npkit_trace/job_example_allreduce/npkit_event_trace.json'
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

    Transformed_Nsys_Events = transform_nsys_events(Npkit_Paired_Events, Nsys_Events)
    with open("./results/transformed_nsys_events_output.json", "w") as json_file:
        json.dump(Transformed_Nsys_Events, json_file, indent=4)
    print("Transformed_Nsys_Events has been exported to transformed_nsys_events_output.json")

    Mapped_Npkit_Events = map_npkit_to_nsys(Npkit_Paired_Events, Transformed_Nsys_Events, FileRank_2_GoalRank)
    with open("./results/npkit_mapped_events_output.json", "w") as json_file:
        json.dump(Mapped_Npkit_Events, json_file, indent=4)
        json_file.write('\n\n')
    print("Mapped_Npkit_Events has been exported to npkit_mapped_events_output.json")

    Combined_Events = combine_npkit_nsys_events(Mapped_Npkit_Events, Transformed_Nsys_Events)
    with open("./results/combined_events_output.json", "w") as json_file:
        json.dump(Combined_Events, json_file, indent=4)
    print("Combined_Events has been exported to combined_events_output.json")

    Merged_Nsys_Events = merge_nsys_events(Combined_Events, FileRank_2_GoalRank, HostName_2_GoalRank)
    with open("./results/merged_events_output.json", "w") as json_file:
        json.dump(Merged_Nsys_Events, json_file, indent=4)
    print("Merged_Nsys_Events has been exported to merged_events_output.json")

    Goal_File_Path = './results/example_2.goal'
    if args.use_slots:
        get_goal_file_slots(Merged_Nsys_Events, Goal_File_Path, GoalRank_2_NumOfRanks)
        print("Final goal file has been generated using get_goal_file_slots.")
    else:
        get_goal_file(Merged_Nsys_Events, Goal_File_Path, GoalRank_2_NumOfRanks)
        print("Final goal file has been generated using get_goal_file.")

if __name__ == '__main__':
    main()