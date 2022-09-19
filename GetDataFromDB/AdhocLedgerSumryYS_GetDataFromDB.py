import os
from datetime import datetime
from PrintPDF import AdhocLedgerSumryYS_PrintPDF as pdfADLSYS
from Global_Files import Connection_String as con
from ProcessSelection import AdhocLedgerPDF_ProcessSelection as ADLV

counter = 0


def AdhocLedger_PrintPDF(LSCompanyUnitCode, LSAccountCode, LSSubAccountCode, LDStartDate, LDEndDate, LCAccountCode,
                         LCSubAccountCode, LCCompanyUnitCode, LCEject, LCNarration, LCAddress, LMMergeSubAcc):
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"

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

    sql = "Select     FINBUSINESSUNIT.LONGDESCRIPTION As BusinessUnit " \
          ", GLMASTER.LONGDESCRIPTION As GLAccount " \
          ", COALESCE(BUSINESSPARTNER.LEGALNAME1,'') As SubAccount " \
          ", Case When ADDRESS.UNIQUEID is not Null Then (COALESCE(ADDRESS.ADDRESSEE,'') ||' '|| COALESCE(ADDRESS.ADDRESSLINE1,'') " \
          "||' '|| COALESCE(ADDRESS.ADDRESSLINE2,'') ||' '|| COALESCE(ADDRESS.ADDRESSLINE3,'') " \
          "||' '|| COALESCE(ADDRESS.ADDRESSLINE4,'') ||' '|| COALESCE(ADDRESS.ADDRESSLINE5,'') ||' '|| COALESCE(ADDRESS.POSTALCODE,'') " \
          "||' '|| COALESCE(ADDRESS.TOWN,'') || ' '|| COALESCE(ADDRESS.DISTRICT,'')) Else (COALESCE(businesspartner.ADDRESSLINE1, '') " \
          "||' '|| COALESCE(businesspartner.ADDRESSLINE2, '') " \
          "||' '|| COALESCE(businesspartner.ADDRESSLINE3, '') ||' '|| COALESCE(businesspartner.ADDRESSLINE4, '') " \
          "||' '|| RTRIM(COALESCE(businesspartner.ADDRESSLINE5, '')) " \
          "||' '|| RTRIM(COALESCE(businesspartner.POSTALCODE, '')) ||' '|| RTRIM(COALESCE(businesspartner.TOWN, '')) " \
          "||' '|| COALESCE(businesspartner.DISTRICT, '')) End As Address " \
          ", COALESCE(ORDERPARTNERIE.PANNO,'') As PAN " \
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
          "join FINBUSINESSUNIT          on      FINDOCUMENT.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "join GLMASTER                 on      FINDOCUMENTLINE.glCODE = GLMASTER.CODE " \
          "Left join orderpartner        on      FINDOCUMENTLINE.SLCUSTOMERSUPPLIERTYPE =orderpartner.CUSTOMERSUPPLIERTYPE " \
          "AND     FINDOCUMENTLINE.SLCUSTOMERSUPPLIERCODE = orderpartner.CUSTOMERSUPPLIERCODE " \
          "Left Join ORDERPARTNERIE     On      ORDERPARTNER.CUSTOMERSUPPLIERTYPE = ORDERPARTNERIE.CUSTOMERSUPPLIERTYPE " \
          "And     ORDERPARTNER.CUSTOMERSUPPLIERCODE = ORDERPARTNERIE.CUSTOMERSUPPLIERCODE " \
          "Left join businesspartner     on      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID " \
          "Left Join ADDRESS            On      BUSINESSPARTNER.ABSUNIQUEID = ADDRESS.UNIQUEID " \
          "AND     ADDRESS.ADDRESSTYPE = 1 " \
          "Where   FINDOCUMENT.FINANCEDOCUMENTDATE      <= "+enddate+" "+companyunitcode+" "+accountcode+" "+subaccountcode+" " \
          "And FinDocument.CURRENTSTATUS = '1'  " \
          "Group By FINBUSINESSUNIT.LONGDESCRIPTION, GLMASTER.LONGDESCRIPTION, COALESCE(BUSINESSPARTNER.LEGALNAME1,'') " \
          ", Case When ADDRESS.UNIQUEID is not Null Then (COALESCE(ADDRESS.ADDRESSEE,'') ||' '|| COALESCE(ADDRESS.ADDRESSLINE1,'') " \
          "||' '|| COALESCE(ADDRESS.ADDRESSLINE2,'') ||' '|| COALESCE(ADDRESS.ADDRESSLINE3,'') " \
          "||' '|| COALESCE(ADDRESS.ADDRESSLINE4,'') ||' '|| COALESCE(ADDRESS.ADDRESSLINE5,'') ||' '|| COALESCE(ADDRESS.POSTALCODE,'') " \
          "||' '|| COALESCE(ADDRESS.TOWN,'') || ' '|| COALESCE(ADDRESS.DISTRICT,'')) Else (COALESCE(businesspartner.ADDRESSLINE1, '') " \
          "||' '|| COALESCE(businesspartner.ADDRESSLINE2, '') " \
          "||' '|| COALESCE(businesspartner.ADDRESSLINE3, '') ||' '|| COALESCE(businesspartner.ADDRESSLINE4, '') " \
          "||' '|| RTRIM(COALESCE(businesspartner.ADDRESSLINE5, '')) " \
          "||' '|| RTRIM(COALESCE(businesspartner.POSTALCODE, '')) ||' '|| RTRIM(COALESCE(businesspartner.TOWN, '')) " \
          "||' '|| COALESCE(businesspartner.DISTRICT, '')) End " \
          ", COALESCE(ORDERPARTNERIE.PANNO,'') " \
          "order by  BusinessUnit, GLAccount, SubAccount"

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

        pdfADLSYS.textsize(pdfADLSYS.c, result, pdfADLSYS.d, stdt, etdt, LCEject, LCNarration, LCAddress)
        pdfADLSYS.d = pdfADLSYS.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfADLSYS.d < 40:
            pdfADLSYS.d = 740
            pdfADLSYS.c.showPage()
            pdfADLSYS.header(stdt, etdt, pdfADLSYS.divisioncode)

    if result == False:
        if counter > 0:

            # *************** total print  at End ******************
            pdfADLSYS.d = pdfADLSYS.dvalue()
            pdfADLSYS.c.setFont('Helvetica-Bold', 7)
            pdfADLSYS.c.drawString(230, pdfADLSYS.d, "Totals :")
            if float(pdfADLSYS.openingbalance) != 0:
                if float(pdfADLSYS.openingbalance) < 0:
                    pdfADLSYS.c.drawAlignedString(335, pdfADLSYS.d, str('{0:1.2f}'.format(-pdfADLSYS.openingbalance)) + ' CR')
                else:
                    pdfADLSYS.c.drawAlignedString(335, pdfADLSYS.d, str('{0:1.2f}'.format(pdfADLSYS.openingbalance)) + ' DR')
            else:
                pdfADLSYS.c.drawAlignedString(335, pdfADLSYS.d, str('{0:1.2f}'.format(pdfADLSYS.openingbalance)))
            pdfADLSYS.c.drawAlignedString(420, pdfADLSYS.d, str('{0:1.2f}'.format(pdfADLSYS.DRAmountTotal)))
            pdfADLSYS.c.drawAlignedString(495, pdfADLSYS.d, str('{0:1.2f}'.format(pdfADLSYS.CRAmountTotal)))
            if float(pdfADLSYS.ClosingBalance) != 0:
                if float(pdfADLSYS.ClosingBalance) < 0:
                    pdfADLSYS.c.drawAlignedString(570, pdfADLSYS.d, str('{0:1.2f}'.format(-pdfADLSYS.ClosingBalance)) + ' CR')
                else:
                    pdfADLSYS.c.drawAlignedString(570, pdfADLSYS.d, str('{0:1.2f}'.format(pdfADLSYS.ClosingBalance)) + ' DR')
            else:
                pdfADLSYS.c.drawAlignedString(570, pdfADLSYS.d, str('{0:1.2f}'.format(pdfADLSYS.ClosingBalance)))
            # ************************               **************************

            ADLV.Exceptions = ""
            counter = 0
        elif counter == 0:
            ADLV.Exceptions = "Note: No Report Form For Given Criteria"
            return

    pdfADLSYS.c.showPage()
    pdfADLSYS.c.save()

    pdfADLSYS.newrequest()
    pdfADLSYS.d = pdfADLSYS.newpage()