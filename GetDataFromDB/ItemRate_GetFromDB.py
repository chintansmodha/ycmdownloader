from django.shortcuts import render
import os
from datetime import datetime

from django.shortcuts import render
from django.views.static import serve

from FormLoad import ItemRate_FormLoad as views

from Global_Files import Connection_String as con
from PrintPDF import ItemRate_PrintPDF as pdfrpt
save_name=""

Exceptions=""

counter=0
item1 = []
item2 = []
item3 = []
item4 = []
price1 = []
price2 = []
price3 = []
price4 = []
CODE = []

def ItemRate_PDF(request):
    # print(request)

    global CODE
    CODE = []
    Codee = request.GET.getlist('Code')
    Codees = "'" + Codee[0] + "'"

    sql = "Select  Distinct SPDPrev.InitialDate, TRIM(SPDPrev.PriceListCode) As Code " \
          "From SalesPriceDefinition SPDPrev " \
          "Join    SalesPriceDefinition SPDCurr    ON      SPDPrev.AreaCode = SPDCurr.AreaCode " \
          "Where   SPDCurr.PriceListCode = " + Codees + " " \
                                                       "And     SPDPrev.InitialDate < SPDCurr.InitialDate " \
                                                       "Order by SPDPrev.InitialDate Desc; "

    stmt = con.db.prepare(con.conn, sql)
    # Explicitly bind parameters
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        CODE.append(str(result['CODE']))
        result = con.db.fetch_both(stmt)

    CODES = "(" + str(CODE)[1:-1] + ")"
    # print(CODES)




    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "ItemRate" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Item Rate/",
                             LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    stdt = request.GET.getlist('Date')
    startdate = str(stdt[0])
    print(startdate)
    enddate = ""
    Item = request.GET.getlist('Item')
    Price = request.GET.getlist('Price')
    Column = request.GET.getlist('Column')
    Code = request.GET.getlist('Code')
    # print('Codes :   ',Codes)
    # print('CODES :   ', CODES)

    Items = " COALESCE(ADProduct.VALUESTRING,Product.LONGDESCRIPTION) in " + "(" + str(Item)[1:-1] + ")"
    Prices = " AND SPDL.PRICE in  " + "(" + str(Price)[1:-1] + ")"
    Columns = ''
    Codes = "'" + Code[0] + "'"
    # print(Items)

    PrintPDF(Items, Prices, Columns, Codes, CODES, startdate, enddate)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        Exceptions = "Rohit"
        return render(request, 'ItemRateTable.html',
                      {'GDItemSummary': views.GDItemSummary, 'Exception': Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


def PrintPDF(Items,Prices, Columns, Codes, CODES, startdate, enddate):
    global Exceptions
    sql = "Select  COALESCE(ADProduct.VALUESTRING,Product.LONGDESCRIPTION) As Item " \
          ", COALESCE(CAST(SPDLCurr.PRICE As Decimal(15,2)),0)  As PriceCurr " \
          ", COALESCE(CAST(SPDLPrev.PRICE As Decimal(15,2)),CAST(SPDLCurr.PRICE As Decimal(15,2)),0)  As PricePrev " \
          ", 'BEEKAYLON GROUP OF COMPANIES' AS Company " \
          ", ColumnNo.VALUESTRING As Column " \
          ", AREA.LONGDESCRIPTION As Location " \
          ", COALESCE(Remark1.VALUESTRING, '') As Remarks1 " \
          ", COALESCE(Remark2.VALUESTRING, '') As Remarks2 " \
          ", COALESCE(Remark3.VALUESTRING, '') As Remarks3 " \
          ", COALESCE(Remark4.VALUESTRING, '') As Remarks4 " \
          ", COALESCE(Remark5.VALUESTRING, '') As Remarks5 " \
          ", COALESCE(Remark6.VALUESTRING, '') As Remarks6 " \
          "From SalesPriceDefinition SPDCurr " \
          "Join    PRICELIST                       On      SPDCurr.PRICELISTCODE = PRICELIST.CODE " \
          "And     SPDCurr.PRICELISTTYPE = PRICELIST.PRICELISTTYPE " \
          "Left Join ADSTORAGE Remark1             On      Remark1.UniqueId = PRICELIST.AbsUniqueId " \
          "And     Remark1.NameEntityName = 'PriceList' " \
          "And     Remark1.NAmeName ='Remark1' " \
          "And     Remark1.FieldName = 'Remark1' " \
          "Left Join ADSTORAGE Remark2             On      Remark2.UniqueId = PRICELIST.AbsUniqueId " \
          "And     Remark2.NameEntityName = 'PriceList' " \
          "And     Remark2.NAmeName ='Remark2' " \
          "And     Remark2.FieldName = 'Remark2' " \
          "Left Join ADSTORAGE Remark3             On      Remark3.UniqueId = PRICELIST.AbsUniqueId " \
          "And     Remark3.NameEntityName = 'PriceList' " \
          "And     Remark3.NAmeName ='Remark3' " \
          "And     Remark3.FieldName = 'Remark3' " \
          "Left Join ADSTORAGE Remark4             On      Remark4.UniqueId = PRICELIST.AbsUniqueId " \
          "And     Remark4.NameEntityName = 'PriceList' " \
          "And     Remark4.NAmeName ='Remark4' " \
          "And     Remark4.FieldName = 'Remark4' " \
          "Left Join ADSTORAGE Remark5             On      Remark5.UniqueId = PRICELIST.AbsUniqueId " \
          "And     Remark5.NameEntityName = 'PriceList' " \
          "And     Remark5.NAmeName ='Remark5' " \
          "And     Remark5.FieldName = 'Remark5' " \
          "Left Join ADSTORAGE Remark6             On      Remark6.UniqueId = PRICELIST.AbsUniqueId " \
          "And     Remark6.NameEntityName = 'PriceList' " \
          "And     Remark6.NAmeName ='Remark6' " \
          "And     Remark6.FieldName = 'Remark6' " \
          "Join Area                               On      SPDCurr.AreaCode = Area.CODE " \
          "Join ADSTORAGE ColumnNo                 On      ColumnNo.UniqueId = SPDCurr.AbsUniqueId " \
          "And     ColumnNo.NameEntityName = 'SalesPriceDefinition' " \
          "And     ColumnNo.NAmeName ='AdditonalInfo' " \
          "And     ColumnNo.FieldName = 'AdditonalInfo' " \
          "Left Join ADSTORAGE ADProduct           On      ADProduct.UniqueId = SPDCurr.AbsUniqueId " \
          "And     ADProduct.NameEntityName = 'SalesPriceDefinition' " \
          "And     ADProduct.NAmeName ='ItemDescription' " \
          "And     ADProduct.FieldName = 'ItemDescription' " \
          "Left JOIN Product                       ON      SPDCurr.ITEMTYPEAFICODE = Product.ITEMTYPECODE " \
          "AND     COALESCE(SPDCurr.SubCode01, '') = COALESCE(Product.SubCode01, '') " \
          "AND     COALESCE(SPDCurr.SubCode02, '') = COALESCE(Product.SubCode02, '') " \
          "AND     COALESCE(SPDCurr.SubCode03, '') = COALESCE(Product.SubCode03, '') " \
          "AND     COALESCE(SPDCurr.SubCode04, '') = COALESCE(Product.SubCode04, '') " \
          "AND     COALESCE(SPDCurr.SubCode05, '') = COALESCE(Product.SubCode05, '') " \
          "AND     COALESCE(SPDCurr.SubCode06, '') = COALESCE(Product.SubCode06, '') " \
          "AND     COALESCE(SPDCurr.SubCode07, '') = COALESCE(Product.SubCode07, '') " \
          "AND     COALESCE(SPDCurr.SubCode08, '') = COALESCE(Product.SubCode08, '') " \
          "AND     COALESCE(SPDCurr.SubCode09, '') = COALESCE(Product.SubCode09, '') " \
          "AND     COALESCE(SPDCurr.SubCode10, '') = COALESCE(Product.SubCode10, '') " \
          "Left Join SALESPRICEDEFINITIONDETAIL SPDLCurr    On      SPDCurr.COMPANYCODE  =  SPDLCurr.SALPRICEDEFINITIONCOMPANYCODE " \
          "And     SPDCurr.NUMBERID  =  SPDLCurr.SALESPRICEDEFINITIONNUMBERID " \
          "Left Join SalesPriceDefinition SPDPrev       On      SPDPrev.PRICELISTCode in "+CODES+" " \
          "AND     COALESCE(SPDCurr.SubCode01, '') = COALESCE(SPDPrev.SubCode01, '') " \
          "AND     COALESCE(SPDCurr.SubCode02, '') = COALESCE(SPDPrev.SubCode02, '') " \
          "AND     COALESCE(SPDCurr.SubCode03, '') = COALESCE(SPDPrev.SubCode03, '') " \
          "AND     COALESCE(SPDCurr.SubCode04, '') = COALESCE(SPDPrev.SubCode04, '') " \
          "AND     COALESCE(SPDCurr.SubCode05, '') = COALESCE(SPDPrev.SubCode05, '') " \
          "AND     COALESCE(SPDCurr.SubCode06, '') = COALESCE(SPDPrev.SubCode06, '') " \
          "AND     COALESCE(SPDCurr.SubCode07, '') = COALESCE(SPDPrev.SubCode07, '') " \
          "AND     COALESCE(SPDCurr.SubCode08, '') = COALESCE(SPDPrev.SubCode08, '') " \
          "AND     COALESCE(SPDCurr.SubCode09, '') = COALESCE(SPDPrev.SubCode09, '') " \
          "AND     COALESCE(SPDCurr.SubCode10, '') = COALESCE(SPDPrev.SubCode10, '') " \
          "Left Join SALESPRICEDEFINITIONDETAIL SPDLPrev    On      SPDPrev.COMPANYCODE  =  SPDLPrev.SALPRICEDEFINITIONCOMPANYCODE " \
          "And     SPDPrev.NUMBERID  =  SPDLPrev.SALESPRICEDEFINITIONNUMBERID " \
          "Where   SPDCurr.PRICELISTCode = "+Codes+" " \
          "AND COALESCE(ADProduct.VALUESTRING,Product.LONGDESCRIPTION) is not null " \
          "Order By Column,Item "

    # try:


    stmt = con.db.prepare(con.conn, sql)
    # Explicitly bind parameters
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result,startdate, pdfrpt.x)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 150:
            pdfrpt.d = 470
            pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
            pdfrpt.c.showPage()
            pdfrpt.header(pdfrpt.divisioncode, result,startdate, pdfrpt.x)

    if result == False:
        if counter > 0:
            if pdfrpt.lastclm == 1:
                pdfrpt.d = pdfrpt.dvalueincrese()
                pdfrpt.d = pdfrpt.dvalue()
                if pdfrpt.boldornot != 0:
                    pdfrpt.boldfonts(7)
                pdfrpt.x = 32
                pdfrpt.c.drawAlignedString(pdfrpt.x + 170, pdfrpt.d, pdfrpt.price[-1])
            # print(pdfrpt.price[-1])
            elif pdfrpt.lastclm == 2:
                pdfrpt.d = pdfrpt.dvalueincrese()
                pdfrpt.d = pdfrpt.dvalue()
                if pdfrpt.boldornot != 0:
                    pdfrpt.boldfonts(7)
                pdfrpt.x = 217
                pdfrpt.c.drawAlignedString(pdfrpt.x + 170, pdfrpt.d, pdfrpt.price[-1])

            elif pdfrpt.lastclm == 3:
                pdfrpt.d = pdfrpt.dvalueincrese()
                pdfrpt.d = pdfrpt.dvalue()
                if pdfrpt.boldornot != 0:
                    pdfrpt.boldfonts(7)
                pdfrpt.x = 417
                pdfrpt.c.drawAlignedString(pdfrpt.x + 170, pdfrpt.d, pdfrpt.price[-1])

            elif pdfrpt.lastclm == 4:
                pdfrpt.d = pdfrpt.dvalueincrese()
                pdfrpt.d = pdfrpt.dvalue()
                if pdfrpt.boldornot != 0:
                    pdfrpt.boldfonts(7)
                pdfrpt.x = 617
                pdfrpt.c.drawAlignedString(pdfrpt.x + 170, pdfrpt.d, pdfrpt.price[-1])

            Exceptions = ""
            counter = 0
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria "
            return

    pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.d = pdfrpt.newpage()
    pdfrpt.newrequest()
    pdfrpt.x = 0
    pdfrpt.itemlen = 0
    pdfrpt.lastclm = 0
    pdfrpt.boldornot = 0

