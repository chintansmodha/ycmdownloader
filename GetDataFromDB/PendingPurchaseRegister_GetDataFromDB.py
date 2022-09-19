import os

from PrintPDF import PendingPurchaseRegister_PrintPDF as pdfrpt
from Global_Files import Connection_String as con

def PrintPDF(LSCompanyCode, LSparty, LSFileName, LSallCompany, LSallParty, LSallByPending, LSallPartlyPending,LSallClose):
    sqlwhere = ''
    allcompany = str(LSallCompany)
    if allcompany == 'None' and len(LSCompanyCode) != 0:
        company = str(LSCompanyCode)
        LSCompanycode = '(' + company[1:-1] + ')'
        sqlwhere = 'DIVISION.CODE in ' + LSCompanycode
        print('sqlwhere in company : ' + sqlwhere)

    allparty = str(LSparty)
    if allparty == 'None' and len(LSparty) != 0:
        if sqlwhere != '':
            sqlwhere += ' AND '
        party = str(LSparty)
        LSparty = '(' + party[1:-1] + ')'
        print('party from form : ' + LSparty)
        # sqlwhere += ' BusinessPartner.CODE  in ' + LSparty + ''
        sqlwhere += ' BusinessPartner.LegalName1  in ' + LSparty + ''
        print('sqlwhere in party : ' + sqlwhere)

    if LSallByPending == '1' and LSallPartlyPending == '1':
        if sqlwhere != '':
            sqlwhere += ' AND '
        sqlwhere += ' PurchaseOrderDelivery.ProgressStatus IN (0,1) '
    elif LSallByPending == '1':
        if sqlwhere != '':
            sqlwhere += ' And '
        sqlwhere += ' PurchaseOrderDelivery.ProgressStatus IN (0) '
    elif LSallPartlyPending == '1':
        if sqlwhere != '':
            sqlwhere += ' And '
        sqlwhere += ' PurchaseOrderDelivery.ProgressStatus IN (1) '


    if sqlwhere != '':
        sqlwhere = 'WHERE ' + sqlwhere

    print(sqlwhere)

    if (len(sqlwhere) == 6):
        sqlwhere = ''

    print('sqlwhere after if : ' + sqlwhere)

    sql = "Select  DIVISION.LONGDESCRIPTION AS DIVISIONName " \
          "        ,purchaseorder.code as PONo " \
          "        , purchaseorder.orderdate as PODate " \
          "        , BusinessPartner.LegalName1 as Supplier " \
          "        , Product.LongDescription as ProductName " \
          "        , QualityLevel.LongDescription as QualityName " \
          "        , purchaseorderline.userprimaryquantity as POQuantity " \
          "        , PurchaseOrderDelivery.userprimaryquantity as PendingQuantity " \
          "From    PurchaseOrderline " \
          "JOIN    purchaseorder   ON      purchaseorderline.PURCHASEORDERCOUNTERCODE      = purchaseorder.countercode " \
          "                        AND     purchaseorderline.PURCHASEORDERCODE             = purchaseorder.code " \
          "JOIN    DIVISION        ON      PurchaseOrder.DIVISIONCODE                      = DIVISION.CODE " \
          "JOIN    OrderPartner    ON      PurchaseOrder.ORDPRNCUSTOMERSUPPLIERCODE        = OrderPartner.CUSTOMERSUPPLIERCODE " \
          "                        AND     OrderPartner.CUSTOMERSUPPLIERTYPE               = 2 " \
          "JOIN    BusinessPartner ON      OrderPartner.ORDERBUSINESSPARTNERNUMBERID     = BusinessPartner.NUMBERID " \
          "JOIN    PurchaseOrderDelivery   ON      PurchaseOrderDelivery.PurOrderLinePurchaseOrderCode = PurchaseOrderLine.PurchaseOrderCode " \
          "         AND PurchaseOrderDelivery.ItemTypeAFICode = PurchaseOrderLine.ItemTypeAFICode " \
          "         AND COALESCE(PurchaseOrderDelivery.SubCode01,'') = COALESCE(PurchaseOrderLine.SubCode01,'') " \
          "         AND COALESCE(PurchaseOrderDelivery.SubCode02,'') = COALESCE(PurchaseOrderLine.SubCode02,'') " \
          "         AND COALESCE(PurchaseOrderDelivery.SubCode03,'') = COALESCE(PurchaseOrderLine.SubCode03,'') " \
          "         AND COALESCE(PurchaseOrderDelivery.SubCode04,'') = COALESCE(PurchaseOrderLine.SubCode04,'') " \
          "         AND COALESCE(PurchaseOrderDelivery.SubCode05,'') = COALESCE(PurchaseOrderLine.SubCode05,'') " \
          "         AND COALESCE(PurchaseOrderDelivery.SubCode06,'') = COALESCE(PurchaseOrderLine.SubCode06,'') " \
          "         AND COALESCE(PurchaseOrderDelivery.SubCode07,'') = COALESCE(PurchaseOrderLine.SubCode07,'') " \
          "         AND COALESCE(PurchaseOrderDelivery.SubCode08,'') = COALESCE(PurchaseOrderLine.SubCode08,'') " \
          "         AND COALESCE(PurchaseOrderDelivery.SubCode09,'') = COALESCE(PurchaseOrderLine.SubCode09,'') " \
          "         AND COALESCE(PurchaseOrderDelivery.SubCode10,'') = COALESCE(PurchaseOrderLine.SubCode10,'') " \
          "JOIN    Product         ON      PurchaseOrderLine.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "         AND COALESCE(PurchaseOrderLine.SubCode01,'') = COALESCE(Product.SubCode01,'') " \
          "         AND COALESCE(PurchaseOrderLine.SubCode02,'') = COALESCE(Product.SubCode02,'') " \
          "         AND COALESCE(PurchaseOrderLine.SubCode03,'') = COALESCE(Product.SubCode03,'') " \
          "         AND COALESCE(PurchaseOrderLine.SubCode04,'') = COALESCE(Product.SubCode04,'') " \
          "         AND COALESCE(PurchaseOrderLine.SubCode05,'') = COALESCE(Product.SubCode05,'') " \
          "         AND COALESCE(PurchaseOrderLine.SubCode06,'') = COALESCE(Product.SubCode06,'') " \
          "         AND COALESCE(PurchaseOrderLine.SubCode07,'') = COALESCE(Product.SubCode07,'') " \
          "         AND COALESCE(PurchaseOrderLine.SubCode08,'') = COALESCE(Product.SubCode08,'') " \
          "         AND COALESCE(PurchaseOrderLine.SubCode09,'') = COALESCE(Product.SubCode09,'') " \
          "         AND COALESCE(PurchaseOrderLine.SubCode10,'') = COALESCE(Product.SubCode10,'') " \
          "JOIN    QualityLevel    ON      PurchaseOrderLine.ITEMTYPEAFICODE       = QualityLevel.ITEMTYPECODE " \
          "                        AND     PurchaseOrderLine.QualityCode               = QualityLevel.Code " \

    sql += sqlwhere + " Order By DivisionName, ProductName, PODate, PONo ;" \

    print(sql)

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:

        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, "", "")
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 20:
            pdfrpt.d = 730
            pdfrpt.c.showPage()
            pdfrpt.header("", "", pdfrpt.divisioncode)
            pdfrpt.d = pdfrpt.d - 20
            # pdfrpt.productname(result, pdfrpt.d)

    if result == False:
        pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
        pdfrpt.fonts(7)
        pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
        pdfrpt.fonts(8)
        pdfrpt.c.drawString(10, pdfrpt.d, str(pdfrpt.divisioncode[-2]) + " TOTAL : ")
        pdfrpt.c.drawAlignedString(225, pdfrpt.d, str("%.3f" % float(pdfrpt.CompanyQuentityTotal)))
        pdfrpt.c.drawAlignedString(300, pdfrpt.d, str("%.2f" % float(pdfrpt.CompanyAmountTotal)))

    pdfrpt.c.showPage()
    pdfrpt.c.save()
    # url="file:///D:/Report Development/Generated Reports/Pending Purchase Register/"+LSFileName+".pdf"
    # os.startfile(url)
    pdfrpt.newrequest()
    pdfrpt.d=pdfrpt.newpage()