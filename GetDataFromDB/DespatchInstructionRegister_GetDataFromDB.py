import os
from datetime import datetime
from PrintPDF import DespatchInstructionRegister_PrintPDF as pdfDIR
from Global_Files import Connection_String as con
from ProcessSelection import DespatchInstructionRegister_ProcessSelection as DIRV

counter = 0


def DespatchInstructionRegister_PrintPDF(LSCompanyUnitCode, LSParty, LDstdt, LDEndDate, LCParty, LCCompanyCode, LSDocumentType,
                               LCDocumentType, LSFileName):
    # party = str(LSParty)
    # companyunitcode = str(LSCompanyUnitCode)
    # LSPartys = '(' + party[1:-1] + ')'
    # LSCompanyUnitCodes = '(' + companyunitcode[1:-1] + ')'
    party = str(LSParty)
    companyunitcode = str(LSCompanyUnitCode)
    DocumentTypes = str(LSDocumentType)
    LSPartys = '(' + party[1:-1] + ')'
    LSCompanyUnitCodes = '(' + companyunitcode[1:-1] + ')'
    LSDocumentTypes    = '(' + DocumentTypes[1:-1] + ')'
    stdt = datetime.strptime(LDstdt, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"
    if not LCDocumentType and not LSDocumentType:
        DocumentType = "('00' , '02' , '03')"
    elif LCDocumentType:
        DocumentType = "('00' , '02' , '03')"
    elif LSDocumentType:
        DocumentType = LSDocumentTypes

    if not LCParty and not LSParty:
        Party = " "
    elif LCParty:
        Party = " "
    elif LSParty:
        Party = "AND FIKD.ITEMTYPECODE in " + str(LSPartys)

    if not LCCompanyCode and not LSCompanyUnitCode:
        CompanyCode = " "
    elif LCCompanyCode:
        CompanyCode = " "
    elif LSCompanyUnitCode:
        CompanyCode = "AND SALESORDER.DIVISIONCODE in " + str(LSCompanyUnitCodes)

    sql ="Select  Division.LongDescription As BUSINESSUNITName" \
         ", Itemtype.LongDescription As ItemType" \
         ", Salesorder.OrderDate  as OrdDate" \
         ", Salesorder.Code  as OrdNo" \
         ", BusinessPartner.LegalName1   As CustomerName" \
         ", Agent.LongDescription  as Broker" \
         ", SOL.USERPRIMARYQUANTITY As OrderQty" \
         ", IndTaxDetail.CalculatedValuerCC as rate" \
         ", Product.LongDescription As ProductName " \
         ", Product.LongDescription || '  ' || COALESCE(QualityLevel.ShortDescription,'') As ProductName " \
         ", UGG.LongDescription || '  ' || UGG.Code As ShadeName " \
         ", COALESCE(SODelivery.UsedUserPrimaryQuantity,0) As DespQty " \
         ", '' As LotNo " \
         ", SalesOrder.DocumentTypeType As DocuMentTYpe" \
         ", Case SOL.ProgressStatus When 0 Then 'Entered' When 1 Then ' Par. Used' When 2 Then 'Closed' End As ProgressStatus " \
         "From         SalesOrder " \
         "Join         Division           On      SalesOrder.DIVISIONCODE = Division.code " \
         "Join         Agent              on      SalesOrder.Agent1Code = Agent.code " \
         "join         OrderPartner       On      SalesOrder.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode " \
         "And     OrderPartner.CustomerSupplierType = 1 " \
         "join         BusinessPartner    On      OrderPartner.OrderbusinessPartnerNumberId=BusinessPartner.NumberID " \
         "join         SalesOrderLine SOL On      SalesOrder.Code = SOL.SalesOrderCode " \
         "And     SalesOrder.CounterCode = SOL.SalesOrderCounterCode " \
         "And     SalesOrder.DocumentTypeType = SOL.DocumentTypeType " \
         "join         FullItemKeyDecoder FIKD     ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
         "AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
         "AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
         "AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
         "AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
         "AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
         "AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
         "AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
         "AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
         "AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
         "AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
         "Join         Product            On      SOL.ITEMTYPEAFICODE = Product.ITEMTYPECODE " \
         "And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
         "Join         QualityLevel       On      SOL.QualityCode = QualityLevel.Code  " \
         "And     SOL.ItemTypeAfiCode = QualityLevel.ItemTypeCode " \
         "Join         ItemType           On      SOL.ITEMTYPEAFICODE = ItemType.Code " \
         "JOIN         IndTaxDETAIL       ON      SOL.AbsUniqueId = IndTaxDETAIL.ABSUNIQUEID " \
         "AND     IndTaxDetail.ITaxCode = 'INR' " \
         "JOIN         ItemSubcodeTemplate IST    ON      SOL.ITEMTYPEAFICODE = IST.ItemTypeCode " \
         "AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
         "Left JOIN    UserGenericGroup UGG       ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
         "AND     Case IST.Position When 1 Then SOL.SubCode01 When 2 Then SOL.SubCode02 When 3 Then SOL.SubCode03 When 4 Then SOL.SubCode04 When 5 Then SOL.SubCode05 " \
         "When 6 Then SOL.SubCode06 When 7 Then SOL.SubCode07 When 8 Then SOL.SubCode08 When 9 Then SOL.SubCode09 When 10 Then SOL.SubCode10 End = UGG.Code " \
         "Left Join    SalesOrderDelivery SODelivery On      SOL.SalesOrderCode = SODelivery.SalesOrderLineSalesOrderCode " \
         "And     SOL.SalesOrderCounterCode = SODelivery.SalOrdLinesALOrderCounterCode " \
         "And     SOL.OrderLine = SODelivery.SalesOrderLineOrderLine " \
         "Where   Salesorder.orderDate  between "+startdate+" And "+enddate+"" +CompanyCode+" "+Party+"  " \
         "And     Salesorder.DocumentTypeType In "+DocumentType+" " \
         "order by Division.LongDescription" \
         ", ItemType" \
         ", ordDate" \
         ", ordNo"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfDIR.textsize(pdfDIR.c, result, pdfDIR.d,stdt,etdt)
        pdfDIR.d=pdfDIR.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfDIR.d<20 :
            pdfDIR.d=745
            #pdfDIR.c.setPageSize(pdfDIR.landscape(pdfDIR.A3))
            pdfDIR.c.showPage()
            pdfDIR.header(stdt,etdt,pdfDIR.divisioncode)
            pdfDIR.c.drawAlignedString(91.25,780,pdfDIR.DocumentType[-1])

    if result == False:
        if counter > 0:

            DIRV.Exceptions = ""
            counter = 0
        elif counter==0:
            DIRV.Exceptions="Note: Please Select Valid Credentials"
            return
    #pdfDIR.workbook.close()
    # pdfDIR.c.setPageSize(pdfDIR.landscape(pdfDIR.A3))

    pdfDIR.c.showPage()
    pdfDIR.c.save()
    # url = "file:///D:/Report Development/Generated Reports/GST Register/" + LSFileName + ".pdf"
    # os.startfile(url)
    pdfDIR.newrequest()
    pdfDIR.d = pdfDIR.newpage()