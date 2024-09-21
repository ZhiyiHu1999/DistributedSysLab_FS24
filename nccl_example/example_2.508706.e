Traceback (most recent call last):
  File "npkit_trace_generator.py", line 262, in <module>
    convert_npkit_dump_to_trace(args.npkit_dump_dir, args.output_dir, npkit_event_def)
  File "npkit_trace_generator.py", line 240, in convert_npkit_dump_to_trace
    gpu_events = parse_gpu_event_file(npkit_dump_dir, npkit_event_def, rank, buf_idx, gpu_clock_scale, cpu_clock_scale)
  File "npkit_trace_generator.py", line 63, in parse_gpu_event_file
    with open(gpu_event_file_path, 'rb') as f:
FileNotFoundError: [Errno 2] No such file or directory: '/users/zhu/DistributedSysLab_FS24/nccl_example/results/npkit_run/npkit_dump/job_example_2/gpu_events_rank_0_buf_380'
