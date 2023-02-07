from datetime import datetime
from Global_Files import Connection_String as con
from FormLoad import TransporterWiseDispatch_FormLoad as views
from PrintPDF import TWDD_PrintPDF as pdfrpt1
from PrintPDF import TWDS_PrintPDF as pdfrpt2
from PrintPDF import TWPWDD_PrintPDF as pdfrpt3
from PrintPDF import TWPWDS_PrintPDF as pdfrpt4

def TWDDGDFDB(LSCompany,LSBranch,LSTransporter,LSDispatch,LSParty,LSAllCompany,LSAllBranch,LSAllTransporter,LSAllDispatch,LSAllParty,LDStartDate,LDEndDate,LSReportType):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.Code in ("+str(LSCompany)[1:-1]+")"
    if not LSAllBranch and not LSBranch or LSAllBranch:
        LSBranch = ""
    elif LSBranch:
        LSBranch = " And xyz.Code in ("+str(LSBranch)[1:-1]+")"
    if not LSAllTransporter and not LSTransporter or LSAllTransporter:
        LSTransporter = ""
    elif LSTransporter:
        LSTransporter = " And xyz.Code in ("+str(LSTransporter)[1:-1]+")"
    if not LSAllDispatch and not LSDispatch or LSAllDispatch:
        LSDispatch = ""
    elif LSDispatch:
        LSDispatch = " And xyz.Code in ("+str(LSDispatch)[1:-1]+")"
    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And xyz.Code in ("+str(LSParty)[1:-1]+")"
    
    sql=("Select  PI.code                       AS InvoiceNo"
        " ,TR_BP.Legalname1 as Transporter  "
        " ,BP.legalname1 as Party "
        " ,Cast(sum(PI.NETTVALUE) as decimal(18,2))  as Quantity "
        " ,Cast(COALESCE(sum(Freight.Value),0) As decimal(18,2)) AS Freight  "
        " ,PI.LRNO "
        " ,PI.LRDATE "
        " ,COALESCE(TZ.Longdescription,'') as Despatch "
" from PlantInvoice as PI "
" Join    PLANTINVOICELINE PIL            ON      PI.CODE = PIL.PLANTINVOICECODE "
" Join Plant on PI.FACTORYCODE = Plant.Code "
" join OrderPartner as OP    On      PI.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OP.CUSTOMERSUPPLIERTYPE  "
                                  " And     PI.BUYERIFOTCCUSTOMERSUPPLIERCODE = OP.CUSTOMERSUPPLIERCODE   "
" join BusinessPartner as BP  On     OP.OrderbusinessPartnerNumberId = BP.NumberID "
 " "
" join OrderPartner as TR_OP    On      PI.TRANSPORTERCODCSMSUPPLIERTYPE = TR_OP.CUSTOMERSUPPLIERTYPE  "
                                  " And     PI.TRANSPORTERCODCSMSUPPLIERCODE = TR_OP.CUSTOMERSUPPLIERCODE   "
" join BusinessPartner as TR_BP  On     TR_OP.OrderbusinessPartnerNumberId = TR_BP.NumberID "
 " "
" Left Join TransportZone  TZ       ON  TR_BP.Transportzonecode = TZ.Code     "
" Left Join    INDTAXDETAIL Freight       ON      PIL.ABSUNIQUEID = Freight.ABSUNIQUEID   "
          " And     Freight.ITAXCODE = 'FRT'   "
          " And     Freight.TAXCATEGORYCODE = 'GFR' "
          "Where PI.Invoicedate between '"+LDStartDate+"' and '"+LDEndDate+"'"
" Group By TR_BP.Legalname1,TZ.Longdescription,BP.legalname1,PI.LRDATE, PI.LRNO, PI.Code"
" order by Transporter,Despatch,LRDate")

    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        pdfrpt1.textsize(pdfrpt1.c,result, pdfrpt1.d, stdt, etdt)
        pdfrpt1.d = pdfrpt1.dvalue(stdt, etdt, pdfrpt1.transporter)
        result = con.db.fetch_both(stmt)  
    if pdfrpt1.d < 20:
        pdfrpt1.d = 740
        pdfrpt1.c.showPage()
        pdfrpt1.header(stdt, etdt, pdfrpt1.transporter)
    if result == False:
        pdfrpt1.d = pdfrpt1.dlocvalue(pdfrpt1.d)
        pdfrpt1.fonts(7)
        pdfrpt1.c.drawString(10, pdfrpt1.d, str(pdfrpt1.transporter[-1]) + " TOTAL : ")
        pdfrpt1.companyclean()
    elif counter == 0:
        views.Exceptions = "Note: Please Select Valid Credentials"
        return
    pdfrpt1.c.setPageSize(pdfrpt1.A4)
    pdfrpt1.c.showPage()
    pdfrpt1.c.save()

