from datetime import datetime
from django.shortcuts import render
from Global_Files import Connection_String as con
from FormLoad import PrintDespatchInstruction_FormLoad as PDIFL
Exceptions=""
save_name=""
LSFileName=""
GDataPrintDespatch = []
LSDocumentType=[]
def PrintDespatch_PrintPDF(request):
    global LSFileName
    global save_name
    global GDataPrintDespatch
    GDataPrintDespatch = []
    LSReportType = request.GET.getlist('type')

    if LSReportType[0]=='1':
        response = PrintDespatch(request)
        return response


    elif LSReportType[0]=='2':
        response = PrintDespatchWithoutRD(request)
        return response


def PrintDespatch(request):
    global save_name
    global GDataPrintDespatch
    global LSDocumentType
    LSDocumentType=[]
    GDataPrintDespatch = []
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LDStartDate = "'" + request.GET['startdate'] + "'"
    LDEndDate = "'" + request.GET['enddate'] + "'"
    LSStartOrderNo = request.GET.getlist('stordno')
    LSEndOrderNo = request.GET.getlist('endordno')
    LSItemType = request.GET.getlist('item')
    ItemType = str(LSItemType)
    ItemType = '(' + ItemType[1:-1] + ')'
    # LSDriveForOrdTrfTofatory = request.GET['drive']
    LSReportType = request.GET.getlist('type')
    LSDocumentType = request.GET.getlist('documenttype')
    # LSFolderName = request.GET['fname']


    if not LSStartOrderNo:
        StartordNo=" "
    else:
        StartordNo = "" + str(LSStartOrderNo)

    if not LSEndOrderNo:
        EndordNo=" "
    else:
        EndordNo = "" + str(LSEndOrderNo)

    if not LSItemType:
        ItemType = " "
    else:
        ItemType = " And SOL.ITEMTYPEAFICODE in " + ItemType

    # if not LSDriveForOrdTrfTofatory:
    #     Drive=" "
    # else:
    #     Drive = "" + str(LSDriveForOrdTrfTofatory)

    if not LSReportType:
        ReportType=" "
    else:
        ReportType = "" + str(LSReportType)

    if not LSDocumentType:
        DocumentType=" "
    else:
        DocumentType="" + str(LSDocumentType)

    # if not LSFolderName:
    #     FolderName=" "
    # else:
    #     FolderName = "" + str(LSFolderName)

    sql = "SELECT " \
          " SO.CODE AS DespatchNo" \
          " ,VARCHAR_FORMAT(SO.ORDERDATE,'YYYY-MM-DD') AS DespatchDate" \
          " ,BP.LEGALNAME1 AS BuyerName" \
          " ,AGENT.LONGDESCRIPTION AS Broker" \
          " FROM SALESORDER AS SO" \
          " JOIN SalesOrderLine     AS SOL                          ON      SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE" \
          " AND     SO.CODE = SOL.SALESORDERCODE " \
          " JOIN OrderPartner       AS OP                           ON      SO.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode" \
          " AND     OP.CustomerSupplierType = 1" \
          " JOIN BusinessPartner    AS BP                           ON      OP.OrderbusinessPartnerNumberId = BP.NumberID" \
          " LEFT JOIN AGENT                                         ON      SO.Agent1Code = Agent.Code" \
          " WHERE SOL.DOCUMENTTYPETYPE IN ('"+LSDocumentType[0]+"') AND SO.ORDERDATE between" \
          "" + LDStartDate + "AND" + LDEndDate +""+ ItemType+"" \
          " ORDER BY DespatchNo"

    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)


    if result==False:
        Exceptions=1
        return render(request, 'PrintDespatchInstruction.html', {'GDataItemType': PDIFL.GDataItemType,'Exception':Exceptions})
    else:
        while result != False:
            if result not in GDataPrintDespatch:
                GDataPrintDespatch.append(result)
            result = con.db.fetch_both(stmt)
        return render(request, 'PrintDespatchInstructionTable.html',
                      {'GDataPrintDespatch': GDataPrintDespatch})



def PrintDespatchWithoutRD(request):
    global save_name
    global GDataPrintDespatch
    global LSDocumentType
    GDataPrintDespatch = []
    LSDocumentType = []
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LDStartDate = "'" + request.GET['startdate'] + "'"
    LDEndDate = "'" + request.GET['enddate'] + "'"
    LSStartOrderNo = request.GET.getlist('stordno')
    LSEndOrderNo = request.GET.getlist('endordno')
    LSItemType = request.GET.getlist('item')
    ItemType = str(LSItemType)
    ItemType = '(' + ItemType[1:-1] + ')'
    # LSDriveForOrdTrfTofatory = request.GET['drive']
    LSReportType = request.GET.getlist('type')
    LSDocumentType = request.GET.getlist('documenttype')
    # LSFolderName = request.GET['fname']

    if not LSStartOrderNo:
        StartordNo = " "
    else:
        StartordNo = "" + str(LSStartOrderNo)

    if not LSEndOrderNo:
        EndordNo = " "
    else:
        EndordNo = "" + str(LSEndOrderNo)

    if not LSItemType:
        ItemType = " "
    else:
        ItemType = " And SOL.ITEMTYPEAFICODE in " + ItemType

    # if not LSDriveForOrdTrfTofatory:
    #     Drive = " "
    # else:
    #     Drive = "" + str(LSDriveForOrdTrfTofatory)

    if not LSReportType:
        ReportType = " "
    else:
        ReportType = "" + str(LSReportType)

    if not LSDocumentType:
        DocumentType=" "
    else:
        DocumentType="" + str(LSDocumentType)

    # if not LSFolderName:
    #     FolderName = " "
    # else:
    #     FolderName = "" + str(LSFolderName)

    sql = "SELECT DISTINCT" \
          " SO.CODE AS DespatchNo" \
          " ,VARCHAR_FORMAT(SO.ORDERDATE,'YYYY-MM-DD') AS DespatchDate" \
          " ,BP.LEGALNAME1 AS BuyerName" \
          " ,AGENT.LONGDESCRIPTION AS Broker" \
          " FROM SALESORDER AS SO" \
          " JOIN SalesOrderLine     AS SOL                          ON      SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE" \
          " AND     SO.CODE = SOL.SALESORDERCODE " \
          " JOIN OrderPartner       AS OP                           ON      SO.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode" \
          " AND     OP.CustomerSupplierType = 1" \
          " JOIN BusinessPartner    AS BP                           ON      OP.OrderbusinessPartnerNumberId = BP.NumberID" \
          " LEFT JOIN AGENT                                         ON      SO.Agent1Code = Agent.Code" \
          " WHERE SOL.DOCUMENTTYPETYPE IN ('"+LSDocumentType[0]+"') AND SO.ORDERDATE between" \
          "" + LDStartDate + "AND" + LDEndDate +""+ ItemType+"" \
          " ORDER BY DespatchNo"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)

    if result==False:
        Exceptions=1
        return render(request, 'PrintDespatchInstruction.html', {'GDataItemType': PDIFL.GDataItemType,'Exception':Exceptions})
    else:
        while result != False:
            if result not in GDataPrintDespatch:
                GDataPrintDespatch.append(result)
            result = con.db.fetch_both(stmt)
        return render(request, 'PrintDepatchInstructionTable_WithoutRD.html',
                      {'GDataPrintDespatch': GDataPrintDespatch})


