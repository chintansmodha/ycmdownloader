import os
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve

from FormLoad import PrintIssueSlip_FormLoad as views

from Global_Files import Connection_String as con
from PrintPDF import PrintIssueSlip_PrintPDF as pdfrpt
save_name = ""

Exceptions = ""

counter = 0

def PrintIssueSlip_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintIssueSlip" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Goods Receipt Note/",LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSNumber = request.GET.getlist('number')
    LSDate = request.GET.getlist('date')
    LSQuantity = request.GET.getlist('quantity')
    Company = ''
    Party = ''
    # print(LSNumber, LSDate)

    LSNumbers = " Stxn.DERIVATIONCODE IN " + "(" + str(LSNumber)[1:-1] + ")"
    LSDates = " AND VARCHAR_FORMAT(INTERNALDOCUMENT.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') IN  " + "(" + str(LSDate)[1:-1] + ")"
    LSQuantitys = " AND Cast(IDL.USERPRIMARYQUANTITY As Decimal(10,3)) IN " + "(" + str(LSQuantity)[1:-1] + ")"
    # print(LSNumbers)
    # print(LSGrnDate)
    # print(LSGrndate)

    PrintPDF(LSNumbers, LSDates, LSQuantity, Company, Party, LSQuantitys)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PrintIssueSlip_Table.html', {'GDataIssueSlipSummary': views.GDataIssueSlipSummary,
                                                             'Exception': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response


