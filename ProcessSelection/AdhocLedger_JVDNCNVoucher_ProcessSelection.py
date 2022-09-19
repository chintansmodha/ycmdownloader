from datetime import datetime

from django.shortcuts import render

from . import AdhocLedger_ProcessSelection
from Global_Files import Connection_String as con
GDataJVDNCNVoucher=[]
def JVDNCNVoucher(request):

    global GDataJVDNCNVoucher
    GDataJVDNCNVoucher=[]
    LIVoucherNo = str(request.GET['vchno'])
    LSDocType = str(request.GET['doctype'])
    LSYear = str(request.GET['year'])
    LDVoucherDate = str(request.GET['vchdate'])[6:]+str(request.GET['vchdate'])[5]+str(request.GET['vchdate'])[3:5]+str(request.GET['vchdate'])[2]+str(request.GET['vchdate'])[0:2]


    LIChequeNo = request.GET.getlist('chqno')


    if LSYear == None:
        LSYear=''
    else:
        LSYear = " AND FD.FINANCIALYEARCODE ='"+LSYear+"'"

    if LSDocType == None:
        LSDocType=''
    else:
        LSDocType = " FD.DocumentTypeCode ='"+LSDocType+"'"

    if LIVoucherNo == None:
        LIVoucherNo=''
    else:
        LIVoucherNo=" AND FD.CODE='"+LIVoucherNo+"'"

    if LDVoucherDate == None:
        LDVoucherDate=''
    else:
        LDVoucherDate=" AND FD.FINANCEDOCUMENTDATE='"+LDVoucherDate+"'"

    # if not LIChequeNo or LIChequeNo[0]=='None':
    #     LIChequeNo=''
    # else:
    #     LIChequeNo=" AND FD.CHEQUENUMBER='"+str(LIChequeNo[0])+"'"

    sql = " select BUnit.LongDescription As Company " \
          ",BankMaster.LongDescription As BankName" \
          ",BP.LegalName1 As Party" \
          ",UGGSH.LongDescription As SummHead" \
          ",Agent.LONGDESCRIPTION As Broker" \
          ",FD.Code As VoucherNo" \
          ",VARCHAR_FORMAT(FD.PostingDate, 'YYYY-MM-DD') As VoucherDate" \
          ",FD.CHEQUENUMBER As ChqNo" \
          ",FD.CHEQUEDATE As ChqDate " \
          ",COALESCE(FD.VENDORREFERENCE, FD.CUSTOMERREFERENCE, '') As REFNO" \
          ",VARCHAR_FORMAT(COALESCE(FD.VENDORREFERENCEDATE" \
          ",FD.CUSTOMERREFERENCEDATE, '1900-01-01'), 'YYYY-MM-DD') As REFDATE" \
          ",COALESCE(NT.Note,'') As Remarks" \
          ",Case When FDL_GL.GLType = 'A' Then 'Assets' " \
          "When FDL_GL.GLType = 'L' Then 'Liabilities' " \
          "When FDL_GL.GLType = 'I' Then 'Income' " \
          "When FDL_GL.GLType = 'E' Then 'Expenses' " \
          "End As ACHead" \
          ",FDL_GL.LONGDESCRIPTION As FDL_LedgerAccount" \
          ",BP_SubLedger.LEGALNAME1 As FDL_SubLedger" \
          ",CASE WHEN FDL.Creditline=1 THEN 'Credit' ELSE 'Debit' END As DRCR" \
          ",cast(abs(FDL.AMOUNTINCC)as decimal(18,2)) As Amount" \
          ",cast(abs(FDL.AMOUNTINDC) As decimal(18,2)) As CURR_AMT" \
          ",FD.DOCUMENTAMOUNT AS HEADAMOUNT" \
          ", COALESCE(NTE.NOTE,'') As Detail_Remarks" \
          ",FDL.DOCUMENTCURRENCYCODE as Currancy" \
          ",cast(FD.TDSPERCENTAGE as decimal(18,2)) as TDS" \
          ",cast(FD.TDSAMOUNT as decimal(18,2)) as TDSAMOUNT" \
          ",cast(FD.TDSAPPLICABLEAMOUNT as decimal(18,2)) as  TDSAPPLICABLEAMOUNT " \
          ",FD.TDSGLCODE as  TDSGLCODE " \
          " FROM FinDocument AS FD " \
          " JOIN FinBusinessUnit BUnit           ON      FD.BusinessUnitcode = BUnit.Code " \
          " AND BUnit.GroupFlag = 0" \
          " Left JOIN OrderPartner AS OP ON COALESCE(FD.CUSTOMERCODE,FD.SUPPLIERCODE,'') = OP.CUSTOMERSUPPLIERCODE " \
          " And COALESCE(FD.CUSTOMERType,FD.SUPPLIERType,'') = OP.CUSTOMERSUPPLIERTYPE" \
          " Left JOIN BusinessPartner AS BP           ON OP.ORDERBUSINESSPARTNERNUMBERID = BP.NumberID" \
          " JOIN GLMaster AS BankMaster          ON FD.GLCODE = BankMaster.Code" \
          " LEFT JOIN Agent                           ON FD.AGENT1CODE = Agent.CODE " \
          " LEFT JOIN Note AS NT                      ON FD.AbsUniqueID = NT.FatherId " \
          " LEFT JOIN AdStorage As SummHead           ON      FD.AbsUniqueId = SummHead.UniqueId " \
          " And SummHead.NameEntityName = 'FINDocument'" \
          " And SummHead.NameName = 'summaryhead'" \
          " And SummHead.FieldName = 'summaryheadCode'" \
          " LEFT JOIN UserGenericGroup As UGGSH       ON UserGenericGroupTypeCode = 'SH'" \
          " AND SummHead.ValueString = UGGSH.Code" \
          " JOIN FinDocumentLine  AS FDL         ON  FD.BUSINESSUNITCODE = FDL.FINDOCUMENTBUSINESSUNITCODE " \
          " AND FD.CODE = FDL.FINDOCUMENTCODE " \
          " AND FD.FINANCIALYEARCODE = FDL.FINDOCUMENTFINANCIALYEARCODE" \
          " LEFT JOIN NOTE AS NTE                     ON FDL.AbsUniqueID = NT.FatherId" \
          " JOIN GLMaster AS FDL_GL              ON FDL.GLCODE = FDL_GL.CODE" \
          " LEFT JOIN OrderPartner AS FDL_SubLedger   ON  FDL.SLCUSTOMERSUPPLIERCODE = FDL_SubLedger.CUSTOMERSUPPLIERCODE " \
          " AND FDL.SLCUSTOMERSUPPLIERTYPE = FDL_SubLedger.CUSTOMERSUPPLIERTYPE" \
          " Left JOIN businesspartner AS BP_SubLedger ON  FDL_SubLedger.ORDERBUSINESSPARTNERNUMBERID = BP_SubLedger.NUMBERID " \
          " where " + LSDocType + "" + LIVoucherNo + LSYear + LDVoucherDate + "" \
    #, 'JV', 'CD', 'CC', 'VD', 'VC'

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    resultset = result
    print(resultset)
    while result != False:
        if result['REFDATE'] == '1900-01-01':
            result['REFDATE'] = ''
        GDataJVDNCNVoucher.append(result)
        result = con.db.fetch_both(stmt)

    return render(request, "JVDNCNVoucher.html", {'result': resultset,'GDataJVDNCNVoucher':GDataJVDNCNVoucher})