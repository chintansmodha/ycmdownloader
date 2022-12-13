from PrintPDF import BrokerWiseSalesSummaryItemWiseSummaryWise_PrintPDF as pdfrpt1
from PrintPDF import BrokerWiseSalesSummary_PrintPDF as pdfrpt2
from PrintPDF import BrokerWiseSalesSummaryItemWise_PrintPDF as pdfrpt3
from PrintPDF import BrokerWiseSalesSummarySummaryWise_PrintPDF as pdfrpt4
from datetime import datetime
from Global_Files import Connection_String as con

#GetDataFromDB
counter=0
Exceptions=""
def BrokerWiseSalesSummaryItemWiseSummaryWise(LSCompany,LSAllCompanies,LSParty,LSAllParties,LSBrokerGroup,LSAllBrokerGroup,LDEndDate,LDStartDate,ItemWise,SummaryWise):
    
    if not LSAllCompanies and not LSCompany or LSAllCompanies:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"
    
    if not LSAllParties and not LSParty or LSAllParties:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"
    if not LSAllBrokerGroup and not LSBrokerGroup or LSAllBrokerGroup:
        LSBrokerGroup=""
    elif LSBrokerGroup:
        LSBrokerGroup= " And AGENTSGROUP.CODE in("+str(LSBrokerGroup)[1:-1]+")"
  
    sql=("Select Plant.LONGDESCRIPTION as company,AgGrp.LONGDESCRIPTION as agentgroup, BP.Legalname1 as Party, product.longdescription as item" 
" ,sum(PI.totalquantity) as quantity,sum(pi.BASICVALUE) as amount"
" from PlantInvoice as PI"
"        Join Plant                              ON PI.FactoryCode = Plant.code"
"        JOIN plantinvoiceline as PIL"
"                                                ON PI.code = PIL.plantinvoicecode "
"                                                AND PI.divisioncode =                 PIL.plantinvoicedivisioncode "
"                                                AND PI.invoicedate = PIL.invoicedate"
" JOIN fullitemkeydecoder FIKD  "
"                   ON PIL.itemtypecode = FIKD.itemtypecode  "
"                      AND COALESCE(PIL.subcode01, '') =                COALESCE(FIKD.subcode01, '') "  
"                      AND COALESCE(PIL.subcode02, '') =                COALESCE(FIKD.subcode02, '')  "
"                      AND COALESCE(PIL.subcode03, '') =                COALESCE(FIKD.subcode03, '')  "
"                      AND COALESCE(PIL.subcode04, '') =                COALESCE(FIKD.subcode04, '')  "
"                      AND COALESCE(PIL.subcode05, '') =                COALESCE(FIKD.subcode05, '')  "
"                      AND COALESCE(PIL.subcode06, '') =                COALESCE(FIKD.subcode06, '')  "
"                      AND COALESCE(PIL.subcode07, '') =                COALESCE(FIKD.subcode07, '')  "
"                      AND COALESCE(PIL.subcode08, '') =                COALESCE(FIKD.subcode08, '')  "
"                      AND COALESCE(PIL.subcode09, '') =                COALESCE(FIKD.subcode09, '')  "
"                      AND COALESCE(PIL.subcode10, '') =                COALESCE(FIKD.subcode10, '')  "
" JOIN product    ON PIL.itemtypecode = product.itemtypecode  "
"                AND FIKD.itemuniqueid = product.absuniqueid "
"        Join    AgentsGroupDetail AGD           On      PI.Agent1Code = AGD.AgentCode "
"        Join    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code "
"        Join SalesDocument SD                   ON    PI.CODE = SD.PROVISIONALCODE "
"                                                And SD.DOCUMENTTYPETYPE = '06' "
"        Join OrderPartner As OP                 On SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode "
"                                                And OP.CustomerSupplierType = 1"
"        Join BusinessPartner BP ON OP.OrderBusinessPartnerNumberId = BP.NumberId "
"  where pi.invoicedate between '"+str(LDStartDate)+"' and '"+str(LDEndDate)+"'"+LSCompany+LSParty+LSBrokerGroup+" "
"        group by product.longdescription,BP.Legalname1,AgGrp.LONGDESCRIPTION,Plant.LONGDESCRIPTION "
" Order By agentgroup ")
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    print(type(stdt))
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt1.textsize(pdfrpt1.c, result, pdfrpt1.d, stdt, etdt)
        pdfrpt1.d = pdfrpt1.dvalue(stdt, etdt, pdfrpt1.divisioncode)
        result = con.db.fetch_both(stmt)

    if pdfrpt1.d < 20:
        pdfrpt1.d = 730
        pdfrpt1.c.showPage()
        pdfrpt1.header(stdt, etdt, pdfrpt1.divisioncode)

    if result == False:
        global Exceptions
    if counter>0:
        pdfrpt1.d = pdfrpt1.dlocvalue(pdfrpt1.d)
        pdfrpt1.fonts(7)
        # pdfrpt1.c.drawString(10, pdfrpt1.d, str(pdfrpt1.divisioncode[-2]) + " TOTAL : ")
        # pdfrpt1.c.drawAlignedString(570, pdfrpt1.d, str("%.2f" % float(pdfrpt1.CompanyAmountTotal)))
        pdfrpt1.companyclean()
        Exceptions = ""
    elif counter == 0:
        Exceptions = "Note: Please Select Valid Credentials"
        return
    pdfrpt1.newrequest()
    pdfrpt1.c.setPageSize(pdfrpt1.A4)
    pdfrpt1.c.showPage()
    pdfrpt1.c.save()

