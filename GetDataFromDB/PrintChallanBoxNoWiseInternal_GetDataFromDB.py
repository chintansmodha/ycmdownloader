import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
from Global_Files import Connection_String as con
from FormLoad import PrintYarnChallan_FormLoad as views
from ProcessSelection import PrintYarnChallan_ProcessSelection as PrintChallan_Views
from PrintPDF import PrintChallanBoxNoWiseInternal_PrintPDF as pdfrpt
save_name=""
counter=0
def PrintChallanBoxNoWiseInternalPDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "DespatchReport" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Challan Box No Wise Internal/",
                             LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSChallanNo = request.GET.getlist('challanno')
    LSChallanDate = request.GET.getlist('challandt')
    LSLotNo = request.GET.getlist('lotno')
    LSLrNo = request.GET.getlist('lrno')
    LSLrDt = request.GET.getlist('lrdt')
    LSQuantity = request.GET.getlist('qty')
    LSBoxes = request.GET.getlist('box')
    Company = ''
    Party = ''

    LSChallanNo = " AND ID.PROVISIONALCODE in " + "(" + str(LSChallanNo)[1:-1] + ")"
    LSChallanDate = " AND VARCHAR_FORMAT(ID.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') in  " + "(" + str(LSChallanDate)[1:-1] + ")"

    PrintPDF(LSChallanNo, LSChallanDate, LSLotNo, LSLrNo, LSLrDt, LSQuantity, LSBoxes, Company, Party)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PrintChallanBoxNoWiseInternalTable.html', {'GDataPrintChallan': PrintChallan_Views.GDataPrintChallan,
                                                            'Exception': PrintChallan_Views.Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

