


Traceback (most recent call last):
  File "parser_sqlite2goal.py", line 1643, in <module>
    main()
  File "parser_sqlite2goal.py", line 1639, in main
    get_goal_file(Merged_Nsys_Events, Goal_File_Path, GoalRank_2_NumOfRanks)
  File "parser_sqlite2goal.py", line 1538, in get_goal_file
    net_event = net_channel_events["NVTX_EVENT_NET_SEND_TEST"][child_1_rank][net_event_pair_num - 1]
IndexError: list index out of range