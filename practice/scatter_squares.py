# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

x_values = list(range(1,1001))
y_values = [x**2 for x in x_values]

# 使用颜色映射   参数cmap告诉Plot使用哪个颜色映射
plt.scatter(x_values,y_values,c=y_values, cmap=plt.cm.Blues, edgecolors='none',s=40)

# 设置图表标题，并给坐标轴加上标签
plt.title("Square Numbers",fontsize=24)
plt.xlabel("Value",fontsize = 14)
plt.ylabel("Square of Value",fontsize = 14)

# 设置每个坐标轴的取值范围
plt.axis([0,1100,0,1100000])

# 自动保存图表  第一个参数以什么文件名保存，第二个指定图表多余的空白区裁减掉
# plt.savefig('squares_lot.png',bbox_inches='tight')
plt.show()