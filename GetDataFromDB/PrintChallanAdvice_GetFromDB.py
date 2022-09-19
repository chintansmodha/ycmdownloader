import os
from datetime import datetime
# email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# ***********
from django.http import FileResponse
from django.shortcuts import render
from django.views.static import serve

from FormLoad import PrintChallanAdvice_FormLoad as views

from Global_Files import Connection_String as con
from PrintPDF import PrintChallanAdvice_PrintPDF as pdfrpt
save_name=""

Exceptions=""

Mail = ""

counter=0


def PrintChallanAdvice_PDF(request):
    global save_nam
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintChallanAdvice" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/PrintChallanAdvice/",
                             LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSChallanno = request.GET.getlist('challanno')
    LSChallandt = request.GET.getlist('challandt')
    LSLotno = request.GET.getlist('lotno')
    LSLrno = request.GET.getlist('lrno')
    LSLrdt = request.GET.getlist('lrdt')
    LSQUANTITY = request.GET.getlist('qty')
    LSBOX = request.GET.getlist('box')
    # print(LSQUANTITY)
    Company = ''
    Party = ''
    # print(LSChallanno)

    LSChallanNo = " And SD.PROVISIONALCODE IN " + "(" + str(LSChallanno)[1:-1] + ")"
    LSChallandDt = " And VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') IN " + "(" + str(LSChallandt)[1:-1] + ")"
    LSLotNo = " And Stxn.LotCode IN " + "(" + str(LSLotno)[1:-1] + ")" + " "
    LSLrNo = ''
    LSLrDt = ''

    PrintPDF(LSChallanNo, LSChallandDt, LSLotNo, Company, Party, LSLrNo, LSLrDt)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PrintChallanAdvice_Table.html',
                      {'GDataSummary': views.GDataSummary, 'Exception':Exceptions})

    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


