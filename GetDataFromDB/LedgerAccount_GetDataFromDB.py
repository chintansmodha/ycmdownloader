from PrintPDF import   LedgerAccount_PrintPDF as pdfrpt
from PrintPDF import LedgerAccount_Ledger_PrintPDF as pdfrpt1
from Global_Files import Connection_String as con
from PrintPDF import LedgerAccount_TrialBalance_PrintPDF as pdfrpt2
from datetime import datetime
def LedgerAccount_GetDataSummary(LSCompany,LCCompany,GLCode,startdate,enddate,reportName):
    print("IN Summary")
    if not LCCompany and not LSCompany or LCCompany:
        LSCompany = " "
    elif LSCompany:
        LSCompany = " AND finbusinessunit.CODE in (" + str(LSCompany)[1:-1] + ")"

    sql = ("Select  finbusinessunit.Longdescription As divcode, "
                   "COALESCE(BUSINESSPARTNER.LegalName1,'') As Party," 
         "Sum(cast(Case When FinDocument.FINANCEDOCUMENTDATE <'"+startdate+"'" 
         " Then findocumentline.AMOUNTINCC Else 0 End as decimal(18,2))) As OpBal," 
         "Sum(cast(Case When findocumentline.AMOUNTINCC > 0 And FinDocument.FINANCEDOCUMENTDATE" 
         " Between '"+startdate+"' And '"+enddate+"' Then findocumentline.AMOUNTINCC Else 0 End as decimal(18,2))) As DrAmount," 
         "Abs(Sum(cast(Case When findocumentline.AMOUNTINCC < 0 And FinDocument.FINANCEDOCUMENTDATE Between '"+startdate+"' And '"+enddate+"'" 
         " Then findocumentline.AMOUNTINCC Else 0 End as decimal(18,2)))) As CrAmount," 
         "Sum(cast(findocumentline.AMOUNTINCC as decimal(18,2))) As ClBal" 
         " from findocumentline" 
         " join findocument on findocumentline.FINDOCUMENTCOMPANYCODE = findocument.COMPANYCODE" 
         " AND findocumentline.FINDOCUMENTBUSINESSUNITCODE = findocument.BUSINESSUNITCODE" 
         " AND findocumentline.FINDOCUMENTFINANCIALYEARCODE = findocument.FINANCIALYEARCODE" 
         " AND findocumentline.FINDOCDOCUMENTTEMPLATECODE = findocument.DOCUMENTTEMPLATECODE" 
         " AND findocumentline.FINDOCUMENTCODE = findocument.CODE" 
         " join finbusinessunit on findocument.BUSINESSUNITCODE = finbusinessunit.code" 
         " Join FINFinancialYear FInYear On FinYear.Code = FinDocument.FINANCIALYEARCODE" 
         " join glmaster on findocumentline.glcode = glmaster.code" 
         " Left join orderpartner on  findocumentline.SLCUSTOMERSUPPLIERTYPE =orderpartner.CUSTOMERSUPPLIERTYPE" 
         " AND findocumentline.SLCUSTOMERSUPPLIERCODE = orderpartner.CUSTOMERSUPPLIERCODE" 
         " Left join businesspartner on ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID" 
         " Where   FinDocument.FINANCEDOCUMENTDATE Between '"+startdate+"' And '"+enddate+"' " 
         " "+LSCompany+GLCode+"" 
         " Group By finbusinessunit.Longdescription,COALESCE(BUSINESSPARTNER.LegalName1,'')"
         " order by  finbusinessunit.Longdescription,COALESCE(BUSINESSPARTNER.LegalName1,'')")
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d,reportName,startdate,enddate)
        pdfrpt.d = pdfrpt.dvalue(pdfrpt.divisioncode,result,reportName,startdate,enddate)
        result = con.db.fetch_both(stmt)
    pdfrpt.c.line(0, pdfrpt.d, 600, pdfrpt.d)
    pdfrpt.printTotal(pdfrpt.d-10)
    pdfrpt.c.line(0, pdfrpt.d-20, 600, pdfrpt.d-20)
    pdfrpt.companyclean()
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    pdfrpt.d = pdfrpt.newpage()



