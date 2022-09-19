from django.shortcuts import render
from Global_Files import Connection_String as con

Exceptions = ''

GDataIssueNoteSummary = []
GDataDepartment = []
GDataToDepartment = []

stmt = con.db.exec_immediate(con.conn,"select code,LONGDESCRIPTION  from LOGICALWAREHOUSE order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataDepartment:
        GDataDepartment.append(result)
    result = con.db.fetch_both(stmt)


def PrintIssueNoteHtml(request):
    return render(request, 'PrintIssueNote.html',
                  {'GDataDepartment': GDataDepartment, 'GDataToDepartment': GDataDepartment })


def PrintIssueNote(request):
    return render(request, 'PrintIssueNote_Table.html',
                  {'GDataDepartment': GDataDepartment, 'GDataToDepartment': GDataDepartment})