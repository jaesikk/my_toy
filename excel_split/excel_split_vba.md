```visual basic
Function isNum(n As String) As Boolean
    If Asc(n) >= 48 And Asc(n) <= 57 Then ' 숫자
        isNum = True
    Else ' 문자
        isNum = False
    End If
End Function

Sub main()
    Dim dict As Object
    Set dict = CreateObject("Scripting.Dictionary")


    Dim row_num As Integer
    row_num = 1
    
    For Each cell In ActiveSheet.UsedRange
        If Not IsEmpty(cell.Value) Then
            sentence = Split(cell.Value, " ")
            For j = 0 To UBound(sentence)
                Dim tmp_str As String
                Dim tmp_int As String
                tmp_str = ""
                tmp_int = ""
                For k = 1 To Len(sentence(j))
                    If isNum(Mid(sentence(j), k, 1)) Then ' 숫자
                        tmp_int = tmp_int & Mid(sentence(j), k, 1)
                    Else ' 문자
                        tmp_str = tmp_str & Mid(sentence(j), k, 1)
                    End If
                Next k
                If dict.Exists(tmp_str) Then 'dict에 키 값이 있으면
                    dict(tmp_str) = dict(tmp_str) + CInt(tmp_int)
                Else 'dict에 키 값이 없으면
                    dict.Add tmp_str, CInt(tmp_int)
                End If
            Next j
        End If
    Next cell
    
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
    Dim wsName As String
    wsName = "Result" & ThisWorkbook.Worksheets.Count
    ws.Name = wsName
    row_num = 1
    For Each Key In dict.keys
        ws.Cells(row_num, 1).Value = Key
        ws.Cells(row_num, 2).Value = dict(Key)
        row_num = row_num + 1
    Next Key
End Sub
```

