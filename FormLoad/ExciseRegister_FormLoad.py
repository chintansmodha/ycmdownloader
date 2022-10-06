from django.shortcuts import render
from Global_Files import Connection_String as con
GDataParty=[]
GDataCompanyCode=[]
GDataChallanType=[]
GDataCharges=[]
GDataDepartment=[]
GDataItemType=[]




def ExciseRegister(request):
   global GDataChallanType
   global GDataCharges
   global GDataCompanyCode
   global GDataDepartment
   global GDataItemType
   global GDataParty
   GDataParty=[]
   GDataCompanyCode=[]
   GDataChallanType=[]
   GDataCharges=[]
   GDataDepartment=[]
   GDataItemType=[]
   
   stmt = con.db.exec_immediate(con.conn,"select NUMBERID,Legalname1 from BUSINESSPARTNER order by Legalname1")
   result = con.db.fetch_both(stmt)
   while result != False:
      if result not in GDataParty:
         GDataParty.append(result)
         result = con.db.fetch_both(stmt)

   stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from PLANT order by LONGDESCRIPTION")
   result = con.db.fetch_both(stmt)
   while result != False:
      if result not in GDataCompanyCode:
         GDataCompanyCode.append(result)
         result = con.db.fetch_both(stmt)

   stmt = con.db.exec_immediate(con.conn,"select DISTINCT TAXTEMPLATECODE from plantinvoice order by TAXTEMPLATECODE")
   result = con.db.fetch_both(stmt)
   while result != False:
      if result not in GDataChallanType:
         GDataChallanType.append(result)
         result = con.db.fetch_both(stmt)

   stmt = con.db.exec_immediate(con.conn,"select code,longdescription from itax order by longdescription")
   result = con.db.fetch_both(stmt)
   while result != False:
      if result not in GDataCharges:
         GDataCharges.append(result)
         result = con.db.fetch_both(stmt)

   stmt = con.db.exec_immediate(con.conn,"select code,longdescription from costcenter order by longdescription")
   result = con.db.fetch_both(stmt)
   while result != False:
      if result not in GDataDepartment:
         GDataDepartment.append(result)
         result = con.db.fetch_both(stmt)
         
   stmt = con.db.exec_immediate(con.conn,"select code,longdescription from itemtype order by longdescription")
   result = con.db.fetch_both(stmt)
   while result != False:
      if result not in GDataItemType:
         GDataItemType.append(result)
         result = con.db.fetch_both(stmt)

   return render(request,"ExciseRegister.html",{'GDataItemType':GDataItemType,'GDataDepartment':GDataDepartment,
   'GDataParty':GDataParty,'GDataCompanyCode':GDataCompanyCode,'GDataChallanType':GDataChallanType,
   'GDataCharges':GDataCharges}) 