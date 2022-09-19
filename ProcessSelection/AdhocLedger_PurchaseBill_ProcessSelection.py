from datetime import datetime
import re

from django.shortcuts import render

from Global_Files import Connection_String as con

TotalGSTOnCurrentItem = 0
TotalItemAmount = 0
ItemTable = []
GDataItemGSTDetails = []
GDataOtherChargesDetail = []
resultset = []
firstresult = []
totalgst = []
ids = []
TotalGSTONALLItems = 0


def PurchaseBill(request):
    global TotalGSTOnCurrentItem
    TotalGSTOnCurrentItem = 0
    global TotalItemAmount
    TotalItemAmount = 0
    global ids
    ids = []
    global ItemTable
    ItemTable = []
    global resultset
    global firstresult
    resultset = []
    firstresult = []
    LSVchno = request.GET.getlist("vchno")
    LSVchDate = request.GET.getlist("vchdate")
    LSDocType = request.GET.getlist("doctype")
    LSYear = request.GET.getlist("year")

    Company = " FD.code='" + LSVchno[0] + "'"
    Supplier = (
        "AND FD.FINANCEDOCUMENTDATE='"
        + datetime.strptime(LSVchDate[0], "%d-%m-%Y").strftime("%Y-%m-%d")
        + "'"
    )
    BillNo = "AND FD.DOCUMENTTYPECODE='" + LSDocType[0] + "'"
    VoucherDate = "AND FD.FINANCIALYEARCODE='" + LSYear[0] + "'"

    if request.GET["CompanyCode"]:
        companycode = (
            " And FD.BUSINESSUNITCODE='" + str(request.GET["CompanyCode"]) + "'"
        )

    if request.GET["AccountCode"]:
        accountcode = " And FD.GLCODE='" + str(request.GET["AccountCode"]) + "'"

    if int(request.GET["SubAccountCode"]) != 0:
        subaccountcode = " And BP.NUMBERID='" + str(request.GET["SubAccountCode"]) + "'"

    if request.GET["year"]:
        yearcode = " And FD.FINANCIALYEARCODE='" + str(request.GET["year"]) + "'"

    if request.GET["doctype"]:
        doccode = " And FD.DOCUMENTTEMPLATECODE='" + str(request.GET["doccode"]) + "'"

    if request.GET["vchno"]:
        vchno = " And FD.CODE='" + str(request.GET["vchno"]) + "'"

    sql = (
        "Select company.LONGDESCRIPTION as Company,BP.legalname1 as Supplier"
        " ,MRNDETAIL.ABSUNIQUEID AS ID,FD.Code as Vchno,VARCHAR_FORMAT(FD.PostingDate, 'YYYY-MM-DD') As VchDate"
        ",VARCHAR_FORMAT(PI.INVOICEDATE, 'YYYY-MM-DD') AS BILLDATE"
        ",PI.CODE AS BILLNO, PI.INVOICEAMOUNT AS BILLAMOUNT"
        ",MRH.CODE as Mrnno,VARCHAR_FORMAT(MRH.MRNDATE,'YYYY-MM-DD') as mrndate, FD.DOCUMENTTEMPLATECODE as billtype"
        ",FD.TDSAPPLICABLEAMOUNT as  TDSAPPLICABLEAMOUNT,Note.Note as Narration,PRODUCT.LONGDESCRIPTION AS ITEM"
        ",GLmaster.LONGDESCRIPTION as Account,BP.legalname1 as SubAccount,cast(MRNDETAIL.INVOICEQUANTITY as decimal(18,2)) AS QUANTITY,"
        " cast(MRNDETAIL.UNITPRICE as decimal(18,2)) AS RATE,cast(MRNDETAIL.BASICVALUE as decimal(18,2)) AS BASICVALUE,"
        " COALESCE(FD.CUSTOMERREFERENCE,FD.VENDORREFERENCE) as Refno,"
        " COALESCE(FD.CUSTOMERREFERENCEDATE,FD.VENDORREFERENCEDATE) as refdate,"
        " MRH.DISPATCHSTATION as placeofsupply,FD.TDSAMOUNT as TDSAmount,FD.TDSPERCENTAGE as TDSPERCENTAGE"
        ",COALESCE(ADDRESSGST.GSTINNUMBER,ADDRESSGST.PROVISIONALGSTINNUMBER,'') as GSTNO"
        " from Findocument AS FD"
        " JOIN FinBusinessUnit as company"
        " ON      FD.BusinessUnitcode = company.Code"
        " AND company.GroupFlag = 0"
        " JOIN    PURCHASEINVOICE as PI "
        " ON  FD.PURCHASEINVOICEDIVISIONCODE=PI.DIVISIONCODE"
        " AND FD.PURINVOICEORDPRNCSMSUPTYPE=PI.ORDPRNCUSTOMERSUPPLIERTYPE"
        " AND FD.PURINVOICEORDPRNCSMSUPCODE=PI.ORDPRNCUSTOMERSUPPLIERCODE"
        " AND FD.PURCHASEINVOICECODE=PI.CODE "
        " AND FD.PURCHASEINVOICEINVOICEDATE=PI.INVOICEDATE"
        " LEFT JOIN OrderPartner AS OP "
        " ON  PI.ORDPRNCUSTOMERSUPPLIERCODE = OP.CUSTOMERSUPPLIERCODE"
        " AND PI.ORDPRNCUSTOMERSUPPLIERTYPE = OP.CUSTOMERSUPPLIERTYPE"
        " Left JOIN businesspartner AS BP "
        " ON  OP.ORDERBUSINESSPARTNERNUMBERID = BP.NUMBERID"
        " Left JOIN    MRNHEADER as MRH "
        " ON      MRH.COMPANYCODE = PI.COMPANYCODE"
        " AND MRH.DIVISIONCODE=PI.DIVISIONCODE"
        " AND MRH.ORDPRNCUSTOMERSUPPLIERTYPE=PI.ORDPRNCUSTOMERSUPPLIERTYPE"
        " AND MRH.ORDPRNCUSTOMERSUPPLIERCODE=PI.ORDPRNCUSTOMERSUPPLIERCODE"
        " AND MRH.PURCHASEINVOICECODE=PI.CODE"
        " AND MRH.PURCHASEINVOICEINVOICEDATE=PI.INVOICEDATE"
        " JOIN    MRNDETAIL       ON      MRH.COMPANYCODE = MRNDETAIL.MRNHEADERCOMPANYCODE "
        " AND MRH.DIVISIONCODE = MRNDETAIL.MRNHEADERDIVISIONCODE "
        " AND MRH.MRNPREFIXCODE = MRNDETAIL.MRNHEADERMRNPREFIXCODE "
        " AND MRH.CODE =  MRNDETAIL.MRNHEADERCODE "
        " JOIN    FullItemKeyDecoder FIKD         ON      MRNDETAIL.ITEMTYPEAFICODE  = FIKD.ITEMTYPECODE "
        "                                        AND     COALESCE(MrnDetail.SubCode01, '') = COALESCE(FIKD.SubCode01, '')"
        "                                        AND     COALESCE(MrnDetail.SubCode02, '') = COALESCE(FIKD.SubCode02, '')"
        "                                        AND     COALESCE(MrnDetail.SubCode03, '') = COALESCE(FIKD.SubCode03, '')"
        "                                        AND     COALESCE(MrnDetail.SubCode04, '') = COALESCE(FIKD.SubCode04, '')"
        "                                        AND     COALESCE(MrnDetail.SubCode05, '') = COALESCE(FIKD.SubCode05, '')"
        "                                        AND     COALESCE(MrnDetail.SubCode06, '') = COALESCE(FIKD.SubCode06, '')"
        "                                        AND     COALESCE(MrnDetail.SubCode07, '') = COALESCE(FIKD.SubCode07, '')"
        "                                        AND     COALESCE(MrnDetail.SubCode08, '') = COALESCE(FIKD.SubCode08, '')"
        "                                        AND     COALESCE(MrnDetail.SubCode09, '') = COALESCE(FIKD.SubCode09, '')"
        "                                        AND     COALESCE(MrnDetail.SubCode10, '') = COALESCE(FIKD.SubCode10, '')"
        " JOIN    PRODUCT                         ON MRNDETAIL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE"
        " AND FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID "
        " Left JOIN Note On PI.ABSUNIQUEID = Note.FatherID"
        " Left Join GLmaster On FD.GLCODE=GLMASTER.code"
        " LEFT JOIN      ADDRESSGST      ON      BP.ABSUNIQUEID=ADDRESSGST.ABSUNIQUEID"
        " WHERE FD.COMPANYCODE='100' "
        + companycode
        + subaccountcode
        + yearcode
        + doccode
        + vchno
        + ""
    )

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    resultset = result
    firstresult = result
    while result != False:
        TotalItemAmount = TotalItemAmount + float(result["BASICVALUE"])
        ids.append(result["ID"])
        ItemTable.append(result)
        result = con.db.fetch_both(stmt)
    print(ids)
    a = firstloadGST(request)
    return a


