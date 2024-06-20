import numpy as np
# 加载GR4J其他参数
other_para = np.loadtxt('others.txt')
area = other_para[0]  # 流域面积(km2)
upperTankRatio = other_para[1]  # 产流水库初始填充率 S0/x1
lowerTankRatio = other_para[2]  # 汇流水库初始填充率 R0/x3

# 加载数据文件
data = np.loadtxt('inputData.txt')
P = data[:, 0]  # 第二列: 日降雨量(mm)
E = data[:, 1]  # 第三列: 蒸散发量(mm)
Qobs = data[:, 2]  # 第四列: 流域出口观测流量(ML/day)

Qobs_mm = Qobs * 86.4 / area  # 将径流量单位从ML/day转化为mm/s

# 根据逐日降雨量及逐日蒸发量，计算流域出口断面逐日径流量
nStep = data.shape[0]  # 计算数据中有多少天
