from datetime import datetime

from django.shortcuts import render
from babel.numbers import format_currency
from FormLoad import AdhocLedger_FormLoad as views
from Global_Files import Connection_String as con
GDataAdhocLedgerDetail=[]
GDataAdhocLedgerDetailData=[]
close=0
company=''
bank=''
subaccount=''

def AdhocLedgerDetail(request):
    global GDataAdhocLedgerDetail
    global GDataAdhocLedgerDetailData
    global close
    global Credit
    global Debit
    global company
    global bank
    global subaccount

    GDataAdhocLedgerDetail=[]
    GDataAdhocLedgerDetailData=[]
    Debit=0
    Credit=0
    LSCompanyUnitCode = request.GET['Businessunitcode']
    LSAccountCode = request.GET['Accountcode']
    LSSubAccountCode = request.GET['Subaccountcode']
    LSYearCode = request.GET['Subaccount']
    LSDocCode = request.GET['Yearcode']
    companycode = ''
    accountcode = ''
    subaccountcode = ''
    yearcode = ''
    doccode = ''
    if request.GET['Businessunitcode']:
        companycode = " And findocumentline.FINDOCUMENTBUSINESSUNITCODE='" + str(request.GET['Businessunitcode']) + "'"

    if request.GET['Accountcode']:
        accountcode = " And findocumentline.GLCODE='" + str(request.GET['Accountcode']) + "'"

    if int(request.GET['Subaccountcode']) != 0:
        subaccountcode = " And businesspartner.NUMBERID='" + str(request.GET['Subaccountcode']) + "'"

    if request.GET['Yearcode']:
        yearcode = " And findocumentline.FINDOCUMENTFINANCIALYEARCODE='" + str(request.GET['Yearcode']) + "'"

    # if request.GET['Doccode']:
    #     doccode = " And findocumentline.FINDOCDOCUMENTTEMPLATECODE='" + str(request.GET['Doccode']) + "'"
    LSOpeningBalance = request.GET['Opbal']
    close = LSOpeningBalance.replace('₹', '')
    close = close.replace(',', '')
    close = float(close)

    startdate = datetime.strptime(request.GET['startdate'], "%d %B %Y")
    enddate = datetime.strptime(request.GET['enddate'], "%d %B %Y")
    stdt = startdate
    etdt = enddate
    startdate = str(startdate.strftime("%Y-%m-%d"))
    enddate = str(enddate.strftime("%Y-%m-%d"))
    sql = "Select  finbusinessunit.LongDescription As BusinessUnit, " \
          "GLMaster.LongDescription As GLAccount" \
          ",findocumentline.FINDOCUMENTFINANCIALYEARCODE AS YEARcode" \
          ",findocumentline.FINDOCDOCUMENTTEMPLATECODE as DocCode," \
          "         COALESCE(BUSINESSPARTNER.LegalName1,'') As SubAccount, findocument.code as number," \
          "          VARCHAR_FORMAT(findocument.FINANCEDOCUMENTDATE, 'DD-MM-YYYY') as date" \
          ", findocument.DOCUMENTTYPECODE as docno," \
          "           COALESCE(findocument.CHEQUENUMBER,'') as  chqno, " \
          "(cast(Case When FinDocument.FINANCEDOCUMENTDATE <'"+startdate+"'" \
         " Then findocumentline.AMOUNTINCC Else 0 End as decimal(18,2))) As OpBal," \
         "(cast(Case When findocumentline.AMOUNTINCC > 0 And FinDocument.FINANCEDOCUMENTDATE" \
         " Between '"+startdate+"' And '"+enddate+"' Then findocumentline.AMOUNTINCC Else 0 End as decimal(18,2))) As DrAmount," \
         "Abs((cast(Case When findocumentline.AMOUNTINCC < 0 And FinDocument.FINANCEDOCUMENTDATE Between '"+startdate+"' And '"+enddate+"'" \
         " Then findocumentline.AMOUNTINCC Else 0 End as decimal(18,2)))) As CrAmount," \
          "           cast(findocumentline.AMOUNTINCC as decimal(18,2)) As ClBal" \
          " , PI.CODE as INVNO" \
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
          " Where   FinDocument.FINANCEDOCUMENTDATE between '" + startdate + "' And '" + enddate + "' " + companycode + accountcode + subaccountcode+yearcode+" " \
          " order by  findocument.FINANCEDOCUMENTDATE"
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    GDataAdhocLedgerDetail.append(result)

    company=str(result['BUSINESSUNIT'])
    bank=result['GLACCOUNT']
    subaccount=result['SUBACCOUNT']

    while result != False:
        result['CR'] = str(format_currency(result['CRAMOUNT'], 'INR', locale='en_IN')).replace('₹', '')
        result['DR'] = str(format_currency(result['DRAMOUNT'], 'INR', locale='en_IN')).replace('₹', '')
        Debit = Debit + (float("%.2f" % float(result['DRAMOUNT'])))
        Credit = Credit + (float("%.2f" % float(result['CRAMOUNT'])))
        close = close - float(result['CRAMOUNT'])+float(result['DRAMOUNT'])
        result['CL'] = str(format_currency(close, 'INR', locale='en_IN')).replace('₹', '')
        GDataAdhocLedgerDetailData.append(result)
        result = con.db.fetch_both(stmt)
    return render(request, 'AdhocLedgerDetail.html',{'GDataAdhocLedgerDetail':GDataAdhocLedgerDetail,'LSOpeningBalance':LSOpeningBalance,
                                                     'GDataAdhocLedgerDetailData':GDataAdhocLedgerDetailData,'Debit':str(format_currency((float("%.2f" % float(Debit))), 'INR', locale='en_IN')).replace('₹', ''),
                                                      'Credit':str(format_currency((float("%.2f" % float(Credit))), 'INR', locale='en_IN')).replace('₹', ''),
                                                     'startdate':stdt.strftime("%d %B %Y"),
                                                     'enddate':etdt.strftime("%d %B %Y"),
                                                     'comp':company,'bank':bank,'subaccount':subaccount,"companycode": request.GET['Businessunitcode']
        ,"accountcode": request.GET['Accountcode'],"subaccountcode": request.GET['Subaccountcode']})
