import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
from Global_Files import Connection_String as con
from PrintPDF import IndentRequisition_PrintPDF as pdfrpt
from ProcessSelection import IndentRequisition_ProcessSelection as IRQPS
save_name=""
counter=0
def IndentRequisitionPDF(request):
    print("Sanika")
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "IndentRequisition" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Indent Requisition/", LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSIndentNo = request.GET.getlist('indentno')
    LSIndentDate = request.GET.getlist('indentdt')
    LSIndentNo = " AND REPL_REQ.REQUISITIONTEMPLATECODE ||''||REPL_REQ.CODE in" + "(" + str(LSIndentNo)[1:-1] + ")"
    LSIndentDate = " AND REPL_REQ.PROPOSALDATE = " + "(" + str(LSIndentDate)[1:-1] + ")"

    PrintPDF(LSIndentNo, LSIndentDate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'IndentRequisitionTable.html', {'GDataIndentRequisition': IRQPS.GDataIndentRequisition,
                                                               'Exception': IRQPS.Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

def PrintPDF(LSIndentNo, LSIndentDate):
    sql="SELECT COSTCENTER.LONGDESCRIPTION AS COSTCENTERNAME" \
        " ,REPL_REQ.REQUISITIONTEMPLATECODE ||''||REPL_REQ.CODE AS INDENTNO" \
        " ,REPL_REQ.PROPOSALDATE AS INDENTDATE" \
        " ,REPL_REQ.LONGDESCRIPTION AS ITEM" \
        " ,REPL_REQ.ORDERUSERPRIMARYQUANTITY AS QUANTITY" \
        " ,REPL_REQ.ORDERUSERPRIMARYUOMCODE AS UNIT" \
        " ,REPL_REQ.DELIVERYDATE AS DELIVERYDATE" \
        " ,REPL_REQ.FIRSTLEVELAPPROVALDATE AS FIRSTLEVELAPPROVALDATE" \
        " ,REPL_REQ.FIRSTLEVELAPPROVALUSER AS FIRSTLEVELAPPROVALUSER" \
        " ,REPL_REQ.SECONDLEVELAPPROVALDATE AS SECONDLEVELAPPROVALDATE" \
        " ,REPL_REQ.SECONDLEVELAPPROVALUSER AS SECONDLEVELAPPROVALUSER" \
        " FROM REPLENISHMENTREQUISITION AS REPL_REQ" \
        " JOIN COSTCENTER         ON      REPL_REQ.COSTCENTERCODE = COSTCENTER.CODE" \
        " WHERE REPL_REQ.REPLENISHMENTTYPE = '1' " + LSIndentNo + " " \
        " ORDER BY INDENTNO,INDENTDATE"

    print("After query 1")
    stmt = con.db.prepare(con.conn, sql)
    print("After query 2")
    con.db.execute(stmt)
    print("After query 3")
    result = con.db.fetch_both(stmt)

    if result==False:
        IRQPS.Exceptions = "Note: No Result found according to your selected criteria"
        return

    while result != False:
        global counter
        counter = counter + 1

        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, '', '')
        pdfrpt.d = pdfrpt.dvalue('', '', result, pdfrpt.divisioncode)
        result = con.db.fetch_both(stmt)
        if pdfrpt.d < 20:
            pdfrpt.d = 720
            pdfrpt.c.showPage()
            pdfrpt.header('', '', pdfrpt.d,result, pdfrpt.divisioncode)

    if result == False:
        if counter > 0:
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dvalue('', '', result, pdfrpt.divisioncode)
            pdfrpt.printtotal(pdfrpt.d)
            pdfrpt.signature(pdfrpt.d)
            IRQPS.Exceptions = ""
        elif counter == 0:
            IRQPS.Exceptions = "Note: No Result found according to your selected criteria "
            return

    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    counter = 0
    pdfrpt.d = pdfrpt.newpage()