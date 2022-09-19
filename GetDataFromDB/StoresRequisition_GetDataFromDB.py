import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
from Global_Files import Connection_String as con
from PrintPDF import StoresRequisition_PrintPDF as pdfrpt
from ProcessSelection import StoresRequisition_ProcessSelection as SRQPS
save_name=""
counter=0
def StoresRequisitionPDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "StoresRequisition" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),
                             "D:/Report Development/Generated Reports/Stores Requisition/", LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSRequisitionNo = request.GET.getlist('requisitionno')
    LSRequisitionDate = request.GET.getlist('requisitiondt')
    LSRequisitionNo = " AND ID.PROVISIONALCODE in " + "(" + str(LSRequisitionNo)[1:-1] + ")"
    LSRequisitionDate = " AND ID.PROVISIONALDOCUMENTDATE in  " + "(" + str(LSRequisitionDate)[1:-1] + ")"

    PrintPDF(LSRequisitionNo,LSRequisitionDate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'StoresRequisitionTable.html',{'GDataStoresRequisition': SRQPS.GDataStoresRequisition,
                       'Exception': SRQPS.Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

def PrintPDF(LSRequisitionNo,LSRequisitionDate):
    sql="SELECT COSTCENTER.LONGDESCRIPTION AS DEPARTMENTNAME" \
        " ,ID.PROVISIONALCODE AS REQUISITIONNO" \
        " ,VARCHAR_FORMAT(ID.PROVISIONALDOCUMENTDATE,'DD-MM-YYYY') AS REQUISITIONDATE" \
        " ,IDL.ITEMDESCRIPTION AS ITEM" \
        " ,IDL.USERPRIMARYUOMCODE AS UNIT" \
        " ,IDL.USERPRIMARYQUANTITY AS QUANTITY" \
        " FROM INTERNALDOCUMENT AS ID" \
        " JOIN InternalDocumentLine AS IDL        ON      ID.PROVISIONALCODE = IDL.INTDOCUMENTPROVISIONALCODE" \
        " AND     ID.PROVISIONALCOUNTERCODE = IDL.INTDOCPROVISIONALCOUNTERCODE" \
        " JOIN ORDERPARTNER AS OP                 ON      ID.ORDPRNCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode" \
        " AND     OP.CustomerSupplierType = 3" \
        " JOIN LOGICALWAREHOUSE                   ON      OP.ORDERLOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
        " JOIN COSTCENTER                         ON      LogicalWarehouse.COSTCENTERCODE = CostCenter.Code" \
        " WHERE ID.PROVISIONALCOUNTERCODE='I04' AND ID.DOCUMENTTYPETYPE='05'" + LSRequisitionNo +" "\
        " ORDER BY DEPARTMENTNAME,REQUISITIONNO,REQUISITIONDATE "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    print(sql)

    if result==False:
        SRQPS.Exceptions = "Note: No Result found according to your selected criteria"
        return

    while result != False:
        global counter
        counter = counter + 1

        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, '', '')
        pdfrpt.d = pdfrpt.dvalue('', '', result, pdfrpt.divisioncode)
        result = con.db.fetch_both(stmt)
        if pdfrpt.d < 20:
            pdfrpt.d = 730
            pdfrpt.c.showPage()
            pdfrpt.header('', '', pdfrpt.d,result, pdfrpt.divisioncode)

    if result == False:
        if counter > 0:
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dvalue('', '', result, pdfrpt.divisioncode)
            pdfrpt.printtotal(pdfrpt.d)
            pdfrpt.signature(pdfrpt.d)
            SRQPS.Exceptions = ""
        elif counter == 0:
            SRQPS.Exceptions = "Note: No Result found according to your selected criteria "
            return

    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    counter = 0
    pdfrpt.d = pdfrpt.newpage()