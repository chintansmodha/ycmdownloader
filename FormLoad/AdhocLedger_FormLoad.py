from datetime import datetime
import locale
from traceback import print_tb
locale.setlocale(locale.LC_MONETARY, 'en_IN')
from babel.numbers import format_currency
from django.shortcuts import render
from Global_Files import Connection_String as con
GDataCompany=[]
GDataAccount=[]
GDataSubAccount=[]
LDStartDate=''
LDEndDate=''
GDAdhocSummary=[]
stdt=''
etdt=''
Exception=''
OpeningBalance=0
Debit=0
Credit=0
ClosingBalance=0
GDataYear=[]
# Create your views here.
def AdhocLedger(request):
    global GDataYear
    global GDAdhocSummary
    global GDataAccount
    global GDataCompany
    global GDataSubAccount

    stmt = con.db.exec_immediate(con.conn, "Select Code,varchar_format(FROMDATE,'YYYY-MM-DD') as FROMDATE"
                                           ",varchar_format(TODATE,'YYYY-MM-DD') as TODATE from FinFinancialYear order by Code desc")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataYear:
            GDataYear.append(result)
        result = con.db.fetch_both(stmt)
    print(GDataYear)

    stmt = con.db.exec_immediate(con.conn,
                                 "select code,longdescription from finbusinessunit where groupflag=0 order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        if result not in GDataCompany:
            GDataCompany.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn, "select code,longdescription from glmaster order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataAccount:
            GDataAccount.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn, "select numberid,legalname1 from businesspartner order by legalname1")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataSubAccount:
            GDataSubAccount.append(result)
        result = con.db.fetch_both(stmt)

    return render(request,'AdhocLedger.html',{'GDataCompany':GDataCompany,'GDataAccount':GDataAccount,'GDataSubAccount':GDataSubAccount,"GDataYear":GDataYear})

