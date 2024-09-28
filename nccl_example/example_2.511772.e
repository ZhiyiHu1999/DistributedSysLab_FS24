Traceback (most recent call last):
  File "npkit_trace_generator.py", line 262, in <module>
    convert_npkit_dump_to_trace(args.npkit_dump_dir, args.output_dir, npkit_event_def)
  File "npkit_trace_generator.py", line 244, in convert_npkit_dump_to_trace
    cpu_events = parse_cpu_event_file(npkit_dump_dir, npkit_event_def, rank, channel, cpu_clock_scale)
  File "npkit_trace_generator.py", line 184, in parse_cpu_event_file
    fiber_id = slot_to_fiber_id[slot]
KeyError: 0
