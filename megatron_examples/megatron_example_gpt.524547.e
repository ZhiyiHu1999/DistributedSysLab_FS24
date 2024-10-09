WARNING:torch.distributed.run:
*****************************************
Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
*****************************************
WARNING:torch.distributed.run:
*****************************************
Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
*****************************************
[W socket.cpp:426] [c10d] The server socket has failed to bind to [::]:6000 (errno: 98 - Address already in use).
[W socket.cpp:426] [c10d] The server socket has failed to bind to 0.0.0.0:6000 (errno: 98 - Address already in use).
[E socket.cpp:462] [c10d] The server socket has failed to listen on any local network address.
WARNING:torch.distributed.run:
*****************************************
Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
*****************************************
WARNING:torch.distributed.run:
*****************************************
Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
*****************************************
[W socket.cpp:426] [c10d] The server socket has failed to bind to [::]:6000 (errno: 98 - Address already in use).
[W socket.cpp:426] [c10d] The server socket has failed to bind to 0.0.0.0:6000 (errno: 98 - Address already in use).
[E socket.cpp:462] [c10d] The server socket has failed to listen on any local network address.
Traceback (most recent call last):
  File "/opt/conda/bin/torchrun", line 33, in <module>
    sys.exit(load_entry_point('torch==1.13.0a0+d321be6', 'console_scripts', 'torchrun')())
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/multiprocessing/errors/__init__.py", line 345, in wrapper
    return f(*args, **kwargs)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/run.py", line 761, in main
    run(args)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/run.py", line 752, in run
    elastic_launch(
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/launcher/api.py", line 132, in __call__
    return launch_agent(self._config, self._entrypoint, list(args))
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/launcher/api.py", line 237, in launch_agent
    result = agent.run()
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/metrics/api.py", line 129, in wrapper
    result = f(*args, **kwargs)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/agent/server/api.py", line 709, in run
    result = self._invoke_run(role)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/agent/server/api.py", line 844, in _invoke_run
    self._initialize_workers(self._worker_group)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/metrics/api.py", line 129, in wrapper
    result = f(*args, **kwargs)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/agent/server/api.py", line 678, in _initialize_workers
    self._rendezvous(worker_group)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/metrics/api.py", line 129, in wrapper
    result = f(*args, **kwargs)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/agent/server/api.py", line 538, in _rendezvous
    store, group_rank, group_world_size = spec.rdzv_handler.next_rendezvous()
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/rendezvous/static_tcp_rendezvous.py", line 55, in next_rendezvous
    self._store = TCPStore(  # type: ignore[call-arg]
RuntimeError: The server socket has failed to listen on any local network address. The server socket has failed to bind to [::]:6000 (errno: 98 - Address already in use). The server socket has failed to bind to 0.0.0.0:6000 (errno: 98 - Address already in use).
Traceback (most recent call last):
  File "/opt/conda/bin/torchrun", line 33, in <module>
    sys.exit(load_entry_point('torch==1.13.0a0+d321be6', 'console_scripts', 'torchrun')())
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/multiprocessing/errors/__init__.py", line 345, in wrapper
    return f(*args, **kwargs)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/run.py", line 761, in main
    run(args)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/run.py", line 752, in run
    elastic_launch(
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/launcher/api.py", line 132, in __call__
    return launch_agent(self._config, self._entrypoint, list(args))
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/launcher/api.py", line 237, in launch_agent
    result = agent.run()
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/metrics/api.py", line 129, in wrapper
    result = f(*args, **kwargs)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/agent/server/api.py", line 709, in run
    result = self._invoke_run(role)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/agent/server/api.py", line 844, in _invoke_run
    self._initialize_workers(self._worker_group)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/metrics/api.py", line 129, in wrapper
    result = f(*args, **kwargs)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/agent/server/api.py", line 678, in _initialize_workers
    self._rendezvous(worker_group)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/metrics/api.py", line 129, in wrapper
    result = f(*args, **kwargs)
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/agent/server/api.py", line 538, in _rendezvous
    store, group_rank, group_world_size = spec.rdzv_handler.next_rendezvous()
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/elastic/rendezvous/static_tcp_rendezvous.py", line 55, in next_rendezvous
    self._store = TCPStore(  # type: ignore[call-arg]
RuntimeError: The server socket has failed to listen on any local network address. The server socket has failed to bind to [::]:6000 (errno: 98 - Address already in use). The server socket has failed to bind to 0.0.0.0:6000 (errno: 98 - Address already in use).
srun: error: ault44: task 3: Exited with exit code 1
srun: error: ault43: task 1: Exited with exit code 1
srun: got SIGCONT
slurmstepd: error: *** STEP 524547.1 ON ault43 CANCELLED AT 2024-10-09T23:20:53 ***
slurmstepd: error: *** JOB 524547 ON ault43 CANCELLED AT 2024-10-09T23:20:53 ***
srun: forcing job termination
srun: Job step aborted: Waiting up to 32 seconds for job step to finish.
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/blkio/system.slice/slurmd.service/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/net_cls,net_prio/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/freezer/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/systemd/system.slice/slurmd.service/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/devices/system.slice/slurmd.service/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/cpu,cpuacct/system.slice/slurmd.service/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/pids/system.slice/slurmd.service/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/cpuset/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/memory/slurm/uid_29811/job_524547/step_1/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/net_cls,net_prio/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/perf_event/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/rdma/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/cpu,cpuacct/system.slice/slurmd.service/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/hugetlb/container-iplaccbiyxrqquel: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/devices/system.slice/slurmd.service/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/cpu,cpuacct/system.slice/slurmd.service/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/pids/system.slice/slurmd.service/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/hugetlb/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/freezer/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/net_cls,net_prio/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/memory/slurm/uid_29811/job_524547/step_1/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/blkio/system.slice/slurmd.service/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/net_cls,net_prio/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/cpuset/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/cpu,cpuacct/system.slice/slurmd.service/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/perf_event/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/rdma/container-fdefmpipwuwnwjlb: device or resource busy"
time="2024-10-09T23:20:53+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/systemd/system.slice/slurmd.service/container-fdefmpipwuwnwjlb: device or resource busy"
