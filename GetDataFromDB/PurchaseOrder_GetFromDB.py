import os
from datetime import datetime

from django.shortcuts import render
from django.views.static import serve

from FormLoad import PurchaseOrder_FormLoad as views

from Global_Files import Connection_String as con
from PrintPDF import PurchaseOrder_PrintPDF as pdfrpt
save_name=""

Exceptions=""

counter=0


def PurchaseOrder_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PurchaseOrder" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Purchase Order/",
                             LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    startdate = ""
    enddate = ""
    PoNo = request.GET.getlist('PoNo')
    PoDt = request.GET.getlist('PoDt')
    Amount = request.GET.getlist('Amount')

    PoNos = " PURCHASEORDER.CODE in " + "(" + str(PoNo)[1:-1] + ")"
    PoDts = " AND VARCHAR_FORMAT(PURCHASEORDER.ORDERDATE, 'DD-MM-YYYY') in  " + "(" + str(PoDt)[1:-1] + ")"

    PrintPDF(PoNos, PoDts, Amount, startdate, enddate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PurchaseOrderTable.html',
                      {'GDOrderSummary': views.GDOrderSummary, 'Exception': Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


def PrintPDF(PoNos, PoDts, Amount, startdate, enddate):
    global Exceptions
    sql = "Select    Comp.LONGDESCRIPTION As CompName " \
          ", COALESCE(PLANT.ADDRESSLINE1,'') ||' '|| COALESCE(PLANT.ADDRESSLINE2,'') ||' '|| COALESCE(PLANT.ADDRESSLINE3,'') " \
          "||' '|| COALESCE(PLANT.ADDRESSLINE4,'') ||' '|| COALESCE(PLANT.ADDRESSLINE5,'') ||' '|| COALESCE(PLANT.POSTALCODE,'') As CompADDRESS " \
          ", BUSINESSPARTNER.LEGALNAME1 As PartyName " \
          ", Case When PURCHASEORDER.ALTERNATIVEADDRESSCODE is not null Then COALESCE(ADDRESS.ADDRESSEE ,'') ||' '||  COALESCE(ADDRESS.ADDRESSLINE1, '') " \
          "||' '|| COALESCE(ADDRESS.ADDRESSLINE2, '') ||' '|| COALESCE(ADDRESS.ADDRESSLINE3, '') ||' '|| COALESCE(ADDRESS.ADDRESSLINE4, '') " \
          "|| ' ' || COALESCE(ADDRESS.ADDRESSLINE5, '') ||' '|| COALESCE(ADDRESS.POSTALCODE, '') ||' '|| COALESCE(ADDRESS.TOWN, '') " \
          "||' '|| COALESCE(ADDRESS.DISTRICT, '') Else COALESCE(BUSINESSPARTNER.ADDRESSLINE1, '') ||' '|| COALESCE(BUSINESSPARTNER.ADDRESSLINE2, '') " \
          "||' '|| COALESCE(BUSINESSPARTNER.ADDRESSLINE3, '') ||' '|| COALESCE(BUSINESSPARTNER.ADDRESSLINE4, '')  ||' '|| COALESCE(BUSINESSPARTNER.ADDRESSLINE5, '') " \
          "||' '|| COALESCE(BUSINESSPARTNER.POSTALCODE, '') " \
          "||' '|| COALESCE(BUSINESSPARTNER.TOWN, '') ||' '|| COALESCE(BUSINESSPARTNER.DISTRICT, '') End As PartyAddress " \
          ", COALESCE(ADDRESSGST.GSTINNUMBER,'') As PGstNo " \
          ", COSTCENTER.LONGDESCRIPTION As Costcenter " \
          ", PURCHASEORDER.CODE As PoNo " \
          ", PURCHASEORDER.ORDERDATE As PoDt " \
          ", COALESCE(CompGST.GSTINNUMBER,'') As CompGstNo " \
          ", Case When PURCHASEORDER.DELIVERYPOINTTYPE = 2  Then ConsineeBp.LEGALNAME1 Else FINBUSINESSUNIT.LONGDESCRIPTION End As ShippName " \
          ", Case When PURCHASEORDER.DELIVERYPOINTTYPE = 2  Then COALESCE(ConsineeAdd.ADDRESSEE ,'') ||' '||  COALESCE(ConsineeAdd.ADDRESSLINE1, '') " \
          "||' '|| COALESCE(ConsineeAdd.ADDRESSLINE2, '') ||' '|| COALESCE(ConsineeAdd.ADDRESSLINE3, '') ||' '|| COALESCE(ConsineeAdd.ADDRESSLINE4, '') " \
          "|| ' ' || COALESCE(ConsineeAdd.ADDRESSLINE5, '') ||' '|| COALESCE(ConsineeAdd.POSTALCODE, '') ||' '|| COALESCE(ConsineeAdd.TOWN, '') " \
          "||' '|| COALESCE(ConsineeAdd.DISTRICT, '') Else COALESCE(PLANT.ADDRESSLINE1,'') ||' '|| COALESCE(PLANT.ADDRESSLINE2,'') ||' '|| COALESCE(PLANT.ADDRESSLINE3,'') " \
          "||' '|| COALESCE(PLANT.ADDRESSLINE4,'') ||' '|| COALESCE(PLANT.ADDRESSLINE5,'') ||' '|| COALESCE(PLANT.POSTALCODE,'') End As ShippAddress " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LONGDESCRIPTION, '') ||' '|| COALESCE(QUALITYLEVEL.LONGDESCRIPTION,'') As ItemName " \
          ", COALESCE(PURCHASEORDERLINEIE.TARIFFCODE,'') As HsnNo " \
          ", COALESCE(PURCHASEORDERLINEIE.TAXTEMPLATECODE,'') As GSTTAXTEMP " \
          ", (Select CAST(Sum(gstVal.Value) AS DECIMAL(10,1)) ||' '|| '%' From INDTAXDETAIL gstVal " \
          "where PURCHASEORDERLINE.ABSUNIQUEID = gstVal.ABSUNIQUEID " \
          "AND     PURCHASEORDERLINEIE.TAXTEMPLATECODE = gstVal.TAXTEMPLATECODE " \
          "And     gstVal.TAXCATEGORYCODE = 'GST' " \
          "And     gstVal.CALCULATIONTYPE = 2) As Gst " \
          ", Cast((PURCHASEORDERLINE.USERPRIMARYQUANTITY) As Decimal(18,2)) As Quantity " \
          ", PURCHASEORDERLINEIE.GROSSVALUEEXT As GrossVal " \
          ", Cast(COALESCE(INDTAXDETAIL.BASEVALUE,PURCHASEORDERLINE.PRICE) As Decimal(18,3)) As GrossRate " \
          ", COALESCE(Cast(INDTAXDETAIL.Value As Decimal(18,2)),0.00) As DisPerAmt " \
          ", PURCHASEORDERLINE.USERPRIMARYUOMCODE As Unit " \
          ", Cast(COALESCE(RateAfterPer.BASEVALUE,PURCHASEORDERLINE.PRICE) As Decimal(18,3)) As Rate " \
          ", Cast((PURCHASEORDERLINE.NETVALUEINCLUDINGTAX) As Decimal(20,3)) As Amount " \
          ", (Select Cast(INDTAXDETAIL.BASEVALUE + sum( INDTAXDETAIL.CALCULATEDVALUERTC) As Decimal(20,3)) From INDTAXDETAIL " \
          "where PURCHASEORDERLINE.ABSUNIQUEID = INDTAXDETAIL.ABSUNIQUEID " \
          "AND     PURCHASEORDERLINEIE.TAXTEMPLATECODE = INDTAXDETAIL.TAXTEMPLATECODE " \
          "And     INDTAXDETAIL.TAXCATEGORYCODE = 'GST' " \
          "And     INDTAXDETAIL.CALCULATIONBASISCODE IS NOT NULL " \
          "group by INDTAXDETAIL.BASEVALUE) AS Amount2 " \
          ", COALESCE(Varchar_Format(PURCHASEORDER.CONFIRMEDDUEDATE,'DD-MM-YYYY'), Varchar_Format(PURCHASEORDER.REQUIREDDUEDATE,'DD-MM-YYYY'), '')  As Delivery " \
          ", PAYMENTMETHOD.LONGDESCRIPTION As Payment " \
          ", COALESCE(VARCHAR(NOTE.NOTE), '') As Remarks " \
          "From                            PURCHASEORDER " \
          "Left Join ORDERPARTNER ConsineeOp       On      PURCHASEORDER.DLVORDPRNCUSTOMERSUPPLIERCODE = ConsineeOp.CUSTOMERSUPPLIERCODE   " \
          "And     PURCHASEORDER.DLVORDPRNCUSTOMERSUPPLIERTYPE = ConsineeOp.CUSTOMERSUPPLIERTYPE " \
          "Left Join BUSINESSPARTNER ConsineeBp    On      ConsineeOp.ORDERBUSINESSPARTNERNUMBERID = ConsineeBp.NUMBERID     " \
          "And     PURCHASEORDER.DELIVERYPOINTUNIQUEID = ConsineeBp.ABSUNIQUEID " \
          "Left Join ADDRESS ConsineeAdd           On      PURCHASEORDER.DELIVERYPOINTCODE = ConsineeAdd.CODE " \
          "And     PURCHASEORDER.DELIVERYPOINTUNIQUEID = ConsineeAdd.UNIQUEID  " \
          "join ORDERPARTNER               On      PURCHASEORDER.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE  " \
          "And     PURCHASEORDER.ORDERTYPE = ORDERPARTNER.CUSTOMERSUPPLIERTYPE " \
          "Join BUSINESSPARTNER            On      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID " \
          "lEFT Join ADDRESS               On      PURCHASEORDER.ALTERNATIVEADDRESSCODE = ADDRESS.CODE " \
          "And     PURCHASEORDER.ALTERNATIVEADDRESSUNIQUEID = ADDRESS.UNIQUEID " \
          "Left Join ADDRESSGST            On      BUSINESSPARTNER.ABSUNIQUEID = ADDRESSGST.UNIQUEID  " \
          "Join PAYMENTMETHOD              On      PURCHASEORDER.PAYMENTMETHODCODE = PAYMENTMETHOD.CODE " \
          "Left Join NOTE                  On      PURCHASEORDER.ABSUNIQUEID = NOTE.FATHERID " \
          "Join PURCHASEORDERLINE          On      PURCHASEORDER.CODE = PURCHASEORDERLINE.PURCHASEORDERCODE " \
          "Join    LOGICALWAREHOUSE        On      PURCHASEORDERLINE.WAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Join    BUSINESSUNITVSCOMPANY   On      LOGICALWAREHOUSE.PLANTCODE =  BUSINESSUNITVSCOMPANY.FACTORYCODE " \
          "Join    FACTORY                On      BUSINESSUNITVSCOMPANY.FACTORYCODE = FACTORY.CODE " \
          "Left Join AddressGST CompGST    On      FACTORY.AbsUniqueId = CompGST.UniqueId " \
          "Join    FINBUSINESSUNIT         On      BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "Join    FINBUSINESSUNIT Comp    On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
          "Join    PLANT                   On      BUSINESSUNITVSCOMPANY.FACTORYCODE = PLANT.CODE " \
          "And     PURCHASEORDER.COUNTERCODE = PURCHASEORDERLINE.PURCHASEORDERCOUNTERCODE " \
          "Join COSTCENTER                 On      PURCHASEORDERLINE.COSTCENTERCODE = COSTCENTER.CODE " \
          "join FULLITEMKEYDECODER FIKD    ON      PURCHASEORDERLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(PURCHASEORDERLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(PURCHASEORDERLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '')  " \
          "AND     COALESCE(PURCHASEORDERLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(PURCHASEORDERLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '')  " \
          "AND     COALESCE(PURCHASEORDERLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '')  " \
          "AND     COALESCE(PURCHASEORDERLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '')  " \
          "AND     COALESCE(PURCHASEORDERLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
          "AND     COALESCE(PURCHASEORDERLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '')  " \
          "AND     COALESCE(PURCHASEORDERLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '')  " \
          "AND     COALESCE(PURCHASEORDERLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join PRODUCT                    On      PURCHASEORDERLINE.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Join PURCHASEORDERLINEIE        On      PURCHASEORDERLINE.PURCHASEORDERCODE = PURCHASEORDERLINEIE.PURCHASEORDERCODE " \
          "And     PURCHASEORDERLINE.PURCHASEORDERCOUNTERCODE = PURCHASEORDERLINEIE.PURCHASEORDERCOUNTERCODE " \
          "And     PURCHASEORDERLINE.ORDERLINE = PURCHASEORDERLINEIE.ORDERLINE " \
          "Left JOIN ItemSubcodeTemplate IST    ON      PURCHASEORDERLINE.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN USERGENERICGROUP UGG       On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then PURCHASEORDERLINE.SUBCODE01 When 2 Then PURCHASEORDERLINE.SUBCODE02 When 3 Then PURCHASEORDERLINE.SUBCODE03 When 4 Then PURCHASEORDERLINE.SUBCODE04 When 5 Then PURCHASEORDERLINE.SUBCODE05 " \
          "When 6 Then PURCHASEORDERLINE.SUBCODE06 When 7 Then PURCHASEORDERLINE.SUBCODE07 When 8 Then PURCHASEORDERLINE.SUBCODE08 When 9 Then PURCHASEORDERLINE.SUBCODE09 When 10 Then PURCHASEORDERLINE.SUBCODE10 End = UGG.Code " \
          "JOIN QUALITYLEVEL               ON      PURCHASEORDERLINE.QUALITYCODE = QUALITYLEVEL.CODE " \
          "AND     PURCHASEORDERLINE.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
          "Left Join INDTAXDETAIL RateAfterPer    On      PURCHASEORDERLINE.ABSUNIQUEID = RateAfterPer.ABSUNIQUEID " \
          "And     RateAfterPer.TAXCATEGORYCODE = 'DIS' " \
          "And     RateAfterPer.ITAXCODE = 'GD4' " \
          "Left Join INDTAXDETAIL          On      PURCHASEORDERLINE.ABSUNIQUEID = INDTAXDETAIL.ABSUNIQUEID " \
          "And     INDTAXDETAIL.TAXCATEGORYCODE = 'DIS' " \
          "And     INDTAXDETAIL.ITAXCODE = 'GD3' " \
          "where "+PoNos+" "+PoDts+" " \
          "Order   By   CompName, PartyName, Costcenter, PoNo, ShippName "

    stmt = con.db.prepare(con.conn, sql)
    # Explicitly bind parameters
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 30:
            pdfrpt.d = 515
            pdfrpt.c.showPage()
            pdfrpt.header(pdfrpt.divisioncode)

    if result == False:
        if counter > 0:

            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.c.drawString(30, pdfrpt.d, "Costcenter: " + pdfrpt.Costcenter[-1])
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.c.line(0, pdfrpt.d, 600, pdfrpt.d)
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.TotalPrit(pdfrpt.d,pdfrpt.i)
            pdfrpt.d = pdfrpt.dlocalvalue()
            pdfrpt.c.drawString(10, pdfrpt.d, "Delivery: " + '        ' + pdfrpt.Delivery[-1])
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.c.drawString(10, pdfrpt.d, "Payment: " + '        ' + pdfrpt.Payment[-1])
            pdfrpt.d = pdfrpt.dslocal()
            pdfrpt.c.drawString(10, pdfrpt.d, pdfrpt.Remarks[-1])
            pdfrpt.d = pdfrpt.dlocalvalue()
            pdfrpt.c.drawString(10, pdfrpt.d, "Note: Please Kindly Confirm Receipt Of This Order")
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.c.drawString(400, pdfrpt.d, "For " + ' ' + pdfrpt.divisioncode[-1])
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.Footer(pdfrpt.d)

            Exceptions = ""
            counter = 0
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria "
            return


    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    pdfrpt.TotalClean()
    # counter = 0
    pdfrpt.d = pdfrpt.newpage()
    pdfrpt.i = pdfrpt.SetSerialNo()