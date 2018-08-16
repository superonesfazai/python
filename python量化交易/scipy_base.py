# coding:utf-8

'''
@author = super_fazai
@File    : scipy_base.py
@Time    : 2017/3/15 17:53
@connect : superonesfazai@gmail.com
'''

"""
NumPy替我们搞定了向量和矩阵的相关操作，基本上算是一个高级的科学计算器。
SciPy基于NumPy提供了更为丰富和高级的功能扩展，在统计、优化、插值、数值积分、时频转换等方面提供了大量的可用函数，基本覆盖了基础科学计算相关的问题

    在量化分析中，运用最广泛的是统计和优化的相关技术
"""

import numpy as np
import scipy.stats as stats
import scipy.optimize as opt

"""
统计部分
"""

'''生成随机数'''
# rv_continuous表示连续型的随机分布，如均匀分布（uniform）、正态分布（norm）、贝塔分布（beta）等
# rv_discrete表示离散型的随机分布，如伯努利分布（bernoulli）、几何分布（geom）、泊松分布（poisson）等

# 生成10个[0, 1]区间上的随机数
rv_unif = stats.uniform.rvs(size=10)
print(rv_unif)
# [0.40724459 0.09985714 0.81497799 0.72176607 0.13320602 0.4141679
#  0.32257506 0.67493034 0.02521065 0.59899874]

# 生成10个服从参数a=4，b=2的贝塔分布随机数
rv_beta = stats.beta.rvs(size=10, a=4, b=2)
print(rv_beta)
# [0.82845095 0.61869186 0.48966922 0.82297325 0.57183903 0.54696049
#  0.53687095 0.15694508 0.68522656 0.61492356]

# 指定了随机数的生成种子
np.random.seed(seed=2015)
rv_beta = stats.beta.rvs(size=10, a=4, b=2)
print('方法1: ', rv_beta)
# 方法1:  [0.43857338 0.9411551  0.75116671 0.92002864 0.62030521 0.56585548
#  0.41843548 0.5953096  0.88983036 0.94675351]

np.random.seed(seed=2015)
beta = stats.beta(a=4, b=2)
print('方法2: ', beta.rvs(size=10))
# 方法2:  [0.43857338 0.9411551  0.75116671 0.92002864 0.62030521 0.56585548
#  0.41843548 0.5953096  0.88983036 0.94675351]

'''假设检验'''
# 生成一组数据，并查看相关的统计量
norm_dist = stats.norm(loc=0.5, scale=2)
n = 200
dat = norm_dist.rvs(size=n)
print("数据的平均值为: ", str(np.mean(dat)))
# 数据的平均值为:  0.7051951380685283
print("数据的中位数为: ", str(np.median(dat)))
# 数据的中位数为:  0.658167882933473
print("数据的标准差为: ", str(np.std(dat)))
# 数据的标准差为:  2.0896700690524734

'''k-s检验'''
# 假设这个数据是我们获取到的实际的某些数据，如股票日涨跌幅
# 最简单的是检验这一组数据是否服从假设的分布，如正态分布
# 这个问题是典型的单样本假设检验问题
# 最为常见的解决方案是采用K-S检验
# 单样本K-S检验的原假设是给定的数据来自和原假设分布相同的分布
# 在SciPy中提供了kstest函数，参数分别是数据、拟检验的分布名称和对应的参数
mu = np.mean(dat)
sigma = np.std(dat)
stat_val, p_val = stats.kstest(dat, 'norm', (mu, sigma))
print('KS-statistic D = %6.3f p-value = %6.4f' % (stat_val, p_val))
# KS-statistic D =  0.045 p-value = 0.8195

'''t检验'''
# 假设检验的p-value值很大（在原假设下，p-value是服从[0, 1]区间上的均匀分布的随机变量, 可参考 http://en.wikipedia.org/wiki/P-value
# 因此我们接受原假设，即该数据通过了正态性的检验。
# 在正态性的前提下，我们可进一步检验这组数据的均值是不是0。
# 典型的方法是t检验（t-test），其中单样本的t检验函数为ttest_1samp
stat_val, p_val = stats.ttest_1samp(dat, 0)
print('One-sample t-statistic D = %6.3f, p-value = %6.4f' % (stat_val, p_val))
# One-sample t-statistic D =  4.761, p-value = 0.0000
# 我们看到p-value<0.05，即给定显著性水平0.05的前提下，我们应拒绝原假设：数据的均值为0

