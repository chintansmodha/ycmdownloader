import os
from datetime import datetime

from django.shortcuts import render
from django.views.static import serve

from FormLoad import PrintYarnChallan_FormLoad as views
from ProcessSelection import PrintYarnChallan_ProcessSelection as PrintChallan_Views
from PrintPDF import PrintYeanChallanBoxNoWisePDF as printchallanrpt
from PrintPDF import PrintYeanChallanBoxNoWisePDF as pdfrptboxnowise
from Global_Files import Connection_String as con
from PrintPDF import PrintChallanRule55_PrintPDF as pdfrpt
from  ProcessSelection import PrintYarnChallan_ProcessSelection as ps
from django.http import FileResponse
save_name=""

counter=0
def PrintChallanBoxNoWise_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintChallan" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Yarn Challan/",
    #                          LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
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

    LSChallanNo = " AND SALESDOCUMENT.PROVISIONALCODE in " + "(" + str(LSChallanNo)[1:-1] + ")"
    LSChallanDate = " AND VARCHAR_FORMAT(SALESDOCUMENT.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') in  " + "(" + str(LSChallanDate)[
                                                                                                 1:-1] + ")"

    save_name = ''
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintYeanChallan_BoxNo_Wise" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"),
    #                          "D:/Report Development/Generated Reports/Print Yarn Challan Box No Wise/",
    #                          LSFileName)
    # print("file path : " + save_name)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    printchallanrpt.c = printchallanrpt.canvas.Canvas(save_name + ".pdf")
    PrintChallanBoxNoWise(LSChallanNo,request)
    filepath =save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PrintChallan_Boxes_No_Wise_Table.html',
                      {'GDataPrintChallan': ps.GDataPrintChallan})

    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response

