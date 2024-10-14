
Due to MODULEPATH changes, the following have been reloaded:
  1) libxml2/2.9.10

No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
2024-10-14 14:31:28.763 | INFO     | __main__:log_dist:54 - [Rank 0] Creating Experiment Directory
2024-10-14 14:31:29.495 | INFO     | __main__:log_dist:54 - [Rank 0] Experiment Directory created at /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed/bert_pretrain.2024.10.14.5.31.29.addjtvxg
2024-10-14 14:31:29.498 | INFO     | __main__:log_dist:54 - [Rank 0] Creating Datasets
2024-10-14 14:31:35.264 | INFO     | __main__:log_dist:54 - [Rank 0] Dataset Creation Done
2024-10-14 14:31:35.264 | INFO     | __main__:log_dist:54 - [Rank 0] Creating Model
2024-10-14 14:31:35.656 | INFO     | __main__:log_dist:54 - [Rank 0] Model Creation Done
2024-10-14 14:31:35.657 | INFO     | __main__:log_dist:54 - [Rank 0] Creating DeepSpeed engine
Using /users/zhu/.cache/torch_extensions/py312_cu118 as PyTorch extensions root...
Using /users/zhu/.cache/torch_extensions/py312_cu118 as PyTorch extensions root...
Emitting ninja build file /users/zhu/.cache/torch_extensions/py312_cu118/cpu_adam/build.ninja...
Building extension module cpu_adam...
Allowing ninja to set a default number of workers... (overridable by setting the environment variable MAX_JOBS=N)
Loading extension module cpu_adam...
Loading extension module cpu_adam...
2024-10-14 14:31:39.074 | INFO     | __main__:log_dist:54 - [Rank 0] DeepSpeed engine created
2024-10-14 14:31:39.074 | INFO     | __main__:log_dist:54 - [Rank 0] Total number of model parameters: 16,345,177
2024-10-14 14:31:40.874 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 10.7125
2024-10-14 14:31:41.919 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 10.5469
2024-10-14 14:31:43.056 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 10.4083
2024-10-14 14:31:44.086 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 10.2734
2024-10-14 14:31:45.106 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 10.1625
2024-10-14 14:31:46.139 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 10.0323
2024-10-14 14:31:47.128 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 9.9045
2024-10-14 14:31:48.215 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 9.7727
2024-10-14 14:31:49.303 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 9.6514
2024-10-14 14:31:50.316 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 9.5256
2024-10-14 14:31:51.546 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 9.4065
2024-10-14 14:31:52.509 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 9.2901
2024-10-14 14:31:53.585 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 9.1690
2024-10-14 14:31:54.677 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 9.0815
2024-10-14 14:31:55.668 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.9850
2024-10-14 14:31:56.826 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.9006
2024-10-14 14:31:57.779 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.8298
2024-10-14 14:31:58.864 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.7635
2024-10-14 14:31:59.844 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.7003
2024-10-14 14:32:00.867 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.6481
2024-10-14 14:32:01.970 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.5902
2024-10-14 14:32:02.967 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.5345
2024-10-14 14:32:04.061 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.4902
2024-10-14 14:32:05.085 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.4461
2024-10-14 14:32:06.091 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.3984
2024-10-14 14:32:07.161 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.3546
2024-10-14 14:32:08.155 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.3194
2024-10-14 14:32:09.289 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.2838
2024-10-14 14:32:10.436 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.2514
2024-10-14 14:32:11.448 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.2250
2024-10-14 14:32:12.559 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.1908
2024-10-14 14:32:13.627 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.1688
2024-10-14 14:32:14.583 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.1409
2024-10-14 14:32:15.741 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.1210
2024-10-14 14:32:16.749 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.0989
2024-10-14 14:32:17.897 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.0764
2024-10-14 14:32:18.886 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.0473
2024-10-14 14:32:19.873 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.0263
2024-10-14 14:32:20.965 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 8.0059
2024-10-14 14:32:21.926 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.9882
2024-10-14 14:32:23.067 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.9702
2024-10-14 14:32:24.210 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.9523
2024-10-14 14:32:25.252 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.9392
2024-10-14 14:32:26.297 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.9240
2024-10-14 14:32:27.286 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.9057
2024-10-14 14:32:28.310 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.8850
2024-10-14 14:32:29.333 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.8719
2024-10-14 14:32:30.516 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.8595
2024-10-14 14:32:31.669 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.8458
2024-10-14 14:32:32.669 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.8339
2024-10-14 14:32:33.673 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.8206
2024-10-14 14:32:34.747 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.8121
2024-10-14 14:32:35.781 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.7998
2024-10-14 14:32:36.957 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.7863
2024-10-14 14:32:37.946 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.7752
2024-10-14 14:32:38.966 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.7655
2024-10-14 14:32:40.112 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.7586
2024-10-14 14:32:41.107 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.7469
2024-10-14 14:32:42.189 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.7404
2024-10-14 14:32:43.163 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.7302
2024-10-14 14:32:44.112 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.7206
2024-10-14 14:32:45.228 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.7111
2024-10-14 14:32:46.345 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.7015
2024-10-14 14:32:47.481 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6951
2024-10-14 14:32:48.482 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6886
2024-10-14 14:32:49.492 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6827
2024-10-14 14:32:50.580 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6734
2024-10-14 14:32:51.610 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6633
2024-10-14 14:32:52.639 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6541
2024-10-14 14:32:53.724 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6494
2024-10-14 14:32:54.703 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6418
2024-10-14 14:32:55.843 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6336
2024-10-14 14:32:56.837 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6267
2024-10-14 14:32:57.883 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6220
2024-10-14 14:32:58.992 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6122
2024-10-14 14:32:59.972 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6066
2024-10-14 14:33:01.081 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.6005
2024-10-14 14:33:02.112 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5956
2024-10-14 14:33:03.301 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5888
2024-10-14 14:33:04.486 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5843
2024-10-14 14:33:05.517 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5780
2024-10-14 14:33:06.761 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5734
2024-10-14 14:33:07.807 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5677
2024-10-14 14:33:08.802 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5622
2024-10-14 14:33:09.963 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5556
2024-10-14 14:33:10.930 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5509
2024-10-14 14:33:11.941 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5462
2024-10-14 14:33:13.005 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5374
2024-10-14 14:33:14.066 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5317
2024-10-14 14:33:15.204 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5256
2024-10-14 14:33:16.168 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5187
2024-10-14 14:33:17.170 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5129
2024-10-14 14:33:18.270 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5095
2024-10-14 14:33:19.300 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5047
2024-10-14 14:33:20.509 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.5023
2024-10-14 14:33:21.494 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4959
2024-10-14 14:33:22.458 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4904
2024-10-14 14:33:23.614 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4858
2024-10-14 14:33:24.661 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4803
2024-10-14 14:33:25.760 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4771
2024-10-14 14:33:26.198 | INFO     | __main__:log_dist:54 - [Rank 0] Saved model to /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed/bert_pretrain.2024.10.14.5.31.29.addjtvxg
2024-10-14 14:33:27.193 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4725
2024-10-14 14:33:28.232 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4670
2024-10-14 14:33:29.411 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4629
2024-10-14 14:33:30.414 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4571
2024-10-14 14:33:31.502 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4543
2024-10-14 14:33:32.606 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4498
2024-10-14 14:33:33.554 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4478
2024-10-14 14:33:34.737 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4416
2024-10-14 14:33:35.769 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4385
2024-10-14 14:33:36.927 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4332
2024-10-14 14:33:37.977 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4292
2024-10-14 14:33:38.965 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4262
2024-10-14 14:33:40.218 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4214
2024-10-14 14:33:41.187 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4167
2024-10-14 14:33:42.228 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4144
2024-10-14 14:33:43.446 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4106
2024-10-14 14:33:44.439 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4065
2024-10-14 14:33:45.579 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4039
2024-10-14 14:33:46.567 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.4018
2024-10-14 14:33:47.517 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3975
2024-10-14 14:33:48.598 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3942
2024-10-14 14:33:49.621 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3926
2024-10-14 14:33:50.803 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3910
2024-10-14 14:33:51.826 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3873
2024-10-14 14:33:52.907 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3839
2024-10-14 14:33:54.242 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3810
2024-10-14 14:33:55.294 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3781
2024-10-14 14:33:56.358 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3754
2024-10-14 14:33:57.452 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3720
2024-10-14 14:33:58.469 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3689
2024-10-14 14:33:59.493 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3635
2024-10-14 14:34:00.481 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3602
2024-10-14 14:34:01.505 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3570
2024-10-14 14:34:02.549 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3529
2024-10-14 14:34:03.610 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3506
2024-10-14 14:34:04.834 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3472
2024-10-14 14:34:05.813 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3433
2024-10-14 14:34:06.799 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3413
2024-10-14 14:34:07.938 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3372
2024-10-14 14:34:09.067 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3349
2024-10-14 14:34:10.249 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3305
2024-10-14 14:34:11.396 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3277
2024-10-14 14:34:12.377 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3237
2024-10-14 14:34:13.580 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3213
2024-10-14 14:34:14.594 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3186
2024-10-14 14:34:15.834 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3157
2024-10-14 14:34:16.865 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3135
2024-10-14 14:34:17.860 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3105
2024-10-14 14:34:19.065 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3076
2024-10-14 14:34:20.115 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3044
2024-10-14 14:34:21.151 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.3003
2024-10-14 14:34:22.318 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2962
2024-10-14 14:34:23.361 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2936
2024-10-14 14:34:24.529 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2920
2024-10-14 14:34:25.616 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2884
2024-10-14 14:34:26.612 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2862
2024-10-14 14:34:27.729 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2827
2024-10-14 14:34:28.871 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2801
2024-10-14 14:34:30.027 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2779
2024-10-14 14:34:31.003 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2762
2024-10-14 14:34:31.942 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2740
2024-10-14 14:34:33.033 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2709
2024-10-14 14:34:34.050 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2681
2024-10-14 14:34:35.194 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2657
2024-10-14 14:34:36.160 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2640
2024-10-14 14:34:37.166 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2619
2024-10-14 14:34:38.283 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2596
2024-10-14 14:34:39.306 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2565
2024-10-14 14:34:40.504 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2548
2024-10-14 14:34:41.583 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2524
2024-10-14 14:34:42.551 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2500
2024-10-14 14:34:43.663 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2462
2024-10-14 14:34:44.822 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2441
2024-10-14 14:34:45.887 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2422
2024-10-14 14:34:46.981 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2386
2024-10-14 14:34:47.985 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2363
2024-10-14 14:34:49.065 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2325
2024-10-14 14:34:50.100 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2299
2024-10-14 14:34:51.069 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2277
2024-10-14 14:34:52.175 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2256
2024-10-14 14:34:53.255 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2222
2024-10-14 14:34:54.448 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2179
2024-10-14 14:34:55.530 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2157
2024-10-14 14:34:56.593 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2139
2024-10-14 14:34:57.649 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2099
2024-10-14 14:34:58.636 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2081
2024-10-14 14:34:59.660 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2052
2024-10-14 14:35:00.665 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2034
2024-10-14 14:35:01.817 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.2015
2024-10-14 14:35:03.016 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1996
2024-10-14 14:35:04.023 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1984
2024-10-14 14:35:05.049 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1972
2024-10-14 14:35:06.196 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1950
2024-10-14 14:35:07.207 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1933
2024-10-14 14:35:08.304 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1917
2024-10-14 14:35:09.301 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1900
2024-10-14 14:35:10.342 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1889
2024-10-14 14:35:11.596 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1871
2024-10-14 14:35:12.626 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1851
2024-10-14 14:35:13.834 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1828
2024-10-14 14:35:14.016 | INFO     | __main__:log_dist:54 - [Rank 0] Saved model to /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed/bert_pretrain.2024.10.14.5.31.29.addjtvxg
2024-10-14 14:35:14.998 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1809
2024-10-14 14:35:16.030 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1799
2024-10-14 14:35:17.183 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1789
2024-10-14 14:35:18.157 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1772
2024-10-14 14:35:19.539 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1752
2024-10-14 14:35:20.510 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1739
2024-10-14 14:35:21.544 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1729
2024-10-14 14:35:22.714 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1702
2024-10-14 14:35:23.713 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1689
2024-10-14 14:35:24.792 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1666
2024-10-14 14:35:25.811 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1646
2024-10-14 14:35:26.876 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1626
2024-10-14 14:35:28.039 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1615
2024-10-14 14:35:29.053 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1593
2024-10-14 14:35:30.045 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1578
2024-10-14 14:35:31.198 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1554
2024-10-14 14:35:32.227 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1532
2024-10-14 14:35:33.294 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1515
2024-10-14 14:35:34.307 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1501
2024-10-14 14:35:35.349 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1484
2024-10-14 14:35:36.568 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1470
2024-10-14 14:35:37.601 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1455
2024-10-14 14:35:38.783 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1443
2024-10-14 14:35:39.736 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1423
2024-10-14 14:35:40.798 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1407
2024-10-14 14:35:42.002 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1392
2024-10-14 14:35:43.050 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1379
2024-10-14 14:35:44.161 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1367
2024-10-14 14:35:45.218 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1352
2024-10-14 14:35:46.178 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1338
2024-10-14 14:35:47.272 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1319
2024-10-14 14:35:48.315 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1308
2024-10-14 14:35:49.333 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1293
2024-10-14 14:35:50.421 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1269
2024-10-14 14:35:51.398 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1255
2024-10-14 14:35:52.670 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1231
2024-10-14 14:35:53.625 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1221
2024-10-14 14:35:54.604 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1200
2024-10-14 14:35:55.684 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1177
2024-10-14 14:35:56.744 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1163
2024-10-14 14:35:57.864 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1144
2024-10-14 14:35:58.827 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1129
2024-10-14 14:35:59.811 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1120
2024-10-14 14:36:00.961 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1103
2024-10-14 14:36:01.937 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1092
2024-10-14 14:36:03.084 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1082
2024-10-14 14:36:04.069 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1065
2024-10-14 14:36:05.123 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1046
2024-10-14 14:36:06.301 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1035
2024-10-14 14:36:07.303 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1019
2024-10-14 14:36:08.457 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1006
2024-10-14 14:36:09.616 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.1001
2024-10-14 14:36:10.575 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0983
2024-10-14 14:36:11.729 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0967
2024-10-14 14:36:12.739 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0947
2024-10-14 14:36:13.756 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0930
2024-10-14 14:36:14.759 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0918
2024-10-14 14:36:15.725 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0907
2024-10-14 14:36:16.822 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0890
2024-10-14 14:36:17.862 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0880
2024-10-14 14:36:18.838 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0869
2024-10-14 14:36:19.905 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0851
2024-10-14 14:36:20.896 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0829
2024-10-14 14:36:21.971 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0815
2024-10-14 14:36:22.937 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0806
2024-10-14 14:36:23.871 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0797
2024-10-14 14:36:24.961 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0789
2024-10-14 14:36:26.153 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0775
2024-10-14 14:36:27.251 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0758
2024-10-14 14:36:28.274 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0747
2024-10-14 14:36:29.219 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0735
2024-10-14 14:36:30.358 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0719
2024-10-14 14:36:31.384 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0710
2024-10-14 14:36:32.428 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0701
2024-10-14 14:36:33.462 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0689
2024-10-14 14:36:34.461 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0679
2024-10-14 14:36:35.546 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0667
2024-10-14 14:36:36.528 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0656
2024-10-14 14:36:37.512 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0647
2024-10-14 14:36:38.557 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0643
2024-10-14 14:36:39.532 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0630
2024-10-14 14:36:40.755 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0616
2024-10-14 14:36:41.888 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0607
2024-10-14 14:36:42.965 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0598
2024-10-14 14:36:44.145 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0584
2024-10-14 14:36:45.148 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0570
2024-10-14 14:36:46.271 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0550
2024-10-14 14:36:47.231 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0543
2024-10-14 14:36:48.269 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0534
2024-10-14 14:36:49.357 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0529
2024-10-14 14:36:50.389 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0511
2024-10-14 14:36:51.467 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0504
2024-10-14 14:36:52.450 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0501
2024-10-14 14:36:53.517 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0487
2024-10-14 14:36:54.627 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0473
2024-10-14 14:36:55.622 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0463
2024-10-14 14:36:56.766 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0446
2024-10-14 14:36:57.852 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0433
2024-10-14 14:36:58.923 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0420
2024-10-14 14:36:59.993 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0404
2024-10-14 14:37:00.198 | INFO     | __main__:log_dist:54 - [Rank 0] Saved model to /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed/bert_pretrain.2024.10.14.5.31.29.addjtvxg
2024-10-14 14:37:01.127 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0396
2024-10-14 14:37:02.136 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0385
2024-10-14 14:37:03.252 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0370
2024-10-14 14:37:04.310 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0364
2024-10-14 14:37:05.405 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0352
2024-10-14 14:37:06.371 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0340
2024-10-14 14:37:07.367 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0334
2024-10-14 14:37:08.530 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0321
2024-10-14 14:37:09.572 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0310
2024-10-14 14:37:10.666 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0299
2024-10-14 14:37:11.861 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0290
2024-10-14 14:37:12.856 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0275
2024-10-14 14:37:14.055 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0268
2024-10-14 14:37:15.181 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0260
2024-10-14 14:37:16.447 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0247
2024-10-14 14:37:17.390 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0240
2024-10-14 14:37:18.414 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0232
2024-10-14 14:37:19.522 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0220
2024-10-14 14:37:20.487 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0199
2024-10-14 14:37:21.477 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0184
2024-10-14 14:37:22.664 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0175
2024-10-14 14:37:23.708 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0166
2024-10-14 14:37:24.852 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0158
2024-10-14 14:37:25.856 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0154
2024-10-14 14:37:26.953 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0142
2024-10-14 14:37:28.037 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0135
2024-10-14 14:37:29.072 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0120
2024-10-14 14:37:30.213 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0109
2024-10-14 14:37:31.212 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0094
2024-10-14 14:37:32.333 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0087
2024-10-14 14:37:33.487 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0079
2024-10-14 14:37:34.523 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0067
2024-10-14 14:37:35.606 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0055
2024-10-14 14:37:36.619 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0048
2024-10-14 14:37:37.628 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0041
2024-10-14 14:37:38.718 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0028
2024-10-14 14:37:39.704 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0020
2024-10-14 14:37:40.794 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0015
2024-10-14 14:37:41.995 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 7.0011
2024-10-14 14:37:42.983 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9993
2024-10-14 14:37:44.068 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9992
2024-10-14 14:37:45.044 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9978
2024-10-14 14:37:46.068 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9971
2024-10-14 14:37:47.229 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9961
2024-10-14 14:37:48.245 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9946
2024-10-14 14:37:49.508 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9935
2024-10-14 14:37:50.475 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9922
2024-10-14 14:37:51.447 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9911
2024-10-14 14:37:52.514 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9897
2024-10-14 14:37:53.513 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9892
2024-10-14 14:37:54.687 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9878
2024-10-14 14:37:55.686 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9868
2024-10-14 14:37:56.769 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9866
2024-10-14 14:37:57.848 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9852
2024-10-14 14:37:58.885 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9835
2024-10-14 14:38:00.007 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9826
2024-10-14 14:38:01.017 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9819
2024-10-14 14:38:02.046 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9812
2024-10-14 14:38:03.106 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9805
2024-10-14 14:38:04.114 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9797
2024-10-14 14:38:05.081 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9783
2024-10-14 14:38:06.363 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9772
2024-10-14 14:38:07.333 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9758
2024-10-14 14:38:08.445 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9751
2024-10-14 14:38:09.464 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9742
2024-10-14 14:38:10.447 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9734
2024-10-14 14:38:11.603 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9719
2024-10-14 14:38:12.566 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9707
2024-10-14 14:38:13.797 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9699
2024-10-14 14:38:14.788 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9689
2024-10-14 14:38:15.803 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9677
2024-10-14 14:38:16.876 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9668
2024-10-14 14:38:17.850 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9661
2024-10-14 14:38:18.922 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9657
2024-10-14 14:38:19.916 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9645
2024-10-14 14:38:20.939 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9638
2024-10-14 14:38:22.123 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9631
2024-10-14 14:38:23.263 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9617
2024-10-14 14:38:24.320 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9610
2024-10-14 14:38:25.311 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9603
2024-10-14 14:38:26.374 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9597
2024-10-14 14:38:27.630 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9589
2024-10-14 14:38:28.639 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9582
2024-10-14 14:38:29.599 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9577
2024-10-14 14:38:30.745 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9567
2024-10-14 14:38:31.748 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9554
2024-10-14 14:38:32.855 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9550
2024-10-14 14:38:33.926 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9538
2024-10-14 14:38:34.938 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9523
2024-10-14 14:38:36.101 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9516
2024-10-14 14:38:37.059 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9501
2024-10-14 14:38:38.165 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9494
2024-10-14 14:38:39.414 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9486
2024-10-14 14:38:40.376 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9476
2024-10-14 14:38:41.602 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9471
2024-10-14 14:38:42.695 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9462
2024-10-14 14:38:43.820 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9450
2024-10-14 14:38:44.828 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9444
2024-10-14 14:38:45.931 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9429
2024-10-14 14:38:46.997 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9419
2024-10-14 14:38:47.214 | INFO     | __main__:log_dist:54 - [Rank 0] Saved model to /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed/bert_pretrain.2024.10.14.5.31.29.addjtvxg
2024-10-14 14:38:48.250 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9403
2024-10-14 14:38:49.297 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9390
2024-10-14 14:38:50.555 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9384
2024-10-14 14:38:51.547 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9374
2024-10-14 14:38:52.709 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9362
2024-10-14 14:38:53.749 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9354
2024-10-14 14:38:54.749 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9344
2024-10-14 14:38:55.858 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9335
2024-10-14 14:38:57.055 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9327
2024-10-14 14:38:58.286 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9323
2024-10-14 14:38:59.251 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9318
2024-10-14 14:39:00.243 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9307
2024-10-14 14:39:01.345 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9293
2024-10-14 14:39:02.345 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9287
2024-10-14 14:39:03.494 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9281
2024-10-14 14:39:04.506 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9271
2024-10-14 14:39:05.487 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9264
2024-10-14 14:39:06.558 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9256
2024-10-14 14:39:07.615 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9244
2024-10-14 14:39:08.825 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9237
2024-10-14 14:39:09.854 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9229
2024-10-14 14:39:10.844 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9218
2024-10-14 14:39:11.962 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9213
2024-10-14 14:39:12.944 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9206
2024-10-14 14:39:14.131 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9198
2024-10-14 14:39:15.298 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9190
2024-10-14 14:39:16.351 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9174
2024-10-14 14:39:17.525 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9166
2024-10-14 14:39:18.666 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9158
2024-10-14 14:39:19.733 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9148
2024-10-14 14:39:20.869 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9136
2024-10-14 14:39:21.870 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9125
2024-10-14 14:39:23.032 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9119
2024-10-14 14:39:24.052 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9114
2024-10-14 14:39:25.061 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9106
2024-10-14 14:39:26.174 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9099
2024-10-14 14:39:27.176 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9093
2024-10-14 14:39:28.411 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9083
2024-10-14 14:39:29.407 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9080
2024-10-14 14:39:30.542 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9070
2024-10-14 14:39:31.693 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9060
2024-10-14 14:39:32.673 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9055
2024-10-14 14:39:33.733 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9043
2024-10-14 14:39:34.738 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9034
2024-10-14 14:39:35.701 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9029
2024-10-14 14:39:36.843 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9019
2024-10-14 14:39:37.828 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9007
2024-10-14 14:39:38.857 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.9003
2024-10-14 14:39:40.064 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8998
2024-10-14 14:39:41.018 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8994
2024-10-14 14:39:42.154 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8988
2024-10-14 14:39:43.252 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8978
2024-10-14 14:39:44.274 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8968
2024-10-14 14:39:45.412 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8962
2024-10-14 14:39:46.431 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8953
2024-10-14 14:39:47.709 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8946
2024-10-14 14:39:48.721 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8939
2024-10-14 14:39:49.743 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8933
2024-10-14 14:39:50.881 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8927
2024-10-14 14:39:51.928 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8920
2024-10-14 14:39:53.117 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8910
2024-10-14 14:39:54.119 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8901
2024-10-14 14:39:55.133 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8898
2024-10-14 14:39:56.234 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8890
2024-10-14 14:39:57.220 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8882
2024-10-14 14:39:58.344 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8873
2024-10-14 14:39:59.475 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8865
2024-10-14 14:40:00.453 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8855
2024-10-14 14:40:01.595 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8846
2024-10-14 14:40:02.548 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8838
2024-10-14 14:40:03.576 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8829
2024-10-14 14:40:04.833 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8819
2024-10-14 14:40:05.908 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8810
2024-10-14 14:40:07.008 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8806
2024-10-14 14:40:08.006 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8800
2024-10-14 14:40:09.033 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8792
2024-10-14 14:40:10.231 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8782
2024-10-14 14:40:11.210 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8773
2024-10-14 14:40:12.361 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8770
2024-10-14 14:40:13.460 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8766
2024-10-14 14:40:14.440 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8762
2024-10-14 14:40:15.492 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8755
2024-10-14 14:40:16.486 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8746
2024-10-14 14:40:17.585 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8737
2024-10-14 14:40:18.696 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8727
2024-10-14 14:40:19.729 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8723
2024-10-14 14:40:20.797 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8716
2024-10-14 14:40:21.952 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8709
2024-10-14 14:40:22.928 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8706
2024-10-14 14:40:24.075 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8697
2024-10-14 14:40:25.156 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8692
2024-10-14 14:40:26.245 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8686
2024-10-14 14:40:27.240 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8681
2024-10-14 14:40:28.288 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8669
2024-10-14 14:40:29.438 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8665
2024-10-14 14:40:30.451 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8658
2024-10-14 14:40:31.555 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8644
2024-10-14 14:40:32.593 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8635
2024-10-14 14:40:33.552 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8627
2024-10-14 14:40:34.648 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8623
2024-10-14 14:40:34.845 | INFO     | __main__:log_dist:54 - [Rank 0] Saved model to /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed/bert_pretrain.2024.10.14.5.31.29.addjtvxg
2024-10-14 14:40:35.863 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8615
2024-10-14 14:40:36.992 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8610
2024-10-14 14:40:38.224 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8607
2024-10-14 14:40:39.276 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8600
2024-10-14 14:40:40.426 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8589
2024-10-14 14:40:41.434 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8581
2024-10-14 14:40:42.498 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8574
2024-10-14 14:40:43.692 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8564
2024-10-14 14:40:44.674 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8553
2024-10-14 14:40:45.928 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8548
2024-10-14 14:40:47.067 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8543
2024-10-14 14:40:48.087 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8534
2024-10-14 14:40:49.208 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8526
2024-10-14 14:40:50.237 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8518
2024-10-14 14:40:51.341 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8507
2024-10-14 14:40:52.347 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8498
2024-10-14 14:40:53.367 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8492
2024-10-14 14:40:54.555 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8485
2024-10-14 14:40:55.710 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8477
2024-10-14 14:40:56.867 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8470
2024-10-14 14:40:57.876 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8467
2024-10-14 14:40:58.910 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8461
2024-10-14 14:41:00.022 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8450
2024-10-14 14:41:00.977 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8445
2024-10-14 14:41:02.038 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8439
2024-10-14 14:41:03.099 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8429
2024-10-14 14:41:04.075 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8422
2024-10-14 14:41:05.261 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8416
2024-10-14 14:41:06.308 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8412
2024-10-14 14:41:07.330 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8405
2024-10-14 14:41:08.470 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8393
2024-10-14 14:41:09.535 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8387
2024-10-14 14:41:10.757 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8381
2024-10-14 14:41:11.847 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8376
2024-10-14 14:41:13.035 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8372
2024-10-14 14:41:14.160 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8367
2024-10-14 14:41:15.190 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8358
2024-10-14 14:41:16.309 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8351
2024-10-14 14:41:17.335 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8347
2024-10-14 14:41:18.325 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8339
2024-10-14 14:41:19.499 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8332
2024-10-14 14:41:20.534 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8323
2024-10-14 14:41:21.606 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8318
2024-10-14 14:41:22.667 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8315
2024-10-14 14:41:23.699 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8312
2024-10-14 14:41:24.821 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8306
2024-10-14 14:41:25.801 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8305
2024-10-14 14:41:26.862 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8300
2024-10-14 14:41:27.963 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8292
2024-10-14 14:41:29.015 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8284
2024-10-14 14:41:30.437 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8278
2024-10-14 14:41:31.458 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8270
2024-10-14 14:41:32.416 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8264
2024-10-14 14:41:33.584 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8257
2024-10-14 14:41:34.570 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8251
2024-10-14 14:41:35.684 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8247
2024-10-14 14:41:36.693 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8244
2024-10-14 14:41:37.729 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8236
2024-10-14 14:41:38.812 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8228
2024-10-14 14:41:39.781 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8221
2024-10-14 14:41:40.870 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8215
2024-10-14 14:41:41.926 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8211
2024-10-14 14:41:42.903 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8204
2024-10-14 14:41:44.059 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8197
2024-10-14 14:41:45.047 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8189
2024-10-14 14:41:46.388 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8184
2024-10-14 14:41:47.483 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8179
2024-10-14 14:41:48.509 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8175
2024-10-14 14:41:49.667 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8170
2024-10-14 14:41:50.684 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8168
2024-10-14 14:41:51.638 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8161
2024-10-14 14:41:52.719 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8153
2024-10-14 14:41:53.742 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8146
2024-10-14 14:41:54.912 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8138
2024-10-14 14:41:56.003 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8135
2024-10-14 14:41:57.080 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8127
2024-10-14 14:41:58.269 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8124
2024-10-14 14:41:59.248 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8118
2024-10-14 14:42:00.424 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8108
2024-10-14 14:42:01.473 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8104
2024-10-14 14:42:02.447 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8098
2024-10-14 14:42:03.681 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8091
2024-10-14 14:42:04.764 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8084
2024-10-14 14:42:05.873 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8078
2024-10-14 14:42:06.909 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8073
2024-10-14 14:42:07.892 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8066
2024-10-14 14:42:09.134 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8061
2024-10-14 14:42:10.109 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8058
2024-10-14 14:42:11.201 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8050
2024-10-14 14:42:12.289 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8046
2024-10-14 14:42:13.373 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8038
2024-10-14 14:42:14.507 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8032
2024-10-14 14:42:15.645 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8028
2024-10-14 14:42:16.679 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8026
2024-10-14 14:42:17.899 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8021
2024-10-14 14:42:18.907 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8015
2024-10-14 14:42:20.078 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8007
2024-10-14 14:42:21.202 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.8001
2024-10-14 14:42:22.266 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7999
2024-10-14 14:42:23.433 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7989
2024-10-14 14:42:23.613 | INFO     | __main__:log_dist:54 - [Rank 0] Saved model to /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed/bert_pretrain.2024.10.14.5.31.29.addjtvxg
2024-10-14 14:42:24.685 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7984
2024-10-14 14:42:25.838 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7976
2024-10-14 14:42:26.921 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7970
2024-10-14 14:42:27.952 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7964
2024-10-14 14:42:29.113 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7958
2024-10-14 14:42:30.066 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7952
2024-10-14 14:42:31.193 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7949
2024-10-14 14:42:32.179 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7940
2024-10-14 14:42:33.220 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7934
2024-10-14 14:42:34.440 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7925
2024-10-14 14:42:35.490 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7920
2024-10-14 14:42:36.482 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7914
2024-10-14 14:42:37.798 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7907
2024-10-14 14:42:38.797 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7902
2024-10-14 14:42:39.899 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7896
2024-10-14 14:42:40.904 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7892
2024-10-14 14:42:41.928 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7885
2024-10-14 14:42:43.090 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7875
2024-10-14 14:42:44.050 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7870
2024-10-14 14:42:45.226 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7866
2024-10-14 14:42:46.351 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7861
2024-10-14 14:42:47.357 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7857
2024-10-14 14:42:48.512 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7849
2024-10-14 14:42:49.513 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7845
2024-10-14 14:42:50.667 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7839
2024-10-14 14:42:51.684 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7836
2024-10-14 14:42:52.674 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7830
2024-10-14 14:42:53.740 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7823
2024-10-14 14:42:54.949 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7819
2024-10-14 14:42:56.030 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7814
2024-10-14 14:42:57.102 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7810
2024-10-14 14:42:58.124 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7803
2024-10-14 14:42:59.325 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7796
2024-10-14 14:43:00.334 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7787
2024-10-14 14:43:01.467 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7780
2024-10-14 14:43:02.717 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7776
2024-10-14 14:43:03.770 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7772
2024-10-14 14:43:04.899 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7768
2024-10-14 14:43:05.927 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7761
2024-10-14 14:43:06.929 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7756
2024-10-14 14:43:08.077 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7751
2024-10-14 14:43:09.060 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7745
2024-10-14 14:43:10.169 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7745
2024-10-14 14:43:11.174 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7738
2024-10-14 14:43:12.425 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7731
2024-10-14 14:43:13.583 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7727
2024-10-14 14:43:14.617 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7723
2024-10-14 14:43:15.706 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7719
2024-10-14 14:43:16.774 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7715
2024-10-14 14:43:17.872 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7705
2024-10-14 14:43:19.068 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7699
2024-10-14 14:43:20.125 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7695
2024-10-14 14:43:21.181 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7689
2024-10-14 14:43:22.226 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7683
2024-10-14 14:43:23.186 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7679
2024-10-14 14:43:24.313 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7673
2024-10-14 14:43:25.317 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7664
2024-10-14 14:43:26.309 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7658
2024-10-14 14:43:27.466 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7649
2024-10-14 14:43:28.590 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7646
2024-10-14 14:43:29.826 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7641
2024-10-14 14:43:30.776 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7634
2024-10-14 14:43:31.722 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7630
2024-10-14 14:43:32.877 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7623
2024-10-14 14:43:33.900 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7617
2024-10-14 14:43:35.093 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7613
2024-10-14 14:43:36.085 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7611
2024-10-14 14:43:37.079 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7606
2024-10-14 14:43:38.267 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7600
2024-10-14 14:43:39.262 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7596
2024-10-14 14:43:40.331 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7590
2024-10-14 14:43:41.322 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7586
2024-10-14 14:43:42.270 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7582
2024-10-14 14:43:43.390 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7578
2024-10-14 14:43:44.409 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7571
2024-10-14 14:43:45.581 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7564
2024-10-14 14:43:46.706 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7558
2024-10-14 14:43:47.785 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7550
2024-10-14 14:43:48.813 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7545
2024-10-14 14:43:49.833 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7540
2024-10-14 14:43:50.832 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7537
2024-10-14 14:43:51.952 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7533
2024-10-14 14:43:52.973 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7525
2024-10-14 14:43:54.075 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7522
2024-10-14 14:43:55.093 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7515
2024-10-14 14:43:56.126 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7510
2024-10-14 14:43:57.258 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7505
2024-10-14 14:43:58.220 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7496
2024-10-14 14:43:59.292 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7492
2024-10-14 14:44:00.306 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7488
2024-10-14 14:44:01.339 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7482
2024-10-14 14:44:02.627 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7475
2024-10-14 14:44:03.718 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7470
2024-10-14 14:44:04.795 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7466
2024-10-14 14:44:05.910 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7460
2024-10-14 14:44:06.957 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7457
2024-10-14 14:44:08.054 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7447
2024-10-14 14:44:09.023 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7444
2024-10-14 14:44:10.011 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7436
2024-10-14 14:44:11.148 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7432
2024-10-14 14:44:11.332 | INFO     | __main__:log_dist:54 - [Rank 0] Saved model to /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed/bert_pretrain.2024.10.14.5.31.29.addjtvxg
2024-10-14 14:44:12.367 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7426
2024-10-14 14:44:13.530 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7422
2024-10-14 14:44:14.585 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7415
2024-10-14 14:44:15.681 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7411
2024-10-14 14:44:16.779 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7405
2024-10-14 14:44:17.841 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7398
2024-10-14 14:44:18.981 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7392
2024-10-14 14:44:20.182 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7389
2024-10-14 14:44:21.199 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7384
2024-10-14 14:44:22.357 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7379
2024-10-14 14:44:23.357 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7375
2024-10-14 14:44:24.425 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7371
2024-10-14 14:44:25.417 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7367
2024-10-14 14:44:26.424 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7362
2024-10-14 14:44:27.562 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7357
2024-10-14 14:44:28.552 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7351
2024-10-14 14:44:29.545 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7348
2024-10-14 14:44:30.590 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7341
2024-10-14 14:44:31.567 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7338
2024-10-14 14:44:32.699 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7330
2024-10-14 14:44:33.733 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7325
2024-10-14 14:44:34.761 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7322
2024-10-14 14:44:36.083 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7319
2024-10-14 14:44:37.052 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7312
2024-10-14 14:44:38.159 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7307
2024-10-14 14:44:39.189 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7302
2024-10-14 14:44:40.153 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7297
2024-10-14 14:44:41.319 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7295
2024-10-14 14:44:42.261 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7288
2024-10-14 14:44:43.450 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7282
2024-10-14 14:44:44.461 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7278
2024-10-14 14:44:45.471 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7272
2024-10-14 14:44:46.558 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7268
2024-10-14 14:44:47.628 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7265
2024-10-14 14:44:48.699 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7258
2024-10-14 14:44:49.675 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7252
2024-10-14 14:44:50.702 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7250
2024-10-14 14:44:51.852 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7244
2024-10-14 14:44:53.059 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7243
2024-10-14 14:44:54.083 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7237
2024-10-14 14:44:55.245 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7230
2024-10-14 14:44:56.226 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7224
2024-10-14 14:44:57.304 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7222
2024-10-14 14:44:58.347 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7218
2024-10-14 14:44:59.393 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7214
2024-10-14 14:45:00.571 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7210
2024-10-14 14:45:01.593 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7204
2024-10-14 14:45:02.887 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7196
2024-10-14 14:45:04.013 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7188
2024-10-14 14:45:04.979 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7185
2024-10-14 14:45:06.225 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7181
2024-10-14 14:45:07.247 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7173
2024-10-14 14:45:08.436 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7168
2024-10-14 14:45:09.451 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7163
2024-10-14 14:45:10.602 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7154
2024-10-14 14:45:11.734 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7150
2024-10-14 14:45:12.709 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7144
2024-10-14 14:45:13.737 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7138
2024-10-14 14:45:14.774 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7134
2024-10-14 14:45:15.833 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7132
2024-10-14 14:45:17.032 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7128
2024-10-14 14:45:18.139 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7123
2024-10-14 14:45:19.205 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7115
2024-10-14 14:45:20.409 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7110
2024-10-14 14:45:21.424 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7107
2024-10-14 14:45:22.642 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7102
2024-10-14 14:45:23.725 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7095
2024-10-14 14:45:24.705 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7089
2024-10-14 14:45:25.930 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7086
2024-10-14 14:45:27.082 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7084
2024-10-14 14:45:28.396 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7076
2024-10-14 14:45:29.394 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7066
2024-10-14 14:45:30.378 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7060
2024-10-14 14:45:31.502 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7053
2024-10-14 14:45:32.485 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7045
2024-10-14 14:45:33.581 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7040
2024-10-14 14:45:34.790 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7035
2024-10-14 14:45:35.788 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7032
2024-10-14 14:45:36.982 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7027
2024-10-14 14:45:38.012 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7020
2024-10-14 14:45:39.069 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7016
2024-10-14 14:45:40.176 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7012
2024-10-14 14:45:41.194 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7008
2024-10-14 14:45:42.316 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.7002
2024-10-14 14:45:43.324 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6998
2024-10-14 14:45:44.640 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6995
2024-10-14 14:45:45.747 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6990
2024-10-14 14:45:46.776 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6984
2024-10-14 14:45:47.808 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6980
2024-10-14 14:45:48.856 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6979
2024-10-14 14:45:49.904 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6972
2024-10-14 14:45:51.046 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6967
2024-10-14 14:45:52.004 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6963
2024-10-14 14:45:53.164 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6960
2024-10-14 14:45:54.161 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6954
2024-10-14 14:45:55.153 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6950
2024-10-14 14:45:56.353 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6945
2024-10-14 14:45:57.344 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6938
2024-10-14 14:45:58.385 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6934
2024-10-14 14:45:59.450 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6930
2024-10-14 14:45:59.629 | INFO     | __main__:log_dist:54 - [Rank 0] Saved model to /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed/bert_pretrain.2024.10.14.5.31.29.addjtvxg
2024-10-14 14:46:00.565 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6926
2024-10-14 14:46:01.848 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6922
2024-10-14 14:46:02.848 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6918
2024-10-14 14:46:03.849 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6914
2024-10-14 14:46:05.101 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6905
2024-10-14 14:46:06.130 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6898
2024-10-14 14:46:07.294 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6894
2024-10-14 14:46:08.251 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6889
2024-10-14 14:46:09.236 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6887
2024-10-14 14:46:10.358 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6882
2024-10-14 14:46:11.349 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6875
2024-10-14 14:46:12.522 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6872
2024-10-14 14:46:13.516 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6870
2024-10-14 14:46:14.518 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6864
2024-10-14 14:46:15.676 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6861
2024-10-14 14:46:16.676 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6852
2024-10-14 14:46:17.808 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6849
2024-10-14 14:46:19.007 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6842
2024-10-14 14:46:20.153 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6837
2024-10-14 14:46:21.373 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6832
2024-10-14 14:46:22.352 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6827
2024-10-14 14:46:23.382 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6822
2024-10-14 14:46:24.507 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6819
2024-10-14 14:46:25.560 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6814
2024-10-14 14:46:26.744 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6812
2024-10-14 14:46:27.794 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6809
2024-10-14 14:46:28.822 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6806
2024-10-14 14:46:30.034 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6797
2024-10-14 14:46:30.989 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6794
2024-10-14 14:46:32.201 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6792
2024-10-14 14:46:33.195 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6788
2024-10-14 14:46:34.153 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6781
2024-10-14 14:46:35.576 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6777
2024-10-14 14:46:36.663 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6773
2024-10-14 14:46:37.828 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6770
2024-10-14 14:46:38.855 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6766
2024-10-14 14:46:39.860 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6761
2024-10-14 14:46:40.986 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6758
2024-10-14 14:46:41.964 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6755
2024-10-14 14:46:43.114 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6751
2024-10-14 14:46:44.210 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6744
2024-10-14 14:46:45.221 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6742
2024-10-14 14:46:46.394 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6738
2024-10-14 14:46:47.423 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6735
2024-10-14 14:46:48.480 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6728
2024-10-14 14:46:49.643 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6725
2024-10-14 14:46:50.798 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6722
2024-10-14 14:46:51.973 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6718
2024-10-14 14:46:53.188 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6714
2024-10-14 14:46:54.205 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6709
2024-10-14 14:46:55.381 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6706
2024-10-14 14:46:56.395 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6704
2024-10-14 14:46:57.643 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6700
2024-10-14 14:46:58.613 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6694
2024-10-14 14:46:59.620 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6690
2024-10-14 14:47:00.752 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6686
2024-10-14 14:47:01.745 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6684
2024-10-14 14:47:02.900 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6679
2024-10-14 14:47:03.925 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6676
2024-10-14 14:47:04.928 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6672
2024-10-14 14:47:06.111 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6668
2024-10-14 14:47:07.147 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6661
2024-10-14 14:47:08.186 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6657
2024-10-14 14:47:09.312 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6653
2024-10-14 14:47:10.518 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6648
2024-10-14 14:47:11.677 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6644
2024-10-14 14:47:12.740 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6643
2024-10-14 14:47:13.768 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6639
2024-10-14 14:47:14.949 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6633
2024-10-14 14:47:16.049 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6627
2024-10-14 14:47:17.218 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6624
2024-10-14 14:47:18.225 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6620
2024-10-14 14:47:19.233 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6618
2024-10-14 14:47:20.388 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6614
2024-10-14 14:47:21.476 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6610
2024-10-14 14:47:22.718 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6604
2024-10-14 14:47:23.698 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6600
2024-10-14 14:47:24.723 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6597
2024-10-14 14:47:25.852 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6592
2024-10-14 14:47:26.847 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6590
2024-10-14 14:47:28.203 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6589
2024-10-14 14:47:29.307 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6584
2024-10-14 14:47:30.364 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6580
2024-10-14 14:47:31.576 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6577
2024-10-14 14:47:32.562 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6573
2024-10-14 14:47:33.592 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6568
2024-10-14 14:47:34.788 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6564
2024-10-14 14:47:35.806 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6561
2024-10-14 14:47:36.966 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6558
2024-10-14 14:47:38.020 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6553
2024-10-14 14:47:38.992 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6547
2024-10-14 14:47:40.193 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6543
2024-10-14 14:47:41.177 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6540
2024-10-14 14:47:42.347 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6535
2024-10-14 14:47:43.393 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6531
2024-10-14 14:47:44.526 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6526
2024-10-14 14:47:45.675 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6521
2024-10-14 14:47:46.703 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6517
2024-10-14 14:47:47.805 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6514
2024-10-14 14:47:48.773 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6510
2024-10-14 14:47:48.960 | INFO     | __main__:log_dist:54 - [Rank 0] Saved model to /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed/bert_pretrain.2024.10.14.5.31.29.addjtvxg
2024-10-14 14:47:49.947 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6504
2024-10-14 14:47:51.102 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6499
2024-10-14 14:47:52.110 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6495
2024-10-14 14:47:53.252 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6489
2024-10-14 14:47:54.385 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6487
2024-10-14 14:47:55.417 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6485
2024-10-14 14:47:56.518 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6481
2024-10-14 14:47:57.481 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6477
2024-10-14 14:47:58.512 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6474
2024-10-14 14:47:59.679 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6471
2024-10-14 14:48:00.690 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6466
2024-10-14 14:48:01.932 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6459
2024-10-14 14:48:02.941 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6455
2024-10-14 14:48:03.921 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6452
2024-10-14 14:48:05.092 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6448
2024-10-14 14:48:06.104 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6445
2024-10-14 14:48:07.263 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6438
2024-10-14 14:48:08.398 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6437
2024-10-14 14:48:09.414 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6432
2024-10-14 14:48:10.586 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6428
2024-10-14 14:48:11.627 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6423
2024-10-14 14:48:12.758 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6419
2024-10-14 14:48:13.777 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6415
2024-10-14 14:48:14.823 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6413
2024-10-14 14:48:16.019 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6410
2024-10-14 14:48:17.103 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6406
2024-10-14 14:48:18.241 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6398
2024-10-14 14:48:19.536 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6395
2024-10-14 14:48:20.570 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6391
2024-10-14 14:48:21.699 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6386
2024-10-14 14:48:22.716 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6384
2024-10-14 14:48:23.803 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6379
2024-10-14 14:48:25.009 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6374
2024-10-14 14:48:25.988 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6368
2024-10-14 14:48:27.154 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6363
2024-10-14 14:48:28.131 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6359
2024-10-14 14:48:29.116 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6358
2024-10-14 14:48:30.270 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6352
2024-10-14 14:48:31.261 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6348
2024-10-14 14:48:32.477 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6346
2024-10-14 14:48:33.506 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6341
2024-10-14 14:48:34.583 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6339
2024-10-14 14:48:35.776 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6335
2024-10-14 14:48:37.003 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6332
2024-10-14 14:48:38.225 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6329
2024-10-14 14:48:39.308 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6323
2024-10-14 14:48:40.301 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6320
2024-10-14 14:48:41.463 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6316
2024-10-14 14:48:42.460 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6311
2024-10-14 14:48:43.498 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6307
2024-10-14 14:48:44.646 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6303
2024-10-14 14:48:45.608 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6300
2024-10-14 14:48:46.762 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6295
2024-10-14 14:48:47.735 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6291
2024-10-14 14:48:48.721 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6287
2024-10-14 14:48:49.874 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6285
2024-10-14 14:48:50.890 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6281
2024-10-14 14:48:52.107 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6276
2024-10-14 14:48:53.200 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6272
2024-10-14 14:48:54.241 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6268
2024-10-14 14:48:55.382 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6263
2024-10-14 14:48:56.404 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6257
2024-10-14 14:48:57.536 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6252
2024-10-14 14:48:58.572 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6248
2024-10-14 14:48:59.542 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6247
2024-10-14 14:49:00.773 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6244
2024-10-14 14:49:01.762 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6241
2024-10-14 14:49:02.784 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6236
2024-10-14 14:49:04.002 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6231
2024-10-14 14:49:05.061 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6227
2024-10-14 14:49:06.319 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6222
2024-10-14 14:49:07.270 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6215
2024-10-14 14:49:08.234 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6211
2024-10-14 14:49:09.516 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6208
2024-10-14 14:49:10.699 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6204
2024-10-14 14:49:11.854 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6200
2024-10-14 14:49:12.879 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6194
2024-10-14 14:49:13.915 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6187
2024-10-14 14:49:15.087 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6184
2024-10-14 14:49:16.133 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6183
2024-10-14 14:49:17.312 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6180
2024-10-14 14:49:18.364 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6177
2024-10-14 14:49:19.481 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6171
2024-10-14 14:49:20.660 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6168
2024-10-14 14:49:21.690 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6164
2024-10-14 14:49:22.802 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6160
2024-10-14 14:49:23.898 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6158
2024-10-14 14:49:24.981 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6153
2024-10-14 14:49:26.154 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6151
2024-10-14 14:49:27.234 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6147
2024-10-14 14:49:28.480 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6142
2024-10-14 14:49:29.635 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6138
2024-10-14 14:49:30.668 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6134
2024-10-14 14:49:31.848 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6129
2024-10-14 14:49:32.878 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6126
2024-10-14 14:49:33.917 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6122
2024-10-14 14:49:35.118 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6118
2024-10-14 14:49:36.111 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6115
2024-10-14 14:49:37.331 | INFO     | __main__:log_dist:54 - [Rank 0] Loss: 6.6111
[rank0]:[W1014 14:49:41.088533445 ProcessGroupNCCL.cpp:1168] Warning: WARNING: process group has NOT been destroyed before we destruct ProcessGroupNCCL. On normal program exit, the application should call destroy_process_group to ensure that any pending NCCL operations have finished in this process. In rare cases this process can exit before this point and block the progress of another member of the process group. This constraint has always been present,  but this warning has only been added since PyTorch 2.4 (function operator())
[rank1]:[W1014 14:49:41.044460053 ProcessGroupNCCL.cpp:1168] Warning: WARNING: process group has NOT been destroyed before we destruct ProcessGroupNCCL. On normal program exit, the application should call destroy_process_group to ensure that any pending NCCL operations have finished in this process. In rare cases this process can exit before this point and block the progress of another member of the process group. This constraint has always been present,  but this warning has only been added since PyTorch 2.4 (function operator())
Processing 80472594 events: [1%                                                ]Processing 80472594 events: [2%                                                ]Processing 80472594 events: [3%                                                ]Processing 80472594 events: [4%                                                ]Processing 80472594 events: [5%                                                ]Processing 80472594 events: [=6%                                               ]Processing 80472594 events: [=7%                                               ]Processing 80472594 events: [==8%                                              ]Processing 80472594 events: [==9%                                              ]Processing 80472594 events: [==10%                                             ]Processing 80472594 events: [==11%                                             ]Processing 80472594 events: [===12%                                            ]Processing 80472594 events: [===13%                                            ]Processing 80472594 events: [====14%                                           ]Processing 80472594 events: [====15%                                           ]Processing 80472594 events: [=====16%                                          ]Processing 80472594 events: [=====17%                                          ]Processing 80472594 events: [======18%                                         ]Processing 80472594 events: [======19%                                         ]Processing 80472594 events: [=======20%                                        ]Processing 80472594 events: [=======21%                                        ]Processing 80472594 events: [========22%                                       ]Processing 80472594 events: [========23%                                       ]Processing 80472594 events: [=========24%                                      ]Processing 80472594 events: [=========25%                                      ]Processing 80472594 events: [==========26%                                     ]Processing 80472594 events: [==========27%                                     ]Processing 80472594 events: [===========28%                                    ]Processing 80472594 events: [===========29%                                    ]Processing 80472594 events: [============30%                                   ]Processing 80472594 events: [============31%                                   ]Processing 80472594 events: [=============32%                                  ]Processing 80472594 events: [=============33%                                  ]Processing 80472594 events: [==============34%                                 ]Processing 80472594 events: [==============35%                                 ]Processing 80472594 events: [===============36%                                ]Processing 80472594 events: [===============37%                                ]Processing 80472594 events: [================38%                               ]Processing 80472594 events: [================39%                               ]Processing 80472594 events: [=================40%                              ]Processing 80472594 events: [=================41%                              ]Processing 80472594 events: [==================42%                             ]Processing 80472594 events: [==================43%                             ]Processing 80472594 events: [===================44%                            ]Processing 80472594 events: [===================45%                            ]Processing 80472594 events: [====================46%                           ]Processing 80472594 events: [====================47%                           ]Processing 80472594 events: [=====================48%                          ]Processing 80472594 events: [=====================49%                          ]Processing 80472594 events: [======================50%                         ]Processing 80472594 events: [======================51%                         ]Processing 80472594 events: [=======================52%                        ]Processing 80472594 events: [=======================53%                        ]Processing 80472594 events: [========================54%                       ]Processing 80472594 events: [========================55%                       ]Processing 80472594 events: [=========================56%                      ]Processing 80472594 events: [=========================57%                      ]Processing 80472594 events: [==========================58%                     ]Processing 80472594 events: [==========================59%                     ]Processing 80472594 events: [===========================60%                    ]Processing 80472594 events: [===========================61%                    ]Processing 80472594 events: [============================62%                   ]Processing 80472594 events: [============================63%                   ]Processing 80472594 events: [=============================64%                  ]Processing 80472594 events: [=============================65%                  ]Processing 80472594 events: [==============================66%                 ]Processing 80472594 events: [==============================67%                 ]Processing 80472594 events: [===============================68%                ]Processing 80472594 events: [===============================69%                ]Processing 80472594 events: [================================70%               ]Processing 80472594 events: [================================71%               ]Processing 80472594 events: [=================================72%              ]Processing 80472594 events: [=================================73%              ]Processing 80472594 events: [==================================74%             ]Processing 80472594 events: [==================================75%             ]Processing 80472594 events: [===================================76%            ]Processing 80472594 events: [===================================77%            ]Processing 80472594 events: [====================================78%           ]Processing 80472594 events: [====================================79%           ]Processing 80472594 events: [=====================================80%          ]Processing 80472594 events: [=====================================81%          ]Processing 80472594 events: [======================================82%         ]Processing 80472594 events: [======================================83%         ]Processing 80472594 events: [=======================================84%        ]Processing 80472594 events: [=======================================85%        ]Processing 80472594 events: [========================================86%       ]Processing 80472594 events: [========================================87%       ]Processing 80472594 events: [=========================================88%      ]Processing 80472594 events: [=========================================89%      ]Processing 80472594 events: [==========================================90%     ]Processing 80472594 events: [==========================================91%     ]Processing 80472594 events: [===========================================92%    ]Processing 80472594 events: [===========================================93%    ]Processing 80472594 events: [============================================94%   ]Processing 80472594 events: [============================================95%   ]Processing 80472594 events: [=============================================96%  ]Processing 80472594 events: [=============================================97%  ]Processing 80472594 events: [==============================================98% ]Processing 80472594 events: [==============================================99% ]Processing 80472594 events: [==============================================100%]
Processing 53155273 events: [1%                                                ]Processing 53155273 events: [2%                                                ]Processing 53155273 events: [3%                                                ]Processing 53155273 events: [4%                                                ]Processing 53155273 events: [5%                                                ]Processing 53155273 events: [=6%                                               ]Processing 53155273 events: [=7%                                               ]Processing 53155273 events: [==8%                                              ]Processing 53155273 events: [==9%                                              ]Processing 53155273 events: [==10%                                             ]Processing 53155273 events: [==11%                                             ]Processing 53155273 events: [===12%                                            ]Processing 53155273 events: [===13%                                            ]Processing 53155273 events: [====14%                                           ]Processing 53155273 events: [====15%                                           ]Processing 53155273 events: [=====16%                                          ]Processing 53155273 events: [=====17%                                          ]Processing 53155273 events: [======18%                                         ]Processing 53155273 events: [======19%                                         ]Processing 53155273 events: [=======20%                                        ]Processing 53155273 events: [=======21%                                        ]Processing 53155273 events: [========22%                                       ]Processing 53155273 events: [========23%                                       ]Processing 53155273 events: [=========24%                                      ]Processing 53155273 events: [=========25%                                      ]Processing 53155273 events: [==========26%                                     ]Processing 53155273 events: [==========27%                                     ]Processing 53155273 events: [===========28%                                    ]Processing 53155273 events: [===========29%                                    ]Processing 53155273 events: [============30%                                   ]Processing 53155273 events: [============31%                                   ]Processing 53155273 events: [=============32%                                  ]Processing 53155273 events: [=============33%                                  ]Processing 53155273 events: [==============34%                                 ]Processing 53155273 events: [==============35%                                 ]Processing 53155273 events: [===============36%                                ]Processing 53155273 events: [===============37%                                ]Processing 53155273 events: [================38%                               ]Processing 53155273 events: [================39%                               ]Processing 53155273 events: [=================40%                              ]Processing 53155273 events: [=================41%                              ]Processing 53155273 events: [==================42%                             ]Processing 53155273 events: [==================43%                             ]Processing 53155273 events: [===================44%                            ]Processing 53155273 events: [===================45%                            ]Processing 53155273 events: [====================46%                           ]Processing 53155273 events: [====================47%                           ]Processing 53155273 events: [=====================48%                          ]Processing 53155273 events: [=====================49%                          ]Processing 53155273 events: [======================50%                         ]Processing 53155273 events: [======================51%                         ]Processing 53155273 events: [=======================52%                        ]Processing 53155273 events: [=======================53%                        ]Processing 53155273 events: [========================54%                       ]Processing 53155273 events: [========================55%                       ]Processing 53155273 events: [=========================56%                      ]Processing 53155273 events: [=========================57%                      ]Processing 53155273 events: [==========================58%                     ]Processing 53155273 events: [==========================59%                     ]Processing 53155273 events: [===========================60%                    ]Processing 53155273 events: [===========================61%                    ]Processing 53155273 events: [============================62%                   ]Processing 53155273 events: [============================63%                   ]Processing 53155273 events: [=============================64%                  ]Processing 53155273 events: [=============================65%                  ]Processing 53155273 events: [==============================66%                 ]Processing 53155273 events: [==============================67%                 ]Processing 53155273 events: [===============================68%                ]Processing 53155273 events: [===============================69%                ]Processing 53155273 events: [================================70%               ]Processing 53155273 events: [================================71%               ]Processing 53155273 events: [=================================72%              ]Processing 53155273 events: [=================================73%              ]Processing 53155273 events: [==================================74%             ]Processing 53155273 events: [==================================75%             ]Processing 53155273 events: [===================================76%            ]Processing 53155273 events: [===================================77%            ]Processing 53155273 events: [====================================78%           ]Processing 53155273 events: [====================================79%           ]Processing 53155273 events: [=====================================80%          ]Processing 53155273 events: [=====================================81%          ]Processing 53155273 events: [======================================82%         ]Processing 53155273 events: [======================================83%         ]Processing 53155273 events: [=======================================84%        ]Processing 53155273 events: [=======================================85%        ]Processing 53155273 events: [========================================86%       ]Processing 53155273 events: [========================================87%       ]Processing 53155273 events: [=========================================88%      ]Processing 53155273 events: [=========================================89%      ]Processing 53155273 events: [==========================================90%     ]Processing 53155273 events: [==========================================91%     ]Processing 53155273 events: [===========================================92%    ]Processing 53155273 events: [===========================================93%    ]Processing 53155273 events: [============================================94%   ]Processing 53155273 events: [============================================95%   ]Processing 53155273 events: [=============================================96%  ]Processing 53155273 events: [=============================================97%  ]Processing 53155273 events: [==============================================98% ]Processing 53155273 events: [==============================================99% ]Processing 53155273 events: [==============================================100%]
