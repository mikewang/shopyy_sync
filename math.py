# 载入模块
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# 生成数据
x = np.linspace(-6 * np.pi, 6 * np.pi, 1000)
y = np.sin(x)
z = np.cos(x)

# 创建 3D 图形对象
fig = plt.figure()
ax = Axes3D(fig)

# 绘制线型图
ax.plot(x, y, z)

# 显示图
plt.show()

# --*--coding: utf_8--*--

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

# 画边长为1的正四棱锥

fig = plt.figure()

ax = fig.gca(projection='3d')

p_0 = (0, 0, 0)
p_1 = (0, 1, 0)
p_2 = (1, 1, 0)
p_3 = (1, 0, 0)
p_4 = (0.5, 0.5, 0.707)

# 画底边四条线
x = [0, 0, 1, 1, 0]
y = [0, 1, 1, 0, 0]
z = [0, 0, 0, 0, 0]
ax.plot(x, y, z, label='line 1')

# 连接其它的线
x1 = [0.5, 0, 1, 0.5, 1, 0, 0.5]
y1 = [0.5, 0, 0, 0.5, 1, 1, 0.5]
z1 = [0.707, 0, 0, 0.707, 0, 0, 0.707]
ax.plot(x1, y1, z1, label='line 2')

ax.legend()

plt.show()