def PrintChallanBoxNoWise(LSChallanNo,request):
    # Company = str(LSCompany)
    # Company = '(' + Company[1:-1] + ')'
    # Party = str(LSParty)
    # Party = '(' + Party[1:-1] + ')'
    # StartDate = "'" + LDStartDate + "'"
    # EndDate = "'" + LDEndDate + "'"
    # counter=0
    # if not LSCompany:
    #     Company = " "
    # elif LSCompany:
    #     Company = " And BUnit.Code in " + Company
    # if not LSParty:
    #     Party = " "
    # elif LSParty:
    #     Party = " And BP.NumberId in " + Party
    sql = "SELECT  COMPANY.LONGDESCRIPTION AS  companyname    " \
          "        , SALESDOCUMENT.PROVISIONALCODE AS CHALLANNUMBER " \
          "        , COALESCE(VARCHAR_FORMAT(SALESDOCUMENT.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY'),'') AS CHALLANDATE " \
          "        , SALESDOCUMENT.SALESORDERCODE AS REFERANCECODE " \
          "        , trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS PRODUCT " \
          "        , cast(SALESDOCUMENTLINE.USERPRIMARYQUANTITY as decimal(18,2)) AS QUANTITY " \
          "        , TRIM (UGG.Code)  ||' / '||UGG.LONGDESCRIPTION As ShadeCode  " \
          "        , BusinessPartner.LEGALNAME1  AS CUSTOMER " \
          "        , Coalesce(BusinessPartner.ADDRESSLINE1,'') " \
          "           || Coalesce(','||BusinessPartner.ADDRESSLINE2,'') " \
          "           || Coalesce(','||BusinessPartner.ADDRESSLINE3,'') " \
          "           || Coalesce(','||BusinessPartner.ADDRESSLINE4,'') " \
          "           || Coalesce(','||BusinessPartner.ADDRESSLINE5,'') " \
          "           ||', Postal Code : '||Coalesce(BusinessPartner.POSTALCODE,'')as CustomerAddress " \
          "        , ADDRESS_Consignee.Addressee AS CONSIGNEE " \
          "        , Coalesce(ADDRESS_Consignee.ADDRESSLINE1,'') " \
          "           || Coalesce(','||ADDRESS_Consignee.ADDRESSLINE2,'') " \
          "           || Coalesce(','||ADDRESS_Consignee.ADDRESSLINE3,'') " \
          "           || Coalesce(','||ADDRESS_Consignee.ADDRESSLINE4,'') " \
          "           ||','|| Coalesce(ADDRESS_Consignee.ADDRESSLINE5,'')" \
          "           ||', Postal Code : '||Coalesce(ADDRESS_Consignee.POSTALCODE,'') as CONSIGNEEADDRESS" \
          "        , COALESCE(VARCHAR_FORMAT(SAlESDOCUMENTLINE.EXTERNALREFERENCEDATE, 'DD-MM-YYYY'),'') AS LRDATE " \
          "        , COALESCE(SAlESDOCUMENTLINE.EXTERNALREFERENCE,'') AS LRNO " \
          "        , Boxes.NoOfSpools As COPS " \
          "        , Boxes.ACTUALUNITCODE as WeightUnit " \
          "        , BOXES.ACTUALGROSSWT AS GROSSWT " \
          "        , BOXES.ACTUALTAREWT AS TAREWT " \
          "        , BOXES.ACTUALNETWT AS NETWT " \
          "        , Boxes.TwistCode as Twist " \
          "        , ST.LOTCODE As LotNo " \
          "        , ST.ContainerElementCode As BoxNo " \
          "        , Plant.Town As DespFrom " \
          "        , ADDRESS_Consignee.Town As DespTo" \
          "        , COALESCE(ADDRESS_Consignee.ADDRESSEE,'') As CONSIGNEE " \
          "        , Plant.AddressLine1 AS PlantAddress " \
          "        , COALESCE(PILine.SalesDocumentProvisionalCode ,'') As PlantInvoiceNo  " \
          "        , COALESCE(VARCHAR_FORMAT(PI.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY'),'') As PlantInvoiceDate " \
          "         , count(*) over(partition by SALESDOCUMENT.PROVISIONALCODE)  as totalnoofchallan " \
          " FROM SALESDOCUMENT " \
          " join OrderPartner               On      SALESDOCUMENT.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode " \
          "                                And     OrderPartner.CustomerSupplierType = 1 " \
          " join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
          " left JOIN Agent                      ON SALESDOCUMENT.Agent1Code                       = Agent.Code  " \
          " JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE = SALESDOCUMENT.PROVISIONALCODE " \
          "                                AND SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
          " JOIN LOGICALWAREHOUSE           ON SALESDOCUMENTLINE.WAREHOUSECODE                = LOGICALWAREHOUSE.CODE " \
          " JOIN BusinessUnitVsCompany BUC  ON SalesDocument.DivisionCode   					= BUC.DivisionCode " \
          "                                AND LOGICALWAREHOUSE.plantcode  					= BUC.factorycode " \
          " JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode 						= BUnit.Code And BUnit.GroupFlag = 0 " \
          " JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode 						= Company.Code And Company.GroupFlag = 1 " \
          " JOIN ITEMTYPE                   ON SALESDOCUMENTLINE.ITEMTYPEAFICODE              = ITEMTYPE.CODE " \
          " JOIN QUALITYLEVEL               ON SALESDOCUMENTLINE.QUALITYCODE                  = QUALITYLEVEL.CODE " \
          "                                AND SALESDOCUMENTLINE.ITEMTYPEAFICODE              = QUALITYLEVEL.ITEMTYPECODE " \
          " JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE 		= IST.ItemTypeCode " \
          "                                AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
          " JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "                                        AND     Case IST.Position  " \
          " When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03  " \
          " When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06  " \
          " When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09  " \
          " When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code " \
          " JOIN         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          " Join Product                    On      SALESDOCUMENTLINE.ITEMTYPEAFICODE = Product.ITEMTYPECODE  " \
          "                                And     FIKD.ItemUniqueId = Product.AbsUniqueId  " \
          " LEFT JOIN ADDRESS  ADDRESS_Consignee             ON      BusinessPartner.ABSUNIQUEID = ADDRESS_Consignee.UNIQUEID  " \
          "                                AND     SALESDOCUMENT.DELIVERYPOINTCODE = ADDRESS_Consignee.CODE  " \
          " JOIN PLANT                      ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE  " \
          " Join    StockTransaction St     On      SALESDOCUMENT.ProvisionalCode   = ST.OrderCode " \
          "                                And     ST.TemplateCode = 'S04' " \
          " Join    BKLElements Boxes       On      ST.ContainerElementCode = Boxes.Code " \
          " Left Join SalesDocumentLine PILine      On      PILine.DocumentTypeType = '06' " \
          "                                And     PILine.PreviousCode = SALESDOCUMENT.ProvisionalCode " \
          "                                And     PILine.PreviousDocumentTypeType = '05' " \
          " Left Join SalesDocument PI      On     PILine.SalesDocumentProvisionalCode = PI.ProvisionalCode " \
          "                                And     PILine.DocumentTypeType = PI.DocumentTypeType " \
          "                                And     PILine.SaldocPROVISIONALCOUNTERCODE = PI.PROVISIONALCOUNTERCODE " \
          "                                " \
          " WHERE SALESDOCUMENT.DocumentTypeType = '05'   " \
          "  "+LSChallanNo+"  " \
          " ORDER  BY Company.longdescription, " \
          "          SALESDOCUMENT.PROVISIONALCODE, " \
          "          SALESDOCUMENT.PROVISIONALDOCUMENTDATE  " \
          "          ,ShadeCode,Lotno,BoxNo"
    print(LSChallanNo)
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    if result != False:
        pdfrptboxnowise.newrequest()

        while result != False:
            global counter
            counter = counter + 1
            # pdfrptboxnowise.textsize(pdfrptboxnowise.c, result, pdfrptboxnowise.d,pdfrptboxnowise.x)
            pdfrptboxnowise.textsize(pdfrptboxnowise.c, result)

            pdfrptboxnowise.d = pdfrptboxnowise.dvalue()
            result = con.db.fetch_both(stmt)

        pdfrptboxnowise.printlasttotal(pdfrptboxnowise.d)
        pdfrptboxnowise.printtotalmain()
        pdfrptboxnowise.d = 530

        pdfrptboxnowise.d = pdfrptboxnowise.d - 20
        pdfrptboxnowise.c.showPage()
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
            pdfrptboxnowise.c.showPage()
            pdfrptboxnowise.c.save()
            # url = "file:///D:/New format Report/Generated Reports/Print yan challan/" + LSFileName + ".pdf"
            # os.startfile(url)
            pdfrptboxnowise.newrequest()
            pdfrptboxnowise.d = pdfrpt.newpage()
    else:
        Exceptions = "Note: Please Select Valid Credentials"
        return