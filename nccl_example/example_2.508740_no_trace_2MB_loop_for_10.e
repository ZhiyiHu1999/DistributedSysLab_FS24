tee: /log.txt: Permission denied

real	0m22.397s
user	0m0.011s
sys	0m0.012s

time 命令将输出三个值：
    real：从命令开始到结束的总时间（即实际的运行时间）
    user：在用户态执行代码所花的时间
    sys：在内核态执行代码所花的时间
你可以根据 real 值来确定 srun 命令的总运行时间。
