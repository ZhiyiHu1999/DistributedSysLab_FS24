seq = "24788886666"  # 你的 seq 值
channel_id = "0"  # 你的 channel_id 值

# 使用 zfill 补全 channel_id 到两位数
channel_id_padded = channel_id.zfill(2)

# 串联 seq 和补全后的 channel_id
result = seq + channel_id_padded

print(result)  # 输出结果: 2401