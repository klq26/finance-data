# coding=utf-8

# 持仓基金
class fund:
	def __init__(self,name,code,netValue,cash):
		'''初始化一只基金'''
		self.name = name						# 中文名
		self.code = code						# 代码
		self.netValue = netValue				# 持仓成本
		self.netMarketCap = netValue			# 市场价
		self.positions = int(cash / netValue)	# 持仓仓位
		pass
	
	def buy(self,netValue,cash):
		'''买入一定金额'''
		self.netMarketCap = netValue
		newNetValue = netValue
		newPositions = int(cash / netValue)
		print('买入价格：{0} 操作仓位：{1}'.format(round(newNetValue,2),newPositions))
		self.netValue = round((self.netValue * self.positions + newNetValue * newPositions)/(self.positions + newPositions),4)
		self.positions = self.positions + newPositions
		print('最新成本：{0} 最新仓位：{1}'.format(self.netValue, self.positions))
		pass
	
	def sell(self,netValue,cash):
		'''卖出一定金额'''
		self.netMarketCap = netValue
		newNetValue = netValue
		newPositions = int(cash / netValue)		
		if -newPositions >= self.positions:
			# 相当于清仓
			newPositions = -self.positions
			currentValue = self.netMarketCap * self.positions
			print('清仓价格：{0} 操作仓位：{1}'.format(round(newNetValue,2),newPositions))
			self.netValue = 0
			self.positions = 0
			print('最新成本：{0} 最新仓位：{1}'.format(self.netValue, self.positions))
			return currentValue
		else:
			print('卖出价格：{0} 操作仓位：{1}'.format(newNetValue,newPositions))
			self.netValue = round((self.netValue * self.positions + newNetValue * newPositions)/(self.positions + newPositions),4)
			self.positions = self.positions + newPositions
			print('最新成本：{0} 最新仓位：{1}'.format(self.netValue, self.positions))
			return -cash	# 返回卖出所得金额
		pass
	pass
	
class portfolio:
	'''投资组合(暂时只支持一只权益类资产 + 现金剩余)'''
	def __init__(self, cash):
		'''初始化投资组合'''
		self.cash = cash				# 现金类
		self.positionValue = 0			# 权益类
		self.marketCap = self.cash		# 总市值
		pass
			
	def initFund(self,name,code,netValue,cash):
		self.fund = fund(name,code,netValue,cash)
		pass
	
	def printFund(self):
		print('现金：{0} 权益类：{1} 投资组合：{2}'.format(self.cash, self.positionValue, self.marketCap))
		print('现金：{:.2f}% 权益类：{:.2f}% 投资组合：{:.2f}%'.format(self.cash / self.marketCap * 100, self.positionValue / self.marketCap * 100, 100))
	
	def updateFund(self,netValue,percent):		
		self.updatePortfolio(netValue)
		cash = round(self.marketCap * percent - self.positionValue,2)
		if cash > 0:
			self.fund.buy(netValue,cash)
			self.cash = round(self.cash - cash,2)
			self.positionValue = cash
			self.marketCap = round(self.cash + self.fund.netMarketCap * self.fund.positions,2)
		if cash <= 0:
			returnCash = self.fund.sell(netValue,cash)	# 赎回收益
			self.cash = round(self.cash + returnCash,2)
			self.positionValue = self.positionValue - returnCash
			self.marketCap = round(self.cash + self.fund.netMarketCap * self.fund.positions,2)
		pass
		
	def updatePortfolio(self,netValue):
		self.fund.netMarketCap = netValue	# 市场价
		self.positionValue = netValue * self.fund.positions	# 权益类市值
		self.marketCap = round(self.cash + self.positionValue,2)	# 组合市值
		pass
		
	pass

	
