from datetime import datetime

from django.shortcuts import render
from . import MISBrokerWiseOS_ProcessSelection
from Global_Files import Connection_String as con
GDataInvoiceDetails=[]
GDataItemGSTDetails=[]
GDataOtherChargesDetail=[]
resultset=[]
firstresult=[]
from GetDataFromDB import MISBrokerWiseOS_GetDataFromDB
def InvoiceDetails(request):
    global GDataInvoiceDetails
    global GDataItemGSTDetails
    global GDataOtherChargesDetail
    global resultset
    global firstresult
    firstresult=[]
    resultset=[]
    GDataItemGSTDetails=[]
    GDataInvoiceDetails = []
    companycode = ''
    accountcode = ''
    subaccountcode = ''
    yearcode = ''
    doccode = ''
    vchno = ''
    startdate = datetime.strptime(request.GET['startdate'], "%d %B %Y")
    enddate = datetime.strptime(request.GET['enddate'], "%d %B %Y")
    if request.GET['CompanyCode']:
        companycode = " And FDL.FINDOCUMENTBUSINESSUNITCODE='" + str(request.GET['CompanyCode']) + "'"

    if request.GET['AccountCode']:
        accountcode = " And FDL.GLCODE='" + str(request.GET['AccountCode']) + "'"

    if int(request.GET['SubAccountCode']) != 0:
        subaccountcode = " And businesspartner.NUMBERID='" + str(request.GET['SubAccountCode']) + "'"

    if request.GET['year']:
        yearcode = " And FDL.FINDOCUMENTFINANCIALYEARCODE='" + str(request.GET['year']) + "'"

    if request.GET['doctype']:
        doccode = " And FDL.FINDOCDOCUMENTTEMPLATECODE='" + str(request.GET['doccode']) + "'"

    if request.GET['vchno']:
        vchno = " And FDL.FINDOCUMENTCODE='" + str(request.GET['vchno']) + "'"

    print(companycode,accountcode,yearcode,doccode,vchno)
    sql=" SELECT " \
        "COALESCE(SDL.PREVIOUSCODE,'') As ChallanNo" \
        ",COALESCE(QualityLevel.ShortDescription,'') as QLT" \
        ",CAST(SDL.USERPRIMARYQUANTITY as decimal(18,3)) As Quantity" \
        ",PIL.ABSUNIQUEID as ID" \
        ",PI.ROUNDOFFVALUE as ROUNDOFFVALUE" \
        ",CAST(ItemRate.CALCULATEDVALUE as decimal(18,2)) AS BILLRATE " \
        ",cast(ItemAmt.CALCULATEDVALUE as decimal(18,2)) ItemAmount" \
        ",CAST(PI.NETTVALUE as decimal(18,2)) AS INVAMT" \
        ",CAST(Payments.CLEAREDAMOUNT as decimal(18,2)) As OSAMT" \
        ",Product.Longdescription  as Item" \
        ",VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'YYYY-MM-DD') as Challandate" \
        ",Product.ITEMTYPECODE AS Type" \
        ",PRODUCTIE.TARIFFCODE AS HSNCD" \
        ",UGG.LongDescription AS shade" \
        ",Company.LongDescription AS Company" \
        ",BU.LongDescription AS branch" \
        ",PI.Code AS INVNO" \
        ",VARCHAR_FORMAT(PI.INVOICEDATE, 'YYYY-MM-DD') AS ISSUEDATE" \
        ",BusinessPartner.legalname1 AS Customer" \
        ",AgGrp.Longdescription AS Broker" \
        ",SD.TEMPLATECODE AS Saltype" \
        ",AD.ADDRESSEE AS Con" \
        ",0 AS LotNO" \
        ",0 AS Cops" \
        ",0 AS Boxes" \
        " From FinDocument as FD" \
        " JOIN findocumentline as FDL             on  FD.COMPANYCODE  = FDL.FINDOCUMENTCOMPANYCODE" \
        " AND FD.BUSINESSUNITCODE  = FDL.FINDOCUMENTBUSINESSUNITCODE" \
        " AND FD.FINANCIALYEARCODE = FDL.FINDOCUMENTFINANCIALYEARCODE" \
        " AND FD.DOCUMENTTEMPLATECODE  = FDL.FINDOCDOCUMENTTEMPLATECODE" \
        " AND FD.CODE = FDL.FINDOCUMENTCODE" \
        " JOIN    PlantInvoice PI                 ON FD.BUSINESSUNITCODE  = PI.FINDOCBUSINESSUNITCODE" \
        " AND FD.CODE = PI.FINDOCCODE" \
        " AND FD.FINANCIALYEARCODE = PI.FINDOCFINANCIALYEARCODE" \
        " AND FD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE" \
        " Join   PlantInvoiceLine PIL             ON PI.CODE = PIL.PLANTINVOICECODE" \
        " AND PI.DIVISIONCODE = PIL.PLANTINVOICEDIVISIONCODE" \
        " JOIN    AgentsGroupDetail AGD           ON PI.Agent1Code = AGD.AgentCode" \
        " JOIN    AgentsGroup AgGrp               ON AGD.AgentsGroupCode = AgGrp.Code" \
        " JOIN    BUSINESSUNITVSCOMPANY BC        ON PI.FACTORYCODE = BC.FACTORYCODE" \
        " JOIN    FinBusinessUnit BU              ON BC.BUSINESSUNITCODE = BU.Code" \
        " JOIN    FinBusinessUnit Company         ON BU.GroupbuCode = Company.Code" \
        " LEFT    JOIN   (Select ORIGINBUSINESSUNITCODE, ORIGINFINANCIALYEARCODE, ORIGINDOCUMENTTEMPLATECODE, ORIGINCODE," \
        " Sum(CLEAREDAMOUNT) AS CLEAREDAMOUNT From FinOpenDocumentsTransactions" \
        " Group By ORIGINBUSINESSUNITCODE, ORIGINFINANCIALYEARCODE, ORIGINDOCUMENTTEMPLATECODE, ORIGINCODE)AS Payments" \
        " ON PI.FINDOCBUSINESSUNITCODE = Payments.ORIGINBUSINESSUNITCODE" \
        " AND PI.FINDOCFINANCIALYEARCODE = Payments.ORIGINFINANCIALYEARCODE" \
        " AND PI.FINDOCTEMPLATECODE = Payments.ORIGINDOCUMENTTEMPLATECODE" \
        " AND PI.FINDOCCODE = Payments.ORIGINCODE" \
        " JOIN    SalesDocument SD                ON PI.CODE = SD.PROVISIONALCODE" \
        " AND SD.DOCUMENTTYPETYPE = '06'" \
        " JOIN SalesDocumentLine  AS SDL          ON SD.PROVISIONALCOUNTERCODE = SDL.SALDOCPROVISIONALCOUNTERCODE" \
        " AND SD.PROVISIONALCODE = SDL.SALESDOCUMENTPROVISIONALCODE" \
        " JOIN    OrderPartner AS OrderPartner    ON SD.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode" \
        " AND OrderPartner.CustomerSupplierType = 1" \
        " JOIN    BusinessPartner                 ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId" \
        " LEFT    JOIN    Address AD              ON SD.DELIVERYPOINTCODE = AD.CODE" \
        " AND BusinessPartner.NUMBERID = AD.UNIQUEID" \
        " JOIN FullItemKeyDecoder FIKD    ON      SDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE" \
        " AND     COALESCE(SDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
        " AND     COALESCE(SDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
        " AND     COALESCE(SDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
        " AND     COALESCE(SDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
        " AND     COALESCE(SDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
        " AND     COALESCE(SDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
         " AND     COALESCE(SDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
        " AND     COALESCE(SDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
        " AND     COALESCE(SDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
        " AND     COALESCE(SDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
        " JOIN Product                      ON      SDL.ITEMTYPEAFICODE = Product.ITEMTYPECODE" \
        " AND     FIKD.ItemUniqueId = Product.ABSUNIQUEID" \
        " JOIN PRODUCTIE                    ON PRODUCT.ITEMTYPECODE = PRODUCTIE.ITEMTYPECODE" \
        " AND COALESCE(PRODUCT.SubCode01, '') = COALESCE(PRODUCTIE.SubCode01, '')" \
        " AND     COALESCE(PRODUCT.SubCode02, '') = COALESCE(PRODUCTIE.SubCode02, '')" \
        " AND     COALESCE(PRODUCT.SubCode03, '') = COALESCE(PRODUCTIE.SubCode03, '')" \
        " AND     COALESCE(PRODUCT.SubCode04, '') = COALESCE(PRODUCTIE.SubCode04, '')" \
        " AND     COALESCE(PRODUCT.SubCode05, '') = COALESCE(PRODUCTIE.SubCode05, '')" \
        " AND     COALESCE(PRODUCT.SubCode06, '') = COALESCE(PRODUCTIE.SubCode06, '')" \
        " AND     COALESCE(PRODUCT.SubCode07, '') = COALESCE(PRODUCTIE.SubCode07, '')" \
        " AND     COALESCE(PRODUCT.SubCode08, '') = COALESCE(PRODUCTIE.SubCode08, '')" \
        " AND     COALESCE(PRODUCT.SubCode09, '') = COALESCE(PRODUCTIE.SubCode09, '')" \
        " AND     COALESCE(PRODUCT.SubCode10, '') = COALESCE(PRODUCTIE.SubCode10, '')" \
        " LEFT JOIN IndTaxDetail ItemAmt   ON      PIL.AbsUniqueID = ItemAmt.AbsUniqueID" \
        " And     ItemAmt.ITaxCOde In ('998','PPU')" \
        " And ItemAmt.TaxCategoryCode = 'OTH'  " \
        " Join IndTaxDetail ItemRate    On  PIL.AbsUniqueID = ItemRate.AbsUniqueID " \
        " And    ItemRate.ITaxCOde In ('INR','DNV') " \
        " And    ItemRate.TaxCategoryCode = 'OTH' " \
        " JOIN QUALITYLEVEL               ON PRODUCT.QUALITYGROUPCODE = QUALITYLEVEL.CODE" \
        " AND SDL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE" \
        " Left    JOIN ItemSubcodeTemplate IST    ON      SDL.ITEMTYPEAFICODE = IST.ItemTypeCode" \
        " AND     IST.GroupTypeCode In ('MB4','P09','B07')" \
        " JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
        " AND     CASE IST.Position When 1 Then SDL.SubCode01 When 2 Then SDL.SubCode02 When 3 Then SDL.SubCode03" \
        " When 4 Then SDL.SubCode04 When 5 Then SDL.SubCode05 When 6 Then SDL.SubCode06 When 7 Then SDL.SubCode07" \
        " When 8 Then SDL.SubCode08 When 9 Then SDL.SubCode09 When 10 Then SDL.SubCode10 End = UGG.Code     " \
        " WHERE FD.COMPANYCODE='100'"+companycode+accountcode+yearcode+doccode+vchno+""\
        " ORDER BY ChallanNo "
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    resultset=result
    firstresult=result
    while result != False:
        GDataInvoiceDetails.append(result)
        result = con.db.fetch_both(stmt)
    a = firstloadGST(request)
    return a

