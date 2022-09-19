from django.shortcuts import render
from Global_Files import Connection_String as con

GDataDivision=[]
GDataLOGICALWAREHOUSE = []
GDataStartGrnNo = []
GDataEndGrnNo = []
GDGoodsSummary = []

Exceptions = ''
# companyunitcode = " "
# StartDate = ''
# EndDate = ''

stmt = con.db.exec_immediate(con.conn,"select code,longdescription from DIVISION order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataDivision:
        GDataDivision.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select code,longdescription from LOGICALWAREHOUSE order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataLOGICALWAREHOUSE:
        GDataLOGICALWAREHOUSE.append(result)
    result = con.db.fetch_both(stmt)


def PrintGoodsReceiptNoteHtml(request):
    return render(request, 'PrintGoodsReceiptNote.html',
                  {'GDataDivision': GDataDivision, 'GDataLOGICALWAREHOUSE':GDataLOGICALWAREHOUSE })

# Create your views here.
# def home(request):
#     return render(request,'index.html')

#value in Grid
def PrintGoodsReceipt(request):
    global GDGoodsSummary
    # global companyunitcode
    # global StartDate
    # global EndDate

    GDGoodsSummary = []
    LSCompanyUnitCode = request.GET.getlist('Division')
    LSLOGICALWAREHOUSE = request.GET.getlist('comp')
    LSLOGICALWAREHOUSEs = '(' + str(request.GET.getlist('comp'))[1:-1] + ')'
    LCLOGICALWAREHOUSE = request.GET.getlist('allcomp')
    LDStartDate = "'" + str(request.GET['startdate']) + "'"
    LDEndDate = "'" + str(request.GET['enddate']) + "'"
    # StartDate = request.GET['startdate']
    # EndDate = request.GET['enddate']
    # print((LSLOGICALWAREHOUSE))
    # print("End : ", len(LSEndGrnNos))

    LCCompanyUnitCode = request.GET.getlist('allDivision')

    companyunitcodes = str(LSCompanyUnitCode)
    LSCompanyUnitCodes = '(' + companyunitcodes[1:-1] + ')'

    if not LCCompanyUnitCode and not LSCompanyUnitCode:
        companyunitcode = " "
    elif LCCompanyUnitCode:
        companyunitcode = " "
    elif LSCompanyUnitCode:
        companyunitcode = "AND MRNHEADER.DIVISIONCODE in " + str(LSCompanyUnitCodes)

    if not LCLOGICALWAREHOUSE and not LSLOGICALWAREHOUSE:
        LOGICALWAREHOUSECODE = " "
    elif LCLOGICALWAREHOUSE:
        LOGICALWAREHOUSECODE = " "
    elif LSLOGICALWAREHOUSE:
        LOGICALWAREHOUSECODE = "AND LOGICALWAREHOUSE.CODE in " + str(LSLOGICALWAREHOUSEs)
    # print(LOGICALWAREHOUSECODE)

    sql = "Select  LOGICALWAREHOUSE.CODE AS Whcode " \
          ", MRNHEADER.CODE  AS GRNNumber " \
          ", VARCHAR_FORMAT(MRNHEADER.MRNDATE, 'DD-MM-YYYY') As GRNDate " \
          ", CAST(SUM(Round(MRNDETAIL.GROSSVALUEWOHEADER,0)) AS INT) As Amount " \
          "From      MRNHEADER " \
          "Join      Division                On      MRNHEADER.DIVISIONCODE = DIVISION.CODE " \
          "JOIN      MRNDETAIL               On      MRNHEADER.CODE =  MRNDETAIL.MRNHEADERCODE " \
          "AND     MRNHEADER.MRNPREFIXCODE  =  MRNDETAIL.MRNHEADERMRNPREFIXCODE " \
          "Join     LOGICALWAREHOUSE        On       MRNDETAIL.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "WHERE    MRNHEADER.MRNDATE       BETWEEN "+LDStartDate+"    AND     "+LDEndDate+" "+companyunitcode+" " \
          " "+LOGICALWAREHOUSECODE+" " \
          "Group By  LOGICALWAREHOUSE.CODE,MRNHEADER.CODE,VARCHAR_FORMAT(MRNHEADER.MRNDATE, 'DD-MM-YYYY') " \
          "ORDER BY       Whcode, GRNDATE Asc, GRNNUMBER "
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        GDGoodsSummary.append(result)
        result = con.db.fetch_both(stmt)


    # if result == False:
    #     if counter > 0:
    #         Exceptions = ""
    #         counter = 0

    if GDGoodsSummary == []:
        global Exceptions
        Exceptions = "Note: No Result found on given criteria "
        return render(request, 'PrintGoodsReceiptNote.html',
                      {'GDataDivision': GDataDivision, 'GDataStartGrnNo': GDataStartGrnNo,
                       'GDataEndGrnNo': GDataEndGrnNo, 'Exception': Exceptions})
    else:
        return render(request, 'PrintGoodsReceiptNote_Table.html',
                  {'GDGoodsSummary': GDGoodsSummary})