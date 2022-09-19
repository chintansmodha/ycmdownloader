import os
from datetime import datetime

from babel.numbers import format_currency
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.static import serve

from PrintPDF import SalesRegister_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
from FormLoad import  SalesRegister_FormLoad as views

from django.http import FileResponse
Exceptions = ""

counter = 0


def SalesRegister(request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Sales Register/",
    #                          LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    LSItemTypecode = request.GET.getlist('selitemtype')
    LSCostcentercode = request.GET.getlist('selcostcenter')
    LSPartycode = request.GET.getlist('selparty')
    LSUnitcode = request.GET.getlist('selunit')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])
    LSRegisterType = str(request.GET['CboRegisterType'])
    # LSReportType = str(request.GET['CboReportType'])
    LSReportType = ''
    try:
        LSallUnit = str(request.GET['allunit'])
    except MultiValueDictKeyError:
        LSallUnit = False
    try:
        LSallParty = str(request.GET['allparty'])
    except MultiValueDictKeyError:
        LSallParty = False
    try:
        LSallCostcenter = str(request.GET['allcostcenter'])
    except MultiValueDictKeyError:
        LSallCostcenter = False
    try:
        LSallItemtype = str(request.GET['allitemtype'])
    except MultiValueDictKeyError:
        LSallItemtype = False

    if LSRegisterType=='0':
        GSTRegisterPrintPDF(LSUnitcode, LSItemTypecode, LSCostcentercode, LSPartycode, LDStartDate, LDEndDate, LSFileName,
                            LSRegisterType, LSallUnit, LSallCostcenter, LSallItemtype, LSallParty)
    elif LSRegisterType == '2':
        ChargesSummaryPrintPDF(LSUnitcode, LSItemTypecode, LSCostcentercode, LSPartycode, LDStartDate, LDEndDate,
                               LSFileName,
                               LSRegisterType, LSallUnit, LSallCostcenter, LSallItemtype, LSallParty)
    elif LSRegisterType=='1':
        ItemSummaryPrintPDF(LSUnitcode, LSItemTypecode, LSCostcentercode, LSPartycode, LDStartDate, LDEndDate, LSFileName,
                            LSRegisterType, LSallUnit, LSallCostcenter, LSallItemtype, LSallParty)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'SalesRegister.html',
                      {'unit': views.unit, 'costcenter': views.costcenter, 'party': views.party,
                       'itemtype': views.itemtype,
                       'code': views.code, 'ccode': views.ccode, 'Exception': Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response




def GSTRegisterPrintPDF(LSUnitcode, LSItemTypecode, LSCostcentercode, LSPartycode, LDStartDate, LDEndDate, LSFileName,
                        LSRegisterType, LSallUnit, LSallCostcenter, LSallItemtype, LSallParty):
    itemcode = str(LSItemTypecode)
    unitcode = str(LSUnitcode)
    partycode = str(LSPartycode)

    rows=500
    cols = 500
    invoicecounter = []
    result = ''
    result1 = ''
    result2 = ''
    stmt = ''
    stmt1 = ''
    stmt2 = ''
    sql = ''
    print("Register type : " + LSRegisterType)

    sqlwhere = ''
    sqlunit = ''
    sqlcostcenter = ''
    sqlparty = ''
    sqlitemtype = ''

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    allunit = str(LSallUnit)
    if allunit == 'None' and len(unitcode) != 0 or str(LSallUnit) == 'False':
        unit = str(unitcode)
        LSUnitcode = '(' + unit[1:-1] + ')'
        sqlwhere += ' AND PLANTINVOICE.FactoryCODE IN  ' + LSUnitcode

    allitemtype = str(LSallItemtype)
    if allitemtype == 'None' and len(itemcode) != 0 or str(LSallItemtype) == 'False':
        item = str(itemcode)
        LSItemTypecode = '(' + item[1:-1] + ')'
        sqlwhere += ' AND PLANTINVOICELINE.ITEMTYPECODE  IN  ' + LSItemTypecode

    allparty = str(LSallParty)
    if allparty == 'None' and len(partycode) != 0 or str(LSallParty) == 'False':
        party = str(partycode)
        LSPartycode = '(' + party[1:-1] + ')'
        sqlwhere += ' AND ORDERPARTNER.CUSTOMERSUPPLIERCODE IN ' + LSPartycode

    sql = "SELECT   " \
          "                   PlantInvoice.CODE AS INVOICENO " \
          "                   , Plant.LongDescription As Plant " \
          "                   , PlantInvoice.AbsUniqueId As InvoiceAbsUniqueId " \
          "                   , PlantInvoiceLine.AbsUniqueId As ProductAbsUniqueId " \
          "                   , PLANTINVOICE.INVOICEDATE AS INVDATE " \
          "                   , BusinessPartner.LegalName1 As Buyer " \
          "                   , AGENT.LONGDESCRIPTION AS BROKER " \
          "                   , QUALITYLEVEL.LONGDESCRIPTION AS QUALITY " \
          "                   , PLANTINVOICELINE.PRIMARYQTY AS QUANTITY " \
          "                   , Product.LONGDESCRIPTION As Product " \
          "                   , (Select calculatedvalue From IndTaxDetail Where AbsUniqueID = PLANTINVOICELINE.AbsUniqueID And ITaxCOde = 'INR' And TaxCategoryCode = 'OTH') AS RATE " \
          "                   , (Select calculatedvalue From IndTaxDetail Where AbsUniqueID = PLANTINVOICELINE.AbsUniqueID And ITaxCOde = '998' And TaxCategoryCode = 'OTH') AS BasicValue " \
          "                   , PLANTINVOICE.DIVISIONCODE " \
          "                   , NettValue As InvoiceAmount " \
          "                   , PLANTINVOICE.LRNO  AS LRNO " \
          "                   , PLANTINVOICE.LRDATE AS LRDATE " \
          "                   , Product.LONGDESCRIPTION As Product " \
          "                   , DIVISION.LONGDESCRIPTION AS DIVI " \
          "                   ,count(*) over(partition by PlantInvoice.CODE)  as TOTALITEM " \
          "           FROM    PlantInvoice " \
          "                   JOIN ORDERPARTNER       ON PLANTINVOICE.BUYERIFOTCCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE " \
          "                                           AND  PLANTINVOICE.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OrderPartner.CUSTOMERSUPPLIERTYPE " \
          "                   Join BusinessPartner    ON  OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId " \
          "                   Left JOIN AGENT              ON PLANTINVOICE.AGENT1CODE = AGENT.CODE " \
          "                   JOIN PLANTINVOICELINE   ON PLANTINVOICE.CODE = PLANTINVOICELINE.PLANTINVOICECODE " \
          "                                          And PLANTINVOICE.DivisionCODE = PLANTINVOICELINE.PLANTINVOICEDivisionCODE " \
          "                                           And PLANTINVOICE.InvoiceDate = PLANTINVOICELINE.InvoiceDate " \
          "                   JOIN QUALITYLEVEL       ON PLANTINVOICELINE.QUALITYLEVELCODE = QUALITYLEVEL.CODE " \
          "                                           And PLANTINVOICELINE.ITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          "                   JOIN  DIVISION          ON DIVISION.CODE = PLANTINVOICE.DIVISIONCODE " \
          "                   JOIN LOGICALWAREHOUSE   ON      PlantInvoiceLine.LogicalWarehouseCode           = LOGICALWAREHOUSE.Code " \
          "                   JOIN Plant              ON      LOGICALWAREHOUSE.PLANTCODE                      = PLANT.CODE " \
          "                   JOIN PRODUCT            ON PLANTINVOICELINE.ITEMTYPECODE = PRODUCT.ITEMTYPECODE " \
          "                   AND     COALESCE(PLANTINVOICELINE.SubCode01, '') = COALESCE(Product.SubCode01, '') " \
          "                   AND     COALESCE(PLANTINVOICELINE.SubCode02, '') = COALESCE(Product.SubCode02, '') " \
          "                   AND     COALESCE(PLANTINVOICELINE.SubCode03, '') = COALESCE(Product.SubCode03, '') " \
          "                   AND     COALESCE(PLANTINVOICELINE.SubCode04, '') = COALESCE(Product.SubCode04, '') " \
          "                   AND     COALESCE(PLANTINVOICELINE.SubCode05, '') = COALESCE(Product.SubCode05, '') " \
          "                   AND     COALESCE(PLANTINVOICELINE.SubCode06, '') = COALESCE(Product.SubCode06, '') " \
          "                   AND     COALESCE(PLANTINVOICELINE.SubCode07, '') = COALESCE(Product.SubCode07, '') " \
          "                   AND     COALESCE(PLANTINVOICELINE.SubCode08, '') = COALESCE(Product.SubCode08, '') " \
          "                   AND     COALESCE(PLANTINVOICELINE.SubCode09, '') = COALESCE(Product.SubCode09, '') " \
          "                   AND     COALESCE(PLANTINVOICELINE.SubCode10, '') = COALESCE(Product.SubCode10, '') " \
          " WHERE PLANTINVOICE.INVOICEDATE between '" + str(stdt) + "' and '" + str(etdt) + "' " + sqlwhere + " " \
          " ORDER BY PlantInvoice.CODE,  Product.LONGDESCRIPTION "

    # print(sql)


    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    productcounter=1
    # temptotal=1
    # numberofproductsin_invoice=float(result['TOTALITEM'])
    numberofproductsin_invoice=1
    # print(result['TOTALITEM'])
    # pdfrpt.header(stdt, etdt, pdfrpt.plantname)
    while result != False:
        global counter
        counter = counter + 1
        flag = pdfrpt.invoicenocounter
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        # pdfrpt.header(stdt, etdt, pdfrpt.divisioncode)
        getproducttaxdetail(result)
        if productcounter==numberofproductsin_invoice:
            getinvoicetaxdetail(result)
            productcounter=0
            temptotal=0
            print("productcounter == 1  :" +str(productcounter))
            print()
        else:
            productcounter=productcounter+1
            print("productcounter != 1  :" + str(productcounter))

        result = con.db.fetch_both(stmt)
        print("temptotal****")

        if pdfrpt.d < 14:
            pdfrpt.d = 480
            pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
            pdfrpt.c.showPage()
            pdfrpt.header(stdt, etdt, pdfrpt.plantname)
            pdfrpt.d = pdfrpt.d
            print("after heafder-")
        else :
            print("else")

        try:
            numberofproductsin_invoice =float(result['TOTALITEM'])
        except:
            pass
        print("numberofproductsin_invoice : "+str(numberofproductsin_invoice))
    # getinvoicetaxdetail(result)
    print(LSRegisterType)
    if result == False and LSRegisterType == '0':
    # if LSRegisterType == 0:
        pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
        pdfrpt.fonts(10)    # pdfrpt.c.drawString(60, pdfrpt.d, str(pdfrpt.itemcode[-1]) + " TOTAL : ")
        # pdfrpt.c.drawAlignedString(200, pdfrpt.d, "Gross Amount : " + str("%.3f" % float(pdfrpt.GrossAmountTotal)))
        # pdfrpt.c.drawAlignedString(200, pdfrpt.d, "Total number of Invoice : " + str("%.3f" % float(counter)))
        pdfrpt.c.drawString(110, pdfrpt.d, "Total : ")
        pdfrpt.c.drawCentredString(565, pdfrpt.d, str(("%.0f" % float(pdfrpt.TotalBoxes))))
        pdfrpt.c.drawAlignedString(625, pdfrpt.d, str(("%.3f" % float(pdfrpt.Totalquantity))))
        pdfrpt.c.drawAlignedString(810, pdfrpt.d ,
                                       "" + str("%.2f" % float(pdfrpt.InvoiceAmountTotal)))
        pdfrpt.itemcodeclean()

        pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)

        pdfrpt.fonts(8)
        pdfrpt.companyclean()
        # pdfrpt.pageno = 0
    # if result == False:
    #     pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
    #     pdfrpt.fonts(10)
    #
    #     # pdfrpt.c.drawString(60, pdfrpt.d, str(pdfrpt.itemcode[-1]) + " TOTAL : ")
    #     pdfrpt.c.drawAlignedString(200, pdfrpt.d, "Total number of Invoice : " + str("%.3f" % float(counter)))
    #     pdfrpt.c.drawAlignedString(300, pdfrpt.d, "Gross Amount : " + str("%.3f" % float(pdfrpt.GrossAmountTotal)))
    #     pdfrpt.c.drawAlignedString(770, pdfrpt.d - 15,
    #                                "Invoice Amount : " + str("%.2f" % float(pdfrpt.InvoiceAmountTotal)))
    #     pdfrpt.itemcodeclean()
    #
    #     pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
    #
    #     pdfrpt.fonts(8)
    #     pdfrpt.companyclean()

    if counter == 0:
        global Exceptions
        Exceptions = "Note: No Result found according to your selected criteria "
    else:
        Exceptions = ""
        pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
        pdfrpt.c.save()
        # url = "file:///D:/Reports/ReportDevelopment/" + LSFileName + ".pdf"
        # os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()

