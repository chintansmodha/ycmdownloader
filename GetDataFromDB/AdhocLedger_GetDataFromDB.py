import os
from datetime import datetime
from PrintPDF import AdhocLedger_PrintPDF as pdfADL
from Global_Files import Connection_String as con
from ProcessSelection import AdhocLedgerPDF_ProcessSelection as ADLV

counter = 0


def AdhocLedger_PrintPDF(LSCompanyUnitCode, LSAccountCode, LSSubAccountCode, LDStartDate, LDEndDate, LCAccountCode,
                         LCSubAccountCode, LCCompanyUnitCode, LCEject, LCNarration, LMMergeCompany, LMMergeSubAcc):
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"
    # ************* Merge Comp And Sub Account **************
    if LMMergeCompany == ['true']:
        mergecomp = '1'
    else:
        mergecomp = '0'

    if LMMergeSubAcc == ['true']:
        mergesubacc = '1'
    else:
        mergesubacc = '0'

    # ********************************************************

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

    sql = "Select     Case " + mergecomp + " When 1 Then 'Beekaylon Group Of Companies' When 0 Then FINBUSINESSUNIT.LONGDESCRIPTION End As BusinessUnit " \
          ", Case " + mergesubacc + " When 1 Then GLMASTER.LONGDESCRIPTION When 0 Then (Case COALESCE(BUSINESSPARTNER.LEGALNAME1,'') When BUSINESSPARTNER.LEGALNAME1 Then GLMASTER.LONGDESCRIPTION ||' - '|| " \
          "BUSINESSPARTNER.LEGALNAME1 Else GLMASTER.LONGDESCRIPTION End) End as GLAccount " \
          ", Case When FinDocument.FINANCEDOCUMENTDATE < " + startdate + " Then '' Else FINDOCUMENT.CODE End as VchNo " \
          ", Case When FinDocument.FINANCEDOCUMENTDATE < " + startdate + " Then '1900-01-01' Else FINDOCUMENT.FINANCEDOCUMENTDATE End as VchDate " \
          ", Case When FinDocument.FINANCEDOCUMENTDATE < " + startdate + " Then '' Else FINDOCUMENT.DOCUMENTTYPECODE End as TxnType " \
          ", Case When FinDocument.FINANCEDOCUMENTDATE < " + startdate + " Then '' Else COALESCE(FINDOCUMENT.CHEQUENUMBER,'') End as ChqNo " \
          ", cast(Sum(Case When FinDocument.FINANCEDOCUMENTDATE <" + startdate + " " \
          "Then FINDOCUMENTLINE.AMOUNTINCC Else 0 End)as decimal(18,2)) As OpBal " \
          ", cast(Sum(Case When FINDOCUMENTLINE.AMOUNTINCC > 0 And FinDocument.FINANCEDOCUMENTDATE " \
          "Between " + startdate + " And " + enddate + " Then FINDOCUMENTLINE.AMOUNTINCC Else 0 End)as decimal(18,2)) As DrAmount " \
          ", cast(Abs(Sum(Case When FINDOCUMENTLINE.AMOUNTINCC < 0 And FinDocument.FINANCEDOCUMENTDATE Between " + startdate + " And " + enddate + " " \
          "Then FINDOCUMENTLINE.AMOUNTINCC Else 0 End)) as decimal(18,2)) As CrAmount " \
          ", cast(Sum(FINDOCUMENTLINE.AMOUNTINCC) as decimal(18,2)) As ClBal " \
          ", '' as DocNo " \
          ", COALESCE(Varchar(NoteHdr.Note),'') As HdrRemarks " \
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
          "Left join businesspartner     on      ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID " \
          "Left Join Note As NoteHdr     On      FINDOCUMENT.AbsUniqueID = NoteHdr.FatherId " \
          "Where   FINDOCUMENT.FINANCEDOCUMENTDATE       <= " + enddate + " " + companyunitcode + " " + accountcode + " " + subaccountcode + " " \
          "And FinDocument.CURRENTSTATUS = '1'  " \
          "Group By Case " + mergecomp + " when 1 Then 'Beekaylon Group Of Companies' When 0 Then FINBUSINESSUNIT.LONGDESCRIPTION End" \
          ", COALESCE(Varchar(NoteHdr.Note),'') " \
          ", Case When FinDocument.FINANCEDOCUMENTDATE < " + startdate + " Then '' Else FINDOCUMENT.CODE End " \
          ", Case When FinDocument.FINANCEDOCUMENTDATE < " + startdate + " Then '1900-01-01' Else FINDOCUMENT.FINANCEDOCUMENTDATE End " \
          ", Case When FinDocument.FINANCEDOCUMENTDATE < " + startdate + " Then '' Else FINDOCUMENT.DOCUMENTTYPECODE End " \
          ", Case When FinDocument.FINANCEDOCUMENTDATE < " + startdate + " Then '' Else COALESCE(FINDOCUMENT.CHEQUENUMBER,'') End " \
          ", Case " + mergesubacc + " When 1 Then GLMASTER.LONGDESCRIPTION When 0 Then (Case COALESCE(BUSINESSPARTNER.LEGALNAME1,'') When BUSINESSPARTNER.LEGALNAME1 Then GLMASTER.LONGDESCRIPTION ||' - '|| " \
          "BUSINESSPARTNER.LEGALNAME1 Else GLMASTER.LONGDESCRIPTION End) End " \
          "order by  BusinessUnit, GLAccount, VchDate, VchNo"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfADL.textsize(pdfADL.c, result, pdfADL.d, stdt, etdt, LCEject, LCNarration, LMMergeCompany, LMMergeSubAcc)
        pdfADL.d = pdfADL.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfADL.d < 40:
            pdfADL.d = 740
            pdfADL.c.showPage()
            pdfADL.header(stdt, etdt, pdfADL.divisioncode, LMMergeCompany, LMMergeSubAcc)

    if result == False:
        if counter > 0:

            # *************** total print  at End ******************
            pdfADL.d = pdfADL.dvalue()
            # pdfADL.c.setFont('Helvetica-Bold', 7)
            # pdfADL.c.drawString(270, pdfADL.d, 'Totals :')
            # ******************** LINE *************************
            if LMMergeCompany == ['true']:
                pdfADL.d = pdfADL.dvalueIn()
                pdfADL.c.line(340, pdfADL.d, 500, pdfADL.d)
                pdfADL.d = pdfADL.dvalue()
                pdfADL.d = pdfADL.dvalue()
                pdfADL.c.setFont('Helvetica-Bold', 7)
                pdfADL.c.drawAlignedString(480, pdfADL.d, str('{0:1.2f}'.format(pdfADL.CRAmountTotal)))
                pdfADL.c.drawAlignedString(390, pdfADL.d, str('{0:1.2f}'.format(pdfADL.DRAmountTotal)))
            # ****************************************************
            else:
                pdfADL.c.setFont('Helvetica-Bold', 7)
                pdfADL.c.drawString(270, pdfADL.d, 'Totals :')
                if float(pdfADL.CRAmountTotal) != 0:
                    pdfADL.c.drawAlignedString(480, pdfADL.d, str('{0:1.2f}'.format(pdfADL.CRAmountTotal)))
                if float(pdfADL.DRAmountTotal) != 0:
                    pdfADL.c.drawAlignedString(390, pdfADL.d, str('{0:1.2f}'.format(pdfADL.DRAmountTotal)))
                if float(pdfADL.openingbalance) != 0:
                    if float(pdfADL.openingbalance) > 0:
                        pdfADL.c.drawAlignedString(570, pdfADL.d, str('{0:1.2f}'.format(pdfADL.openingbalance)) + ' DR')
                    else:
                        pdfADL.c.drawAlignedString(570, pdfADL.d, str('{0:1.2f}'.format(-pdfADL.openingbalance)) + ' CR')
                else:
                    pdfADL.c.drawAlignedString(570, pdfADL.d, str('{0:1.2f}'.format(pdfADL.openingbalance)))
            # ******************** LINE End *************************
            if LMMergeCompany == ['true']:
                pdfADL.d = pdfADL.dvalue()
                pdfADL.c.line(340, pdfADL.d, 500, pdfADL.d)
            # ****************************************************
            pdfADL.CompanyAmtclean()
            # ************************               **************************

            ADLV.Exceptions = ""
            counter = 0
        elif counter == 0:
            ADLV.Exceptions = "Note: No Report Form For Given Criteria"
            return

    pdfADL.c.showPage()
    pdfADL.c.save()

    pdfADL.newrequest()
    pdfADL.d = pdfADL.newpage()