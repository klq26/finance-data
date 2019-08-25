var aStockColor = {color: '#0aa3b5'};			// A �ɣ����̹ɣ���С�̹ɣ�������ֵ����ҵ�ɣ�
var outSideNewColor = {color: '#187a2f'};		// �������ˣ���ۣ����⻥������
var outSideMatureColor = {color: '#ebb40f'};	// ������죨�¹���
var universalGoodsColor = {color: '#dd4c51'};	// ��Ʒ���ƽ𣬰�����ԭ�ͣ�
var bondColor = {color: '#be8663'};				// ծȯ����תծ����Ԫծ��
var cashColor = {color: '#f7a128'};				// �ͷ�����ƣ����һ��𣬵ز���Ŀ��
var frozenCashColor = {color: '#8b8c90'};		// �����ʽ𣨹�����

/* ����Ʒ�� */
function financeKind(name, value, itemStyle, children)
{
	return {name : name + ' , ' + value + '%', value : value, itemStyle : itemStyle, children : children};
}

/* ���ϲ�λռ������ */
function sumFinanceKindValue(array)
{
	total = 0.0;
	for(var i in array) {
		total += array[i].value;
	}
	return Math.round(total * 100) / 100;
}

/** A �� */
function getAStock()
{
	// ���̹�
	var a1 = new financeKind('��֤50',0.63,aStockColor,null);
	var a2 = new financeKind('����300',4.63,aStockColor,null);
	// ��С�̹�
	var b1 = new financeKind('��֤500',17.08,aStockColor,null);
	// var b2 = new financeKind('��֤1000',0.00,aStockColor,null);
	var b3 = new financeKind('��ҵ��',1.76,aStockColor,null);
	// ������ֵ
	var c1 = new financeKind('��֤����',5.63,aStockColor,null);
	// ��ҵ��
	var d1 = new financeKind('���ϲ�ҵ',4.74,aStockColor,null);
	var d2 = new financeKind('ȫָҽҩ',4.14,aStockColor,null);
	var d3 = new financeKind('��֤��ý',2.41,aStockColor,null);
	var d4 = new financeKind('��֤����',3.25,aStockColor,null);
	//var d5 = new financeKind('ȫָ����',0.00,aStockColor,null);
	var d6 = new financeKind('���ڵز�',1.80,aStockColor,null);
	var d7 = new financeKind('֤ȯ��˾',2.43,aStockColor,null);

	var A1_subKind = [a1,a2];
	var B1_subKind = [b1,b3];
	var C1_subKind = [c1];
	var D1_subKind = [d1,d2,d3,d4,d6,d7];
	var A1 = new financeKind('���̹�',sumFinanceKindValue(A1_subKind),aStockColor,A1_subKind);
	var B1 = new financeKind('��С�̹�',sumFinanceKindValue(B1_subKind),aStockColor,B1_subKind);
	var C1 = new financeKind('������ֵ',sumFinanceKindValue(C1_subKind),aStockColor,C1_subKind);
	var D1 = new financeKind('��ҵ��',sumFinanceKindValue(D1_subKind),aStockColor,D1_subKind);

	var aStock_subKind = [A1,B1,C1,D1];
	var aStock = new financeKind('A��',sumFinanceKindValue(aStock_subKind),aStockColor,aStock_subKind);
	return aStock;
}

/** �������� */
function getOutsideNew()
{
	// ���
	var e1 = new financeKind('����',0.51,outSideNewColor,null);
	// ���⻥��
	var f1 = new financeKind('���⻥����',1.53,outSideNewColor,null);

	var E1_subKind = [e1];
	var F1_subKind = [f1];
	var E1 = new financeKind('���',sumFinanceKindValue(E1_subKind),outSideNewColor,E1_subKind);
	var F1 = new financeKind('���⻥��',sumFinanceKindValue(F1_subKind),outSideNewColor,F1_subKind);

	var outsideNew_subKind = [E1,F1];
	var outsideNew = new financeKind('��������',sumFinanceKindValue(outsideNew_subKind),outSideNewColor,outsideNew_subKind);
	return outsideNew;
}

