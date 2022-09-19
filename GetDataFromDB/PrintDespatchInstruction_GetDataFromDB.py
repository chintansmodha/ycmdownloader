import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
from ProcessSelection import PrintDespatchInstruction_ProcessSelection as PDIPS
from Global_Files import Connection_String as con
from PrintPDF import PrintDespatchInstruction_PrintPDF as pdfrpt
save_name=""
counter=0

def PrintDespatchPDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "PrintDespatchInstruction" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Despatch Instruction/",
                             LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSDespatchNo = request.GET.getlist('despatchno')
    LSDespatchDate = request.GET.getlist('despatchdate')
    LSDocumentType = PDIPS.LSDocumentType
    LSDespatchNo = " AND SO.CODE in "+"("+str(LSDespatchNo)[1:-1]+")"
    LSDespatchDate = " AND SO.ORDERDATE in  " + "(" + str(LSDespatchDate)[1:-1] + ")"

    PrintPDF(LSDespatchNo,LSDespatchDate,LSDocumentType)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PrintDespatchInstructionTable.html', {'GDataPrintDespatch': PDIPS.GDataPrintDespatch,
                                                          'Exception': PDIPS.Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


def PrintPDF(LSDespatchNo,LSDespatchDate,LSDocumentType):
    sql = " SELECT   Company.LONGDESCRIPTION AS Company" \
          " , ITD.RateWithDhara As RATE" \
          " , ITD.DharaRate As RD" \
          " ,SO.CODE AS DespatchNo" \
          " ,VARCHAR_FORMAT(SO.ORDERDATE, 'DD-MM-YYYY') AS DespatchDate" \
          " ,AddressCon.TOWN As DespTo" \
          " ,AGENT.LONGDESCRIPTION AS Broker" \
          " ,AGENT.EMAILADDRESS AS BrokerEmail" \
          " ,BP.LEGALNAME1 AS BuyerName" \
          " ,COALESCE(BP.ADDRESSLINE1,'') As BUYERADDRESS1" \
          " ,COALESCE(BP.ADDRESSLINE2,'') As BUYERADDRESS2" \
          " ,COALESCE(BP.ADDRESSLINE3,'') As BUYERADDRESS3" \
          " ,COALESCE(BP.ADDRESSLINE4,'') As BUYERADDRESS4" \
          " ,COALESCE(BP.ADDRESSLINE5,'') As BUYERADDRESS5" \
          " ,COALESCE(BP.POSTALCODE,'')   AS BUYERPOSTALCODE" \
          " ,COALESCE(OP_ADG.GSTINNUMBER,'') AS BuyerGSTNO" \
          " ,COALESCE(OPIE.COMMISSIONERATE,'') AS BuyerPANNO" \
          " ,COALESCE(AddressCon.ADDRESSLINE1,'') As CONADDRESS1" \
          " ,COALESCE(AddressCon.ADDRESSLINE2,'') As CONADDRESS2" \
          " ,COALESCE(AddressCon.ADDRESSLINE3,'') As CONADDRESS3" \
          " ,COALESCE(AddressCon.ADDRESSLINE4,'') As CONADDRESS4" \
          " ,COALESCE(AddressCon.ADDRESSLINE5,'') As CONADDRESS5" \
          " ,Coalesce(AddressCon.POSTALCODE,'')   AS CONPOSTALCODE" \
          " ,AddressGSTCon.GSTINNUMBER As ConsigneeGSTNo" \
          " ,COALESCE(AddressCon.ADDRESSEE,'') AS ConsigneeName" \
          " ,Product.Longdescription || ' ' || COALESCE(QualityLevel.ShortDescription,'') as Item" \
          " ,TRIM (UGG.Code)  ||'/'||UGG.LONGDESCRIPTION As ShadeCode" \
          " ,COALESCE(SOL_LotNo.ValueString,'') AS LOTNO" \
          " ,cast(SOL.USERPRIMARYQUANTITY as decimal(18,0)) As Quantity" \
          " ,SO.LASTUPDATEUSER As AUTHUSER" \
          " ,SDRemarks.note as remarks" \
          " FROM SALESORDER                         AS SO" \
          " JOIN SalesOrderLine                     AS SOL                          ON      SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE" \
          " AND     SO.CODE = SOL.SALESORDERCODE" \
          " JOIN LogicalWarehouse                   AS LWH                          ON      SOL.WAREHOUSECODE = LWH.CODE" \
          " JOIN BusinessUnitVsCompany              AS BUC                          ON      SO.DIVISIONCODE   = BUC.DivisionCode" \
          " AND     LWH.PlantCode    = BUC.FactoryCode" \
          " JOIN FinBusinessUnit                    AS BUnit                        ON      BUC.BusinessUnitcode = BUnit.Code" \
          " AND     BUnit.GroupFlag = 0" \
          " JOIN FinBusinessUnit                    As Company                      ON      Bunit.GroupBUCode = Company.Code" \
          " AND     Company.GroupFlag = 1" \
          " JOIN OrderPartner                       AS OP                           ON      SO.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode" \
          " AND     OP.CustomerSupplierType = 1" \
          " JOIN OrderPartnerIE                     AS OPIE                         ON      OP.CustomerSupplierType = OPIE.CustomerSupplierType" \
          " AND     OP.CustomerSupplierCode = OPIE.CustomerSupplierCode" \
          " JOIN BUSINESSPARTNER                    AS BP                           ON      OP.OrderbusinessPartnerNumberId = BP.NumberID" \
          " LEFT JOIN ADDRESSGST                    AS OP_ADG                       ON      BP.ABSUNIQUEID = OP_ADG.UNIQUEID" \
          " Left JOIN Address                       As AddressCon                   ON      BP.ABSUNIQUEID = AddressCon.UNIQUEID" \
          " AND     OP.DeliveryPointCode = AddressCon.Code" \
          " Left JOIN AddressGST                    As AddressGSTCon                ON      AddressCon.ABSUNIQUEID = AddressGSTCon.UNIQUEID" \
          " LEFT JOIN AGENT                                                         ON      SO.Agent1Code = Agent.Code" \
          " JOIN FullItemKeyDecoder                 AS FIKD                         ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
          " AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
          " AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
          " AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
          " AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
          " AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
          " AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
          " JOIN Product                                                            ON      SOL.ITEMTYPEAFICODE = Product.ITEMTYPECODE" \
          " AND     FIKD.ItemUniqueId = Product.ABSUNIQUEID" \
          " JOIN QUALITYLEVEL                                                  ON      SOL.QUALITYCODE = QUALITYLEVEL.CODE" \
          " AND     SOL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE" \
          " JOIN ItemSubcodeTemplate                AS IST                          ON      SOL.ITEMTYPEAFICODE = IST.ItemTypeCode" \
          " AND     IST.GroupTypeCode In ('MB4','P09','B07')" \
          " JOIN UserGenericGroup                   AS UGG                          ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
          " AND     Case IST.POSITION" \
          " When 1 Then SOL.SubCode01" \
          " When 2 Then SOL.SubCode02" \
          " When 3 Then SOL.SubCode03" \
          " When 4 Then SOL.SubCode04" \
          " When 5 Then SOL.SubCode05" \
          " When 6 Then SOL.SubCode06" \
          " When 7 Then SOL.SubCode07" \
          " When 8 Then SOL.SubCode08" \
          " When 9 Then SOL.SubCode09" \
          " When 10 Then SOL.SubCode10 End = UGG.Code" \
          " LEFT Join AdStorage                     As SOL_LotNo                    ON      SOL.AbsUniqueId = SOL_LotNo.UniqueId" \
          " AND     SOL_LotNo.NameEntityName = 'SalesOrderLine' And SOL_LotNo.NameName = 'Lotno' And SOL_LotNo.FieldName = 'Lotno'" \
          " LEFT JOIN NOTE                          AS SDRemarks                    ON      SO.ABSUNIQUEID = SDRemarks.fatherid" \
          " Left Join (Select  ITDtl.AbsUniqueId" \
          " , Sum(Case When ITaxCode = 'INR' Then ITDtl.CalculatedValue Else 0 End) As RateWithDhara" \
          " , Sum(Case When ITaxCode = 'BSR' Then ITDtl.CalculatedValue Else 0 End) As RateWithoutDhara" \
          " , Sum(Case When ITaxCode = 'DRD' Then ITDtl.CalculatedValue Else 0 End) As DharaRate" \
          " From IndTaxDetail ITDtl, SalesOrderLine SOL" \
          " Where ITDtl.AbsUniqueId = SOL.AbsUniqueId" \
          " And ITDtl.TaxCategoryCode = 'OTH'" \
          " And ITDtl.ITaxCode In ('INR','DRD','BSR')" \
          " AND SOL.DocumentTypeType = '02'" \
          " Group By ITDtl.AbsUniqueId)AS ITD                          ON      SOL.ABSUNIQUEID = ITD.ABSUNIQUEID" \
          " WHERE SOL.DOCUMENTTYPETYPE = '"+LSDocumentType[0]+"' " +LSDespatchNo+LSDespatchDate+"" \
          " ORDER BY DespatchNo,SOL.ORDERLINE"

    stmt = con.db.prepare(con.conn, sql)
    # Explicitly bind parameters
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    # print(sql)


    while result != False:
          global counter
          counter = counter + 1

          pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, '', '')
          pdfrpt.d = pdfrpt.dvalue('', '', result,pdfrpt.divisioncode)
          result = con.db.fetch_both(stmt)

          if pdfrpt.d < 20:
                pdfrpt.d = 560
                pdfrpt.c.showPage()
                pdfrpt.header('', '', result,pdfrpt.divisioncode)
                # pdfrpt.d=pdfrpt.d-20
                # pdfrpt.itemcodes(result, pdfrpt.d)
    if result == False:

        if counter > 0:
            pdfrpt.signature('','',result,pdfrpt.d - 20)
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dvalue('', '', result,pdfrpt.divisioncode)
            pdfrpt.companyclean()
            PDIPS.Exceptions = ""
        elif counter == 0:
            PDIPS.Exceptions = "Note: No Result found according to your selected criteria"
            return

    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    counter = 0
    pdfrpt.d = pdfrpt.newpage()