def firstloadGST(request):
    global TotalGSTOnCurrentItem
    global TotalGSTONALLItems
    TotalGSTONALLItems = 0
    TotalGSTOnCurrentItem = 0
    global TotalItemAmount
    TotalCharges = 0
    j = True
    global firstresult
    global ids
    global totalgst
    totalgst = []
    resultset = firstresult
    global GDataOtherChargesDetail
    global GDataItemGSTDetails
    GDataOtherChargesDetail = []
    GDataItemGSTDetails = []

    sql = (
        "Select TaxCategoryCode,GSTName,cast(ChargeVALUE as decimal(18,2)) as Chargevalue from "
        " (SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('IGS')"
        " AND MRNDETAIL.AbsUniqueID = '" + str(resultset["ID"]) + "'"
        " Union All"
        " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('CGS')"
        " AND MRNDETAIL.AbsUniqueID = '" + str(resultset["ID"]) + "'"
        " Union All"
        " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('SGS')"
        " AND MRNDETAIL.AbsUniqueID = '" + str(resultset["ID"]) + "'"
        " Union All"
        " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('INS')"
        " AND MRNDETAIL.AbsUniqueID = '" + str(resultset["ID"]) + "'"
        " Union All"
        " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('FRT')"
        " AND MRNDETAIL.AbsUniqueID = '" + str(resultset["ID"]) + "'"
        " Union All"
        " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('TCS')"
        " AND MRNDETAIL.AbsUniqueID = '" + str(resultset["ID"]) + "' )"
        " AS ItemGST"
    )

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result1 = con.db.fetch_both(stmt)
    while result1 != False:
        TotalCharges = TotalCharges + float(result1["CHARGEVALUE"])
        if result1["TAXCATEGORYCODE"] in ("IGS", "CGS", "SGS"):
            GDataItemGSTDetails.append(result1)
            TotalGSTOnCurrentItem = TotalGSTOnCurrentItem + float(
                result1["CHARGEVALUE"]
            )
        else:
            GDataOtherChargesDetail.append(result1)
        result1 = con.db.fetch_both(stmt)
    sql = (
        "Select TaxCategoryCode,GSTName,cast(ChargeVALUE as decimal(18,2)) as Chargevalue from "
        " (SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('IGS')"
        " AND MRNDETAIL.AbsUniqueID in (" + str(ids)[1:-1] + ")"
        " Group by ITax.TaxCategoryCode,ITax.LONGDESCRIPTION"
        " Union All"
        " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('CGS')"
        " AND MRNDETAIL.AbsUniqueID in (" + str(ids)[1:-1] + ")"
        " Group by ITax.TaxCategoryCode,ITax.LONGDESCRIPTION"
        " Union All"
        " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, sum(IndTaxDetail.CALCULATEDVALUER) as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('SGS')"
        " AND MRNDETAIL.AbsUniqueID in (" + str(ids)[1:-1] + ") "
        " Group by ITax.TaxCategoryCode,ITax.LONGDESCRIPTION"
        ")"
        " AS ItemGST"
    )
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result1 = con.db.fetch_both(stmt)
    while result1 != False:
        TotalCharges = TotalCharges + float(result1["CHARGEVALUE"])
        if result1["TAXCATEGORYCODE"] in ("IGS", "CGS", "SGS"):
            TotalGSTONALLItems = TotalGSTONALLItems + float(result1["CHARGEVALUE"])
            totalgst.append(result1)
        result1 = con.db.fetch_both(stmt)
    print(totalgst)
    return render(
        request,
        "Supplier_PurchaseBill.html",
        {
            "result": resultset,
            "ItemTable": ItemTable,
            "GDataItemGSTDetails": GDataItemGSTDetails,
            "GDataOtherChargesDetail": GDataOtherChargesDetail,
            # "ROUNDOFFVALUE": resultset["ROUNDOFFVALUE"],
            "j": j,
            "TotalCharges": TotalCharges,
            "totalgst": totalgst,
            "tottalitemamt": TotalItemAmount,
            "TotalGSTONALLItems": TotalGSTONALLItems,
            "TotalGSTOnCurrentItem": TotalGSTOnCurrentItem,
        },
    )