def PrintPDF(LSChallanNo, LSChallandDt, LSLotNo, Company, Party, LSLrNo, LSLrDt):
    global Exceptions
    sql = "select            BUnit.LONGDESCRIPTION AS CompanyName " \
          ", Plant.ADDRESSLINE1 As CompAddress " \
          ", SD.PROVISIONALCODE As ChallanNo " \
          ", VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') As ChallanDate " \
          ", COALESCE(AGENT.LONGDESCRIPTION,'') AS Agent " \
          ", BP.LEGALNAME1 As PartyNAME " \
          ", COALESCE(BP.ADDRESSLINE1, '') ||' '|| COALESCE(BP.ADDRESSLINE2, '') ||' '|| COALESCE(BP.ADDRESSLINE3, '') ||' '|| COALESCE(BP.ADDRESSLINE4,'')  " \
          "||' '|| COALESCE(BP.POSTALCODE, '') ||' '|| COALESCE(BP.TOWN, '') ||' '|| COALESCE(BP.DISTRICT, '') As PARTYADDRESS " \
          ", Stxn.LotCode As LotNO " \
          ", COALESCE(SD.EXTERNALREFERENCE,'-') As LRNO " \
          ", COALESCE(VARCHAR(SD.EXTERNALREFERENCEDATE),'-') As LRDT " \
          ", Product.Longdescription || ' ' || COALESCE(QualityLevel.ShortDescription,'') as Product " \
          " , COALESCE(UGG.Longdescription, '') As ShadeName" \
          " , CAST(Sum(BKLELEMENTS.ACTUALNETWT) As DECIMAL(10,3)) As Quantity" \
          " , COUNT(Stxn.CONTAINERELEMENTCODE) As Boxes " \
          " , COALESCE(CAST(Sum  (Case WHEN Stxn.CONTAINERELEMENTCODE = BKLELEMENTS.CODE Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3 " \
          "       + BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8 " \
          "       + BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13 " \
          "       + BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) As INT), 0) As Cops " \
          ", SDL.DLVSALORDERLINESALESORDERCODE AS ordRef " \
          "from SalesDocument As SD " \
          "join OrderPartner As OP                 on      SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode " \
          "And     OP.CustomerSupplierType = 1  " \
          "Join BusinessPartner As BP              On      OP.ORDERBUSINESSPARTNERNUMBERID = BP.NumberID " \
          "Left Join   AGENT                       ON      SD.AGENT1CODE = AGENT.CODE " \
          "LEFT JOIN ADDRESS                       ON      BP.ABSUNIQUEID = ADDRESS.UNIQUEID " \
          "AND     SD.DELIVERYPOINTCODE = ADDRESS.CODE " \
          "join SalesDocumentLine  AS SDL          on      SD.PROVISIONALCOUNTERCODE = SDL.SALDOCPROVISIONALCOUNTERCODE  " \
          "AND     SD.PROVISIONALCODE = SDL.SALESDOCUMENTPROVISIONALCODE " \
          "JOIN STOCKTRANSACTION Stxn              ON      SDL.SALESDOCUMENTPROVISIONALCODE = Stxn.ORDERCODE " \
          "AND     SDL.SALDOCPROVISIONALCOUNTERCODE = Stxn.ORDERCOUNTERCODE " \
          "AND     Stxn.TEMPLATECODE = 'S04' " \
          "AND     SDL.ITEMTYPEAFICODE = Stxn.ITEMTYPECODE " \
          "AND     COALESCE(SDL.SubCode01, '') = COALESCE(Stxn.DECOSUBCODE01, '') " \
          "AND     COALESCE(SDL.SubCode02, '') = COALESCE(Stxn.DECOSUBCODE02, '')  " \
          "AND     COALESCE(SDL.SubCode03, '') = COALESCE(Stxn.DECOSUBCODE03, '') " \
          "AND     COALESCE(SDL.SubCode04, '') = COALESCE(Stxn.DECOSUBCODE04, '')  " \
          "AND     COALESCE(SDL.SubCode05, '') = COALESCE(Stxn.DECOSUBCODE05, '')  " \
          "AND     COALESCE(SDL.SubCode06, '') = COALESCE(Stxn.DECOSUBCODE06, '')  " \
          "AND     COALESCE(SDL.SubCode07, '') = COALESCE(Stxn.DECOSUBCODE07, '')   " \
          "AND     COALESCE(SDL.SubCode08, '') = COALESCE(Stxn.DECOSUBCODE08, '')  " \
          "AND     COALESCE(SDL.SubCode09, '') = COALESCE(Stxn.DECOSUBCODE09, '')  " \
          "AND     COALESCE(SDL.SubCode10, '') = COALESCE(Stxn.DECOSUBCODE10, '') " \
          "AND     Stxn.CONTAINERITEMTYPECODE = 'CNT' " \
          "Join BKLELEMENTS                        ON      Stxn.CONTAINERELEMENTCODE = BKLELEMENTS.CODE " \
          "JOIN LOGICALWAREHOUSE                   ON      SDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE  " \
          "JOIN BusinessUnitVsCompany BUC          ON      LOGICALWAREHOUSE.PLANTCODE   = BUC.FACTORYCODE " \
          "JOIN FinBusinessUnit BUnit              ON      BUC.BusinessUnitcode = BUnit.Code " \
          "JOIN PLANT                              ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE " \
          "JOIN FinBusinessUnit Company            ON      Bunit.GroupBUCode = Company.Code " \
          "And Company.GROUPFLAG = 1 " \
          "join     FullItemKeyDecoder FIKD        ON      SDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE  " \
          "AND     COALESCE(SDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')  " \
          "AND     COALESCE(SDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')  " \
          "AND     COALESCE(SDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join         Product                    On      SDL.ITEMTYPEAFICODE = Product.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = Product.ABSUNIQUEID " \
          "Left JOIN    ItemSubcodeTemplate IST    ON      SDL.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then SDL.SUBCODE01 When 2 Then SDL.SUBCODE02 When 3 Then SDL.SUBCODE03 When 4 Then SDL.SUBCODE04 When 5 Then SDL.SUBCODE05 " \
          "When 6 Then SDL.SUBCODE06 When 7 Then SDL.SUBCODE07 When 8 Then SDL.SUBCODE08 When 9 Then SDL.SUBCODE09 When 10 Then SDL.SUBCODE10 End = UGG.Code " \
          "JOIN QUALITYLEVEL                       ON      SDL.QUALITYCODE = QUALITYLEVEL.CODE " \
          "AND     SDL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
          "Where   SD.DOCUMENTTYPETYPE='05'  AND BKLELEMENTS.ITEMTYPECODE = 'CNT' "+LSChallanNo+" "+LSChallandDt+" "+LSLotNo+" " \
          "Group By BUnit.LONGDESCRIPTION " \
          ", Plant.ADDRESSLINE1 " \
          ", VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') " \
          ", SD.PROVISIONALCODE " \
          ", COALESCE(AGENT.LONGDESCRIPTION,'') " \
          ", BP.LEGALNAME1 " \
          ", COALESCE(BP.ADDRESSLINE1, '') ||' '|| COALESCE(BP.ADDRESSLINE2, '') ||' '|| COALESCE(BP.ADDRESSLINE3, '') ||' '|| COALESCE(BP.ADDRESSLINE4, '') " \
          "||' '|| COALESCE(BP.POSTALCODE, '') ||' '|| COALESCE(BP.TOWN, '') ||' '|| COALESCE(BP.DISTRICT, '') " \
          ", Stxn.LotCode " \
          ", COALESCE(SD.EXTERNALREFERENCE,'-') " \
          ", COALESCE(VARCHAR(SD.EXTERNALREFERENCEDATE),'-') " \
          ", Product.Longdescription || ' ' || COALESCE(QualityLevel.ShortDescription,'') " \
          ", COALESCE(UGG.Longdescription, '') " \
          ", SD.PROVISIONALDOCUMENTDATE, SDL.DLVSALORDERLINESALESORDERCODE " \
          "Order by CompanyName, PartyName, SD.PROVISIONALDOCUMENTDATE Asc , ChallanNo , LotNo, Product"

    stmt = con.db.prepare(con.conn, sql)
    # Explicitly bind parameters
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        # pdfrpt.c.line(0, 12, 600, 12)
        if pdfrpt.d < 80:
            pdfrpt.c.drawCentredString(300, pdfrpt.d - 10, "Cotinue................")
            pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A5))
            pdfrpt.c.showPage()
            pdfrpt.d = 400
            pdfrpt.fonts(7)
            # pdfrpt.header(pdfrpt.divisioncode, pdfrpt.CompanyAddress)

    if result == False:
        if counter > 0:

            # pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.c.line(0, pdfrpt.d, 600, pdfrpt.d)
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.c.drawString(200, pdfrpt.d, "Total: ")
            pdfrpt.TotalPrit(pdfrpt.d)
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.c.line(0, pdfrpt.d, 600, pdfrpt.d)
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.c.drawString(10, pdfrpt.d, "Agent         :" + "       " + pdfrpt.Agent[-1])
            pdfrpt.d = pdfrpt.dlocalvalue()
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.c.drawString(10, pdfrpt.d, "Order Ref  :" + "        " + pdfrpt.OrdRef[-1])
            pdfrpt.c.drawString(400, pdfrpt.d, "For " + pdfrpt.divisioncode[-1])
            pdfrpt.d = pdfrpt.dslocal()
            pdfrpt.c.drawString(400, pdfrpt.d, "Authorised Signatory")

            Exceptions = ""
            counter = 0
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria "
            return

    pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A5))
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    pdfrpt.d = pdfrpt.newpage()

