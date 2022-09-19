from PrintPDF import BrokerWiseOrderOS_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
counter = 0
def BrokerWiseOrderOS_PrintPDF(Company,Broker,Party,startdate,enddate):
    global total
    global netout
    global totalout
    global cumamt
    cumamt=0
    netout =0
    totalout=0
    total=0
    print(Company,Broker,Party)
    if Company:
        Company = " AND BU.Code in('"+Company[-1]+"')"
    else:
        Company = ""
    if Broker:
        Broker = " AND Agent.Code in('"+Broker[-1]+"')"
    else:
        Broker = ""
    if Party:
        Party = " AND BusinessPartner.numberid in('"+Party[-1]+"')"
    else:
        Party = ""
    sql = " Select  PI.Code as INVNO, PI.INVOICEDATE as ISSUEDATE, FD.DUEDATE as DUEDATE," \
          " days (current date) - days (FD.DUEDATE) as OD," \
          " cast(PI.NETTVALUE as decimal(18,2)) AS INVAMT" \
          ",cast(PI.NETTVALUE as decimal(18,0)) As OSAMT,cast(PI.NETTVALUE as decimal(18,2)) As CUMAMT," \
          " BusinessPartner.legalname1 As Party" \
          ",0 As ChallanNo," \
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
          " And PI. FINDOCTEMPLATECODE Is Not Null And  PI.FINDOCCODE Is Not Null"+Company+Broker+Party+"" \
          " group by PI.Code, PI.INVOICEDATE, PI.INVOICEDATE," \
          " days (current date) - days (FD.DUEDATE),PI.NETTVALUE,PI.NETTVALUE,BusinessPartner.legalname1," \
          " Company.Longdescription,AgGrp.Longdescription,Agent.Longdescription,FD.DUEDATE,TRANSPORTZONE.LONGDESCRIPTION" \
          " order by Broker, Company, Party"
    #"And  days (current date) - days (FD.DUEDATE) >30" \
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        global counter
        counter=counter+1
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d,startdate,enddate)
        pdfrpt.d=pdfrpt.dvalue(startdate,enddate,result,pdfrpt.divisioncode)
        result = con.db.fetch_both(stmt)
    if result == False:
        pdfrpt.d=pdfrpt.dvalue(startdate,enddate,result,pdfrpt.divisioncode)
        pdfrpt.printdivisiontotallast()
        pdfrpt.d=pdfrpt.dvalue(startdate,enddate,result,pdfrpt.divisioncode)
        pdfrpt.printbrokergrptotal()
        pdfrpt.d=pdfrpt.dvalue(startdate,enddate,result,pdfrpt.divisioncode)
        pdfrpt.printbrokertotallast()
        pdfrpt.d=pdfrpt.dvalue(startdate,enddate,result,pdfrpt.divisioncode)
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    counter = 0
    pdfrpt.d = pdfrpt.newpage()