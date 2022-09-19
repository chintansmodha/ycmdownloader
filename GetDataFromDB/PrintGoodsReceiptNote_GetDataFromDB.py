import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve

from FormLoad import PrintGoodsReceiptNote_FormLoad as views

from Global_Files import Connection_String as con
from PrintPDF import PrintGoodsReceiptNote_PrintPDF as pdfrpt
save_name=""

Exceptions=""

counter=0


def PrintGoodsReceiptNote_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintGoodsReceiptNote" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Goods Receipt Note/",LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    # stdt = datetime.strptime(views.StartDate, '%Y-%m-%d').date()
    # etdt = datetime.strptime(views.EndDate, '%Y-%m-%d').date()
    startdate = ""
    enddate = ""
    LSGrnno = request.GET.getlist('grnno')
    LSGrndate = request.GET.getlist('grndt')
    LSAmount = request.GET.getlist('amount')
    Company = ''
    Party = ''
    # print("Amount: ", LSAmount)
    # print("GrnNO: " , LSGrnno)
    # print("GrnDate: " , LSGrndate)

    LSGrnNo = " MRNHEADER.CODE in " + "(" + str(LSGrnno)[1:-1] + ")"
    LSGrnDate = " AND VARCHAR_FORMAT(MRNHEADER.MRNDATE, 'DD-MM-YYYY') in  " + "(" + str(LSGrndate)[1:-1] + ")"
    # print(LSGrnDate)
    # print(LSGrndate)

    PrintPDF(LSGrnNo, LSGrnDate, LSAmount, Company, Party, startdate, enddate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PrintGoodsReceiptNote_Table.html', {'GDGoodsSummary':views.GDGoodsSummary,
                                                          'Exception': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response


def PrintPDF(LSGrnNo, LSGrnDate, LSLotNo, Company, Party, startdate, enddate):
    global Exceptions
    sql = "Select          Division.LongDescription As Company , PLANT.ADDRESSLINE1 AS CompAddress " \
          ", FINBUSINESSUNIT.LONGDESCRIPTION As CompName " \
          ", MRNHEADER.CODE AS GRNNumber " \
          ", VARCHAR_FORMAT(MRNHEADER.MRNDATE, 'DD-MM-YYYY') As GRNDate " \
          ", BPTNR.LEGALNAME1 As Supplier " \
          ", COALESCE(ADDRESS.ADDRESSLINE1,'') ||' '|| COALESCE(ADDRESS.ADDRESSLINE2,'') ||' '|| COALESCE(ADDRESS.ADDRESSLINE3,'') " \
          "||' '|| COALESCE(ADDRESS.ADDRESSLINE4,'') ||' '|| COALESCE(ADDRESS.ADDRESSLINE5,'') ||' '|| COALESCE(ADDRESS.POSTALCODE,'') " \
          "||' '|| COALESCE(ADDRESS.TOWN,'') || ' '|| COALESCE(ADDRESS.DISTRICT,'') As Address " \
          ", COALESCE(MRNHEADER.CHALLANNO,'') As ChalNo " \
          ", COALESCE(VARCHAR_FORMAT(MRNHEADER.CHALLANDATE, 'DD-MM-YYYY'),'') As ChalDt " \
          ", COALESCE(MRNHEADER.INVOICENO,'') As BillNo " \
          ", COALESCE(VARCHAR_FORMAT(MRNHEADER.INVOICEDATE, 'DD-MM-YYYY'),'') As BillDt " \
          ", COALESCE(MRNHEADER.LRNO,'') As LrNo " \
          ", COALESCE(VARCHAR_FORMAT(MRNHEADER.LRDATE, 'DD-MM-YYYY'),'') As LrDt " \
          ", PRODUCT.LONGDESCRIPTION As Product " \
          ", COALESCE(UGG.LongDescription,'') As ShadeName " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LongDescription,'') ||' '|| (Case UGG.LongDescription " \
          "When UGG.LongDescription Then COALESCE(QualityLevel.ShortDescription, '') Else '' End) AS ProductName " \
          ", UNITOFMEASURE.SHORTDESCRIPTION As Units " \
          ", PURCHASEORDER.CODE AS PoNo " \
          ", COALESCE(VARCHAR_FORMAT(PURCHASEORDER.ORDERDATE, 'DD-MM-YYYY'),'') As PoDt " \
          ", CAST(MRNDETAIL.PRIMARYQTY AS DECIMAL(10,3)) As Quantity " \
          ", COALESCE(NOTE.NOTE,'') AS Remark " \
          ", COALESCE(MRNDETAIL.TARIFFCODE,'')  As TariffCode " \
          ", COALESCE(StkTxn.LotCode,'') As LotNo " \
          "From      MRNHEADER " \
          "Join      Division                On      MRNHEADER.DIVISIONCODE = DIVISION.CODE " \
          "JOIN      ORDERPARTNER            On      MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE =  ORDERPARTNER.CUSTOMERSUPPLIERCODE " \
          "AND     MRNHEADER.ORDPRNCUSTOMERSUPPLIERType =  ORDERPARTNER.CUSTOMERSUPPLIERTYPE " \
          "JOIN      BUSINESSPARTNER BPTNR   On      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BPTNR.NUMBERID " \
          "Left Join ADDRESS                 On      BPTNR.ABSUNIQUEID = ADDRESS.UNIQUEID " \
          "AND     ADDRESS.ADDRESSTYPE = 1 " \
          "JOIN      PURCHASEORDER           ON      MRNHEADER.PURCHASEORDERCODE = PURCHASEORDER.CODE " \
          "AND     ORDERPARTNER.CUSTOMERSUPPLIERCODE = PURCHASEORDER.ORDPRNCUSTOMERSUPPLIERCODE " \
          "Left Join NOTE                    On      MRNHEADER.ABSUNIQUEID = NOTE.FATHERID " \
          "JOIN      MRNDETAIL               On      MRNHEADER.CODE =  MRNDETAIL.MRNHEADERCODE " \
          "AND     MRNHEADER.MRNPREFIXCODE  =  MRNDETAIL.MRNHEADERMRNPREFIXCODE " \
          "AND     MRNHEADER.PURCHASEORDERCODE  =  MRNDETAIL.PURCHASEORDERCODE " \
          "JOIN     LOGICALWAREHOUSE         ON      LOGICALWAREHOUSE.CODE = MRNDETAIL.LOGICALWAREHOUSECODE " \
          "AND     LOGICALWAREHOUSE.COMPANYCODE = MRNDETAIL.LOGICALWAREHOUSECOMPANYCODE " \
          "JOIN     PLANT                    ON      PLANT.CODE = LOGICALWAREHOUSE.PLANTCODE " \
          "JOIN    BUSINESSUNITVSCOMPANY     ON      PLANT.CODE = BUSINESSUNITVSCOMPANY.FACTORYCODE " \
          "JOIN    FINBUSINESSUNIT           ON      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "JOIN   FULLITEMKEYDECODER FIKD    ON      MRNDETAIL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(MRNDETAIL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(MRNDETAIL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(MRNDETAIL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(MRNDETAIL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(MRNDETAIL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(MRNDETAIL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(MRNDETAIL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(MRNDETAIL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(MRNDETAIL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(MRNDETAIL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join         PRODUCT             On      MRNDETAIL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
          "Join     StockTransaction StkTxn On      MRNDetail.TransactionNumber = StkTxn.TransactionNumber " \
          "Join    QualityLevel             On      StkTxn.QualityLevelCode = QualityLevel.Code " \
          "And     MRNDETAIL.ItemTypeAfiCode = QualityLevel.ItemTypeCode " \
          "Left JOIN    ItemSubcodeTemplate IST     ON      MRNDETAIL.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN UserGenericGroup UGG           ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then MRNDETAIL.SubCode01 When 2 Then MRNDETAIL.SubCode02 When 3 Then MRNDETAIL.SubCode03 When 4 Then MRNDETAIL.SubCode04 When 5 Then MRNDETAIL.SubCode05 " \
          "When 6 Then MRNDETAIL.SubCode06 When 7 Then MRNDETAIL.SubCode07 When 8 Then MRNDETAIL.SubCode08 When 9 Then MRNDETAIL.SubCode09 When 10 Then MRNDETAIL.SubCode10 End = UGG.Code " \
          "Join     UNITOFMEASURE           On      MRNDETAIL.PRIMARYUMCODE = UNITOFMEASURE.CODE " \
          "WHERE    " +LSGrnNo+ " "+LSGrnDate+" " \
          "ORDER BY         COMPANY, GRNNUMBER, GRNDATE  "

    stmt = con.db.prepare(con.conn, sql)
    # Explicitly bind parameters
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, pdfrpt.i)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        # pdfrpt.c.line(0, 12, 600, 12)
        if pdfrpt.d < 30:
            pdfrpt.d = 230
            pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A5))
            pdfrpt.c.showPage()
            pdfrpt.header(result, pdfrpt.divisioncode, pdfrpt.CompanyAddress)
            # pdfrpt.d=pdfrpt.d-20
            # pdfrpt.itemcodes(result, pdfrpt.d)

    if result == False:
        if counter > 0:

            pdfrpt.c.line(0, pdfrpt.d, 600, pdfrpt.d)
            # pdfrpt.d = pdfrpt.dvalue()
            # pdfrpt.Remarks(result, pdfrpt.d)
            str1 = ''
            string = str1.join(pdfrpt.Remark[-1])
            res = sum(not chr.isspace() for chr in string)
            if res != 0:
                pdfrpt.d = pdfrpt.dvalue()
                pdfrpt.d = pdfrpt.dvalue()
                pdfrpt.c.drawString(10, pdfrpt.d, "Remarks: ")
            pdfrpt.c.drawString(45, pdfrpt.d, pdfrpt.Remark[-1])
            pdfrpt.c.drawString(10, 10, "Store")
            pdfrpt.c.drawString(200, 10, "Inspected By")
            pdfrpt.c.drawString(360, 10, "Store Incharge")
            pdfrpt.c.drawString(510, 10, "Authorised By")

            Exceptions = ""
            counter = 0
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria "
            return

    pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A5))
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    # counter = 0
    pdfrpt.d = pdfrpt.newpage()
    pdfrpt.i = pdfrpt.newserialNo()
