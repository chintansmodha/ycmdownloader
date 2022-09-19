from ProcessSelection import MRNRegister_ProcessSelection as MRV
from PrintPDF import ItemWise_Details_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
from datetime import datetime
counter=0
def ItemWise_Details_PrintPDF(LSDepartment, LSSupplier, LSItemType, LSItems, LDStartDate, LDEndDate, LCDepartment,LCSupplier, LCItemType, LCItem, LSFileName, LSReportType):
    Department = str(LSDepartment)
    Supplier = str(LSSupplier)
    ItemType = str(LSItemType)
    Item = str(LSItems)

    Department = '(' + Department[1:-1] + ')'
    Supplier = '(' + Supplier[1:-1] + ')'
    ItemType = '(' + ItemType[1:-1] + ')'
    Item = '(' + Item[1:-1] + ')'

    if not LCDepartment and not LSDepartment:
        Department = " "
    elif LCDepartment:
        Department = " "
    elif LSDepartment:
        Department = "AND COSTCENTER.CODE in " + Department

    if not LCSupplier and not LSSupplier:
        Supplier = " "
    elif LCSupplier:
        Supplier = " "
    elif LSSupplier:
        Supplier = "AND BUSINESSPARTNER.NUMBERID in " + Supplier

    if not LCItemType and not LSItemType:
        ItemType = " "
    elif LCItemType:
        ItemType = " "
    elif LSItemType:
        ItemType = "AND MRNDETAIL.ITEMTYPEAFICODE in " + ItemType

    if not LCItem and not LSItems:
        Item=" "
    elif LCItem:
        Item=" "
    elif LSItems:
        Item = "AND COALESCE(MRNDETAIL.ITEMTYPEAFICODE,'')||COALESCE(MRNDETAIL.SubCode01,'')" \
          "||COALESCE(MRNDETAIL.SubCode02,'')||COALESCE(MRNDETAIL.SubCode03,'')||COALESCE(MRNDETAIL.SubCode04,'')" \
          "||COALESCE(MRNDETAIL.SubCode05,'')||COALESCE(MRNDETAIL.SubCode06,'')||COALESCE(MRNDETAIL.SubCode07,'')" \
          "||COALESCE(MRNDETAIL.SubCode08,'')||COALESCE(MRNDETAIL.SubCode09,'')" \
          "||COALESCE(MRNDETAIL.SubCode10,'') in "+Item

    sql = "select DIVISION.LONGDESCRIPTION AS DIVCODE,MRNHEADER.CODE AS MRNNO,MRNHEADER.MRNDATE AS MRNDATE," \
          "PRODUCT.LONGDESCRIPTION AS ITEM,MRNDETAIL.PRIMARYQTY AS QUANTITY," \
          "MRNDETAIL.BASICVALUE AS AMOUNT,MRNDETAIL.UNITPRICE AS MRNRATE,COSTCENTER.LONGDESCRIPTION AS STORE," \
          "BUSINESSPARTNER.LEGALNAME1 AS SUPPLIER,PURCHASEORDERLINE.PRICE AS PORATE " \
          "FROM MRNHEADER " \
          "JOIN    DIVISION        ON      MRNHEADER.DIVISIONCODE = DIVISION.CODE " \
          "JOIN ORDERPARTNER             ON      MRNHEADER.ORDPRNCUSTOMERSUPPLIERTYPE = ORDERPARTNER.CUSTOMERSUPPLIERTYPE " \
          "AND     MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE " \
          "JOIN BUSINESSPARTNER          ON      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID " \
          "JOIN    MRNDETAIL       ON      MRNHEADER.COMPANYCODE = MRNDETAIL.MRNHEADERCOMPANYCODE " \
          "AND MRNHEADER.DIVISIONCODE = MRNDETAIL.MRNHEADERDIVISIONCODE " \
          "AND MRNHEADER.MRNPREFIXCODE = MRNDETAIL.MRNHEADERMRNPREFIXCODE " \
          "AND MRNHEADER.CODE =  MRNDETAIL.MRNHEADERCODE " \
          "JOIN COSTCENTER ON COSTCENTER.CODE=MRNDETAIL.COSTCENTERCODE " \
          "JOIN    FullItemKeyDecoder FIKD         ON      MRNDETAIL.ITEMTYPEAFICODE  = FIKD.ITEMTYPECODE " \
          "                                AND     COALESCE(MrnDetail.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          "                                        AND     COALESCE(MrnDetail.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          "                                        AND     COALESCE(MrnDetail.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          "                                        AND     COALESCE(MrnDetail.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
          "                                        AND     COALESCE(MrnDetail.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
          "                                        AND     COALESCE(MrnDetail.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
          "                                        AND     COALESCE(MrnDetail.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
          "                                        AND     COALESCE(MrnDetail.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
          "                                        AND     COALESCE(MrnDetail.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
          "                                        AND     COALESCE(MrnDetail.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
          "                                        JOIN    PRODUCT                         ON MRNDETAIL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE                                        AND FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "JOIN PURCHASEORDERLINE ON MRNDETAIL.PURCHASEORDERCODE=PURCHASEORDERLINE.PURCHASEORDERCODE " \
          "AND MRNDETAIL.PURCHASEORDERCOUNTERCODE=PURCHASEORDERLINE.PURCHASEORDERCOUNTERCODE " \
          "AND MRNDETAIL.ORDERLINE = PURCHASEORDERLINE.ORDERLINE "\
          "AND MRNDETAIL.ITEMTYPEAFICODE = PURCHASEORDERLINE.ITEMTYPEAFICODE " \
          "AND COALESCE(MrnDetail.SubCode01,'') = COALESCE(PURCHASEORDERLINE.SubCode01,'') " \
          "AND COALESCE(MrnDetail.SubCode02,'') = COALESCE(PURCHASEORDERLINE.SubCode02,'') " \
          "AND COALESCE(MrnDetail.SubCode03,'') = COALESCE(PURCHASEORDERLINE.SubCode03,'') " \
          "AND COALESCE(MrnDetail.SubCode04,'') = COALESCE(PURCHASEORDERLINE.SubCode04,'') " \
          "AND COALESCE(MrnDetail.SubCode05,'') = COALESCE(PURCHASEORDERLINE.SubCode05,'') " \
          "AND COALESCE(MrnDetail.SubCode06,'') = COALESCE(PURCHASEORDERLINE.SubCode06,'') " \
          "AND COALESCE(MrnDetail.SubCode07,'') = COALESCE(PURCHASEORDERLINE.SubCode07,'') " \
          "AND COALESCE(MrnDetail.SubCode08,'') = COALESCE(PURCHASEORDERLINE.SubCode08,'') " \
          "AND COALESCE(MrnDetail.SubCode09,'') = COALESCE(PURCHASEORDERLINE.SubCode09,'') "  \
          "where MRNHEADER.MRNDATE between ? and ? " + Department + Supplier + ItemType + Item + " " \
          "And MRNHEADER.INVOICENO is not null " \
          "order by DIVISION.LONGDESCRIPTION,COSTCENTER.LONGDESCRIPTION,MRNHEADER.CODE,MRNHEADER.MRNDATE Desc,PRODUCT.LONGDESCRIPTION,BUSINESSPARTNER.LEGALNAME1"\

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    # Explicitly bind parameters
    con.db.bind_param(stmt, 1, stdt)
    con.db.bind_param(stmt, 2, etdt)

    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        # pdfrpt.d = pdfrpt.dvalue()

        result = con.db.fetch_both(stmt)

        # pdfrpt.c.line(0, 12, 600, 12)
        if pdfrpt.d < 20:
            pdfrpt.d = 730
            pdfrpt.c.showPage()
            pdfrpt.header(stdt, etdt, pdfrpt.divisioncode)
            pdfrpt.fonts(7)
            # pdfrpt.d=pdfrpt.d-20
            # pdfrpt.itemcodes(result, pdfrpt.d)

    if result == False:
        if counter > 0:
            pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
            pdfrpt.fonts(7)
            pdfrpt.printstoretotal()
            pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
            pdfrpt.printcompanytotallast()
            # pdfrpt.printtotal()
            # pdfrpt.storeclean()
            #pdfrpt.companyclean()
            pdfrpt.cleanstore()
            MRV.Exceptions = ""
        elif counter == 0:
            MRV.Exceptions = "Note: No Result found according to your selected criteria "
            return

    pdfrpt.c.showPage()
    pdfrpt.c.save()
    # url = "file:///D:/Report Development/Generated Reports/MRN REGISTER/" + LSFileName + ".pdf"
    # os.startfile(url)
    pdfrpt.newrequest()
    counter = 0
    #pdfrpt.d = pdfrpt.newpage()