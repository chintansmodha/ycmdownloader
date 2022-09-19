from Global_Files import Connection_String as con
from datetime import datetime
from ProcessSelection import BrokerGroupCompanyWiseOS_ProcessSelection as BGCV
from PrintPDF import BrokerGroupCompanyWiseOS_PrintPDF as pdfrpt
counter=0
new=0
GDataCummAmt=[]
def BrokerGroupCompanyWiseOS_PrintPDF(LSCompany,LSBroker,LSBrokerGroup,LCCompany,LCBroker,LCBrokerGroup,LDStartDate,LDEndDate,LSFileName):
    global GDataCummAmt
    global new
    new=0
    GDataCummAmt=[]
    # company=str(LSCompany)
    # broker=str(LSBroker)
    # brokergrp=str(LSBrokerGroup)
    # stdate = str(LDStartDate)
    # etdate = str(LDEndDate)
    # LSCompanys = '(' + company[1:-1] + ')'
    # LSBrokers = '(' + broker[1:-1] + ')'
    # LSBrokerGroups = '(' + brokergrp[1:-1] + ')'

    if not LCCompany and not LSCompany:
        Company=""
    elif LCCompany:
        Company=" "
    elif LSCompany:
        Company = "AND BU.Code in (" + str(LSCompany)[1:-1]+")"

    if not LCBroker and not LSBroker:
        Broker=""
    elif LCBroker:
        Broker=" "
    elif LSBroker:
        Broker = "AND Agnt.Code in (" + str(LSBroker)[1:-1]+")"

    if not LCBrokerGroup and not LSBrokerGroup:
        Brokergrp=""
    elif LCBrokerGroup:
        Brokergrp=" "
    elif LSBrokerGroup:
        Brokergrp = "AND AgGrp.Code in (" + str(LSBrokerGroup)[1:-1]+")"
    print(Company,Brokergrp,Broker)
    sql="SELECT  Company.Longdescription AS Company " \
        " , PI.Code AS INVNO" \
        " , AgGrp.Longdescription AS BrokerGroup" \
        " , Agnt.LONGDESCRIPTION AS Broker" \
        " , VARCHAR_FORMAT(PI.INVOICEDATE, 'DD-MM-YYYY') AS ISSUEDATE" \
        " , PI.TERMSOFPAYMENTCODE AS DAYS" \
        " , BusinessPartner.legalname1 AS Party" \
        " , days (current date) - days (FD.DUEDATE) AS OD" \
        " , cast(PI.NETTVALUE as decimal(18,2)) AS INVAMT" \
        " , cast(PI.NETTVALUE as decimal(18,2)) AS OSAMT" \
        " , cast(PI.NETTVALUE as decimal(18,2)) AS CUMAMT" \
        " FROM    PlantInvoice PI" \
        " JOIN    BUSINESSUNITVSCOMPANY BC        ON PI.FACTORYCODE = BC.FACTORYCODE " \
        " JOIN    FinBusinessUnit BU              ON BC.BUSINESSUNITCODE = BU.Code" \
        " JOIN    FinBusinessUnit Company         ON BU.GroupbuCode = Company.Code" \
        " JOIN    AgentsGroupDetail AGD           ON PI.Agent1Code = AGD.AgentCode" \
        " JOIN    Agent       Agnt                ON PI.AGENT1CODE = Agnt.CODE" \
        " JOIN    AgentsGroup AgGrp               ON AGD.AgentsGroupCode = AgGrp.Code" \
        " JOIN    FinDocument FD                  ON PI.FINDOCBUSINESSUNITCODE = FD.BUSINESSUNITCODE" \
        " AND PI.FINDOCFINANCIALYEARCODE = FD.FINANCIALYEARCODE" \
        " AND PI.FINDOCTEMPLATECODE = FD.DOCUMENTTEMPLATECODE" \
        " AND PI.FINDOCCODE = FD.CODE" \
        " JOIN SalesDocument SD                   ON PI.CODE = SD.PROVISIONALCODE" \
        " JOIN OrderPartner As OrderPartner       ON SD.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode" \
        " AND OrderPartner.CustomerSupplierType = 1" \
        " JOIN BusinessPartner                    ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId" \
        " Where   PI.FINDOCBUSINESSUNITCODE Is Not Null And PI.FINDOCFINANCIALYEARCODE Is Not Null" \
        " AND PI. FINDOCTEMPLATECODE Is Not Null And  PI.FINDOCCODE Is Not Null" \
        " AND  days (current date) - days (FD.DUEDATE) and PI.INVOICEDATE BETWEEN '" + LDStartDate + "' " +"and" +" '" + LDEndDate + "' " + Company + " " + Broker + " " + Brokergrp + " "\
        " GROUP BY PI.Code, PI.INVOICEDATE, PI.INVOICEDATE,days (current date) - days (FD.DUEDATE),PI.NETTVALUE,PI.NETTVALUE,BusinessPartner.legalname1," \
        " Company.Longdescription,AgGrp.Longdescription,FD.DUEDATE ,PI.TERMSOFPAYMENTCODE,Agnt.LONGDESCRIPTION" \
        " ORDER BY BrokerGroup,Broker,Company,ISSUEDATE,INVNO"
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    # con.db.bind_param(stmt, 1, stdt)
    # con.db.bind_param(stmt, 2, etdt)

    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    if result==False:
        BGCV.Exceptions = "Note: No Result found according to your selected criteria "
        return
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d,stdt,etdt)
        pdfrpt.d=pdfrpt.dvalue(stdt,etdt,result,pdfrpt.divisioncode)
        result = con.db.fetch_both(stmt)

        if pdfrpt.d<20:
            pdfrpt.d=560
            pdfrpt.c.showPage()
            pdfrpt.header(stdt,etdt,result,pdfrpt.divisioncode)

    if result == False:
        if counter > 0:
            pdfrpt.fonts(7)
            # if pdfrpt.count > 0:
            #     pdfrpt.printdivisiontotal()
            pdfrpt.count = 0
            pdfrpt.boldfonts(8)
            pdfrpt.printdivisiontotallast()
            pdfrpt.d = pdfrpt.dvalue(stdt, etdt, result, pdfrpt.divisioncode)
            pdfrpt.printbrokertotallast()
            pdfrpt.d = pdfrpt.dvalue(stdt, etdt, result, pdfrpt.divisioncode)
            pdfrpt.printbrokergrptotallast()
            pdfrpt.d = pdfrpt.dvalue(stdt, etdt, result, pdfrpt.divisioncode)
            BGCV.Exceptions = ""
        elif counter==0:
            BGCV.Exceptions="Note: No Result found according to your selected criteria "
            return
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    counter = 0
    pdfrpt.d = pdfrpt.newpage()