def AdhocLedgerSummary(request):
    global OpeningBalance
    global Credit
    global Debit
    global ClosingBalance
    global Exception
    OpeningBalance=0
    ClosingBalance=0
    Credit=0
    Debit=0
    Exception=''


    global GDAdhocSummary
    global LDStartDate
    global LDEndDate
    global stdt
    global etdt
    GDAdhocSummary=[]
    startdate = request.GET['startdate']
    enddate = request.GET['enddate']
    startdate = datetime(int(startdate[0:4]), int(startdate[6:7]), int(startdate[8:]))
    enddate = datetime(int(enddate[0:4]), int(enddate[6:7]), int(enddate[8:]))
    Year = request.GET['year']
    FinDate=''
    if Year == "2022":
        print("it")
        if startdate < datetime(2021, 4, 1):
            Exceptions = "Start Date Should Be Between 2021-03-31 and 2022-04-01"
            return render(request, 'AdhocLedger.html', {"Exception": Exceptions})
        elif enddate > datetime(2022, 3, 31):
            Exceptions = "End Date Should Be Between 2021-03-31 and 2022-04-01"
            return render(request, 'AdhocLedger.html', {"Exception": Exceptions})
    elif Year == "2021":
        if startdate < datetime(2021, 4, 1):
            Exceptions = "Start Date Should Be Between 2020-04-01 and 2021-03-31"
            return render(request, 'AdhocLedger.html', {"Exception": Exceptions})
        elif enddate > datetime(2022, 3, 31):
            Exceptions = "End Date Should Be Between 2020-04-01 and 2021-03-31"
            return render(request, 'AdhocLedger.html', {"Exception": Exceptions})
    elif Year == "2019":
        if startdate < datetime(2021, 4, 1):
            Exceptions = "Start Date Should Be Between 2019-04-01 and 2020-03-31"
            return render(request, 'AdhocLedger.html', {"Exception": Exceptions})
        elif enddate > datetime(2022, 3, 31):
            Exceptions = "End Date Should Be Between 2019-04-01 and 2020-03-31"
            return render(request, 'AdhocLedger.html', {"Exception": Exceptions})
    elif Year == "1920":
        if startdate < datetime(2021, 4, 1):
            Exceptions = "Start Date Should Be Between 2019-04-01 and 2020-03-31"
            return render(request, 'AdhocLedger.html', {"Exception": Exceptions})
        elif enddate > datetime(2022, 3, 31):
            Exceptions = "End Date Should Be Between 2019-04-01 and 2020-03-31"
            return render(request, 'AdhocLedger.html', {"Exception": Exceptions})

    if not request.GET.getlist('unit') and not request.GET.getlist('allcomp') :
        LSCompanyUnitCode=""
    elif  request.GET.getlist('allcomp'):
        LSCompanyUnitCode=""
    elif request.GET.getlist('unit'):
        LSCompanyUnitCode = "AND finbusinessunit.code in (" +str(request.GET.getlist('unit'))[1:-1]+")"

    if not request.GET.getlist('account') and not request.GET.getlist('allaccount') :
        LSAccountCode=""
    elif  request.GET.getlist('allaccount'):
        LSAccountCode=""
    elif request.GET.getlist('account'):
        LSAccountCode = "AND findocumentline.GLCODE in (" +str(request.GET.getlist('account'))[1:-1]+")"

    if not request.GET.getlist('subaccount') and not request.GET.getlist('allsubaccount') :
        LSSubAccountCode=""
    elif  request.GET.getlist('allsubaccount'):
        LSSubAccountCode=""
    elif request.GET.getlist('subaccount'):
        LSSubAccountCode = "AND BUSINESSPARTNER.NUMBERID in (" +str(request.GET.getlist('subaccount'))[1:-1]+")"

    stdt = startdate
    etdt = enddate
    startdate = str(startdate.strftime('%Y-%m-%d'))
    enddate = str(enddate.strftime('%Y-%m-%d'))

    sql ="Select  finbusinessunit.Shortdescription As BusinessUnit," \
         "          findocumentline.FINDOCUMENTBUSINESSUNITCODE as businesscode" \
         "          ,findocumentline.GLCODE as glcode" \
         "          ,COALESCE(BUSINESSPARTNER.NUMBERID,0)  as SubAccountcode" \
         "          ,findocumentline.FINDOCUMENTFINANCIALYEARCODE AS YEARcode" \
         "          ,GLMaster.LongDescription As GLAccount" \
         "          ,findocumentline.SLCUSTOMERSUPPLIERTYPE as suppliertype," \
         "            findocumentline.SLCUSTOMERSUPPLIERCODE as suppliercode," \
         "          COALESCE(BUSINESSPARTNER.LegalName1,'') As SubAccount," \
         "Sum(cast(Case When FinDocument.FINANCEDOCUMENTDATE <'"+startdate+"'" \
         " Then findocumentline.AMOUNTINCC Else 0 End as decimal(18,2))) As OpBal," \
         "Sum(cast(Case When findocumentline.AMOUNTINCC > 0 And FinDocument.FINANCEDOCUMENTDATE" \
         " Between '"+startdate+"' And '"+enddate+"' Then findocumentline.AMOUNTINCC Else 0 End as decimal(18,2))) As DrAmount," \
         "Abs(Sum(cast(Case When findocumentline.AMOUNTINCC < 0 And FinDocument.FINANCEDOCUMENTDATE Between '"+startdate+"' And '"+enddate+"'" \
         " Then findocumentline.AMOUNTINCC Else 0 End as decimal(18,2)))) As CrAmount," \
         "Sum(cast(findocumentline.AMOUNTINCC as decimal(18,2))) As ClBal" \
         " from findocumentline" \
         " join findocument on findocumentline.FINDOCUMENTCOMPANYCODE = findocument.COMPANYCODE" \
         " AND findocumentline.FINDOCUMENTBUSINESSUNITCODE = findocument.BUSINESSUNITCODE" \
         " AND findocumentline.FINDOCUMENTFINANCIALYEARCODE = findocument.FINANCIALYEARCODE" \
         " AND findocumentline.FINDOCDOCUMENTTEMPLATECODE = findocument.DOCUMENTTEMPLATECODE" \
         " AND findocumentline.FINDOCUMENTCODE = findocument.CODE" \
         " join finbusinessunit on findocument.BUSINESSUNITCODE = finbusinessunit.code" \
         " Join FINFinancialYear FInYear On FinYear.Code = FinDocument.FINANCIALYEARCODE" \
         " join glmaster on findocumentline.glcode = glmaster.code" \
         " Left join orderpartner on  findocumentline.SLCUSTOMERSUPPLIERTYPE =orderpartner.CUSTOMERSUPPLIERTYPE" \
         " AND findocumentline.SLCUSTOMERSUPPLIERCODE = orderpartner.CUSTOMERSUPPLIERCODE" \
         " Left join businesspartner on ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID" \
         " Where   FinDocument.FINANCEDOCUMENTDATE Between '"+startdate+"' And '"+enddate+"' " \
         " "+LSCompanyUnitCode+LSAccountCode+LSSubAccountCode+"" \
         " Group By finbusinessunit.Shortdescription, " \
        " GLMaster.LongDescription,COALESCE(BUSINESSPARTNER.LegalName1,''),BUSINESSPARTNER.NUMBERID," \
        " findocumentline.FINDOCUMENTBUSINESSUNITCODE,findocumentline.GLCODE,findocumentline.FINDOCUMENTFINANCIALYEARCODE        ,findocumentline.SLCUSTOMERSUPPLIERTYPE,findocumentline.SLCUSTOMERSUPPLIERCODE" \
         " order by  findocumentline.FINDOCUMENTBUSINESSUNITCODE,findocumentline.GLCODE,COALESCE(BUSINESSPARTNER.LegalName1,'')"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        GDAdhocSummary.append(result)
        OpeningBalance = OpeningBalance + (float("%.2f" % float(result['OPBAL'])))
        Debit = Debit + (float("%.2f" % float(result['DRAMOUNT'])))
        Credit = Credit + (float("%.2f" % float(result['CRAMOUNT'])))
        ClosingBalance = ClosingBalance + (float("%.2f" % float(result['CLBAL'])))
        result['OP'] = str(format_currency(result['OPBAL'], 'INR', locale='en_IN')).replace('₹', '')
        result['CR'] = str(format_currency(result['CRAMOUNT'], 'INR', locale='en_IN')).replace('₹', '')
        result['DR'] = str(format_currency(result['DRAMOUNT'], 'INR', locale='en_IN')).replace('₹', '')
        result['CL'] = str(format_currency(result['CLBAL'], 'INR', locale='en_IN')).replace('₹', '')
        result = con.db.fetch_both(stmt)

    return render(request, 'AdhocLedgerSummary.html',{'GDAdhocSummary': GDAdhocSummary,
                                                      'OpeningBalance':str(format_currency((float("%.2f" % float(OpeningBalance))), 'INR', locale='en_IN')).replace('₹', ''),
                                                      'Debit':str(format_currency((float("%.2f" % float(Debit))), 'INR', locale='en_IN')).replace('₹', ''),
                                                      'Credit':str(format_currency((float("%.2f" % float(Credit))), 'INR', locale='en_IN')).replace('₹', ''),
                                                      'ClosingBalance':str(format_currency((float("%.2f" % float(ClosingBalance))), 'INR', locale='en_IN')).replace('₹', ''),
                                                        'startdate':stdt.strftime("%d %B %Y"),'enddate':etdt.strftime("%d %B %Y")})