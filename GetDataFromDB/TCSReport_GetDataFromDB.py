from datetime import datetime
from Global_Files import Connection_String as con
from PrintPDF import TCSReport_XLS as xlsrpt

def TCSReport_GetData(LSCompany,LCCompany,LSAccount,LCAccount,LDStartDate,LDEndDate):
    xlsrpt.filename()
    LSName = datetime.now()
    LSstring = str(LSName)
    global LSFileName
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = " Sale Inv " + LSFileName + ".xlsx"


    if not LCCompany and not LSCompany or LCCompany:
        LSCompany = " "
    elif LSCompany:
        LSCompany = " AND UNIT.CODE in (" + str(LSCompany)[1:-1] + ")"

    if not LCAccount and not LSAccount or LCAccount:
        LSAccount = " "
    elif LSAccount:
        LSAccount = " AND GLMASTER.CODE in (" + str(LSAccount)[1:-1] + ")"

    stdt = datetime.strptime(LDStartDate, "%Y-%m-%d").date()
    etdt = datetime.strptime(LDEndDate, "%Y-%m-%d").date()

    sql = (
    
    " Select  FD.Code as vchno "
        " ,FD.FINANCEDOCUMENTDATE as Dateofpayment  "
         " ,ORDERPARTNERIE.PANNO as PANNO "
         " ,businesspartner.legalname1 as party "
         " ,cast(PI.GROSSVALUE-FINDOCUMENTLINE.AMOUNTINDC as decimal(18,3)) as GrossAmount "
         " ,cast(FINDOCUMENTLINE.AMOUNTINDC as decimal(18,3)) as TDSAMOUNT "
         " ,PI.INVOICEDATE as invoicedate "
         " ,PI.COde as Invoiceno "
" from Findocument as FD "
" JOIN FINBUSINESSUNIT UNIT       ON      FD.BUSINESSUNITCODE=UNIT.CODE "
 " join FINDOCUMENTLINE         On      FD.COMPANYCODE       =  FINDOCUMENTLINE.FINDOCUMENTCOMPANYCODE   "
           " And     FD.BUSINESSUNITCODE  =  FINDOCUMENTLINE.FINDOCUMENTBUSINESSUNITCODE   "
           " AND     FD.FINANCIALYEARCODE =  FINDOCUMENTLINE.FINDOCUMENTFINANCIALYEARCODE   "
           " AND     FD.DOCUMENTTEMPLATECODE = FINDOCUMENTLINE.FINDOCDOCUMENTTEMPLATECODE   "
           " And     FD.CODE = FINDOCUMENTLINE.FINDOCUMENTCODE  "
" Join PlantInvoice PI            on FD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE  "
                                 " And  FD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE "
                                 " And FD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE  "
                                 " And FD.CODE = PI.FINDOCCODE  "
" JOIN ORDERPARTNERIE        On      FD.CUSTOMERTYPE    =ORDERPARTNERIE.CUSTOMERSUPPLIERTYPE  "
                                " AND     FD.CUSTOMERCODE=ORDERPARTNERIE.CUSTOMERSUPPLIERCODE "
" Left Join GLmaster On FD.GLCODE=GLMASTER.code "
" Left join orderpartner          on      FD.CUSTOMERTYPE =orderpartner.CUSTOMERSUPPLIERTYPE   "
                                " AND     FD.CUSTOMERCODE = orderpartner.CUSTOMERSUPPLIERCODE   "
" Left join businesspartner       on      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID  "
" Where FD.DOCUMENTTYPECODE='SD' and FD.POSTINGDATE Between '"+LDStartDate+"' and '"+LDEndDate+"'"+LSCompany+LSAccount
    )
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    if result == False:
        return
    while result != False:
        xlsrpt.textsize( result, stdt, etdt)
        result = con.db.fetch_both(stmt)
    xlsrpt.workbook.close()
    # xlsrpt.newrequest()