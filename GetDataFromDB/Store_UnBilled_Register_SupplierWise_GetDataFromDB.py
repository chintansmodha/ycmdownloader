import os
from Global_Files import Connection_String as con
from PrintPDF import Store_UnBilled_Register_SupplierWise_PrintPDF as pdfrpt
from datetime import datetime
from ProcessSelection import Store_Unbilled_GRN_ProcessSelection as SRV
counter=0

def StoreRegisterSupplierWisePrintPDF(LSallPlant, LSallSupplier, LSallItem, LSPlant, LSSupplier, LSItem, LDStartDate,
                                 LDEndDate, LSReportType, LSFileName, LScheckboxgoods, LScheckboxcapitalgoods,
                                 LScheckboxservice):
    sqlwhere = ''
    sqlwhereGoods = ''
    sqlwhereCapitalGoods = ''
    sqlwhereServices = ''

    allplant = str(LSallPlant)
    if allplant == 'None' and len(LSPlant)!=0:
        if sqlwhere != '':
            sqlwhere += ' AND '
        plant = str(LSPlant)
        LSPlant = '(' + plant[1:-1] + ')'
        sqlwhere += ' AND PLANT.CODE IN  ' + LSPlant
        print('sqlwhere in Plant : ' + sqlwhere)

    allsupplier= str(LSallSupplier)
    if allsupplier == 'None' and len(LSSupplier)!=0:
        if sqlwhere != '':
            sqlwhere += ' AND '
        supplier = str(LSSupplier)
        LSSupplier = '(' + supplier[1:-1] + ')'
        print('Supplier from form : ' + LSSupplier)
        sqlwhere += ' BusinessPartner.NUMBERID IN ' + LSSupplier + ''
        print('sqlwhere in supplier : ' + sqlwhere)

    allitem=str(LSallItem)
    if allitem == 'None' and len(LSItem)!=0:
        if sqlwhere != '':
            sqlwhere += ' AND '
        item = str(LSItem)
        LSItem = '(' + item[1:-1] + ')'
        print('Item from form : ' + LSItem)
        sqlwhere += 'PRODUCTIE.ITEMTYPECODE IN ' + LSItem + ''

    # if LScheckboxgoods == '1':
    #     sqlwhere += ' AND '
    #     sqlwhere += 'PRODUCTIE.InputCapital = 0 And PRODUCTIE.ServiceBillFlag = 0'
    #     print('sqlwhere in inputcapital and serviceflag : ' + sqlwhere)
    #
    # if LScheckboxcapitalgoods == '1':
    #     if sqlwhere != '':
    #         sqlwhere += ' AND '
    #     sqlwhere += ' PRODUCTIE.InputCapital = 1 And PRODUCTIE.ServiceBillFlag = 0'
    #     print('inputcapital : '+sqlwhere)
    #
    # if LScheckboxservice == '1':
    #     if sqlwhere != '':
    #         sqlwhere += ' AND '
    #     sqlwhere += 'PRODUCTIE.ServiceBillFlag = 1'
    #     print('sevicebillflag : '+sqlwhere)

    if LScheckboxgoods == '1' or LScheckboxcapitalgoods == '1' or LScheckboxservice == '1':
        sqlwhere += ' AND '
        if LScheckboxgoods == '1':
            sqlwhereGoods = '(PRODUCTIE.InputCapital = 0 And PRODUCTIE.ServiceBillFlag = 0)'

    if LScheckboxcapitalgoods == '1':
        if LScheckboxgoods != "" or LScheckboxcapitalgoods == "":
            if LScheckboxgoods == '1':
                sqlwhereCapitalGoods = ' AND '
            sqlwhereCapitalGoods += '(PRODUCTIE.InputCapital = 1 And PRODUCTIE.ServiceBillFlag = 0)'
    if LScheckboxservice == '1':
        if LScheckboxcapitalgoods != "" or LScheckboxservice != "":
            if LScheckboxcapitalgoods == '1' or LScheckboxgoods == '1':
                sqlwhereServices = ' AND '
            sqlwhereServices += '(PRODUCTIE.ServiceBillFlag = 1)'
        # if (LScheckboxgoods != "" Or LScheckboxcapitalgoods != "", " Or ", "") + '(PRODUCTIE.ServiceBillFlag = 1)'

    if LScheckboxgoods == '1' or LScheckboxcapitalgoods == '1' or LScheckboxservice == '1':
        sqlwhere += '('+sqlwhereGoods + sqlwhereCapitalGoods + sqlwhereServices+")"

    sql = "SELECT  Distinct  Plant.LONGDESCRIPTION as PlantName " \
          "        , MRNHEADER.MRNPREFIXCODE AS MRNPREFIX " \
          "        , MRNHEADER.CODE AS MRNCODE " \
          "        , MRNHEADER.MRNDATE  " \
          "        , BusinessPartner.LegalName1 as Supplier " \
          "        , COALESCE(MRNHEADER.CHALLANNO,'') AS CHALNO " \
          "        , COALESCE(MRNHEADER.CHALLANDATE,'1991-01-01') AS CHALDATE " \
          "        , MrnHeader.InvoiceNo " \
          "        , MrnHeader.InvoiceDate " \
          "         , COSTCENTER.LONGDESCRIPTION as Costcentername " \
          "FROM     MRNHEADER " \
          "JOIN    ORDERPARTNER    ON      MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE    = ORDERPARTNER.CUSTOMERSUPPLIERCODE " \
          "                        AND     MRNHEADER.ORDPRNCUSTOMERSUPPLIERTYPE    = ORDERPARTNER.CUSTOMERSUPPLIERType " \
          "JOIN    BusinessPartner ON      ORDERPARTNER.OrderBusinessPartnerNumberId     = BusinessPartner.NUMBERID " \
          "JOIN    MRNDetAil       ON      MrnHeader.code = MrnDetail.MRNHEADERCODE " \
          "                        AND     MrnHeader.DIVISIONCODE = MrnDetail.MRNHEADERDIVISIONCODE " \
          "                        AND     MrnHeader.MRNPREFIXCODE = MrnDetail.MRNHEADERMRNPREFIXCODE " \
          "JOIN    COSTCENTER      ON      MrnDetail.costcentercode          = costcenter.code " \
          "JOIN    LogicalWarehouse ON      MrnDetail.LogicalWarehouseCode   = LogicalWarehouse.code " \
          "                        AND     MrnDetail.LOGICALWAREHOUSECOMPANYCODE    = LogicalWarehouse.COMPANYCODE  " \
          "JOIN    Plant           ON      LogicalWarehouse.Plantcode               = Plant.Code " \
          "JOIN    PRODUCTIE       ON      MrnDetail.ItemTypeAFICODE                            = PRODUCTIE.ITEMTYPECODE " \
          "             AND COALESCE(MrnDetail.SubCode01,'') = COALESCE(ProductIE.SubCode01,'')   " \
          "             AND COALESCE(MrnDetail.SubCode02,'') = COALESCE(ProductIE.SubCode02,'')   " \
          "             AND COALESCE(MrnDetail.SubCode03,'') = COALESCE(ProductIE.SubCode03,'')   " \
          "             AND COALESCE(MrnDetail.SubCode04,'') = COALESCE(ProductIE.SubCode04,'')   " \
          "             AND COALESCE(MrnDetail.SubCode05,'') = COALESCE(ProductIE.SubCode05,'')   " \
          "             AND COALESCE(MrnDetail.SubCode06,'') = COALESCE(ProductIE.SubCode06,'')   " \
          "             AND COALESCE(MrnDetail.SubCode07,'') = COALESCE(ProductIE.SubCode07,'')   " \
          "             AND COALESCE(MrnDetail.SubCode08,'') = COALESCE(ProductIE.SubCode08,'')   " \
          "             AND COALESCE(MrnDetail.SubCode09,'') = COALESCE(ProductIE.SubCode09,'')   " \
          "             AND COALESCE(MrnDetail.SubCode10,'') = COALESCE(ProductIE.SubCode10,'') " \
          "WHERE   MrnHeader.PurchaseInvoiceCode Is Null And MrnHeader.PurchaseInvoiceInvoiceDate Is Null " \
          "             AND MRNHEADER.MRNDATE between ? and ? "
    sql += sqlwhere + " ORDER BY  PlantName,Supplier"

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    # Explicitly bind parameters

    con.db.bind_param(stmt, 1, stdt)
    con.db.bind_param(stmt, 2, etdt)

    # stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        global counter
        counter = counter + 1

        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d,stdt,etdt)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 14:
            pdfrpt.d = 730
            pdfrpt.c.showPage()
            pdfrpt.header(stdt,etdt,pdfrpt.divisioncode)
            pdfrpt.d = pdfrpt.d - 20
            pdfrpt.itemcodes(result, pdfrpt.d)

    if result == False:
        if counter >= 0:
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(7)

            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)

            pdfrpt.fonts(8)
                # ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)
            SRV.Exceptions = ""
        elif counter == 0:
            SRV.Exceptions = "Note: No Result found according to your selected criteria"
            return


    if counter==0:
        SRV.Exceptions = "Note: No Result found according to your selected criteria "
    else:
        pdfrpt.c.showPage()
        pdfrpt.c.save()
        # url = "file:///D:/Reports/ReportDevelopment/" + LSFileName + ".pdf"
        # os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()
