from datetime import datetime
from Global_Files import Connection_String as con
from django.shortcuts import render
from babel.numbers import format_currency
LDStartDate=''
LDEndDate=''
GDataOnlineBankBalance=[]
counter=0
ClosingBalance=0

OpeningBalance=0
Payment=0
Receipt=0
ClosingBalanced=0
def OnlineBankBalanceHtml(request):
    return render(request,'OnlineBankBalance.html')

def OnlineBankBalanceSummary(request):
    global GDataOnlineBankBalance
    global LDStartDate
    global LDEndDate
    global ClosingBalance

    global OpeningBalance
    global Payment
    global Receipt
    global ClosingBalanced
    OpeningBalance = 0
    ClosingBalanced = 0
    Payment = 0
    Receipt = 0

    ClosingBalance=0
    LDStartDate = "'" + str(request.GET['startdate']) + "'"
    LDEndDate = "'" + str(request.GET['enddate']) + "'"
    stdt = datetime.strptime(request.GET['startdate'], '%Y-%m-%d').date()
    etdt = datetime.strptime(request.GET['enddate'], '%Y-%m-%d').date()
    GDataOnlineBankBalance=[]

    sql = " Select  Company.LongDescription As BUSINESSUNITName, BankMaster.LongDescription As BankName," \
          " cast(Sum(Case When FinDocument.FinanceDocumentDate < " + LDStartDate + " " \
          " Then FinDocument.DocumentAmount * Case When DocumentTypeCode In ('BR','CR') Then 1 Else -1 End Else 0 End)as decimal(18,2)) As OpBal," \
          " cast(Sum(Case When FinDocument.FinanceDocumentDate >= " + LDStartDate + "" \
          " And FinDocument.DocumentTypeCode In ('BR','CR') Then FinDocument.DocumentAmount Else 0 End)as decimal(18,2)) as Receipts" \
          " , cast(Sum(Case When FinDocument.FinanceDocumentDate >= " + LDStartDate + "" \
          " And FinDocument.DocumentTypeCode In ('BP','CP') Then FinDocument.DocumentAmount Else 0 End)as decimal(18,2)) as Payments" \
          " , '' as RecievedFrom, '' as PaidTo, Company.Code, FinDocument.GLCODE As BankCode, 1 as SortOrder " \
          " From    FinDocument" \
          " Join    FinBusinessUnit         On      FinDocument.BUSINESSUNITCODE = FinBusinessUnit.CODE" \
          " Join    FinBusinessUnit As Company On FinBusinessUnit.GroupbuCode = Company.Code" \
          " JoiN    GLMaster As BankMaster  On      FinDocument.GLCODE = BankMaster.Code" \
          " Join FINBalanceSheetLineTemplateGL As OnLineBBal  ON FinDocument.GLCode = OnLineBBal.GLCode " \
          " And OnLineBBal.FinBalanceSheetTemplateCode = 'ONLINEBBAL' " \
          " And  OnLineBBal.FinBlnSheetLineTemplateCode = 'ONLINEBBAL'" \
          " Where   FinDocument.FinanceDocumentDate <= " + LDEndDate + "" \
          " And     FinDocument.DocumentTypeCode In ('BP','BR','CP','CR')" \
          " Group By company.LongDescription, BankMaster.LongDescription, Company.Code, FinDocument.GLCODE" \
          " order by company.LongDescription, BankMaster.LongDescription"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        global counter
        counter = counter + 1
        ClosingBalance = 0
        ClosingBalance = ClosingBalance + float(result['OPBAL']) + float(result['RECEIPTS']) - float(result['PAYMENTS'])
        result['CLBAL'] = ClosingBalance

        OpeningBalance = OpeningBalance + (float("%.2f" % float(result['OPBAL'])))
        Receipt = Receipt + (float("%.2f" % float(result['RECEIPTS'])))
        Payment = Payment + (float("%.2f" % float(result['PAYMENTS'])))
        ClosingBalanced = ClosingBalanced + (float("%.2f" % float(result['CLBAL'])))

        result['BUSINESSUNITNAME']=str(result['BUSINESSUNITNAME'])[:str(result['BUSINESSUNITNAME']).index(" ")]
        GDataOnlineBankBalance.append(result)
        result = con.db.fetch_both(stmt)

    return render(request, 'OnlineBankBalanceSummary.html',{"GDataOnlineBankBalance":GDataOnlineBankBalance,'startdate':stdt.strftime("%d %B %Y"),'enddate':etdt.strftime("%d %B %Y")
                ,'OpeningBalance':str(format_currency((float("%.2f" % float(OpeningBalance))), 'INR', locale='en_IN')).replace('₹', ''),
                                                      'Receipt':str(format_currency((float("%.2f" % float(Receipt))), 'INR', locale='en_IN')).replace('₹', ''),
                                                      'Payment':str(format_currency((float("%.2f" % float(Payment))), 'INR', locale='en_IN')).replace('₹', ''),
                                                      'ClosingBalanced':str(format_currency((float("%.2f" % float(ClosingBalanced))), 'INR', locale='en_IN')).replace('₹', ''),
                                                        })
