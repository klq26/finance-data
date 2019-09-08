var aStockColor = {color: '#0aa3b5'};			// A �ɣ����̹ɣ���С�̹ɣ�������ֵ����ҵ�ɣ�
var outSideNewColor = {color: '#187a2f'};		// �������ˣ���ۣ����⻥������
var outSideMatureColor = {color: '#ebb40f'};	// ������죨�¹���
var universalGoodsColor = {color: '#dd4c51'};	// ��Ʒ���ƽ𣬰�����ԭ�ͣ�
var bondColor = {color: '#be8663'};				// ծȯ����תծ����Ԫծ��
var cashColor = {color: '#f7a128'};				// �ͷ�����ƣ����һ��𣬵ز���Ŀ��
var nailPortfolioColor = {color: '#009ad6'};	// ��˿��Ͷ�����

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
	var a1 = new financeKind('��֤50',1.51,aStockColor,null);
	var a2 = new financeKind('����300',5.45,aStockColor,null);
	// ��С�̹�
	var b1 = new financeKind('��֤500',15.23,aStockColor,null);
	var b2 = new financeKind('��֤1000',1.34,aStockColor,null);
	var b3 = new financeKind('��ҵ��',2.80,aStockColor,null);
	// ������ֵ
	var c1 = new financeKind('��֤����',10.29,aStockColor,null);
	// ��ҵ��
	var d1 = new financeKind('���ϲ�ҵ',6.50,aStockColor,null);
	var d2 = new financeKind('ȫָҽҩ',6.23,aStockColor,null);
	var d3 = new financeKind('��֤��ý',3.65,aStockColor,null);
	var d4 = new financeKind('��֤����',3.68,aStockColor,null);
	var d5 = new financeKind('ȫָ����',3.27,aStockColor,null);
	var d6 = new financeKind('���ڵز�',1.09,aStockColor,null);
	var d7 = new financeKind('֤ȯ��˾',0.56,aStockColor,null);
	// ��˿����϶�Ͷ
	var e1 = new financeKind('���̹�',2.97,nailPortfolioColor,null);
	var e2 = new financeKind('���̹�',3.49,nailPortfolioColor,null);
	var e3 = new financeKind('��˿������',2.39,nailPortfolioColor,null);
	var e4 = new financeKind('ҽҩ����',0.36,nailPortfolioColor,null);
	var e5 = new financeKind('��������',1.53,nailPortfolioColor,null);

	var A1_subKind = [a1,a2];
	var B1_subKind = [b1,b2,b3];
	var C1_subKind = [c1];
	var D1_subKind = [d1,d2,d3,d4,d5,d6,d7];
	var E1_subKind = [e1,e2,e3,e4,e5];
	var A1 = new financeKind('���̹�',sumFinanceKindValue(A1_subKind),aStockColor,A1_subKind);
	var B1 = new financeKind('��С�̹�',sumFinanceKindValue(B1_subKind),aStockColor,B1_subKind);
	var C1 = new financeKind('������ֵ',sumFinanceKindValue(C1_subKind),aStockColor,C1_subKind);
	var D1 = new financeKind('��ҵ��',sumFinanceKindValue(D1_subKind),aStockColor,D1_subKind);
	var E1 = new financeKind('��˿����Ͷ',sumFinanceKindValue(E1_subKind),nailPortfolioColor,E1_subKind);

	var aStock_subKind = [A1,B1,C1,D1,E1];
	var aStock = new financeKind('A��',sumFinanceKindValue(aStock_subKind),aStockColor,aStock_subKind);
	return aStock;
}

/** �������� */
function getOutsideNew()
{
	// ���
	var e1 = new financeKind('����',0.46,outSideNewColor,null);
	// ���⻥��
	var f1 = new financeKind('���⻥����',1.84,outSideNewColor,null);

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
	var g1 = new financeKind('�¹�30',2.33,outSideMatureColor,null);

	var G1_subKind = [g1];
	var G1 = new financeKind('�������',sumFinanceKindValue(G1_subKind),outSideMatureColor,G1_subKind);

	var outsideNew_subKind = [G1];
	var outsideMature = new financeKind('�������',sumFinanceKindValue(outsideNew_subKind),outSideMatureColor,outsideNew_subKind);
	return outsideMature;
}

/** ��Ʒ */
function getUniversalGoods()
{
	var h1 = new financeKind('ԭ��',1.03,universalGoodsColor,null);
	var h2 = new financeKind('�ƽ�',1.04,universalGoodsColor,null);

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
	var i1 = new financeKind('��תծ',5.85,bondColor,null);

	var I1_subKind = [i1];
	var I1 = new financeKind('����ծȯ',sumFinanceKindValue(I1_subKind),bondColor,I1_subKind);

	var bond_subKind = [I1];
	var bond = new financeKind('ծȯ',sumFinanceKindValue(bond_subKind),bondColor,bond_subKind);
	return bond;
}

/** �ֽ� */
function getCash()
{
	// ���һ���
	var k1 = new financeKind('���һ���',15.10,cashColor,null);

	var K1_subKind = [k1];
	var K1 = new financeKind('�ͷ������',sumFinanceKindValue(K1_subKind),cashColor,K1_subKind);

	var cash_subKind = [K1];
	var cash = new financeKind('�ֽ�',sumFinanceKindValue(cash_subKind),cashColor,cash_subKind);
	return cash;
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

	data = [aStock, outsideNew, outsideMature, universalGoods, bond, cash];
	console.log(data);
	return data;
}

getPortfolioData();
