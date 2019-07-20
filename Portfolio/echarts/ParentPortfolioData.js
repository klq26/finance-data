var aStockColor = {color: '#0aa3b5'};			// A 股（大盘股，中小盘股，红利价值，行业股）
var outSideNewColor = {color: '#187a2f'};		// 海外新兴（香港，海外互联网）
var outSideMatureColor = {color: '#ebb40f'};	// 海外成熟（德国）
var universalGoodsColor = {color: '#dd4c51'};	// 商品（黄金，白银，原油）
var bondColor = {color: '#be8663'};				// 债券（可转债，美元债）
var cashColor = {color: '#f7a128'};				// 低风险理财（货币基金，地产项目）
var nailPortfolioColor = {color: '#009ad6'};	// 螺丝钉投资组合

/* 金融品种 */
function financeKind(name, value, itemStyle, children)
{
	return {name : name + ' , ' + value + '%', value : value, itemStyle : itemStyle, children : children};
}

/* 整合仓位占比数据 */
function sumFinanceKindValue(array)
{
	total = 0.0;
	for(var i in array) {
		total += array[i].value;
	}
	return Math.round(total * 100) / 100;
}

/** A 股 */
function getAStock()
{
	// 大盘股
	var a1 = new financeKind('上证50',1.59,aStockColor,null);
	var a2 = new financeKind('沪深300',5.72,aStockColor,null);
	// 中小盘股
	var b1 = new financeKind('中证500',16.10,aStockColor,null);
	var b2 = new financeKind('中证1000',1.43,aStockColor,null);
	var b3 = new financeKind('创业板',2.86,aStockColor,null);
	// 红利价值
	var c1 = new financeKind('中证红利',11.15,aStockColor,null);
	// 行业股
	var d1 = new financeKind('养老产业',6.68,aStockColor,null);
	var d2 = new financeKind('全指医药',6.20,aStockColor,null);
	var d3 = new financeKind('中证传媒',3.81,aStockColor,null);
	var d4 = new financeKind('中证环保',3.90,aStockColor,null);
	var d5 = new financeKind('全指消费',0.00,aStockColor,null);
	var d6 = new financeKind('金融地产',1.18,aStockColor,null);
	var d7 = new financeKind('证券公司',0.62,aStockColor,null);
	// 螺丝钉组合定投
	var e1 = new financeKind('大盘股',2.28,nailPortfolioColor,null);
	var e2 = new financeKind('中盘股',2.46,nailPortfolioColor,null);
	var e3 = new financeKind('螺丝钉红利',2.11,nailPortfolioColor,null);
	var e4 = new financeKind('医药100',0.27,nailPortfolioColor,null);
	var e5 = new financeKind('海外新兴',1.72,nailPortfolioColor,null);

	var A1_subKind = [a1,a2];
	var B1_subKind = [b1,b2,b3];
	var C1_subKind = [c1];
	var D1_subKind = [d1,d2,d3,d4,d5,d6,d7];
	var E1_subKind = [e1,e2,e3,e4,e5];
	var A1 = new financeKind('大盘股',sumFinanceKindValue(A1_subKind),aStockColor,A1_subKind);
	var B1 = new financeKind('中小盘股',sumFinanceKindValue(B1_subKind),aStockColor,B1_subKind);
	var C1 = new financeKind('红利价值',sumFinanceKindValue(C1_subKind),aStockColor,C1_subKind);
	var D1 = new financeKind('行业股',sumFinanceKindValue(D1_subKind),aStockColor,D1_subKind);
	var E1 = new financeKind('螺丝钉定投',sumFinanceKindValue(E1_subKind),nailPortfolioColor,E1_subKind);

	var aStock_subKind = [A1,B1,C1,D1,E1];
	var aStock = new financeKind('A股',sumFinanceKindValue(aStock_subKind),aStockColor,aStock_subKind);
	return aStock;
}

/** 海外新兴 */
function getOutsideNew()
{
	// 香港
	var e1 = new financeKind('恒生',0.52,outSideNewColor,null);
	// 海外互联
	var f1 = new financeKind('海外互联网',1.96,outSideNewColor,null);

	var E1_subKind = [e1];
	var F1_subKind = [f1];
	var E1 = new financeKind('香港',sumFinanceKindValue(E1_subKind),outSideNewColor,E1_subKind);
	var F1 = new financeKind('海外互联',sumFinanceKindValue(F1_subKind),outSideNewColor,F1_subKind);

	var outsideNew_subKind = [E1,F1];
	var outsideNew = new financeKind('海外新兴',sumFinanceKindValue(outsideNew_subKind),outSideNewColor,outsideNew_subKind);
	return outsideNew;
}

/** 海外成熟 */
function getOutsideMature()
{
	var g1 = new financeKind('德国30',2.56,outSideMatureColor,null);

	var G1_subKind = [g1];
	var G1 = new financeKind('海外成熟',sumFinanceKindValue(G1_subKind),outSideMatureColor,G1_subKind);

	var outsideNew_subKind = [G1];
	var outsideMature = new financeKind('海外成熟',sumFinanceKindValue(outsideNew_subKind),outSideMatureColor,outsideNew_subKind);
	return outsideMature;
}

/** 商品 */
function getUniversalGoods()
{
	var h1 = new financeKind('原油',1.19,universalGoodsColor,null);
	var h2 = new financeKind('黄金',1.04,universalGoodsColor,null);

	var H1_subKind = [h1,h2];
	var H1 = new financeKind('商品',sumFinanceKindValue(H1_subKind),universalGoodsColor,H1_subKind);

	var universalGoods_subKind = [H1];
	var universalGoods = new financeKind('商品',sumFinanceKindValue(universalGoods_subKind),universalGoodsColor,universalGoods_subKind);
	return universalGoods;
}

/** 债券 */
function getBond()
{
	// 国内债券
	var i1 = new financeKind('可转债',5.11,bondColor,null);

	var I1_subKind = [i1];
	var I1 = new financeKind('国内债券',sumFinanceKindValue(I1_subKind),bondColor,I1_subKind);

	var bond_subKind = [I1];
	var bond = new financeKind('债券',sumFinanceKindValue(bond_subKind),bondColor,bond_subKind);
	return bond;
}

/** 现金 */
function getCash()
{
	// 货币基金
	var k1 = new financeKind('货币基金',17.53,cashColor,null);

	var K1_subKind = [k1];
	var K1 = new financeKind('低风险理财',sumFinanceKindValue(K1_subKind),cashColor,K1_subKind);

	var cash_subKind = [K1];
	var cash = new financeKind('现金',sumFinanceKindValue(cash_subKind),cashColor,cash_subKind);
	return cash;
}

/* 获取投资组合数据 */
function getPortfolioData()
{
	// A 股
	var aStock = getAStock();
	// 海外新兴
	var outsideNew = getOutsideNew();
	// 海外成熟
	var outsideMature = getOutsideMature();
	// 商品
	var universalGoods = getUniversalGoods();
	// 债券
	var bond = getBond();
	// 现金
	var cash = getCash();

	data = [aStock, outsideNew, outsideMature, universalGoods, bond, cash];
	console.log(data);
	return data;
}

getPortfolioData();
