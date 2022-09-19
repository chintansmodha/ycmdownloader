from datetime import datetime
from PrintPDF import MRNRegister_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
counter=0
from ProcessSelection import MRNRegister_ProcessSelection as MRV
def MRNRegister_PrintPDF(LSDepartment,LSSupplier,LSItemType,LSItems,LDStartDate,LDEndDate,LCDepartment,LCSupplier,LCItemType,LCItem,LSFileName,LSReportType):

    Department = str(LSDepartment)
    Supplier = str(LSSupplier)
    ItemType = str(LSItemType)
    Item = str(LSItems)

    Department = '(' + Department[1:-1] + ')'
    Supplier = '(' + Supplier[1:-1] + ')'
    ItemType = '(' + ItemType[1:-1] + ')'
    Item = '(' + Item[1:-1] + ')'

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    if not LCDepartment and not LSDepartment:
        Department=" "
    elif LCDepartment:
        Department=" "
    elif LSDepartment:
        Department = "AND COSTCENTER.CODE in " + Department

    if not LCSupplier and not LSSupplier:
        Supplier=" "
    elif LCSupplier:
        Supplier=" "
    elif LSSupplier:
        Supplier="AND BUSINESSPARTNER.NUMBERID in " + Supplier

    if not LCItemType and not LSItemType:
        ItemType=" "
    elif LCItemType:
        ItemType=" "
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
          " PRODUCT.LONGDESCRIPTION AS ITEM,MRNHEADER.INVOICEDATE AS BILLDATE,MRNHEADER.CHALLANDATE AS CHALLANDATE," \
          " MRNHEADER.CHALLANNO AS CHALLANNO,BUSINESSPARTNER.LEGALNAME1 AS SUPPLIER,COSTCENTER.LONGDESCRIPTION AS STORE, " \
          "MRNHEADER.INVOICENO AS BILLNO,UNITOFMEASURE.LONGDESCRIPTION AS UNIT, MRNHEADER.NETVALUE AS BILLAMOUNT," \
          "MRNDETAIL.LRDATE AS LRDATE, " \
          "MRNDETAIL.LRNO AS LRNO, MRNDETAIL.PRIMARYQTY AS QUANTITY  " \
          "FROM MRNHEADER " \
          "JOIN    DIVISION        ON      MRNHEADER.DIVISIONCODE = DIVISION.CODE " \
          "JOIN ORDERPARTNER             ON      MRNHEADER.ORDPRNCUSTOMERSUPPLIERTYPE = ORDERPARTNER.CUSTOMERSUPPLIERTYPE " \
          "AND     MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE " \
          "JOIN BUSINESSPARTNER          ON      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID " \
          "JOIN    MRNDETAIL       ON      MRNHEADER.COMPANYCODE = MRNDETAIL.MRNHEADERCOMPANYCODE " \
          "AND MRNHEADER.DIVISIONCODE = MRNDETAIL.MRNHEADERDIVISIONCODE " \
          "AND MRNHEADER.MRNPREFIXCODE = MRNDETAIL.MRNHEADERMRNPREFIXCODE " \
          "AND MRNHEADER.CODE =  MRNDETAIL.MRNHEADERCODE " \
          "JOIN    UNITOFMEASURE         ON      MRNDETAIL.PRIMARYUMCODE = UNITOFMEASURE.CODE " \
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
          " where MRNHEADER.MRNDATE between '"+str(stdt)+"' and '"+str(etdt)+"' "+Department+Supplier+ItemType+Item+" " \
                                                                                                          " And MRNHEADER.INVOICENO is not null " \
            "order by DIVISION.LONGDESCRIPTION,COSTCENTER.CODE,MRNHEADER.CODE,MRNHEADER.MRNDATE Desc,BUSINESSPARTNER.NUMBERID,MRNDETAIL.ITEMTYPEAFICODE"

    print(sql)
    stmt = con.db.prepare(con.conn, sql)

    # Explicitly bind parameters
    # con.db.bind_param(stmt, 1, stdt)
    # con.db.bind_param(stmt, 2, etdt)

    con.db.execute(stmt)

    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d,stdt,etdt)
        pdfrpt.d=pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
        result = con.db.fetch_both(stmt)

        #pdfrpt.c.line(0, 12, 600, 12)
        if pdfrpt.d<20:
            pdfrpt.d=720
            pdfrpt.c.showPage()
            pdfrpt.header(stdt,etdt,pdfrpt.divisioncode)
            # pdfrpt.d=pdfrpt.d-20
            # pdfrpt.itemcodes(result, pdfrpt.d)

    if result == False:
        if counter > 0:
            pdfrpt.d=pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
            pdfrpt.fonts(7)
            pdfrpt.printstoretotallast(stdt,etdt,pdfrpt.divisioncode)
            pdfrpt.d=pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
            pdfrpt.printtotallast()
            pdfrpt.storeclean()
            pdfrpt.companyclean()
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
    counter=0
    pdfrpt.d = pdfrpt.newpage()