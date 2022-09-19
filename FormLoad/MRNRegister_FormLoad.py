from django.shortcuts import render
from Global_Files import Connection_String as con

GDataDepartment=[]
GDataSupplier=[]
GDataItemType=[]
GDataItem=[]
GDataItemconcate=[]
GDataItemconcatemrn=[]

ITEMTYPECODE=[]
ITEMTYPEAFICODE=[]

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from COSTCENTER order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataDepartment:
        GDataDepartment.append(result)
    result = con.db.fetch_both(stmt)

stmt1 = con.db.exec_immediate(con.conn,"select NUMBERID,Legalname1 from BUSINESSPARTNER order by Legalname1")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in GDataSupplier:
        GDataSupplier.append(result1)
    result1 = con.db.fetch_both(stmt1)

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from ITEMTYPE order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataItemType:
        GDataItemType.append(result)
    result = con.db.fetch_both(stmt)

stmt1 = con.db.exec_immediate(con.conn,"select LONGDESCRIPTION,COALESCE(ITEMTYPECODE,'')||COALESCE(SubCode01,'')"
                                       "||COALESCE(SubCode02,'')||COALESCE(SubCode03,'')||COALESCE(SubCode04,'')"
                                       "||COALESCE(SubCode05,'')||COALESCE(SubCode06,'')||COALESCE(SubCode07,'')"
                                       "||COALESCE(SubCode08,'')||COALESCE(SubCode09,'')||COALESCE(SubCode10,'') as ITEMTYPECODE "
                                       "from Product order by LONGDESCRIPTION")
result1 = con.db.fetch_both(stmt1)
while result1 != False:
    if result1 not in GDataItemconcate:
        GDataItem.append(result1)

        # ITEMTYPECODE.append(result1['2'])
    result1 = con.db.fetch_both(stmt1)

def MRNRegisterHtml(request):
    return render(request,'MRNRegister.html',{'GDataDepartment':GDataDepartment,'GDataSupplier':GDataSupplier,'GDataItemType':GDataItemType, 'GDataItem':GDataItem})
