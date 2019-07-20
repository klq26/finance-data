import os
import sys

# 判断字符串是否可以转换为数值
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# 打开代码源文件
rawfile = open('./ParentPortfolioData.js',encoding='utf-8')
# 读取所有代码行
rawLines = rawfile.readlines()
# 关闭代码源文件
rawfile.close()

# 打开数据文件
datafile = open('./ParentData.txt',encoding='utf-8')
# 读取数据
dataLines = datafile.readlines()
dataArray = []
# 分析整合数据
for line in dataLines:
	if len(line) != 0 and line != '\n':
		elements = line.replace('%','').replace('\n','').split(' , ')
		dataArray.append((elements[0],elements[1]))
# print(dataArray)
# 关闭数据源文件
datafile.close()

targetLines = []
for line in rawLines:
	rawSpliter = 'new financeKind(\''
	# 如果有 new financeKind 字样，判断是否需要处理
	if rawSpliter in line:
		rawElements = line.split(rawSpliter)
		# 仓位数值
		elements = line.split(',')
		# 如果有数值，说明是人工更新的部分
		if is_number(elements[1]):
			result = ''
			# 查找匹配仓位数据
			for data in dataArray:
				if data[0] in line:
					result = elements[0] + ',' + data[1] + ',' + elements[2] + ',' + elements[3]
					break
			targetLines.append(result)
		# 如果没有数值，则是 JS 脚本自动计算部分，原样填写即可
		else:
			targetLines.append(line)
	else:
		targetLines.append(line)

# 以写入模式重新打开之前文件，写入修改结果
targetfile = open('./ParentPortfolioData.js','w+')
targetfile.writelines(targetLines)
targetfile.flush()
targetfile.close()
