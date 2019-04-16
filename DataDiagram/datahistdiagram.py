from numpy import array
import numpy as np
from matplotlib import pyplot
from matplotlib.ticker import PercentFormatter

def get_data():
    lenths=[]
    readfile=open("data.txt")
    lines=readfile.readlines()
    for line in lines:
        line=float(line)
        lenths.append(line)
    return array(lenths)

lenths=get_data()

main_color = '#398BC0'
# 文档
# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.hist.html#matplotlib.pyplot.hist
# density n. 比重：显示占比而不是个数
y, x, patches = pyplot.hist(lenths, 100,density=True, facecolor=main_color, alpha=0.4)	# 两个数组，包含 x 和 y 值
pyplot.grid(True)
pyplot.xlabel('PE')
pyplot.xticks(np.linspace(1,8,8,endpoint=True))
pyplot.ylabel('Occur Frequency')
pyplot.title('All market PB Frequency')

average = lenths.mean() # 平均数
std = lenths.std() # 标准差
targets = [round(average - std,2), round(average,2), round(average + std,2), round(average + std * 2,2)] # 标准差
for i in range(0,len(targets)):
    result = np.where(x < targets[i])[0]
    if len(result) == 0:
        continue
    idx = result[-1] # 取索引
    print(idx)
    print(targets[i])
    val_x = x[idx]
    val_y = y[idx]
    print(val_x)
    print(val_y)
    print('/n')
    pyplot.text(val_x, val_y, '{0}-{1}%'.format(round(val_x,2), round(val_y * 100,2)),bbox=dict(facecolor=main_color, alpha=0.6))
pyplot.show()

print(x)
print(y)
