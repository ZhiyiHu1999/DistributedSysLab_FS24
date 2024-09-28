Traceback (most recent call last):
  File "npkit_trace_generator.py", line 265, in <module>
    convert_npkit_dump_to_trace(args.npkit_dump_dir, args.output_dir, npkit_event_def)
  File "npkit_trace_generator.py", line 247, in convert_npkit_dump_to_trace
    cpu_events = parse_cpu_event_file(npkit_dump_dir, npkit_event_def, rank, channel, cpu_clock_scale)
  File "npkit_trace_generator.py", line 144, in parse_cpu_event_file
    event_type = npkit_event_def['id_to_type'][parsed_cpu_event['id']]
KeyError: 210