/** ������� */
function getOutsideMature()
{
	var g1 = new financeKind('�¹�30',1.79,outSideMatureColor,null);

	var G1_subKind = [g1];
	var G1 = new financeKind('�������',sumFinanceKindValue(G1_subKind),outSideMatureColor,G1_subKind);

	var outsideNew_subKind = [G1];
	var outsideMature = new financeKind('�������',sumFinanceKindValue(outsideNew_subKind),outSideMatureColor,outsideNew_subKind);
	return outsideMature;
}

/** ��Ʒ */
function getUniversalGoods()
{
	var h1 = new financeKind('ԭ��',1.16,universalGoodsColor,null);
	var h2 = new financeKind('�ƽ�',1.21,universalGoodsColor,null);
	//var h3 = new financeKind('����',0.00,universalGoodsColor,null);

	var H1_subKind = [h1,h2];
	var H1 = new financeKind('��Ʒ',sumFinanceKindValue(H1_subKind),universalGoodsColor,H1_subKind);

	var universalGoods_subKind = [H1];
	var universalGoods = new financeKind('��Ʒ',sumFinanceKindValue(universalGoods_subKind),universalGoodsColor,universalGoods_subKind);
	return universalGoods;
}

/** ծȯ */
function getBond()
{
	// ����ծȯ
	var i1 = new financeKind('��תծ',6.08,bondColor,null);
	// ����ծȯ
	var j1 = new financeKind('��Ԫծ',0.58,bondColor,null);

	var I1_subKind = [i1];
	var J1_subKind = [j1];
	var I1 = new financeKind('����ծȯ',sumFinanceKindValue(I1_subKind),bondColor,I1_subKind);
	var J1 = new financeKind('����ծȯ',sumFinanceKindValue(J1_subKind),bondColor,J1_subKind);

	var bond_subKind = [I1,J1];
	var bond = new financeKind('ծȯ',sumFinanceKindValue(bond_subKind),bondColor,bond_subKind);
	return bond;
}

/** �ֽ� */
function getCash()
{
	// ���һ���
	var k1 = new financeKind('���һ���',5.18,cashColor,null);
	// �ز�����
	var l1 = new financeKind('�ز�����',8.55,cashColor,null);

	var K1_subKind = [k1];
	var L1_subKind = [l1];
	var K1 = new financeKind('�ͷ������',sumFinanceKindValue(K1_subKind),cashColor,K1_subKind);
	var L1 = new financeKind('�еͷ������',sumFinanceKindValue(L1_subKind),cashColor,L1_subKind);

	var cash_subKind = [K1,L1];
	var cash = new financeKind('�ֽ�',sumFinanceKindValue(cash_subKind),cashColor,cash_subKind);
	return cash;
}

/** �����ʽ� */
function getFrozenCash()
{
	// ������
	var m1 = new financeKind('������',24.92,frozenCashColor,null);

	var M1_subKind = [m1];
	var M1 = new financeKind('������',sumFinanceKindValue(M1_subKind),frozenCashColor,M1_subKind);

	var frozenCash_subKind = [M1];
	var frozenCash = new financeKind('�����ʽ�',sumFinanceKindValue(frozenCash_subKind),frozenCashColor,frozenCash_subKind);
	return frozenCash;
}

/* ��ȡͶ��������� */
function getPortfolioData()
{
	// A ��
	var aStock = getAStock();
	// ��������
	var outsideNew = getOutsideNew();
	// �������
	var outsideMature = getOutsideMature();
	// ��Ʒ
	var universalGoods = getUniversalGoods();
	// ծȯ
	var bond = getBond();
	// �ֽ�
	var cash = getCash();
	// �����ʽ�
	var frozenCash = getFrozenCash();

	data = [aStock, outsideNew, outsideMature, universalGoods, bond, cash, frozenCash];
	console.log(data);
	return data;
}

getPortfolioData();
