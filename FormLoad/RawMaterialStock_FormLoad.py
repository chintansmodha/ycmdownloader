from django.shortcuts import render
from Global_Files import Connection_String as con
GDataDeptDetail=[]
GDataPlantDetail=[]
GDataItemDetail=[]
GDataLotDetail=[]
deptclqtytotal=0
plantclqtytotal=0
itemclqtytotal=0
lotclqtytotal=0
def RawMaterialStockHTML(request):
    global GDataDeptDetail
    global GDataPlantDetail
    global plantclqtytotal
    global deptclqtytotal
    GDataPlantDetail=[]
    GDataDeptDetail=[]
    deptclqtytotal = 0
    plantclqtytotal = 0
    #Department
    sql =" Select LogicalWareHouse.LONGDESCRIPTION as Dept" \
         ",LogicalWareHouse.CODE as DEPTCODE" \
         " ,cast(Sum(BASEPRIMARYQUANTITYUNIT)as decimal(18)) As BalQty" \
         " From    Balance" \
         " JOIN LogicalWareHouse On Balance.LOGICALWAREHOUSECODE=LogicalWareHouse.CODE" \
         " JOIN Plant ON LogicalWareHouse.PLANTCODE = Plant.Code" \
         " Where Balance.ItemTypeCode In ('MBB','MBP','CHP')" \
         " Group By LogicalWareHouse.LONGDESCRIPTION,LogicalWareHouse.CODE" \
         " Order By  LogicalWareHouse.LONGDESCRIPTION"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        deptclqtytotal = deptclqtytotal + float(result['BALQTY'])
        GDataDeptDetail.append(result)
        result = con.db.fetch_both(stmt)

    #Site
    sql = " Select Plant.SHORTDESCRIPTION as Site,cast(Sum(BASEPRIMARYQUANTITYUNIT)as decimal(18)) As BalQty " \
          " From    Balance" \
          " JOIN LogicalWareHouse On Balance.LOGICALWAREHOUSECODE=LogicalWareHouse.CODE" \
          " JOIN Plant ON LogicalWareHouse.PLANTCODE = Plant.Code" \
          " Where Balance.ItemTypeCode In ('MBB','MBP','CHP')" \
          " Group By Plant.SHORTDESCRIPTION" \
          " Order By  Plant.SHORTDESCRIPTION"


    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        plantclqtytotal = plantclqtytotal + float(result['BALQTY'])
        GDataPlantDetail.append(result)
        result = con.db.fetch_both(stmt)

    return render(request, 'RawMaterialStock.html',{"GDataDeptDetail":GDataDeptDetail,"GDataPlantDetail":GDataPlantDetail
        ,"deptclqtytotal":round(deptclqtytotal),"plantclqtytotal":round(plantclqtytotal)})

