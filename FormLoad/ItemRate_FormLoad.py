from datetime import datetime

from django.shortcuts import render
from Global_Files import Connection_String as con
GDATAPriceCode=[]
GDItemSummary = []
Date = []
Location = []
stdt = []

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from PRICELIST order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDATAPriceCode:
        GDATAPriceCode.append(result)
    result = con.db.fetch_both(stmt)

def ItemRateHtml(request):
    return render(request,'ItemRate.html', {'GDATAPriceCode':GDATAPriceCode})


def ItemRate(request):
    global GDItemSummary, stdt, Date, Location
    Date = []
    Location = []
    stdt = []
    GDItemSummary = []

    # LSLocationCode = request.GET.getlist('Location')
    # LDStartDate = "'" + str(request.GET['startdate']) + "'"
    # SDate = str(request.GET['startdate'])
    LSPriceCode = request.GET.getlist('Price')
    # print(LDStartDate)

    PriceCodes = str(LSPriceCode)
    LSPriceCodes = '(' + PriceCodes[1:-1] + ')'

    PriceCode = "PRICELIST.CODE In " + str(LSPriceCodes)

    sql = "Select  COALESCE(ADProduct.VALUESTRING,Product.LONGDESCRIPTION) As Item " \
          ", COALESCE(CAST((SPDL.PRICE) As Decimal(15,2)),0) As Price " \
          ", PRICELIST.CODE As Code " \
          ", ColumnNo.VALUESTRING As Column " \
          ", (SPD.INITIALDATE) As Date" \
          ", Area.LONGDESCRIPTION As Location " \
          "From PRICELIST " \
          "Join SALESPRICEDEFINITION SPD           On      PRICELIST.CODE  =  SPD.PRICELISTCODE " \
          "And     PRICELIST.PRICELISTTYPE  =  SPD.PRICELISTTYPE " \
          "Join Area                               On      SPD.AreaCode = Area.CODE " \
          "Join ADSTORAGE ColumnNo                 On      ColumnNo.UniqueId = SPD.AbsUniqueId " \
          "And     ColumnNo.NameEntityName = 'SalesPriceDefinition' " \
          "And     ColumnNo.NAmeName ='AdditonalInfo' " \
          "And     ColumnNo.FieldName = 'AdditonalInfo' " \
          "Left Join ADSTORAGE ADProduct           On      ADProduct.UniqueId = SPD.AbsUniqueId " \
          "And     ADProduct.NameEntityName = 'SalesPriceDefinition' " \
          "And     ADProduct.NAmeName ='ItemDescription' " \
          "And     ADProduct.FieldName = 'ItemDescription' " \
          "Left JOIN Product                            ON      SPD.ITEMTYPEAFICODE = Product.ITEMTYPECODE " \
          "AND     COALESCE(SPD.SubCode01, '') = COALESCE(Product.SubCode01, '') " \
          "AND     COALESCE(SPD.SubCode02, '') = COALESCE(Product.SubCode02, '') " \
          "AND     COALESCE(SPD.SubCode03, '') = COALESCE(Product.SubCode03, '') " \
          "AND     COALESCE(SPD.SubCode04, '') = COALESCE(Product.SubCode04, '') " \
          "AND     COALESCE(SPD.SubCode05, '') = COALESCE(Product.SubCode05, '') " \
          "AND     COALESCE(SPD.SubCode06, '') = COALESCE(Product.SubCode06, '') " \
          "AND     COALESCE(SPD.SubCode07, '') = COALESCE(Product.SubCode07, '') " \
          "AND     COALESCE(SPD.SubCode08, '') = COALESCE(Product.SubCode08, '') " \
          "AND     COALESCE(SPD.SubCode09, '') = COALESCE(Product.SubCode09, '') " \
          "AND     COALESCE(SPD.SubCode10, '') = COALESCE(Product.SubCode10, '') " \
          "Left Join SALESPRICEDEFINITIONDETAIL SPDL    On      SPD.COMPANYCODE  =  SPDL.SALPRICEDEFINITIONCOMPANYCODE " \
          "And     SPD.NUMBERID  =  SPDL.SALESPRICEDEFINITIONNUMBERID " \
          "Where "+PriceCode+" And COALESCE(ADProduct.VALUESTRING,Product.LONGDESCRIPTION) is  not null " \
          "Order By Column,Item,Price "


    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        GDItemSummary.append(result)
        stdt = []
        if Date == []:
            stdt.append(result['DATE'])
            Dates = datetime.strptime(str(stdt[0]), '%Y-%m-%d').date().strftime('%d-%m-%Y')
            Date.append(Dates)
            Location.append(str(result['LOCATION']))
        result = con.db.fetch_both(stmt)

    if GDItemSummary == []:
        global Exceptions
        Exceptions = "Note: No Result found on given criteria "
        return render(request,'ItemRate.html', {'GDATAPriceCode':GDATAPriceCode,'Exception':Exceptions})

    return render(request, 'ItemRateTable.html',
                  {'GDItemSummary': GDItemSummary, 'Date': Date[-1], 'Location': Location[0]})
