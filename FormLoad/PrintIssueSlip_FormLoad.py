from django.shortcuts import render
from Global_Files import Connection_String as con

Exceptions = ''

GDataIssueSlipSummary = []
GDataDepartment = []
GDataToDepartment = []

stmt = con.db.exec_immediate(con.conn,"select code,LONGDESCRIPTION  from LOGICALWAREHOUSE order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataDepartment:
        GDataDepartment.append(result)
    result = con.db.fetch_both(stmt)


def PrintIssueSlipHtml(request):
    return render(request, 'PrintIssueSlip.html',
                  {'GDataDepartment': GDataDepartment, 'GDataToDepartment': GDataDepartment })


def PrintIssueSlip(request):
    global GDataIssueSlipSummary

    GDataIssueSlipSummary = []
    LSDepartmentUnitCode = request.GET.getlist('department')
    LSToDepartmentUnitCode = request.GET.getlist('todepartment')
    LDStartDate = "'" + str(request.GET['startdate']) + "'"
    LDEndDate = "'" + str(request.GET['enddate']) + "'"
    # print(LDStartDate, LDStartDate)

    LCDepartmentUnitCode = request.GET.getlist('alldepartment')

    Departmentunitcodes = str(LSDepartmentUnitCode)
    LSDepartmentUnitCodes = '(' + Departmentunitcodes[1:-1] + ')'

    ToDepartmentunitcodes = str(LSToDepartmentUnitCode)
    LSToDepartmentUnitCodes = '(' + ToDepartmentunitcodes[1:-1] + ')'

    if not LCDepartmentUnitCode and not LSDepartmentUnitCode:
        departmentunitcode = " "
    elif LCDepartmentUnitCode:
        departmentunitcode = " "
    elif LSDepartmentUnitCode:
        if LSDepartmentUnitCode != ['']:
            departmentunitcode = "AND ID.WAREHOUSECODE in " + str(LSDepartmentUnitCodes)
        else:
            departmentunitcode = ""

    if LSToDepartmentUnitCode:
        if LSToDepartmentUnitCode != ['']:
            todepartmentunitcode = "AND ID.DESTINATIONWAREHOUSECODE in " + str(LSToDepartmentUnitCodes)
        else:
            todepartmentunitcode = ""
    else:
        todepartmentunitcode = " "
    # print(companyunitcode)
    # print(departmentunitcode,todepartmentunitcode)

    sql = "Select    Stxn.DERIVATIONCODE As IssueNo " \
          ", VARCHAR_FORMAT(Stxn.TRANSACTIONDATE, 'DD-MM-YYYY') As IssueDt " \
          ", ID.PROVISIONALCODE As ReqNumber " \
          ", VARCHAR_FORMAT(ID.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') As ReqDate " \
          ", Cast(Sum(Stxn.USERPRIMARYQUANTITY) As Decimal(20,3)) As IssueQuantity " \
          ", LOGICALWAREHOUSE.LONGDESCRIPTION  As FromDepartment " \
          ", COALESCE(IsuDept.LONGDESCRIPTION,' ') As   toDepartment " \
          "From    STOCKTRANSACTION Stxn " \
          "Join    INTERNALDOCUMENT  ID                    On      Stxn.OrderCode = ID.PROVISIONALCODE " \
          "AND     Stxn.ORDERCOUNTERCODE = ID.PROVISIONALCOUNTERCODE " \
          "join    LOGICALWAREHOUSE                        On      ID.WAREHOUSECODE             =      LOGICALWAREHOUSE.Code " \
          "join    LOGICALWAREHOUSE As IsuDept             On      ID.DESTINATIONWAREHOUSECODE  =      IsuDept.CODE " \
          "Join    ALLOCATION                              On      Stxn.DERIVATIONCODE = ALLOCATION.CODE " \
          "And     Stxn.DERIVATIONLINENUMBER = ALLOCATION.LINENUMBER " \
          "And     ALLOCATION.DETAILTYPE = '0' " \
          "Where   Stxn.TRANSACTIONDATE  between      "+LDStartDate+"     and     "+LDEndDate+" "+departmentunitcode+"  " \
          " "+todepartmentunitcode+" " \
          "Group   By  Stxn.DERIVATIONCODE " \
          ", VARCHAR_FORMAT(Stxn.TRANSACTIONDATE, 'DD-MM-YYYY') " \
          ", ID.PROVISIONALCODE " \
          ", VARCHAR_FORMAT(ID.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') " \
          ", LOGICALWAREHOUSE.LONGDESCRIPTION " \
          ", COALESCE(IsuDept.LONGDESCRIPTION,' ') " \
          "Order   By      IssueNo, IssueDt Desc, ReqNumber, ReqDate Desc, FromDepartment, toDepartment "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        GDataIssueSlipSummary.append(result)
        result = con.db.fetch_both(stmt)


    if GDataIssueSlipSummary == []:
        global Exceptions
        Exceptions = "Note: No Result found on given criteria "
        return render(request, 'PrintIssueSlip.html',
                      {'GDataDepartment': GDataDepartment, 'GDataToDepartment': GDataDepartment, 'Exception': Exceptions})
    else:
        return render(request, 'PrintIssueSlip_Table.html',
                      {'GDataIssueSlipSummary': GDataIssueSlipSummary})


    # return render(request, 'PrintIssueSlip_Table.html',
    #               {'GDataDepartment': GDataDepartment, 'GDataToDepartment': GDataDepartment})