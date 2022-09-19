from datetime import datetime
from PrintPDF import PendingDespatchInstructionDatewise_PrintPDF as pdfPDID
from Global_Files import Connection_String as con
from Global_Files import Connection_String as con
from ProcessSelection import DespatchInstructionRegister_ProcessSelection as DIRV

counter = 0


def PendingDespatchInstructionDatewise_PrintPDF(LSCompanyUnitCode, LSParty, LDstdt, LDEndDate, LCParty, LCCompanyCode, LSDocumentType,
                               LCDocumentType, LCRemarks, LSAgent,  LCAgent, LSShade, LCShade, LSparty, LCparty, LSAgentGroup,
                                                  LCAgentGroup, LSGrade, LCGrade, LSItem, LCItem   ,LSFileName):

    party = str(LSParty)
    companyunitcode = str(LSCompanyUnitCode)
    DocumentTypes = str(LSDocumentType)
    agent = str(LSAgent)
    LSPartys = '(' + party[1:-1] + ')'
    LSCompanyUnitCodes = '(' + companyunitcode[1:-1] + ')'
    LSAgents = '(' + agent[1:-1] + ')'
    LSDocumentTypes    = '(' + DocumentTypes[1:-1] + ')'
    stdt = datetime.strptime(LDstdt, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"
    # new
    shade = str(LSShade)
    prty  = str(LSparty)
    agentgroup = str(LSAgentGroup)
    grade = str(LSGrade)
    Item  = str(LSItem)
    LSShades = '(' + shade [1:-1] + ')'
    LSPrtys  = '(' + prty[1:-1] + ')'
    LSAgentsGroups = '(' + agentgroup[1:-1] + ')'
    LSgrades       = '(' + grade[1:-1] + ')'
    LSItems     =  '(' + Item[1:-1] + ')'

    if not LCDocumentType and not LSDocumentType:
        DocumentType = "('00' , '02' , '03')"
    elif LCDocumentType:
        DocumentType = "('00' , '02' , '03')"
    elif LSDocumentType:
        DocumentType = LSDocumentTypes

    if not LCParty and not LSParty:
        Itemtype = " "
    elif LCParty:
        Itemtype = " "
    elif LSParty:
        # Party = "AND FULLITEMKEYDECODER.ITEMTYPECODE in " + str(LSPartys)
        Itemtype = "AND ITEMTYPE.CODE in " + str(LSPartys)

    if not LCCompanyCode and not LSCompanyUnitCode:
        CompanyCode = " "
    elif LCCompanyCode:
        CompanyCode = " "
    elif LSCompanyUnitCode:
        CompanyCode = "AND SALESORDER.DIVISIONCODE in " + str(LSCompanyUnitCodes)

    if not LCAgent and not LSAgent:
        Agent = " "
    elif LCAgent:
        Agent = " "
    elif LSAgent:
        Agent = "AND AGENT.CODE in " + str(LSAgents)

    if not LCShade and not LSShade:
        Shade = " "
    elif LCShade:
        Shade = " "
    elif LSShade:
        Shade = "AND UGG.LONGDESCRIPTION in " + str(LSShades)

    if not LCparty and not LSparty:
        Party = " "
    elif LCparty:
        Party = " "
    elif LSparty:
        Party = "AND BUSINESSPARTNER.LEGALNAME1 in " + str(LSPrtys)

    if not LCAgentGroup and not LSAgentGroup:
        AgentGroup = " "
    elif LCAgentGroup:
        AgentGroup = " "
    elif LSAgentGroup:
        AgentGroup = "AND AGENTSGROUP.CODE in " + str(LSAgentsGroups)

    if not LCGrade and not LSGrade:
        Grade = " "
    elif LCGrade:
        Grade = " "
    elif LSGrade:
        Grade = "AND QUALITYLEVEL.LONGDESCRIPTION in " + str(LSgrades)

    if not LCItem and not LSItem:
        Items = " "
    elif LCItem:
        Items = " "
    elif LSItem:
        Items = "AND PRODUCT.LONGDESCRIPTION in " + str(LSItems)

    sql ="Select  Division.LongDescription As BUSINESSUNITName" \
         ", Salesorder.OrderDate  as OrdDate" \
         ", Salesorder.Code  as OrdNo" \
         ", BusinessPartner.LegalName1   As CustomerName" \
         ", Agent.LongDescription  as Broker" \
         ", SOL.USERPRIMARYQUANTITY As OrderQty" \
         ", SOL.UserPrimaryQuantity - COALESCE(SODelivery.UsedUserPrimaryQuantity,0) As PendingQty" \
         ", IndTaxDetail.CalculatedValuerCC as rate" \
         ", Product.LongDescription || '  ' || COALESCE(QualityLevel.ShortDescription,'') As ProductName " \
         ", UGG.LongDescription || '-' || UGG.Code As ShadeName" \
         ", COALESCE(TransportZone.LongDescription,'') As DespTo" \
         ", COALESCE(NOTE.Note,'')  As Remark" \
         ", COALESCE(SalesOrder.EXTERNALREFERENCE,'') As Reference" \
         ", '' As LotNo " \
         "From         SalesOrder " \
         "Join         Division           On      SalesOrder.DIVISIONCODE = Division.code " \
         "Join         Agent              on      SalesOrder.Agent1Code = Agent.code " \
         "join         AgentsGroupDetail  On      Agent.Code = AgentsGroupDetail.AgentCode " \
         "Join         AgentsGroup        On      AgentsGroupDetail.AgentsGroupCode = AgentsGroup.code " \
         "join         OrderPartner       On      SalesOrder.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode " \
         "And     OrderPartner.CustomerSupplierType = 1 " \
         "join         BusinessPartner    On      OrderPartner.OrderbusinessPartnerNumberId=BusinessPartner.NumberID " \
         "left Join         Address            On      BusinessPartner.AbsUniqueId = Address.UniqueId " \
         "And      SalesOrder.DeliveryPointCode = Address.Code " \
         "Left Join         TransportZone      ON      Address.TransportZoneCode = TransportZone.Code " \
         "left join         Note               On      SalesOrder.AbsUniqueId = Note.FATHERID " \
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
         "Join         ItemType           On      SOL.ITEMTYPEAFICODE = ItemType.Code " \
         "Join         QualityLevel       On      SOL.QualityCode = QualityLevel.Code " \
         "And     SOL.ItemTypeAfiCode = QualityLevel.ItemTypeCode " \
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
         "Where   Salesorder.orderDate  between "+startdate+" And "+enddate+" "+CompanyCode+" "+Itemtype+" "+Agent+" "+AgentGroup+" "+Grade+" "+Shade+" "+Party+" "+Items+" " \
         "And     Salesorder.DocumentTypeType In "+DocumentType+" " \
         "And     SOL.UserPrimaryQuantity - COALESCE(SODelivery.UsedUserPrimaryQuantity,0) > 0 " \
         "order by Division.LongDescription, ordDate, ordNo"

    # "+Agent+" "+Shade+" "+Party+" "+AgentGroup+" "+Grade+"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1
        # print(LSItems)

        pdfPDID.textsize(pdfPDID.c, result, pdfPDID.d,stdt,etdt,LCRemarks)
        pdfPDID.d=pdfPDID.dvalue()
        result = con.db.fetch_both(stmt)

        if LCRemarks == ['1']:
            if pdfPDID.d<50 :
                pdfPDID.d=745
                pdfPDID.c.showPage()
                pdfPDID.header(stdt,etdt,pdfPDID.divisioncode)
                pdfPDID.fonts(8)
        else:
            if pdfPDID.d<40 :
                pdfPDID.d=745
                pdfPDID.c.showPage()
                pdfPDID.header(stdt,etdt,pdfPDID.divisioncode)
                pdfPDID.fonts(8)

    if result == False:
        if counter > 0:
            pdfPDID.d = pdfPDID.dvalue()
            pdfPDID.fonts(8)
            if LCRemarks == ['1']:
                if pdfPDID.Remark == '':
                    pdfPDID.c.drawString(19, pdfPDID.d, "Remarks :")
                else:
                    pdfPDID.c.drawString(19, pdfPDID.d, pdfPDID.Remark)
                pdfPDID.c.drawAlignedString(465, pdfPDID.d,str(pdfPDID.format_number(float(pdfPDID.Broker_Total), locale='en_IN')))
                pdfPDID.c.drawAlignedString(580, pdfPDID.d,str(pdfPDID.format_number(float(pdfPDID.BrokerBAL_Total), locale='en_IN')))
                pdfPDID.dvalue()
            # pdfPDID.c.drawString(250, pdfPDID.d, "Broker Total: ")
            # pdfPDID.c.drawAlignedString(465, pdfPDID.d, str(pdfPDID.format_number(float(pdfPDID.Broker_Total), locale='en_IN')))
            # pdfPDID.c.drawAlignedString(580, pdfPDID.d, str(pdfPDID.format_number(float(pdfPDID.BrokerBAL_Total), locale='en_IN')))
            pdfPDID.dvalue()
            pdfPDID.c.drawString(250, pdfPDID.d, "Grand Total: ")
            pdfPDID.c.drawAlignedString(465, pdfPDID.d,str(pdfPDID.format_number(float(pdfPDID.Grand_Total), locale='en_IN')))
            pdfPDID.c.drawAlignedString(580, pdfPDID.d,str(pdfPDID.format_number(float(pdfPDID.GrandBal_Total), locale='en_IN')))

            DIRV.Exceptions = ""
            counter = 0
        elif counter==0:
            DIRV.Exceptions="Note: Please Select Valid Credentials"
            return
    #pdfPDID.workbook.close()
    # pdfPDID.c.setPageSize(pdfPDID.landscape(pdfPDID.A3))

    pdfPDID.c.showPage()
    pdfPDID.c.save()
    # url = "file:///D:/Report Development/Generated Reports/GST Register/" + LSFileName + ".pdf"
    # os.startfile(url)
    pdfPDID.newrequest()
    pdfPDID.d = pdfPDID.newpage()