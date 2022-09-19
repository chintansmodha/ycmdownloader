from datetime import datetime
from PrintPDF import BankCashStatement_CS_PrintPDF as pdfCSrpt
from Global_Files import Connection_String as con
from ProcessSelection import BankCashStatement_ProcessSelection as BCSV

counter = 0

def BankCashStatement_CS_PrintPDF(LSCompanyUnitCode, LSParty, LDstdt, LDEndDate, LCParty, LCCompanyCode, LSConsolidate,
                               LSACSummary, LSFileName):
    # party = str(LSParty)
    # companyunitcode = str(LSCompanyUnitCode)
    # LSPartys = '(' + party[1:-1] + ')'
    # LSCompanyUnitCodes = '(' + companyunitcode[1:-1] + ')'
    party = str(LSParty)
    companyunitcode = str(LSCompanyUnitCode)
    LSPartys = '(' + party[1:-1] + ')'
    LSCompanyUnitCodes = '(' + companyunitcode[1:-1] + ')'
    stdt = datetime.strptime(LDstdt, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"
    if not LCParty and not LSParty:
        Party = " "
    elif LCParty:
        Party = " "
    elif LSParty:
        Party = "AND FINDOCUMENT.GLCODE in " + str(LSPartys)

    if not LCCompanyCode and not LSCompanyUnitCode:
        CompanyCode = " "
    elif LCCompanyCode:
        CompanyCode = " "
    elif LSCompanyUnitCode:
        CompanyCode = "AND FINDOCUMENTLINE.FINDOCUMENTBUSINESSUNITCODE in " + str(LSCompanyUnitCodes)

    sql = "Select  Finbusinessunit.LongDescription As BUSINESSUNITName, AccMaster.LongDescription As AccName" \
          ", Sum(Case When FinDocumentLine.AmountInCC > 0 And FinDocumentLine.CreditLine = 0 And FinDocument.FinanceDocumentDate >= "+startdate+" Then FinDocumentLine.AmountInCC Else 0 End) as DrAmt" \
          ", Sum(Case When FinDocumentLine.AmountInCC < 0 And FinDocumentLine.CreditLine = 1 And FinDocument.FinanceDocumentDate >= "+startdate+" Then Abs(FinDocumentLine.AmountInCC) Else 0 End) as CrAmt " \
          "From    FinDocument " \
          "Join    FinDocumentLine      On      FinDocument.BUSINESSUNITCODE = FinDocumentLine.FINDOCUMENTBUSINESSUNITCODE " \
          "And     FinDocument.FINANCIALYEARCODE = FinDocumentLine.FINDOCUMENTFINANCIALYEARCODE " \
          "And     FinDocument.DOCUMENTTEMPLATECODE = FinDocumentLine.FINDOCDOCUMENTTEMPLATECODE " \
          "And     FinDocument.Code = FinDocumentLine.FINDOCUMENTCODE " \
          "And     FinDocument.GLCode <> FinDocumentLine.GLCODE " \
          "Join    FinBusinessUnit         On      FinDocument.BUSINESSUNITCODE = FinBusinessUnit.CODE " \
          "Join    GLMaster As AccMaster   On      FinDocumentline.GLCODE = AccMaster.Code " \
          "Where   FinDocument.FinanceDocumentDate Between "+startdate+" And "+enddate+"" +CompanyCode+" "+Party+" " \
          "And     FinDocument.DocumentTypeCode In ('BP','BR','CP','CR') " \
          "Group By Finbusinessunit.LongDescription, AccMaster.LongDescription " \
          "order by Finbusinessunit.LongDescription"
    # FinDocumentLine.CreditLine = 1 That Means DrCrType = 'C'
    # FinDocumentLine.CreditLine = 0 That Means DrCrType = 'D'






    stmt = con.db.prepare(con.conn, sql)

    # print(stdt)
    # Explicitly bind parameters
    # con.db.bind_param(stmt, 1, stdt)
    # con.db.bind_param(stmt, 2, stdt)
    # con.db.bind_param(stmt, 3, stdt)
    # con.db.bind_param(stmt, 4, stdt)
    # con.db.bind_param(stmt, 5, stdt)
    # con.db.bind_param(stmt, 6, stdt)
    # con.db.bind_param(stmt, 7, stdt)
    # con.db.bind_param(stmt, 8, stdt)
    # con.db.bind_param(stmt, 9, stdt)
    # con.db.bind_param(stmt, 10, stdt)
    # con.db.bind_param(stmt, 11, stdt)
    # con.db.bind_param(stmt, 12, stdt)
    # con.db.bind_param(stmt, 13, stdt)
    # con.db.bind_param(stmt, 14, stdt)
    # con.db.bind_param(stmt, 15, stdt)
    # con.db.bind_param(stmt, 16, stdt)

    # print(sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1
        pdfCSrpt.textsize(pdfCSrpt.c, result, pdfCSrpt.d, stdt, etdt)
        pdfCSrpt.d = pdfCSrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfCSrpt.d < 20:
            pdfCSrpt.d = 740
            # pdfCSrpt.c.setPageSize(pdfCSrpt.landscape(pdfCSrpt.A3))
            pdfCSrpt.c.showPage()
            pdfCSrpt.header(stdt, etdt, pdfCSrpt.CompanyName)
            # pdfCSrpt.fonts(7)
            # pdfCSrpt.c.drawString(250, pdfCSrpt.d, pdfCSrpt.BankName[-1])
            # pdfCSrpt.d = pdfCSrpt.dvalue()
            # pdfCSrpt.c.drawString(10, pdfCSrpt.d, result['ACCNAME'])
            # pdfCSrpt.c.drawAlignedString(400, pdfCSrpt.d, str(pdfCSrpt.locale.currency(float(result['DRAMT']), grouping=True))[1:])
            # pdfCSrpt.c.drawAlignedString(550, pdfCSrpt.d, str(pdfCSrpt.locale.currency(float(result['CRAMT']), grouping=True))[1:])
            # pdfCSrpt.data(result, pdfCSrpt.d)

    if result == False:
        if counter > 0:
            pdfCSrpt.d = pdfCSrpt.dvalue()
            pdfCSrpt.c.setFont('Helvetica-Bold', 8)
            pdfCSrpt.c.setFillColorRGB(0, 0, 0)
            pdfCSrpt.c.drawString(200, pdfCSrpt.d, " TOTAL : ")
            if (float(pdfCSrpt.totaldramt))!= 0:
                pdfCSrpt.c.drawAlignedString(400, pdfCSrpt.d, str(pdfCSrpt.locale.currency(float(pdfCSrpt.totaldramt), grouping=True))[1:])
            if (float(pdfCSrpt.totalcramt)) != 0:
                pdfCSrpt.c.drawAlignedString(560, pdfCSrpt.d, str(pdfCSrpt.locale.currency(float(pdfCSrpt.totalcramt), grouping=True))[1:])
            # pdfCSrpt.c.drawString(10, pdfCSrpt.d, str(pdfCSrpt.divisioncode[-1]) + " TOTAL : ")
            # pdfCSrpt.c.drawAlignedString(575, pdfCSrpt.d, str("%.3f" % float(pdfCSrpt.OpeningBalance)))
            # pdfCSrpt.printstoretotal()
            # pdfCSrpt.d = pdfCSrpt.dvalue()
            # pdfCSrpt.printtotal()
            # pdfCSrpt.storeclean()
            # pdfCSrpt.companyclean()
            # pdfCSrpt.cleanstore()
            BCSV.Exceptions = ""
            counter = 0
        elif counter == 0:
            BCSV.Exceptions = "Note: Please Select Valid Credentials"
            return
    # pdfCSrpt.workbook.close()
    # pdfCSrpt.c.setPageSize(pdfCSrpt.landscape(pdfCSrpt.A3))
    pdfCSrpt.c.showPage()
    pdfCSrpt.c.save()
    # url = "file:///D:/Report Development/Generated Reports/GST Register/" + LSFileName + ".pdf"
    # os.startfile(url)
    pdfCSrpt.newrequest()
    pdfCSrpt.d = pdfCSrpt.newpage()