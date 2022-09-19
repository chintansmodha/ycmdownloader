from datetime import datetime
from django.shortcuts import render
from Global_Files import Connection_String as con
from FormLoad import StoresRequisition_FormLoad as SRFL
Company=[]
Exceptions=""
save_name=""
LSFileName=""
GDataStoresRequisition=[]

def StoresRequisition_PrintPDF(LSCompany,LDStartDate,LDEndDate,request):
    global save_name
    global GDataStoresRequisition
    GDataStoresRequisition = []
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSCompany = request.GET.getlist('dept')
    Company = str(LSCompany)
    Company = '(' + Company[1:-1] + ')'
    LDStartDate = "'" + request.GET['startdate'] + "'"
    LDEndDate = "'" + request.GET['enddate'] + "'"
    LSStartNo = request.GET.getlist('stno')
    LSEndNo = request.GET.getlist('endno')

    if not LSCompany:
        Company = " "
    else:
        Company = " And CostCenter.Code in " + Company

    if not LSStartNo:
        StartNo = " "
    else:
        StartNo = "" + str(LSStartNo)

    if not LSEndNo:
        EndNo = " "
    else:
        EndNo = "" + str(LSEndNo)

    sql="SELECT DISTINCT ID.PROVISIONALCODE AS REQUISITIONNO" \
        " ,VARCHAR_FORMAT(ID.PROVISIONALDOCUMENTDATE,'DD-MM-YYYY') AS REQUISITIONDATE" \
        " FROM INTERNALDOCUMENT AS ID" \
        " JOIN InternalDocumentLine AS IDL        ON      ID.PROVISIONALCODE = IDL.INTDOCUMENTPROVISIONALCODE" \
        " AND     ID.PROVISIONALCOUNTERCODE = IDL.INTDOCPROVISIONALCOUNTERCODE" \
        " JOIN ORDERPARTNER AS OP                 ON      ID.ORDPRNCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode" \
        " AND     OP.CustomerSupplierType = 3" \
        " JOIN LOGICALWAREHOUSE                   ON      OP.ORDERLOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
        " JOIN COSTCENTER                         ON      LogicalWarehouse.COSTCENTERCODE = CostCenter.Code" \
        " WHERE ID.PROVISIONALCOUNTERCODE='I04' AND ID.DOCUMENTTYPETYPE='05' AND ID.PROVISIONALDOCUMENTDATE BETWEEN" \
        " " + LDStartDate + "AND" + LDEndDate +""+ Company+" " \
        " ORDER BY REQUISITIONNO,REQUISITIONDATE"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    if result==False:
        Exceptions = "Note: No Result found according to your selected criteria"
        return render(request, 'StoresRequisition.html',{'GDataCompany':SRFL.GDataCompany,'Exception':Exceptions})

    while result != False:
        GDataStoresRequisition.append(result)
        result = con.db.fetch_both(stmt)

    return render(request, 'StoresRequisitionTable.html',{'GDataStoresRequisition': GDataStoresRequisition})