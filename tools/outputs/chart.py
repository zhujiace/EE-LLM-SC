import matplotlib.pyplot as plt

# 数据准备
labels = ['COT@20(0.9)-baseline1', 'COT@20-baseline2', 'COT@40-baseline3', 'COT@20-our method1', 'COT@20-baseline4', 'COT@20-baseline5', 'COT@20-our method2']
data = [0.17952635599694422, 0.23565416985462892, 0.2494313874147081, 0.23214285714285715, 0.6766304347826086, 0.7038043478260869, 0.7011494252873564]

plt.figure(figsize=(15, 6))
# 创建柱状图
plt.barh(labels, data)

# 设置坐标轴标签
plt.xlabel('Accuracy')
plt.ylabel('Label')

# 设置标题
# plt.title('Bar Chart')
plt.savefig('accuracy.png')
# 显示图形
plt.show()