def TWDSGDFDB(LSCompany,LSBranch,LSTransporter,LSDispatch,LSParty,LSAllCompany,LSAllBranch,LSAllTransporter,LSAllDispatch,LSAllParty,LDStartDate,LDEndDate,LSReportType):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.Code in ("+str(LSCompany)[1:-1]+")"
    if not LSAllBranch and not LSBranch or LSAllBranch:
        LSBranch = ""
    elif LSBranch:
        LSBranch = " And xyz.Code in ("+str(LSBranch)[1:-1]+")"
    if not LSAllTransporter and not LSTransporter or LSAllTransporter:
        LSTransporter = ""
    elif LSTransporter:
        LSTransporter = " And xyz.Code in ("+str(LSTransporter)[1:-1]+")"
    if not LSAllDispatch and not LSDispatch or LSAllDispatch:
        LSDispatch = ""
    elif LSDispatch:
        LSDispatch = " And xyz.Code in ("+str(LSDispatch)[1:-1]+")"
    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And xyz.Code in ("+str(LSParty)[1:-1]+")"
    
    sql=(
        " Select  Plant.Longdescription                       AS Company "
        " ,TR_BP.Legalname1 as Transporter  "
        " ,Cast(sum(PI.NETTVALUE) as decimal(18,2))  as Quantity "
        " ,Cast(COALESCE(sum(Freight.Value),0) As decimal(18,2)) AS Freight  "
" from PlantInvoice as PI "
" Join    PLANTINVOICELINE PIL            ON      PI.CODE = PIL.PLANTINVOICECODE "
" Join Plant on PI.FACTORYCODE = Plant.Code "
" join OrderPartner as TR_OP    On      PI.TRANSPORTERCODCSMSUPPLIERTYPE = TR_OP.CUSTOMERSUPPLIERTYPE  "
                                  " And     PI.TRANSPORTERCODCSMSUPPLIERCODE = TR_OP.CUSTOMERSUPPLIERCODE   "
" join BusinessPartner as TR_BP  On     TR_OP.OrderbusinessPartnerNumberId = TR_BP.NumberID     "
" Left Join    INDTAXDETAIL Freight       ON      PIL.ABSUNIQUEID = Freight.ABSUNIQUEID   "
          " And     Freight.ITAXCODE = 'FRT'   "
          " And     Freight.TAXCATEGORYCODE = 'GFR' "
" Group By Plant.Longdescription,TR_BP.Legalname1 "
" Order By Plant.Longdescription,TR_BP.Legalname1"
     )
	
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        pdfrpt2.textsize(pdfrpt2.c, result, pdfrpt2.d, stdt, etdt)
        pdfrpt2.d = pdfrpt2.dvalue(stdt, etdt, pdfrpt2.transporter)
        result = con.db.fetch_both(stmt)  
    if pdfrpt2.d < 20:
        pdfrpt2.d = 740
        pdfrpt2.c.showPage()
        pdfrpt2.header(stdt, etdt, pdfrpt2.transporter)
    if result == False:
        pdfrpt2.d = pdfrpt2.dlocvalue(pdfrpt2.d)
        pdfrpt2.fonts(7)
        pdfrpt2.c.drawString(10, pdfrpt2.d, str(pdfrpt2.transporter[-1]) + " TOTAL : ")
        pdfrpt2.companyclean()
        views.Exceptions = ""
    elif counter == 0:
        views.Exceptions = "Note: Please Select Valid Credentials"
        return
    pdfrpt2.c.setPageSize(pdfrpt2.A4)
    pdfrpt2.c.showPage()
    pdfrpt2.c.save()
