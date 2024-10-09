WARNING:torch.distributed.run:
*****************************************
Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
*****************************************
WARNING:torch.distributed.run:
*****************************************
Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
*****************************************
[W socket.cpp:426] [c10d] The server socket has failed to bind to [::]:6000 (errno: 98 - Address already in use).
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
[W socket.cpp:426] [c10d] The server socket has failed to bind to 0.0.0.0:6000 (errno: 98 - Address already in use).
[E socket.cpp:462] [c10d] The server socket has failed to listen on any local network address.
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
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
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
/opt/conda/bin/python: can't open file 'pretrain_gpt.py': [Errno 2] No such file or directory
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
srun: error: ault44: task 2: Exited with exit code 1
srun: error: ault43: task 0: Exited with exit code 1
ERROR:torch.distributed.elastic.multiprocessing.api:failed (exitcode: 2) local_rank: 0 (pid: 1006189) of binary: /opt/conda/bin/python
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
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/launcher/api.py", line 246, in launch_agent
    raise ChildFailedError(
torch.distributed.elastic.multiprocessing.errors.ChildFailedError: 
============================================================
pretrain_gpt.py FAILED
------------------------------------------------------------
Failures:
[1]:
  time      : 2024-10-09_21:16:02
  host      : ault44.cscs.ch
  rank      : 1 (local_rank: 1)
  exitcode  : 2 (pid: 1006190)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
[2]:
  time      : 2024-10-09_21:16:02
  host      : ault44.cscs.ch
  rank      : 2 (local_rank: 2)
  exitcode  : 2 (pid: 1006191)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
[3]:
  time      : 2024-10-09_21:16:02
  host      : ault44.cscs.ch
  rank      : 3 (local_rank: 3)
  exitcode  : 2 (pid: 1006192)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
[4]:
  time      : 2024-10-09_21:16:02
  host      : ault44.cscs.ch
  rank      : 4 (local_rank: 4)
  exitcode  : 2 (pid: 1006193)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
[5]:
  time      : 2024-10-09_21:16:02
  host      : ault44.cscs.ch
  rank      : 5 (local_rank: 5)
  exitcode  : 2 (pid: 1006194)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
[6]:
  time      : 2024-10-09_21:16:02
  host      : ault44.cscs.ch
  rank      : 6 (local_rank: 6)
  exitcode  : 2 (pid: 1006195)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
[7]:
  time      : 2024-10-09_21:16:02
  host      : ault44.cscs.ch
  rank      : 7 (local_rank: 7)
  exitcode  : 2 (pid: 1006196)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
------------------------------------------------------------
Root Cause (first observed failure):
[0]:
  time      : 2024-10-09_21:16:02
  host      : ault44.cscs.ch
  rank      : 0 (local_rank: 0)
  exitcode  : 2 (pid: 1006189)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
============================================================
ERROR:torch.distributed.elastic.multiprocessing.api:failed (exitcode: 2) local_rank: 0 (pid: 865062) of binary: /opt/conda/bin/python
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
  File "/opt/conda/lib/python3.8/site-packages/torch/distributed/launcher/api.py", line 246, in launch_agent
    raise ChildFailedError(
torch.distributed.elastic.multiprocessing.errors.ChildFailedError: 
============================================================
pretrain_gpt.py FAILED
------------------------------------------------------------
Failures:
[1]:
  time      : 2024-10-09_21:16:02
  host      : ault43.cscs.ch
  rank      : 1 (local_rank: 1)
  exitcode  : 2 (pid: 865063)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
[2]:
  time      : 2024-10-09_21:16:02
  host      : ault43.cscs.ch
  rank      : 2 (local_rank: 2)
  exitcode  : 2 (pid: 865064)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
[3]:
  time      : 2024-10-09_21:16:02
  host      : ault43.cscs.ch
  rank      : 3 (local_rank: 3)
  exitcode  : 2 (pid: 865065)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
[4]:
  time      : 2024-10-09_21:16:02
  host      : ault43.cscs.ch
  rank      : 4 (local_rank: 4)
  exitcode  : 2 (pid: 865066)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
[5]:
  time      : 2024-10-09_21:16:02
  host      : ault43.cscs.ch
  rank      : 5 (local_rank: 5)
  exitcode  : 2 (pid: 865067)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
[6]:
  time      : 2024-10-09_21:16:02
  host      : ault43.cscs.ch
  rank      : 6 (local_rank: 6)
  exitcode  : 2 (pid: 865068)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
[7]:
  time      : 2024-10-09_21:16:02
  host      : ault43.cscs.ch
  rank      : 7 (local_rank: 7)
  exitcode  : 2 (pid: 865069)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
------------------------------------------------------------
Root Cause (first observed failure):
[0]:
  time      : 2024-10-09_21:16:02
  host      : ault43.cscs.ch
  rank      : 0 (local_rank: 0)
  exitcode  : 2 (pid: 865062)
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
============================================================
srun: error: ault44: task 3: Exited with exit code 1
srun: error: ault43: task 1: Exited with exit code 1
