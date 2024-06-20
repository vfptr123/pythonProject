# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

def evaluate_gr4j_model(nStep, Qobs_mm, Q):
    # 精度评估
    count = 0  # 计数器：记录总天数
    Q_accum = 0.0  # 记录累计径流量
    Q_ave = 0.0  # 记录平均径流量
    NSE = 0.0  # 记录纳什效率系数
    Q_diff1 = 0.0
    Q_diff2 = 0.0

    for i in range(365, nStep):
        count += 1
        Q_accum += Qobs_mm[i]

    Q_ave = Q_accum / count  # 计算观测流量平均值

    for i in range(365, nStep):
        Q_diff1 += (Qobs_mm[i] - Q[i]) ** 2  # 计算Nash-Sutcliffe指数分子
        Q_diff2 += (Qobs_mm[i] - Q_ave) ** 2  # 计算Nash-Sutcliffe指数分母

    NSE = 1 - Q_diff1 / Q_diff2
    # 修正中文乱码
    import matplotlib as mpl
    mpl.rcParams['font.sans-serif'] = ['KaiTi']
    mpl.rcParams['font.serif'] = ['KaiTi']
    # 评估径流模拟效果：模型流域出口断面流量及模拟得到的流域出口断面流量
    # 绘制相关图
    axis = range(1, nStep + 1)
    plt.figure()
    plt.plot(axis, Q, 'r--', label='模拟径流量')
    plt.plot(axis, Qobs_mm, 'k-', label='观测径流量')
    plt.title('GR4J模型模拟效果图, NSE=' + str(NSE))
    plt.xlabel('时间（天）')
    plt.ylabel('流量（mm/d）')
    plt.legend()
    plt.show()

    return NSE



