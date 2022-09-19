from django.shortcuts import render
from FormLoad import OSMoreThanDays_FormLoad as views
from Global_Files import Connection_String as con
from PrintPDF import OSMoreThanDays_PrintPDF as pdfrpt
counter=0
cumamt=0
day=0
Exceptions=''
def OSMorethanDays_PrintPDF(Company,BrkGroup,Days,LCCompany,LCBrokerGroup,request):
    global Exceptions
    global cumamt
    global day
    day = Days
    cumamt = 0
    print(Days[-1])
    if not LCCompany and not Company:
        Company = ""
    elif LCCompany:
        Company = " "
    elif Company:
        Company = "AND BU.Code in (" + str(Company)[1:-1] + ")"

    if not LCBrokerGroup and not BrkGroup:
        BrkGroup=""
    elif LCBrokerGroup:
        BrkGroup=" "
    elif BrkGroup:
        BrkGroup = "AND AgGrp.Code in (" + str(BrkGroup)[1:-1]+")"

    sql = " Select  PI.Code as INVNO, PI.INVOICEDATE as ISSUEDATE, FD.DUEDATE as DUEDATE," \
          " days (current date) - days (FD.DUEDATE) as OD," \
          " cast(PI.NETTVALUE as decimal(18,3)) AS INVAMT,cast(PI.NETTVALUE as decimal(18,3)) As OSAMT,cast(PI.NETTVALUE as decimal(18,3)) As CUMAMT," \
          " BusinessPartner.legalname1 As Party,0 As ChallanNo," \
          " Company.Longdescription As Company " \
          " ,AgGrp.Longdescription AS BrokerGrp" \
          " ,Agent.Longdescription as Broker" \
          " , TRANSPORTZONE.LONGDESCRIPTION As Despatch" \
          " From    PlantInvoice PI" \
          " join    BUSINESSUNITVSCOMPANY BC on PI.FACTORYCODE = BC.FACTORYCODE" \
          " Join    FinBusinessUnit BU on BC.BUSINESSUNITCODE = BU.Code" \
          " Join    FinBusinessUnit Company On BU.GroupbuCode = Company.Code" \
          " Join    AgentsGroupDetail AGD   On      PI.Agent1Code = AGD.AgentCode" \
          " Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code" \
          " Join    Agent                   On      AGD.AGENTCODE = Agent.CODE" \
          " Join FinDocument FD on PI.FINDOCBUSINESSUNITCODE = FD.BUSINESSUNITCODE" \
          " And PI.FINDOCFINANCIALYEARCODE = FD.FINANCIALYEARCODE" \
          " And PI.FINDOCTEMPLATECODE = FD.DOCUMENTTEMPLATECODE" \
          " And PI.FINDOCCODE = FD.CODE" \
          " Join SalesDocument SD On PI.CODE = SD.PROVISIONALCODE" \
          " join OrderPartner As OrderPartner         on SD.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode" \
          " And OrderPartner.CustomerSupplierType = '1'" \
          " Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId" \
          " Left Join Address On BusinessPartner.ABSUNIQUEID = Address.UNIQUEID" \
          " And SD.DELIVERYPOINTCODE = Address.CODE" \
          " Left Join TRANSPORTZONE On Address.TRANSPORTZONECODE = TRANSPORTZONE.Code" \
          " Where   PI.FINDOCBUSINESSUNITCODE Is Not Null And PI.FINDOCFINANCIALYEARCODE Is Not Null" \
          " And PI. FINDOCTEMPLATECODE Is Not Null And  PI.FINDOCCODE Is Not Null" \
          " And  days (current date) - days (FD.DUEDATE) >= "+Days[-1]+Company+BrkGroup+"" \
          " group by PI.Code, PI.INVOICEDATE, PI.INVOICEDATE," \
          " days (current date) - days (FD.DUEDATE),PI.NETTVALUE,PI.NETTVALUE,BusinessPartner.legalname1," \
          " Company.Longdescription,AgGrp.Longdescription,Agent.Longdescription,FD.DUEDATE,TRANSPORTZONE.LONGDESCRIPTION" \
          " order by Company,BrokerGrp,Broker,ISSUEDATE,INVNO"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    if result==False:
        Exceptions = "No Data Found According To Your Criteria"
        return render(request, "OSMoreThanDays.html",
                      {'GDataCompany': views.GDataCompany, 'GDataBroker': views.GDataBroker,
                       'GDataBrokerGroup': views.GDataBrokerGroup, 'Exceptions': Exceptions})
    while result != False:
        global counter
        counter = counter + 1
        cumamt = cumamt + round(float(result['INVAMT']), 3)
        result['CUMAMTT'] = round(cumamt, 2)
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d,"","")
        result = con.db.fetch_both(stmt)
    if result == False:
        pdfrpt.d = pdfrpt.dvalue('', '', pdfrpt.divisioncode)
        pdfrpt.printtotal(pdfrpt.cumamtlist)
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    counter = 0
    pdfrpt.d = pdfrpt.newpage()