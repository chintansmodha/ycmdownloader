from datetime import datetime
from PrintPDF import BankRecon_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
from ProcessSelection import BankRecon_ProcessSelection as BRPS
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

    sql =  ("select  distinct  "
        " FD.code as vchNo "
        " ,FINBUSINESSUNIT.Longdescription as divcode "
        " ,VARCHAR_FORMAT(FD.POSTINGDATE,'DD-MM-YYYY') as vchdate "
        " ,cast(FD.DOCUMENTAMOUNT as decimal(18,2))as amount "
        " ,COALESCE(FD.CHEQUENUMBER,'') as chqno "
        " ,COALESCE(FD.CHEQUEDATE,'1999-01-01') as chqdate "
        " ,COALESCE(businesspartner.legalname1,'') as party "
       " ,bank.LONGDESCRIPTION as bankname "
  " from findocument as FD "
 " join FINBUSINESSUNIT            on      FD.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE "
" left Join FinOpenDocumentsTransactions as FODT  On FD.BUSINESSUNITCODE  =  FODT.DESTBUSINESSUNITCODE  "
 "          AND     FD.FINANCIALYEARCODE =  FODT.DESTFINANCIALYEARCODE  "
  "         AND     FD.DOCUMENTTEMPLATECODE = FODT.DESTDOCUMENTTEMPLATECODE  "
   "        And     FD.CODE = FODT.DESTCODE "
 " join Glmaster as bank           on     FD.glCODE = bank.CODE "
" Left Join Note As NoteHdr     On      FD.AbsUniqueID = NoteHdr.FatherId "
" Left join orderpartner          on      FD.CUSTOMERTYPE =orderpartner.CUSTOMERSUPPLIERTYPE   "
 "                                AND     FD.CUSTOMERCODE = orderpartner.CUSTOMERSUPPLIERCODE   "
" Left join businesspartner       on      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID "
 " Where FODT.TRANSACTIONDATE between '" + str(LDStartDate) + "' and '" + str(LDEndDate) + "' " +LSCompany+LSBank+ "  "
 )

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
        pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode,result)
        result = con.db.fetch_both(stmt)

    if pdfrpt.d < 20:
        pdfrpt.d = 740
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