def BrokerWiseSalesSummary(LSCompany,LSAllCompanies,LSParty,LSAllParties,LSBrokerGroup,LSAllBrokerGroup,LDEndDate,LDStartDate,
    ItemWise,SummaryWise):
    if not LSAllCompanies and not LSCompany or LSAllCompanies:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"
    if not LSAllParties and not LSParty or LSAllParties:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"
    if not LSAllBrokerGroup and not LSBrokerGroup or LSAllBrokerGroup:
        LSBrokerGroup=""
    elif LSBrokerGroup:
        LSBrokerGroup= " And AGENTSGROUP.CODE in("+str(LSBrokerGroup)[1:-1]+")"
  
    sql=("Select Plant.LONGDESCRIPTION as company,AgGrp.LONGDESCRIPTION as agentgroup, BP.Legalname1 as Party" 
" ,SD.PROVISIONALCODE as vchno,SD.PROVISIONALDOCUMENTDATE as vchdate "    
" ,sum(pi.BASICVALUE) as amount"
" from PlantInvoice as PI"
"        Join Plant                              ON PI.FactoryCode = Plant.code"
"        JOIN plantinvoiceline as PIL"
"                                                ON PI.code = PIL.plantinvoicecode "
"                                                AND PI.divisioncode =                 PIL.plantinvoicedivisioncode "
"                                                AND PI.invoicedate = PIL.invoicedate"
" JOIN fullitemkeydecoder FIKD  "
"                   ON PIL.itemtypecode = FIKD.itemtypecode  "
"                      AND COALESCE(PIL.subcode01, '') =                COALESCE(FIKD.subcode01, '') "  
"                      AND COALESCE(PIL.subcode02, '') =                COALESCE(FIKD.subcode02, '')  "
"                      AND COALESCE(PIL.subcode03, '') =                COALESCE(FIKD.subcode03, '')  "
"                      AND COALESCE(PIL.subcode04, '') =                COALESCE(FIKD.subcode04, '')  "
"                      AND COALESCE(PIL.subcode05, '') =                COALESCE(FIKD.subcode05, '')  "
"                      AND COALESCE(PIL.subcode06, '') =                COALESCE(FIKD.subcode06, '')  "
"                      AND COALESCE(PIL.subcode07, '') =                COALESCE(FIKD.subcode07, '')  "
"                      AND COALESCE(PIL.subcode08, '') =                COALESCE(FIKD.subcode08, '')  "
"                      AND COALESCE(PIL.subcode09, '') =                COALESCE(FIKD.subcode09, '')  "
"                      AND COALESCE(PIL.subcode10, '') =                COALESCE(FIKD.subcode10, '')  "
" JOIN product    ON PIL.itemtypecode = product.itemtypecode  "
"                AND FIKD.itemuniqueid = product.absuniqueid "
"        Join    AgentsGroupDetail AGD           On      PI.Agent1Code = AGD.AgentCode "
"        Join    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code "
"        Join SalesDocument SD                   ON    PI.CODE = SD.PROVISIONALCODE "
"                                                And SD.DOCUMENTTYPETYPE = '06' "
"        Join OrderPartner As OP                 On SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode "
"                                                And OP.CustomerSupplierType = 1"
"        Join BusinessPartner BP ON OP.OrderBusinessPartnerNumberId = BP.NumberId "
"  where pi.invoicedate between '"+str(LDStartDate)+"' and '"+str(LDEndDate)+"'"+LSCompany+LSParty+LSBrokerGroup+" "
"        group by SD.PROVISIONALCODE,SD.PROVISIONALDOCUMENTDATE,BP.Legalname1,AgGrp.LONGDESCRIPTION,Plant.LONGDESCRIPTION "
" Order By agentgroup ")
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    print(type(stdt))
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt2.textsize(pdfrpt2.c, result, pdfrpt2.d, stdt, etdt)
        pdfrpt2.d = pdfrpt2.dvalue(stdt, etdt, pdfrpt2.divisioncode)
        result = con.db.fetch_both(stmt)

    if pdfrpt2.d < 20:
        pdfrpt2.d = 730
        pdfrpt2.c.showPage()
        pdfrpt2.header(stdt, etdt, pdfrpt2.divisioncode)

    if result == False:
        global Exceptions
    if counter>0:
        pdfrpt2.d = pdfrpt2.dlocvalue(pdfrpt2.d)
        pdfrpt2.fonts(7)
        # pdfrpt2.c.drawString(10, pdfrpt2.d, str(pdfrpt2.divisioncode[-2]) + " TOTAL : ")
        # pdfrpt2.c.drawAlignedString(570, pdfrpt2.d, str("%.2f" % float(pdfrpt2.CompanyAmountTotal)))
        pdfrpt2.companyclean()
        Exceptions = ""
    elif counter == 0:
        Exceptions = "Note: Please Select Valid Credentials"
        return

    pdfrpt2.c.setPageSize(pdfrpt2.A4)
    pdfrpt2.c.showPage()
    pdfrpt2.c.save()
    pdfrpt2.newrequest()