def ItemGST(request):
    global TotalGSTOnCurrentItem
    TotalGSTOnCurrentItem = 0
    global TotalGSTONALLItems
    TotalCharges = 0
    j = False
    global resultset
    resulin = request.GET["ID"]
    rownumber = request.GET["rownumber"]
    print(resulin)
    global GDataOtherChargesDetail
    global GDataItemGSTDetails
    global TotalItemAmount
    GDataOtherChargesDetail = []
    GDataItemGSTDetails = []
    global totalgst
    sql = (
        "Select TaxCategoryCode,GSTName,cast(ChargeVALUE as decimal(18,2)) as Chargevalue from "
        " (SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('IGS')"
        " AND MRNDETAIL.AbsUniqueID = '" + str(resulin) + "'"
        " Union All"
        " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('CGS')"
        " AND MRNDETAIL.AbsUniqueID = '" + str(resulin) + "'"
        " Union All"
        " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('SGS')"
        " AND MRNDETAIL.AbsUniqueID = '" + str(resulin) + "'"
        " Union All"
        " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('INS')"
        " AND MRNDETAIL.AbsUniqueID = '" + str(resulin) + "'"
        " Union All"
        " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('FRT')"
        " AND MRNDETAIL.AbsUniqueID = '" + str(resulin) + "'"
        " Union All"
        " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE"
        " FROM IndTaxDetail"
        " JOIN MRNDETAIL   ON INDTAXDETAIL.AbsUniqueID     = MRNDETAIL.AbsUniqueID"
        " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code"
        " WHERE IndTaxDetail.CALCULATEDVALUER <> 0"
        " AND ITax.TaxCategoryCode IN ('TCS')"
        " AND MRNDETAIL.AbsUniqueID = '" + str(resulin) + "' )"
        " AS ItemGST"
    )

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result1 = con.db.fetch_both(stmt)
    while result1 != False:
        TotalCharges = TotalCharges + float(result1["CHARGEVALUE"])
        if result1["TAXCATEGORYCODE"] in ("IGS", "CGS", "SGS"):
            TotalGSTOnCurrentItem = TotalGSTOnCurrentItem + float(
                result1["CHARGEVALUE"]
            )
            GDataItemGSTDetails.append(result1)
        else:
            GDataOtherChargesDetail.append(result1)
        result1 = con.db.fetch_both(stmt)
    print("JIGR", rownumber)
    return render(
        request,
        "Supplier_PurchaseBill.html",
        {
            "result": resultset,
            "ItemTable": ItemTable,
            "GDataItemGSTDetails": GDataItemGSTDetails,
            "GDataOtherChargesDetail": GDataOtherChargesDetail,
            # "ROUNDOFFVALUE": resultset["ROUNDOFFVALUE"],
            "j": j,
            "TotalCharges": TotalCharges,
            "rownumber": rownumber,
            "totalgst": totalgst,
            "tottalitemamt": TotalItemAmount,
            "TotalGSTONALLItems": TotalGSTONALLItems,
            "TotalGSTOnCurrentItem": TotalGSTOnCurrentItem,
        },
    )
