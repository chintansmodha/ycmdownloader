from datetime import datetime
from Global_Files import Connection_String as con
from PrintPDF import PartyWiseBookDebits_PrintPDF as pdfrpt

def PartyWiseBookDebits_GetData(LSCompany,LSAllCompany,LSParty,LSAllParty,LDDate,LS1,LS2,LS3):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = " "
    elif LSCompany:
        LSCompany = " AND FINBUSINESSUNIT.CODE in (" + str(LSCompany)[1:-1] + ")"

    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = " "
    elif LSParty:
        LSParty = " AND BUSINESSPARTNER.NUMBERID in (" + str(LSParty)[1:-1] + ")"
    print(LS1,LS2,LS3)
    if not LS1:
        LS1='0'
    else:
        pass
    if  not LS2:
        LS2='0'
    else:
        pass
    if not LS3:
        LS3='0'
    else:
        pass


    sql =("Select BrokerGrpOS.Company, BrokerGrpOS.BrokerGrp, "
         "Sum(BrokerGrpOS.Between1) As Between1,Sum(BrokerGrpOS.Between2) As Between2,Sum(BrokerGrpOS.Between3) As Between3 "
         ", Sum(BrokerGrpOS.Over4) As Over4 "
         "From ( "
"Select  Company.LongDescription As Company "
        ",BusinessPartner.legalname1 As BrokerGrp "
        ",cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as Between1 "
        ",cast(0 as decimal(18,2)) as Between2 "
        ",cast(0 as decimal(18,2)) as Between3 "
        ",cast(0 as decimal(18,2)) as Over4 "
 "from FinOpendocuments as FOD "
   "JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE "
   "JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE "
   "join OrderPartner As OrderPartner         on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode  "
        "And                                     FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType  "
        "Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId  "
 "Where DocumentTypeCode in('SD') "
                                "AND FinancialYearCode ='2023' "
                                "And AmountinCC-ClearedAmount>0 "
                                "AND days (current date) - days (POSTINGDATE) between 1 and "+LS1+" "
 " Group By Company.LongDescription,BusinessPartner.legalname1 "
 "Union All "
 "Select  Company.LongDescription As Company "
        ",BusinessPartner.legalname1 As BrokerGrp "
        ",cast(0 as decimal(18,2)) as Between1 "
        ",cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as Between2 "
        ",cast(0 as decimal(18,2)) as Between3 "
        ",cast(0 as decimal(18,2)) as Over4 "
 "from FinOpendocuments as FOD "
  "JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE "
  "JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE "
"join OrderPartner As OrderPartner         on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode  "
        "And                                     FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType  "
        "Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId "
 "Where DocumentTypeCode in('SD') "
                                "AND FinancialYearCode ='2023' "
                                "And AmountinCC-ClearedAmount>0 "
                                "AND days (current date) - days (POSTINGDATE) between "+str(int(LS1)+1)+" and "+LS2+""
  " Group By Company.LongDescription,BusinessPartner.legalname1 "
 "Union All "
 "Select  Company.LongDescription As Company "
        ",BusinessPartner.legalname1 As BrokerGrp "
        ",cast(0 as decimal(18,2)) as Between1 "
        ",cast(0 as decimal(18,2)) as Between2 "
        ",cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as Between3 "
        ",cast(0 as decimal(18,2)) as Over4 "
 "from FinOpendocuments as FOD "
   "JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE "
   "JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE "
"join OrderPartner As OrderPartner         on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode  "
        "And                                     FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType  "
        "Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId "
 "Where DocumentTypeCode in('SD') "
                                "AND FinancialYearCode ='2023' "
                                "And AmountinCC-ClearedAmount>0 "
                                "AND days (current date) - days (POSTINGDATE) between "+str(int(LS2)+1)+" and "+LS3+""
  " Group By Company.LongDescription,BusinessPartner.legalname1 "
 "Union All "
 "Select  Company.LongDescription As Company "
        ",BusinessPartner.legalname1 As BrokerGrp "
        ",cast(0 as decimal(18,2)) as Between1 "
        ",cast(0 as decimal(18,2)) as Between2 "
        ",cast(0 as decimal(18,2)) as Between3 "
        ",cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as Over4 "
 "from FinOpendocuments as FOD "
   "JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE "
   "JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE "
"join OrderPartner As OrderPartner         on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode  "
        "And                                     FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType  "
        "Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId "
 "Where DocumentTypeCode in('SD') "
                                "AND FinancialYearCode ='2023' "
                                "And AmountinCC-ClearedAmount>0 "
                                "AND days (current date) - days (POSTINGDATE) > "+LS3+" "
  " Group By Company.LongDescription,BusinessPartner.legalname1) as BrokerGrpOS "
  " Group bY BrokerGrpOS.Company, BrokerGrpOS.BrokerGrp "
  " Order By BrokerGrpOS.Company, BrokerGrpOS.BrokerGrp ")
    
    print(sql)
    etdt=""
    stdt = datetime.strptime(LDDate, "%Y-%m-%d").date()
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    if result == False:
        return
    while result != False:
       pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt,etdt,LS1,LS2,LS3)
       pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode,result,LS1,LS2,LS3)
       result = con.db.fetch_both(stmt)
    
    pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode,result,LS1,LS2,LS3)
    pdfrpt.c.drawString(10, pdfrpt.d, str(pdfrpt.divisioncode[-1]) + " TOTAL : ")
    
    pdfrpt.c.drawAlignedString(560, pdfrpt.d, str("%.2f" % float(pdfrpt.CompanyAmountTotal)))  
    pdfrpt.c.showPage()
    pdfrpt.c.save()
   
    pdfrpt.newrequest()
    pdfrpt.d = pdfrpt.newpage()

    