def BrokerWiseSalesSummaryItemWise(LSCompany,LSAllCompanies,LSParty,LSAllParties,LSBrokerGroup,LSAllBrokerGroup,LDEndDate,LDStartDate,
    ItemWise,SummaryWise):
    if not LSAllCompanies and not LSCompany or LSAllCompanies:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"
    if not LSAllParties and not LSParty or LSAllParties:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"
    if not LSAllBrokerGroup and not LSBrokerGroup or LSAllBrokerGroup:
        LSBrokerGroup=""
    elif LSBrokerGroup:
        LSBrokerGroup= " And AGENTSGROUP.CODE in("+str(LSBrokerGroup)[1:-1]+")"
  
    sql=(" Select Plant.LONGDESCRIPTION as company,AgGrp.LONGDESCRIPTION as agentgroup, BP.Legalname1 as Party, product.longdescription as item "
    " ,cast(PI.totalquantity as decimal(18,3)) as quantity"
    " ,cast(pi.BASICVALUE as decimal(18,2)) as amount "
    " ,SD.PROVISIONALCODE as vchno,SD.PROVISIONALDOCUMENTDATE as vchdate "
    " ,cast(PIL.PRICE as decimal(18,2)) as Rate "
    " from PlantInvoice as PI "
    "        Join Plant                              ON PI.FactoryCode = Plant.code "
    "        JOIN plantinvoiceline as PIL "
    "                                                ON PI.code = PIL.plantinvoicecode "
    "                                                AND PI.divisioncode =                 PIL.plantinvoicedivisioncode "
    "                                                AND PI.invoicedate = PIL.invoicedate "
    " JOIN fullitemkeydecoder FIKD  "
    "                   ON PIL.itemtypecode = FIKD.itemtypecode  "
    "                      AND COALESCE(PIL.subcode01, '') =                COALESCE(FIKD.subcode01, '')  "
    "                      AND COALESCE(PIL.subcode02, '') =                COALESCE(FIKD.subcode02, '')  "
    "                      AND COALESCE(PIL.subcode03, '') =                COALESCE(FIKD.subcode03, '')  "
    "                      AND COALESCE(PIL.subcode04, '') =                COALESCE(FIKD.subcode04, '')  "
    "                      AND COALESCE(PIL.subcode05, '') =                COALESCE(FIKD.subcode05, '')  "
    "                      AND COALESCE(PIL.subcode06, '') =                COALESCE(FIKD.subcode06, '')  "
    "                      AND COALESCE(PIL.subcode07, '') =                COALESCE(FIKD.subcode07, '')  "
    "                      AND COALESCE(PIL.subcode08, '') =                COALESCE(FIKD.subcode08, '')  "
    "                      AND COALESCE(PIL.subcode09, '') =                COALESCE(FIKD.subcode09, '')  "
    "                      AND COALESCE(PIL.subcode10, '') =                COALESCE(FIKD.subcode10, '')  "
    " JOIN product    ON PIL.itemtypecode = product.itemtypecode  "
    "                AND FIKD.itemuniqueid = product.absuniqueid  "
    "        Join    AgentsGroupDetail AGD           On      PI.Agent1Code = AGD.AgentCode "
    "        Join    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code "
    "        Join SalesDocument SD                   ON    PI.CODE = SD.PROVISIONALCODE "
    "                                                And SD.DOCUMENTTYPETYPE = '06' "
    "        Join OrderPartner As OP                 On SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode "
    "                                                And OP.CustomerSupplierType = 1 "
    "        Join BusinessPartner BP ON OP.OrderBusinessPartnerNumberId = BP.NumberId "
    "        where pi.invoicedate between '"+str(LDStartDate)+"' and '"+str(LDEndDate)+"'"+LSCompany+LSParty+LSBrokerGroup+" "  
    " Order By agentgroup ")
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    print(type(stdt))
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt3.textsize(pdfrpt3.c, result, pdfrpt3.d, stdt, etdt)
        pdfrpt3.d = pdfrpt3.dvalue(stdt, etdt, pdfrpt3.divisioncode)
        result = con.db.fetch_both(stmt)

    if pdfrpt3.d < 20:
        pdfrpt3.d = 730
        pdfrpt3.c.showPage()
        pdfrpt3.header(stdt, etdt, pdfrpt3.divisioncode)

    if result == False:
        global Exceptions
    if counter>0:
        pdfrpt3.d = pdfrpt3.dlocvalue(pdfrpt3.d)
        pdfrpt3.fonts(7)
        # pdfrpt3.c.drawString(10, pdfrpt3.d, str(pdfrpt3.divisioncode[-2]) + " TOTAL : ")
        # pdfrpt3.c.drawAlignedString(570, pdfrpt3.d, str("%.2f" % float(pdfrpt3.CompanyAmountTotal)))
        pdfrpt3.companyclean()
        Exceptions = ""
    elif counter == 0:
        Exceptions = "Note: Please Select Valid Credentials"
        return

    pdfrpt3.c.setPageSize(pdfrpt3.A4)
    pdfrpt3.c.showPage()
    pdfrpt3.c.save()
    pdfrpt3.newrequest()

