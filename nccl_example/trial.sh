#!/bin/bash

export NPKIT_RUN_DIR="/users/zhu/DistributedSysLab_FS24/nccl_example/npkit_run"
# Tag of this NPKit run.
npkit_run_tag="job_example_2"
# Path to NPKit dump directory.
npkit_dump_dir="${NPKIT_RUN_DIR}/npkit_dump/${npkit_run_tag}"
# Path to NPKit post-process directory.
npkit_trace_dir="${NPKIT_RUN_DIR}/npkit_trace/${npkit_run_tag}"
# Path to NPKit result directory.
npkit_result_dir="${NPKIT_RUN_DIR}/npkit_result/${npkit_run_tag}"
export NPKIT_DUMP_DIR="${NPKIT_RUN_DIR}/npkit_dump/${npkit_run_tag}" # Path to generate dump files


python3 npkit_trace_generator.py --npkit_dump_dir=$npkit_dump_dir\
                                 --npkit_event_header_path="/users/zhu/nccl_npkit/nccl/src/include/npkit/npkit_event.h"\
                                 --output_dir="/users/zhu/DistributedSysLab_FS24/nccl_example/trial"