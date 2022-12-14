
from datetime import datetime
from Global_Files import Connection_String as con
from PrintPDF import PartyBillOS_PrintPDF as pdfrpt
def GetDataSummary(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate,LDYear):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = " "
    elif LSCompany:
        LSCompany = " AND FINBUSINESSUNIT.CODE in (" + str(LSCompany)[1:-1] + ")"

    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = " "
    elif LSParty:
        LSParty = " AND BUSINESSPARTNER.NUMBERID in (" + str(LSParty)[1:-1] + ")"

    if not LSAllBroker and not LSBroker or LSAllBroker:
        LSBroker = " "
    elif LSBroker:
        LSBroker = " AND AGENT.CODE in (" + str(LSBroker)[1:-1] + ")"

    stdt = datetime.strptime(LDAsOnDate, "%Y-%m-%d").date()
    etdt=""

    sql = ("Select  PI.Code as INVNO"
        ",VARCHAR_FORMAT(PI.INVOICEDATE, 'DD-MM-YYYY') as InvoiceDate "
        ",cast(FOD.AMOUNTINCC as decimal(18,2)) AS INVAMT "
        ",cast((FOD.AmountinCC-FOD.CLEAREDAMOUNT) as decimal(18,2)) As OSAMT "
        ",cast(FDL.AMOuntINCC as decimal(18,2)) as ledbal "
        ",BusinessPartner.legalname1 As Party "
        ",Company.Longdescription As Company  "
        ",AgGrp.Longdescription AS Broker "
       "From FinOpendocuments as FOD "
        "JOIN FINBUSINESSUNIT UNIT       ON      FOD.BUSINESSUNITCODE=UNIT.CODE "
        "JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE "
        "Join PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE  "
                                        "And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE "
                                        "And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE  "
                                        "And FOD.CODE = PI.FINDOCCODE "
        "Join FinDocumentLine  as FDL    ON   FOD.BUSINESSUNITCODE=FDL.FINDOCUMENTBUSINESSUNITCODE  "
                                        "And  FOD.FINANCIALYEARCODE=FDL.FINDOCUMENTFINANCIALYEARCODE "
                                        "And FOD.DOCUMENTTEMPLATECODE = FDL.FINDOCDOCUMENTTEMPLATECODE  "
                                        "And FOD.CODE = FDL.FINDOCUMENTCODE                                          "
        "Join    AgentsGroupDetail AGD   On      PI.Agent1Code = AGD.AgentCode  "
        "Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code  "
        "join OrderPartner As OrderPartner         on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode "
        "And                                     FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType "
        "Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId "
        "Where  FOD.postingdate <= '"+str(stdt)+"' "
        "And    FOD.FINANCIALYEARCODE = '"+LDYear+"' "
        "And    FOD.DOCUMENTTEMPLATECODE = 'S01' "
        "And    (FOD.AmountinCC-FOD.CLEAREDAMOUNT) > 0 " +LSCompany+LSParty+LSBroker+""
"Union All      "
"Select  '' as INVNO "
        ",VARCHAR_FORMAT(FOD.POSTINGDATE, 'DD-MM-YYYY') as InvoiceDate "
        ",cast(FOD.AMOUNTINCC as decimal(18,2)) AS INVAMT "
        ",cast((FOD.AmountinCC-FOD.CLEAREDAMOUNT) as decimal(18,2)) As OSAMT "
        ",cast(FDL.AMOuntINCC as decimal(18,2)) as ledbal "
        ",BusinessPartner.legalname1 As Party "
        ",Company.Longdescription As Company  "
        ",AgGrp.Longdescription AS Broker "
       "From FinOpendocuments as FOD "
        "JOIN FINBUSINESSUNIT UNIT       ON      FOD.BUSINESSUNITCODE=UNIT.CODE "
        "JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE "
        "Join Findocument FD            on FOD.BUSINESSUNITCODE=FD.BUSINESSUNITCODE  "
                                        "And  FOD.FINANCIALYEARCODE=FD.FINANCIALYEARCODE "
                                        "And FOD.DOCUMENTTEMPLATECODE = FD.DOCUMENTTEMPLATECODE  "
                                        "And FOD.CODE = FD.CODE  "
        "Join FinDocumentLine  as FDL    ON   FOD.BUSINESSUNITCODE=FDL.FINDOCUMENTBUSINESSUNITCODE  "
                                        "And  FOD.FINANCIALYEARCODE=FDL.FINDOCUMENTFINANCIALYEARCODE "
                                        "And FOD.DOCUMENTTEMPLATECODE = FDL.FINDOCDOCUMENTTEMPLATECODE  "
                                        "And FOD.CODE = FDL.FINDOCUMENTCODE "
        "Join    AgentsGroupDetail AGD   On      FD.Agent1Code = AGD.AgentCode  "
        "Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code  "
        "join OrderPartner As OrderPartner         on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode "
        "And                                     FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType "
        "Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId "
        "Where  FOD.postingdate <= '"+str(stdt)+"' "
        "And    FOD.FINANCIALYEARCODE = '"+LDYear+"' "
        "And    FOD.DOCUMENTTEMPLATECODE = 'OB' "
        "And    (FOD.AmountinCC-FOD.CLEAREDAMOUNT) > 0 " +LSCompany+LSParty+LSBroker+""
"Union all       "
"Select  '' as INVNO "
        ",VARCHAR_FORMAT(FD.POSTINGDATE, 'DD-MM-YYYY') as InvoiceDate "
        ",cast(FOD.AMOUNTINCC as decimal(18,2)) AS INVAMT "
        ",cast((FODT.CLEAREDAMOUNT) as decimal(18,2)) As OSAMT "
        ",cast(FDL.AMOuntINCC as decimal(18,2)) as ledbal "
        ",BusinessPartner.legalname1 As Party "
        ",Company.Longdescription As Company  "
        ",AgGrp.Longdescription AS Broker "
"From    FinOpendocuments as FOD "
        "JOIN FINBUSINESSUNIT UNIT               ON      FOD.BUSINESSUNITCODE=UNIT.CODE "
        "JOIN FINBUSINESSUNIT Company            ON      UNIT.GROUPBUCODE=Company.CODE "
       "Join Findocument FD            on FOD.BUSINESSUNITCODE=FD.BUSINESSUNITCODE  "
                                        "And  FOD.FINANCIALYEARCODE=FD.FINANCIALYEARCODE "
                                        "And FOD.DOCUMENTTEMPLATECODE = FD.DOCUMENTTEMPLATECODE  "
                                        "And FOD.CODE = FD.CODE  "
        "Join FinDocumentLine  as FDL    ON   FOD.BUSINESSUNITCODE=FDL.FINDOCUMENTBUSINESSUNITCODE  "
                                        "And  FOD.FINANCIALYEARCODE=FDL.FINDOCUMENTFINANCIALYEARCODE "
                                        "And FOD.DOCUMENTTEMPLATECODE = FDL.FINDOCDOCUMENTTEMPLATECODE  "
                                        "And FOD.CODE = FDL.FINDOCUMENTCODE                                         "
        "Join    AgentsGroupDetail AGD   On      FD.Agent1Code = AGD.AgentCode  "
        "Join    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code  "
        "join OrderPartner As OrderPartner       on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode "
                                                "And FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType "
        "Join BusinessPartner                    ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId "
        "Join FinopendocumentsTransactions as FODT "
                                                "ON      FOD.BUSINESSUNITCODE=FODT.ORIGINBUSINESSUNITCODE "
                                                "And     FOD.FINANCIALYEARCODE=FODT.ORIGINFINANCIALYEARCODE "
                                                "And     FOD.DOCUMENTTEMPLATECODE=FODT.ORIGINDOCUMENTTEMPLATECODE "
                                                "And     FOD.CODE=FODT.ORIGINCODE "
"Where FODT.TRANSACTIONDATE > '"+str(stdt)+"' and FOD.postingdate <= '"+str(stdt)+"' "
        "And    FOD.FINANCIALYEARCODE = '"+LDYear+"' "
        "And    FOD.DOCUMENTTEMPLATECODE = 'OB' "
        "And    (FOD.AmountinCC-FOD.CLEAREDAMOUNT) > 0 " +LSCompany+LSParty+LSBroker+""
"Union All   "
"Select  PI.Code as INVNO "
        ",VARCHAR_FORMAT(PI.INVOICEDATE, 'DD-MM-YYYY') as InvoiceDate "
        ",cast(FOD.AMOUNTINCC as decimal(18,2)) AS INVAMT "
        ",cast((FODT.CLEAREDAMOUNT) as decimal(18,2)) As OSAMT "
        ",cast(FDL.AMOuntINCC as decimal(18,2)) as ledbal "
        ",BusinessPartner.legalname1 As Party "
        ",Company.Longdescription As Company  "
        ",AgGrp.Longdescription AS Broker "
"From    FinOpendocuments as FOD "
        "JOIN FINBUSINESSUNIT UNIT               ON      FOD.BUSINESSUNITCODE=UNIT.CODE "
        "JOIN FINBUSINESSUNIT Company            ON      UNIT.GROUPBUCODE=Company.CODE "
        "Join PlantInvoice PI                    on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE  "
                                                "And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE "
                                                "And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE  "
                                                "And FOD.CODE = PI.FINDOCCODE "
        "Join FinDocumentLine  as FDL    ON   FOD.BUSINESSUNITCODE=FDL.FINDOCUMENTBUSINESSUNITCODE  "
                                        "And  FOD.FINANCIALYEARCODE=FDL.FINDOCUMENTFINANCIALYEARCODE "
                                        "And FOD.DOCUMENTTEMPLATECODE = FDL.FINDOCDOCUMENTTEMPLATECODE  "
                                        "And FOD.CODE = FDL.FINDOCUMENTCODE  "
        "Join    AgentsGroupDetail AGD           On      PI.Agent1Code = AGD.AgentCode  "
        "Join    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code  "
        "join OrderPartner As OrderPartner       on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode "
                                                "And FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType "
        "Join BusinessPartner                    ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId "
        "Join FinopendocumentsTransactions as FODT "
                                                "ON      FOD.BUSINESSUNITCODE=FODT.ORIGINBUSINESSUNITCODE "
                                                "And     FOD.FINANCIALYEARCODE=FODT.ORIGINFINANCIALYEARCODE "
                                                "And     FOD.DOCUMENTTEMPLATECODE=FODT.ORIGINDOCUMENTTEMPLATECODE "
                                                "And     FOD.CODE=FODT.ORIGINCODE "
        "Where FODT.TRANSACTIONDATE > '"+str(stdt)+"' and FOD.postingdate <= '"+str(stdt)+"' "
        "And    FOD.FINANCIALYEARCODE = '"+LDYear+"' "
        "And    FOD.DOCUMENTTEMPLATECODE = 'S01' "
        "And    (FOD.AmountinCC-FOD.CLEAREDAMOUNT) > 0 " +LSCompany+LSParty+LSBroker+"")

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    if result == False:
        return
    while result != False:
       pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt,etdt)
       pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode,result)
       result = con.db.fetch_both(stmt)
       
    pdfrpt.c.showPage()
    pdfrpt.c.save()
   
    pdfrpt.newrequest()
    pdfrpt.d = pdfrpt.newpage()