from PrintPDF import PurchaseRegister_ChargeSummary_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
import os
from datetime import datetime
from ProcessSelection import PurchaseRegister_ProcessSelection as PRV
counter=0
def PurchaseRegister_ChargeSummary_PrintPDF(LSCompanyUnitCode, LSItemTypeCode, LDStartDate, LDEndDate, LSFileName,  LCItemTypeCode, LCCompanyCode, LSReportType):
    itemcode=str(LSItemTypeCode)
    companyunitcode=str(LSCompanyUnitCode)
    LSItemTypeCodes = '(' + itemcode[1:-1] + ')'
    LSCompanyUnitCodes='('+companyunitcode[1:-1]+')'

    if not LCItemTypeCode and not LSItemTypeCode:
        ItemCode=" "
    elif LCItemTypeCode:
        ItemCode=" "
    elif LSItemTypeCode:
        ItemCode = "AND MRNDETAIL.ITEMTYPEAFICODE in " + str(LSItemTypeCodes)

    if not LCCompanyCode and not LSCompanyUnitCode:
        CompanyCode=" "
    elif LCCompanyCode:
        CompanyCode=" "
    elif LSCompanyUnitCode:
        CompanyCode="AND MRNHEADER.DIVISIONCODE in "+str(LSCompanyUnitCodes)

    sql=" Select  DIVISION.LONGDESCRIPTION AS DIVCODE" \
        ",ITAX.LONGDESCRIPTION AS CHARGENAME" \
        ",SUM(INDTAXDETAIL.CALCULATEDVALUE) AS CHARGEAMOUNT" \
        " FROM MRNHEADER JOIN    DIVISION        ON      MRNHEADER.DIVISIONCODE = DIVISION.CODE" \
        " JOIN    PURCHASEINVOICE ON      PURCHASEINVOICE.COMPANYCODE=MRNHEADER.COMPANYCODE" \
        " AND PURCHASEINVOICE.DIVISIONCODE=MRNHEADER.DIVISIONCODE" \
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERTYPE" \
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE" \
        " AND PURCHASEINVOICE.CODE=MRNHEADER.PURCHASEINVOICECODE" \
        " AND PURCHASEINVOICE.INVOICEDATE= MRNHEADER.PURCHASEINVOICEINVOICEDATE" \
        " JOIN ORDERPARTNER ON PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE = ORDERPARTNER.CUSTOMERSUPPLIERTYPE" \
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE" \
        " JOIN BUSINESSPARTNER ON ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID" \
        " JOIN    FINDOCUMENT     ON      FINDOCUMENT.COMPANYCODE=PURCHASEINVOICE.COMPANYCODE" \
        " AND FINDOCUMENT.BUSINESSUNITCODE=PURCHASEINVOICE.FINDOCBUSINESSUNITCODE" \
        " AND FINDOCUMENT.FINANCIALYEARCODE=PURCHASEINVOICE.FINDOCFINANCIALYEARCODE" \
        " AND FINDOCUMENT.DOCUMENTTEMPLATECODE=PURCHASEINVOIcE.FINDOCTEMPLATECODE" \
        " AND FINDOCUMENT.CODE=PURCHASEINVOICE.FINDOCCODE" \
        " JOIN    MRNDETAIL       ON      MRNHEADER.COMPANYCODE = MRNDETAIL.MRNHEADERCOMPANYCODE" \
        " AND MRNHEADER.DIVISIONCODE = MRNDETAIL.MRNHEADERDIVISIONCODE" \
        " AND MRNHEADER.MRNPREFIXCODE = MRNDETAIL.MRNHEADERMRNPREFIXCODE" \
        " AND MRNHEADER.CODE =  MRNDETAIL.MRNHEADERCODE" \
        " JOIN    FullItemKeyDecoder FIKD         ON      MRNDETAIL.ITEMTYPEAFICODE  = FIKD.ITEMTYPECODE" \
        " AND     COALESCE(MrnDetail.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
        " AND     COALESCE(MrnDetail.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
        " AND     COALESCE(MrnDetail.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
        " AND     COALESCE(MrnDetail.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
        " AND     COALESCE(MrnDetail.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
        " AND     COALESCE(MrnDetail.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
        " AND     COALESCE(MrnDetail.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
        " AND     COALESCE(MrnDetail.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
        " AND     COALESCE(MrnDetail.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
        " AND     COALESCE(MrnDetail.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
        " JOIN    PRODUCT                 ON MRNDETAIL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE" \
        " AND FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID" \
        " JOIN    INDTAXDETAIL            ON      MRNDETAIL.ABSUNIQUEID = INDTAXDETAIL.ABSUNIQUEID" \
        " AND     INDTAXDETAIL.TAXCATEGORYCODE <> 'OTH'" \
        " AND     INDTAXDETAIL.CALCULATEDVALUE <> 0" \
        " join ITAX ON INDTAXDETAIL.ITAXCODE = ITAX.CODE                                     " \
        " WHERE MRNHEADER.CONFIRMEDFLAG = '0' And FINDOCUMENT.FINANCEDOCUMENTDATE BETWEEN ? and ? " + ItemCode + " " + CompanyCode + " " \
        " GROUP BY DIVISION.LONGDESCRIPTION,ITAX.LONGDESCRIPTION"\
        " ORDER BY DIVISION.LONGDESCRIPTION,ITAX.LONGDESCRIPTION "

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
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 20:
            pdfrpt.d = 730
            pdfrpt.c.showPage()
            pdfrpt.header(stdt, etdt, pdfrpt.divisioncode)

    if result == False:
        global Exceptions
        if counter>0:
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(7)
            pdfrpt.c.drawString(10, pdfrpt.d, str(pdfrpt.divisioncode[-2]) + " TOTAL : ")
            pdfrpt.c.drawAlignedString(570, pdfrpt.d, str("%.2f" % float(pdfrpt.CompanyAmountTotal)))
            pdfrpt.companyclean()
            PRV.Exceptions = ""
        elif counter == 0:
            PRV.Exceptions = "Note: Please Select Valid Credentials"
            return

    pdfrpt.c.showPage()
    pdfrpt.c.save()
    # url = "file:///D:/Report Development/Generated Reports/Purchase Register - Charge Summary/" + LSFileName + ".pdf"
    # os.startfile(url)
    pdfrpt.newrequest()
    pdfrpt.d = pdfrpt.newpage()