def RawMaterialStock_ItemDetail(request):
    global GDataDeptDetail
    global GDataPlantDetail
    global GDataItemDetail
    global plantclqtytotal
    global deptclqtytotal
    global itemclqtytotal
    GDataPlantDetail = []
    GDataDeptDetail = []
    GDataItemDetail = []
    deptclqtytotal = 0
    plantclqtytotal = 0
    itemclqtytotal = 0
    Dept = request.GET['Dept']
    # Department
    sql = " Select LogicalWareHouse.LONGDESCRIPTION as Dept" \
          ",LogicalWareHouse.CODE as DEPTCODE" \
          " ,cast(Sum(BASEPRIMARYQUANTITYUNIT)as decimal(18)) As BalQty" \
          " From    Balance" \
          " JOIN LogicalWareHouse On Balance.LOGICALWAREHOUSECODE=LogicalWareHouse.CODE" \
          " JOIN Plant ON LogicalWareHouse.PLANTCODE = Plant.Code" \
          " Where Balance.ItemTypeCode In ('MBB','MBP','CHP')" \
          " Group By LogicalWareHouse.LONGDESCRIPTION,LogicalWareHouse.CODE" \
          " Order By  LogicalWareHouse.LONGDESCRIPTION"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        deptclqtytotal = deptclqtytotal + float(result['BALQTY'])
        GDataDeptDetail.append(result)
        result = con.db.fetch_both(stmt)

    # Site
    sql = " Select Plant.SHORTDESCRIPTION as Site,cast(Sum(BASEPRIMARYQUANTITYUNIT)as decimal(18)) As BalQty " \
          " From    Balance" \
          " JOIN LogicalWareHouse On Balance.LOGICALWAREHOUSECODE=LogicalWareHouse.CODE" \
          " JOIN Plant ON LogicalWareHouse.PLANTCODE = Plant.Code" \
          " Where Balance.ItemTypeCode In ('MBB','MBP','CHP')" \
          " Group By Plant.SHORTDESCRIPTION" \
          " Order By  Plant.SHORTDESCRIPTION"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        plantclqtytotal = plantclqtytotal + float(result['BALQTY'])
        GDataPlantDetail.append(result)
        result = con.db.fetch_both(stmt)

    # Item
    sql = " Select  Product.LongDescription As ProductName,Product.AbsUniqueId as id" \
          " , cast(Sum(Balance.BASEPRIMARYQUANTITYUNIT)as decimal(18)) As ClQty " \
          " , UGG.LongDescription as Shade" \
          ", LogicalWareHouse.Code as Dept" \
          " From    Balance" \
          " JOIN FullItemKeyDecoder FIKD    ON      Balance.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(Balance.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(Balance.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(Balance.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(Balance.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
          " AND     COALESCE(Balance.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
          " AND     COALESCE(Balance.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
          " AND     COALESCE(Balance.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
          " AND     COALESCE(Balance.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
          " AND     COALESCE(Balance.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
          " AND     COALESCE(Balance.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
          " Join Product                    On      Balance.ITEMTYPECODE           = Product.ITEMTYPECODE" \
          " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
          " JOIN LogicalWareHouse           On Balance.LOGICALWAREHOUSECODE=LogicalWareHouse.CODE" \
          " JOIN Plant ON LogicalWareHouse.PLANTCODE = Plant.Code" \
          " Left JOIN ItemSubcodeTemplate IST    ON      Balance.ITEMTYPECODE = IST.ItemTypeCode" \
          " AND     IST.GroupTypeCode In ('P09','B07')" \
          " Left JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
          " AND     CASE IST.Position When 1 Then Balance.DecoSubCode01" \
          " When 2 Then Balance.DecoSubCode02 When 3 Then Balance.DecoSubCode03" \
          " When 4 Then Balance.DecoSubCode04 When 5 Then Balance.DecoSubCode05" \
          " When 6 Then Balance.DecoSubCode06 When 7 Then Balance.DecoSubCode07" \
          " When 8 Then Balance.DecoSubCode08 When 9 Then Balance.DecoSubCode09" \
          " When 10 Then Balance.DecoSubCode10 End = UGG.Code" \
          " Where  Balance.ItemTypeCode In ('MBP','MBB','CHP')" \
          " And     LogicalWareHouse.CODE = '"+Dept+"'" \
          " Group By Product.LongDescription,UGG.LongDescription,Product.AbsUniqueId,LogicalWareHouse.Code "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        itemclqtytotal = itemclqtytotal + float(result['CLQTY'])
        GDataItemDetail.append(result)
        result = con.db.fetch_both(stmt)

    return render(request, 'RawMaterialStock.html',
                  {"GDataDeptDetail": GDataDeptDetail, "GDataPlantDetail": GDataPlantDetail
                      , "deptclqtytotal": round(deptclqtytotal), "plantclqtytotal": round(plantclqtytotal)
                      ,"GDataItemDetail":GDataItemDetail,"itemclqtytotal":round(itemclqtytotal)})