# 双样本的t检验(ttest_ind)
norm_dist2 = stats.norm(loc=-0.2, scale=1.2)
dat2 = norm_dist2.rvs(size=int(n/2))
stat_val, p_val = stats.ttest_ind(dat, dat2, equal_var=False)
print('Two-sample t-statistic D = %6.3f, p-value = %6.4f' % (stat_val, p_val))
# Two-sample t-statistic D =  5.565, p-value = 0.0000
# 注意，这里我们生成的第二组数据样本大小、方差和第一组均不相等，在运用t检验时需要使用Welch's t-test，即指定ttest_ind中的equal_var=False
# 我们同样得到了比较小的p-value$，在显著性水平0.05的前提下拒绝原假设，即认为两组数据均值不等

# stats还提供其他大量的假设检验函数，如bartlett和levene用于检验方差是否相等；anderson_ksamp用于进行Anderson-Darling的K-样本检验等

'''求分位'''
# 有时需要知道某数值在一个分布中的分位，或者给定了一个分布，求某分位上的数值
# 可以通过cdf和ppf函数完成
g_dist = stats.gamma(a=2)
print('quantiles of 2, 4 and 5: ', g_dist.cdf([2, 4, 5]))
# quantiles of 2, 4 and 5:  [0.59399415 0.90842181 0.95957232]
print('Values of 25%, 50% and 90%: ', g_dist.pdf([0.25, 0.5, 0.95]))
# Values of 25%, 50% and 90%:  [0.1947002  0.30326533 0.36740397]

# 查看分布的矩信息
# 对于一个给定的分布，可以用moment很方便的查看分布的矩信息
# 例如我们查看N(0,1)的六阶原点矩
print(stats.norm.moment(6, loc=0, scale=1))
# 15.000000000895332

# describe函数提供对数据集的统计描述分析，包括数据样本大小，极值，均值，方差，偏度和峰度
norm_dist = stats.norm(loc=0, scale=1.8)
dat = norm_dist.rvs(size=100)
info = stats.describe(dat)
print("Data size is: " + str(info[0]))   # Data size is: 100
print("最小值: " + str(info[1][0]))       # 最小值: -4.124145646873789
print("最大值: " + str(info[1][1]))       # 最大值: 4.82577602488523
print("算术平均数: " + str(info[2]))       # 算术平均数: 0.09629135922094763
print("方差: " + str(info[3]))            # 方差: 2.8871929246345207
print("偏度: " + str(info[4]))            # 偏度: -0.0025654879468099447
print("峰度: " + str(info[5]))            # 峰度: -0.3174634211772229

'''极大似然估计'''
# 当我们知道一组数据服从某些分布的时候，可以调用fit函数来得到对应分布参数的极大似然估计（MLE, maximum-likelihood estimation）
# 以下代码示例了假设数据服从正态分布，用极大似然估计分布参数
norm_dist = stats.norm(loc=0, scale=1.8)
dat = norm_dist.rvs(size=100)
mu, sigma = stats.norm.fit(dat)
print("MLE of data mean:" + str(mu))                    # MLE of data mean:-0.24988082991177035
print("MLE of data standard deviation:" + str(sigma))   # MLE of data standard deviation:1.891953035074205

'''Pearson和Spearman相关系数'''
# pearsonr和spearmanr可以计算Pearson和Spearman相关系数，这两个相关系数度量了两组数据的相互线性关联程度
norm_dist = stats.norm()
dat1 = norm_dist.rvs(size=100)
exp_dist = stats.expon()
dat2 = exp_dist.rvs(size=100)
cor, pval = stats.pearsonr(dat1, dat2)
print("Pearson correlation coefficient: " + str(cor))           # Pearson correlation coefficient: -0.02629119310142525
cor, pval = stats.pearsonr(dat1, dat2)
print("Spearman's rank correlation coefficient: " + str(cor))   # Spearman's rank correlation coefficient: -0.02629119310142525
# 其中的p-value表示原假设（两组数据不相关）下，相关系数的显著性

