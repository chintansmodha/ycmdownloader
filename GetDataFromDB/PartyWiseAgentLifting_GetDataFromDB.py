from Global_Files import Connection_String as con
from datetime import datetime
from PrintPDF import PartyWiseAgentLiftingMiniatureCopy_PrintPDF as pdfrpt1
from PrintPDF import PartWiseAgentLiftingNo_PrintPDF as pdfrpt2
counter=0


def PWALGDFDBYES(LSCompany,LSAllCompany,LSParty,LSAllParty,LSYarnType,LSAllYarnType,LDStartDate,LDEndDate,LSSalesTax,LSAllSalesTax):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"

    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

    if not LSAllYarnType and not LSYarnType or LSAllYarnType:
        LSYarnType=""
    elif LSYarnType:
        LSYarnType= " And ITEMTYPE.CODE in("+str(LSYarnType)[1:-1]+")"

    if not LSAllSalesTax and not LSSalesTax or LSAllSalesTax:
        LSSalesTax=""
    elif LSSalesTax:
        LSSalesTax= " And ITax.CODE in("+str(LSSalesTax)[1:-1]+")"
    

    sql=("select  Plant.Longdescription as company"
        " ,cast(PIL.PRICE as decimal(18,2)) as Rate"
        " ,cast(PI.totalquantity as decimal(18,3)) as quantity"
        " ,cast(pi.BASICVALUE as decimal(18,2)) as amount "
        " ,PI.COde as invno"
        " ,PI.INvoicedate as invdate"
        " ,PI.LRNO"
        " ,product.longdescription as item"
        " ,BP_Trpt.legalname1 as transporter"
        " ,AgGrp.LONGDESCRIPTION as agentgroup"
        " ,BP.legalname1 as party"
" From PlantInvoice as PI        "
        " Join Plant                              ON PI.FactoryCode = Plant.code "
            " JOIN plantinvoiceline as PIL "
                                                    " ON PI.code = PIL.plantinvoicecode "
                                                    " AND PI.divisioncode =                 PIL.plantinvoicedivisioncode "
                                                    " AND PI.invoicedate = PIL.invoicedate "
     " JOIN fullitemkeydecoder FIKD  "
                       " ON PIL.itemtypecode = FIKD.itemtypecode  "
                          " AND COALESCE(PIL.subcode01, '') =                COALESCE(FIKD.subcode01, '')  "
                          " AND COALESCE(PIL.subcode02, '') =                COALESCE(FIKD.subcode02, '')  "
                          " AND COALESCE(PIL.subcode03, '') =                COALESCE(FIKD.subcode03, '')  "
                          " AND COALESCE(PIL.subcode04, '') =                COALESCE(FIKD.subcode04, '')  "
                          " AND COALESCE(PIL.subcode05, '') =                COALESCE(FIKD.subcode05, '')  "
                          " AND COALESCE(PIL.subcode06, '') =                COALESCE(FIKD.subcode06, '')  "
                          " AND COALESCE(PIL.subcode07, '') =                COALESCE(FIKD.subcode07, '')  "
                          " AND COALESCE(PIL.subcode08, '') =                COALESCE(FIKD.subcode08, '')  "
                          " AND COALESCE(PIL.subcode09, '') =                COALESCE(FIKD.subcode09, '')  "
                          " AND COALESCE(PIL.subcode10, '') =                COALESCE(FIKD.subcode10, '')  "
     " JOIN product    ON PIL.itemtypecode = product.itemtypecode  "
                    " AND FIKD.itemuniqueid = product.absuniqueid  "
                   " Join    AgentsGroupDetail AGD           On      PI.Agent1Code = AGD.AgentCode "
            " Join    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code  "
" Left join OrderPartner OP_Trpt    On      PI.TRANSPORTERCODCSMSUPPLIERTYPE = OP_Trpt.CUSTOMERSUPPLIERTYPE"
                                       " And     PI.TRANSPORTERCODCSMSUPPLIERCODE = OP_Trpt.CUSTOMERSUPPLIERCODE "
     " Left join BusinessPartner BP_Trpt  On     OP_Trpt.OrderbusinessPartnerNumberId = BP_Trpt.NumberID "
     " join OrderPartner OP                    ON      PI.BUYERIFOTCCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode "
          " AND     PI.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OP.CustomerSupplierType "
          " join BusinessPartner BP                 ON      OP.OrderbusinessPartnerNumberId =  BP.NumberID "
          " join indtaxdetail as IT on PI.AbsUniqueID  = IT.AbsUniqueID "
          " Join ITAX on IT.ITAXCODE  =ITAX.CODE "
          " where pi.invoicedate between '"+str(LDStartDate)+"' and '"+str(LDEndDate)+"'"+LSCompany+LSParty+LSYarnType+LSSalesTax+" "  
    " Order By agentgroup ")
    

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    print(type(stdt))
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    
    
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt1.textsize(pdfrpt1.c, result, pdfrpt1.d, stdt, etdt)
        pdfrpt1.d = pdfrpt1.dvalue(stdt, etdt, pdfrpt1.divisioncode)
        result = con.db.fetch_both(stmt)
    if  result == False:
        pdfrpt1.d =pdfrpt1.dvalue(stdt, etdt, pdfrpt1.divisioncode)
        pdfrpt1.d =pdfrpt1.dvalue(stdt, etdt, pdfrpt1.divisioncode)
        pdfrpt1.partytotalprint(pdfrpt1.d,stdt,etdt)
        pdfrpt1.d =pdfrpt1.dvalue(stdt, etdt, pdfrpt1.divisioncode)
        pdfrpt1.d =pdfrpt1.dvalue(stdt, etdt, pdfrpt1.divisioncode)
        pdfrpt1.brokertotalprint(pdfrpt1.d,stdt,etdt)
        
    if pdfrpt1.d < 20:
        pdfrpt1.d = 730
        pdfrpt1.c.showPage()
        pdfrpt1.header(stdt, etdt, pdfrpt1.divisioncode)

    pdfrpt1.c.setPageSize(pdfrpt1.landscape(pdfrpt1.A4))
    pdfrpt1.c.showPage()
    pdfrpt1.c.save()
    pdfrpt1.newrequest()