def RawMaterialStock_LotDetail(request):
    global GDataDeptDetail
    global GDataPlantDetail
    global GDataItemDetail
    global GDataLotDetail
    global plantclqtytotal
    global deptclqtytotal
    global lotclqtytotal
    global itemclqtytotal
    GDataPlantDetail = []
    GDataDeptDetail = []
    GDataLotDetail = []
    GDataItemDetail = []
    deptclqtytotal = 0
    plantclqtytotal = 0
    itemclqtytotal = 0
    lotclqtytotal = 0
    Dept = request.GET['Dept']
    Item = request.GET['Item']
    # Department
    sql = " Select LogicalWareHouse.LONGDESCRIPTION as Dept" \
          ",LogicalWareHouse.CODE as DEPTCODE" \
          " ,cast(Sum(Balance.BASEPRIMARYQUANTITYUNIT)as decimal(18)) As BalQty" \
          " From    Balance" \
          " JOIN LogicalWareHouse On Balance.LOGICALWAREHOUSECODE=LogicalWareHouse.CODE" \
          " JOIN Plant ON LogicalWareHouse.PLANTCODE = Plant.Code" \
          " Where Balance.ItemTypeCode In ('MBB','MBP','CHP')" \
          " Group By LogicalWareHouse.LONGDESCRIPTION,LogicalWareHouse.CODE" \
          " Order By  LogicalWareHouse.LONGDESCRIPTION"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        deptclqtytotal = deptclqtytotal + float(result['BALQTY'])
        GDataDeptDetail.append(result)
        result = con.db.fetch_both(stmt)

    # Site
    sql = " Select Plant.SHORTDESCRIPTION as Site,cast(Sum(BASEPRIMARYQUANTITYUNIT)as decimal(18)) As BalQty " \
          " From    Balance" \
          " JOIN LogicalWareHouse On Balance.LOGICALWAREHOUSECODE=LogicalWareHouse.CODE" \
          " JOIN Plant ON LogicalWareHouse.PLANTCODE = Plant.Code" \
          " Where Balance.ItemTypeCode In ('MBB','MBP','CHP')" \
          " Group By Plant.SHORTDESCRIPTION" \
          " Order By  Plant.SHORTDESCRIPTION"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        plantclqtytotal = plantclqtytotal + float(result['BALQTY'])
        GDataPlantDetail.append(result)
        result = con.db.fetch_both(stmt)

    # Item
    sql = " Select  Product.LongDescription As ProductName,Product.AbsUniqueId as id" \
          " , cast(Sum(Balance.BASEPRIMARYQUANTITYUNIT)as decimal(18)) As ClQty " \
          " , UGG.LongDescription as Shade" \
          ", LogicalWareHouse.Code as Dept" \
          " From    Balance" \
          " JOIN FullItemKeyDecoder FIKD    ON      Balance.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(Balance.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(Balance.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(Balance.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(Balance.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
          " AND     COALESCE(Balance.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
          " AND     COALESCE(Balance.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
          " AND     COALESCE(Balance.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
          " AND     COALESCE(Balance.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
          " AND     COALESCE(Balance.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
          " AND     COALESCE(Balance.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
          " Join Product                    On      Balance.ITEMTYPECODE           = Product.ITEMTYPECODE" \
          " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
          " JOIN LogicalWareHouse           On Balance.LOGICALWAREHOUSECODE=LogicalWareHouse.CODE" \
          " JOIN Plant ON LogicalWareHouse.PLANTCODE = Plant.Code" \
          " Left JOIN ItemSubcodeTemplate IST    ON      Balance.ITEMTYPECODE = IST.ItemTypeCode" \
          " AND     IST.GroupTypeCode In ('P09','B07')" \
          " Left JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
          " AND     CASE IST.Position When 1 Then Balance.DecoSubCode01" \
          " When 2 Then Balance.DecoSubCode02 When 3 Then Balance.DecoSubCode03" \
          " When 4 Then Balance.DecoSubCode04 When 5 Then Balance.DecoSubCode05" \
          " When 6 Then Balance.DecoSubCode06 When 7 Then Balance.DecoSubCode07" \
          " When 8 Then Balance.DecoSubCode08 When 9 Then Balance.DecoSubCode09" \
          " When 10 Then Balance.DecoSubCode10 End = UGG.Code" \
          " Where  Balance.ItemTypeCode In ('MBP','MBB','CHP')" \
          " And     LogicalWareHouse.CODE = '" + Dept + "'" \
        " Group By Product.LongDescription,UGG.LongDescription,Product.AbsUniqueId,LogicalWareHouse.Code "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        itemclqtytotal = itemclqtytotal + float(result['CLQTY'])
        GDataItemDetail.append(result)
        result = con.db.fetch_both(stmt)

    # Item
    sql = " Select  Balance.LotCode as Lotcode" \
          " ,cast(Balance.BASEPRIMARYQUANTITYUNIT as decimal(18)) As ClQty" \
          " From    Balance" \
          " JOIN FullItemKeyDecoder FIKD    ON      Balance.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(Balance.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(Balance.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(Balance.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(Balance.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
          " AND     COALESCE(Balance.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
          " AND     COALESCE(Balance.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
          " AND     COALESCE(Balance.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
          " AND     COALESCE(Balance.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
          " AND     COALESCE(Balance.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
          " AND     COALESCE(Balance.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
          " Join Product                    On      Balance.ITEMTYPECODE           = Product.ITEMTYPECODE" \
          " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
          " JOIN LogicalWareHouse           On Balance.LOGICALWAREHOUSECODE=LogicalWareHouse.CODE" \
          " JOIN Plant ON LogicalWareHouse.PLANTCODE = Plant.Code" \
          " Where   Balance.ItemTypeCode In ('MBB','MBP','CHP')" \
          " And     Product.AbsUniqueId = '"+Item+"'" \
          " And LogicalWareHouse.Code = '"+Dept+"'" \

    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        lotclqtytotal = lotclqtytotal + float(result['CLQTY'])
        GDataLotDetail.append(result)
        result = con.db.fetch_both(stmt)
    return render(request, 'RawMaterialStock.html',
                  {"GDataDeptDetail": GDataDeptDetail, "GDataPlantDetail": GDataPlantDetail
                      , "deptclqtytotal": round(deptclqtytotal), "plantclqtytotal": round(plantclqtytotal)
                      , "GDataItemDetail": GDataItemDetail, "itemclqtytotal": round(itemclqtytotal)
                      ,"GDataLotDetail":GDataLotDetail,"lotclqtytotal":round(lotclqtytotal)})