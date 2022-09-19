from datetime import datetime
from PrintPDF import GSTRegister_PrintPDF as pdfrpt
# from PrintPDF import GSTRegister_PrintXLS as xlsrpt
from Global_Files import Connection_String as con
from ProcessSelection import GSTRegister_ProcessSelection as GRV
counter=0

def GSTRegister_PrintPDF(LSCompanyUnitCode,LSParty,LDStartDate,LDEndDate,LCParty,LCCompanyCode,LSFileName):

    # if LBFileType == '2':
    #     xlsrpt.filename()
    party = str(LSParty)
    companyunitcode = str(LSCompanyUnitCode)
    LSPartys = '(' + party[1:-1] + ')'
    LSCompanyUnitCodes = '(' + companyunitcode[1:-1] + ')'

    if not LCParty and not LSParty:
        Party=" "
    elif LCParty:
        Party=" "
    elif LSParty:
        Party = "AND ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID in " + str(LSPartys)

    if not LCCompanyCode and not LSCompanyUnitCode:
        CompanyCode=" "
    elif LCCompanyCode:
        CompanyCode=" "
    elif LSCompanyUnitCode:
        CompanyCode="AND PLANT.CODE in "+str(LSCompanyUnitCodes)

    sql = " Select DIVISION.LONGDESCRIPTION AS DIVCODE" \
          ", MRNDETAIL.INVOICEQUANTITY AS QUANTITY" \
          ", MRNDETAIL.UNITPRICE AS RATE, " \
          " MRNDETAIL.BASICVALUE AS BASICVALUE" \
          ", MRNDETAIL.ITEMTYPEAFICODE AS ITEMCODE" \
          ", MRNHEADER.CODE AS MRNNO" \
          ", MRNDETAIL.ABSUNIQUEID AS ID," \
          " MRNHEADER.MRNDATE AS MRNDATE" \
          ", PRODUCT.LONGDESCRIPTION AS ITEM" \
          ", PURCHASEINVOICE.INVOICEDATE AS BILLDATE, " \
          " PURCHASEINVOICE.CODE AS BILLNO" \
          ", PURCHASEINVOICE.INVOICEAMOUNT AS BILLAMOUNT," \
          " FINDOCUMENT.CODE AS FINNO" \
          ", FINDOCUMENT.FINANCEDOCUMENTDATE AS FINDATE" \
          ", BUSINESSPARTNER.LEGALNAME1 AS SUPPLIER," \
          "COALESCE(ADDRESSGST.GSTINNumber,ADDRESSGST.ProvisionalGSTINNumber,'') As GSTNO," \
          "COSTCENTER.LONGDESCRIPTION AS STORE" \
          " FROM MRNHEADER" \
          " JOIN    DIVISION                        ON      MRNHEADER.DIVISIONCODE = DIVISION.CODE" \
          " JOIN    PURCHASEINVOICE                 ON      PURCHASEINVOICE.COMPANYCODE=MRNHEADER.COMPANYCODE" \
          "                                         AND PURCHASEINVOICE.DIVISIONCODE=MRNHEADER.DIVISIONCODE" \
          "                                         AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERTYPE" \
          "                                         AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE" \
          "                                         AND PURCHASEINVOICE.CODE=MRNHEADER.PURCHASEINVOICECODE" \
          "                                         AND PURCHASEINVOICE.INVOICEDATE= MRNHEADER.PURCHASEINVOICEINVOICEDATE" \
          " JOIN ORDERPARTNER                       ON PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE = ORDERPARTNER.CUSTOMERSUPPLIERTYPE" \
          "                                        AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE" \
          " JOIN BUSINESSPARTNER                    ON ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID" \
          " JOIN    FINDOCUMENT                     ON      FINDOCUMENT.COMPANYCODE=PURCHASEINVOICE.COMPANYCODE" \
          "                                         AND FINDOCUMENT.BUSINESSUNITCODE=PURCHASEINVOICE.FINDOCBUSINESSUNITCODE" \
          "                                         AND FINDOCUMENT.FINANCIALYEARCODE=PURCHASEINVOICE.FINDOCFINANCIALYEARCODE" \
          "                                         AND FINDOCUMENT.DOCUMENTTEMPLATECODE=PURCHASEINVOIcE.FINDOCTEMPLATECODE" \
          "                                         AND FINDOCUMENT.CODE=PURCHASEINVOICE.FINDOCCODE" \
          " JOIN    MRNDETAIL                       ON      MRNHEADER.COMPANYCODE = MRNDETAIL.MRNHEADERCOMPANYCODE" \
          "                                         AND MRNHEADER.DIVISIONCODE = MRNDETAIL.MRNHEADERDIVISIONCODE" \
          "                                         AND MRNHEADER.MRNPREFIXCODE = MRNDETAIL.MRNHEADERMRNPREFIXCODE" \
          "                                         AND MRNHEADER.CODE =  MRNDETAIL.MRNHEADERCODE" \
          " JOIN    FullItemKeyDecoder FIKD          ON      MRNDETAIL.ITEMTYPEAFICODE  = FIKD.ITEMTYPECODE" \
          "                                         AND     COALESCE(MrnDetail.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          "                                         AND     COALESCE(MrnDetail.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          "                                         AND     COALESCE(MrnDetail.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          "                                         AND     COALESCE(MrnDetail.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
          "                                         AND     COALESCE(MrnDetail.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
          "                                         AND     COALESCE(MrnDetail.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
          "                                         AND     COALESCE(MrnDetail.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
          "                                         AND     COALESCE(MrnDetail.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
          "                                         AND     COALESCE(MrnDetail.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
          "                                         AND     COALESCE(MrnDetail.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
          " JOIN    PRODUCT                         ON MRNDETAIL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE" \
          "                                        AND FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID" \
          " Left JOIN COSTCENTER                    ON COSTCENTER.CODE=MRNDETAIL.COSTCENTERCODE" \
          " LEFT JOIN ADDRESSGST                    ON ADDRESSGST.UniqueID = BUSINESSPARTNER.AbsUniqueId" \
          " WHERE MRNHEADER.CONFIRMEDFLAG = '0' And FINDOCUMENT.FINANCEDOCUMENTDATE between ? and ?" + Party + " " + CompanyCode + ""
    PrintingPDF(sql,LDStartDate,LDEndDate)


def PrintingXLSX(sql,LDStartDate,LDEndDate):
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
        # xlsrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        result = con.db.fetch_both(stmt)

    if result == False:
        if counter > 0:
            GRV.Exceptions = ""
            # xlsrpt.PrintStoreTotal(xlsrpt.store)
            # xlsrpt.PrintCompanyTotal(xlsrpt.divisioncode)
        elif counter == 0:
            GRV.Exceptions = "Note: Please Select Valid Credentials"
            return
    # xlsrpt.workbook.close()
    # xlsrpt.newrequest()

def PrintingPDF(sql,LDStartDate,LDEndDate):
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
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d,stdt,etdt)
        pdfrpt.d=pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d<20:
            pdfrpt.d=730
            pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A3))
            pdfrpt.c.showPage()
            pdfrpt.header(stdt,etdt,pdfrpt.divisioncode)

    if result == False:
        if counter > 0:
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.fonts(7)
            pdfrpt.printstoretotal()
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.printtotal()
            pdfrpt.storeclean()
            pdfrpt.companyclean()
            pdfrpt.cleanstore()
            GRV.Exceptions = ""
        elif counter==0:
            GRV.Exceptions="Note: Please Select Valid Credentials"
            return
    pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A3))
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    pdfrpt.d = pdfrpt.newpage()