def getproducttaxdetail(result):  # product level
    temp=0
    sqlproduct="Select ITax.LongDescription As ITaxName, IndTaxDetail.Value As TaxRate, IndTaxDetail.CalculatedValue As TaxAmount " \
               "From    IndTaxDetail, ITax " \
               "Where   IndTaxDetail.ABsUniqueID = "+str(result['PRODUCTABSUNIQUEID'])+" " \
               "And     IndTaxDetail.TaxCategoryCode = 'GST' " \
               "And     IndTaxDetail.ITaxCode = Itax.Code " \
               "And IndTaxDetail.CalculatedValue <> 0 " \
               "ORder By IndTaxDetail.SequenceNo "
    stmt = con.db.prepare(con.conn, sqlproduct)
    con.db.execute(stmt)
    resultproduct = con.db.fetch_both(stmt)
    print(resultproduct)

    while resultproduct != False:
        # print(result)
        global counter
        counter = counter + 1
        pdfrpt.producttaxdetails(pdfrpt.c, resultproduct, pdfrpt.d )
        resultproduct = con.db.fetch_both(stmt)


def getinvoicetaxdetail(result):     # invocie document level
    sqlinvoice="Select  ITax.LongDescription As ITaxName, IndTaxTotal.* " \
               "From    IndTaxTotal, ITax " \
               "Where   IndTaxTotal.ABsUniqueID = "+str(result['INVOICEABSUNIQUEID'])+" " \
               "And     IndTaxTotal.ITaxCode = Itax.Code " \
               "And     ( " \
               "                IndTaxTotal.TaxCategoryCode In ('FRT','INS','TCS') OR " \
               "                (IndTaxTotal.TaxCategoryCode = 'OTH' And ITax.FormTypeCode = 'ROF') " \
               "        )" \
              "And IndTaxTotal.Calculatedvaluercc <> 0 " \
               "ORder By IndTaxTotal.SequenceNo "
    stmt = con.db.prepare(con.conn, sqlinvoice)
    con.db.execute(stmt)
    resultinvoice = con.db.fetch_both(stmt)
    # print(resultinvoice)

    while resultinvoice != False:
        # print(result)
        global counter
        counter = counter + 1
        pdfrpt.invoicetaxdetails(pdfrpt.c, resultinvoice, pdfrpt.d )
        resultinvoice = con.db.fetch_both(stmt)