def firstloadGST(request):
    TotalCharges=0
    j=True
    global firstresult
    resultset =firstresult
    global GDataOtherChargesDetail
    global GDataItemGSTDetails
    GDataOtherChargesDetail = []
    GDataItemGSTDetails = []
    sql = "Select TaxCategoryCode,GSTName,cast(ChargeVALUE as decimal(18,2)) as Chargevalue from " \
          " (SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE" \
          " FROM IndTaxDetail" \
          " JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID" \
          " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code" \
          " WHERE IndTaxDetail.CALCULATEDVALUER <> 0" \
          " AND ITax.TaxCategoryCode IN ('IGS')" \
          " AND PLANTINVOICELINE.AbsUniqueID = '" + str(resultset['ID']) + "'" \
                                                                           " Union All" \
                                                                           " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE" \
                                                                           " FROM IndTaxDetail" \
                                                                           " JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID" \
                                                                           " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code" \
                                                                           " WHERE IndTaxDetail.CALCULATEDVALUER <> 0" \
                                                                           " AND ITax.TaxCategoryCode IN ('CGS')" \
                                                                           " AND PLANTINVOICELINE.AbsUniqueID = '" + str(
        resultset['ID']) + "'" \
                           " Union All" \
                           " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE" \
                           " FROM IndTaxDetail" \
                           " JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID" \
                           " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code" \
                           " WHERE IndTaxDetail.CALCULATEDVALUER <> 0" \
                           " AND ITax.TaxCategoryCode IN ('SGS')" \
                           " AND PLANTINVOICELINE.AbsUniqueID = '" + str(resultset['ID']) + "'" \
                                                                                            " Union All" \
                                                                                            " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE" \
                                                                                            " FROM IndTaxDetail" \
                                                                                            " JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID" \
                                                                                            " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code" \
                                                                                            " WHERE IndTaxDetail.CALCULATEDVALUER <> 0" \
                                                                                            " AND ITax.TaxCategoryCode IN ('INS')" \
                                                                                            " AND PLANTINVOICELINE.AbsUniqueID = '" + str(
        resultset['ID']) + "'" \
                           " Union All" \
                           " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE" \
                           " FROM IndTaxDetail" \
                           " JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID" \
                           " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code" \
                           " WHERE IndTaxDetail.CALCULATEDVALUER <> 0" \
                           " AND ITax.TaxCategoryCode IN ('FRT')" \
                           " AND PLANTINVOICELINE.AbsUniqueID = '" + str(resultset['ID']) + "'" \
                                                                                            " Union All" \
                                                                                            " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE" \
                                                                                            " FROM IndTaxDetail" \
                                                                                            " JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID" \
                                                                                            " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code" \
                                                                                            " WHERE IndTaxDetail.CALCULATEDVALUER <> 0" \
                                                                                            " AND ITax.TaxCategoryCode IN ('TCS')" \
                                                                                            " AND PLANTINVOICELINE.AbsUniqueID = '" + str(
        resultset['ID']) + "' )" \
                           " AS ItemGST"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result1 = con.db.fetch_both(stmt)
    while result1 != False:
        TotalCharges = TotalCharges + float(result1['CHARGEVALUE'])
        if result1["TAXCATEGORYCODE"] in ("IGS", "CGS", "SGS"):
            GDataItemGSTDetails.append(result1)
        else:
            GDataOtherChargesDetail.append(result1)
        result1 = con.db.fetch_both(stmt)
    return render(request, "InvoiceDetails.html", {'result': resultset, 'GDataInvoiceDetails': GDataInvoiceDetails
        , 'GDataItemGSTDetails': GDataItemGSTDetails, "GDataOtherChargesDetail": GDataOtherChargesDetail,
                                                   'ROUNDOFFVALUE': resultset['ROUNDOFFVALUE'],"j":j,"TotalCharges":TotalCharges})

