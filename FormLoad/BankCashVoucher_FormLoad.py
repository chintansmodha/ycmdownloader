
from Global_Files import Connection_String as con
from django.shortcuts import render
GDataBank=[]
GDataCompany=[]
GDataVChNo=[]
GDataBankCashVoucher=[]

def BankCashVoucherHtml(request):
    global GDataBank
    global GDataCompany
    global GDataVChNo
    GDataVChNo=[]
    GDataCompany=[]
    GDataBank=[]
    stmt = con.db.exec_immediate(con.conn,
                                 "select code,longdescription from GLMASTER order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        if result not in GDataBank:
            GDataBank.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,
                                 "select code,longdescription from FINBUSINESSUNIT order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        if result not in GDataCompany:
            GDataCompany.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn,
                                 "select code from FINDOCUMENT order by CODE")
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        if result not in GDataVChNo:
            GDataVChNo.append(result)
        result = con.db.fetch_both(stmt)
    return render(request, 'BankCashVoucherPDF.html',{'GDataCompany':GDataCompany,'GDataBank':GDataBank,'GDataVChNo':GDataVChNo})


def BankCashVoucherSummary(request):
    global GDataBank
    global GDataCompany
    global GDataVChNo
    comp=request.GET['comp']
    if comp:
        comp = " And FINBUSINESSUNIT.code = '"+comp+"'"
    
    bank=request.GET['bank']
    if bank:
        bank = " And GLMASTER.code = '"+bank+"'"
    startvch=request.GET['vchno']
    endvch=request.GET['refno']
    startdate=request.GET['refdate']
    enddate=request.GET['vchdate']

    if startvch:
        cond = "FD.code between '"+endvch+"' and '"+startvch+"'"
    else:
        cond = "FD.postingdate between '"+startdate+"' and '"+enddate+"'"
 
    global GDataBank
    global GDataCompany
    global GDataVChNo
    global GDataBankCashVoucher
    GDataBankCashVoucher=[]
    sql = ("select FD.code as vchNo"
        " ,VARCHAR_FORMAT(FD.POSTINGDATE, 'DD-MM-YYYY') as vchdate "
        " ,cast(FD.DOCUMENTAMOUNT  as decimal(18,2)) as amount "
        " , COALESCE(FD.CHEQUENUMBER,'') as chqno "
        " , COALESCE(businesspartner.legalname1,'') as party "
        " ,businesspartner.numberid as partycode "
" from findocument as FD "
" join FINBUSINESSUNIT            on      FD.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE   "
" join GLMASTER                   on      FD.glCODE = GLMASTER.CODE   "
" Left join orderpartner          on      FD.SUPPLIERTYPE =orderpartner.CUSTOMERSUPPLIERTYPE   "
                                " AND     FD.SUPPLIERCODE = orderpartner.CUSTOMERSUPPLIERCODE   "
" Left join businesspartner       on      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID  "
"Where "+cond+comp+bank
)

    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    if result == False:
        return
    while result != False:
        GDataBankCashVoucher.append(result)
        result = con.db.fetch_both(stmt)
    return render(request, 'BankCashVoucherPDF.html',{'GDataCompany':GDataCompany,'GDataBank':GDataBank,'GDataVChNo':GDataVChNo,'GDataBankCashVoucher':GDataBankCashVoucher})