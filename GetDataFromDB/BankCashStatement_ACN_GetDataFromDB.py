from datetime import datetime
from PrintPDF import BankCashStatement_ACN_PrintPDF as pdfANrpt
from Global_Files import Connection_String as con
from ProcessSelection import BankCashStatement_ProcessSelection as BCSV

counter = 0


def BankCashStatement_ACN_PrintPDF(LSCompanyUnitCode, LSParty, LDstdt, LDEndDate, LCParty, LCCompanyCode, LSConsolidate,
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
        CompanyCode = "AND FinDocument.BUSINESSUNITCODE in " + str(LSCompanyUnitCodes)

    sql = "Select  '' BUSINESSUNITName, '' BankName," \
          "Case When FinDocument.FinanceDocumentDate < " + startdate + " Then '' Else BusinessPartner.LegalName1 End  As PartyName," \
          "Case When FinDocument.FinanceDocumentDate < " + startdate + " Then '1980-01-01' Else FinDocument.FinanceDocumentDate End as VchDate," \
          "Case When FinDocument.FinanceDocumentDate < " + startdate + " Then 'OP' Else FinDocument.DocumentTypeCode End As TxnType," \
          "Case When FinDocument.FinanceDocumentDate < " + startdate + " Then '' Else FinDocument.ChequeNumber End As ChequeNumber," \
          "Case When FinDocument.FinanceDocumentDate < " + startdate + " Then '' Else FinDocument.Code End As VchNo" \
          ", Sum(Case When FinDocument.FinanceDocumentDate < " + startdate + " Then FinDocument.DocumentAmount * " \
          "Case When FinDocument.DocumentTypeCode In ('BR','CR') Then 1 Else -1 End Else 0 End) As OpBal" \
          ", Sum(Case When FinDocument.DocumentTypeCode In ('BR','CR') And FinDocument.FinanceDocumentDate >= " + startdate + " Then FinDocument.DocumentAmount Else 0 End) as ReceiptAmt" \
          ", Sum(Case When FinDocument.DocumentTypeCode In ('BP','CP') And FinDocument.FinanceDocumentDate >= " + startdate + " Then FinDocument.DocumentAmount Else 0 End) as PaymentAmt " \
          "From    FinDocument " \
          "Join    FinDocumentLine      On      FinDocument.BUSINESSUNITCODE = FinDocumentLine.FINDOCUMENTBUSINESSUNITCODE " \
          "And     FinDocument.FINANCIALYEARCODE = FinDocumentLine.FINDOCUMENTFINANCIALYEARCODE " \
          "And     FinDocument.Code = FinDocumentLine.FINDOCUMENTCODE " \
          "And     FinDocumentLine.GLCODE <> FinDocument.GLCODE " \
          "Join    FinBusinessUnit         On      FinDocument.BUSINESSUNITCODE=FinBusinessUnit.CODE " \
          "Join    OrderPartner            On      FinDocumentLine.SLCUSTOMERSUPPLIERTYPE = OrderPartner.CUSTOMERSUPPLIERTYPE " \
          "And     FinDocumentLine.SLCUSTOMERSUPPLIERCODE =OrderPartner.CUSTOMERSUPPLIERCODE " \
          "Join    BusinessPartner         On      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID " \
          "Join    GLMaster                On      FinDocument.GLCODE = GlMaster.Code " \
          "Where   FinDocument.FinanceDocumentDate <= " + enddate + "" + CompanyCode + " " + Party + " " \
          "And     FinDocument.CurrentStatus = 1 " \
          "And     FinDocument.DocumentTypeCode In ('BP','BR','CP','CR') " \
          "Group By " \
          "Case When FinDocument.FinanceDocumentDate < " + startdate + " Then '' Else BusinessPartner.LegalName1 End," \
          "Case When FinDocument.FinanceDocumentDate < " + startdate + " Then '1980-01-01' Else FinDocument.FinanceDocumentDate End," \
          "Case When FinDocument.FinanceDocumentDate < " + startdate + " Then 'OP' Else FinDocument.DocumentTypeCode End," \
          "Case When FinDocument.FinanceDocumentDate < " + startdate + " Then '' Else FinDocument.ChequeNumber End," \
          "Case When FinDocument.FinanceDocumentDate < " + startdate + " Then '' Else FinDocument.Code End " \
          "order by  BUSINESSUNITName, BankName , VchDate, txnType desc, VchNo"

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

        pdfANrpt.textsize(pdfANrpt.c, result, pdfANrpt.d, stdt, etdt)
        pdfANrpt.d = pdfANrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfANrpt.d < 20:
            pdfANrpt.d = 723
            # pdfANrpt.c.setPageSize(pdfANrpt.landscape(pdfANrpt.A3))
            pdfANrpt.c.showPage()
            pdfANrpt.header(stdt, etdt, pdfANrpt.CompanyName)

    if result == False:
        if counter > 0:
            pdfANrpt.d = pdfANrpt.dvalue()
            pdfANrpt.c.setFont('Helvetica-Bold', 8)
            pdfANrpt.c.drawString(200, pdfANrpt.d, " TOTAL : ")
            pdfANrpt.c.drawAlignedString(400, pdfANrpt.d,
            str(pdfANrpt.locale.currency(float(pdfANrpt.paymentTotal), grouping=True))[1:])
            pdfANrpt.c.drawAlignedString(480, pdfANrpt.d,
            str(pdfANrpt.locale.currency(float(pdfANrpt.receiptTotal), grouping=True))[1:])
            # pdfANrpt.printstoretotal()
            # pdfANrpt.d = pdfANrpt.dvalue()
            # pdfANrpt.printtotal()
            # pdfANrpt.storeclean()
            # pdfANrpt.companyclean()
            # pdfANrpt.cleanstore()
            BCSV.Exceptions = ""
            counter =0
        elif counter == 0:
            BCSV.Exceptions = "Note: Please Select Valid Credentials"
            return
    # pdfANrpt.workbook.close()
    # pdfANrpt.c.setPageSize(pdfANrpt.landscape(pdfANrpt.A3))
    pdfANrpt.c.showPage()
    pdfANrpt.c.save()
    # url = "file:///D:/Report Development/Generated Reports/GST Register/" + LSFileName + ".pdf"
    # os.startfile(url)
    pdfANrpt.newrequest()
    pdfANrpt.d = pdfANrpt.newpage()