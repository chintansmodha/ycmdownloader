from datetime import datetime
from Global_Files import Connection_String as con
from Global_Files import AmmountINWords as amw
from PrintPDF import BankCashVoucher_PrintPDF as BCVPP


def BankCashVoucher_GetData(vchdate,vchno,partycode):
    date=[]
    for i in vchdate:
        temp = datetime.strptime(i, '%d-%m-%Y').date()
        date.append(temp.strftime("%Y-%m-%d"))
    vchdate = " And FD.POSTINGDATE in ("+str(date)[1:-1]+")"
    vchno = "FD.code in ("+str(vchno)[1:-1]+")"
    partycode = " And BP.numberid in ("+str(partycode)[1:-1]+")"
    print(vchdate,vchno,partycode)
    sql=(
        " select  distinct   "
         " FD.code as vchNo  "
         " ,FINBUSINESSUNIT.Longdescription as divcode  "
         " ,FD.DOCUMENTTYPECODE as doctype  "
         " ,businesspartner.Addressline1 as bankaddress  "
        " ,businesspartner.Addressline2 as bankaddress1 "
         " ,VARCHAR_FORMAT(FD.POSTINGDATE,'DD-MM-YYYY') as vchdate  "
        " ,FINDOCUMENTLINE.AMOUNTINDC AS AMOUNTINDC "
        " ,CAST(Case When FINDOCUMENTLINE.AMOUNTINDC < 0 then FINDOCUMENTLINE.AMOUNTINDC ELSE 0 End AS DECIMAL(18,2)) as CREDIT  "
        " ,CAST(Case When FINDOCUMENTLINE.AMOUNTINDC > 0 then FINDOCUMENTLINE.AMOUNTINDC ELSE 0 End  AS DECIMAL(18,2)) as DEBIT  "
         " ,cast(FD.DOCUMENTAMOUNT as decimal(18,2))as amount  "
         " , COALESCE(FD.CHEQUENUMBER,'') as chqno  "
         " , COALESCE(businesspartner.legalname1,'') as party  "
         " ,businesspartner.numberid as partycode   "
         " ,plant.ADDRESSLINE1 as companyaddress  "
         " ,'15-17, MAKER CHAMBERS - III, JAMNALAL BAJAJ ROAD, NARIMAN POINT, MUMBAI - 400 021.' as HOAddress  "
         " ,plant.code as companycode  "
        " ,GLMASTER.LONGDESCRIPTION as Bankline "
        " ,bank.LONGDESCRIPTION as bankname "
        " ,GLMASTER.GLTYPE as GLTYPE "
        " ,FDBill.INVOICENO as Billno "
        " ,,VARCHAR_FORMAT(FD.POSTINGDATE,'DD-MM-YYYY')FDBill.INVOICEDATE as billdate "
        " ,COALESCE(Varchar(NoteHdr.Note),'') As Remarks "
         " "
 " from findocument as FD  "
 " join FINDOCUMENTLINE         On      FD.COMPANYCODE       =  FINDOCUMENTLINE.FINDOCUMENTCOMPANYCODE   "
           " And     FD.BUSINESSUNITCODE  =  FINDOCUMENTLINE.FINDOCUMENTBUSINESSUNITCODE   "
           " AND     FD.FINANCIALYEARCODE =  FINDOCUMENTLINE.FINDOCUMENTFINANCIALYEARCODE   "
           " AND     FD.DOCUMENTTEMPLATECODE = FINDOCUMENTLINE.FINDOCDOCUMENTTEMPLATECODE   "
           " And     FD.CODE = FINDOCUMENTLINE.FINDOCUMENTCODE  "
           " And     FD.GLCODE<>FINDOCUMENTLINE.GLCODE  "
 " join FINBUSINESSUNIT            on      FD.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE  "
 " Join FinOpenDocumentsTransactions as FODT  On FD.BUSINESSUNITCODE  =  FODT.DESTBUSINESSUNITCODE   "
           " AND     FD.FINANCIALYEARCODE =  FODT.DESTFINANCIALYEARCODE   "
           " AND     FD.DOCUMENTTEMPLATECODE = FODT.DESTDOCUMENTTEMPLATECODE   "
           " And     FD.CODE = FODT.DESTCODE "
" Join FinDocument FDBill On FODT.ORIGINBUSINESSUNITCODE  =  FDBill.BUSINESSUNITCODE   "
           " AND     FODT.ORIGINFINANCIALYEARCODE =  FDBill.FINANCIALYEARCODE   "
           " AND     FODT.ORIGINDOCUMENTTEMPLATECODE = FDBill.DOCUMENTTEMPLATECODE   "
           " And     FODT.ORIGINCODE = FDBill.CODE  "
 " join businessunitvscompany as buc on    FINBUSINESSUNIT.CODE = buc.BUSINESSUNITCODE  "
                                 " And     buc.FACTORYCODE <> 'P02'  "
                                 " And     buc.FACTORYCODE <> 'P08'  "
 " join plant                      on      buc.FACTORYCODE=plant.code "
 " join Glmaster as bank           on     FD.glCODE = bank.CODE    "
 " join GLMASTER                   on      FINDOCUMENTLINE.glCODE = GLMASTER.CODE    "
 " Left Join Note As NoteHdr     On      FD.AbsUniqueID = NoteHdr.FatherId "
 " Left join orderpartner          on      FD.SUPPLIERTYPE =orderpartner.CUSTOMERSUPPLIERTYPE    "
                                 " AND     FD.SUPPLIERCODE = orderpartner.CUSTOMERSUPPLIERCODE    "
 " Left join businesspartner       on      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID "
"WHere "+vchno+vchdate+""
" order by divcode,vchno"
    )
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    
    while result != False:
        print(result)
        BCVPP.textsize(BCVPP.c, result, BCVPP.d)
        BCVPP.d = BCVPP.dvalue(BCVPP.divisioncode,result)
        result = con.db.fetch_both(stmt)
    
    BCVPP.d=BCVPP.d-20
    BCVPP.c.drawString(10,BCVPP.d,"Remark :")
    print(BCVPP.remark)
    BCVPP.c.drawString(50,BCVPP.d,BCVPP.remark[-1])
    BCVPP.d=BCVPP.d-10
    BCVPP.c.line(0, BCVPP.d, 600, BCVPP.d)
    # c.drawString(10,d-5,result['REMARK'])
    BCVPP.c.drawString(10,BCVPP.d-10,amw.inwords(BCVPP.amount[-1]))
    BCVPP.d=BCVPP.d-20
    BCVPP.c.line(0, BCVPP.d, 600, BCVPP.d)

    BCVPP.c.drawString(10,BCVPP.d-50,'Prepared By')
    BCVPP.c.drawString(200,BCVPP.d-50,'Checked By')
    BCVPP.c.drawString(400,BCVPP.d-50,'Authorised Signature')
    BCVPP.c.drawString(500,BCVPP.d-50,"Receiver's Signature")
    BCVPP.c.showPage()
    BCVPP.c.save()
    BCVPP.newrequest()
    BCVPP.d = BCVPP.newpage()