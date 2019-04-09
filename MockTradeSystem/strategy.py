# coding=utf-8

# 交易策略
class strategy:
	def __init__(self,name,code,netValue):
		'''初始化一只基金的交易策略'''
		self.name = name						# 中文名
		self.code = code						# 代码
		self.netMarketCap = netValue			# 市场价
		self.recommendPositions = 0				# 推荐仓位占比
		self.recommendPrice = 0					# 推荐买入价格
		pass

	def getRecommendPositions(self,netValue):
		'''根据净值和策略，计算推荐的仓位。返回的是一个百分比'''
		return self.recommendPositions
		pass
		
	def getRecommendPrice(self,netValue):
		'''根据净值和策略，计算推荐的价格。返回的是一个交易价'''
		return self.recommendPrice
		pass
	pass

# 沪深300
class strategyHS300(strategy):
	def getRecommendPositions(self,netValue):		
		if netValue <= 2200:
			self.recommendPositions = 1
		elif netValue >= 4000:
			self.recommendPositions = 0
		return self.recommendPositions
		pass
	
	def getRecommendPrice(self,netValue):		
		self.recommendPrice = round(netValue / 100,2)
		return self.recommendPrice
		pass	
	pass
	
# 中证500
class strategyZZ500(strategy):
	def getRecommendPositions(self,netValue):		
		if netValue <= 4100:
			self.recommendPositions = 1
		elif netValue >= 10000:
			self.recommendPositions = 0
		return self.recommendPositions
		pass
	
	def getRecommendPrice(self,netValue):		
		self.recommendPrice = round(netValue / 100,2)
		return self.recommendPrice
		pass	
	pass
	
# 10年期国债收益率
class strategy10YEAR(strategy):
	def getRecommendPositions(self,netValue):		
		if netValue >= 4.0:
			self.recommendPositions = 1
		elif netValue <= 3.2:
			self.recommendPositions = 0
		return self.recommendPositions
		pass
	
	def getRecommendPrice(self,netValue):		
		self.recommendPrice = round(1.0 / netValue,2)
		return self.recommendPrice
		pass	
	pass