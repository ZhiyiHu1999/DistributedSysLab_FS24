/users/zhu/.local/lib/python3.6/site-packages/torch/cuda/__init__.py:143: UserWarning: 
NVIDIA GeForce RTX 3090 with CUDA capability sm_86 is not compatible with the current PyTorch installation.
The current PyTorch install supports CUDA capabilities sm_37 sm_50 sm_60 sm_70.
If you want to use the NVIDIA GeForce RTX 3090 GPU with PyTorch, please check the instructions at https://pytorch.org/get-started/locally/

  warnings.warn(incompatible_device_warn.format(device_name, capability, " ".join(arch_list), device_name))
/users/zhu/.local/lib/python3.6/site-packages/torch/cuda/__init__.py:143: UserWarning: 
NVIDIA GeForce RTX 3090 with CUDA capability sm_86 is not compatible with the current PyTorch installation.
The current PyTorch install supports CUDA capabilities sm_37 sm_50 sm_60 sm_70.
If you want to use the NVIDIA GeForce RTX 3090 GPU with PyTorch, please check the instructions at https://pytorch.org/get-started/locally/

  warnings.warn(incompatible_device_warn.format(device_name, capability, " ".join(arch_list), device_name))
/users/zhu/.local/lib/python3.6/site-packages/torch/cuda/__init__.py:143: UserWarning: 
NVIDIA GeForce RTX 3090 with CUDA capability sm_86 is not compatible with the current PyTorch installation.
The current PyTorch install supports CUDA capabilities sm_37 sm_50 sm_60 sm_70.
If you want to use the NVIDIA GeForce RTX 3090 GPU with PyTorch, please check the instructions at https://pytorch.org/get-started/locally/

  warnings.warn(incompatible_device_warn.format(device_name, capability, " ".join(arch_list), device_name))
/users/zhu/.local/lib/python3.6/site-packages/torch/cuda/__init__.py:143: UserWarning: 
NVIDIA GeForce RTX 3090 with CUDA capability sm_86 is not compatible with the current PyTorch installation.
The current PyTorch install supports CUDA capabilities sm_37 sm_50 sm_60 sm_70.
If you want to use the NVIDIA GeForce RTX 3090 GPU with PyTorch, please check the instructions at https://pytorch.org/get-started/locally/

  warnings.warn(incompatible_device_warn.format(device_name, capability, " ".join(arch_list), device_name))
Traceback (most recent call last):
  File "/users/zhu/examples/mnist/main.py", line 144, in <module>
    main()
  File "/users/zhu/examples/mnist/main.py", line 135, in main
    train(args, model, device, train_loader, optimizer, epoch)
  File "/users/zhu/examples/mnist/main.py", line 41, in train
    output = model(data)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/module.py", line 1102, in _call_impl
    return forward_call(*input, **kwargs)
  File "/users/zhu/examples/mnist/main.py", line 21, in forward
    x = self.conv1(x)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/module.py", line 1102, in _call_impl
    return forward_call(*input, **kwargs)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/conv.py", line 446, in forward
    return self._conv_forward(input, self.weight, self.bias)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/conv.py", line 443, in _conv_forward
    self.padding, self.dilation, self.groups)
RuntimeError: CUDA error: no kernel image is available for execution on the device
CUDA kernel errors might be asynchronously reported at some other API call,so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1.
srun: error: ault44: task 2: Exited with exit code 1
Traceback (most recent call last):
  File "/users/zhu/examples/mnist/main.py", line 144, in <module>
    main()
  File "/users/zhu/examples/mnist/main.py", line 135, in main
    train(args, model, device, train_loader, optimizer, epoch)
  File "/users/zhu/examples/mnist/main.py", line 41, in train
    output = model(data)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/module.py", line 1102, in _call_impl
    return forward_call(*input, **kwargs)
  File "/users/zhu/examples/mnist/main.py", line 21, in forward
    x = self.conv1(x)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/module.py", line 1102, in _call_impl
    return forward_call(*input, **kwargs)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/conv.py", line 446, in forward
    return self._conv_forward(input, self.weight, self.bias)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/conv.py", line 443, in _conv_forward
    self.padding, self.dilation, self.groups)
RuntimeError: CUDA error: no kernel image is available for execution on the device
CUDA kernel errors might be asynchronously reported at some other API call,so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1.
Traceback (most recent call last):
  File "/users/zhu/examples/mnist/main.py", line 144, in <module>
    main()
  File "/users/zhu/examples/mnist/main.py", line 135, in main
    train(args, model, device, train_loader, optimizer, epoch)
  File "/users/zhu/examples/mnist/main.py", line 41, in train
    output = model(data)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/module.py", line 1102, in _call_impl
    return forward_call(*input, **kwargs)
  File "/users/zhu/examples/mnist/main.py", line 21, in forward
    x = self.conv1(x)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/module.py", line 1102, in _call_impl
    return forward_call(*input, **kwargs)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/conv.py", line 446, in forward
    return self._conv_forward(input, self.weight, self.bias)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/conv.py", line 443, in _conv_forward
    self.padding, self.dilation, self.groups)
RuntimeError: CUDA error: no kernel image is available for execution on the device
CUDA kernel errors might be asynchronously reported at some other API call,so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1.
srun: error: ault43: task 1: Exited with exit code 1
Traceback (most recent call last):
  File "/users/zhu/examples/mnist/main.py", line 144, in <module>
    main()
  File "/users/zhu/examples/mnist/main.py", line 135, in main
    train(args, model, device, train_loader, optimizer, epoch)
  File "/users/zhu/examples/mnist/main.py", line 41, in train
    output = model(data)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/module.py", line 1102, in _call_impl
    return forward_call(*input, **kwargs)
  File "/users/zhu/examples/mnist/main.py", line 21, in forward
    x = self.conv1(x)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/module.py", line 1102, in _call_impl
    return forward_call(*input, **kwargs)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/conv.py", line 446, in forward
    return self._conv_forward(input, self.weight, self.bias)
  File "/users/zhu/.local/lib/python3.6/site-packages/torch/nn/modules/conv.py", line 443, in _conv_forward
    self.padding, self.dilation, self.groups)
RuntimeError: CUDA error: no kernel image is available for execution on the device
CUDA kernel errors might be asynchronously reported at some other API call,so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1.
srun: error: ault43: task 0: Exited with exit code 1
srun: error: ault44: task 3: Exited with exit code 1
