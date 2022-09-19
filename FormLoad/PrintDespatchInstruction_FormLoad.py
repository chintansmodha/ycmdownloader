from django.shortcuts import render
from Global_Files import Connection_String as con
from ProcessSelection import PrintDespatchInstruction_ProcessSelection as PDIPD
LDStartDate = ''
LDEndDate = ''
GDataItemType=[]

stmt = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from ITEMTYPE order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataItemType:
        GDataItemType.append(result)
    result = con.db.fetch_both(stmt)

def PrintDespatchInstructionHtml(request):
    return render(request,'PrintDespatchInstruction.html',{'GDataItemType':GDataItemType})

def PrintDespatchInstructionTableHtml(request):
    global LDStartDate
    global LDEndDate
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    return render(request,'PrintDespatchInstructionTable.html')
