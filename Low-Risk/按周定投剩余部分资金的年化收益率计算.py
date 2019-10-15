#encoding=utf-8

weekOfYear = 52               # 每年 52 周
rate = 0.027                  # 年化 2.7% 收益率
weekRate = rate/weekOfYear    # 周利息
total = 0                     # 最终年化

for portionLeft in range(weekOfYear-1,1,-1):
    moneyLeft = portionLeft / weekOfYear
    # 每周的利息 = 剩余金钱总数（如 51 份） * 每周平均利率
    total = total + moneyLeft * weekRate
    # print(round(moneyLeft * weekRate * 100,4))
print("货币基金利率为 "+str(rate * 100) + "% 时，按 " + str(weekOfYear) + " 周定投")
print("未投入部分最终产生的收益率是：" + str(round(total * 100, 2)) + "%")