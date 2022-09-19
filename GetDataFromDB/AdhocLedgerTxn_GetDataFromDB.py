import os
from datetime import datetime
from PrintPDF import AdhocLedgerTxn_PrintPDF as pdfADLTXN
from Global_Files import Connection_String as con
from ProcessSelection import AdhocLedgerPDF_ProcessSelection as ADLV

counter = 0


def AdhocLedger_PrintPDF(LSCompanyUnitCode, LSAccountCode, LSSubAccountCode, LDStartDate, LDEndDate, LCAccountCode,
                         LCSubAccountCode, LCCompanyUnitCode, LCEject, LCNarration, LCAddress, LMMergeSubAcc, LMMergeCompany):
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"
    if LMMergeCompany == ['true']:
        mergecomp = '1'
    else:
        mergecomp = '0'

    companyunitcode = str(LSCompanyUnitCode)
    LSCompanyUnitCodes = '(' + companyunitcode[1:-1] + ')'

    accountcode = str(LSAccountCode)
    LSAccountCodes = '(' + accountcode[1:-1] + ')'

    subaccountcode = str(LSSubAccountCode)
    LSSubAccountCodes = '(' + subaccountcode[1:-1] + ')'

    if not LCCompanyUnitCode and not LSCompanyUnitCode:
        companyunitcode = " "
    elif LCCompanyUnitCode:
        companyunitcode = " "
    elif LSCompanyUnitCode:
        companyunitcode = "AND findocument.BUSINESSUNITCODE in " + str(LSCompanyUnitCodes)

    if not LCAccountCode and not LSAccountCode:
        accountcode = " "
    elif LCAccountCode:
        accountcode = " "
    elif LSAccountCode:
        accountcode = "AND findocumentline.GLCODE  in " + str(LSAccountCodes)

    if not LCSubAccountCode and not LSSubAccountCode:
        subaccountcode = " "
    elif LCSubAccountCode:
        subaccountcode = " "
    elif LSSubAccountCode:
        subaccountcode = "AND ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID in " + str(LSSubAccountCodes)

    sql = "Select  Case "+mergecomp+" When 1 Then 'Beekaylon Group Of Companies' When 0 Then FINBUSINESSUNIT.LONGDESCRIPTION End As BusinessUnit " \
          ", Case COALESCE(BUSINESSPARTNER.LEGALNAME1,'') When BUSINESSPARTNER.LEGALNAME1 Then GLMASTER.LONGDESCRIPTION ||' - '|| " \
          "BUSINESSPARTNER.LEGALNAME1 Else GLMASTER.LONGDESCRIPTION End As GLAccount " \
          ", Case When FinDocument.FINANCEDOCUMENTDATE < "+startdate+" Then '' Else FINDOCUMENTTYPE.LONGDESCRIPTION End As DocumentType " \
          ", cast(Sum(Case When FinDocument.FINANCEDOCUMENTDATE <"+startdate+" " \
          "Then FINDOCUMENTLINE.AMOUNTINCC Else 0 End)as decimal(18,2)) As OpBal " \
          ", cast(Sum(Case When FINDOCUMENTLINE.AMOUNTINCC > 0 And FinDocument.FINANCEDOCUMENTDATE Between "+startdate+" And "+enddate+" " \
          "Then FINDOCUMENTLINE.AMOUNTINCC Else 0 End)as decimal(18,2)) As DrAmount " \
          ", cast(Abs(Sum(Case When FINDOCUMENTLINE.AMOUNTINCC < 0 And FinDocument.FINANCEDOCUMENTDATE Between "+startdate+" And "+enddate+" " \
          "Then FINDOCUMENTLINE.AMOUNTINCC Else 0 End)) as decimal(18,2)) As CrAmount " \
          ", cast(Sum(FINDOCUMENTLINE.AMOUNTINCC) as decimal(18,2)) As ClBal " \
          "from FINDOCUMENT " \
          "join FINDOCUMENTLINE         On      FINDOCUMENT.COMPANYCODE       =  FINDOCUMENTLINE.FINDOCUMENTCOMPANYCODE " \
          "And     FINDOCUMENT.BUSINESSUNITCODE  =  FINDOCUMENTLINE.FINDOCUMENTBUSINESSUNITCODE " \
          "AND     FINDOCUMENT.FINANCIALYEARCODE =  FINDOCUMENTLINE.FINDOCUMENTFINANCIALYEARCODE " \
          "AND     FINDOCUMENT.DOCUMENTTEMPLATECODE = FINDOCUMENTLINE.FINDOCDOCUMENTTEMPLATECODE " \
          "And     FINDOCUMENT.CODE = FINDOCUMENTLINE.FINDOCUMENTCODE " \
          "join FINBUSINESSUNIT         on      FINDOCUMENT.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "join GLMASTER                on      FINDOCUMENTLINE.glCODE = GLMASTER.CODE " \
          "Left join orderpartner       on      FINDOCUMENTLINE.SLCUSTOMERSUPPLIERTYPE =orderpartner.CUSTOMERSUPPLIERTYPE " \
          "AND     FINDOCUMENTLINE.SLCUSTOMERSUPPLIERCODE = orderpartner.CUSTOMERSUPPLIERCODE " \
          "Left join BUSINESSPARTNER    on      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID " \
          "Join FINDOCUMENTTYPE         On      FINDOCUMENT.DOCUMENTTYPECODE = FINDOCUMENTTYPE.CODE " \
          "Where   FINDOCUMENT.FINANCEDOCUMENTDATE      <= "+enddate+" "+companyunitcode+" "+accountcode+" "+subaccountcode+" " \
          "And FinDocument.CURRENTSTATUS = '1'  " \
          "Group By Case "+mergecomp+" When 1 Then 'Beekaylon Group Of Companies' When 0 Then FINBUSINESSUNIT.LONGDESCRIPTION End " \
          ", Case When FinDocument.FINANCEDOCUMENTDATE < "+startdate+" Then '' Else FINDOCUMENTTYPE.LONGDESCRIPTION End " \
          ", Case COALESCE(BUSINESSPARTNER.LEGALNAME1,'') When BUSINESSPARTNER.LEGALNAME1 Then GLMASTER.LONGDESCRIPTION ||' - '|| " \
          "BUSINESSPARTNER.LEGALNAME1 Else GLMASTER.LONGDESCRIPTION End " \
          "order by  BusinessUnit, GLAccount, DocumentType"

    # ", COALESCE(ADDRESS.ADDRESSLINE1,'') As Address1a " \
    #           ", COALESCE(ADDRESS.ADDRESSLINE2,'') As Address1b " \
    #           ", COALESCE(ADDRESS.ADDRESSLINE3,'') As Address1c " \
    #           ", COALESCE(ADDRESS.ADDRESSLINE4,'') As Address2a " \
    #           ", COALESCE(ADDRESS.ADDRESSLINE5,'') As Address2b " \
    #           ", COALESCE(ADDRESS.POSTALCODE,'') As Address2c " \
    #           ", COALESCE(ADDRESS.TOWN,'') As City " \
    #           ", COALESCE(ADDRESS.DISTRICT,'') As District


    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfADLTXN.textsize(pdfADLTXN.c, result, pdfADLTXN.d, stdt, etdt, LCEject, LCNarration, LCAddress, LMMergeCompany)
        pdfADLTXN.d = pdfADLTXN.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfADLTXN.d < 60:
            pdfADLTXN.d = 740
            pdfADLTXN.c.showPage()
            pdfADLTXN.header(stdt, etdt, pdfADLTXN.divisioncode, LMMergeCompany)

    if result == False:
        if counter > 0:
            pdfADLTXN.d =pdfADLTXN.dvalue()
            pdfADLTXN.fonts(7)
            pdfADLTXN.c.drawString(35, pdfADLTXN.d, "Closing Balance : ")
            if pdfADLTXN.closingbalance != 0:
                if pdfADLTXN.closingbalance < 0:
                    pdfADLTXN.c.drawAlignedString(415, pdfADLTXN.d, str('{0:1.2f}'.format(-pdfADLTXN.closingbalance)))
                else:
                    pdfADLTXN.c.drawAlignedString(555, pdfADLTXN.d, str('{0:1.2f}'.format(pdfADLTXN.closingbalance)))
            elif pdfADLTXN.closingbalance == 0:
                pdfADLTXN.c.drawAlignedString(415, pdfADLTXN.d, str('{0:1.2f}'.format(pdfADLTXN.closingbalance)))
            pdfADLTXN.d = pdfADLTXN.dvalue()
            pdfADLTXN.c.line(340, pdfADLTXN.d, 590, pdfADLTXN.d)
            pdfADLTXN.d = pdfADLTXN.dvalue()
            pdfADLTXN.d = pdfADLTXN.dvalue()
            pdfADLTXN.c.drawString(200, pdfADLTXN.d, "Total : ")
            if pdfADLTXN.closingbalance <= 0:
                pdfADLTXN.c.drawAlignedString(415, pdfADLTXN.d, str('{0:1.2f}'.format(pdfADLTXN.DRAmountTotal - pdfADLTXN.closingbalance)))
            else:
                pdfADLTXN.c.drawAlignedString(415, pdfADLTXN.d, str('{0:1.2f}'.format(pdfADLTXN.DRAmountTotal)))
            if pdfADLTXN.closingbalance > 0:
                pdfADLTXN.c.drawAlignedString(555, pdfADLTXN.d, str('{0:1.2f}'.format(pdfADLTXN.CRAmountTotal + pdfADLTXN.closingbalance)))
            else:
                pdfADLTXN.c.drawAlignedString(555, pdfADLTXN.d, str('{0:1.2f}'.format(pdfADLTXN.CRAmountTotal)))
            pdfADLTXN.d = pdfADLTXN.dvalue()
            # d = dvalue()
            pdfADLTXN.c.line(340, pdfADLTXN.d, 590, pdfADLTXN.d)


            ADLV.Exceptions = ""
            counter = 0
        elif counter == 0:
            ADLV.Exceptions = "Note: No Report Form For Given Criteria"
            return

    pdfADLTXN.c.showPage()
    pdfADLTXN.c.save()

    pdfADLTXN.newrequest()
    pdfADLTXN.d = pdfADLTXN.newpage()
