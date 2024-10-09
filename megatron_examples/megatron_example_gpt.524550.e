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
srun: error: ault43: task 0: Exited with exit code 1
srun: error: ault44: task 1: Exited with exit code 1
