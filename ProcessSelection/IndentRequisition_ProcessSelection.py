from datetime import datetime
from django.shortcuts import render
from Global_Files import Connection_String as con
from FormLoad import IndentRequisition_FormLoad as IRFL
Company=[]
Exceptions=""
save_name=""
LSFileName=""
GDataIndentRequisition=[]

def IndentRequisition_PrintPDF(LSCompany,LDStartDate,LDEndDate,request):
    global save_name
    global GDataIndentRequisition
    GDataIndentRequisition = []
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

    sql="SELECT REPL_REQ.REQUISITIONTEMPLATECODE ||''||REPL_REQ.CODE AS INDENTNO" \
        " ,VARCHAR_FORMAT(REPL_REQ.PROPOSALDATE,'DD-MM-YYYY') AS INDENTDATE" \
        " FROM REPLENISHMENTREQUISITION AS REPL_REQ" \
        " JOIN COSTCENTER         ON      REPL_REQ.COSTCENTERCODE = COSTCENTER.CODE" \
        " WHERE REPL_REQ.REPLENISHMENTTYPE = '1' AND REPL_REQ.PROPOSALDATE BETWEEN" \
        " " + LDStartDate + "AND" + LDEndDate + "" + Company + " " \
        " ORDER BY INDENTNO,INDENTDATE "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)


    if result==False:
        Exceptions = "Note: No Result found according to your selected criteria"
        return render(request, 'IndentRequisition.html',{'GDataCompany':IRFL.GDataCompany,'Exception':Exceptions})

    while result != False:
        GDataIndentRequisition.append(result)
        result = con.db.fetch_both(stmt)

    return render(request, 'IndentRequisitionTable.html',{'GDataIndentRequisition': GDataIndentRequisition})