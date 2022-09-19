from datetime import datetime
from ProcessSelection import SummerizedBankBalance_ProcessSelection as SBBV
from Global_Files import Connection_String as con
from PrintPDF import SummerizedBankBalance_PrintPDF as pdfrpt

counter=0

def SummerizedBankBalance_PrintPDF(LSCompany,LDStartDate,LDEndDate,LCCompany):
    global ClosingBalance

    Company = str(LSCompany)
    Company = '(' + Company[1:-1] + ')'
    StartDate = "'"+LDStartDate+"'"
    EndDate = "'" + LDEndDate + "'"
    if not LCCompany and not LSCompany:
        Company = " "
    elif LCCompany:
        Company = " "
    elif LSCompany:
        Company = "AND FinBusinessUnit.CODE in " + Company


    sql = " Select  Company.LongDescription As BUSINESSUNITName, BankMaster.LongDescription As BankName," \
          " Sum(Case When FinDocument.FinanceDocumentDate < "+StartDate+" " \
          " Then FinDocument.DocumentAmount * Case When DocumentTypeCode In ('BR','CR') Then 1 Else -1 End Else 0 End) As OpBal," \
          " Sum(Case When FinDocument.FinanceDocumentDate >= "+StartDate+"" \
          " And FinDocument.DocumentTypeCode In ('BR','CR') Then FinDocument.DocumentAmount Else 0 End) as Receipts" \
          " , Sum(Case When FinDocument.FinanceDocumentDate >= "+StartDate+"" \
          " And FinDocument.DocumentTypeCode In ('BP','CP') Then FinDocument.DocumentAmount Else 0 End) as Payments" \
          " , '' as RecievedFrom, '' as PaidTo, Company.Code, FinDocument.GLCODE As BankCode, 1 as SortOrder " \
          " From    FinDocument" \
          " Join    FinBusinessUnit         On      FinDocument.BUSINESSUNITCODE = FinBusinessUnit.CODE" \
          " Join    FinBusinessUnit As Company On FinBusinessUnit.GroupbuCode = Company.Code" \
          " JoiN    GLMaster As BankMaster  On      FinDocument.GLCODE = BankMaster.Code" \
           " Join    FINBalanceSheetLineTemplateGL As OnLineBBal ON FinDocument.GLCode = OnLineBBal.GLCode " \
           "           And OnLineBBal.FinBalanceSheetTemplateCode = 'ONLINEBBAL'" \
           " Where   FinDocument.FinanceDocumentDate <= "+EndDate+"" \
          " And     FinDocument.DocumentTypeCode In ('BP','BR','CP','CR')" \
          " Group By company.LongDescription, BankMaster.LongDescription, Company.Code, FinDocument.GLCODE" \
          " order by company.LongDescription, BankMaster.LongDescription"


    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    # Explicitly bind parameters


    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
        result = con.db.fetch_both(stmt)

        # pdfrpt.c.line(0, 12, 600, 12)
        if pdfrpt.d < 20:
            pdfrpt.d = 770
            pdfrpt.c.showPage()
            pdfrpt.header(stdt, etdt, pdfrpt.divisioncode)
            # pdfrpt.d=pdfrpt.d-20
            # pdfrpt.itemcodes(result, pdfrpt.d)

    if result == False:
        if counter > 0:
            pdfrpt.c.line(0, pdfrpt.d, 600, pdfrpt.d)
            pdfrpt.fonts(7)
            # pdfrpt.printstoretotal(stdt, etdt, pdfrpt.divisioncode)
            # pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
            pdfrpt.printtotal(stdt,etdt,pdfrpt.divisioncode,pdfrpt.d)
            pdfrpt.printgrandtotal(stdt, etdt, pdfrpt.divisioncode, pdfrpt.d)
            # pdfrpt.storeclean()
            # pdfrpt.companyclean()
            # pdfrpt.cleanstore()
            SBBV.Exceptions = ""
        elif counter == 0:
            SBBV.Exceptions = "Note: No Result found according to your selected criteria "
            return

    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    counter = 0
    pdfrpt.d = pdfrpt.newpage()