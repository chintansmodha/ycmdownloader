from datetime import datetime
from PrintPDF import BankCashStatement_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
from ProcessSelection import BankCashStatement_ProcessSelection as BCSV
counter=0
def BankReconGetDataFromDB(LSCompany,LSBank,LSAllCompany,LSAllBank,LDEndDate,LDStartDate):
    if not LSAllCompany and not LSCompany or LSAllCompany:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And Plant.CODE in ("+str(LSCompany)[1:-1]+")"
    if not LSAllBank and not LSBank or LSAllBank:
        LSBank = ""
    elif LSBank:
        LSBank = "AND FINDOCUMENT.GLCODE in ("+str(LSBank)[1:-1]+")"  

    sql =  ("Select * from PlantInvoice")

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
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
        result = con.db.fetch_both(stmt)

    if pdfrpt.d < 20:
        pdfrpt.d = 730
        pdfrpt.c.showPage()
        pdfrpt.header(stdt, etdt, pdfrpt.divisioncode)

    if result == False:
        global Exceptions
    if counter>0:
        pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
        pdfrpt.fonts(7)
        pdfrpt.companyclean()
        Exceptions = ""
    elif counter == 0:
        Exceptions = "Note: Please Select Valid Credentials"
        return
    pdfrpt.newrequest()
    pdfrpt.c.setPageSize(pdfrpt.A4)
    pdfrpt.c.showPage()
    pdfrpt.c.save()