def LedgerAccount_GetDataLedger(LSCompany,LCCompany,GLCode,startdate,enddate,reportName):
    if not LCCompany and not LSCompany or LCCompany:
        LSCompany = " "
    elif LSCompany:
        LSCompany = " and finbusinessunit.CODE in (" + str(LSCompany)[1:-1] + ")"

    sql = "Select  finbusinessunit.LongDescription As Divcode, "\
          " GLMaster.LongDescription As bank"\
          ",findocumentline.FINDOCDOCUMENTTEMPLATECODE as doctype,"\
           "        COALESCE(BUSINESSPARTNER.LegalName1,'') As party, findocument.code as vchno,"\
            "        VARCHAR_FORMAT(findocument.FINANCEDOCUMENTDATE, 'DD-MM-YYYY') as vchdate"\
             "        ,COALESCE(findocument.CHEQUENUMBER,'') as  chqno, "\
         " (cast(Case When findocumentline.AMOUNTINCC > 0 And FinDocument.FINANCEDOCUMENTDATE"\
         " Between '"+startdate+"' And '"+enddate+"' Then findocumentline.AMOUNTINCC Else 0 End as decimal(18,2))) As DrAmount," \
         "Abs((cast(Case When findocumentline.AMOUNTINCC < 0 And FinDocument.FINANCEDOCUMENTDATE Between '"+startdate+"' And '"+enddate+"'" \
         " Then findocumentline.AMOUNTINCC Else 0 End as decimal(18,2)))) As CrAmount," \
          "           cast(findocumentline.AMOUNTINCC as decimal(18,2)) As ClBal" \
          " , PI.CODE as INVNO"\
          ",PI.INVOICEDATE as INVOICEDATE" \
          " from findocumentline " \
          " join findocument on findocumentline.FINDOCUMENTCOMPANYCODE = findocument.COMPANYCODE " \
          " AND findocumentline.FINDOCUMENTBUSINESSUNITCODE = findocument.BUSINESSUNITCODE" \
          " AND findocumentline.FINDOCUMENTFINANCIALYEARCODE = findocument.FINANCIALYEARCODE" \
          " AND findocumentline.FINDOCDOCUMENTTEMPLATECODE = findocument.DOCUMENTTEMPLATECODE " \
          " AND findocumentline.FINDOCUMENTCODE = findocument.CODE " \
          "Left JOIN    PlantInvoice PI                 ON findocument.BUSINESSUNITCODE  = PI.FINDOCBUSINESSUNITCODE" \
        " AND findocument.CODE = PI.FINDOCCODE" \
        " AND findocument.FINANCIALYEARCODE = PI.FINDOCFINANCIALYEARCODE" \
        " AND findocument.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE" \
          " join finbusinessunit on findocument.BUSINESSUNITCODE = finbusinessunit.code " \
          " join glmaster on findocumentline.glcode = glmaster.code" \
          " Left join orderpartner on  findocumentline.SLCUSTOMERSUPPLIERTYPE =orderpartner.CUSTOMERSUPPLIERTYPE" \
          " AND findocumentline.SLCUSTOMERSUPPLIERCODE = orderpartner.CUSTOMERSUPPLIERCODE " \
          " Left join businesspartner on ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID " \
          " Where   FinDocument.FINANCEDOCUMENTDATE between '" + startdate + "' And '" + enddate + "' " + LSCompany + GLCode+" " \
          " order by  finbusinessunit.LongDescription,BUSINESSPARTNER.LegalName1,findocument.FINANCEDOCUMENTDATE"
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        pdfrpt1.textsize(pdfrpt1.c, result, pdfrpt1.d,reportName,startdate,enddate)
        pdfrpt1.d = pdfrpt1.dvalue(pdfrpt1.divisioncode,result,reportName,startdate,enddate)
        result = con.db.fetch_both(stmt)
    pdfrpt.c.line(0, pdfrpt.d, 850, pdfrpt.d)
    pdfrpt.printTotal(pdfrpt.d-10)
    pdfrpt.c.line(0, pdfrpt.d-20, 850, pdfrpt.d-20)
    pdfrpt1.c.setPageSize(pdfrpt1.landscape(pdfrpt1.A4))
    pdfrpt1.c.showPage()
    pdfrpt1.c.save()
    pdfrpt1.newrequest()
    pdfrpt1.d = pdfrpt1.newpage()

