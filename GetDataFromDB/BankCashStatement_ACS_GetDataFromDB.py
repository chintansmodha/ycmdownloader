from datetime import datetime
from PrintPDF import BankCashStatement_ACS_PrintPDF as pdfArpt
from Global_Files import Connection_String as con
from ProcessSelection import BankCashStatement_ProcessSelection as BCSV

counter = 0

def BankCashStatement_ACS_PrintPDF(LSCompanyUnitCode, LSParty, LDstdt, LDEndDate, LCParty, LCCompanyCode, LSConsolidate,
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

    sql = "Select  Finbusinessunit.LongDescription As BUSINESSUNITName, BankMaster.LongDescription As BankName, AccMaster.LongDescription As AccName" \
          ", Sum(Case When FinDocumentLine.AmountInCC > 0 And FinDocumentLine.CreditLine = 0 And FinDocument.FinanceDocumentDate >= "+startdate+" Then FinDocumentLine.AmountInCC Else 0 End) as DrAmt" \
          ", Sum(Case When FinDocumentLine.AmountInCC < 0 And FinDocumentLine.CreditLine = 1 And FinDocument.FinanceDocumentDate >= "+startdate+" Then Abs(FinDocumentLine.AmountInCC) Else 0 End) as CrAmt " \
          "From    FinDocument " \
          "Join    FinDocumentLine      On      FinDocument.BUSINESSUNITCODE = FinDocumentLine.FINDOCUMENTBUSINESSUNITCODE " \
          "And     FinDocument.FINANCIALYEARCODE = FinDocumentLine.FINDOCUMENTFINANCIALYEARCODE " \
          "And     FinDocument.DOCUMENTTEMPLATECODE = FinDocumentLine.FINDOCDOCUMENTTEMPLATECODE " \
          "And     FinDocument.Code = FinDocumentLine.FINDOCUMENTCODE " \
          "And     FinDocument.GLCode <> FinDocumentLine.GLCODE " \
          "Join    FinBusinessUnit         On      FinDocument.BUSINESSUNITCODE = FinBusinessUnit.CODE " \
          "Join    GLMaster As BankMaster  On      FinDocument.GLCODE = BankMaster.Code " \
          "Join    GLMaster As AccMaster   On      FinDocumentline.GLCODE = AccMaster.Code " \
          "Where   FinDocument.FinanceDocumentDate Between "+startdate+" And "+enddate+"" +CompanyCode+" "+Party+" " \
          "And     FinDocument.DocumentTypeCode In ('BP','BR','CP','CR') " \
          "Group By Finbusinessunit.LongDescription, BankMaster.LongDescription, AccMaster.LongDescription " \
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
        pdfArpt.textsize(pdfArpt.c, result, pdfArpt.d, stdt, etdt)
        pdfArpt.d = pdfArpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfArpt.d < 20:
            pdfArpt.d = 732
            # pdfArpt.c.setPageSize(pdfArpt.landscape(pdfArpt.A3))
            pdfArpt.c.showPage()
            pdfArpt.header(stdt, etdt, pdfArpt.divisioncode)

            # pdfArpt.d = pdfArpt.dvalue()
            # pdfArpt.fonts(7)
            # pdfArpt.c.drawString(250, pdfArpt.d, pdfArpt.BankName[-1])
            # pdfArpt.d = pdfArpt.dvalue()
            # pdfArpt.data(result, pdfArpt.d)

    if result == False:
        if counter > 0:
            pdfArpt.d = pdfArpt.dvalue()
            # pdfArpt.fonts(8)
            pdfArpt.c.setFillColorRGB(0, 0, 0)
            pdfArpt.c.setFont('Helvetica-Bold', 8)
            pdfArpt.c.drawString(150, pdfArpt.d, "BANK TOTAL : ")
            if (float(pdfArpt.totaldramt))!= 0:
                pdfArpt.c.drawAlignedString(440, pdfArpt.d, str(pdfArpt.locale.currency(float(pdfArpt.totaldramt), grouping=True))[1:])
            if (float(pdfArpt.totalcramt)) != 0:
                pdfArpt.c.drawAlignedString(570, pdfArpt.d, str(pdfArpt.locale.currency(float(pdfArpt.totalcramt), grouping=True))[1:])
            pdfArpt.d = pdfArpt.dvalue()
            pdfArpt.d = pdfArpt.dvalue()
            pdfArpt.c.drawString(150, pdfArpt.d, "Company TOTAL : ")
            if (float(pdfArpt.Comptotaldramt))!= 0:
                pdfArpt.c.drawAlignedString(440, pdfArpt.d, str(pdfArpt.locale.currency(float(pdfArpt.Comptotaldramt), grouping=True))[1:])
            if (float(pdfArpt.Comptotalcramt)) != 0:
                pdfArpt.c.drawAlignedString(570, pdfArpt.d, str(pdfArpt.locale.currency(float(pdfArpt.Comptotalcramt), grouping=True))[1:])
            # pdfArpt.c.drawString(10, pdfArpt.d, str(pdfArpt.divisioncode[-1]) + " TOTAL : ")
            # pdfArpt.c.drawAlignedString(575, pdfArpt.d, str("%.3f" % float(pdfArpt.OpeningBalance)))
            # pdfArpt.printstoretotal()
            # pdfArpt.d = pdfArpt.dvalue()
            # pdfArpt.printtotal()
            # pdfArpt.storeclean()
            # pdfArpt.companyclean()
            # pdfArpt.cleanstore()
            BCSV.Exceptions = ""
            counter = 0
        elif counter == 0:
            BCSV.Exceptions = "Note: Please Select Valid Credentials"
            return
    # pdfArpt.workbook.close()
    # pdfArpt.c.setPageSize(pdfArpt.landscape(pdfArpt.A3))
    pdfArpt.c.showPage()
    pdfArpt.c.save()
    # url = "file:///D:/Report Development/Generated Reports/GST Register/" + LSFileName + ".pdf"
    # os.startfile(url)
    pdfArpt.newrequest()
    pdfArpt.d = pdfArpt.newpage()