'''线性回归'''
# 在分析金融数据中使用频繁的线性回归在SciPy中也有提供
x = stats.chi2.rvs(3, size=50)
y = 2.5 + 1.2 * x + stats.norm.rvs(size=50, loc=0, scale=1.5)
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
print("拟合模型的斜率: " , slope)      # 拟合模型的斜率:  1.4451560119107203
print("拟合模型的截距: ", intercept)   # 拟合模型的截距:  1.9108068451588602
print("R-squared: ", r_value**2)     # R-squared:  0.7987869101731293

# @@@ 挖掘更多功能的最好方法还是直接读原始的文档。
# @@@ 另外，StatsModels（ http://statsmodels.sourceforge.net ）模块提供了更为专业，更多的统计相关函数。若在SciPy没有满足需求，可以采用StatsModels


"""
优化部分
"""
# 优化问题在投资中可谓是根本问题
# 如果手上有众多可选的策略，应如何从中选择一个“最好”的策略进行投资呢？这时就需要用到一些优化技术针对给定的指标进行寻优。
# 随着越来越多金融数据的出现，机器学习逐渐应用在投资领域，在机器学习中，优化也是十分重要的一个部分。

'''无约束优化问题'''
# 所谓的无约束优化问题指的是一个优化问题的寻优可行集合是目标函数自变量的定义域，即没有外部的限制条件
# 更进一步，我们假设考虑的问题全部是凸优化问题，即目标函数是凸函数，其自变量的可行集是凸集。
# （详细定义可参考斯坦福大学Stephen Boyd教授的教材convex optimization，下载链接：http://stanford.edu/~boyd/cvxbook ）

# 我们以Rosenbrock函数
# 作为寻优的目标函数来简要介绍在SciPy中使用优化模块scipy.optimize
def rosen(x):
    """The Rosenbrock function"""
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)

