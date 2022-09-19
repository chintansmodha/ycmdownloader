from django.shortcuts import render
from datetime import datetime
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')
from babel.numbers import format_currency
from django.shortcuts import render
from Global_Files import Connection_String as con
GDataBrokerWiseOS=[]
GDataCompany=[]
GDataTotal=[]
GDataTotalCompany=[]
total=0
upto15=0
range16=0
over30=0
dnamt=0
advance=0
unbilled=0
unadj=0
olddays=0

TOTAL=0


def CompanyWiseOS(request):
    b=0
    t=0
    u=0
    r=0
    o=0
    d=0
    un=0

    global total
    global upto15
    global range16
    global over30
    global dnamt
    global advance
    global unbilled
    global unadj
    global olddays
    global TOTAL
    global i
    total = 0
    a = 0
    upto15 = 0
    range16 = 0
    over30 = 0
    dnamt = 0
    advance = 0
    unbilled = 0
    unadj = 0
    olddays = 0
    TOTAL=0

    global GDataBrokerWiseOS
    global GDataCompany
    global GDataTotal
    global GDataTotalCompany
    GDataTotalCompany = []
    GDataBrokerWiseOS=[]
    GDataCompany=[]
    GDataTotal=[]
    sql = " Select BrokerGrpOS.Company, BrokerGrpOS.BrokerGrp,BrokerGrpOS.CompanyCode,BrokerGrpOS.BrokerCode," \
          " Sum(BrokerGrpOS.Upto15) As Upto15,Sum(BrokerGrpOS.Range16) As Range16,Sum(BrokerGrpOS.Over30) As Over30" \
          " , Sum(BrokerGrpOS.DNAmt) As DNAmt,Sum(BrokerGrpOS.UnBilledAmt) As UnBilledAmt,Sum(BrokerGrpOS.AboveOdDays) As AboveOdDays" \
          " From (Select  Company.LongDescription As Company,AgGrp.LongDescription As BrokerGrp," \
          " Company.Code As CompanyCode,AgGrp.Code As BrokerCode" \
          " , cast(Sum(Case When days  (current date) - days (PI.InvoiceDate) <= 15 Then PI.NETTVALUE - 0 Else 0 End)as decimal(18,2)) AS Upto15" \
          " , cast(Sum(Case When days (current date) - days (PI.InvoiceDate) Between 16 and 30 Then PI.NETTVALUE - 0 Else 0 End)as decimal(18,2)) AS Range16" \
          " , cast(Sum(Case When days (current date) - days (PI.InvoiceDate) > 30 Then PI.NETTVALUE - 0 Else 0 End)as decimal(18,2)) AS Over30 " \
          " ,cast(0 as decimal(18,2)) as DNAmt ,cast(0 as decimal(18,2)) as UnBilledAmt," \
          " cast(Sum(Case When days (current date) - days (PI.InvoiceDate) > 0 Then PI.NETTVALUE - 0 Else 0 End)as decimal(18,2)) AS AboveOdDays  " \
          " From    PlantInvoice PI" \
          " join    BUSINESSUNITVSCOMPANY BC on PI.FACTORYCODE = BC.FACTORYCODE" \
          " Join    FinBusinessUnit BU on BC.BUSINESSUNITCODE = BU.Code" \
          " Join    FinBusinessUnit Company On BU.GroupbuCode = Company.Code" \
          " Join    AgentsGroupDetail AGD   On      PI.Agent1Code = AGD.AgentCode" \
          " Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code" \
          " Where   PI.FINDOCBUSINESSUNITCODE Is Null And PI.FINDOCFINANCIALYEARCODE Is Null And PI. FINDOCTEMPLATECODE Is Null And  PI.FINDOCCODE Is Null" \
          " group by AgGrp.LongDescription , Company.LongDescription,AgGrp.Code, Company.Code,days (current date) - days (PI.InvoiceDate) " \
          " Union All" \
          " Select Company.LongDescription As Company,AgGrp.LongDescription As BrokerGrp," \
          " Company.Code As CompanyCode,AgGrp.Code As BrokerCode" \
          " , cast(Sum(Case When days (current date) - days (FD.DUEDATE) <= 15 Then PI.NETTVALUE - 0 Else 0 End)as decimal(18,2)) AS Upto15" \
          " , cast(Sum(Case When days (current date) - days (FD.DUEDATE) Between 16 and 30 Then PI.NETTVALUE - 0 Else 0 End)as decimal(18,2)) AS Range16" \
          " , cast(Sum(Case When days (current date) - days (FD.DUEDATE) > 30 Then PI.NETTVALUE - 0 Else 0 End)as decimal(18,2)) AS Over30" \
          " ,cast(0 as decimal(18,2))as UnBilledAmt, cast(0 as decimal(18,2))as DNAmt ," \
          " cast(Sum(Case When days (current date) - days (FD.DUEDATE) > 0 Then PI.NETTVALUE - 0 Else 0 End)as decimal(18,2)) AS AboveOdDays    " \
          " From    PlantInvoice PI" \
          " Join FinDocument FD on PI.FINDOCBUSINESSUNITCODE = FD.BUSINESSUNITCODE" \
          " And PI.FINDOCFINANCIALYEARCODE = FD.FINANCIALYEARCODE" \
          " And PI.FINDOCTEMPLATECODE = FD.DOCUMENTTEMPLATECODE " \
          " And PI.FINDOCCODE = FD.CODE" \
          " join    BUSINESSUNITVSCOMPANY BC on PI.FACTORYCODE = BC.FACTORYCODE" \
          " Join    FinBusinessUnit BU on BC.BUSINESSUNITCODE = BU.Code" \
          " Join    FinBusinessUnit Company On BU.GroupbuCode = Company.Code" \
          " Join    AgentsGroupDetail AGD   On      PI.Agent1Code = AGD.AgentCode" \
          " Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code" \
          " Left Join    (Select ORIGINBUSINESSUNITCODE, ORIGINFINANCIALYEARCODE, ORIGINDOCUMENTTEMPLATECODE, ORIGINCODE," \
          " Sum(CLEAREDAMOUNT) As CLEAREDAMOUNT From FinOpenDocumentsTransactions" \
          " Group By ORIGINBUSINESSUNITCODE, ORIGINFINANCIALYEARCODE, ORIGINDOCUMENTTEMPLATECODE, ORIGINCODE)As Payments" \
          " On       PI.FINDOCBUSINESSUNITCODE = Payments.ORIGINBUSINESSUNITCODE " \
          " And   PI.FINDOCFINANCIALYEARCODE = Payments.ORIGINFINANCIALYEARCODE" \
          " And     PI.FINDOCTEMPLATECODE = Payments.ORIGINDOCUMENTTEMPLATECODE" \
          " And     PI.FINDOCCODE = Payments.ORIGINCODE " \
          " Where   PI.FINDOCBUSINESSUNITCODE Is Not Null And PI.FINDOCFINANCIALYEARCODE Is Not Null " \
          " And PI. FINDOCTEMPLATECODE Is Not Null And  PI.FINDOCCODE Is Not Null And  PI.NETTVALUE - COALESCE(Payments.CLEAREDAMOUNT,0) > 0" \
          " group by AgGrp.LongDescription , Company.LongDescription,AgGrp.Code ,Company.Code,days (current date) - days (FD.DUEDATE) " \
          " Union ALL" \
          " Select Company.LongDescription As Company,AgGrp.LongDescription As BrokerGrp," \
          " Company.Code As CompanyCode,AgGrp.Code As BrokerCode" \
          " ,cast(0 as decimal(18,2))as Upto15 , cast(0 as decimal(18,2))as Range16 ,cast(0 as decimal(18,2))as Over30" \
          " , Sum(FD.DOCUMENTAMOUNt - COALESCE(Payments.CLEAREDAMOUNT,0)) as DNAmt, cast(0 as decimal(18,2)) as UnBilledAmt, cast(0 as decimal(18,2))AS AboveOdDays" \
          " From    FinDocument FD" \
          " Join    FinBusinessUnit BU on FD.BUSINESSUNITCODE = BU.Code " \
          " Join    FinBusinessUnit Company On BU.GroupbuCode = Company.Code" \
          " Join    AgentsGroupDetail AGD   On      FD.Agent1Code = AGD.AgentCode" \
          " Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code" \
          " Left Join    (Select ORIGINBUSINESSUNITCODE, ORIGINFINANCIALYEARCODE, ORIGINDOCUMENTTEMPLATECODE, ORIGINCODE," \
          " Sum(CLEAREDAMOUNT) As CLEAREDAMOUNT From FinOpenDocumentsTransactions" \
          " Group By ORIGINBUSINESSUNITCODE, ORIGINFINANCIALYEARCODE, ORIGINDOCUMENTTEMPLATECODE, ORIGINCODE)" \
          " As Payments     On       FD.BUSINESSUNITCODE = Payments.ORIGINBUSINESSUNITCODE " \
          " And   FD.FINANCIALYEARCODE = Payments.ORIGINFINANCIALYEARCODE" \
          " And     FD.DOCUMENTTEMPLATECODE = Payments.ORIGINDOCUMENTTEMPLATECODE" \
          " And     FD.CODE = Payments.ORIGINCODE " \
          " Where   FD.DOCUMENTAMOUNT - COALESCE(Payments.CLEAREDAMOUNT,0) > 0 " \
          " group by AgGrp.LongDescription , Company.LongDescription,AgGrp.Code, Company.Code" \
          " Union All" \
          " Select  Company.LongDescription As Company,AgGrp.LongDescription As BrokerGrp," \
          " Company.Code As CompanyCode,AgGrp.Code As BrokerCode" \
          " ,0 as Upto15, 0 as Range16,0 as Over30, 0 as DNAmt,Sum(SD.ONDOCUMENTTOTALAMOUNT -0)  aS UnBilledAmt " \
          " , 0 AS AboveOdDays From    SalesDocument SD" \
          " JOIN BusinessUnitVsCompany BUC  ON      SD.DivisionCode   = BUC.DivisionCode" \
          " JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode = BUnit.Code And BUnit.GroupFlag = 0" \
          " JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code And Company.GroupFlag = 1" \
          " Join    AgentsGroupDetail AGD   On      SD.AGENT1CODE = AGD.AgentCode" \
          " Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code" \
          " Where   SD.DOCUMENTTYPETYPE In ('05') " \
          " And SD.INVOICEEVOLUTIONTYPE = '1' " \
          " group by Company.LongDescription,AgGrp.LongDescription,Company.Code,AgGrp.Code,SD.ONDOCUMENTTOTALAMOUNT" \
          " ) As BrokerGrpOS " \
          " Group By BrokerGrpOS.Company, BrokerGrpOS.BrokerGrp,BrokerGrpOS.CompanyCode,BrokerGrpOS.BrokerCode" \
          " order by Company"


    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        new = float("%.2f" % float(result['UPTO15'])) + float("%.2f" % float(result['RANGE16']))\
              +float("%.2f" % float(result['OVER30'])) + float("%.2f" % float(result['DNAMT'])) \
              + float("%.2f" % float(result['UNBILLEDAMT']))
        result['TOTAL'] = (float("%.2f" % float(new)))
        result['TOTAL'] = round(float(new) / 100000, 2)
        result['UPTO15'] = round(float(result['UPTO15']) / 100000, 2)
        result['RANGE16'] = round(float(result['RANGE16']) / 100000, 2)
        result['OVER30'] = round(float(result['OVER30']) / 100000, 2)
        result['DNAMT'] = round(float(result['DNAMT']) / 100000, 2)
        result['UNBILLEDAMT'] = round(float(result['UNBILLEDAMT']) / 100000, 2)
        result['ABOVEODDAYS'] = round(float(result['ABOVEODDAYS']) / 100000, 2)
        GDataBrokerWiseOS.append(result)
        total = total + (float("%.2f" % float(result['TOTAL'])))
        upto15 = upto15 + (float("%.2f" % float(result['UPTO15'])))
        range16 = range16 + (float("%.2f" % float(result['RANGE16'])))
        over30 = over30 + (float("%.2f" % float(result['OVER30'])))
        dnamt = dnamt + (float("%.2f" % float(result['DNAMT'])))
        advance = advance + (float("%.2f" % float(result['UNBILLEDAMT'])))
        unbilled = unbilled + (float("%.2f" % float(result['UNBILLEDAMT'])))
        unadj = unadj + (float("%.2f" % float(result['UNBILLEDAMT'])))
        olddays = olddays + (float("%.2f" % float(result['ABOVEODDAYS'])))
        result = con.db.fetch_both(stmt)
    for i in GDataBrokerWiseOS:
        if i['COMPANY'] not in GDataCompany:
            GDataCompany.append(i['COMPANY'])

    for j in GDataCompany:
        for k in GDataBrokerWiseOS:
            if j != k['COMPANY']:
                b=k['COMPANY']
                t = t+float(k['TOTAL'])
                u = u+float(k['UPTO15'])
                r = r+float(k['RANGE16'])
                o = o+float(k['OVER30'])
                d = d+float(k['DNAMT'])
                un = un+float(k['UNBILLEDAMT'])
                a = a + float(k['ABOVEODDAYS'])

        else:
            if b !=0:
                resultset = {
                        'COMPANY':b,
                        'TOTAL': float("%.2f" % t),
                        'UPTO15':float("%.2f" % u),
                        'RANGE16':float("%.2f" % r),
                        'OVER30':float("%.2f" % o),
                        'DNAMT':float("%.2f" % d),
                        'UNBILLEDAMT':float("%.2f" % un),
                        'ABOVEODDAYS':float("%2f" % a)
                    }
                GDataTotalCompany.append(resultset)
                b = 0
                t = 0
                u = 0
                r = 0
                o = 0
                d = 0
                un = 0
                a=0
    print(GDataTotalCompany)
    return render(request, 'CompanyWiseOS.html', {'GDataBrokerWiseOS': GDataBrokerWiseOS,'GDataCompany':GDataCompany,'GDataTotalCompany':GDataTotalCompany,'s':0,
                                                       'total': str(
                                                           format_currency((float("%.2f" % float(total))),
                                                                           'INR', locale='en_IN')).replace('₹', ''),
                                                       'upto15': str(
                                                           format_currency((float("%.2f" % float(upto15))), 'INR',
                                                                           locale='en_IN')).replace('₹', ''),
                                                       'range16': str(
                                                           format_currency((float("%.2f" % float(range16))), 'INR',
                                                                           locale='en_IN')).replace('₹', ''),
                                                       'over30': str(
                                                           format_currency((float("%.2f" % float(over30))),
                                                                           'INR', locale='en_IN')).replace('₹', ''),
                                                       'dnamt': str(
                                                            format_currency((float("%.2f" % float(dnamt))),
                                                                     'INR', locale='en_IN')).replace('₹', ''),
                                                 'advance': str(
                                                     format_currency((float("%.2f" % float(advance))),
                                                                     'INR', locale='en_IN')).replace('₹', ''),
                                                 'unbilled': str(
                                                     format_currency((float("%.2f" % float(unbilled))),
                                                                     'INR', locale='en_IN')).replace('₹', ''),
                                                 'unadj': str(
                                                     format_currency((float("%.2f" % float(unadj))),
                                                                     'INR', locale='en_IN')).replace('₹', ''),
                                                 'olddays': str(
                                                     format_currency((float("%.2f" % float(olddays))),
                                                                     'INR', locale='en_IN')).replace('₹', ''),
                                                 'TOTAL': str(
                                                     format_currency((float("%.2f" % float(TOTAL))),
                                                                     'INR', locale='en_IN')).replace('₹', '')
                                                       # 'startdate': stdt.strftime("%d %B %Y"),
                                                       # 'enddate': etdt.strftime("%d %B %Y")}
                                                 })