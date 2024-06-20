import numpy as np
from evaluatefunction import *
from mytools import *
from data import *
from simulate import *
from scipy.optimize import dual_annealing

# 初始化变量，存储GR4J模型中间变量值
Pn = np.zeros(nStep)  # Pn：降雨扣除损失（蒸发）后得净雨
En = np.zeros(nStep)  # En：当日蒸发未被满足部分，此部分未得到满足得蒸发将消耗土壤中得水分
Ps = np.zeros(nStep)  # Ps：中间变量，记录净雨补充土壤含水量
Es = np.zeros(nStep)  # Es: 中间变量，记录剩余蒸发能力消耗土壤含水量
Perc = np.zeros(nStep)  # Perc: 中间变量，记录产流水库壤中流产流量
Pr = np.zeros(nStep)  # Pr: 记录产流总量

# 根据输入参数x4计算S曲线以及单位线，这里假设单位线长度UH1为10，UH2为20;即x4取值不应该大于10
maxDayDelay = 10

# 定义几个数组以存储SH1, UH1, SH2, UH2
SH1 = np.zeros(maxDayDelay)
UH1 = np.zeros(maxDayDelay)
SH2 = np.zeros(2 * maxDayDelay)
UH2 = np.zeros(2 * maxDayDelay)


# 定义GR4J模型的目标函数，通常是最小化误差（如均方误差）
def objective_function(parameters, nStep, upperTankRatio, lowerTankRatio, maxDayDelay, UH1, UH2, Pn, En, Qobs_mm, flag):
    X1, X2, X3, X4 = parameters
    # 计算SH1以及SH2，由于i是从0开始的，为避免第一个数值为0，我们在函数钟使用i+1
    for i in range(maxDayDelay):
        SH1[i] = SH1_CURVE(i, X4)

    for i in range(2 * maxDayDelay):
        SH2[i] = SH2_CURVE(i, X4)

    # 计算UH1以及UH2
    for i in range(maxDayDelay):
        if i == 0:
            UH1[i] = SH1[i]
        else:
            UH1[i] = SH1[i] - SH1[i - 1]

    for i in range(2 * maxDayDelay):
        if i == 0:
            UH2[i] = SH2[i]
        else:
            UH2[i] = SH2[i] - SH2[i - 1]

    # 计算逐日En及Pn值，En及Pn为GR4J模型的输入，可以提前计算出来
    for i in range(nStep):
        if P[i] >= E[i]:  # 若当日降雨量大于等于当日蒸发量，净降雨量Pn = P - E，净蒸发能力En = 0
            Pn[i] = P[i] - E[i]
            En[i] = 0
        else:  # 若当日降雨量小于当日蒸发量，净降雨量Pn = 0，净蒸发能力En = E - P
            Pn[i] = 0
            En[i] = E[i] - P[i]

    Q = simulate_gr4j(nStep, X1, X2, X3, X4, upperTankRatio, lowerTankRatio, maxDayDelay, UH1, UH2, Pn, En)
    error = 0.0
    for i in range(365, nStep):
        error += (Qobs_mm[i] - Q[i]) ** 2  # 计算Nash-Sutcliffe指数分子,利用它来调参
    if flag == 0:
        return error
    else:
        return Q


# 定义参数范围
parameter_bounds = [
    [10, 700],  # X1范围
    [-5.5, 3.5],  # X2范围
    [20, 400],  # X3范围
    [1.0, 2.5]  # X4范围
]

# 使用模拟退火进行参数优化
result = dual_annealing(objective_function, bounds=parameter_bounds,
                        args=(nStep, upperTankRatio, lowerTankRatio, maxDayDelay, UH1, UH2, Pn, En, Qobs_mm, 0),
                        maxiter=10)

# 得到x1,x2,x3,x4四个参数
optimal_parameters = result.x

Q = objective_function(optimal_parameters, nStep, upperTankRatio, lowerTankRatio, maxDayDelay, UH1, UH2, Pn, En,
                       Qobs_mm, 1)

# 精度评估和绘图
evaluate_gr4j_model(nStep, Qobs_mm, Q)

# 保存参数
np.savetxt('GR4J_Parameter.txt', optimal_parameters, fmt='%f')