'''Nelder-Mead单纯形法'''
# 单纯形法是运筹学中介绍的求解线性规划问题的通用方法
# 这里的Nelder-Mead单纯形法与其并不相同，只是用到单纯形的概念。
# 设定起始点x0=(1.3,0.7,0.8,1.9,1.2)，并进行最小化的寻优。这里xtol表示迭代收敛的容忍误差上界
x_0 = np.array([0.5, 1.6, 1.1, 0.8, 1.2])
res = opt.minimize(rosen, x_0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
print("Result of minimizing Rosenbrock function via Nelder-Mead Simplex algorithm:")
print(res)
# Result of minimizing Rosenbrock function via Nelder-Mead Simplex algorithm:
#  final_simplex: (array([[1.        , 1.        , 1.        , 1.        , 1.        ],
#        [1.        , 1.        , 1.        , 1.        , 1.        ],
#        [1.        , 1.        , 1.        , 1.        , 0.99999999],
#        [1.        , 1.        , 1.        , 1.        , 1.        ],
#        [1.        , 1.        , 1.        , 1.        , 1.00000001],
#        [1.        , 1.        , 1.        , 1.        , 1.00000001]]), array([1.66149699e-17, 6.32117429e-17, 7.44105349e-17, 8.24396866e-17,
#        9.53208876e-17, 1.07882961e-16]))
#            fun: 1.6614969876635003e-17
#        message: 'Optimization terminated successfully.'
#           nfev: 706
#            nit: 436
#         status: 0
#        success: True
#              x: array([1., 1., 1., 1., 1.])

# Rosenbrock函数的性质比较好，简单的优化方法就可以处理了，还可以在minimize中使用method='powell'来指定使用Powell's method。
# 这两种简单的方法并不使用函数的梯度，在略微复杂的情形下收敛速度比较慢

'''函数梯度进行寻优: Broyden-Fletcher-Goldfarb-Shanno法'''
def rosen_der(x):
    # 我们可以如下定义梯度向量的计算函数了
    xm = x[1:-1]
    xm_m1 = x[:-2]
    xm_p1 = x[2:]
    der = np.zeros_like(x)
    der[1:-1] = 200*(xm-xm_m1**2) - 400*(xm_p1 - xm**2)*xm - 2*(1-xm)
    der[0] = -400*x[0]*(x[1]-x[0]**2) - 2*(1-x[0])
    der[-1] = 200*(x[-1]-x[-2]**2)
    return der

# 梯度信息的引入在minimize函数中通过参数jac指定
res = opt.minimize(rosen, x_0, method='BFGS', jac=rosen_der, options={'disp': True})
print("Result of minimizing Rosenbrock function via Broyden-Fletcher-Goldfarb-Shanno algorithm:")
print(res)
# Optimization terminated successfully.
#          Current function value: 0.000000
#          Iterations: 39
#          Function evaluations: 47
#          Gradient evaluations: 47
# Result of minimizing Rosenbrock function via Broyden-Fletcher-Goldfarb-Shanno algorithm:
#       fun: 1.5691916947088243e-14
#  hess_inv: array([[0.00742883, 0.01251316, 0.02376685, 0.04697638, 0.09387584],
#        [0.01251316, 0.02505532, 0.04784533, 0.094432  , 0.18862433],
#        [0.02376685, 0.04784533, 0.09594869, 0.18938093, 0.37814437],
#        [0.04697638, 0.094432  , 0.18938093, 0.37864606, 0.7559884 ],
#        [0.09387584, 0.18862433, 0.37814437, 0.7559884 , 1.51454413]])
#       jac: array([-3.60424798e-06,  2.74743159e-06, -1.94696995e-07,  2.78416196e-06,
#        -1.40984997e-06])
#   message: 'Optimization terminated successfully.'
#      nfev: 47
#       nit: 39
#      njev: 47
#    status: 0
#   success: True
#         x: array([1.        , 1.00000001, 1.00000002, 1.00000004, 1.00000007])

'''牛顿共轭梯度法（Newton-Conjugate-Gradient algorithm）'''
# 用到梯度的方法还有牛顿法，牛顿法是收敛速度最快的方法，其缺点在于要求Hessian矩阵（二阶导数矩阵）。
# 例如，当N=5时的Hessian矩阵为：
# 为使用牛顿共轭梯度法，我们需要提供一个计算Hessian矩阵的函数
def rosen_hess(x):
    x = np.asarray(x)
    H = np.diag(-400*x[:-1],1) - np.diag(400*x[:-1],-1)
    diagonal = np.zeros_like(x)
    diagonal[0] = 1200*x[0]**2-400*x[1]+2
    diagonal[-1] = 200
    diagonal[1:-1] = 202 + 1200*x[1:-1]**2 - 400*x[2:]
    H = H + np.diag(diagonal)
    return H

res = opt.minimize(rosen, x_0, method='Newton-CG', jac=rosen_der, hess=rosen_hess, options={'xtol': 1e-8, 'disp': True})
print("Result of minimizing Rosenbrock function via Newton-Conjugate-Gradient algorithm (Hessian):")
print(res)
# Optimization terminated successfully.
#          Current function value: 0.000000
#          Iterations: 20
#          Function evaluations: 22
#          Gradient evaluations: 41
#          Hessian evaluations: 20
# Result of minimizing Rosenbrock function via Newton-Conjugate-Gradient algorithm (Hessian):
#      fun: 1.47606641102778e-19
#      jac: array([-3.62847530e-11,  2.68148992e-09,  1.16637362e-08,  4.81693414e-08,
#        -2.76999090e-08])
#  message: 'Optimization terminated successfully.'
#     nfev: 22
#     nhev: 20
#      nit: 20
#     njev: 41
#   status: 0
#  success: True
#        x: array([1., 1., 1., 1., 1.])

# 对于一些大型的优化问题，Hessian矩阵将异常大，牛顿共轭梯度法用到的仅是Hessian矩阵和一个任意向量的乘积
# 为此，用户可以提供两个向量，一个是Hessian矩阵和一个任意向量p的乘积，另一个是向量p，这就减少了存储的开销。
# 我们定义如下函数并使用牛顿共轭梯度方法寻优
def rosen_hess_p(x, p):
    x = np.asarray(x)
    Hp = np.zeros_like(x)
    Hp[0] = (1200*x[0]**2 - 400*x[1] + 2)*p[0] - 400*x[0]*p[1]
    Hp[1:-1] = -400*x[:-2]*p[:-2]+(202+1200*x[1:-1]**2-400*x[2:])*p[1:-1] \
               -400*x[1:-1]*p[2:]
    Hp[-1] = -400*x[-2]*p[-2] + 200*p[-1]
    return Hp

res = opt.minimize(rosen, x_0, method='Newton-CG', jac=rosen_der, hessp=rosen_hess_p, options={'xtol': 1e-8, 'disp': True})
print("Result of minimizing Rosenbrock function via Newton-Conjugate-Gradient algorithm (Hessian times arbitrary vector):")
print(res)
# Result of minimizing Rosenbrock function via Newton-Conjugate-Gradient algorithm (Hessian times arbitrary vector):
#      fun: 1.47606641102778e-19
#      jac: array([-3.62847530e-11,  2.68148992e-09,  1.16637362e-08,  4.81693414e-08,
#        -2.76999090e-08])
#  message: 'Optimization terminated successfully.'
#     nfev: 22
#     nhev: 58
#      nit: 20
#     njev: 41
#   status: 0
#  success: True
#        x: array([1., 1., 1., 1., 1.])

'''约束优化问题'''
# 定义目标函数及其导数为
def func(x, sign=1.0):
    """ Objective function """
    return sign*(2*x[0]*x[1] + 2*x[0] - x[0]**2 - 2*x[1]**2)

def func_deriv(x, sign=1.0):
    """ Derivative of objective function """
    dfdx0 = sign*(-2*x[0] + 2*x[1] + 2)
    dfdx1 = sign*(2*x[0] - 4*x[1])
    return np.array([ dfdx0, dfdx1 ])

# 其中sign表示求解最小或者最大值，我们进一步定义约束条件
cons = ({'type': 'eq',  'fun': lambda x: np.array([x[0]**3 - x[1]]), 'jac': lambda x: np.array([3.0*(x[0]**2.0), -1.0])},
      {'type': 'ineq', 'fun': lambda x: np.array([x[1] - 1]), 'jac': lambda x: np.array([0.0, 1.0])})

# 最后我们使用SLSQP（Sequential Least SQuares Programming optimization algorithm）方法进行约束问题的求解（作为比较，同时列出了无约束优化的求解）
res = opt.minimize(func, [-1.0, 1.0], args=(-1.0,), jac=func_deriv, method='SLSQP', options={'disp': True})
print("Result of unconstrained optimization:")
print(res)
# Optimization terminated successfully.    (Exit mode 0)
#             Current function value: -2.0
#             Iterations: 4
#             Function evaluations: 5
#             Gradient evaluations: 4
# Result of unconstrained optimization:
#      fun: -2.0
#      jac: array([-0., -0.])
#  message: 'Optimization terminated successfully.'
#     nfev: 5
#      nit: 4
#     njev: 4
#   status: 0
#  success: True
#        x: array([2., 1.])
res = opt.minimize(func, [-1.0, 1.0], args=(-1.0,), jac=func_deriv, constraints=cons, method='SLSQP', options={'disp': True})
print("Result of constrained optimization:")
print(res)
# Optimization terminated successfully.    (Exit mode 0)
#             Current function value: -1.0000001831052137
#             Iterations: 9
#             Function evaluations: 14
#             Gradient evaluations: 9
# Result of constrained optimization:
#      fun: -1.0000001831052137
#      jac: array([-1.99999982,  1.99999982])
#  message: 'Optimization terminated successfully.'
#     nfev: 14
#      nit: 9
#     njev: 9
#   status: 0
#  success: True
#        x: array([1.00000009, 1.        ])

# 和统计部分一样，Python也有专门的优化扩展模块，CVXOPT（ http://cvxopt.org ）专门用于处理凸优化问题，在约束优化问题上提供了更多的备选方法。
# CVXOPT是著名的凸优化教材convex optimization的作者之一，加州大学洛杉矶分校Lieven Vandenberghe教授的大作，是处理优化问题的利器。