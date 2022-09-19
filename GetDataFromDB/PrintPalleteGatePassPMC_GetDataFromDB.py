import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
from Global_Files import Connection_String as con
from PrintPDF import PrintPalleteGatePassPMC_PrintPDF as pdfrpt
from ProcessSelection import PrintPalleteGatePass_ProcessSelection as PPGPPS
save_name=""
counter=0
def PrintPalleteGatePassPDFPMC(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "PrintPalleteGatePassPMC" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),
                             "D:/Report Development/Generated Reports/Print Pallete Gate Pass PMC/", LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    LSGatePassNo = request.GET.getlist('gatepassno')
    LSGatePassDate = request.GET.getlist('gatepassdt')
    LSGatePassNo = " AND ID.PROVISIONALCODE in " + "(" + str(LSGatePassNo)[1:-1] + ")"
    LSGatePassDate = " AND ID.PROVISIONALDOCUMENTDATE in  " + "(" + str(LSGatePassDate)[1:-1] + ")"

    PrintPDF(LSGatePassNo, LSGatePassDate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PrintPalleteGatePassTable_PMC.html',
                      {'GDataPrintPalleteGatePass': PPGPPS.GDataPrintPalleteGatePass,'Exception': PPGPPS.Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

def  PrintPDF(LSGatePassNo, LSGatePassDate):
    sql="SELECT  BUNIT.LongDescription AS COMPANYNAME" \
        " ,PLANT.ADDRESSLINE1 AS COMPANYADDRESS" \
        " ,ID.PROVISIONALCODE AS GATEPASSNO" \
        " ,VARCHAR_FORMAT(ID.PROVISIONALDOCUMENTDATE,'DD-MM-YYYY') AS GATEPASSDATE" \
        " ,IOT.LONGDESCRIPTION As TemplateName" \
        " ,BP.LEGALNAME1 as SUPPLIER" \
        " ,COALESCE(BP.ADDRESSLINE1,'') AS SUP_ADDR1" \
        " ,COALESCE(BP.ADDRESSLINE2,'') AS SUP_ADDR2" \
        " ,COALESCE(BP.ADDRESSLINE3,'') AS SUP_ADDR3" \
        " ,COALESCE(BP.ADDRESSLINE4,'') AS SUP_ADDR4" \
        " ,COALESCE(BP.ADDRESSLINE5,'') AS SUP_ADDR5" \
        " ,COALESCE(BP.POSTALCODE,'') AS SUP_POSTALCODE" \
        " ,ID.NUMBERPLATE AS VEHICLENO" \
        " ,ID.EXTERNALREFERENCE AS LRNO" \
        " ,TRIM (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS PRODUCT" \
        " ,CAST(IDL.USERPRIMARYQUANTITY as decimal(18,3)) AS QUANTITY" \
        " ,PRODUCTIE.TARIFFCODE AS HSNCODE" \
        " ,NOTE.NOTE AS REMARKS" \
        " FROM INTERNALDOCUMENT AS ID" \
        " JOIN InternalDocumentLine As IDL        ON      ID.PROVISIONALCODE = IDL.INTDOCUMENTPROVISIONALCODE" \
        " AND     ID.PROVISIONALCOUNTERCODE = IDL.INTDOCPROVISIONALCOUNTERCODE" \
        " JOIN LOGICALWAREHOUSE AS LWH            ON      IDL.WAREHOUSECODE = LWH.CODE" \
        " JOIN BUSINESSUNITVSCOMPANY AS BUC       ON      ID.DIVISIONCODE = BUC.DIVISIONCODE" \
        " AND     LWH.PLANTCODE = BUC.FACTORYCODE" \
        " JOIN FINBUSINESSUNIT AS BUnit           ON      BUC.BusinessUnitcode = BUnit.Code" \
        " AND     BUnit.GroupFlag = 0" \
        " JOIN PLANT                              ON      LWH.plantcode = PLANT.CODE" \
        " JOIN INTERNALORDERTEMPLATE AS IOT       ON      ID.TemplateCode = IOT.Code" \
        " JOIN ORDERPARTNER AS OP                 ON      ID.ORDPRNCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode" \
        " AND     IOT.DESTINATIONTYPE     = OP.CustomerSupplierType" \
        " JOIN BUSINESSPARTNER AS BP              ON      OP.OrderBusinessPartnerNumberId = BP.NumberId" \
        " JOIN FullItemKeyDecoder FIKD            ON      IDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE" \
        " AND     COALESCE(IDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
        " AND     COALESCE(IDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
        " AND     COALESCE(IDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
        " AND     COALESCE(IDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
        " AND     COALESCE(IDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
        " AND     COALESCE(IDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
        " AND     COALESCE(IDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
        " AND     COALESCE(IDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
        " AND     COALESCE(IDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
        " AND     COALESCE(IDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
        " JOIN PRODUCT                            ON      IDL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE" \
        " AND     FIKD.ItemUniqueId = PRODUCT.AbsUniqueId" \
        " JOIN PRODUCTIE                          ON      PRODUCT.ITEMTYPECODE = PRODUCTIE.ITEMTYPECODE" \
        " AND     COALESCE(PRODUCT.SubCode01, '') = COALESCE(PRODUCTIE.SubCode01, '')" \
        " AND     COALESCE(PRODUCT.SubCode02, '') = COALESCE(PRODUCTIE.SubCode02, '')" \
        " AND     COALESCE(PRODUCT.SubCode03, '') = COALESCE(PRODUCTIE.SubCode03, '')" \
        " AND     COALESCE(PRODUCT.SubCode04, '') = COALESCE(PRODUCTIE.SubCode04, '')" \
        " AND     COALESCE(PRODUCT.SubCode05, '') = COALESCE(PRODUCTIE.SubCode05, '')" \
        " AND     COALESCE(PRODUCT.SubCode06, '') = COALESCE(PRODUCTIE.SubCode06, '')" \
        " AND     COALESCE(PRODUCT.SubCode07, '') = COALESCE(PRODUCTIE.SubCode07, '')" \
        " AND     COALESCE(PRODUCT.SubCode08, '') = COALESCE(PRODUCTIE.SubCode08, '')" \
        " AND     COALESCE(PRODUCT.SubCode09, '') = COALESCE(PRODUCTIE.SubCode09, '')" \
        " AND     COALESCE(PRODUCT.SubCode10, '') = COALESCE(PRODUCTIE.SubCode10, '')" \
        " JOIN QUALITYLEVEL                       ON      IDL.QUALITYCODE = QUALITYLEVEL.CODE" \
        " AND     IDL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE" \
        " LEFT JOIN NOTE                          ON      ID.ABSUNIQUEID = NOTE.FATHERID" \
        " WHERE ID.DocumentTypeType = '05'  AND ID.TEMPLATECODE='PMC'" +LSGatePassNo+"" \
        " ORDER BY COMPANYNAME,GATEPASSDATE,GATEPASSNO"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)

    if result == False:
        PPGPPS.Exceptions = "Note: No Result found according to your selected criteria"
        return

    while result != False:
        global counter
        counter = counter + 1

        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, '', '')
        pdfrpt.d = pdfrpt.dvalue('', '', result, pdfrpt.divisioncode)
        result = con.db.fetch_both(stmt)
        if pdfrpt.d < 20:
            pdfrpt.d = 620
            pdfrpt.c.showPage()
            pdfrpt.header('', '', pdfrpt.d, result, pdfrpt.divisioncode)

    if result == False:
        if counter > 0:
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dvalue('', '', result, pdfrpt.divisioncode)
            pdfrpt.printtotal(pdfrpt.d)
            pdfrpt.signature(pdfrpt.d - 20, -1)
            PPGPPS.Exceptions = ""
        elif counter == 0:
            PPGPPS.Exceptions = "Note: No Result found according to your selected criteria "
            return

    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    counter = 0
    pdfrpt.d = pdfrpt.newpage()