def PrintPDF(LSChallanNo, LSChallanDate, LSLotNo, LSLrNo, LSLrDt, LSQuantity, LSBoxes, Company, Party):
    sql="Select   Plant.LONGDESCRIPTION As PLANTNAME" \
        " ,ID.PROVISIONALCODE AS CHALLANNUMBER" \
        " ,COALESCE(VARCHAR_FORMAT(ID.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY'),'') AS CHALLANDATE" \
        " ,ID.INTERNALORDERCODE As REFERANCECODE" \
        " ,Plant.Town As DespFrom" \
        " ,'' As DespTo" \
        " ,Plant.AddressLine1 AS PlantAddress" \
        " ,ID.EXTERNALREFERENCE As LRNO" \
        " ,ID.EXTERNALREFERENCEDATE As LRDATE" \
        " ,TRIM (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS PRODUCT" \
        " ,TRIM (UGG.Code)  ||' / '||UGG.LONGDESCRIPTION As ShadeCode" \
        " ,ToDept.LongDescription As ToDept" \
        " ,BE.NoOfSpools As COPS" \
        " ,BE.ACTUALUNITCODE as WeightUnit" \
        " ,BE.ACTUALGROSSWT AS GROSSWT" \
        " ,BE.ACTUALTAREWT AS TAREWT" \
        " ,BE.ACTUALNETWT AS NETWT" \
        " ,BE.TwistCode as Twist" \
        " ,ST.LOTCODE As LotNo" \
        " ,ST.ContainerElementCode As BoxNo" \
        " ,COUNT(*) over(partition by ID.PROVISIONALCODE)  as NoOfBoxes" \
        " FROM InternalDocument As ID" \
        " JOIN OrderPartner As OP                 ON      ID.ORDPRNCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode" \
        " AND     OP.CustomerSupplierType = 3" \
        " JOIN LOGICALWAREHOUSE ToDept            ON      OP.ORDERLOGICALWAREHOUSECODE = ToDept.CODE" \
        " JOIN InternalDocumentLine As IDL        ON      ID.PROVISIONALCODE = IDL.INTDOCUMENTPROVISIONALCODE" \
        " AND     ID.PROVISIONALCOUNTERCODE = IDL.INTDOCPROVISIONALCOUNTERCODE" \
        " JOIN LOGICALWAREHOUSE                   ON      IDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
        " JOIN PLANT                              ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE" \
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
        " JOIN Product                            ON      IDL.ITEMTYPEAFICODE = Product.ITEMTYPECODE" \
        " AND     FIKD.ItemUniqueId = Product.AbsUniqueId" \
        " JOIN QUALITYLEVEL                       ON      IDL.QUALITYCODE = QUALITYLEVEL.CODE" \
        " AND     IDL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE" \
        " JOIN ItemSubcodeTemplate As IST         ON      IDL.ITEMTYPEAFICODE = IST.ItemTypeCode" \
        " AND     IST.GroupTypeCode In ('MB4','P09','B07')" \
        " JOIN UserGenericGroup As UGG            ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
        " AND     Case IST.Position" \
        " When 1 Then IDL.SubCode01 When 2 Then IDL.SubCode02 When 3 Then IDL.SubCode03" \
        " When 4 Then IDL.SubCode04 When 5 Then IDL.SubCode05 When 6 Then IDL.SubCode06" \
        " When 7 Then IDL.SubCode07 When 8 Then IDL.SubCode08 When 9 Then IDL.SubCode09" \
        " When 10 Then IDL.SubCode10 End = UGG.Code" \
        " JOIN StockTransaction ST        ON      IDL.IntDocProvisionalCounterCode = ST.OrderCounterCode" \
        " AND     IDL.IntDocumentProvisionalCode = ST.OrderCode" \
        " AND     IDL.OrderLine = ST.OrderLine" \
        " AND     IDL.OrderSubLine = ST.OrderSubLine" \
        " AND     ST.ContainerElementCode IS NOT NULL" \
        " JOIN BKLELEMENTS BE             ON      ST.ContainerItemTypeCode = BE.ItemTypeCode" \
        " AND     ST.ContainerSubCode01 = BE.SubCodeKey" \
        " AND     ST.ContainerElementCode = BE.Code" \
        " WHERE ID.DocumentTypeType = '05'  AND ID.PROVISIONALCOUNTERCODE='I04' AND ID.TEMPLATECODE='I04'"+LSChallanNo+"" \
        " ORDER BY PlantName, ID.PROVISIONALDOCUMENTDATE, ID.PROVISIONALCODE, LotNo, BoxNo"

    stmt = con.db.prepare(con.conn, sql)
    # stdt = datetime.strptime(views.LDStartDate, '%Y-%m-%d').date()
    # etdt = datetime.strptime(views.LDEndDate, '%Y-%m-%d').date()
    # Explicitly bind parameters
    # con.db.bind_param(stmt, 1, stdt)
    # con.db.bind_param(stmt, 2, etdt)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    if result==False:
        PrintChallan_Views.Exceptions = "Note: No Result found according to your selected criteria "
        return
    if result != False:
        pdfrpt.newrequest()

        while result != False:
            global counter
            counter = counter + 1
            # pdfrptboxnowise.textsize(pdfrptboxnowise.c, result, pdfrptboxnowise.d,pdfrptboxnowise.x)
            pdfrpt.textsize(pdfrpt.c, result)

            pdfrpt.d = pdfrpt.dvalue()
            result = con.db.fetch_both(stmt)

        pdfrpt.printlasttotal(pdfrpt.d)
        pdfrpt.printtotalmain()
        pdfrpt.d = 530

        pdfrpt.d = pdfrpt.d - 20
        pdfrpt.c.showPage()
        # pdfrptpyboxwise.print("after calling register")

        if counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria "
            print("counter = 0")
        else:
            # pdfrptboxnowise.c.showPage()
            # pdfrptboxnowise.c.setPageSize(landscape(A5))
            # pdfrptboxnowise.c.save()
            # pdfrptboxnowise.newrequest()
            # pdfrptboxnowise.d = pdfrpt.newpage()
            # print("from  else befoer over")
            pdfrpt.c.showPage()
            pdfrpt.c.save()
            # url = "file:///D:/New format Report/Generated Reports/Print yan challan/" + LSFileName + ".pdf"
            # os.startfile(url)
            pdfrpt.newrequest()
            pdfrpt.d = pdfrpt.newpage()
    else:
        Exceptions = "Note: Please Select Valid Credentials"
        return

    # pdfrpt.c.showPage()
    # pdfrpt.c.save()
    # pdfrpt.newrequest()
    # counter = 0
    # pdfrpt.d = pdfrpt.newpage()
