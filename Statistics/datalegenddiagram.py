import matplotlib.pyplot as plt
import sys
import os

# 命令行参数获取，非必选
chengben = 0
expectMinValue = 0
if len(sys.argv) >= 2:
    chengben = float(sys.argv[1]) # 运行参数 1 成本价
if len(sys.argv) >= 3:
    expectMinValue = float(sys.argv[2]) # 运行参数 2 预估极限低点

# 打印文件名 不怎么常用
################################################################################
# filenames = []
# for root, dirs, files in os.walk("../Portfolio/indexValues/", topdown=False):
#     for name in files:
#         filenames.append(name)
#         # print(os.path.join(root, name))
# print(filenames)
################################################################################


# 直接改 index 就可以打印不同指数的情况（目前范围 0 ~ 11)
index = 11

# 文件名是用 os.walk 获取的
# 值都是 Excel 中转置复制，然后替换 tab 为 ',' 得到的
filenames = ['中证红利_000922.txt', '上证50_000016.txt', '沪深300_000300.txt','中证500_000905.txt', '中证1000_000852.txt','全指金融_000992.txt', '证券公司_399975.txt', '中证传媒_399971.txt', '全指医药_000991.txt',  '养老产业_399812.txt', '中证环保_000827.txt', '创业板_399006.txt']
# indexNames = ['中证红利','上证50','沪深300','中证500','中证1000','金融地产','证券公司','中证传媒','全指医药','养老产业','中证环保','创业板指']
myindexValues = [3921.21,2337.45,3386.67,5434.43,6125.47,5075.40,606.19,1491.61,8911.91,7342.04,1414.06,1468.44]
expectMinindexValues = [3620.45,2375.92,2960.08,3668.39,3750.68,5059.36,551.29,891.41,7123.00,5609.78,943.26,1054.47]



for index in range(0,10):
    name = filenames[index]
    chengben = myindexValues[index]
    expectMinValue = expectMinindexValues[index]

    f = open('../Portfolio/indexValues/{0}'.format(name),'r')
    lines = f.readlines()

    indexDates = []
    indexValues = []

    for line in lines:
        rawData = line.split('\t')
        indexDates.append(rawData[0])
        indexValues.append(round(float(rawData[1]),2))

    print(index)
    print(name)
    print('数据个数: {0}\n'.format(len(indexDates)))

    # 构件图像
    # plt.figure(1)
    '''
    在matplotlib下，一个Figure对象可以包含多个子图（Axes），可以使用subplot()快速绘制，其调用形式如下：
    subplot(numRows, numCols, plotNum)

    如果numRows = 3，numCols = 2，那整个绘制图表样式为3X2的图片区域，用坐标表示为（1，1），（1，2），（1，3），（2，1），（2，2），（2，3）。这时，当plotNum = 1时，表示的坐标为（1，1），即第一行第一列的子图；
    '''
    #第一行第一列图形
    if 1 + index >= 3 * 4:
        continue
    ax = plt.subplot(3,4, 1 + index)
    #选择 ax
    plt.sca(ax)

    x1 = [x for x in range(1,len(indexDates)+1)]
    y1 = indexValues
    x2 = x1
    y2 = [chengben for x in range(1,len(indexDates)+1)]
    x3 = x1
    y3 = [expectMinValue for x in range(1,len(indexDates)+1)]

    group_labels = indexDates

    length = len(name) # 计算标题
    plt.title(name[(length - 10):(length - 10) + 6])
    # plt.xlabel('date')
    plt.ylabel('value')

    plt.plot(x1, y1,'b', label='Index Value')
    # plt.xticks(x1, group_labels, rotation=0)
    plt.plot(x2, y2,'g',label='My Value')
    plt.plot(x3, y3,'r',label='expect Mininum Value')

    # plt.legend(bbox_to_anchor=[0.3, 1])
# plt.grid()
plt.show()