def trialBalance(LSCompany,LCCompany,startdate,enddate,reportName,opbal):
    if not LCCompany and not LSCompany or LCCompany:
        LSCompany = " "
    elif LSCompany:
        LSCompany = " and finbusinessunit.CODE in (" + str(LSCompany)[1:-1] + ")"
    print
    sql = ("Select finbusinessunit.LONGDESCRIPTION as company "
        " ,Case When glmaster.GLType = 'A' Then 'Assets'  "
           " When glmaster.GLType = 'L' Then 'Liabilities'  "
           " When glmaster.GLType = 'I' Then 'Income'  "
           " When glmaster.GLType = 'E' Then 'Expenses' End as GLTYPE "
        " ,substr(GLMASTER.CODE,1,6) as MainAccount "
        " ,GLMaster.longdescription as account "
        " ,cast(Sum(Case When FD.POSTINGDATE <'2023-02-01'   "
          " Then FD.DOCUMENTAMOUNT Else 0 End)as decimal(18,2)) As OpBal   "
          " , cast(Sum(Case When FODT.CLEAREDAMOUNT > 0 And FODT.TRANSACTIONDATE   "
          " Between  '2023-02-01'  And  '2023-02-20'  Then FODT.CLEAREDAMOUNT Else 0 End)as decimal(18,2)) As DrAmount   "
          " , cast(Abs(Sum(Case When FODT.CLEAREDAMOUNT < 0 And FODT.TRANSACTIONDATE Between  '2023-02-01'  And  '2023-02-20'    "
          " Then FODT.CLEAREDAMOUNT Else 0 End)) as decimal(18,2)) As CrAmount "
         " ,sum(Case When FD.POSTINGDATE <'2023-02-01' Then FD.DOCUMENTAMOUNT Else 0 End +  "
         " Case When FODT.CLEAREDAMOUNT > 0 And FODT.TRANSACTIONDATE Between  '2023-02-01'  And  '2023-02-20'  Then FODT.CLEAREDAMOUNT Else 0 End "
         " -Abs(Case When FODT.CLEAREDAMOUNT < 0 And FODT.TRANSACTIONDATE Between  '2023-02-01'  And  '2023-02-20' Then FODT.CLEAREDAMOUNT Else 0 End)) as bal "
" from FinOpenDocumentsTransactions as FODT "
" Join Findocument as FD       On FODT.ORIGINCODE = FD.CODE  "
                                 " And FODT.ORIGINDOCUMENTTEMPLATECODE = FD.DOCUMENTTEMPLATECODE  "
                                 " And FODT.ORIGINFINANCIALYEARCODE = FD.FINANCIALYEARCODE  "
                                 " And FODT.ORIGINBUSINESSUNITCODE = FD.BUSINESSUNITCODE "
" join finbusinessunit on FD.BUSINESSUNITCODE = finbusinessunit.code "
" Join GLMaster               on FD.GLCODE = GLMaster.code "
          " Where   FODT.TRANSACTIONDATE between '" + startdate + "' And '" + enddate + "' " + LSCompany +" "
          "  Group by finbusinessunit.LONGDESCRIPTION,glmaster.GLType,substr(GLMASTER.CODE,1,6),GLMaster.longdescription"
          " order by  finbusinessunit.LONGDESCRIPTION,glmaster.GLType,substr(GLMASTER.CODE,1,6),GLMaster.longdescription")
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    stdt = datetime.strptime(startdate, '%Y-%m-%d').date()
    etdt = datetime.strptime(enddate, '%Y-%m-%d').date()
    while result != False:
        pdfrpt2.textsize(pdfrpt2.c, result, pdfrpt2.d,opbal,stdt,etdt)
        pdfrpt2.d = pdfrpt2.dvalue(pdfrpt2.divisioncode,result,opbal,stdt,etdt)
        result = con.db.fetch_both(stmt)
    pdfrpt.c.line(0, pdfrpt.d, 850, pdfrpt.d)
    pdfrpt.printTotal(pdfrpt.d-10)
    pdfrpt.c.line(0, pdfrpt.d-20, 850, pdfrpt.d-20)
    pdfrpt2.c.setPageSize(pdfrpt2.landscape(pdfrpt2.A4))
    pdfrpt2.c.showPage()
    pdfrpt2.c.save()
    pdfrpt2.newrequest()
    pdfrpt2.d = pdfrpt2.newpage()