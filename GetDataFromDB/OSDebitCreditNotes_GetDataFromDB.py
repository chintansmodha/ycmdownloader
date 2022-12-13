from FormLoad import OSDebitCreditNotes_FormLoad as OSDCNFL
from ProcessSelection import OSDebitCreditNotes_ProcessSelection as OSDCNPS
from Global_Files import Connection_String as con
from datetime import datetime
from PrintPDF import OSCreditNotesInterCompanySummaryWise_PrintPDF as pdfrpt1
from PrintPDF import OSCreditNotes_PrintPDF as pdfrpt2
from PrintPDF import OSCreditNotesInterCompany_PrintPDF as pdfrpt3
from PrintPDF import OSCreditNotesSummarywise_PrintPDF as pdfrpt4
from PrintPDF import OSDebitNotesInterCompanySummaryWise_PrintPDF as pdfrpt5
from PrintPDF import OSDebitNotes_PrintPDF as pdfrpt6
from PrintPDF import OSDebitNotesInterCompany_PrintPDF as pdfrpt7
from PrintPDF import OSDebitNotesSummaryWise_PrintPDF as pdfrpt8

counter=0

def OSCreditNotesInterCompanySummaryWise(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"

    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

    if not LSAllBroker and not LSBroker or LSAllBroker:
        LSBroker=""
    elif LSBroker:
        LSBroker= " And AGENT.CODE in("+str(LSBroker)[1:-1]+")"

    
    sql=(" Select  PI.Code as INVNO"
"        ,VARCHAR_FORMAT(PI.INVOICEDATE, 'DD-MM-YYYY') as InvoiceDate"
"        ,cast(FOD.AMOUNTINCC as decimal(18,2)) AS INVAMT"
"        ,cast((FOD.AmountinCC-FOD.CLEAREDAMOUNT) as decimal(18,2)) As OSAMT"
"        ,BusinessPartner.legalname1 As Party"
"        ,Company.Longdescription As Company "
"        ,AgGrp.Longdescription AS Broker"
"       From FinOpendocuments as FOD"
"        JOIN FINBUSINESSUNIT UNIT       ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"        JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"        Join PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                        And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                        And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                        And FOD.CODE = PI.FINDOCCODE "
"        Join    AgentsGroupDetail AGD   On      PI.Agent1Code = AGD.AgentCode "
"        Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code "
"        join OrderPartner As OrderPartner         on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode"
"        And                                     FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType"
"        Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId"
"        Where  FOD.postingdate <= '2022-11-01'"
"        And    FOD.FINANCIALYEARCODE = '2023'"
"        And    FOD.DOCUMENTTEMPLATECODE = 'S01'"
"        And    (FOD.AmountinCC-FOD.CLEAREDAMOUNT) > 0"

" Union All     "
"        "
" Select  PI.Code as INVNO"
"        ,VARCHAR_FORMAT(PI.INVOICEDATE, 'DD-MM-YYYY') as InvoiceDate"
"        ,cast(FOD.AMOUNTINCC as decimal(18,2)) AS INVAMT"
"        ,cast((FODT.CLEAREDAMOUNT) as decimal(18,2)) As OSAMT"
"        ,BusinessPartner.legalname1 As Party"
"        ,Company.Longdescription As Company "
"        ,AgGrp.Longdescription AS Broker"
" From    FinOpendocuments as FOD"
"        JOIN FINBUSINESSUNIT UNIT               ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"        JOIN FINBUSINESSUNIT Company            ON      UNIT.GROUPBUCODE=Company.CODE"
"        Join PlantInvoice PI                    on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                                And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                                And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                                And FOD.CODE = PI.FINDOCCODE "
"        Join    AgentsGroupDetail AGD           On      PI.Agent1Code = AGD.AgentCode "
"        Join    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code "
"        join OrderPartner As OrderPartner       on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode"
"                                                And FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType"
"        Join BusinessPartner                    ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId"
"        Join FinopendocumentsTransactions as FODT"
"                                                ON      FOD.BUSINESSUNITCODE=FODT.ORIGINBUSINESSUNITCODE"
"                                                And     FOD.FINANCIALYEARCODE=FODT.ORIGINFINANCIALYEARCODE"
"                                                And     FOD.DOCUMENTTEMPLATECODE=FODT.ORIGINDOCUMENTTEMPLATECODE"
"                                                And     FOD.CODE=FODT.ORIGINCODE"
" Where  FODT.TRANSACTIONDATE > '2022-11-01'"
" and     FOD.postingdate <= '2022-11-01'"
)

    stmt = con.db.prepare(con.conn, sql)
    asondt = datetime.strptime(LDAsOnDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    
    
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt1.textsize(pdfrpt1.c, result, pdfrpt1.d,  asondt)
        pdfrpt1.d = pdfrpt1.dvalue( asondt, pdfrpt1.divisioncode)
        result = con.db.fetch_both(stmt)
    if  result == False:
        pdfrpt1.d =pdfrpt1.dvalue( asondt, pdfrpt1.divisioncode)
        pdfrpt1.d =pdfrpt1.dvalue( asondt, pdfrpt1.divisioncode)
        pdfrpt1.partytotalprint(pdfrpt1.d,asondt)
        pdfrpt1.d =pdfrpt1.dvalue( asondt, pdfrpt1.divisioncode)
        pdfrpt1.d =pdfrpt1.dvalue( asondt, pdfrpt1.divisioncode)
        pdfrpt1.brokertotalprint(pdfrpt1.d,asondt)
        
    if pdfrpt1.d < 20:
        pdfrpt1.d = 730
        pdfrpt1.c.showPage()
        pdfrpt1.header(asondt, pdfrpt1.divisioncode)

    pdfrpt1.c.setPageSize(pdfrpt1.landscape(pdfrpt1.A4))
    pdfrpt1.c.showPage()
    pdfrpt1.c.save()
    pdfrpt1.newrequest()

def OSCreditNotes(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"

    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

    if not LSAllBroker and not LSBroker or LSAllBroker:
        LSBroker=""
    elif LSBroker:
        LSBroker= " And AGENT.CODE in("+str(LSBroker)[1:-1]+")"

    
    sql=()

    stmt = con.db.prepare(con.conn, sql)
    asondt = datetime.strptime(LDAsOnDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    
    
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt2.textsize(pdfrpt2.c, result, pdfrpt2.d,  asondt)
        pdfrpt2.d = pdfrpt2.dvalue( asondt, pdfrpt2.divisioncode)
        result = con.db.fetch_both(stmt)
    if  result == False:
        pdfrpt2.d =pdfrpt2.dvalue( asondt, pdfrpt2.divisioncode)
        pdfrpt2.d =pdfrpt2.dvalue( asondt, pdfrpt2.divisioncode)
        pdfrpt2.partytotalprint(pdfrpt2.d,asondt)
        pdfrpt2.d =pdfrpt2.dvalue( asondt, pdfrpt2.divisioncode)
        pdfrpt2.d =pdfrpt2.dvalue( asondt, pdfrpt2.divisioncode)
        pdfrpt2.brokertotalprint(pdfrpt2.d,asondt)
        
    if pdfrpt2.d < 20:
        pdfrpt2.d = 730
        pdfrpt2.c.showPage()
        pdfrpt2.header(asondt, pdfrpt2.divisioncode)

    pdfrpt2.c.setPageSize(pdfrpt2.landscape(pdfrpt2.A4))
    pdfrpt2.c.showPage()
    pdfrpt2.c.save()
    pdfrpt2.newrequest()

def OSCreditNotesInterCompany(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"

    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

    if not LSAllBroker and not LSBroker or LSAllBroker:
        LSBroker=""
    elif LSBroker:
        LSBroker= " And AGENT.CODE in("+str(LSBroker)[1:-1]+")"

    
    sql=()

    stmt = con.db.prepare(con.conn, sql)
    asondt = datetime.strptime(LDAsOnDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    
    
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt3.textsize(pdfrpt3.c, result, pdfrpt3.d,  asondt)
        pdfrpt3.d = pdfrpt3.dvalue( asondt, pdfrpt3.divisioncode)
        result = con.db.fetch_both(stmt)
    if  result == False:
        pdfrpt3.d =pdfrpt3.dvalue( asondt, pdfrpt3.divisioncode)
        pdfrpt3.d =pdfrpt3.dvalue( asondt, pdfrpt3.divisioncode)
        pdfrpt3.partytotalprint(pdfrpt3.d,asondt)
        pdfrpt3.d =pdfrpt3.dvalue( asondt, pdfrpt3.divisioncode)
        pdfrpt3.d =pdfrpt3.dvalue( asondt, pdfrpt3.divisioncode)
        pdfrpt3.brokertotalprint(pdfrpt3.d,asondt)
        
    if pdfrpt3.d < 20:
        pdfrpt3.d = 730
        pdfrpt3.c.showPage()
        pdfrpt3.header(asondt, pdfrpt3.divisioncode)

    pdfrpt3.c.setPageSize(pdfrpt3.landscape(pdfrpt3.A4))
    pdfrpt3.c.showPage()
    pdfrpt3.c.save()
    pdfrpt3.newrequest()

def OSCreditNotesSummarywise(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"

    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

    if not LSAllBroker and not LSBroker or LSAllBroker:
        LSBroker=""
    elif LSBroker:
        LSBroker= " And AGENT.CODE in("+str(LSBroker)[1:-1]+")"

    
    sql=()

    stmt = con.db.prepare(con.conn, sql)
    asondt = datetime.strptime(LDAsOnDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    
    
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt4.textsize(pdfrpt4.c, result, pdfrpt4.d,  asondt)
        pdfrpt4.d = pdfrpt4.dvalue( asondt, pdfrpt4.divisioncode)
        result = con.db.fetch_both(stmt)
    if  result == False:
        pdfrpt4.d =pdfrpt4.dvalue( asondt, pdfrpt4.divisioncode)
        pdfrpt4.d =pdfrpt4.dvalue( asondt, pdfrpt4.divisioncode)
        pdfrpt4.partytotalprint(pdfrpt4.d,asondt)
        pdfrpt4.d =pdfrpt4.dvalue( asondt, pdfrpt4.divisioncode)
        pdfrpt4.d =pdfrpt4.dvalue( asondt, pdfrpt4.divisioncode)
        pdfrpt4.brokertotalprint(pdfrpt4.d,asondt)
        
    if pdfrpt4.d < 20:
        pdfrpt4.d = 730
        pdfrpt4.c.showPage()
        pdfrpt4.header(asondt, pdfrpt4.divisioncode)

    pdfrpt4.c.setPageSize(pdfrpt4.landscape(pdfrpt4.A4))
    pdfrpt4.c.showPage()
    pdfrpt4.c.save()
    pdfrpt4.newrequest()

def OSDebitNotesInterCompanySummaryWise(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"

    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

    if not LSAllBroker and not LSBroker or LSAllBroker:
        LSBroker=""
    elif LSBroker:
        LSBroker= " And AGENT.CODE in("+str(LSBroker)[1:-1]+")"

    sql=(" Select  PI.Code as INVNO"
"        ,VARCHAR_FORMAT(PI.INVOICEDATE, 'DD-MM-YYYY') as InvoiceDate"
"        ,cast(FOD.AMOUNTINCC as decimal(18,2)) AS INVAMT"
"        ,cast((FOD.AmountinCC-FOD.CLEAREDAMOUNT) as decimal(18,2)) As OSAMT"
"        ,BusinessPartner.legalname1 As Party"
"        ,Company.Longdescription As Company "
"        ,AgGrp.Longdescription AS Broker"
"       From FinOpendocuments as FOD"
"        JOIN FINBUSINESSUNIT UNIT       ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"        JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"        Join PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                        And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                        And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                        And FOD.CODE = PI.FINDOCCODE "
"        Join    AgentsGroupDetail AGD   On      PI.Agent1Code = AGD.AgentCode "
"        Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code "
"        join OrderPartner As OrderPartner         on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode"
"        And                                     FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType"
"        Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId"
"        Where  FOD.postingdate <= '2022-11-01'"
"        And    FOD.FINANCIALYEARCODE = '2023'"
"        And    FOD.DOCUMENTTEMPLATECODE = 'S01'"
"        And    (FOD.AmountinCC-FOD.CLEAREDAMOUNT) > 0"

" Union All     "
"        "
" Select  PI.Code as INVNO"
"        ,VARCHAR_FORMAT(PI.INVOICEDATE, 'DD-MM-YYYY') as InvoiceDate"
"        ,cast(FOD.AMOUNTINCC as decimal(18,2)) AS INVAMT"
"        ,cast((FODT.CLEAREDAMOUNT) as decimal(18,2)) As OSAMT"
"        ,BusinessPartner.legalname1 As Party"
"        ,Company.Longdescription As Company "
"        ,AgGrp.Longdescription AS Broker"
" From    FinOpendocuments as FOD"
"        JOIN FINBUSINESSUNIT UNIT               ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"        JOIN FINBUSINESSUNIT Company            ON      UNIT.GROUPBUCODE=Company.CODE"
"        Join PlantInvoice PI                    on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                                And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                                And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                                And FOD.CODE = PI.FINDOCCODE "
"        Join    AgentsGroupDetail AGD           On      PI.Agent1Code = AGD.AgentCode "
"        Join    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code "
"        join OrderPartner As OrderPartner       on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode"
"                                                And FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType"
"        Join BusinessPartner                    ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId"
"        Join FinopendocumentsTransactions as FODT"
"                                                ON      FOD.BUSINESSUNITCODE=FODT.ORIGINBUSINESSUNITCODE"
"                                                And     FOD.FINANCIALYEARCODE=FODT.ORIGINFINANCIALYEARCODE"
"                                                And     FOD.DOCUMENTTEMPLATECODE=FODT.ORIGINDOCUMENTTEMPLATECODE"
"                                                And     FOD.CODE=FODT.ORIGINCODE"
" Where  FODT.TRANSACTIONDATE > '2022-11-01'"
" and     FOD.postingdate <= '2022-11-01'"
)

    stmt = con.db.prepare(con.conn,sql)
    asondt = datetime.strptime(LDAsOnDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt5.textsize(pdfrpt5.c, result, pdfrpt5.d,  asondt)
        pdfrpt5.d = pdfrpt5.dvalue( asondt, pdfrpt5.divisioncode)
        result = con.db.fetch_both(stmt)
    if  result == False:
        pdfrpt5.d =pdfrpt5.dvalue( asondt, pdfrpt5.divisioncode)
        pdfrpt5.d =pdfrpt5.dvalue( asondt, pdfrpt5.divisioncode)
        pdfrpt5.partytotalprint(pdfrpt5.d,asondt)
        pdfrpt5.d =pdfrpt5.dvalue( asondt, pdfrpt5.divisioncode)
        pdfrpt5.d =pdfrpt5.dvalue( asondt, pdfrpt5.divisioncode)
        pdfrpt5.brokertotalprint(pdfrpt5.d,asondt)
        
    if pdfrpt5.d < 20:
        pdfrpt5.d = 730
        pdfrpt5.c.showPage()
        pdfrpt5.header(asondt, pdfrpt5.divisioncode)

    pdfrpt5.c.setPageSize(pdfrpt5.landscape(pdfrpt5.A4))
    pdfrpt5.c.showPage()
    pdfrpt5.c.save()
    pdfrpt5.newrequest()

def OSDebitNotes(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"

    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

    if not LSAllBroker and not LSBroker or LSAllBroker:
        LSBroker=""
    elif LSBroker:
        LSBroker= " And AGENT.CODE in("+str(LSBroker)[1:-1]+")"

    
    sql=()

    stmt = con.db.prepare(con.conn, sql)
    asondt = datetime.strptime(LDAsOnDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    
    
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt6.textsize(pdfrpt6.c, result, pdfrpt6.d,  asondt)
        pdfrpt6.d = pdfrpt6.dvalue( asondt, pdfrpt6.divisioncode)
        result = con.db.fetch_both(stmt)
    if  result == False:
        pdfrpt6.d =pdfrpt6.dvalue( asondt, pdfrpt6.divisioncode)
        pdfrpt6.d =pdfrpt6.dvalue( asondt, pdfrpt6.divisioncode)
        pdfrpt6.partytotalprint(pdfrpt6.d,asondt)
        pdfrpt6.d =pdfrpt6.dvalue( asondt, pdfrpt6.divisioncode)
        pdfrpt6.d =pdfrpt6.dvalue( asondt, pdfrpt6.divisioncode)
        pdfrpt6.brokertotalprint(pdfrpt6.d,asondt)
        
    if pdfrpt6.d < 20:
        pdfrpt6.d = 730
        pdfrpt6.c.showPage()
        pdfrpt6.header(asondt, pdfrpt6.divisioncode)

    pdfrpt6.c.setPageSize(pdfrpt6.landscape(pdfrpt6.A4))
    pdfrpt6.c.showPage()
    pdfrpt6.c.save()
    pdfrpt6.newrequest()

def OSDebitNotesInterCompany(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"

    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

    if not LSAllBroker and not LSBroker or LSAllBroker:
        LSBroker=""
    elif LSBroker:
        LSBroker= " And AGENT.CODE in("+str(LSBroker)[1:-1]+")"

    
    sql=()

    stmt = con.db.prepare(con.conn, sql)
    asondt = datetime.strptime(LDAsOnDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    
    
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt7.textsize(pdfrpt7.c, result, pdfrpt7.d,  asondt)
        pdfrpt7.d = pdfrpt7.dvalue( asondt, pdfrpt7.divisioncode)
        result = con.db.fetch_both(stmt)
    if  result == False:
        pdfrpt7.d =pdfrpt7.dvalue( asondt, pdfrpt7.divisioncode)
        pdfrpt7.d =pdfrpt7.dvalue( asondt, pdfrpt7.divisioncode)
        pdfrpt7.partytotalprint(pdfrpt7.d,asondt)
        pdfrpt7.d =pdfrpt7.dvalue( asondt, pdfrpt7.divisioncode)
        pdfrpt7.d =pdfrpt7.dvalue( asondt, pdfrpt7.divisioncode)
        pdfrpt7.brokertotalprint(pdfrpt7.d,asondt)
        
    if pdfrpt7.d < 20:
        pdfrpt7.d = 730
        pdfrpt7.c.showPage()
        pdfrpt7.header(asondt, pdfrpt7.divisioncode)

    pdfrpt7.c.setPageSize(pdfrpt7.landscape(pdfrpt7.A4))
    pdfrpt7.c.showPage()
    pdfrpt7.c.save()
    pdfrpt7.newrequest()

def OSDebitNotesSummaryWise(LSCompany,LSAllCompany,LSParty,LSAllParty,LSBroker,LSAllBroker,LDAsOnDate):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"

    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

    if not LSAllBroker and not LSBroker or LSAllBroker:
        LSBroker=""
    elif LSBroker:
        LSBroker= " And AGENT.CODE in("+str(LSBroker)[1:-1]+")"

    
    sql=()

    stmt = con.db.prepare(con.conn, sql)
    asondt = datetime.strptime(LDAsOnDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    
    
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt8.textsize(pdfrpt8.c, result, pdfrpt8.d,  asondt)
        pdfrpt8.d = pdfrpt8.dvalue( asondt, pdfrpt8.divisioncode)
        result = con.db.fetch_both(stmt)
    if  result == False:
        pdfrpt8.d =pdfrpt8.dvalue( asondt, pdfrpt8.divisioncode)
        pdfrpt8.d =pdfrpt8.dvalue( asondt, pdfrpt8.divisioncode)
        pdfrpt8.partytotalprint(pdfrpt8.d,asondt)
        pdfrpt8.d =pdfrpt8.dvalue( asondt, pdfrpt8.divisioncode)
        pdfrpt8.d =pdfrpt8.dvalue( asondt, pdfrpt8.divisioncode)
        pdfrpt8.brokertotalprint(pdfrpt8.d,asondt)
        
    if pdfrpt8.d < 20:
        pdfrpt8.d = 730
        pdfrpt8.c.showPage()
        pdfrpt8.header(asondt, pdfrpt8.divisioncode)

    pdfrpt8.c.setPageSize(pdfrpt8.landscape(pdfrpt8.A4))
    pdfrpt8.c.showPage()
    pdfrpt8.c.save()
    pdfrpt8.newrequest()
