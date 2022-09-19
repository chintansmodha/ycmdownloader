import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
from FormLoad import PrintYarnChallan_FormLoad as views
from ProcessSelection import PrintYarnChallan_ProcessSelection as PrintChallan_Views
from Global_Files import Connection_String as con
from PrintPDF import DespatchReport_PrintPDF as pdfrpt
save_name=""

counter=0

def DespatchReportPDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "DespatchReport" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Despatch Report/", LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSChallanNo = request.GET.getlist('challanno')
    LSChallanDate = request.GET.getlist('challandt')
    LSLotNo = request.GET.getlist('lotno')
    LSLrNo = request.GET.getlist('lrno')
    LSLrDt = request.GET.getlist('lrdt')
    LSQuantity = request.GET.getlist('qty')
    LSBoxes = request.GET.getlist('box')
    Company=''
    Party=''

    LSChallanNo = " AND SD.PROVISIONALCODE in "+"("+str(LSChallanNo)[1:-1]+")"
    LSChallanDate = " AND VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') in  "+"("+str(LSChallanDate)[1:-1]+")"

    PrintPDF(LSChallanNo,LSChallanDate,LSLotNo,LSLrNo,LSLrDt,LSQuantity,LSBoxes,Company,Party)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'DespatchReportTable.html',{'GDataPrintChallan': PrintChallan_Views.GDataPrintChallan,'Exception':PrintChallan_Views.Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

def PrintPDF(LSChallanNo,LSChallanDate,LSLotNo,LSLrNo,LSLrDt,LSQuantity,LSBoxes,Company,Party):
    sql = " SELECT    BUnit.LONGDESCRIPTION AS COMPANYNAME" \
          " , COSTCENTER.LONGDESCRIPTION As COSTCENTERNAME " \
          " , SDL.EXTERNALREFERENCE AS LRNO" \
          " , TZ_DespTo.LONGDESCRIPTION AS Despatch" \
          " , trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS PRODUCT" \
          " , SD.NUMBERPLATE AS VEHICLENO" \
          " , SD.PROVISIONALCODE AS CHALLANNUMBER" \
          " , BP.LEGALNAME1  AS CUSTOMER" \
          " , ST.ContainerElementCode As CONTAINERELEMENTNO" \
          " , BOXES.ACTUALGROSSWT AS GROSSWT" \
          " , BOXES.ACTUALTAREWT AS TAREWT" \
          " , BOXES.ACTUALNETWT AS NETWT" \
          " , Boxes.NoOfSpools As COPS" \
          " , ST.LOTCODE As LOTNO" \
          " , TRIM (UGG.Code)  ||' / '||UGG.LONGDESCRIPTION As SHADECODE" \
          " , Boxes.TwistCode as TWISTCODE" \
          " , TRIM(BOXES.WINDINGTYPECODE)  ||''||  BOXES.PACKSIZECODE As WindcodeAndPacksize" \
          " , count(*) BOXESCOUNT" \
          " FROM SALESDOCUMENT AS SD" \
          " JOIN SALESDOCUMENTLINE  AS SDL          ON      SDL.SALESDOCUMENTPROVISIONALCODE = SD.PROVISIONALCODE" \
          " AND     SDL.SALDOCPROVISIONALCOUNTERCODE = SD.PROVISIONALCOUNTERCODE" \
          " JOIN LOGICALWAREHOUSE                   ON      SDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
          " JOIN BusinessUnitVsCompany AS BUC       ON      SD.DivisionCode = BUC.DivisionCode" \
          " AND     LOGICALWAREHOUSE.plantcode = BUC.factorycode" \
          " JOIN FinBusinessUnit AS BUnit           ON      BUC.BusinessUnitcode = BUnit.Code" \
          " AND     BUnit.GroupFlag = 0" \
          " JOIN FinBusinessUnit As Company         ON      Bunit.GroupBUCode = Company.Code" \
          " AND     Company.GroupFlag = 1" \
          " LEFT JOIN COSTCENTER 			ON 	SDL.COSTCENTERCODE = COSTCENTER.CODE" \
          " JOIN OrderPartner AS OP                 ON      SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode" \
          " AND     OP.CustomerSupplierType = 1" \
          " JOIN BusinessPartner AS BP              ON      OP.OrderbusinessPartnerNumberId = BP.NumberID" \
          " JOIN FullItemKeyDecoder AS FIKD         ON      SDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(SDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(SDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(SDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(SDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
          " AND     COALESCE(SDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
          " AND     COALESCE(SDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
          " AND     COALESCE(SDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
          " AND     COALESCE(SDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
          " AND     COALESCE(SDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
          " AND     COALESCE(SDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
          " JOIN Product                            ON      SDL.ITEMTYPEAFICODE = Product.ITEMTYPECODE" \
          " AND     FIKD.ItemUniqueId = Product.AbsUniqueId" \
          " JOIN QUALITYLEVEL                       ON      SDL.QUALITYCODE = QUALITYLEVEL.CODE" \
          " AND     SDL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE" \
          " JOIN ItemSubcodeTemplate AS IST         ON      SDL.ITEMTYPEAFICODE = IST.ItemTypeCode" \
          " AND     IST.GroupTypeCode In ('MB4','P09','B07')" \
          " JOIN UserGenericGroup AS UGG            ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
          " AND     Case IST.Position" \
          " When 1 Then SDL.SubCode01 When 2 Then SDL.SubCode02 When 3 Then SDL.SubCode03" \
          " When 4 Then SDL.SubCode04 When 5 Then SDL.SubCode05 When 6 Then SDL.SubCode06" \
          " When 7 Then SDL.SubCode07 When 8 Then SDL.SubCode08 When 9 Then SDL.SubCode09" \
          " When 10 Then SDL.SubCode10 End = UGG.Code" \
          " LEFT JOIN Address AS  ADDRESS_Consignee ON      BP.ABSUNIQUEID = ADDRESS_Consignee.UNIQUEID" \
          " AND     SD.DELIVERYPOINTCODE = ADDRESS_Consignee.CODE" \
          " JOIN StockTransaction AS ST             ON      SD.ProvisionalCode = ST.OrderCode" \
          " AND     ST.TemplateCode = 'S04'" \
          " JOIN BKLElements AS Boxes               ON      ST.ContainerElementCode = Boxes.Code" \
          " AND     Boxes.ItemTypeCode = 'CNT'" \
          " LEFT JOIN Transportzone AS TZ_DespTo    ON      ADDRESS_Consignee.TRANSPORTZONECODE = TZ_DespTo.code" \
          " Where SD.DOCUMENTTYPETYPE='05' "+LSChallanNo+"" \
          " Group By BUnit.LONGDESCRIPTION " \
          " , COSTCENTER.LONGDESCRIPTION " \
          " , SDL.EXTERNALREFERENCE " \
          " , TZ_DespTo.LONGDESCRIPTION " \
          " , trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) " \
          " , SD.NUMBERPLATE " \
          " , SD.PROVISIONALCODE " \
          " , BP.LEGALNAME1 " \
          " , ST.ContainerElementCode " \
          " , BOXES.ACTUALGROSSWT " \
          " , BOXES.ACTUALTAREWT " \
          " , BOXES.ACTUALNETWT " \
          " , Boxes.NoOfSpools " \
          " , ST.LOTCODE " \
          " , TRIM (UGG.Code)  ||' / '||UGG.LONGDESCRIPTION " \
          " , Boxes.TwistCode " \
          " , TRIM(BOXES.WINDINGTYPECODE)  ||''||  BOXES.PACKSIZECODE " \
          " Order by COMPANYNAME,CHALLANNUMBER"


    stmt = con.db.prepare(con.conn, sql)
    # stdt = datetime.strptime(views.LDStartDate, '%Y-%m-%d').date()
    # etdt = datetime.strptime(views.LDEndDate, '%Y-%m-%d').date()
    # Explicitly bind parameters
    # con.db.bind_param(stmt, 1, stdt)
    # con.db.bind_param(stmt, 2, etdt)
    # Explicitly bind parameters
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print("sanika")
    if result != False:
        while result != False:
            global counter
            counter = counter + 1
            pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, '', '')
            pdfrpt.d = pdfrpt.dvalue('', '',result,pdfrpt.divisioncode)
            result = con.db.fetch_both(stmt)

            # pdfrpt.c.line(0, 12, 600, 12)
            if pdfrpt.d < 20:
                pdfrpt.d = 680
                pdfrpt.c.showPage()
                pdfrpt.header('', '',result, pdfrpt.divisioncode)
                # pdfrpt.d=pdfrpt.d-10
        if result == False:
            if counter > 0:
                pdfrpt.d = pdfrpt.dvalue('', '', result, pdfrpt.divisioncode)
                pdfrpt.printtotal(pdfrpt.d)
                pdfrpt.companyclean()
                PrintChallan_Views.Exceptions = ""
            elif counter == 0:
                PrintChallan_Views.Exceptions = "Note: No Result found according to your selected criteria "

    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    counter = 0
    pdfrpt.d = pdfrpt.newpage()