def PWALGDFDBNO(LSCompany,LSAllCompany,LSParty,LSAllParty,LSYarnType,LSAllYarnType,LDStartDate,LDEndDate,LSSalesTax,LSAllSalesTax):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"

    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

    if not LSAllYarnType and not LSYarnType or LSAllYarnType:
        LSYarnType=""
    elif LSYarnType:
        LSYarnType= " And ITEMTYPE.CODE in("+str(LSYarnType)[1:-1]+")"

    if not LSAllSalesTax and not LSSalesTax or LSAllSalesTax:
        LSSalesTax=""
    elif LSSalesTax:
        LSSalesTax= " And ITax.CODE in("+str(LSSalesTax)[1:-1]+")"
    

    sql=("select  Plant.Longdescription as company"
        " ,cast(PIL.PRICE as decimal(18,2)) as Rate"
        " ,cast(PI.totalquantity as decimal(18,3)) as quantity"
        " ,cast(pi.BASICVALUE as decimal(18,2)) as amount "
        " ,PI.COde as invno"
        " ,PI.INvoicedate as invdate"
        " ,PI.LRNO"
        " ,product.longdescription as item"
        " ,BP_Trpt.legalname1 as transporter"
        " ,AgGrp.LONGDESCRIPTION as agentgroup"
        " ,BP.legalname1 as party"
" From PlantInvoice as PI        "
        " Join Plant                              ON PI.FactoryCode = Plant.code "
            " JOIN plantinvoiceline as PIL "
                                                    " ON PI.code = PIL.plantinvoicecode "
                                                    " AND PI.divisioncode =                 PIL.plantinvoicedivisioncode "
                                                    " AND PI.invoicedate = PIL.invoicedate "
     " JOIN fullitemkeydecoder FIKD  "
                       " ON PIL.itemtypecode = FIKD.itemtypecode  "
                          " AND COALESCE(PIL.subcode01, '') =                COALESCE(FIKD.subcode01, '')  "
                          " AND COALESCE(PIL.subcode02, '') =                COALESCE(FIKD.subcode02, '')  "
                          " AND COALESCE(PIL.subcode03, '') =                COALESCE(FIKD.subcode03, '')  "
                          " AND COALESCE(PIL.subcode04, '') =                COALESCE(FIKD.subcode04, '')  "
                          " AND COALESCE(PIL.subcode05, '') =                COALESCE(FIKD.subcode05, '')  "
                          " AND COALESCE(PIL.subcode06, '') =                COALESCE(FIKD.subcode06, '')  "
                          " AND COALESCE(PIL.subcode07, '') =                COALESCE(FIKD.subcode07, '')  "
                          " AND COALESCE(PIL.subcode08, '') =                COALESCE(FIKD.subcode08, '')  "
                          " AND COALESCE(PIL.subcode09, '') =                COALESCE(FIKD.subcode09, '')  "
                          " AND COALESCE(PIL.subcode10, '') =                COALESCE(FIKD.subcode10, '')  "
     " JOIN product    ON PIL.itemtypecode = product.itemtypecode  "
                    " AND FIKD.itemuniqueid = product.absuniqueid  "
                   " Join    AgentsGroupDetail AGD           On      PI.Agent1Code = AGD.AgentCode "
            " Join    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code  "
" Left join OrderPartner OP_Trpt    On      PI.TRANSPORTERCODCSMSUPPLIERTYPE = OP_Trpt.CUSTOMERSUPPLIERTYPE"
                                       " And     PI.TRANSPORTERCODCSMSUPPLIERCODE = OP_Trpt.CUSTOMERSUPPLIERCODE "
     " Left join BusinessPartner BP_Trpt  On     OP_Trpt.OrderbusinessPartnerNumberId = BP_Trpt.NumberID "
     " join OrderPartner OP                    ON      PI.BUYERIFOTCCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode "
          " AND     PI.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OP.CustomerSupplierType "
          " join BusinessPartner BP                 ON      OP.OrderbusinessPartnerNumberId =  BP.NumberID "
          " join indtaxdetail as IT on PI.AbsUniqueID  = IT.AbsUniqueID "
          " Join ITAX on IT.ITAXCODE  =ITAX.CODE "
          " where pi.invoicedate between '"+str(LDStartDate)+"' and '"+str(LDEndDate)+"'"+LSCompany+LSParty+LSYarnType+LSSalesTax+" "  
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
        if  result == False:
            pdfrpt2.d =pdfrpt2.dvalue(stdt, etdt, pdfrpt2.divisioncode)
            pdfrpt2.d =pdfrpt2.dvalue(stdt, etdt, pdfrpt2.divisioncode)
            pdfrpt2.partytotalprint(pdfrpt2.d,stdt,etdt)
            pdfrpt2.d =pdfrpt2.dvalue(stdt, etdt, pdfrpt2.divisioncode)
            pdfrpt2.d =pdfrpt2.dvalue(stdt, etdt, pdfrpt2.divisioncode)
            pdfrpt2.brokertotalprint(pdfrpt2.d,stdt,etdt)

    if pdfrpt2.d < 20:
        pdfrpt2.d = 730
        pdfrpt2.c.showPage()
        pdfrpt2.header(stdt, etdt, pdfrpt2.divisioncode)

    if result == False:
        global Exceptions
    if counter>0:
        pdfrpt2.d = pdfrpt2.dlocvalue(pdfrpt2.d)
        pdfrpt2.fonts(7)
        pdfrpt2.companyclean()
        Exceptions = ""
    elif counter == 0:
        Exceptions = "Note: Please Select Valid Credentials"
        return

    pdfrpt2.c.setPageSize(pdfrpt2.landscape(pdfrpt2.A4))
    pdfrpt2.c.showPage()
    pdfrpt2.c.save()
    pdfrpt2.newrequest()
