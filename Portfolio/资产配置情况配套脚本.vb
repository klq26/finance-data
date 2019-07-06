'输出持仓市值汇总的行游标
Public lineIndex As Integer
'股票尾部索引
Public stockEndIndex As Integer
'基金尾部索引
Public fundEndIndex As Integer


Sub ★更新持仓市值()
    lineIndex = 1
    '下面函数更新 lineIndex
    获取涨乐财富通数据
    获取天天基金对账单
    '数据格式化
    输出到资产配置情况
End Sub

'整理股票账户持仓情况的快捷脚本
Sub 获取涨乐财富通数据()
    Set SheetSource = Sheets("涨乐财富通")
    Set SheetResult = Sheets("持仓市值汇总")
    '非空个数
    Count = Application.WorksheetFunction.CountA(SheetSource.Range("A:A"))
    stockEndIndex = Count
    Dim codeColumn As Integer, nameColumn As Integer, valueColumn As Integer
    codeColumn = 1
    nameColumn = 2
    valueColumn = 9
    For i = 2 To Count
        SheetResult.Cells(i, 1) = SheetSource.Cells(i, codeColumn).Value
        SheetResult.Cells(i, 2) = SheetSource.Cells(i, nameColumn).Value
        SheetResult.Cells(i, 3) = SheetSource.Cells(i, valueColumn).Value
        SheetResult.Range(Cells(i, 1), Cells(i, 3)).Interior.Color = 255
        lineIndex = lineIndex + 1
    Next
End Sub

'整理基金账户持仓情况的快捷脚本
Sub 获取天天基金对账单()
    Set SheetSource = Sheets("天天基金网")
    Set SheetResult = Sheets("持仓市值汇总")
    '非空个数
    Count = Application.WorksheetFunction.CountA(SheetSource.Range("A:A"))
    fundEndIndex = Count
    Dim codeColumn As Integer, nameColumn As Integer, valueColumn As Integer
    codeColumn = 1
    nameColumn = 2
    valueColumn = 7
    For i = 2 To Count
        SheetResult.Cells(i + lineIndex - 1, 1) = SheetSource.Cells(i, codeColumn).Value
        SheetResult.Cells(i + lineIndex - 1, 2) = SheetSource.Cells(i, nameColumn).Value
        SheetResult.Cells(i + lineIndex - 1, 3) = SheetSource.Cells(i, valueColumn).Value
        SheetResult.Range(Cells(i + lineIndex - 1, 1), Cells(i + lineIndex - 1, 3)).Interior.Color = 26367
    Next
End Sub
'数据格式化
Sub 数据格式化()
    Set SheetResult = Sheets("持仓市值汇总")
    Count = Application.WorksheetFunction.CountA(SheetResult.Range("A:A"))
    '选中代码
    SheetResult.Range(Cells(1, 1), Cells(Count + 1, 1)).Select
    '数字格式前面补零
    Selection.NumberFormatLocal = "#000000"
    '选中市值
    SheetResult.Range(Cells(1, 3), Cells(Count + 1, 3)).Select
    '数字格式保留两位小数
    Selection.NumberFormatLocal = "0.00"
End Sub
'根据 code 自动更新市值数据
Sub 输出到资产配置情况()
    Set SheetSource = Sheets("持仓市值汇总")
    Set SheetResult = Sheets("资产配置情况")
    ResultCount = Application.WorksheetFunction.CountA(SheetResult.Range("I:I"))
    SourceCount = Application.WorksheetFunction.CountA(SheetSource.Range("C:C"))
    For i = 2 To ResultCount
        For j = 2 To SourceCount
            If SheetResult.Cells(i, 9).Value = SheetSource.Cells(j, 1).Value Then
                SheetResult.Cells(i, 7).Value = SheetSource.Cells(j, 3).Value
                SheetResult.Cells(i, 7).HorizontalAlignment = xlCenter
                If j > stockEndIndex Then
                    SheetResult.Cells(i, 7).Interior.Color = 26367 '天天基金橙色
                ElseIf j <= stockEndIndex Then
                    SheetResult.Cells(i, 7).Interior.Color = 255   '股票账户红色
                'Else
                '    SheetResult.Cells(i, 11).Interior.Color = 15773696   '支付宝账户蓝色
                End If
            End If
        Next
    Next
End Sub

Sub ★更新基金净值与指数估值()
    
    Set SheetSource = Sheets("且慢估值与基金净值")
    Set SheetResult = Sheets("交易明细")
    '净值更新
    SheetResult.Range("S15:S43") = SheetSource.Range("D1:D29").Value
    SheetResult.Range("S15:S43").NumberFormatLocal = "0.0000"
    SheetResult.Range("S15:S43").HorizontalAlignment = xlCenter
    SheetResult.Range("S15:S43").Interior.Color = 65535
    SheetResult.Range("S15:S43").Select
    
    'PE
    SheetResult.Range("T15:T32") = SheetSource.Range("B31:B48").Value
    SheetResult.Range("T15:T32").NumberFormatLocal = "0.00"
    SheetResult.Range("T15:T32").HorizontalAlignment = xlCenter
    SheetResult.Range("T15:T32").Interior.Color = 65535
    SheetResult.Range("T15:T32").Select
    
    'PB
    SheetResult.Range("V15:V32") = SheetSource.Range("C31:C48").Value
    SheetResult.Range("V15:V32").NumberFormatLocal = "0.00"
    SheetResult.Range("V15:V32").HorizontalAlignment = xlCenter
    SheetResult.Range("V15:V32").Interior.Color = 65535
    SheetResult.Range("V15:V32").Select
End Sub