def ItemSummaryPrintPDF(LSUnitcode, LSItemTypecode, LSCostcentercode, LSPartycode, LDStartDate, LDEndDate, LSFileName,
                        LSRegisterType, LSallUnit, LSallCostcenter, LSallItemtype, LSallParty):
    itemcode = str(LSItemTypecode)
    unitcode = str(LSUnitcode)
    partycode = str(LSPartycode)
    result = ''
    result1 = ''
    result2 = ''
    stmt = ''
    stmt1 = ''
    stmt2 = ''
    sql = ''
    # print("Register type : " + LSRegisterType)
    # costcentercode = str(LSCostcentercode)
    # registertype = str(LSRegisterType)
    # reporttype = str(LSReportType)
    # allunit = str(LSallUnit)
    # allparty = str(LSallParty)
    # allitemtype = str(LSallItemtype)
    # allcostcenter = str(LSallCostcenter)

    # print("item code : - "+itemcode)
    # print("unit code : - "+unitcode)
    # print("party code : - "+partycode)

    # print("all item  : - "+ str(LSallItemtype))
    # print("all unit  : - "+ str(LSallUnit))
    # print("all party  : - "+ str(LSallParty))

    sqlwhere = ''
    sqlunit = ''
    sqlcostcenter = ''
    sqlparty = ''
    sqlitemtype = ''

    # PLANTINVOICE.FactoryCODE  IN
    # PLANTINVOICELINE.ITEMTYPECODE  IN
    # PLANTINVOICE.CUSTOMERSUPPLIERCODE IN
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    allunit = str(LSallUnit)
    if allunit == 'None' and len(unitcode) != 0 or str(LSallUnit) == 'False':
        # if sqlwhere != '':
        #     sqlwhere += ' AND '
        unit = str(unitcode)
        LSUnitcode = '(' + unit[1:-1] + ')'
        sqlwhere += ' AND PLANTINVOICE.FactoryCODE IN  ' + LSUnitcode
        # print('sqlwhere in Plant : ' + sqlwhere)

    allitemtype = str(LSallItemtype)
    if allitemtype == 'None' and len(itemcode) != 0 or str(LSallItemtype) == 'False':
        # if sqlwhere != '':
        #     sqlwhere += ' AND '
        item = str(itemcode)
        LSItemTypecode = '(' + item[1:-1] + ')'
        sqlwhere += ' AND PLANTINVOICELINE.ITEMTYPECODE  IN  ' + LSItemTypecode
        # print('sqlwhere in Itemtype code  : ' + sqlwhere)

    allparty = str(LSallParty)
    if allparty == 'None' and len(partycode) != 0 or str(LSallParty) == 'False':
        # if sqlwhere != '':
        #     sqlwhere += ' AND '
        party = str(partycode)
        LSPartycode = '(' + party[1:-1] + ')'
        # sqlwhere += ' AND PLANTINVOICE.CUSTOMERSUPPLIERCODE IN  ' + LSPartycode
        sqlwhere += ' AND ORDERPARTNER.CUSTOMERSUPPLIERCODE IN ' + LSPartycode
        # print('sqlwhere in Customet supperlier code  : ' + sqlwhere)

    sql = "SELECT" \
          " DIVISION.LONGDESCRIPTION AS DIVI " \
          ", Plant.LongDescription As Plant " \
          ", PRODUCT.LONGDESCRIPTION As Product " \
          ", QUALITYLEVEL.LONGDESCRIPTION AS QUALITY " \
          ", PLANTINVOICELINE.BASEPRIMARYUMCODE as UNIT, " \
          " Sum(PLANTINVOICELINE.PRIMARYQTY) AS QUANTITY, " \
          " Sum(PLANTINVOICELINE.BasicVALUE)  AS BasicAmount " \
          " , count(*)  bills  " \
          "FROM    PlantInvoice " \
          "        JOIN ORDERPARTNER       ON PLANTINVOICE.BUYERIFOTCCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE " \
          "                                AND  PLANTINVOICE.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OrderPartner.CUSTOMERSUPPLIERTYPE " \
          "        Join BusinessPartner    ON  OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId " \
          "        JOIN PLANTINVOICELINE   ON PLANTINVOICE.CODE = PLANTINVOICELINE.PLANTINVOICECODE " \
          "                                And PLANTINVOICE.DivisionCODE = PLANTINVOICELINE.PLANTINVOICEDivisionCODE " \
          "                                And PLANTINVOICE.InvoiceDate = PLANTINVOICELINE.InvoiceDate " \
          "        JOIN QUALITYLEVEL       ON PLANTINVOICELINE.QUALITYLEVELCODE = QUALITYLEVEL.CODE " \
          "                                And PLANTINVOICELINE.ITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          "        JOIN  DIVISION          ON DIVISION.CODE = PLANTINVOICE.DIVISIONCODE " \
          "        JOIN LOGICALWAREHOUSE   ON      PlantInvoiceLine.LogicalWarehouseCode           = LOGICALWAREHOUSE.CODE " \
          "        JOIN Plant              ON      LOGICALWAREHOUSE.PLANTCODE                      = PLANT.CODE " \
          "        JOIN PRODUCT            ON PLANTINVOICELINE.ITEMTYPECODE = PRODUCT.ITEMTYPECODE  " \
          "             AND COALESCE(PLANTINVOICELINE.SubCode01,'') = COALESCE(Product.SubCode01,'') " \
          "             AND COALESCE(PLANTINVOICELINE.SubCode02,'') = COALESCE(Product.SubCode02,'') " \
          "             AND COALESCE(PLANTINVOICELINE.SubCode03,'') = COALESCE(Product.SubCode03,'') " \
          "             AND COALESCE(PLANTINVOICELINE.SubCode04,'') = COALESCE(Product.SubCode04,'') " \
          "             AND COALESCE(PLANTINVOICELINE.SubCode05,'') = COALESCE(Product.SubCode05,'') " \
          "             AND COALESCE(PLANTINVOICELINE.SubCode06,'') = COALESCE(Product.SubCode06,'') " \
          "             AND COALESCE(PLANTINVOICELINE.SubCode07,'') = COALESCE(Product.SubCode07,'') " \
          "             AND COALESCE(PLANTINVOICELINE.SubCode08,'') = COALESCE(Product.SubCode08,'') " \
          "             AND COALESCE(PLANTINVOICELINE.SubCode09,'') = COALESCE(Product.SubCode09,'') " \
          "             AND COALESCE(PLANTINVOICELINE.SubCode10,'') = COALESCE(Product.SubCode10,'') " \
          " WHERE PLANTINVOICE.INVOICEDATE between '" + str(stdt) + "' and '" + str(etdt)  + "' "+sqlwhere+" " \
          " GROUP BY DIVISION.LONGDESCRIPTION, PRODUCT.LONGDESCRIPTION," \
          " QUALITYLEVEL.LONGDESCRIPTION, PLANTINVOICELINE.BASEPRIMARYUMCODE,DIVISION.LONGDESCRIPTION,PRODUCT.LONGDESCRIPTION,Plant.Longdescription "
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print("===============================")
    # print(result)
    # print("===============================")

    while result != False:
        # print(result)
        global counter
        counter = counter + 1
        # print("counter  : "+str(counter))
        flag = 1
        pdfrpt.textsize2(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        # pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)
        # pdfrpt.c.line(0, 12, 600, 12)
        if pdfrpt.d < 14:
            pdfrpt.d = 480
            pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
            pdfrpt.c.showPage()
            pdfrpt.header2(stdt, etdt, pdfrpt.plantname)
            # pdfrpt.d = pdfrpt.d - 10



    # pdfrpt.c.drawString(10, pdfrpt.d, str(pdfrpt.divisioncode[-2]) + " TOTAL : ")
    # pdfrpt.c.drawAlignedString(225, pdfrpt.d, str("%.3f" % float(pdfrpt.CompanyQuentityTotal)))
    # pdfrpt.c.drawAlignedString(300, pdfrpt.d, str("%.2f" % float(pdfrpt.CompanyAmountTotal)))
    pdfrpt.companyclean()

    if result == False:
        pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
        pdfrpt.fonts(10)

        pdfrpt.c.drawString(260, pdfrpt.d,  " TOTAL : ")
        pdfrpt.c.drawAlignedString(380, pdfrpt.d,   str("%.3f" % float(pdfrpt.Totalquantity)))
        pdfrpt.c.drawAlignedString(785, pdfrpt.d, str("%.0f" % float(counter)))
        # pdfrpt.c.drawAlignedString(540, pdfrpt.d, "Basic Amount:      "+ str(format_currency("%.2f" % float(pdfrpt.BasicAmount), '', locale='en_IN')))
        pdfrpt.c.drawAlignedString(540, pdfrpt.d,  str(format_currency("%.2f" % float(pdfrpt.BasicAmount), '', locale='en_IN')))

        # pdfrpt.c.drawAlignedString(770, pdfrpt.d - 15, "Invoice Amount : " + str("%.2f" % float(pdfrpt.InvoiceAmountTotal)))
        pdfrpt.itemcodeclean()

        pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)

        pdfrpt.fonts(8)
        # pdfrpt.c.drawString(10, pdfrpt.d, str(pdfrpt.divisioncode[-2]) + " TOTAL : ")
        # pdfrpt.c.drawAlignedString(225, pdfrpt.d, str("%.3f" % float(pdfrpt.CompanyQuentityTotal)))
        # pdfrpt.c.drawAlignedString(300, pdfrpt.d, str("%.2f" % float(pdfrpt.CompanyAmountTotal)))
        pdfrpt.companyclean()
        # pdfrpt.pageno = 0

    if counter == 0:
        global Exceptions
        Exceptions = "Note: No Result found according to your selected criteria "
    else:
        Exceptions = ""
        pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
        pdfrpt.c.save()
        # url = "file:///D:/Reports/ReportDevelopment/" + LSFileName + ".pdf"
        # os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()