def ItemGST(request):
    TotalCharges=0
    j=False
    global resultset
    global GDataOtherChargesDetail
    global GDataItemGSTDetails
    GDataOtherChargesDetail=[]
    GDataItemGSTDetails=[]
    sql = "Select TaxCategoryCode,GSTName,cast(ChargeVALUE as decimal(18,2)) as Chargevalue from " \
          " (SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE" \
          " FROM IndTaxDetail" \
          " JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID" \
          " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code" \
          " WHERE IndTaxDetail.CALCULATEDVALUER <> 0" \
          " AND ITax.TaxCategoryCode IN ('IGS')" \
          " AND PLANTINVOICELINE.AbsUniqueID = '"+str(resultset['ID'])+"'" \
          " Union All" \
          " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE" \
          " FROM IndTaxDetail" \
          " JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID" \
          " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code" \
          " WHERE IndTaxDetail.CALCULATEDVALUER <> 0" \
          " AND ITax.TaxCategoryCode IN ('CGS')" \
          " AND PLANTINVOICELINE.AbsUniqueID = '"+str(resultset['ID'])+"'" \
          " Union All" \
          " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE" \
          " FROM IndTaxDetail" \
          " JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID" \
          " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code" \
          " WHERE IndTaxDetail.CALCULATEDVALUER <> 0" \
          " AND ITax.TaxCategoryCode IN ('SGS')" \
          " AND PLANTINVOICELINE.AbsUniqueID = '"+str(resultset['ID'])+"'" \
          " Union All" \
          " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE" \
          " FROM IndTaxDetail" \
          " JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID" \
          " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code" \
          " WHERE IndTaxDetail.CALCULATEDVALUER <> 0" \
          " AND ITax.TaxCategoryCode IN ('INS')" \
          " AND PLANTINVOICELINE.AbsUniqueID = '"+str(resultset['ID'])+"'" \
          " Union All" \
          " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE" \
          " FROM IndTaxDetail" \
          " JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID" \
          " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code" \
          " WHERE IndTaxDetail.CALCULATEDVALUER <> 0" \
          " AND ITax.TaxCategoryCode IN ('FRT')" \
          " AND PLANTINVOICELINE.AbsUniqueID = '"+str(resultset['ID'])+"'" \
          " Union All" \
          " SELECT ITax.TaxCategoryCode,ITax.LONGDESCRIPTION  as GSTName, IndTaxDetail.CALCULATEDVALUER as ChargeVALUE" \
          " FROM IndTaxDetail" \
          " JOIN PLANTINVOICELINE   ON INDTAXDETAIL.AbsUniqueID     = PLANTINVOICELINE.AbsUniqueID" \
          " JOIN ITax               ON IndTaxDetail.ITaxCode        = Itax.Code" \
          " WHERE IndTaxDetail.CALCULATEDVALUER <> 0" \
          " AND ITax.TaxCategoryCode IN ('TCS')" \
          " AND PLANTINVOICELINE.AbsUniqueID = '"+str(resultset['ID'])+"' )" \
          " AS ItemGST"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result1 = con.db.fetch_both(stmt)
    while result1 != False:
        TotalCharges = TotalCharges + float(result1['CHARGEVALUE'])
        if result1["TAXCATEGORYCODE"] in ("IGS","CGS","SGS"):
            GDataItemGSTDetails.append(result1)
        else:
            GDataOtherChargesDetail.append(result1)
        result1 = con.db.fetch_both(stmt)
    return render(request, "InvoiceDetails.html", {'result': resultset, 'GDataInvoiceDetails': GDataInvoiceDetails
        ,'GDataItemGSTDetails':GDataItemGSTDetails,"GDataOtherChargesDetail":GDataOtherChargesDetail,'ROUNDOFFVALUE':resultset['ROUNDOFFVALUE'],"j":j,"TotalCharges":TotalCharges})