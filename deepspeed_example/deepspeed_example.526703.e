No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
No ROCm runtime is found, using ROCM_HOME='/opt/rocm'
2024-10-13 20:27:39.459 | INFO     | __main__:train:644 - Creating Experiment Directory
2024-10-13 20:27:39.683 | INFO     | __main__:train:644 - Creating Experiment Directory
2024-10-13 20:27:39.747 | INFO     | __main__:train:666 - Experiment Directory created at experiments/bert_pretrain.2024.10.13.11.27.39.addjtvxg
2024-10-13 20:27:39.749 | INFO     | __main__:train:701 - Creating Datasets
Traceback (most recent call last):
  File "/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/train_bert.py", line 791, in <module>
    fire.Fire(train)
  File "/users/zhu/anaconda3/lib/python3.12/site-packages/fire/core.py", line 141, in Fire
    component_trace = _Fire(component, args, parsed_flag_args, context, name)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/users/zhu/anaconda3/lib/python3.12/site-packages/fire/core.py", line 466, in _Fire
    component, remaining_args = _CallAndUpdateTrace(
                                ^^^^^^^^^^^^^^^^^^^^
  File "/users/zhu/anaconda3/lib/python3.12/site-packages/fire/core.py", line 681, in _CallAndUpdateTrace
    component = fn(*varargs, **kwargs)
                ^^^^^^^^^^^^^^^^^^^^^^
  File "/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/train_bert.py", line 665, in train
    exp_dir = create_experiment_dir(checkpoint_dir, all_arguments)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/train_bert.py", line 460, in create_experiment_dir
    exp_dir.mkdir(exist_ok=False)
  File "/users/zhu/anaconda3/lib/python3.12/pathlib.py", line 1311, in mkdir
    os.mkdir(self, mode)
FileExistsError: [Errno 17] File exists: 'experiments/bert_pretrain.2024.10.13.11.27.39.addjtvxg'
Failed to create '/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/./results/nsys_reports/HelloDeepSpeed_train_bert_nsys_report_ault44.cscs.ch_1037628.nsys-rep': No such file or directory.
srun: error: ault44: task 1: Exited with exit code 1
2024-10-13 20:27:45.521 | INFO     | __main__:train:710 - Dataset Creation Done
2024-10-13 20:27:45.521 | INFO     | __main__:train:714 - Creating Model
2024-10-13 20:27:45.958 | INFO     | __main__:train:723 - Model Creation Done
2024-10-13 20:27:45.958 | INFO     | __main__:train:727 - Creating Optimizer
2024-10-13 20:27:45.959 | INFO     | __main__:train:729 - Optimizer Creation Done
2024-10-13 20:27:45.959 | INFO     | __main__:train:742 - Total number of model parameters: 16,345,177
2024-10-13 20:27:46.370 | INFO     | __main__:train:762 - Loss: 10.7011
2024-10-13 20:27:46.616 | INFO     | __main__:train:762 - Loss: 10.5389
2024-10-13 20:27:46.874 | INFO     | __main__:train:762 - Loss: 10.4017
2024-10-13 20:27:47.140 | INFO     | __main__:train:762 - Loss: 10.2675
2024-10-13 20:27:47.397 | INFO     | __main__:train:762 - Loss: 10.1571
2024-10-13 20:27:47.657 | INFO     | __main__:train:762 - Loss: 10.0281
2024-10-13 20:27:47.919 | INFO     | __main__:train:762 - Loss: 9.9003
2024-10-13 20:27:48.175 | INFO     | __main__:train:762 - Loss: 9.7680
2024-10-13 20:27:48.413 | INFO     | __main__:train:762 - Loss: 9.6470
2024-10-13 20:27:48.666 | INFO     | __main__:train:762 - Loss: 9.5215
2024-10-13 20:27:48.906 | INFO     | __main__:train:762 - Loss: 9.4035
2024-10-13 20:27:49.166 | INFO     | __main__:train:762 - Loss: 9.2870
2024-10-13 20:27:49.408 | INFO     | __main__:train:762 - Loss: 9.1661
2024-10-13 20:27:49.689 | INFO     | __main__:train:762 - Loss: 9.0785
2024-10-13 20:27:49.954 | INFO     | __main__:train:762 - Loss: 8.9824
2024-10-13 20:27:50.210 | INFO     | __main__:train:762 - Loss: 8.8982
2024-10-13 20:27:50.460 | INFO     | __main__:train:762 - Loss: 8.8276
2024-10-13 20:27:50.725 | INFO     | __main__:train:762 - Loss: 8.7616
2024-10-13 20:27:50.962 | INFO     | __main__:train:762 - Loss: 8.6985
2024-10-13 20:27:51.230 | INFO     | __main__:train:762 - Loss: 8.6464
2024-10-13 20:27:51.471 | INFO     | __main__:train:762 - Loss: 8.5886
2024-10-13 20:27:51.718 | INFO     | __main__:train:762 - Loss: 8.5330
2024-10-13 20:27:51.980 | INFO     | __main__:train:762 - Loss: 8.4888
2024-10-13 20:27:52.239 | INFO     | __main__:train:762 - Loss: 8.4446
2024-10-13 20:27:52.541 | INFO     | __main__:train:762 - Loss: 8.3968
2024-10-13 20:27:52.813 | INFO     | __main__:train:762 - Loss: 8.3528
2024-10-13 20:27:53.074 | INFO     | __main__:train:762 - Loss: 8.3176
2024-10-13 20:27:53.332 | INFO     | __main__:train:762 - Loss: 8.2822
2024-10-13 20:27:53.607 | INFO     | __main__:train:762 - Loss: 8.2501
2024-10-13 20:27:53.854 | INFO     | __main__:train:762 - Loss: 8.2238
2024-10-13 20:27:54.117 | INFO     | __main__:train:762 - Loss: 8.1896
2024-10-13 20:27:54.363 | INFO     | __main__:train:762 - Loss: 8.1679
2024-10-13 20:27:54.624 | INFO     | __main__:train:762 - Loss: 8.1400
2024-10-13 20:27:54.885 | INFO     | __main__:train:762 - Loss: 8.1202
2024-10-13 20:27:55.152 | INFO     | __main__:train:762 - Loss: 8.0982
2024-10-13 20:27:55.413 | INFO     | __main__:train:762 - Loss: 8.0758
2024-10-13 20:27:55.671 | INFO     | __main__:train:762 - Loss: 8.0467
2024-10-13 20:27:55.921 | INFO     | __main__:train:762 - Loss: 8.0257
2024-10-13 20:27:56.173 | INFO     | __main__:train:762 - Loss: 8.0054
2024-10-13 20:27:56.419 | INFO     | __main__:train:762 - Loss: 7.9876
2024-10-13 20:27:56.675 | INFO     | __main__:train:762 - Loss: 7.9696
2024-10-13 20:27:56.945 | INFO     | __main__:train:762 - Loss: 7.9517
2024-10-13 20:27:57.274 | INFO     | __main__:train:762 - Loss: 7.9387
2024-10-13 20:27:57.528 | INFO     | __main__:train:762 - Loss: 7.9235
2024-10-13 20:27:57.774 | INFO     | __main__:train:762 - Loss: 7.9053
2024-10-13 20:27:58.039 | INFO     | __main__:train:762 - Loss: 7.8847
2024-10-13 20:27:58.293 | INFO     | __main__:train:762 - Loss: 7.8716
2024-10-13 20:27:58.553 | INFO     | __main__:train:762 - Loss: 7.8592
2024-10-13 20:27:58.798 | INFO     | __main__:train:762 - Loss: 7.8453
2024-10-13 20:27:59.080 | INFO     | __main__:train:762 - Loss: 7.8335
2024-10-13 20:27:59.340 | INFO     | __main__:train:762 - Loss: 7.8203
2024-10-13 20:27:59.598 | INFO     | __main__:train:762 - Loss: 7.8118
2024-10-13 20:27:59.846 | INFO     | __main__:train:762 - Loss: 7.7994
2024-10-13 20:28:00.105 | INFO     | __main__:train:762 - Loss: 7.7860
2024-10-13 20:28:00.358 | INFO     | __main__:train:762 - Loss: 7.7749
2024-10-13 20:28:00.620 | INFO     | __main__:train:762 - Loss: 7.7652
2024-10-13 20:28:00.884 | INFO     | __main__:train:762 - Loss: 7.7582
2024-10-13 20:28:01.178 | INFO     | __main__:train:762 - Loss: 7.7465
2024-10-13 20:28:01.426 | INFO     | __main__:train:762 - Loss: 7.7399
2024-10-13 20:28:01.690 | INFO     | __main__:train:762 - Loss: 7.7299
2024-10-13 20:28:01.936 | INFO     | __main__:train:762 - Loss: 7.7202
2024-10-13 20:28:02.196 | INFO     | __main__:train:762 - Loss: 7.7106
2024-10-13 20:28:02.459 | INFO     | __main__:train:762 - Loss: 7.7011
2024-10-13 20:28:02.704 | INFO     | __main__:train:762 - Loss: 7.6947
2024-10-13 20:28:02.963 | INFO     | __main__:train:762 - Loss: 7.6882
2024-10-13 20:28:03.205 | INFO     | __main__:train:762 - Loss: 7.6823
2024-10-13 20:28:03.460 | INFO     | __main__:train:762 - Loss: 7.6730
2024-10-13 20:28:03.713 | INFO     | __main__:train:762 - Loss: 7.6629
2024-10-13 20:28:03.976 | INFO     | __main__:train:762 - Loss: 7.6536
2024-10-13 20:28:04.227 | INFO     | __main__:train:762 - Loss: 7.6490
2024-10-13 20:28:04.489 | INFO     | __main__:train:762 - Loss: 7.6414
2024-10-13 20:28:04.734 | INFO     | __main__:train:762 - Loss: 7.6333
2024-10-13 20:28:05.003 | INFO     | __main__:train:762 - Loss: 7.6263
2024-10-13 20:28:05.273 | INFO     | __main__:train:762 - Loss: 7.6217
2024-10-13 20:28:05.566 | INFO     | __main__:train:762 - Loss: 7.6118
2024-10-13 20:28:05.852 | INFO     | __main__:train:762 - Loss: 7.6063
2024-10-13 20:28:06.100 | INFO     | __main__:train:762 - Loss: 7.6002
2024-10-13 20:28:06.363 | INFO     | __main__:train:762 - Loss: 7.5953
2024-10-13 20:28:06.634 | INFO     | __main__:train:762 - Loss: 7.5885
2024-10-13 20:28:06.898 | INFO     | __main__:train:762 - Loss: 7.5840
2024-10-13 20:28:07.151 | INFO     | __main__:train:762 - Loss: 7.5776
2024-10-13 20:28:07.415 | INFO     | __main__:train:762 - Loss: 7.5731
2024-10-13 20:28:07.665 | INFO     | __main__:train:762 - Loss: 7.5674
2024-10-13 20:28:07.931 | INFO     | __main__:train:762 - Loss: 7.5619
2024-10-13 20:28:08.174 | INFO     | __main__:train:762 - Loss: 7.5554
2024-10-13 20:28:08.481 | INFO     | __main__:train:762 - Loss: 7.5506
2024-10-13 20:28:08.727 | INFO     | __main__:train:762 - Loss: 7.5461
2024-10-13 20:28:08.987 | INFO     | __main__:train:762 - Loss: 7.5372
2024-10-13 20:28:09.240 | INFO     | __main__:train:762 - Loss: 7.5316
2024-10-13 20:28:09.510 | INFO     | __main__:train:762 - Loss: 7.5253
2024-10-13 20:28:09.752 | INFO     | __main__:train:762 - Loss: 7.5185
2024-10-13 20:28:10.017 | INFO     | __main__:train:762 - Loss: 7.5127
2024-10-13 20:28:10.259 | INFO     | __main__:train:762 - Loss: 7.5092
2024-10-13 20:28:10.506 | INFO     | __main__:train:762 - Loss: 7.5045
2024-10-13 20:28:10.772 | INFO     | __main__:train:762 - Loss: 7.5022
2024-10-13 20:28:11.018 | INFO     | __main__:train:762 - Loss: 7.4958
2024-10-13 20:28:11.285 | INFO     | __main__:train:762 - Loss: 7.4903
2024-10-13 20:28:11.531 | INFO     | __main__:train:762 - Loss: 7.4857
2024-10-13 20:28:11.796 | INFO     | __main__:train:762 - Loss: 7.4802
2024-10-13 20:28:12.091 | INFO     | __main__:train:762 - Loss: 7.4769
2024-10-13 20:28:12.347 | INFO     | __main__:train:771 - Saved model to experiments/bert_pretrain.2024.10.13.11.27.39.addjtvxg/checkpoint.iter_1000.pt
2024-10-13 20:28:12.615 | INFO     | __main__:train:762 - Loss: 7.4724
2024-10-13 20:28:12.877 | INFO     | __main__:train:762 - Loss: 7.4669
2024-10-13 20:28:13.123 | INFO     | __main__:train:762 - Loss: 7.4628
2024-10-13 20:28:13.397 | INFO     | __main__:train:762 - Loss: 7.4570
2024-10-13 20:28:13.651 | INFO     | __main__:train:762 - Loss: 7.4542
2024-10-13 20:28:13.910 | INFO     | __main__:train:762 - Loss: 7.4497
2024-10-13 20:28:14.163 | INFO     | __main__:train:762 - Loss: 7.4477
2024-10-13 20:28:14.439 | INFO     | __main__:train:762 - Loss: 7.4415
2024-10-13 20:28:14.687 | INFO     | __main__:train:762 - Loss: 7.4383
2024-10-13 20:28:14.942 | INFO     | __main__:train:762 - Loss: 7.4330
2024-10-13 20:28:15.190 | INFO     | __main__:train:762 - Loss: 7.4291
2024-10-13 20:28:15.438 | INFO     | __main__:train:762 - Loss: 7.4260
2024-10-13 20:28:15.696 | INFO     | __main__:train:762 - Loss: 7.4212
2024-10-13 20:28:15.986 | INFO     | __main__:train:762 - Loss: 7.4166
2024-10-13 20:28:16.250 | INFO     | __main__:train:762 - Loss: 7.4142
2024-10-13 20:28:16.508 | INFO     | __main__:train:762 - Loss: 7.4103
2024-10-13 20:28:16.766 | INFO     | __main__:train:762 - Loss: 7.4063
2024-10-13 20:28:17.013 | INFO     | __main__:train:762 - Loss: 7.4037
2024-10-13 20:28:17.273 | INFO     | __main__:train:762 - Loss: 7.4016
2024-10-13 20:28:17.526 | INFO     | __main__:train:762 - Loss: 7.3973
2024-10-13 20:28:17.796 | INFO     | __main__:train:762 - Loss: 7.3941
2024-10-13 20:28:18.051 | INFO     | __main__:train:762 - Loss: 7.3925
2024-10-13 20:28:18.312 | INFO     | __main__:train:762 - Loss: 7.3909
2024-10-13 20:28:18.567 | INFO     | __main__:train:762 - Loss: 7.3871
2024-10-13 20:28:18.832 | INFO     | __main__:train:762 - Loss: 7.3837
2024-10-13 20:28:19.119 | INFO     | __main__:train:762 - Loss: 7.3809
2024-10-13 20:28:19.389 | INFO     | __main__:train:762 - Loss: 7.3780
2024-10-13 20:28:19.652 | INFO     | __main__:train:762 - Loss: 7.3753
2024-10-13 20:28:19.948 | INFO     | __main__:train:762 - Loss: 7.3718
2024-10-13 20:28:20.199 | INFO     | __main__:train:762 - Loss: 7.3687
2024-10-13 20:28:20.451 | INFO     | __main__:train:762 - Loss: 7.3633
2024-10-13 20:28:20.704 | INFO     | __main__:train:762 - Loss: 7.3600
2024-10-13 20:28:20.962 | INFO     | __main__:train:762 - Loss: 7.3568
2024-10-13 20:28:21.228 | INFO     | __main__:train:762 - Loss: 7.3527
2024-10-13 20:28:21.481 | INFO     | __main__:train:762 - Loss: 7.3504
2024-10-13 20:28:21.758 | INFO     | __main__:train:762 - Loss: 7.3471
2024-10-13 20:28:22.010 | INFO     | __main__:train:762 - Loss: 7.3431
2024-10-13 20:28:22.277 | INFO     | __main__:train:762 - Loss: 7.3412
2024-10-13 20:28:22.521 | INFO     | __main__:train:762 - Loss: 7.3370
2024-10-13 20:28:22.784 | INFO     | __main__:train:762 - Loss: 7.3347
2024-10-13 20:28:23.031 | INFO     | __main__:train:762 - Loss: 7.3303
2024-10-13 20:28:23.306 | INFO     | __main__:train:762 - Loss: 7.3276
2024-10-13 20:28:23.585 | INFO     | __main__:train:762 - Loss: 7.3236
2024-10-13 20:28:23.842 | INFO     | __main__:train:762 - Loss: 7.3212
2024-10-13 20:28:24.084 | INFO     | __main__:train:762 - Loss: 7.3185
2024-10-13 20:28:24.342 | INFO     | __main__:train:762 - Loss: 7.3156
2024-10-13 20:28:24.584 | INFO     | __main__:train:762 - Loss: 7.3133
2024-10-13 20:28:24.838 | INFO     | __main__:train:762 - Loss: 7.3104
2024-10-13 20:28:25.102 | INFO     | __main__:train:762 - Loss: 7.3074
2024-10-13 20:28:25.359 | INFO     | __main__:train:762 - Loss: 7.3043
2024-10-13 20:28:25.651 | INFO     | __main__:train:762 - Loss: 7.3002
2024-10-13 20:28:25.905 | INFO     | __main__:train:762 - Loss: 7.2962
2024-10-13 20:28:26.182 | INFO     | __main__:train:762 - Loss: 7.2935
2024-10-13 20:28:26.426 | INFO     | __main__:train:762 - Loss: 7.2919
2024-10-13 20:28:26.690 | INFO     | __main__:train:762 - Loss: 7.2883
2024-10-13 20:28:26.950 | INFO     | __main__:train:762 - Loss: 7.2862
2024-10-13 20:28:27.213 | INFO     | __main__:train:762 - Loss: 7.2826
2024-10-13 20:28:27.462 | INFO     | __main__:train:762 - Loss: 7.2801
2024-10-13 20:28:27.722 | INFO     | __main__:train:762 - Loss: 7.2779
2024-10-13 20:28:27.966 | INFO     | __main__:train:762 - Loss: 7.2762
2024-10-13 20:28:28.230 | INFO     | __main__:train:762 - Loss: 7.2740
2024-10-13 20:28:28.482 | INFO     | __main__:train:762 - Loss: 7.2709
2024-10-13 20:28:28.744 | INFO     | __main__:train:762 - Loss: 7.2680
2024-10-13 20:28:28.991 | INFO     | __main__:train:762 - Loss: 7.2657
2024-10-13 20:28:29.244 | INFO     | __main__:train:762 - Loss: 7.2639
2024-10-13 20:28:29.500 | INFO     | __main__:train:762 - Loss: 7.2618
2024-10-13 20:28:29.748 | INFO     | __main__:train:762 - Loss: 7.2596
2024-10-13 20:28:30.009 | INFO     | __main__:train:762 - Loss: 7.2564
2024-10-13 20:28:30.262 | INFO     | __main__:train:762 - Loss: 7.2547
2024-10-13 20:28:30.525 | INFO     | __main__:train:762 - Loss: 7.2523
2024-10-13 20:28:30.785 | INFO     | __main__:train:762 - Loss: 7.2499
2024-10-13 20:28:31.072 | INFO     | __main__:train:762 - Loss: 7.2461
2024-10-13 20:28:31.319 | INFO     | __main__:train:762 - Loss: 7.2440
2024-10-13 20:28:31.575 | INFO     | __main__:train:762 - Loss: 7.2420
2024-10-13 20:28:31.826 | INFO     | __main__:train:762 - Loss: 7.2385
2024-10-13 20:28:32.188 | INFO     | __main__:train:762 - Loss: 7.2362
2024-10-13 20:28:32.454 | INFO     | __main__:train:762 - Loss: 7.2324
2024-10-13 20:28:32.722 | INFO     | __main__:train:762 - Loss: 7.2298
2024-10-13 20:28:32.967 | INFO     | __main__:train:762 - Loss: 7.2276
2024-10-13 20:28:33.232 | INFO     | __main__:train:762 - Loss: 7.2255
2024-10-13 20:28:33.480 | INFO     | __main__:train:762 - Loss: 7.2221
2024-10-13 20:28:33.737 | INFO     | __main__:train:762 - Loss: 7.2179
2024-10-13 20:28:33.992 | INFO     | __main__:train:762 - Loss: 7.2157
2024-10-13 20:28:34.247 | INFO     | __main__:train:762 - Loss: 7.2138
2024-10-13 20:28:34.498 | INFO     | __main__:train:762 - Loss: 7.2098
2024-10-13 20:28:34.743 | INFO     | __main__:train:762 - Loss: 7.2080
2024-10-13 20:28:35.004 | INFO     | __main__:train:762 - Loss: 7.2050
2024-10-13 20:28:35.252 | INFO     | __main__:train:762 - Loss: 7.2033
2024-10-13 20:28:35.509 | INFO     | __main__:train:762 - Loss: 7.2014
2024-10-13 20:28:35.758 | INFO     | __main__:train:762 - Loss: 7.1995
2024-10-13 20:28:36.025 | INFO     | __main__:train:762 - Loss: 7.1983
2024-10-13 20:28:36.282 | INFO     | __main__:train:762 - Loss: 7.1971
2024-10-13 20:28:36.539 | INFO     | __main__:train:762 - Loss: 7.1949
2024-10-13 20:28:36.806 | INFO     | __main__:train:762 - Loss: 7.1932
2024-10-13 20:28:37.070 | INFO     | __main__:train:762 - Loss: 7.1916
2024-10-13 20:28:37.316 | INFO     | __main__:train:762 - Loss: 7.1899
2024-10-13 20:28:37.580 | INFO     | __main__:train:762 - Loss: 7.1888
2024-10-13 20:28:37.835 | INFO     | __main__:train:762 - Loss: 7.1870
2024-10-13 20:28:38.097 | INFO     | __main__:train:762 - Loss: 7.1850
2024-10-13 20:28:38.436 | INFO     | __main__:train:762 - Loss: 7.1827
2024-10-13 20:28:38.676 | INFO     | __main__:train:771 - Saved model to experiments/bert_pretrain.2024.10.13.11.27.39.addjtvxg/checkpoint.iter_2000.pt
2024-10-13 20:28:38.950 | INFO     | __main__:train:762 - Loss: 7.1808
2024-10-13 20:28:39.211 | INFO     | __main__:train:762 - Loss: 7.1798
2024-10-13 20:28:39.459 | INFO     | __main__:train:762 - Loss: 7.1788
2024-10-13 20:28:39.707 | INFO     | __main__:train:762 - Loss: 7.1772
2024-10-13 20:28:39.976 | INFO     | __main__:train:762 - Loss: 7.1751
2024-10-13 20:28:40.232 | INFO     | __main__:train:762 - Loss: 7.1739
2024-10-13 20:28:40.495 | INFO     | __main__:train:762 - Loss: 7.1729
2024-10-13 20:28:40.740 | INFO     | __main__:train:762 - Loss: 7.1702
2024-10-13 20:28:41.008 | INFO     | __main__:train:762 - Loss: 7.1688
2024-10-13 20:28:41.259 | INFO     | __main__:train:762 - Loss: 7.1665
2024-10-13 20:28:41.515 | INFO     | __main__:train:762 - Loss: 7.1646
2024-10-13 20:28:41.775 | INFO     | __main__:train:762 - Loss: 7.1626
2024-10-13 20:28:42.034 | INFO     | __main__:train:762 - Loss: 7.1615
2024-10-13 20:28:42.287 | INFO     | __main__:train:762 - Loss: 7.1593
2024-10-13 20:28:42.548 | INFO     | __main__:train:762 - Loss: 7.1578
2024-10-13 20:28:42.801 | INFO     | __main__:train:762 - Loss: 7.1554
2024-10-13 20:28:43.049 | INFO     | __main__:train:762 - Loss: 7.1531
2024-10-13 20:28:43.305 | INFO     | __main__:train:762 - Loss: 7.1515
2024-10-13 20:28:43.552 | INFO     | __main__:train:762 - Loss: 7.1501
2024-10-13 20:28:43.808 | INFO     | __main__:train:762 - Loss: 7.1484
2024-10-13 20:28:44.050 | INFO     | __main__:train:762 - Loss: 7.1469
2024-10-13 20:28:44.312 | INFO     | __main__:train:762 - Loss: 7.1455
2024-10-13 20:28:44.568 | INFO     | __main__:train:762 - Loss: 7.1442
2024-10-13 20:28:44.841 | INFO     | __main__:train:762 - Loss: 7.1423
2024-10-13 20:28:45.091 | INFO     | __main__:train:762 - Loss: 7.1407
2024-10-13 20:28:45.419 | INFO     | __main__:train:762 - Loss: 7.1391
2024-10-13 20:28:45.670 | INFO     | __main__:train:762 - Loss: 7.1378
2024-10-13 20:28:45.944 | INFO     | __main__:train:762 - Loss: 7.1366
2024-10-13 20:28:46.198 | INFO     | __main__:train:762 - Loss: 7.1352
2024-10-13 20:28:46.464 | INFO     | __main__:train:762 - Loss: 7.1337
2024-10-13 20:28:46.721 | INFO     | __main__:train:762 - Loss: 7.1318
2024-10-13 20:28:46.981 | INFO     | __main__:train:762 - Loss: 7.1307
2024-10-13 20:28:47.228 | INFO     | __main__:train:762 - Loss: 7.1293
2024-10-13 20:28:47.470 | INFO     | __main__:train:762 - Loss: 7.1268
srun: Job step aborted: Waiting up to 32 seconds for job step to finish.
srun: got SIGCONT
slurmstepd: error: *** STEP 526703.1 ON ault43 CANCELLED AT 2024-10-13T20:28:47 ***
slurmstepd: error: *** JOB 526703 ON ault43 CANCELLED AT 2024-10-13T20:28:47 ***
srun: forcing job termination