def ChargesSummaryPrintPDF(LSUnitcode, LSItemTypecode, LSCostcentercode, LSPartycode, LDStartDate, LDEndDate, LSFileName,
                           LSRegisterType, LSallUnit, LSallCostcenter, LSallItemtype, LSallParty):
    itemcode = str(LSItemTypecode)
    unitcode = str(LSUnitcode)
    partycode = str(LSPartycode)
    result = ''
    result1 = ''
    result2 = ''
    stmt = ''
    stmt1 = ''
    stmt2 = ''
    sql = ''
    print("Register type : " + LSRegisterType)

    sqlwhere = ''
    sqlunit = ''
    sqlcostcenter = ''
    sqlparty = ''
    sqlitemtype = ''

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    allunit = str(LSallUnit)
    if allunit == 'None' and len(unitcode) != 0 or str(LSallUnit) == 'False':
        unit = str(unitcode)
        LSUnitcode = '(' + unit[1:-1] + ')'
        sqlwhere += ' AND PLANTINVOICE.FactoryCODE IN  ' + LSUnitcode

    allitemtype = str(LSallItemtype)
    if allitemtype == 'None' and len(itemcode) != 0 or str(LSallItemtype) == 'False':
        item = str(itemcode)
        LSItemTypecode = '(' + item[1:-1] + ')'
        sqlwhere += ' AND PLANTINVOICELINE.ITEMTYPECODE  IN  ' + LSItemTypecode

    allparty = str(LSallParty)
    if allparty == 'None' and len(partycode) != 0 or str(LSallParty) == 'False':
        party = str(partycode)
        LSPartycode = '(' + party[1:-1] + ')'
        sqlwhere += ' AND ORDERPARTNER.CUSTOMERSUPPLIERCODE IN ' + LSPartycode


    sql = "SELECT " \
          "   DIVISION.LONGDESCRIPTION AS DIVI, " \
          "   Plant.Longdescription as plant, " \
          "   QUALITYLEVEL.LONGDESCRIPTION AS QUALITY, " \
          "   PLANTINVOICELINE.BASEPRIMARYUMCODE AS UMCODE, " \
          "   IndTaxDETAIL.LONGDESCRIPTION AS TAXDETAILS, " \
          "   sum(PLANTINVOICE.NETTWEIGHT) AS NETWEIGHT, " \
          "   sum(INDTAXTOTAL.CALCULATEDVALUERCC) AS TAXAMOUNT, " \
          "   Sum(PLANTINVOICELINE.PRIMARYQTY) AS QUANTITY, " \
          "   Sum(PLANTINVOICELINE.BasicVALUE) AS BasicAmount, " \
          "   Sum(PLANTINVOICELINE.GrossValue) AS GrossAmount, " \
          "   count(*) bills " \
          "FROM    PlantInvoice " \
          "   JOIN ORDERPARTNER " \
          "      ON PLANTINVOICE.BUYERIFOTCCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE  " \
          "      AND PLANTINVOICE.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OrderPartner.CUSTOMERSUPPLIERTYPE " \
          "   Join BusinessPartner  " \
          "      ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId " \
          "   JOIN       PLANTINVOICELINE " \
          "      ON PLANTINVOICE.CODE = PLANTINVOICELINE.PLANTINVOICECODE  " \
          "      And PLANTINVOICE.DivisionCODE = PLANTINVOICELINE.PLANTINVOICEDivisionCODE  " \
          "      And PLANTINVOICE.InvoiceDate = PLANTINVOICELINE.InvoiceDate  " \
          "   JOIN      QUALITYLEVEL  " \
          "      ON PLANTINVOICELINE.QUALITYLEVELCODE = QUALITYLEVEL.CODE  " \
          "      And PLANTINVOICELINE.ITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          "   JOIN       DIVISION  " \
          "      ON DIVISION.CODE = PLANTINVOICE.DIVISIONCODE  " \
          "   JOIN       INDTAXTOTAL  " \
          "      ON PlantInvoice.AbsUniqueId = IndTaxTotal.AbsUniqueId  " \
          "      AND IndTaxTotal.TaxCategoryCode In       ( 'GST', 'FRT', 'INS', 'TCS', 'OTH') " \
          "      AND INDTAXTOTAL.CALCULATEDVALUERCC <> 0  " \
          "   JOIN IndTaxDETAIL " \
          "      ON IndTaxTotal.AbsUniqueId = IndTaxDETAIL.ABSUNIQUEID  " \
          "      AND Indtaxtotal.TaxCategoryCode = indtaxdetail.TaxCategoryCode  " \
          "   JOIN       LOGICALWAREHOUSE  " \
          "      ON PlantInvoiceLine.LogicalWarehouseCode = LOGICALWAREHOUSE.code  " \
          "   JOIN      Plant  " \
          "      ON LOGICALWAREHOUSE.PLANTCODE = PLANT.CODE  " \
          "   JOIN      PRODUCT  " \
          "      ON PLANTINVOICELINE.ITEMTYPECODE = PRODUCT.ITEMTYPECODE  " \
          "      AND COALESCE(PLANTINVOICELINE.SubCode01, '') = COALESCE(Product.SubCode01, '')  " \
          "      AND COALESCE(PLANTINVOICELINE.SubCode02, '') = COALESCE (Product.SubCode02, '')  " \
          "      AND COALESCE(PLANTINVOICELINE.SubCode03, '') = COALESCE(Product.SubCode03, '')  " \
          "      AND COALESCE(PLANTINVOICELINE.SubCode04, '') = COALESCE(Product.SubCode04, '')  " \
          "      AND COALESCE(PLANTINVOICELINE.SubCode05, '') = COALESCE(Product.SubCode05, '')  " \
          "      AND COALESCE(PLANTINVOICELINE.SubCode06, '') = COALESCE(Product.SubCode06, '')  " \
          "      AND COALESCE(PLANTINVOICELINE.SubCode07, '') = COALESCE(Product.SubCode07, '')  " \
          "      AND COALESCE(PLANTINVOICELINE.SubCode08, '') = COALESCE(Product.SubCode08, '')  " \
          "      AND COALESCE(PLANTINVOICELINE.SubCode09, '') = COALESCE(Product.SubCode09, '')  " \
          "      AND COALESCE(PLANTINVOICELINE.SubCode10, '') = COALESCE(Product.SubCode10, '') " \
          "WHERE            PLANTINVOICE.INVOICEDATE between '" + str(stdt) + "' and '" + str(etdt)  + "' "+sqlwhere+" " \
          "GROUP BY  " \
          "   DIVISION.LONGDESCRIPTION, " \
          "   QUALITYLEVEL.LONGDESCRIPTION, " \
          "   PLANTINVOICELINE.BASEPRIMARYUMCODE, " \
          "   IndTaxDETAIL.LONGDESCRIPTION, " \
          "   Plant.Longdescription "

    print(sql)
    stmt = con.db.prepare(con.conn, sql )
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print("===============================")
    print(result)
    print("===============================")

    while result != False:
        # print(result)
        global counter
        counter = counter + 1
        pdfrpt.textsize1(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        result = con.db.fetch_both(stmt)
        # # pdfrpt.c.line(0, 12, 600, 12)
        # if pdfrpt.d < 14:
        #     pdfrpt.d = 480
        #     pdfrpt.c.setPageSize1(pdfrpt.landscape(pdfrpt.A4))
        #     pdfrpt.c.showPage()
        #     pdfrpt.header1(stdt, etdt, pdfrpt.divisioncode)
        #     pdfrpt.d = pdfrpt.d - 10

    pdfrpt.companyclean()

    if result == False:
        pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
        pdfrpt.fonts(10)

        d=pdfrpt.dvalue10()
        # d=480
        pdfrpt.c.drawString(200, d , "Total Invoice      : ")
        pdfrpt.c.drawAlignedString(630, d ,str(int(pdfrpt.Bills)))
        d=pdfrpt.dvalue10()
        pdfrpt.c.drawString(200, d , "Net Weight         : ")

        # pdfrpt.c.drawAlignedString(500, d ,  str("%.2f" % float(pdfrpt.netweight)))
        pdfrpt.c.drawAlignedString(630, d ,  str("%.2f" % float(pdfrpt.ChargesummaryTotalquantity)))
        d=pdfrpt.dvalue10()
        pdfrpt.c.drawString(200, d , "Gross Amount       : ")
        pdfrpt.c.drawAlignedString(630, d ,  str(format_currency("%.2f" % float(pdfrpt.GrossAmountTotal), 'INR', locale='en_IN')))
        d=pdfrpt.dvalue10()
        pdfrpt.c.drawString(200, d , "Total Basic Amount : ")
        pdfrpt.c.drawAlignedString(630, d ,  str(format_currency("%.2f" % float(pdfrpt.BasicAmount), 'INR', locale='en_IN')))
        d=pdfrpt.dvalue10()
        pdfrpt.c.drawString(200, pdfrpt.d , "Total Tax Amount   : ")
        # pdfrpt.c.drawAlignedString(500, pdfrpt.d ,  str(format_currency("%.2f" % float(pdfrpt.TaxAmount),'INR',locale='en_IN')))
        pdfrpt.c.drawAlignedString(630, pdfrpt.d ,  str(format_currency("%.2f" % float(pdfrpt.TOTALInvoiceTAXAmount),'INR',locale='en_IN')))
        d=pdfrpt.dvalue10()
        pdfrpt.c.drawString(200, pdfrpt.d , "Invoice Amount     : ")
        pdfrpt.c.drawAlignedString(630, pdfrpt.d ,  str(format_currency("%.2f" % float(pdfrpt.InvoiceAmountTotal),'INR',locale='en_IN')))

        # pdfrpt.pageno=0

    #     pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
    #
    #     pdfrpt.fonts(8)
    #     # pdfrpt.c.drawString(10, pdfrpt.d, str(pdfrpt.divisioncode[-2]) + " TOTAL : ")
    #     # pdfrpt.c.drawAlignedString(225, pdfrpt.d, str("%.3f" % float(pdfrpt.CompanyQuentityTotal)))
    #     # pdfrpt.c.drawAlignedString(300, pdfrpt.d, str("%.2f" % float(pdfrpt.CompanyAmountTotal)))
    #     pdfrpt.companyclean()

    if counter == 0:
        global Exceptions
        Exceptions = "Note: No Result found according to your selected criteria "
    else:
        Exceptions = ""
        pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
        pdfrpt.c.save()
        # url = "file:///D:/Reports/ReportDevelopment/" + LSFileName + ".pdf"
        # os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()