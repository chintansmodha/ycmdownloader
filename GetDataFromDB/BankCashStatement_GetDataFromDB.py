from datetime import datetime
from PrintPDF import BankCashStatement_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
from ProcessSelection import BankCashStatement_ProcessSelection as BCSV
counter=0
def BankCashStatement_PrintPDF(LSCompanyUnitCode,LSParty,LDstdt,LDEndDate,LCParty,LCCompanyCode,LSConsolidate,LSACSummary,LSFileName):
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
        Party=" "
    elif LCParty:
        Party=" "
    elif LSParty:
        Party = "AND FINDOCUMENT.GLCODE in " + str(LSPartys)

    if not LCCompanyCode and not LSCompanyUnitCode:
        CompanyCode=" "
    elif LCCompanyCode:
        CompanyCode=" "
    elif LSCompanyUnitCode:
        CompanyCode="AND FinDocument.BUSINESSUNITCODE in "+str(LSCompanyUnitCodes)

    sql =  "Select  Finbusinessunit.LongDescription As BUSINESSUNITName, GLMaster.LongDescription As BankName," \
           "Case When FinDocument.FinanceDocumentDate < "+startdate+" Then '' Else BusinessPartner.LegalName1 End  As PartyName," \
           "Case When FinDocument.FinanceDocumentDate < "+startdate+" Then '1980-01-01' Else FinDocument.FinanceDocumentDate End as VchDate," \
           "Case When FinDocument.FinanceDocumentDate < "+startdate+" Then '' Else FinDocument.DocumentTypeCode End As TxnType," \
           "Case When FinDocument.FinanceDocumentDate < "+startdate+" Then '' Else FinDocument.ChequeNumber End As ChequeNumber," \
           "Case When FinDocument.FinanceDocumentDate < "+startdate+" Then '' Else FinDocument.Code End As VchNo" \
           ", Sum(Case When FinDocument.FinanceDocumentDate < "+startdate+" Then FinDocument.DocumentAmount * " \
           "Case When FinDocument.DocumentTypeCode In ('BR','CR') Then 1 Else -1 End Else 0 End) As OpBal" \
           ", Sum(Case When FinDocument.DocumentTypeCode In ('BR','CR') And FinDocument.FinanceDocumentDate >= "+startdate+" Then FinDocument.DocumentAmount Else 0 End) as ReceiptAmt" \
           ", Sum(Case When FinDocument.DocumentTypeCode In ('BP','CP') And FinDocument.FinanceDocumentDate >= "+startdate+" Then FinDocument.DocumentAmount Else 0 End) as PaymentAmt " \
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
           "Where   FinDocument.FinanceDocumentDate <= "+enddate+"" +CompanyCode+" "+Party+" " \
           "And          FinDocument.CurrentStatus=1 " \
           "And     FinDocument.DocumentTypeCode In ('BP','BR','CP','CR') " \
           "Group By Finbusinessunit.LongDescription, GLMaster.LongDescription," \
           "Case When FinDocument.FinanceDocumentDate < "+startdate+" Then '' Else BusinessPartner.LegalName1 End," \
           "Case When FinDocument.FinanceDocumentDate < "+startdate+" Then '1980-01-01' Else FinDocument.FinanceDocumentDate End," \
           "Case When FinDocument.FinanceDocumentDate < "+startdate+" Then '' Else FinDocument.DocumentTypeCode End," \
           "Case When FinDocument.FinanceDocumentDate < "+startdate+" Then '' Else FinDocument.ChequeNumber End," \
           "Case When FinDocument.FinanceDocumentDate < "+startdate+" Then '' Else FinDocument.Code End " \
           "order by Finbusinessunit.LongDescription , BankName , VchDate, txnType desc, VchNo"




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

    #print(sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d,stdt,etdt)
        pdfrpt.d=pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d<20:
            pdfrpt.d=715
            #pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A3))
            pdfrpt.c.showPage()
            pdfrpt.header(stdt,etdt,pdfrpt.divisioncode)

    if result == False:
        if counter > 0:
            pdfrpt.d = pdfrpt.dvalue()
            pdfrpt.c.setFont('Helvetica-Bold', 8)
            pdfrpt.c.drawString(200, pdfrpt.d, "Transaction Totals : ")
            # if pdfrpt.paymentTotal != 0:
            pdfrpt.c.drawAlignedString(415, pdfrpt.d, str(pdfrpt.format_currency(float(pdfrpt.paymentTotal), '', locale='en_IN')))
            # if pdfrpt.receiptTotal != 0:
            pdfrpt.c.drawAlignedString(485, pdfrpt.d, str(pdfrpt.format_currency(float(pdfrpt.receiptTotal), '', locale='en_IN')))
            pdfrpt.d = pdfrpt.d -15
            pdfrpt.c.drawString(200, pdfrpt.d, " Closing Balance : ")
            # pdfrpt.c.drawAlignedString(575, pdfrpt.d, str(pdfrpt.locale.currency(float(pdfrpt.OpeningBalance), grouping=True))[1:])
            if pdfrpt.OpeningBalance > 0:
                pdfrpt.c.drawAlignedString(485, pdfrpt.d, str(pdfrpt.format_currency(float(pdfrpt.OpeningBalance), '', locale='en_IN')))
            else:
                pdfrpt.c.drawAlignedString(415, pdfrpt.d, str(pdfrpt.format_currency(float(pdfrpt.OpeningBalance), ' ', locale='en_IN')))
            # pdfrpt.printstoretotal()
            # pdfrpt.d = pdfrpt.dvalue()
            # pdfrpt.printtotal()
            # pdfrpt.storeclean()
            # pdfrpt.companyclean()
            # pdfrpt.cleanstore()
            BCSV.Exceptions = ""
            counter = 0
        elif counter==0:
            BCSV.Exceptions="Note: Please Select Valid Credentials"
            return
    #pdfrpt.workbook.close()
    #pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A3))
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    # url = "file:///D:/Report Development/Generated Reports/GST Register/" + LSFileName + ".pdf"
    # os.startfile(url)
    pdfrpt.newrequest()
    pdfrpt.d = pdfrpt.newpage()