def TWPWDDGDFDB(LSCompany,LSBranch,LSTransporter,LSDispatch,LSParty,LSAllCompany,LSAllBranch,LSAllTransporter,LSAllDispatch,LSAllParty,LDStartDate,LDEndDate,LSReportType):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.Code in ("+str(LSCompany)[1:-1]+")"
    if not LSAllBranch and not LSBranch or LSAllBranch:
        LSBranch = ""
    elif LSBranch:
        LSBranch = " And xyz.Code in ("+str(LSBranch)[1:-1]+")"
    if not LSAllTransporter and not LSTransporter or LSAllTransporter:
        LSTransporter = ""
    elif LSTransporter:
        LSTransporter = " And xyz.Code in ("+str(LSTransporter)[1:-1]+")"
    if not LSAllDispatch and not LSDispatch or LSAllDispatch:
        LSDispatch = ""
    elif LSDispatch:
        LSDispatch = " And xyz.Code in ("+str(LSDispatch)[1:-1]+")"
    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And xyz.Code in ("+str(LSParty)[1:-1]+")"
    
    sql=( )
	
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt1.textsize(result, pdfrpt1.d, stdt, etdt)
        pdfrpt1.d = pdfrpt1.dvalue(stdt, etdt, pdfrpt1.divisioncode)
        result = con.db.fetch_both(stmt)  
    if pdfrpt1.d < 20:
        pdfrpt1.d = 740
        pdfrpt1.c.showPage()
        pdfrpt1.header(stdt, etdt, pdfrpt1.divisioncode)
    if result == False:
        global Exceptions
    if counter>0:
        pdfrpt1.d = pdfrpt1.dlocvalue(pdfrpt1.d)
        pdfrpt1.fonts(7)
        pdfrpt1.c.drawString(10, pdfrpt1.d, str(pdfrpt1.divisioncode[-2]) + " TOTAL : ")
        pdfrpt1.companyclean()
        views.Exceptions = ""
    elif counter == 0:
        views.Exceptions = "Note: Please Select Valid Credentials"
        return
    pdfrpt1.c.setPageSize(pdfrpt1.landscape(pdfrpt1.A4))
    pdfrpt1.c.showPage()
    pdfrpt1.c.save()
def TWPWDSGDFDB(LSCompany,LSBranch,LSTransporter,LSDispatch,LSParty,LSAllCompany,LSAllBranch,LSAllTransporter,LSAllDispatch,LSAllParty,LDStartDate,LDEndDate,LSReportType):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.Code in ("+str(LSCompany)[1:-1]+")"
    if not LSAllBranch and not LSBranch or LSAllBranch:
        LSBranch = ""
    elif LSBranch:
        LSBranch = " And xyz.Code in ("+str(LSBranch)[1:-1]+")"
    if not LSAllTransporter and not LSTransporter or LSAllTransporter:
        LSTransporter = ""
    elif LSTransporter:
        LSTransporter = " And xyz.Code in ("+str(LSTransporter)[1:-1]+")"
    if not LSAllDispatch and not LSDispatch or LSAllDispatch:
        LSDispatch = ""
    elif LSDispatch:
        LSDispatch = " And xyz.Code in ("+str(LSDispatch)[1:-1]+")"
    if not LSAllParty and not LSParty or LSAllParty:
        LSParty = ""
    elif LSParty:
        LSParty = " And xyz.Code in ("+str(LSParty)[1:-1]+")"
    
    sql=( )
	
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt1.textsize(result, pdfrpt1.d, stdt, etdt)
        pdfrpt1.d = pdfrpt1.dvalue(stdt, etdt, pdfrpt1.divisioncode)
        result = con.db.fetch_both(stmt)  
    if pdfrpt1.d < 20:
        pdfrpt1.d = 740
        pdfrpt1.c.showPage()
        pdfrpt1.header(stdt, etdt, pdfrpt1.divisioncode)
    if result == False:
        global Exceptions
    if counter>0:
        pdfrpt1.d = pdfrpt1.dlocvalue(pdfrpt1.d)
        pdfrpt1.fonts(7)
        pdfrpt1.c.drawString(10, pdfrpt1.d, str(pdfrpt1.divisioncode[-2]) + " TOTAL : ")
        pdfrpt1.companyclean()
        views.Exceptions = ""
    elif counter == 0:
        views.Exceptions = "Note: Please Select Valid Credentials"
        return
    pdfrpt1.c.setPageSize(pdfrpt1.landscape(pdfrpt1.A4))
    pdfrpt1.c.showPage()
    pdfrpt1.c.save()