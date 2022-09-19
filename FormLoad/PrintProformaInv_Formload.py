from django.shortcuts import render
from Global_Files import Connection_String as con

Exceptions = ''

GDataCompany = []
GDataProformaInSummary = []

stmt = con.db.exec_immediate(con.conn,"select code,LONGDESCRIPTION  from FINBUSINESSUNIT  Where GROUPFLAG = 1  order by code")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)


def PrintProformaInvHtml(request):
    return render(request, 'PrintProformaInv.html',
                  {'GDataCompany': GDataCompany })


def PrintProformaInvGrid(request):
    global GDataProformaInSummary

    GDataProformaInSummary = []
    LSUnitCode = request.GET.getlist('unit')
    LDStartDate = "'" + str(request.GET['startdate']) + "'"
    LDEndDate = "'" + str(request.GET['enddate']) + "'"

    LCUnitCode = request.GET.getlist('allunit')

    unitcodes = str(LSUnitCode)
    LSUnitCodes = '(' + unitcodes[1:-1] + ')'
    ReportType = str(request.GET['type'])
    # print(ReportType)

    if not LSUnitCode and not LCUnitCode:
        Company = " "
    elif LCUnitCode:
        Company = " "
    elif LSUnitCode:
        Company = "AND Comp.CODE in " + str(LSUnitCodes)
        print(Company)
    # print(companyunitcode)
    if ReportType == 'ProformaInv':
        sql = "Select       DISTINCT(SO.CODE) as InvoiceNo " \
              ", VARCHAR_FORMAT(SO.ORDERDATE,'DD-MM-YYYY') as InvoiceDt " \
              "From    SALESORDER SO " \
              "Join SALESORDERLINE SOL                 On      SO.CODE = SOL.SALESORDERCODE " \
              "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE " \
              "And     SO.DOCUMENTTYPETYPE = SOL.DOCUMENTTYPETYPE " \
              "Join LOGICALWAREHOUSE                   On      SOL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
              "Join BUSINESSUNITVSCOMPANY BUC          On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE  " \
              "Join FINBUSINESSUNIT                          On      BUC.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
              "And     FINBUSINESSUNIT.GROUPFLAG = 0 " \
              "Join FINBUSINESSUNIT Comp                     On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
              "Where SO.ORDERDATE Between "+LDStartDate+" and "+LDEndDate+" "+Company+" " \
              "Order By  InvoiceNo ASC "

        # try:
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        # print(result)
        while result != False:
            GDataProformaInSummary.append(result)
            result = con.db.fetch_both(stmt)


        if GDataProformaInSummary == []:
            global Exceptions
            Exceptions = "Note: No Result found on given criteria "
            return render(request, 'PrintProformaInv.html',
                          {'GDataCompany': GDataCompany, 'Exception': Exceptions})
        else:
                return render(request, 'PrintProformaInv_Table.html',
                              {'GDataProformaInSummary': GDataProformaInSummary})

        # except:
        #     raise Exception("Please Run the Server Again ")

    elif ReportType == 'PackingLiPre':
        sql = "SELECT          DISTINCT(PLANTINVOICE.CODE) as InvoiceNo " \
               ", VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') as InvoiceDt " \
               "From PLANTINVOICE  " \
               "JOIN PLANTINVOICELINE                   ON 	PLANTINVOICELINE.PLANTINVOICECODE = PLANTINVOICE.CODE " \
               "AND 	PLANTINVOICELINE.PLANTINVOICEDIVISIONCODE = PLANTINVOICE.DIVISIONCODE " \
               "Join LOGICALWAREHOUSE                   On      PLANTINVOICELINE.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
               "Join BUSINESSUNITVSCOMPANY BUC          On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE " \
              "Join FINBUSINESSUNIT                          On      BUC.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
              "And     FINBUSINESSUNIT.GROUPFLAG = 0 " \
              "Join FINBUSINESSUNIT Comp                     On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
               "where   PLANTINVOICE.INVOICEDATE between " + LDStartDate + " and " + LDEndDate + " " + Company + " " \
               "Order By     InvoiceNo ASC "

        # try:
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        # print(result)
        while result != False:
            GDataProformaInSummary.append(result)
            result = con.db.fetch_both(stmt)

        if GDataProformaInSummary == []:
            # global Exceptions
            Exceptions = "Note: No Result found on given criteria "
            return render(request, 'PrintProformaInv.html',
                          {'GDataCompany': GDataCompany, 'Exception': Exceptions})

        else:
            return render(request, 'PrintProformaPrePackLis.html',
                          {'GDataProformaInSummary': GDataProformaInSummary})

            # elif ReportType == 'PackingLiPos':
            #     pass
            #
            # elif ReportType == 'CustomPre':
            #     return render(request, 'PrintProformaPreCustom.html',
            #                   {'GDataProformaInSummary': GDataProformaInSummary})
            #
            # elif ReportType == 'Commercial':
            #     pass
            #
            # elif ReportType == 'Instructions':
            #     pass
            #
            # elif ReportType == 'Certificate':
            #     pass
            #
            # else :
            #     pass

        # except:
        #     raise Exception ("Please Run the Server Again ")


    elif ReportType == 'CustomPre':
        sql = "SELECT          Distinct(PLANTINVOICE.CODE) as InvoiceNo " \
              ", VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') as InvoiceDt " \
              ", Coalesce(CUSTOMINVOICE.CODE ||'             DT:   '|| VARCHAR_FORMAT(CUSTOMINVOICE.INVOICEDATE,'DD-MM-YYYY'),'') As InvoiceNoAndDt " \
              "From PLANTINVOICE " \
              "Left Join CUSTOMINVOICE                      On      PlantInvoice.CUSTOMINVOICECODE = CUSTOMINVOICE.CODE " \
              "And     PlantInvoice.CUSTOMINVOICETYPECODE = CUSTOMINVOICE.INVOICETYPECODE " \
              "Left JOIN CUSTOMINVOICELINE  CIL             ON 	CUSTOMINVOICE.CODE = CIL.CUSTOMINVOICECODE " \
              "AND 	CUSTOMINVOICE.DIVISIONCODE = CIL.CUSTOMINVOICEDIVISIONCODE " \
              "Left Join LOGICALWAREHOUSE                   On      CIL.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
              "Left Join BUSINESSUNITVSCOMPANY BUC          On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE " \
              "Left Join FINBUSINESSUNIT                          On      BUC.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
              "And     FINBUSINESSUNIT.GROUPFLAG = 0 " \
              "Left Join FINBUSINESSUNIT Comp                     On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
              "where   PLANTINVOICE.INVOICEDATE between " + LDStartDate + " and " + LDEndDate + " " + Company + " " \
              "Order By     InvoiceNo ASC "

        # try:
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        # print(result)
        while result != False:
            GDataProformaInSummary.append(result)
            result = con.db.fetch_both(stmt)

        if GDataProformaInSummary == []:
            # global Exceptions
            Exceptions = "Note: No Result found on given criteria "
            return render(request, 'PrintProformaInv.html',
                          {'GDataCompany': GDataCompany, 'Exception': Exceptions})

        else:
            return render(request, 'PrintProformaPreCustom.html',
                              {'GDataProformaInSummary': GDataProformaInSummary})

    elif ReportType == 'Commercial':
        sql = "SELECT          Distinct(PLANTINVOICE.CODE) as InvoiceNo" \
              ", VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') as InvoiceDt " \
              ", Coalesce(CONCAT(COMMERCIALINVOICE.CODE,'  & ') ||'  DT:   '|| " \
              "VARCHAR_FORMAT(COMMERCIALINVOICE.INVOICEDATE,'DD-MM-YYYY'),'') As InvoiceNoAndDt " \
              "From PLANTINVOICE " \
              "Left JOIN COMMERCIALINVOICELINE           ON      PlantInvoice.CODE = COMMERCIALINVOICELINE.PLANTINVOICECODE " \
              "Left Join LOGICALWAREHOUSE                   On      COMMERCIALINVOICELINE.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
              "Left Join BUSINESSUNITVSCOMPANY BUC          On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE " \
              "Left Join COMMERCIALINVOICE                       ON      COMMERCIALINVOICELINE.COMMERCIALINVOICECODE = COMMERCIALINVOICE.CODE " \
              "AND     COMMERCIALINVOICELINE.COMMERCIALINVOICEDIVISIONCODE = COMMERCIALINVOICE.DIVISIONCODE " \
              "Left Join FINBUSINESSUNIT                          On      BUC.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
              "And     FINBUSINESSUNIT.GROUPFLAG = 0 " \
              "Left Join FINBUSINESSUNIT Comp                     On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
              "where   PLANTINVOICE.INVOICEDATE between " + LDStartDate + " and " + LDEndDate + " " + Company + " " \
              "Order By     InvoiceNo ASC "

        # try:
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        # print(result)
        while result != False:
            GDataProformaInSummary.append(result)
            result = con.db.fetch_both(stmt)

        if GDataProformaInSummary == []:
            # global Exceptions
            Exceptions = "Note: No Result found on given criteria "
            return render(request, 'PrintProformaInv.html',
                          {'GDataCompany': GDataCompany, 'Exception': Exceptions})

        else:
            return render(request, 'PrintProformaCommercial.html',
                          {'GDataProformaInSummary': GDataProformaInSummary})

    elif ReportType == 'Instructions':
        sql = "SELECT          DISTINCT(PLANTINVOICE.CODE) as InvoiceNo " \
              ", VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') as InvoiceDt " \
              "From PLANTINVOICE  " \
              "JOIN PLANTINVOICELINE                   ON 	PLANTINVOICELINE.PLANTINVOICECODE = PLANTINVOICE.CODE " \
              "AND 	PLANTINVOICELINE.PLANTINVOICEDIVISIONCODE = PLANTINVOICE.DIVISIONCODE " \
              "Join LOGICALWAREHOUSE                   On      PLANTINVOICELINE.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
              "Join BUSINESSUNITVSCOMPANY BUC          On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE " \
              "Join FINBUSINESSUNIT                          On      BUC.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
              "And     FINBUSINESSUNIT.GROUPFLAG = 0 " \
              "Join FINBUSINESSUNIT Comp                     On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
              "where   PLANTINVOICE.INVOICEDATE between " + LDStartDate + " and " + LDEndDate + " " + Company + " " \
                                                                                                                "Order By     InvoiceNo ASC "

        # try:
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        # print(result)
        while result != False:
            GDataProformaInSummary.append(result)
            result = con.db.fetch_both(stmt)

        if GDataProformaInSummary == []:
            # global Exceptions
            Exceptions = "Note: No Result found on given criteria "
            return render(request, 'PrintProformaInv.html',
                          {'GDataCompany': GDataCompany, 'Exception': Exceptions})

        else:
            return render(request, 'PrintProformaBLInstruction.html',
                          {'GDataProformaInSummary': GDataProformaInSummary})

    elif ReportType == 'Certificate':
        sql = "SELECT          DISTINCT(PLANTINVOICE.CODE) as InvoiceNo " \
              ", VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') as InvoiceDt " \
              "From PLANTINVOICE  " \
              "JOIN PLANTINVOICELINE                   ON 	PLANTINVOICELINE.PLANTINVOICECODE = PLANTINVOICE.CODE " \
              "AND 	PLANTINVOICELINE.PLANTINVOICEDIVISIONCODE = PLANTINVOICE.DIVISIONCODE " \
              "Join LOGICALWAREHOUSE                   On      PLANTINVOICELINE.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
              "Join BUSINESSUNITVSCOMPANY BUC          On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE  " \
              "Join FINBUSINESSUNIT                          On      BUC.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
              "And     FINBUSINESSUNIT.GROUPFLAG = 0 " \
              "Join FINBUSINESSUNIT Comp                     On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
              "where   PLANTINVOICE.INVOICEDATE between " + LDStartDate + " and " + LDEndDate + " " + Company + " " \
                                                                                                                "Order By     InvoiceNo ASC "

        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        # print(result)
        while result != False:
            GDataProformaInSummary.append(result)
            result = con.db.fetch_both(stmt)

        if GDataProformaInSummary == []:
            # global Exceptions
            Exceptions = "Note: No Result found on given criteria "
            return render(request, 'PrintProformaInv.html',
                          {'GDataCompany': GDataCompany, 'Exception': Exceptions})

        else:
            return render(request, 'PrintProformaCertficate.html',
                          {'GDataProformaInSummary': GDataProformaInSummary})

    else:
        sql = "SELECT          DISTINCT(PLANTINVOICE.CODE) as InvoiceNo " \
              ", VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') as InvoiceDt " \
              "From PLANTINVOICE  " \
              "JOIN PLANTINVOICELINE                   ON 	PLANTINVOICELINE.PLANTINVOICECODE = PLANTINVOICE.CODE " \
              "AND 	PLANTINVOICELINE.PLANTINVOICEDIVISIONCODE = PLANTINVOICE.DIVISIONCODE " \
              "Join LOGICALWAREHOUSE                   On      PLANTINVOICELINE.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
              "Join BUSINESSUNITVSCOMPANY BUC          On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE " \
              "Join FINBUSINESSUNIT                          On      BUC.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
              "And     FINBUSINESSUNIT.GROUPFLAG = 0 " \
              "Join FINBUSINESSUNIT Comp                     On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
              "where   PLANTINVOICE.INVOICEDATE between " + LDStartDate + " and " + LDEndDate + " " + Company + " " \
                                                                                                                "Order By     InvoiceNo ASC "

        # try:
        stmt = con.db.prepare(con.conn, sql)
        con.db.execute(stmt)
        result = con.db.fetch_both(stmt)
        # print(result)
        while result != False:
            GDataProformaInSummary.append(result)
            result = con.db.fetch_both(stmt)

        if GDataProformaInSummary == []:
            # global Exceptions
            Exceptions = "Note: No Result found on given criteria "
            return render(request, 'PrintProformaInv.html',
                          {'GDataCompany': GDataCompany, 'Exception': Exceptions})

        else:
            return render(request, 'PrintProformaAnex.html',
                          {'GDataProformaInSummary': GDataProformaInSummary})