from datetime import datetime

from django.shortcuts import render

from . import AdhocLedger_ProcessSelection
from Global_Files import Connection_String as con
GDataBankCashVoucher=[]
def BankCashVoucher(request,type):

    global GDataBankCashVoucher
    GDataBankCashVoucher=[]


    LIVoucherNo = " And FD.CODE='"+str(request.GET['vchno'])+"'"
    LSDocType = str(request.GET['doctype'])
    LSYear = str(request.GET['year'])
    LDVoucherDate = str(request.GET['vchdate'])[6:]+str(request.GET['vchdate'])[5]+str(request.GET['vchdate'])[3:5]+str(request.GET['vchdate'])[2]+str(request.GET['vchdate'])[0:2]
    LIChequeNo = request.GET.getlist('chqno')
    companycode=''
    accountcode=''
    subaccountcode=''
    yearcode=''
    doccode=''
    vchno=''
    startdate = datetime.strptime(request.GET['startdate'], "%d %B %Y")
    enddate = datetime.strptime(request.GET['enddate'], "%d %B %Y")
    if request.GET['CompanyCode']:
        companycode = " And FDL.FINDOCUMENTBUSINESSUNITCODE='"+str(request.GET['CompanyCode'])+"'"

    if request.GET['AccountCode']:
        accountcode = " And FDL.GLCODE='"+str(request.GET['AccountCode'])+"'"

    if int(request.GET['SubAccountCode']) != 0:
        subaccountcode = " And businesspartner.NUMBERID='"+str(request.GET['SubAccountCode'])+"'"

    if request.GET['year']:
        yearcode = " And FDL.FINDOCUMENTFINANCIALYEARCODE='" + str(request.GET['year']) + "'"

    if request.GET['doctype']:
        doccode = " And FDL.FINDOCDOCUMENTTEMPLATECODE='" + str(request.GET['doccode']) + "'"

    if request.GET['vchno']:
        vchno = " And FDL.FINDOCUMENTCODE='" + str(request.GET['vchno']) + "'"

    sql = " select finbusinessunit.LongDescription As Company" \
          ",glmaster.LongDescription As BankName" \
          ",businesspartner.LegalName1 As Party" \
          ",UGGSH.LongDescription As SummHead" \
          ",Agent.LONGDESCRIPTION As Broker" \
          ",FD.Code As VoucherNo" \
          ",VARCHAR_FORMAT(FD.PostingDate, 'YYYY-MM-DD') As VoucherDate" \
          ",COALESCE(FD.CHEQUENUMBER,CHQN.Valuestring,'') As ChqNo" \
          ",COALESCE(FD.CHEQUEDATE,CHQD.ValueDate,'01-01-1990') As ChqDate" \
          ",COALESCE(FD.VENDORREFERENCE, FD.CUSTOMERREFERENCE, '') As REFNO" \
          ",VARCHAR_FORMAT(COALESCE(FD.VENDORREFERENCEDATE" \
          ",FD.CUSTOMERREFERENCEDATE, '1900-01-01'), 'YYYY-MM-DD') As REFDATE" \
          ",COALESCE(NT.Note,'') As Remarks" \
          ",Case When glmaster.GLType = 'A' Then 'Assets'" \
          " When glmaster.GLType = 'L' Then 'Liabilities'" \
          " When glmaster.GLType = 'I' Then 'Income'" \
          " When glmaster.GLType = 'E' Then 'Expenses'" \
          " End As ACHead" \
          ",glmaster.LONGDESCRIPTION As FDL_LedgerAccount" \
          ",businesspartner.LEGALNAME1 As FDL_SubLedger" \
          ",CASE WHEN FDL.Creditline=1 THEN 'Credit' ELSE 'Debit' END As DRCR" \
          ",cast(abs(FDL.AMOUNTINCC)as decimal(18,2)) As Amount" \
          ",cast(abs(FDL.AMOUNTINDC) As decimal(18,2)) As CURR_AMT" \
          ",FD.DOCUMENTAMOUNT AS HEADAMOUNT" \
          ",COALESCE(NT.NOTE,'') As Detail_Remarks" \
          ",FDL.DOCUMENTCURRENCYCODE as Currancy" \
          ",cast(FD.TDSPERCENTAGE as decimal(18,2)) as TDS" \
          ",cast(FD.TDSAMOUNT as decimal(18,2)) as TDSAMOUNT" \
          ",cast(FD.TDSAPPLICABLEAMOUNT as decimal(18,2)) as  TDSAPPLICABLEAMOUNT" \
          ",FD.TDSGLCODE as  TDSGLCODE" \
          ",Case When FD.CURRENTSTATUS = '0' Then 'Suspended'" \
          " When FD.CURRENTSTATUS = '1' Then 'Active' End AS CURRENTSTATUS" \
          ",Case When FD.PROGRESSSTATUS = '0' Then 'Open'" \
          " When FD.PROGRESSSTATUS = '1' Then 'Partial'" \
          " When FD.PROGRESSSTATUS = '2' Then 'Closed' End AS DOCSTATUS" \
          " from FinDocumentLine as FDL" \
          " join findocument as FD on FDL.FINDOCUMENTCOMPANYCODE = FD.COMPANYCODE" \
          " AND FDL.FINDOCUMENTBUSINESSUNITCODE = FD.BUSINESSUNITCODE" \
          " AND FDL.FINDOCUMENTFINANCIALYEARCODE = FD.FINANCIALYEARCODE" \
          " AND FDL.FINDOCDOCUMENTTEMPLATECODE = FD.DOCUMENTTEMPLATECODE" \
          " AND FDL.FINDOCUMENTCODE = FD.CODE" \
          " join finbusinessunit on FD.BUSINESSUNITCODE = finbusinessunit.code" \
          " Join FINFinancialYear FInYear On FinYear.Code = FD.FINANCIALYEARCODE" \
          " join glmaster on FDL.glcode = glmaster.code" \
          " Left join orderpartner on  FDL.SLCUSTOMERSUPPLIERTYPE =orderpartner.CUSTOMERSUPPLIERTYPE" \
          " AND FDL.SLCUSTOMERSUPPLIERCODE = orderpartner.CUSTOMERSUPPLIERCODE" \
          " Left join businesspartner on ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID" \
          " LEFT JOIN Agent                           ON FD.AGENT1CODE = Agent.CODE" \
          " LEFT JOIN Note AS NT                      ON FD.AbsUniqueID = NT.FatherId" \
          " LEFT JOIN AdStorage As SummHead           ON      FD.AbsUniqueId = SummHead.UniqueId" \
          " And SummHead.NameEntityName = 'FINDocument'" \
          " And SummHead.NameName = 'summaryhead'" \
          " And SummHead.FieldName = 'summaryheadCode'" \
          " LEFT JOIN UserGenericGroup As UGGSH       ON UserGenericGroupTypeCode = 'SH'" \
          " AND SummHead.ValueString = UGGSH.Code" \
          " LEFT JOIN AdStorage AS CHQN               ON  FD.AbsUniqueId = CHQN.UniqueId" \
          " AND CHQN.NameEntityName = 'FINDocument'" \
          " And CHQN.NameName = 'CustomerCheque'" \
          " And CHQN.FieldName = 'CustomerCheque'" \
          " LEFT JOIN AdStorage AS CHQD               ON  FD.AbsUniqueId = CHQD.UniqueId" \
          " AND CHQD.NameEntityName = 'FINDocument'" \
          " And CHQD.NameName = 'ChequeDate' And CHQD.FieldName = 'ChequeDate'" \
          " where FD.COMPANYCODE='100'"+companycode+accountcode+subaccountcode+yearcode+doccode+vchno+""
    print()
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    resultset=result
    print(resultset)
    while result!= False:
        if result['REFDATE'] == '1900-01-01':
            result['REFDATE'] = ''
        GDataBankCashVoucher.append(result)
        result = con.db.fetch_both(stmt)

    return render(request, "BankCashVoucher.html", {'result': resultset,'GDataBankCashVoucher':GDataBankCashVoucher,'type':type})