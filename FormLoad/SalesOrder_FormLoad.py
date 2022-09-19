from django.shortcuts import render
from Global_Files import Connection_String as con
GDataDocumentType=[]
GDataDivision=[]
GDataTemplate=[]
GDataAgent=[]
GDataParty=[]

def SalesOrderHtml(request):
    global GDataAgent
    global GDataDivision
    global GDataDocumentType
    global GDataParty
    global GDataTemplate
    GDataDocumentType=[]
    GDataDivision=[]
    GDataTemplate=[]
    GDataAgent=[]
    GDataParty=[]
    
    stmt = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from Division order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataDivision:
            GDataDivision.append(result)
        result = con.db.fetch_both(stmt)

    stmt1 = con.db.exec_immediate(con.conn,"select DOCUMENTTYPETYPE from SalesOrder order by DOCUMENTTYPETYPE")
    result1 = con.db.fetch_both(stmt1)
    while result1 != False:
        if result1 not in GDataDocumentType:
            GDataDocumentType.append(result1)
        result1 = con.db.fetch_both(stmt1)

    stmt = con.db.exec_immediate(con.conn,"select TEMPLATECODE from SalesOrder order by TEMPLATECODE")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataTemplate:
            GDataTemplate.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,"select CODE, LONGDESCRIPTION from Agent order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataAgent:
            GDataAgent.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,"select NumberID, LegalName1 from BusinessPartner order by LegalName1")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataParty:
            GDataParty.append(result)
        result = con.db.fetch_both(stmt)
    print(GDataDivision)
    return render(request,'SalesOrder.html', {'GDataDivision':GDataDivision,'GDataAgent':GDataAgent,"GDataParty":GDataParty,"GDataDocumentType":GDataDocumentType,"GDataTemplate":GDataTemplate})