No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
2024-10-14 00:54:04.827 | INFO     | __main__:log_dist:54 - [Rank 0] Creating Experiment Directory
2024-10-14 00:54:05.088 | INFO     | __main__:log_dist:54 - [Rank 0] Experiment Directory created at /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed/bert_pretrain.2024.10.13.15.54.5.addjtvxg
2024-10-14 00:54:05.091 | INFO     | __main__:log_dist:54 - [Rank 0] Creating Datasets
2024-10-14 00:54:10.744 | INFO     | __main__:log_dist:54 - [Rank 0] Dataset Creation Done
2024-10-14 00:54:10.744 | INFO     | __main__:log_dist:54 - [Rank 0] Creating Model
2024-10-14 00:54:11.075 | INFO     | __main__:log_dist:54 - [Rank 0] Model Creation Done
2024-10-14 00:54:11.075 | INFO     | __main__:log_dist:54 - [Rank 0] Creating DeepSpeed engine
Using /users/zhu/.cache/torch_extensions/py312_cu118 as PyTorch extensions root...
Using /users/zhu/.cache/torch_extensions/py312_cu118 as PyTorch extensions root...
Emitting ninja build file /users/zhu/.cache/torch_extensions/py312_cu118/cpu_adam/build.ninja...
Building extension module cpu_adam...
Allowing ninja to set a default number of workers... (overridable by setting the environment variable MAX_JOBS=N)
[rank1]: Traceback (most recent call last):
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/torch/utils/cpp_extension.py", line 2105, in _run_ninja_build
[rank1]:     subprocess.run(
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/subprocess.py", line 571, in run
[rank1]:     raise CalledProcessError(retcode, process.args,
[rank1]: subprocess.CalledProcessError: Command '['ninja', '-v']' returned non-zero exit status 1.

[rank1]: The above exception was the direct cause of the following exception:

[rank1]: Traceback (most recent call last):
[rank1]:   File "/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/train_bert_ds.py", line 864, in <module>
[rank1]:     fire.Fire(train)
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/fire/core.py", line 141, in Fire
[rank1]:     component_trace = _Fire(component, args, parsed_flag_args, context, name)
[rank1]:                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/fire/core.py", line 466, in _Fire
[rank1]:     component, remaining_args = _CallAndUpdateTrace(
[rank1]:                                 ^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/fire/core.py", line 681, in _CallAndUpdateTrace
[rank1]:     component = fn(*varargs, **kwargs)
[rank1]:                 ^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/train_bert_ds.py", line 802, in train
[rank1]:     model, _, _, _ = deepspeed.initialize(model=model,
[rank1]:                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/__init__.py", line 193, in initialize
[rank1]:     engine = DeepSpeedEngine(args=args,
[rank1]:              ^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/runtime/engine.py", line 313, in __init__
[rank1]:     self._configure_optimizer(optimizer, model_parameters)
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/runtime/engine.py", line 1276, in _configure_optimizer
[rank1]:     basic_optimizer = self._configure_basic_optimizer(model_parameters)
[rank1]:                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/runtime/engine.py", line 1347, in _configure_basic_optimizer
[rank1]:     optimizer = DeepSpeedCPUAdam(model_parameters,
[rank1]:                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/ops/adam/cpu_adam.py", line 94, in __init__
[rank1]:     self.ds_opt_adam = CPUAdamBuilder().load()
[rank1]:                        ^^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/ops/op_builder/builder.py", line 531, in load
[rank1]:     return self.jit_load(verbose)
[rank1]:            ^^^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/ops/op_builder/builder.py", line 578, in jit_load
[rank1]:     op_module = load(name=self.name,
[rank1]:                 ^^^^^^^^^^^^^^^^^^^^
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/torch/utils/cpp_extension.py", line 1312, in load
[rank1]:     return _jit_compile(
[rank1]:            ^^^^^^^^^^^^^
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/torch/utils/cpp_extension.py", line 1722, in _jit_compile
[rank1]:     _write_ninja_file_and_build_library(
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/torch/utils/cpp_extension.py", line 1834, in _write_ninja_file_and_build_library
[rank1]:     _run_ninja_build(
[rank1]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/torch/utils/cpp_extension.py", line 2121, in _run_ninja_build
[rank1]:     raise RuntimeError(message) from e
[rank1]: RuntimeError: Error building extension 'cpu_adam'
Loading extension module cpu_adam...
[rank0]: Traceback (most recent call last):
[rank0]:   File "/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/train_bert_ds.py", line 864, in <module>
[rank0]:     fire.Fire(train)
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/fire/core.py", line 141, in Fire
[rank0]:     component_trace = _Fire(component, args, parsed_flag_args, context, name)
[rank0]:                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/fire/core.py", line 466, in _Fire
[rank0]:     component, remaining_args = _CallAndUpdateTrace(
[rank0]:                                 ^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/fire/core.py", line 681, in _CallAndUpdateTrace
[rank0]:     component = fn(*varargs, **kwargs)
[rank0]:                 ^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/train_bert_ds.py", line 802, in train
[rank0]:     model, _, _, _ = deepspeed.initialize(model=model,
[rank0]:                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/__init__.py", line 193, in initialize
[rank0]:     engine = DeepSpeedEngine(args=args,
[rank0]:              ^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/runtime/engine.py", line 313, in __init__
[rank0]:     self._configure_optimizer(optimizer, model_parameters)
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/runtime/engine.py", line 1276, in _configure_optimizer
[rank0]:     basic_optimizer = self._configure_basic_optimizer(model_parameters)
[rank0]:                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/runtime/engine.py", line 1347, in _configure_basic_optimizer
[rank0]:     optimizer = DeepSpeedCPUAdam(model_parameters,
[rank0]:                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/ops/adam/cpu_adam.py", line 94, in __init__
[rank0]:     self.ds_opt_adam = CPUAdamBuilder().load()
[rank0]:                        ^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/ops/op_builder/builder.py", line 531, in load
[rank0]:     return self.jit_load(verbose)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/ops/op_builder/builder.py", line 578, in jit_load
[rank0]:     op_module = load(name=self.name,
[rank0]:                 ^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/torch/utils/cpp_extension.py", line 1312, in load
[rank0]:     return _jit_compile(
[rank0]:            ^^^^^^^^^^^^^
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/torch/utils/cpp_extension.py", line 1747, in _jit_compile
[rank0]:     return _import_module_from_library(name, build_directory, is_python_module)
[rank0]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "/users/zhu/anaconda3/lib/python3.12/site-packages/torch/utils/cpp_extension.py", line 2141, in _import_module_from_library
[rank0]:     module = importlib.util.module_from_spec(spec)
[rank0]:              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[rank0]:   File "<frozen importlib._bootstrap>", line 813, in module_from_spec
[rank0]:   File "<frozen importlib._bootstrap_external>", line 1289, in create_module
[rank0]:   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
[rank0]: ImportError: /users/zhu/.cache/torch_extensions/py312_cu118/cpu_adam/cpu_adam.so: cannot open shared object file: No such file or directory
Exception ignored in: <function DeepSpeedCPUAdam.__del__ at 0x155470f83880>
Traceback (most recent call last):
  File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/ops/adam/cpu_adam.py", line 102, in __del__
    self.ds_opt_adam.destroy_adam(self.opt_id)
    ^^^^^^^^^^^^^^^^
AttributeError: 'DeepSpeedCPUAdam' object has no attribute 'ds_opt_adam'
Exception ignored in: <function DeepSpeedCPUAdam.__del__ at 0x155470f87880>
Traceback (most recent call last):
  File "/users/zhu/anaconda3/lib/python3.12/site-packages/deepspeed/ops/adam/cpu_adam.py", line 102, in __del__
AttributeError: 'DeepSpeedCPUAdam' object has no attribute 'ds_opt_adam'
[rank1]:[W1014 00:54:32.329567195 ProcessGroupNCCL.cpp:1168] Warning: WARNING: process group has NOT been destroyed before we destruct ProcessGroupNCCL. On normal program exit, the application should call destroy_process_group to ensure that any pending NCCL operations have finished in this process. In rare cases this process can exit before this point and block the progress of another member of the process group. This constraint has always been present,  but this warning has only been added since PyTorch 2.4 (function operator())
[rank0]:[W1014 00:54:32.470090861 ProcessGroupNCCL.cpp:1168] Warning: WARNING: process group has NOT been destroyed before we destruct ProcessGroupNCCL. On normal program exit, the application should call destroy_process_group to ensure that any pending NCCL operations have finished in this process. In rare cases this process can exit before this point and block the progress of another member of the process group. This constraint has always been present,  but this warning has only been added since PyTorch 2.4 (function operator())
srun: error: ault43: task 0: Exited with exit code 1
srun: error: ault44: task 1: Exited with exit code 1