def PrintPDF(LSNumbers, LSDates, LSQuantity, Company, Party, LSQuantitys):
    global Exceptions
    # print(LSNumbers)

    sql = "Select   LOGICALWAREHOUSE.LONGDESCRIPTION  As Department " \
          ", Stxn.DERIVATIONCODE As IssueNo " \
          ", VARCHAR_FORMAT(Stxn.TRANSACTIONDATE, 'DD-MM-YYYY') As IssueDt " \
          ", INTERNALDOCUMENT.PROVISIONALCODE As ReqNumber " \
          ", VARCHAR_FORMAT(INTERNALDOCUMENT.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') As ReqDate " \
          ", COALESCE(IsuDept.LONGDESCRIPTION,' ') As   toDepartment " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LongDescription,'') As ItemName " \
          ", COALESCE(QualityLevel.ShortDescription, '') As Quality " \
          ", Cast(Sum(Stxn.USERPRIMARYQUANTITY) As Decimal(20,3)) As Quantity " \
          ", Cast(Coalesce(Sum(BKLELEMENTS.TOTALBOXES),0) As INT) As Boxes " \
          ", Cast(Coalesce(Sum(BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3 + BKLELEMENTS.COPSQUANTITY4 + " \
          "BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8 + " \
          "BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + " \
          "BKLELEMENTS.COPSQUANTITY13 + BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15),0) As Int) As Cops " \
          ", COALESCE(Stxn.LotCode,'')  As LotNo " \
          ", '' As BaseName " \
          "From    INTERNALDOCUMENT " \
          "join    LOGICALWAREHOUSE                On      INTERNALDOCUMENT.WAREHOUSECODE            =      LOGICALWAREHOUSE.Code " \
          "left join    LOGICALWAREHOUSE As IsuDept    On       INTERNALDOCUMENT.DESTINATIONWAREHOUSECODE  =      IsuDept.CODE " \
          "Join    INTERNALDOCUMENTLINE IDL       On       INTERNALDOCUMENT.PROVISIONALCOUNTERCODE   =  IDL.INTDOCPROVISIONALCOUNTERCODE " \
          "And      INTERNALDOCUMENT.PROVISIONALCODE          =  IDL.INTDOCUMENTPROVISIONALCODE " \
          "Join    StockTransaction  Stxn          On      INTERNALDOCUMENT.PROVISIONALCODE  =  Stxn.OrderCode " \
          "AND     INTERNALDOCUMENT.PROVISIONALCOUNTERCODE   =  Stxn.ORDERCOUNTERCODE " \
          "And     IDL.ORDERLINE = Stxn.ORDERLINE " \
          "AND     Stxn.DERIVATIONCODE is Not Null " \
          "Left Join    BKLELEMENTS                On      Stxn.CONTAINERELEMENTCODE =  BKLELEMENTS.Code " \
          "And     Stxn.CONTAINERSUBCODE01 =  BKLELEMENTS.SUBCODEKEY " \
          "join         FULLITEMKEYDECODER FIKD    ON      IDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(IDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')  " \
          "AND     COALESCE(IDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(IDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(IDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(IDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(IDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(IDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(IDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(IDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(IDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join         PRODUCT                    On      IDL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
          "Join    QualityLevel                    On      IDL.QualityCode = QualityLevel.Code " \
          "And     IDL.ItemTypeAfiCode = QualityLevel.ItemTypeCode " \
          "Left JOIN    ItemSubcodeTemplate IST         ON      IDL.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN UserGenericGroup UGG          ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then IDL.SubCode01 When 2 Then IDL.SubCode02 When 3 Then IDL.SubCode03 When 4 Then IDL.SubCode04 When 5 Then IDL.SubCode05 " \
          "When 6 Then IDL.SubCode06 When 7 Then IDL.SubCode07 When 8 Then IDL.SubCode08 When 9 Then IDL.SubCode09 When 10 Then IDL.SubCode10 End = UGG.Code " \
          "Where   "+LSNumbers+" " \
          "Group By LOGICALWAREHOUSE.LONGDESCRIPTION " \
          ", Stxn.DERIVATIONCODE " \
          ", VARCHAR_FORMAT(Stxn.TRANSACTIONDATE, 'DD-MM-YYYY') " \
          ", INTERNALDOCUMENT.PROVISIONALCODE " \
          ", VARCHAR_FORMAT(INTERNALDOCUMENT.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') " \
          ", COALESCE(IsuDept.LONGDESCRIPTION,' ') " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(UGG.LongDescription,'') " \
          ", COALESCE(QualityLevel.ShortDescription, '') " \
          ", COALESCE(Stxn.LotCode,'') " \
          "order  by IssueNo, IssueDt Desc, ReqNumber,  ReqDate,  Department, toDepartment "

    stmt = con.db.prepare(con.conn, sql)
    # Explicitly bind parameters
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, pdfrpt.i)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        # pdfrpt.c.line(0, 12, 600, 12)
        if pdfrpt.d < 30:
            pdfrpt.d = 660
            pdfrpt.c.showPage()
            pdfrpt.header(result, pdfrpt.divisioncode, pdfrpt.todepartment)
            # pdfrpt.d=pdfrpt.d-20
            # pdfrpt.itemcodes(result, pdfrpt.d)

    if result == False:
        if counter > 0:

            pdfrpt.c.line(0, pdfrpt.d, 600, pdfrpt.d)
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.c.setFont("Helvetica-Bold", 8)
            pdfrpt.c.drawString(275, pdfrpt.d, "Total : ")
            pdfrpt.c.drawAlignedString(450, pdfrpt.d, str('{0:1.0f}'.format(pdfrpt.boxtotal)))
            pdfrpt.c.drawAlignedString(508, pdfrpt.d, str('{0:1.0f}'.format(pdfrpt.copstotal)))
            pdfrpt.c.drawAlignedString(570, pdfrpt.d, str('{0:1.3f}'.format(pdfrpt.quantitytotal)))
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.c.line(0, pdfrpt.d, 600, pdfrpt.d)
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dlocalvalue()
            pdfrpt.c.drawString(30, pdfrpt.d, "Dept.Incharge")
            pdfrpt.c.drawString(400, pdfrpt.d, "Receiver's Signature")

            Exceptions = ""
            counter = 0
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria "
            return

    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    # counter = 0
    pdfrpt.d = pdfrpt.newpage()
    pdfrpt.i = pdfrpt.newserialNo()