Traceback (most recent call last):
  File "/users/zhu/examples/siamese_network/main.py", line 9, in <module>
    import torchvision
  File "/users/zhu/.local/lib/python3.8/site-packages/torchvision/__init__.py", line 10, in <module>
    from torchvision import _meta_registrations, datasets, io, models, ops, transforms, utils  # usort:skip
  File "/users/zhu/.local/lib/python3.8/site-packages/torchvision/_meta_registrations.py", line 164, in <module>
    def meta_nms(dets, scores, iou_threshold):
  File "/users/zhu/.local/lib/python3.8/site-packages/torch/library.py", line 654, in register
    use_lib._register_fake(op_name, func, _stacklevel=stacklevel + 1)
  File "/users/zhu/.local/lib/python3.8/site-packages/torch/library.py", line 154, in _register_fake
    handle = entry.abstract_impl.register(func_to_register, source)
  File "/users/zhu/.local/lib/python3.8/site-packages/torch/_library/abstract_impl.py", line 31, in register
    if torch._C._dispatch_has_kernel_for_dispatch_key(self.qualname, "Meta"):
RuntimeError: operator torchvision::nms does not exist
Traceback (most recent call last):
  File "/users/zhu/examples/siamese_network/main.py", line 9, in <module>
    import torchvision
  File "/users/zhu/.local/lib/python3.8/site-packages/torchvision/__init__.py", line 10, in <module>
    from torchvision import _meta_registrations, datasets, io, models, ops, transforms, utils  # usort:skip
  File "/users/zhu/.local/lib/python3.8/site-packages/torchvision/_meta_registrations.py", line 164, in <module>
    def meta_nms(dets, scores, iou_threshold):
  File "/users/zhu/.local/lib/python3.8/site-packages/torch/library.py", line 654, in register
    use_lib._register_fake(op_name, func, _stacklevel=stacklevel + 1)
  File "/users/zhu/.local/lib/python3.8/site-packages/torch/library.py", line 154, in _register_fake
    handle = entry.abstract_impl.register(func_to_register, source)
  File "/users/zhu/.local/lib/python3.8/site-packages/torch/_library/abstract_impl.py", line 31, in register
    if torch._C._dispatch_has_kernel_for_dispatch_key(self.qualname, "Meta"):
RuntimeError: operator torchvision::nms does not exist
srun: error: ault44: tasks 2-3: Exited with exit code 1
Traceback (most recent call last):
  File "/users/zhu/examples/siamese_network/main.py", line 9, in <module>
    import torchvision
  File "/users/zhu/.local/lib/python3.8/site-packages/torchvision/__init__.py", line 10, in <module>
    from torchvision import _meta_registrations, datasets, io, models, ops, transforms, utils  # usort:skip
  File "/users/zhu/.local/lib/python3.8/site-packages/torchvision/_meta_registrations.py", line 164, in <module>
    def meta_nms(dets, scores, iou_threshold):
  File "/users/zhu/.local/lib/python3.8/site-packages/torch/library.py", line 654, in register
    use_lib._register_fake(op_name, func, _stacklevel=stacklevel + 1)
  File "/users/zhu/.local/lib/python3.8/site-packages/torch/library.py", line 154, in _register_fake
    handle = entry.abstract_impl.register(func_to_register, source)
  File "/users/zhu/.local/lib/python3.8/site-packages/torch/_library/abstract_impl.py", line 31, in register
    if torch._C._dispatch_has_kernel_for_dispatch_key(self.qualname, "Meta"):
RuntimeError: operator torchvision::nms does not exist
Traceback (most recent call last):
  File "/users/zhu/examples/siamese_network/main.py", line 9, in <module>
    import torchvision
  File "/users/zhu/.local/lib/python3.8/site-packages/torchvision/__init__.py", line 10, in <module>
    from torchvision import _meta_registrations, datasets, io, models, ops, transforms, utils  # usort:skip
  File "/users/zhu/.local/lib/python3.8/site-packages/torchvision/_meta_registrations.py", line 164, in <module>
    def meta_nms(dets, scores, iou_threshold):
  File "/users/zhu/.local/lib/python3.8/site-packages/torch/library.py", line 654, in register
    use_lib._register_fake(op_name, func, _stacklevel=stacklevel + 1)
  File "/users/zhu/.local/lib/python3.8/site-packages/torch/library.py", line 154, in _register_fake
    handle = entry.abstract_impl.register(func_to_register, source)
  File "/users/zhu/.local/lib/python3.8/site-packages/torch/_library/abstract_impl.py", line 31, in register
    if torch._C._dispatch_has_kernel_for_dispatch_key(self.qualname, "Meta"):
RuntimeError: operator torchvision::nms does not exist
srun: error: ault43: tasks 0-1: Exited with exit code 1
