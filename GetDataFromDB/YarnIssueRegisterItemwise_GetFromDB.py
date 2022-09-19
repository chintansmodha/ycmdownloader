import os
from datetime import datetime
from PrintPDF import YarnIssueRegisterItemwise_PrintPDF as pdfYIRI
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
          "And     INTERNALDOCUMENT.PROGRESSSTATUS In  " + Progress + "  " \
          "And     "+Status+" " \
          "Group By LOGICALWAREHOUSE.LONGDESCRIPTION " \
          ", COALESCE(PRODUCT.LONGDESCRIPTION || ' ' || COALESCE(UGG.LongDescription,'') || ' ' ||" \
          " COALESCE(QualityLevel.ShortDescription, ''), '') " \
          ", Case  INTERNALDOCUMENT.PROGRESSSTATUS When 0 Then 'Entered' When 1 Then 'Partly Shipped' When 2 Then 'Shipped' End " \
          ", Case INTERNALDOCUMENT.DESTINATIONTYPE  when 1 Then BPTNR.LEGALNAME1  when 2 Then BPTNR.LEGALNAME1  " \
          " when 3 Then COALESCE(IsuDept.LONGDESCRIPTION,' ') End " \
          "order  by  Department , IssuetoDepartment, ProductName "


    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfYIRI.textsize(pdfYIRI.c, result, pdfYIRI.d,stdt,etdt,Summary,IssueStatus)
        pdfYIRI.d=pdfYIRI.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfYIRI.d<20 :
            pdfYIRI.d=740
            #pdfYIRI.c.setPageSize(pdfYIRI.landscape(pdfYIRI.A3))
            pdfYIRI.c.showPage()
            pdfYIRI.header(stdt,etdt,pdfYIRI.divisioncode,Summary,IssueStatus)
            # pdfYIRI.c.drawAlignedString(91.25,780,pdfYIRI.DocumentType[-1])

    if result == False:
        if counter > 0:

            pdfYIRI.boldfonts(8)
            pdfYIRI.d = pdfYIRI.dvalue()
            pdfYIRI.d = pdfYIRI.dvalue()
            pdfYIRI.c.drawString(250, pdfYIRI.d, 'Issued To Whouse Total: ')
            pdfYIRI.c.drawAlignedString(455, pdfYIRI.d, str('{0:1.3f}'.format(pdfYIRI.IssueDepttotal)))
            pdfYIRI.c.drawAlignedString(500, pdfYIRI.d, str(pdfYIRI.Issuecops))
            pdfYIRI.c.drawAlignedString(530, pdfYIRI.d, str(pdfYIRI.Issuebox))
            pdfYIRI.d = pdfYIRI.dvalue()
            pdfYIRI.d = pdfYIRI.dvalue()
            pdfYIRI.c.drawString(250, pdfYIRI.d, 'Warehouse Total: ')
            pdfYIRI.c.drawAlignedString(455, pdfYIRI.d, str('{0:1.3f}'.format(pdfYIRI.Depttotal)))
            pdfYIRI.c.drawAlignedString(500, pdfYIRI.d, str(pdfYIRI.Deptcops))
            pdfYIRI.c.drawAlignedString(530, pdfYIRI.d, str(pdfYIRI.Deptbox))
            pdfYIRI.d = pdfYIRI.dvalue()
            pdfYIRI.d = pdfYIRI.dvalue()
            pdfYIRI.c.drawString(250, pdfYIRI.d, 'Grand Total: ')
            pdfYIRI.c.drawAlignedString(455, pdfYIRI.d, str('{0:1.3f}'.format(pdfYIRI.grandtotal)))
            pdfYIRI.c.drawAlignedString(500, pdfYIRI.d, str(pdfYIRI.grandcops))
            pdfYIRI.c.drawAlignedString(530, pdfYIRI.d, str(pdfYIRI.grandbox))
            pdfYIRI.fonts(7)

            YIRV.Exceptions = ""
            counter = 0
        elif counter==0:
            YIRV.Exceptions="Note: Please Select Valid Credentials"
            return
    #pdfYIRI.workbook.close()
    # pdfYIRI.c.setPageSize(pdfYIRI.landscape(pdfYIRI.A3))

    pdfYIRI.c.showPage()
    pdfYIRI.c.save()
    # url = "file:///D:/Report Development/Generated Reports/GST Register/" + LSFileName + ".pdf"
    # os.startfile(url)
    pdfYIRI.newrequest()
    pdfYIRI.d = pdfYIRI.newpage()