def mail(request):
    global save_nam, Mail
    Mail = ""
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintChallanAdvice" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/PrintChallanAdvice/",
                             LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSChallanno = request.GET.getlist('challanno')
    LSChallandt = request.GET.getlist('challandt')
    LSLotno = request.GET.getlist('lotno')
    LSLrno = request.GET.getlist('lrno')
    LSLrdt = request.GET.getlist('lrdt')
    LSQUANTITY = request.GET.getlist('qty')
    LSBOX = request.GET.getlist('box')
    # print(LSQUANTITY)
    Company = ''
    Party = ''
    # print(LSChallanno)

    LSChallanNo = " And SD.PROVISIONALCODE IN " + "(" + str(LSChallanno)[1:-1] + ")"
    LSChallandDt = " And VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') IN " + "(" + str(LSChallandt)[
                                                                                               1:-1] + ")"
    LSLotNo = " And Stxn.LotCode IN " + "(" + str(LSLotno)[1:-1] + ")" + " "
    LSLrNo = ''
    LSLrDt = ''

    PrintPDF(LSChallanNo, LSChallandDt, LSLotNo, Company, Party, LSLrNo, LSLrDt)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PrintChallanAdvice_Table.html',
                      {'GDataSummary': views.GDataSummary, 'Exception': Exceptions})

    FromMail = 'rm30847@gmail.com'
    password = ''
    ToMail = 'rohit50024@gmail.com'

    # isinstance of MIMEMultipart
    msg = MIMEMultipart()

    #Storing Sender
    msg['From'] = 'Rohit Mishra'
    msg['To'] = ToMail
    msg['Subject'] = 'Pdf Document'
    #Storing The Body Of mail

    body = 'body of the mail'

    #Attach file
    msg.attach(MIMEText(body,'plain'))

    pdfname = str(filepath)

    # open the file to be sent
    attachment = open(pdfname,"rb")

     # instance for MIMEBase as p-->pay_load
    p = MIMEBase('application','octet-stream', Name=pdfname)

    # To change the payload into encoded form
    p.set_payload(attachment.read())

    # encode to base64
    encoders.encode_base64(p)

    # p.add_header('Content-Disposition', 'attachment; filname = %s' % filepath)

    # attach instance 'p' to 'msg'
    msg.attach(p)

    # Create SMTP Session
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(FromMail,password)

    # Convert multipart msg to string
    text = msg.as_string()
    server.sendmail(FromMail, ToMail, text)
    server.quit()
    Mail = "Note"
    # return render(request, 'PrintChallanAdvice_Table.html',
    #               {'GDataSummary': views.GDataSummary, 'Mail': Mail})
    return render(request, 'PrintChallanAdvice.html',
                  {'GDataCompany': views.GDataCompany, 'GDataParty': views.GDataParty, 'GDataDespatch':views.GDataDespatch, 'Mail': Mail})





