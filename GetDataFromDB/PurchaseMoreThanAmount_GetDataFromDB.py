from datetime import datetime
from Global_Files import Connection_String as con
from PrintPDF import PurchaseMoreThanAmount_PrintPDF as pdfrpt

LNamount = 0


def PurchaseMoreThanAmount_GetData(
    LSCompany,
    LSItem,
    LSQuality,
    LSSupplier,
    LCCompany,
    LCItem,
    LCQuality,
    LCSupplier,
    LDStartDate,
    LDEndDate,
    LNAmount,
    LSFileName,
):
    global LNamount
    LNamount = LNAmount
    if not LCCompany and not LSCompany or LCCompany:
        LSCompany = " "
    elif LSCompany:
        LSCompany = "AND FINBUSINESSUNIT.CODE in (" + str(LSCompany)[1:-1] + ")"

    if not LCItem and not LSItem or LCItem:
        LSItem = " "
    elif LSItem:
        LSItem = "AND PRODUCT.ABSUNIQUEID in (" + str(LSItem)[1:-1] + ")"

    if not LCQuality and not LSQuality or LCItem:
        LSQuality = " "
    elif LSQuality:
        LSQuality = "AND QualityLevel.CODE in (" + str(LSQuality)[1:-1] + ")"

    if not LCSupplier and not LSSupplier or LCSupplier:
        LSSupplier = " "
    elif LSSupplier:
        LSSupplier = "AND Bisunesspartner.Numberid in (" + str(LSSupplier)[1:-1] + ")"

    stdt = datetime.strptime(LDStartDate, "%Y-%m-%d").date()
    etdt = datetime.strptime(LDEndDate, "%Y-%m-%d").date()

    sql = (
        " Select  "
        "FINBUSINESSUNIT.LONGDESCRIPTION as DIVCODE,BUSINESSPARTNER.legalname1 as SUPPLIER,SUM(PURCHASEINVOICE.INVOICEAMOUNT) AS BILLAMOUNT"
        ",Coalesce(BUSINESSPARTNER.ADDRESSLINE1,'')     "
        "|| Coalesce(','||BUSINESSPARTNER.ADDRESSLINE2,'') "
        "|| Coalesce(','||BUSINESSPARTNER.ADDRESSLINE3,'')   "
        "|| Coalesce(','||BUSINESSPARTNER.ADDRESSLINE4,'')   "
        "||','|| Coalesce(BUSINESSPARTNER.ADDRESSLINE5,'')   "
        "||','||Coalesce(BUSINESSPARTNER.TOWN,'') "
        "||','||Coalesce(BUSINESSPARTNER.DISTRICT,'')     "
        "||'-'||Coalesce(BUSINESSPARTNER.POSTALCODE,'')  as Address"
        ",Coalesce(ORDERPARTNERIE.COMMISSIONERATE,'') as PANNO"
        " FROM  PURCHASEINVOICE"
        " JOIN ORDERPARTNER ON PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE = ORDERPARTNER.CUSTOMERSUPPLIERTYPE  "
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE  "
        " JOIN ORDERPARTNERIE                    ON  PURCHASEINVOICE.COMPANYCODE  = ORDERPARTNERIE.CUSTOMERSUPPLIERCOMPANYCODE"
        " AND  PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE   = ORDERPARTNERIE.CUSTOMERSUPPLIERTYPE"
        " JOIN BUSINESSPARTNER ON ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID  "
        " JOIN    FINDOCUMENT     ON      FINDOCUMENT.COMPANYCODE=PURCHASEINVOICE.COMPANYCODE  "
        " AND FINDOCUMENT.BUSINESSUNITCODE=PURCHASEINVOICE.FINDOCBUSINESSUNITCODE  "
        " AND FINDOCUMENT.FINANCIALYEARCODE=PURCHASEINVOICE.FINDOCFINANCIALYEARCODE  "
        " AND FINDOCUMENT.DOCUMENTTEMPLATECODE=PURCHASEINVOIcE.FINDOCTEMPLATECODE  "
        " AND FINDOCUMENT.CODE=PURCHASEINVOICE.FINDOCCODE"
        " JOIN FINBUSINESSUNIT ON FINDOCUMENT.BUSINESSUNITCODE=FINBUSINESSUNIT.CODE  "
        " WHERE  FINDOCUMENT.FINANCEDOCUMENTDATE between '"
        + LDStartDate
        + "' and '"
        + LDEndDate
        + "' "
        + LSCompany
        + " "
        + LSItem
        + " "
        + LSQuality
        + " "
        + LSSupplier
        + " And PURCHASEINVOICE.INVOICEAMOUNT>="
        + str(LNamount)
        + " GROUP BY FINBUSINESSUNIT.LONGDESCRIPTION,BUSINESSPARTNER.LEGALNAME1,ORDERPARTNERIE.COMMISSIONERATE"
        ",BUSINESSPARTNER.ADDRESSLINE1,BUSINESSPARTNER.ADDRESSLINE2,BUSINESSPARTNER.ADDRESSLINE3"
        ",BUSINESSPARTNER.ADDRESSLINE4,BUSINESSPARTNER.ADDRESSLINE5,BUSINESSPARTNER.TOWN,BUSINESSPARTNER.DISTRICT,BUSINESSPARTNER.POSTALCODE"
        " ORDER BY DIVCODE,SUPPLIER"
    )
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    if result == False:
        return
    while result != False:
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
        result = con.db.fetch_both(stmt)
    pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
    pdfrpt.boldfonts(9)
    pdfrpt.c.drawString(400, pdfrpt.d, " Total : ")
    pdfrpt.c.drawAlignedString(
        570, pdfrpt.d, str("%.2f" % float(pdfrpt.CompanyAmountTotal))
    )
    pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.divisioncode)
    pdfrpt.c.drawString(400, pdfrpt.d, "Grand Total : ")
    pdfrpt.c.drawAlignedString(
        570, pdfrpt.d, str("%.2f" % float(pdfrpt.ItemQuantityTotal))
    )
    # pdfrpt.c.drawAlignedString(580, pdfrpt.d, str("%.2f" % float(pdfrpt.ItemAmountTotal)))
    # pdfrpt.ItemAmountTotal=0
    pdfrpt.ItemQuantityTotal = 0
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    # url="file:///D:/Report Development/Generated Reports/Purchase Register/"+LSFileName+".pdf"
    # os.startfile(url)
    pdfrpt.newrequest()
    pdfrpt.d = pdfrpt.newpage()
