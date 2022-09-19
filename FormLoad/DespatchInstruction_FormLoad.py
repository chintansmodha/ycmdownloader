from Global_Files import Connection_String as con
from django.shortcuts import render

GDataItemCode = []
GDataCompanyCode = []
GDataAgentCode = []
GDataItmCode = []
GDataShadeCode = []
GDataGradeCode = []
GDataPartyCode = []
GDataAgentGroupCode = []

stmt = con.db.exec_immediate(con.conn, "select CODE,Longdescription from division ")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompanyCode:
        GDataCompanyCode.append(result)
    result = con.db.fetch_both(stmt)

stmt1 = con.db.exec_immediate(con.conn, "select CODE,Longdescription from itemtype ")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in GDataItemCode:
        GDataItemCode.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt2 = con.db.exec_immediate(con.conn, "select CODE,Longdescription from AGENT ")
result2 = con.db.fetch_both(stmt2)
while result2 != False:
    if result2 not in GDataAgentCode:
        GDataAgentCode.append(result2)
    result2 = con.db.fetch_both(stmt2)

stmt3 = con.db.exec_immediate(con.conn, "select ITEMTYPECODE,Longdescription from Product ")
result3 = con.db.fetch_both(stmt3)
while result3 != False:
    if result3 not in GDataItmCode:
        GDataItmCode.append(result3)
    result3 = con.db.fetch_both(stmt3)

stmt4 = con.db.exec_immediate(con.conn, "select CODE,Longdescription from USERGENERICGROUP ")
result4 = con.db.fetch_both(stmt4)
while result4 != False:
    if result4 not in GDataShadeCode:
        GDataShadeCode.append(result4)
    result4 = con.db.fetch_both(stmt4)

stmt5 = con.db.exec_immediate(con.conn, "select CODE,Longdescription from QUALITYLEVEL ")
result5 = con.db.fetch_both(stmt5)
while result5 != False:
    if result5 not in GDataGradeCode:
        GDataGradeCode.append(result5)
    result5 = con.db.fetch_both(stmt5)

stmt6 = con.db.exec_immediate(con.conn, "select LEGALNAME1 from BUSINESSPARTNER ")
result6 = con.db.fetch_both(stmt6)
while result6 != False:
    if result6 not in GDataPartyCode:
        GDataPartyCode.append(result6)
    result6 = con.db.fetch_both(stmt6)

stmt7 = con.db.exec_immediate(con.conn, "select CODE,Longdescription from AGENTSGROUP ")
result7 = con.db.fetch_both(stmt7)
while result7 != False:
    if result7 not in GDataAgentGroupCode:
        GDataAgentGroupCode.append(result7)
    result7 = con.db.fetch_both(stmt7)

def DespatchInstructionRegisterHtml(request):
    return render(request, 'DespatchInstructionRegister.html', {'GDataItemCode': GDataItemCode, 'GDataCompanyCode': GDataCompanyCode})

def PendingDespatchInstructionHtml(request):
    return render(request, 'PendingDespatchInstruction.html', {'GDataItemCode': GDataItemCode, 'GDataCompanyCode': GDataCompanyCode,
                                                     'GDataAgentCode': GDataAgentCode, 'GDataItmCode': GDataItmCode,
                                                       'GDataShadeCode': GDataShadeCode, 'GDataGradeCode': GDataGradeCode,
                                                        'GDataPartyCode': GDataPartyCode, 'GDataAgentGroupCode': GDataAgentGroupCode})

