import re
from django.shortcuts import render
from Global_Files import Connection_String as con

GData151630 = [
    "Invoice No",
    "Issue Date",
    "Due Date",
    "O/D",
    "Invoice Amt",
    "O/S Amt",
    "Cum.Amt",
    "Despatch",
    "Party",
    "Challan No",
]
GDataDnAmt = ["Vch.No", "Vch.Date", "Ammount", "O/S Amt", "Cum.Amt", "Party"]
amount = 0
new = 0
Heading = ""
Bills = 0
Company = ""
Broker = ""
GDataUpto15 = []
GDataRange16 = []
GDataOver30 = []
GDataDnAmmt = []
GDataUnbilled = []
GDataAdvance = []
GDataUnAdj = []
GDataOdDay = []
Unadj = 0


def BrokerWiseOSDetail(request):
    global Heading
    global Bills
    global Company
    global Broker
    global new
    global amount
    global Unadj
    amount = 0
    new = 0
    Bills = 0
    Company = ""
    Broker = ""
    Heading = ""
    global GDataUpto15
    global GDataRange16
    global GDataOver30
    global GDataDnAmmt
    global GDataUnbilled
    global GDataOdDay
    global GDataUnAdj
    GDataUpto15 = []
    GDataRange16 = []
    GDataOver30 = []
    GDataDnAmmt = []
    GDataUnbilled = []
    GDataOdDay = []
    GDataUnAdj = []

    if int(request.GET["up15"]) == 1 or int(request.GET["rg16"])==1 or int(request.GET["ov30"])==1:
        if int(request.GET["up15"]) == 1:
            Head="Upto15"
            Cond="<= 15"
        if int(request.GET["rg16"]) == 1:
            Head="16-30"
            Cond="between 16 and 30"
        if int(request.GET["ov30"]) == 1:
            Head="Over30"
            Cond="> 30"
        Heading = "Broker Wise OS "+Head
        LSCompanyCode = request.GET["companycode"]
        LSBrokerCode = request.GET["brokercode"]
        # LSUpto15 = request.GET["upto15"]
        LSCompanyCode = " And    Company.code = " + "'" + LSCompanyCode + "'"
        LSBrokerCode = " And     AgGrp.code = " + "'" + LSBrokerCode + "'"
        sql = (
            "Select  PI.Code as INVNO, VARCHAR_FORMAT(PI.INVOICEDATE, 'DD-MM-YYYY') as ISSUEDATE, "
"             VARCHAR_FORMAT(FD.DUEDATE, 'DD-MM-YYYY') as DUEDATE,"
"             days (current date) - days (FD.DUEDATE) as OD, cast(FOD.AMOUNTINCC as decimal(18,2)) AS INVAMT,"
"             cast((FOD.AmountinCC-FOD.CLEAREDAMOUNT) as decimal(18,2)) As OSAMT,"
"             COALESCE(BusinessPartner.DISTRICT,'') As Despatch,BusinessPartner.legalname1 As Party,"
"             Company.Longdescription As Company ,AgGrp.Longdescription AS Broker,"
"             SDL.PREVIOUSCODE as challanno"
"             from FinOpendocuments as FOD"
"                JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"                JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"                Join PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                 And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                 And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                 And FOD.CODE = PI.FINDOCCODE "
"             Join    AgentsGroupDetail AGD   On      PI.Agent1Code = AGD.AgentCode "
"             Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code "
"             Join FinDocument FD on FOD.BUSINESSUNITCODE = FD.BUSINESSUNITCODE"
"             And FOD.FINANCIALYEARCODE = FD.FINANCIALYEARCODE"
"             And FOD.DOCUMENTTEMPLATECODE = FD.DOCUMENTTEMPLATECODE "
"             And FOD.CODE = FD.CODE"
"             Join SalesDocument SD On PI.CODE = SD.PROVISIONALCODE"
"             JOIN SalesDocumentLine SDL ON SD.PROVISIONALCODE=SDL.SALESDOCUMENTPROVISIONALCODE"
"             AND  SD.PROVISIONALCOUNTERCODE=SDL.SALDOCPROVISIONALCOUNTERCODE"
"             AND  SD.DOCUMENTTYPETYPE='06'"
"             join OrderPartner As OrderPartner         on SD.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode"
"             And OrderPartner.CustomerSupplierType = 1"
"             Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId"
"             Where   PI.FINDOCBUSINESSUNITCODE Is Not Null And PI.FINDOCFINANCIALYEARCODE Is Not Null"
"             And PI. FINDOCTEMPLATECODE Is Not Null And  PI.FINDOCCODE Is Not Null"
"             AND days (current date) - days (FOD.POSTINGDATE) " +Cond+LSCompanyCode+LSBrokerCode+""
        )
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        print(result)
        while result != False:
            new = new + round(float(result["INVAMT"]), 2)
            result["CUMAMT"] = round(new, 2)
            GDataUpto15.append(result)
            result = con.db.fetch_both(stmt)

        if len(GDataUpto15) > 0:
            Bills = len(GDataUpto15)
            Company = GDataUpto15[0]["COMPANY"]
            Broker = GDataUpto15[0]["BROKER"]
        return render(
            request,
            "BrokerWiseOSUpto15.html",
            {
                "Header": GData151630,
                "Heading": Heading,
                "GDataUpto15": GDataUpto15,
                "Bills": Bills,
                "Company": Company,
                "Broker": Broker,
                "OsAmt": round(new, 2),
            },
        )

    if int(request.GET["dna"]) == 1:
        Heading = "Broker Wise OS DnAmt"
        LSCompanyCode = request.GET["companycode"]
        LSBrokerCode = request.GET["brokercode"]
        LIDnAmt = request.GET["dnamt"]
        LSCompanyCode = " And    Company.code = " + "'" + LSCompanyCode + "'"
        LSBrokerCode = " And     AgGrp.code = " + "'" + LSBrokerCode + "'"
        year=request.GET['year']
        sql = (
            " Select  Company.LongDescription As Company "
"         ,AgGrp.LongDescription As BrokerGrp "
"         ,Company.Code As CompanyCode "
"         ,AgGrp.Code As BrokerCode "
"         ,cast(FD.DOCUMENTAMOUNT as decimal(18,2)) as Amount,cast((FOD.AMOUNTINCC-FOD.CLEAREDAMOUNT) as decimal(18,2)) as DNamt "
" ,BusinessPartner.legalname1 as Party"
" ,FD.Code as FINNO,VARCHAR_FORMAT(FD.FINANCEDOCUMENTDATE, 'DD-MM-YYYY') as FINDATE"
"   from FinOpendocuments as FOD "
"   JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE "
"   JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE "
" Join    OrderPartner            On      FOD.ORDERPARTNERTYPE = OrderPartner.CUSTOMERSUPPLIERTYPE "
" And     FOD.ORDERPARTNERCODE =OrderPartner.CUSTOMERSUPPLIERCODE "
" Join    BusinessPartner         On      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID "
"   JOIN FinDocument FD            on FOD.BUSINESSUNITCODE=FD.BUSINESSUNITCODE  "
"                                  And  FOD.FINANCIALYEARCODE=FD.FINANCIALYEARCODE "
"                                  And FOD.DOCUMENTTEMPLATECODE = FD.DOCUMENTTEMPLATECODE  "
"                                  And FOD.CODE = FD.CODE       "
"   JOIN    AgentsGroupDetail AGD    On      FD.Agent1Code = AGD.AgentCode "
"   JOIN    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code "

"  Where FOD.DocumentTypeCode in('CD') "
"                                 AND FOD.FinancialYearCode ='"+year+"'"+LSCompanyCode+LSBrokerCode+""
"                                 And FOD.AMOUNTINCC-FOD.ClearedAmount>0 ")

        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        while result != False:
            new = new + float(result["DNAMT"])
            result["CUMAMT"] = new
            GDataDnAmmt.append(result)
            result = con.db.fetch_both(stmt)

        if len(GDataDnAmmt) > 0:
            Bills = len(GDataDnAmmt)
            Company = GDataDnAmmt[0]["COMPANY"]
            Broker = GDataDnAmmt[0]["BROKERGRP"]
        return render(
            request,
            "BrokerWiseOSDnAmt.html",
            {
                "Header": GDataDnAmt,
                "Heading": Heading,
                "GDataUpto15": GDataDnAmmt,
                "Bills": Bills,
                "Company": Company,
                "Broker": Broker,
                "OsAmt": round(new, 2),
            },
        )

    if int(request.GET["unb"]) == 1:
        Heading = "Broker Wise OS Unbilled"
        LSCompanyCode = request.GET["companycode"]
        LSBrokerCode = request.GET["brokercode"]
        LSCompanyCode = " And    Company.code = " + "'" + LSCompanyCode + "'"
        LSBrokerCode = " And     AgGrp.code = " + "'" + LSBrokerCode + "'"
        sql = (
            " Select Company.LongDescription As Company "
"                 ,AgGrp.LongDescription As BrokerGrp, "
"              Company.Code As CompanyCode "
"              ,AgGrp.Code As BrokerCode "
"              ,SD.PROVISIONALCODE as INVNO,VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') As DUEDATE "
"              ,VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') As ISSUEDATE "
"              ,days (current date) - days (SD.PROVISIONALDOCUMENTDATE) As OD "
"              ,cast(Sum(SD.ONDOCUMENTTOTALAMOUNT - 0)as decimal(18,2)) AS INVAMT "
"              ,cast(Sum(SD.ONDOCUMENTTOTALAMOUNT - 0)as decimal(18,2)) AS OSAMT "
"              ,BusinessPartner.Legalname1 As Party "
"              ,COALESCE(BusinessPartner.DISTRICT,'') As Despatch "
"              From    SalesDocument SD "
"              join OrderPartner As OrderPartner on SD.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode "
"              And OrderPartner.CustomerSupplierType = 1 "
"              Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId "
"              JOIN BusinessUnitVsCompany BUC  ON      SD.DivisionCode   = BUC.DivisionCode "
"              JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode = BUnit.Code And BUnit.GroupFlag = 0 "
"              JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code And Company.GroupFlag = 1 "
"              Join    AgentsGroupDetail AGD   On      SD.AGENT1CODE = AGD.AgentCode "
"              Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code "
"              Where   SD.DOCUMENTTYPETYPE In ('05')" + LSCompanyCode + LSBrokerCode +  ""
"              And SD.INVOICEEVOLUTIONTYPE = '1' "
"              group by Company.LongDescription,AgGrp.LongDescription,Company.Code,AgGrp.Code, "
"              SD.ONDOCUMENTTOTALAMOUNT, BusinessPartner.Legalname1,BusinessPartner.DISTRICT, "
"              days (current date) - days (SD.PROVISIONALDOCUMENTDATE),SD.PROVISIONALDOCUMENTDATE,PROVISIONALCODE "
)

        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        print(result)
        while result != False:
            new = new + round(float(result["INVAMT"]), 3)
            result["CUMAMT"] = round(new, 3)
            GDataUnbilled.append(result)
            result = con.db.fetch_both(stmt)

        if len(GDataUnbilled) > 0:
            Bills = len(GDataUnbilled)
            Company = GDataUnbilled[0]["COMPANY"]
            Broker = GDataUnbilled[0]["BROKERGRP"]
        print(len(GDataUnbilled))
        return render(
            request,
            "BrokerWiseOSUnbilled.html",
            {
                "Header": GDataDnAmt,
                "Heading": Heading,
                "GDataUnbilled": GDataUnbilled,
                "Bills": Bills,
                "Company": Company,
                "Broker": Broker,
                "OsAmt": round(new, 2),
            },
        )
    if int(request.GET["odd"]) == 1:
        Heading = "Broker Wise OS > OD Days"
        LSCompanyCode = request.GET["companycode"]
        LSBrokerCode = request.GET["brokercode"]
        LSODDay = request.GET["odday"]
        LSCompanyCode = " And    Company.code = " + "'" + LSCompanyCode + "'"
        LSBrokerCode = " And     AgGrp.code = " + "'" + LSBrokerCode + "'"
        sql = (
            " Select  PI.Code as INVNO "
"         , VARCHAR_FORMAT(PI.INVOICEDATE, 'DD-MM-YYYY') as ISSUEDATE "
"         , VARCHAR_FORMAT(FD.DUEDATE, 'DD-MM-YYYY') as DUEDATE "
"         ,days (current date) - days (FD.DUEDATE) as OD "
"         , cast(PI.NETTVALUE as decimal(18,2)) AS INVAMT "
"         ,cast(PI.NETTVALUE as decimal(18,2)) As OSAMT "
"         ,cast(PI.NETTVALUE as decimal(18,2)) As CUMAMT "
"         ,TRANSPORTZONE.LONGDESCRIPTION As Despatch "
"         ,BusinessPartner.legalname1 As Party,0 As ChallanNo "
"         ,company.Longdescription As Company  "
"         ,AgGrp.Longdescription AS Broker  "
"              From    PlantInvoice PI  "
"              join    BUSINESSUNITVSCOMPANY BC on PI.FACTORYCODE = BC.FACTORYCODE "
"              Join    FinBusinessUnit BU on BC.BUSINESSUNITCODE = BU.Code "
"              Join    FinBusinessUnit Company On BU.GroupbuCode = Company.Code "
"              Join    AgentsGroupDetail AGD   On      PI.Agent1Code = AGD.AgentCode  "
"              Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code  "
"              Join FinDocument FD on PI.FINDOCBUSINESSUNITCODE = FD.BUSINESSUNITCODE "
"              And PI.FINDOCFINANCIALYEARCODE = FD.FINANCIALYEARCODE "
"              And PI.FINDOCTEMPLATECODE = FD.DOCUMENTTEMPLATECODE  "
"              And PI.FINDOCCODE = FD.CODE "
"              Join SalesDocument SD On PI.CODE = SD.PROVISIONALCODE "
"              join OrderPartner As OrderPartner         on SD.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode "
"              And OrderPartner.CustomerSupplierType = 1 "
"              Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId "
"              Left Join Address On BusinessPartner.ABSUNIQUEID = Address.UNIQUEID "
"              And SD.DELIVERYPOINTCODE = Address.CODE "
"              Left Join TRANSPORTZONE On Address.TRANSPORTZONECODE = TRANSPORTZONE.Code "
"              Where   PI.FINDOCBUSINESSUNITCODE Is Not Null And PI.FINDOCFINANCIALYEARCODE Is Not Null "
"              And PI. FINDOCTEMPLATECODE Is Not Null And  PI.FINDOCCODE Is Not Null "
"              And  days (current date) - days (FD.DUEDATE) > 0 "
"              group by PI.Code, PI.INVOICEDATE, PI.INVOICEDATE, "
"              days (current date) - days (FD.DUEDATE),PI.NETTVALUE,PI.NETTVALUE,BusinessPartner.legalname1, "
"              Company.Longdescription,AgGrp.Longdescription,FD.DUEDATE,TRANSPORTZONE.LONGDESCRIPTION "
"              order by INVNO "
        )

        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        while result != False:
            new = new + round(float(result["INVAMT"]), 2)
            result["CUMAMT"] = round(new, 2)
            GDataOdDay.append(result)
            result = con.db.fetch_both(stmt)

        if len(GDataOdDay) > 0:
            Bills = len(GDataOdDay)
            Company = GDataOdDay[0]["COMPANY"]
            Broker = GDataOdDay[0]["BROKER"]
        return render(
            request,
            "BrokerWiseOSUpto15.html",
            {
                "Header": GData151630,
                "Heading": Heading,
                "GDataUpto15": GDataOdDay,
                "Bills": Bills,
                "Company": Company,
                "Broker": Broker,
                "OsAmt": round(new, 2),
            },
        )

    if int(request.GET["una"]) == 1:
        jigar = 0
        Heading = "Broker Wise OS UnAdjusted"
        LSCompanyCode = request.GET["companycode"]
        LSBrokerCode = request.GET["brokercode"]
        Unadj = request.GET["unadj"]
        print(LSBrokerCode, LSCompanyCode, Unadj)
        LSCompanyCode = " And    Company.code = " + "'" + LSCompanyCode + "'"
        LSBrokerCode = " And     AgGrp.code = " + "'" + LSBrokerCode + "'"
        sql = (
            "  Select distinct company.LONGDESCRIPTION as Company "
"                 ,company.Code as CompanyCode "
"             ,VARCHAR_FORMAT(FD.PostingDate, 'YYYY-MM-DD') As VchDate "
"             ,COALESCE(FD.CHEQUENUMBER,CHQN.Valuestring,'') As ChqNo "
"             ,days (current date) - days (FD.DUEDATE) as Day "
"             ,cast(FOD.AMOUNTINCC - FOD.ClearedAmount as Decimal(18,2))  as amount "
"             ,'' as drawer "
"             ,AgGrp.LONGDESCRIPTION as Agent "
"             ,AgGrp.Code as AgentCode "
"             ,FD.Code as FinDocumentCode "
"             ,BusinessPartner.LegalName1 as Party "
"              from Findocument AS FD "
"              Join    FINOpenDocuments FOD On FOD.CODE = FD.Code "
"              AND FOD.BusinessUnitCode = FD.BusinessUnitCode "
"              AND FOD.FinancialYearCode = FD.FinancialYearCode "
"              AND FOD.DocumentTemplateCode = FD.DocumentTemplateCode "
"              AND FOD.DocumentTypeCode = 'BR' "
"              Join    FinDocumentLine      On      FD.BUSINESSUNITCODE = FinDocumentLine.FINDOCUMENTBUSINESSUNITCODE "
"              And     FD.FINANCIALYEARCODE = FinDocumentLine.FINDOCUMENTFINANCIALYEARCODE "
"              And     FD.DOCUMENTTEMPLATECODE = FinDocumentLine.FINDOCDOCUMENTTEMPLATECODE "
"              And     FD.Code = FinDocumentLine.FINDOCUMENTCODE "
"              Join    OrderPartner            On      FinDocumentLine.SLCUSTOMERSUPPLIERTYPE = OrderPartner.CUSTOMERSUPPLIERTYPE "
"              Join    BusinessPartner         On      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID   "
"              And     FinDocumentLine.SLCUSTOMERSUPPLIERCODE =OrderPartner.CUSTOMERSUPPLIERCODE   "
"              Join    FinBusinessUnit BU on FD.BusinessUnitcode = BU.Code "
"              Join    FinBusinessUnit Company On BU.GroupbuCode = Company.Code "
"              JOIN    AgentsGroupDetail AGD           ON FD.Agent1Code = AGD.AgentCode "
"              JOIN    AgentsGroup AgGrp               ON AGD.AgentsGroupCode = AgGrp.Code "
"              LEFT JOIN AdStorage AS CHQN               ON  FD.AbsUniqueId = CHQN.UniqueId "
"              AND CHQN.NameEntityName = 'FINDocument' "
"              And CHQN.NameName = 'CustomerCheque' "
"              And CHQN.FieldName = 'CustomerCheque' "
"              Where FOD.AMOUNTINCC > 0 "
"              AND FOD.AMOUNTINCC - FOD.ClearedAmount <> 0 "
"              And FD.DOCUMENTTYPECODE In ('BR','CR') And FD.DOCUMENTTEMPLATECODE In ('B12','B18')  "
        )

        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        while result != False:
            GDataUnAdj.append(result)
            result = con.db.fetch_both(stmt)
        if len(GDataUnAdj) > 0:
            Bills = len(GDataUnAdj)
            Company = GDataUnAdj[0]["COMPANY"]
            Broker = GDataUnAdj[0]["AGENT"]

        return render(
            request,
            "BrokerWiseOSUnAdj.html",
            {
                "Header": GData151630,
                "Heading": Heading,
                "GDataUnAdj": GDataUnAdj,
                "Bills": Bills,
                "Company": Company,
                "Broker": Broker,
                "OsAmt": round(new, 2),
                "Amount": Unadj,
            },
        )
