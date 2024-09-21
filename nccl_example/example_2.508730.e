Traceback (most recent call last):
  File "npkit_trace_generator.py", line 262, in <module>
    convert_npkit_dump_to_trace(args.npkit_dump_dir, args.output_dir, npkit_event_def)
  File "npkit_trace_generator.py", line 244, in convert_npkit_dump_to_trace
    cpu_events = parse_cpu_event_file(npkit_dump_dir, npkit_event_def, rank, channel, cpu_clock_scale)
  File "npkit_trace_generator.py", line 137, in parse_cpu_event_file
    with open(cpu_event_file_path, 'rb') as f:
FileNotFoundError: [Errno 2] No such file or directory: '/users/zhu/DistributedSysLab_FS24/nccl_example/results/npkit_run/npkit_dump/job_example_2/cpu_events_rank_2_channel_28'
