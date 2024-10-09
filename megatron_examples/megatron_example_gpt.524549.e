WARNING:torch.distributed.run:
*****************************************
Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
*****************************************
WARNING:torch.distributed.run:
*****************************************
Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
*****************************************
[W socket.cpp:426] [c10d] The server socket has failed to bind to [::]:29500 (errno: 98 - Address already in use).
[W socket.cpp:426] [c10d] The server socket has failed to bind to 0.0.0.0:29500 (errno: 98 - Address already in use).
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
RuntimeError: The server socket has failed to listen on any local network address. The server socket has failed to bind to [::]:29500 (errno: 98 - Address already in use). The server socket has failed to bind to 0.0.0.0:29500 (errno: 98 - Address already in use).
WARNING:torch.distributed.run:
*****************************************
Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
*****************************************
WARNING:torch.distributed.run:
*****************************************
Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
*****************************************
[W socket.cpp:426] [c10d] The server socket has failed to bind to [::]:29500 (errno: 98 - Address already in use).
[W socket.cpp:426] [c10d] The server socket has failed to bind to 0.0.0.0:29500 (errno: 98 - Address already in use).
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
RuntimeError: The server socket has failed to listen on any local network address. The server socket has failed to bind to [::]:29500 (errno: 98 - Address already in use). The server socket has failed to bind to 0.0.0.0:29500 (errno: 98 - Address already in use).
srun: error: ault44: task 3: Exited with exit code 1
srun: error: ault43: task 0: Exited with exit code 1
srun: Job step aborted: Waiting up to 32 seconds for job step to finish.
slurmstepd: error: *** JOB 524549 ON ault43 CANCELLED AT 2024-10-09T23:25:32 ***
srun: got SIGCONT
srun: forcing job termination
slurmstepd: error: *** STEP 524549.1 ON ault43 CANCELLED AT 2024-10-09T23:25:32 ***
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/memory/slurm/uid_29811/job_524549/step_1/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/cpu,cpuacct/system.slice/slurmd.service/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/freezer/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/systemd/system.slice/slurmd.service/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/pids/system.slice/slurmd.service/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/cpuset/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/devices/system.slice/slurmd.service/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/hugetlb/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/net_cls,net_prio/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/rdma/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/cpu,cpuacct/system.slice/slurmd.service/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/blkio/system.slice/slurmd.service/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/net_cls,net_prio/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/perf_event/container-gsnmgsqigkzhjttd: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/perf_event/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/rdma/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/devices/system.slice/slurmd.service/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/pids/system.slice/slurmd.service/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/hugetlb/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/cpuset/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/systemd/system.slice/slurmd.service/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/memory/slurm/uid_29811/job_524549/step_1/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/net_cls,net_prio/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/net_cls,net_prio/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/freezer/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/cpu,cpuacct/system.slice/slurmd.service/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/cpu,cpuacct/system.slice/slurmd.service/container-nlrrufeumtgxmnxa: device or resource busy"
time="2024-10-09T23:25:32+02:00" level=warning msg="Failed to remove cgroup (will retry)" error="rmdir /sys/fs/cgroup/blkio/system.slice/slurmd.service/container-nlrrufeumtgxmnxa: device or resource busy"