def BrokerWiseSalesSummarySummaryWise(LSCompany,LSAllCompanies,LSParty,LSAllParties,LSBrokerGroup,LSAllBrokerGroup,LDEndDate,LDStartDate,
    ItemWise,SummaryWise):    
    if not LSAllCompanies and not LSCompany or LSAllCompanies:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"
    if not LSAllParties and not LSParty or LSAllParties:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"
    if not LSAllBrokerGroup and not LSBrokerGroup or LSAllBrokerGroup:
        LSBrokerGroup=""
    elif LSBrokerGroup:
        LSBrokerGroup= " And AGENTSGROUP.CODE in("+str(LSBrokerGroup)[1:-1]+")"
  
    sql=("Select Plant.LONGDESCRIPTION as company,AgGrp.LONGDESCRIPTION as agentgroup, BP.Legalname1 as Party" 
" ,sum(pi.BASICVALUE) as amount"
" from PlantInvoice as PI"
"        Join Plant                              ON PI.FactoryCode = Plant.code"
"        JOIN plantinvoiceline as PIL"
"                                                ON PI.code = PIL.plantinvoicecode "
"                                                AND PI.divisioncode =                 PIL.plantinvoicedivisioncode "
"                                                AND PI.invoicedate = PIL.invoicedate"
" JOIN fullitemkeydecoder FIKD  "
"                   ON PIL.itemtypecode = FIKD.itemtypecode  "
"                      AND COALESCE(PIL.subcode01, '') =                COALESCE(FIKD.subcode01, '') "  
"                      AND COALESCE(PIL.subcode02, '') =                COALESCE(FIKD.subcode02, '')  "
"                      AND COALESCE(PIL.subcode03, '') =                COALESCE(FIKD.subcode03, '')  "
"                      AND COALESCE(PIL.subcode04, '') =                COALESCE(FIKD.subcode04, '')  "
"                      AND COALESCE(PIL.subcode05, '') =                COALESCE(FIKD.subcode05, '')  "
"                      AND COALESCE(PIL.subcode06, '') =                COALESCE(FIKD.subcode06, '')  "
"                      AND COALESCE(PIL.subcode07, '') =                COALESCE(FIKD.subcode07, '')  "
"                      AND COALESCE(PIL.subcode08, '') =                COALESCE(FIKD.subcode08, '')  "
"                      AND COALESCE(PIL.subcode09, '') =                COALESCE(FIKD.subcode09, '')  "
"                      AND COALESCE(PIL.subcode10, '') =                COALESCE(FIKD.subcode10, '')  "
" JOIN product    ON PIL.itemtypecode = product.itemtypecode  "
"                AND FIKD.itemuniqueid = product.absuniqueid "
"        Join    AgentsGroupDetail AGD           On      PI.Agent1Code = AGD.AgentCode "
"        Join    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code "
"        Join SalesDocument SD                   ON    PI.CODE = SD.PROVISIONALCODE "
"                                                And SD.DOCUMENTTYPETYPE = '06' "
"        Join OrderPartner As OP                 On SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode "
"                                                And OP.CustomerSupplierType = 1"
"        Join BusinessPartner BP ON OP.OrderBusinessPartnerNumberId = BP.NumberId "
"        where pi.invoicedate between '"+str(LDStartDate)+"' and '"+str(LDEndDate)+"'"+LSCompany+LSParty+LSBrokerGroup+" "
"        group by BP.Legalname1,AgGrp.LONGDESCRIPTION,Plant.LONGDESCRIPTION "
" Order By agentgroup ")
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    print(type(stdt))
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt4.textsize(pdfrpt4.c, result, pdfrpt4.d, stdt, etdt)
        pdfrpt4.d = pdfrpt4.dvalue(stdt, etdt, pdfrpt4.divisioncode)
        result = con.db.fetch_both(stmt)

    if pdfrpt4.d < 20:
        pdfrpt4.d = 730
        pdfrpt4.c.showPage()
        pdfrpt4.header(stdt, etdt, pdfrpt4.divisioncode)

    if result == False:
        global Exceptions
    if counter>0:
        pdfrpt4.d = pdfrpt4.dlocvalue(pdfrpt4.d)
        pdfrpt4.fonts(7)
        # pdfrpt4.c.drawString(10, pdfrpt4.d, str(pdfrpt4.divisioncode[-2]) + " TOTAL : ")
        # pdfrpt4.c.drawAlignedString(570, pdfrpt4.d, str("%.2f" % float(pdfrpt4.CompanyAmountTotal)))
        pdfrpt4.companyclean()
        Exceptions = ""
    elif counter == 0:
        Exceptions = "Note: Please Select Valid Credentials"
        return

    pdfrpt4.c.setPageSize(pdfrpt4.A4)
    pdfrpt4.c.showPage()
    pdfrpt4.c.save()
    pdfrpt4.newrequest()