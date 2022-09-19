import os
from datetime import datetime
from PrintPDF import YarnIssueRegisterItemLotwise_PrintPDF as pdfYIRIL
from Global_Files import Connection_String as con
from ProcessSelection import YarnIssueRegister_ProcessSelection as YIRV

counter = 0

Summary = " "
IssueStatus = " "
Progress = ''
def YarnIssueRegister_PrintPDF(LSDepartmentCode, LSIssue2DepartmentCode, LSSupplierCode, LCIssue2DepartmentCode, LCSupplierCode,LCDepartmentCode,
                               LCSummary, LDStartDate, LDEndDate, LCStatus, LSPROGRESStype, LCPROGRESStype, LSDesttype, LCDesttype):

    global Summary , IssueStatus
    Issues = str(LCStatus)
    IssueStatus = Issues[2:-2]
    Details = str(LCSummary)
    Summary = Details[2:-2]
    if LCStatus == ['Confirmed Issues Only']:
        Status = "IDL.ReceivingStatus In (2)"

    elif LCStatus == ['Pending Issues Only']:
        Status = "IDL.ReceivingStatus In (0,1)"

    else:
        Status = "IDL.ReceivingStatus In (0,1,2)"

    Departmentcode = str(LSDepartmentCode)
    Issue2DepartmentCode = str(LSIssue2DepartmentCode)
    SupplierCode = str(LSSupplierCode)
    DestinationType = str(LSDesttype)
    ProgressType = str(LSPROGRESStype)
    LSDepartmentCodes = '(' + Departmentcode[1:-1] + ')'
    LSIssue2DepartmentCodes = '(' + Issue2DepartmentCode[1:-1] + ')'
    LSSupplierCodes = '(' + SupplierCode[1:-1] + ')'
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"

    if not LSDesttype and not LCDesttype:
        Desttype = "(1,2,3)"
    elif LCDesttype:
        Desttype = "(1,2,3)"
    elif LSDesttype:
        Desttype = '(' + DestinationType[1:-1] + ')'

    if not LSPROGRESStype and not LCPROGRESStype:
        Progress = "(0,1,2)"
    elif LCPROGRESStype:
        Progress = "(0,1,2)"
    elif LSPROGRESStype:
        Progress = '(' + ProgressType[1:-1] + ')'

    if not LCDepartmentCode and not LSDepartmentCode:
        Departmentcode = " "
    elif LCDepartmentCode:
        Departmentcode = " "
    elif LSDepartmentCode:
        Departmentcode = "AND INTERNALDOCUMENT.WAREHOUSECODE in " + str(LSDepartmentCodes)

    if not LCIssue2DepartmentCode and not LSIssue2DepartmentCode:
        Destinationcode = " "
    elif LCIssue2DepartmentCode:
        Destinationcode = " "
    elif LSIssue2DepartmentCode:
        Destinationcode = "AND INTERNALDOCUMENT.DESTINATIONWAREHOUSECODE in " + str(LSIssue2DepartmentCodes)

    if not LCSupplierCode and not LSSupplierCode:
        Suppliercode = " "
    elif LCSupplierCode:
        Suppliercode = " "
    elif LSSupplierCode:
        Suppliercode = "AND ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID in " + str(LSSupplierCodes)

    sql = "Select  LOGICALWAREHOUSE.LONGDESCRIPTION  As Department " \
          ", COALESCE(PRODUCT.LONGDESCRIPTION || ' ' || COALESCE(UGG.LongDescription,'') || ' ' ||" \
          " COALESCE(QualityLevel.ShortDescription, ''), '') As ProductName " \
          ", Case  INTERNALDOCUMENT.PROGRESSSTATUS When 0 Then 'Entered' When 1 Then 'Partly Shipped' When 2 Then 'Shipped' End As STATUS " \
          ", Case INTERNALDOCUMENT.DESTINATIONTYPE  when 1 Then BPTNR.LEGALNAME1  when 2 Then BPTNR.LEGALNAME1  " \
          " when 3 Then COALESCE(IsuDept.LONGDESCRIPTION,' ') End As IssuetoDepartment " \
          ", Cast(Sum(Stxn.USERPRIMARYQUANTITY) As Decimal(10,3)) As Quantity " \
          ", Cast(Sum(Coalesce(BKLELEMENTS.TOTALBOXES,0)) As INT) As Boxes " \
          ", Cast(Sum(Coalesce((BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3 + BKLELEMENTS.COPSQUANTITY4 + " \
          "BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8 + " \
          "BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + " \
          "BKLELEMENTS.COPSQUANTITY13 + BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15),0)) As Int) As Cops " \
          ", COALESCE(Stxn.LotCode,'') As LotNo " \
          "From    INTERNALDOCUMENT " \
          "Join    INTERNALDOCUMENTLINE IDL  On       INTERNALDOCUMENT.PROVISIONALCOUNTERCODE   =  IDL.INTDOCPROVISIONALCOUNTERCODE " \
          "And      INTERNALDOCUMENT.PROVISIONALCODE          =  IDL.INTDOCUMENTPROVISIONALCODE " \
          "join    LOGICALWAREHOUSE    On      INTERNALDOCUMENT.WAREHOUSECODE            =      LOGICALWAREHOUSE.CODE " \
          "left join    LOGICALWAREHOUSE As IsuDept    On       INTERNALDOCUMENT.DESTINATIONWAREHOUSECODE  =      IsuDept.CODE " \
          "Left Join    ORDERPARTNER         On        INTERNALDOCUMENT.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE " \
          "And  Case  INTERNALDOCUMENT.DESTINATIONTYPE When 1 Then ORDERPARTNER.CUSTOMERSUPPLIERTYPE =1 When 2 Then ORDERPARTNER.CUSTOMERSUPPLIERTYPE =2 When 3 Then ORDERPARTNER.CUSTOMERSUPPLIERTYPE =2 End " \
          "Left Join    BUSINESSPARTNER  BPTNR    On        ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BPTNR.NUMBERID " \
          " Join    StockTransaction  Stxn          On      IDL.INTDOCUMENTPROVISIONALCODE  =  Stxn.OrderCode " \
          "AND     IDL.INTDOCPROVISIONALCOUNTERCODE   =  Stxn.ORDERCOUNTERCODE " \
          "And     IDL.ORDERLINE = Stxn.ORDERLINE " \
          "AND     Stxn.DERIVATIONCODE is Not Null " \
          "Left Join    BKLELEMENTS                On      Stxn.CONTAINERELEMENTCODE =  BKLELEMENTS.Code " \
          "And     Stxn.CONTAINERSUBCODE01 =  BKLELEMENTS.SUBCODEKEY   " \
          "join         FULLITEMKEYDECODER FIKD     ON      IDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(IDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(IDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(IDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(IDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(IDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(IDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(IDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(IDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(IDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(IDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join         PRODUCT            On      IDL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
          "Join    QualityLevel              On      IDL.QualityCode = QualityLevel.Code " \
          "And     IDL.ItemTypeAfiCode = QualityLevel.ItemTypeCode " \
          "LEFT JOIN    ItemSubcodeTemplate IST    ON      IDL.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then IDL.SubCode01 When 2 Then IDL.SubCode02 When 3 Then IDL.SubCode03 When 4 Then IDL.SubCode04 When 5 Then IDL.SubCode05 " \
          "When 6 Then IDL.SubCode06 When 7 Then IDL.SubCode07 When 8 Then IDL.SubCode08 When 9 Then IDL.SubCode09 When 10 Then IDL.SubCode10 End = UGG.Code " \
          "Where   INTERNALDOCUMENT.PROVISIONALDOCUMENTDATE  between      " + startdate + "     and     " + enddate + " " + Departmentcode + " " + Destinationcode + " " + Suppliercode + " " \
          "And     INTERNALDOCUMENT.DESTINATIONTYPE In " + Desttype + " " \
          "And     "+Status+" " \
          "And     INTERNALDOCUMENT.PROGRESSSTATUS In  " + Progress + " " \
          "Group By LOGICALWAREHOUSE.LONGDESCRIPTION " \
          ", COALESCE(PRODUCT.LONGDESCRIPTION || ' ' || COALESCE(UGG.LongDescription,'') || ' ' ||" \
          " COALESCE(QualityLevel.ShortDescription, ''), '') " \
          ", Case  INTERNALDOCUMENT.PROGRESSSTATUS When 0 Then 'Entered' When 1 Then 'Partly Shipped' When 2 Then 'Shipped' End " \
          ", Case INTERNALDOCUMENT.DESTINATIONTYPE  when 1 Then BPTNR.LEGALNAME1  when 2 Then BPTNR.LEGALNAME1  " \
          " when 3 Then COALESCE(IsuDept.LONGDESCRIPTION,' ') End " \
          ", COALESCE(Stxn.LotCode,'') " \
          "order  by  Department, IssuetoDepartment, ProductName, LotNo"


    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfYIRIL.textsize(pdfYIRIL.c, result, pdfYIRIL.d,stdt,etdt,Summary,IssueStatus)
        pdfYIRIL.d = pdfYIRIL.dvalue(stdt, etdt, pdfYIRIL.divisioncode, Summary, IssueStatus)
        result = con.db.fetch_both(stmt)

        # if pdfYIRIL.d<40 :
        #     pdfYIRIL.d=740
        #     #pdfYIRIL.c.setPageSize(pdfYIRIL.landscape(pdfYIRIL.A3))
        #     pdfYIRIL.c.showPage()
        #     pdfYIRIL.header(stdt,etdt,pdfYIRIL.divisioncode,Summary,IssueStatus)
        #     pdfYIRIL.fonts(7)
            # pdfYIRIL.c.drawAlignedString(91.25,780,pdfYIRIL.DocumentType[-1])

    if result == False:
        if counter > 0:

            pdfYIRIL.d = pdfYIRIL.dvalue(stdt, etdt, pdfYIRIL.divisioncode, Summary, IssueStatus)
            pdfYIRIL.boldfonts(8)
            if pdfYIRIL.count > 1:
                pdfYIRIL.c.drawString(250, pdfYIRIL.d, 'Item Total: ')
                pdfYIRIL.c.drawAlignedString(385, pdfYIRIL.d, str('{0:1.3f}'.format(pdfYIRIL.itemtotal)))
                pdfYIRIL.c.drawAlignedString(452, pdfYIRIL.d, str(pdfYIRIL.itemcops))
                pdfYIRIL.c.drawAlignedString(512, pdfYIRIL.d, str(pdfYIRIL.itembox))
                pdfYIRIL.d = pdfYIRIL.dvalue(stdt, etdt, pdfYIRIL.divisioncode, Summary, IssueStatus)
                pdfYIRIL.d = pdfYIRIL.dvalue(stdt, etdt, pdfYIRIL.divisioncode, Summary, IssueStatus)
                pdfYIRIL.count = 0
            pdfYIRIL.c.drawString(250, pdfYIRIL.d, 'Issued To Whouse Total: ')
            pdfYIRIL.c.drawAlignedString(385, pdfYIRIL.d, str('{0:1.3f}'.format(pdfYIRIL.issuedepttotal)))
            pdfYIRIL.c.drawAlignedString(452, pdfYIRIL.d, str(pdfYIRIL.issuecops))
            pdfYIRIL.c.drawAlignedString(512, pdfYIRIL.d, str(pdfYIRIL.issuebox))
            pdfYIRIL.d = pdfYIRIL.dvalue(stdt, etdt, pdfYIRIL.divisioncode, Summary, IssueStatus)
            pdfYIRIL.d = pdfYIRIL.dvalue(stdt, etdt, pdfYIRIL.divisioncode, Summary, IssueStatus)
            pdfYIRIL.c.drawString(250, pdfYIRIL.d, 'Warehouse Total: ')
            pdfYIRIL.c.drawAlignedString(385, pdfYIRIL.d, str('{0:1.3f}'.format(pdfYIRIL.depttotal)))
            pdfYIRIL.c.drawAlignedString(452, pdfYIRIL.d, str(pdfYIRIL.deptcops))
            pdfYIRIL.c.drawAlignedString(512, pdfYIRIL.d, str(pdfYIRIL.deptbox))
            pdfYIRIL.d = pdfYIRIL.dvalue(stdt, etdt, pdfYIRIL.divisioncode, Summary, IssueStatus)
            pdfYIRIL.d = pdfYIRIL.dvalue(stdt, etdt, pdfYIRIL.divisioncode, Summary, IssueStatus)
            pdfYIRIL.c.drawString(250, pdfYIRIL.d, 'Grand Total: ')
            pdfYIRIL.c.drawAlignedString(385, pdfYIRIL.d, str('{0:1.3f}'.format(pdfYIRIL.grandtotal)))
            pdfYIRIL.c.drawAlignedString(452, pdfYIRIL.d, str(pdfYIRIL.grandcops))
            pdfYIRIL.c.drawAlignedString(512, pdfYIRIL.d, str(pdfYIRIL.grandbox))
            pdfYIRIL.fonts(7)

            YIRV.Exceptions = ""
            counter = 0
        elif counter==0:
            YIRV.Exceptions="Note: Please Select Valid Credentials"
            return
    #pdfYIRIL.workbook.close()
    # pdfYIRIL.c.setPageSize(pdfYIRIL.landscape(pdfYIRIL.A3))

    pdfYIRIL.c.showPage()
    pdfYIRIL.c.save()
    # url = "file:///D:/Report Development/Generated Reports/GST Register/" + LSFileName + ".pdf"
    # os.startfile(url)
    pdfYIRIL.newrequest()
    pdfYIRIL.d = pdfYIRIL.newpage()
    pdfYIRIL.itemlineCount = 0
    pdfYIRIL.count = 0
