from django.shortcuts import render
from Global_Files import Connection_String as con
import json
from datetime import datetime
GDataProductLedgerSummary=[]
GDataProductLedgerDetail=[]
OpeningBalance = 0
IssQty=0
RecQty=0
ClosingBalance = 0
close=0
GDataPlant=[]
GDataItemType=[]
GDataProduct=[]
GDataYear=[]
GDataLogicalWarehouse = []
GDataGrade = []
def ProductLedger(request):
    global GDataPlant
    global GDataItemType
    global GDataProduct
    global GDataYear
    GDataPlant=[]
    GDataItemType=[]
    GDataProduct=[]
    GDataYear=[]
    year = 0
    stmt = con.db.exec_immediate(con.conn, "Select Code,varchar_format(FROMDATE,'YYYY-MM-DD') as FROMDATE"
                                           ",varchar_format(TODATE,'YYYY-MM-DD') as TODATE from FinFinancialYear order by Code Asc")
    result = con.db.fetch_both(stmt)
    #YearBeginingDate = result!FROMDATE
    while result != False:
        if result not in GDataYear:
            if year == 0:
                year = int(result['CODE'])
            GDataYear.append(result)
        result = con.db.fetch_both(stmt)
    # print(GDataYear)
    stmt = con.db.exec_immediate(con.conn,"select code,longdescription from plant order by code")
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        if result not in GDataPlant:
            GDataPlant.append(result)
        result = con.db.fetch_both(stmt)
    print(GDataPlant)
    stmt = con.db.exec_immediate(con.conn, "select ITEMTYPECODE from product order by ITEMTYPECODE")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataItemType:
            GDataItemType.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn, "select LONGDESCRIPTION,ABSUNIQUEID from product order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataProduct:
            GDataProduct.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn, "select LONGDESCRIPTION,CODE from LOGICALWAREHOUSE order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataLogicalWarehouse:
            GDataLogicalWarehouse.append(result)
        result = con.db.fetch_both(stmt)

    stmt = con.db.exec_immediate(con.conn, "select SHORTDESCRIPTION,CODE,ITEMTYPECODE from QUALITYLEVEL order by LONGDESCRIPTION")
    result = con.db.fetch_both(stmt)
    while result != False:
        if result not in GDataGrade:
            GDataGrade.append(result)
        result = con.db.fetch_both(stmt)


    return render(request,'ProductLedger.html',{"GDataPlant":GDataPlant
        ,"GDataItemType":GDataItemType,"GDataProduct":GDataProduct,"GDataYear":GDataYear, 'YEAR':year,
                                                'GDataLogicalWarehouse':GDataLogicalWarehouse , 'GDataGrade':GDataGrade})

def ProductLedgerSummary(request):
    global GDataProductLedgerSummary
    GDataProductLedgerSummary = []
    global IssQty, OpeningBalance
    global RecQty, ClosingBalance
    IssQty = 0
    OpeningBalance = 0
    RecQty = 0
    ClosingBalance = 0
    Year = request.GET['year']
    Years = int(Year) - 1
    beginDate  = str(Years) + '-04-01'
    # Year = Year - 1
    # print(Year)
    startdate =request.GET['startdate']
    enddate = request.GET['enddate']

    startdate = datetime(int(startdate[0:4]),int(startdate[5:7]),int(startdate[8:]))
    enddate =  datetime(int(enddate[0:4]),int(enddate[5:7]),int(enddate[8:]))

    Company = "("+str(request.GET.getlist('unit'))[1:-1]+")"
    Account = "("+str(request.GET.getlist('account'))[1:-1]+")"
    SubAccount = "("+str(request.GET.getlist('subaccount'))[1:-1]+")"
    LogicalWarehouse = "(" + str(request.GET.getlist('logicalware'))[1:-1] + ")"
    Grade = "(" + str(request.GET.getlist('grade'))[1:-1] + ")"
    # print(LogicalWarehouse,Grade)

    # if Year == "2022":
    #     print("it")
    # if startdate < datetime(int(Year)-1, 4, 1):
    #     Exceptions = "Start Date Should Be Between 2021-04-01 and 2022-03-31"
    #     return render(request, 'ProductLedger.html',{"Exception":Exceptions})
    # elif enddate > datetime(int(Year), 3, 31):
    #     Exceptions = "End Date Should Be Between 2021-04-01 and 2022-03-31"
    #     return render(request, 'ProductLedger.html', {"Exception": Exceptions})
    # elif Year == "2021":
    #     if startdate < datetime(2021, 4, 1):
    #         Exceptions = "Start Date Should Be Between 2020-04-01 and 2021-03-31"
    #         return render(request, 'ProductLedger.html',{"Exception":Exceptions})
    #     elif enddate > datetime(2022, 3, 31):
    #         Exceptions = "End Date Should Be Between 2020-04-01 and 2021-03-31"
    #         return render(request, 'ProductLedger.html', {"Exception": Exceptions})
    # elif Year == "2019":
    #     if startdate < datetime(2021, 4, 1):
    #         Exceptions = "Start Date Should Be Between 2019-04-01 and 2020-03-31"
    #         return render(request, 'ProductLedger.html',{"Exception":Exceptions})
    #     elif enddate > datetime(2022, 3, 31):
    #         Exceptions = "End Date Should Be Between 2019-04-01 and 2020-03-31"
    #         return render(request, 'ProductLedger.html', {"Exception": Exceptions})
    # elif Year == "1920":
    #     if startdate < datetime(2021, 4, 1):
    #         Exceptions = "Start Date Should Be Between 2019-04-01 and 2020-03-31"
    #         return render(request, 'ProductLedger.html',{"Exception":Exceptions})
    #     elif enddate > datetime(2022, 3, 31):
    #         Exceptions = "End Date Should Be Between 2019-04-01 and 2020-03-31"
    #         return render(request, 'ProductLedger.html', {"Exception": Exceptions})

    if request.GET.getlist('unit'):
        Company = " And Plant.Code in "+Company
    else:
        Company = ""
    if request.GET.getlist('account'):
        Account = " And Product.ItemTypeCode in " + Account
    else:
        Account = ""
    if request.GET.getlist('subaccount'):
        SubAccount = " And Product.ABSUNIQUEID in " + SubAccount
    else:
        SubAccount = ""

    if request.GET.getlist('logicalware'):
        LogicalWarehouse = " And LOGICALWAREHOUSE.Code in " + LogicalWarehouse
    else:
        LogicalWarehouse = ""

    if request.GET.getlist('grade'):
        Grade = " AND QUALITYLEVEL.LONGDESCRIPTION ||'-'|| QUALITYLEVEL.ITEMTYPECODE in " + Grade
    else:
        Grade = ""

    stdt = str(startdate.strftime('%d-%m-%Y'))
    startdate = str(startdate.strftime('%Y-%m-%d'))
    etdt = str(enddate.strftime('%d-%m-%Y'))
    enddate = str(enddate.strftime('%Y-%m-%d'))
    # print(stdt,etdt)
    sql = "Select ST.ItemTypeCode as ItemType" \
          ",Product.Longdescription  as ProductName " \
          ", Costcenter.SHORTDESCRIPTION as Dept " \
          ",cast(Sum(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 " \
          "End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End)as decimal(18,2)) as OpBal" \
          ",cast(Sum(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' " \
          "And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End)as decimal(18,2)) as RecQty" \
          ",cast(Sum(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' " \
          "And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End)as decimal(18,2)) as IssQty" \
          ",cast(Sum(Case When TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case " \
          "When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End)as decimal(18,2)) as BalQty" \
          ",LOGICALWAREHOUSE.CODE as WareHouseCode" \
          ",Plant.Code as PlantCode" \
          ",Plant.Shortdescription as PlantName" \
          ",Plant.Longdescription as PlantNamess" \
          ",Product.AbsUniqueid as id" \
          " From StockTransaction ST" \
          " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
          " JOIN FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(ST.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(ST.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(ST.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(ST.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
          " AND     COALESCE(ST.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
          " AND     COALESCE(ST.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
          " AND     COALESCE(ST.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
          " AND     COALESCE(ST.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
          " AND     COALESCE(ST.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
          " AND     COALESCE(ST.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
          " Join Product                    On      ST.ITEMTYPECODE           = Product.ITEMTYPECODE" \
          " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
          " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
          " Join Costcenter                 On      LOGICALWAREHOUSE.COSTCENTERCODE = Costcenter.CODE" \
          " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code " \
          " Where ST.TRANSACTIONDATE <=   '"+enddate+"' "+Company+Account+SubAccount+LogicalWarehouse+Grade+" " \
          " And ST.TemplateCode not in('QC1','QCR') " \
          " Group by ST.ItemTypeCode " \
          ",Product.Longdescription ,LOGICALWAREHOUSE.CODE,Plant.Code,Product.AbsUniqueid,Plant.Shortdescription" \
          " ,Plant.Longdescription " \
          " ,Costcenter.SHORTDESCRIPTION  " \
          " Having Sum(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 " \
          "End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End) != 0 Or Sum(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' " \
          "And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End) != 0 Or Sum(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' " \
          "And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End) != 0 Or Sum(Case When TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case " \
          "When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End) != 0 " \
          " Order By ProductName"

    # print(beginDate, 'bbbb')
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        OpeningBalance += float(result['OPBAL'])
        IssQty=IssQty+float(result['ISSQTY'])
        RecQty=RecQty+float(result['RECQTY'])
        GDataProductLedgerSummary.append(result)
        result = con.db.fetch_both(stmt)
    ClosingBalance += OpeningBalance + RecQty - IssQty
    # print(IssQty, OpeningBalance)
    # print(OpeningBalance - IssQty)
    # print(ClosingBalance)
    return render(request, 'ProductLedgerSummary.html',
                  {'GDataProductLedgerSummary': GDataProductLedgerSummary,"RecQty":round(RecQty,2)
                      ,"IssQty":round(IssQty,2),'startdate':stdt,'enddate':etdt,
                   'OpeningBalance': round(OpeningBalance,2), 'ClosingBalance': round(ClosingBalance,2)})

def ProductLedgerDetail(request):
    # TxnDate = datetime.strptime(request.GET['txndate'],'%d-%m-%Y')
    # TxnDate = str(TxnDate)[:11]
    Dept = request.GET['Dept']
    # print(Dept)
    Warehouse = request.GET['ware']
    Company = request.GET['comp']
    Item = request.GET['item']
    ItemName = str(request.GET['ItemName'])[0:]
    PlantName = str(request.GET['PlantName'])[0:]
    # print(PlantName)
    # print(ItemName)
    OpBal = request.GET['opbal']
    # print(OpBal)
    Template = request.GET['temp']
    startdate = str(request.GET['startdate'])
    startdate = (datetime.strptime(startdate, '%d-%m-%Y').date()).strftime('%Y-%m-%d')
    enddate = str(request.GET['enddate'])
    enddate = (datetime.strptime(enddate, '%d-%m-%Y').date()).strftime('%Y-%m-%d')
    # enddate = str(enddate.strftime('%Y-%m-%d'))
    # print(startdate, enddate)
    print(Warehouse,Company,Item,startdate,enddate)
    global close
    global GDataProductLedgerDetail
    GDataProductLedgerDetail=[]
    close=0
    # print(sql)
    sql =   " Select Production.Company" \
            "   ,Production.StType" \
            " ,Production.Dept" \
            " ,Production.TxnDate" \
            " ,Production.TxnNo" \
            " ,Production.TxnType" \
            " ,(Production.OpBal) as Opbal" \
            " ,(Production.RecQty) as RecQty" \
            " ,(Production.IssQty) as IssQty" \
            " ,(Production.BalQty) as BalQty" \
            " from" \
            " (" \
            " Select  Plant.Longdescription as Company" \
            ", Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End as StType" \
            ",Costcenter.SHORTDESCRIPTION as Dept" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.TRANSACTIONNUMBER) End as TxnNo" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
            " ,SUM(cast(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End as decimal(18,2))) as OpBal" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2))) as RecQty" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2))) as IssQty" \
            " ,SUM(cast(Case When TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,2))) as BalQty" \
            " From    StockTransaction ST" \
            " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN    FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
            " AND     COALESCE(ST.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
            " AND     COALESCE(ST.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
            " AND     COALESCE(ST.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
            " AND     COALESCE(ST.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
            " AND     COALESCE(ST.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
            " AND     COALESCE(ST.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
            " AND     COALESCE(ST.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
            " AND     COALESCE(ST.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
            " AND     COALESCE(ST.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
            " AND     COALESCE(ST.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
            " Join Product                    On      ST.ITEMTYPECODE           = Product.ITEMTYPECODE" \
            " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Left Join MRNHEADER             ON      St.ORDERCODE = MRNHEADER.PURCHASEORDERCODE " \
            " And St.ORDERCOUNTERCODE = MRNHEADER.PURCHASEORDERCOUNTERCODE " \
            " Left Join Costcenter            On      MRNHEADER.COSTCENTERCODE = Costcenter.CODE " \
            " where ST.TRANSACTIONDATE between '"+startdate+"' and '"+enddate+"'" \
            " and LOGICALWAREHOUSE.CODE = '"+Warehouse+" '" \
            " and Plant.Code = '"+Company+" '" \
            " and Product.AbsUniqueid = '"+Item+" '" \
            " and ST.TemplateCode in ('098','099','CGI','G02','GES','P01','PKC','PKE','PKG'" \
            ",'PS1','PS2','PS3','PS4','PS5','QC2', 'QCT' " \
            ",'REJ','REN','SC2','SCP','T01','T02','T03','T04','T05'" \
            ",'T06','T07','W01') " \
            " Group By Plant.Longdescription " \
            ", Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE End " \
            ",Costcenter.SHORTDESCRIPTION " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.TRANSACTIONNUMBER) End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End " \
            " Union ALl" \
            " Select  Plant.Longdescription as Company" \
            " , Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  as StType" \
            " ,Costcenter.SHORTDESCRIPTION as Dept" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.ProductionOrderCode) End as TxnNo" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
            " ,SUM(cast(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End as decimal(18,2)))   as OpBal" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2)))  as RecQty" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2)))  as IssQty" \
            " ,SUM(cast(Case When ST.TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,2)))  as BalQty" \
            " From    StockTransaction ST" \
             " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN    FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
            " AND     COALESCE(ST.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
            " AND     COALESCE(ST.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
            " AND     COALESCE(ST.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
            " AND     COALESCE(ST.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
            " AND     COALESCE(ST.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
            " AND     COALESCE(ST.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
            " AND     COALESCE(ST.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
            " AND     COALESCE(ST.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
            " AND     COALESCE(ST.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
            " AND     COALESCE(ST.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
            " Join Product                    On      ST.ITEMTYPECODE           = Product.ITEMTYPECODE" \
            " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Join PRODUCTIONORDER PO    On      ST.ProductionOrderCode = PO.CODE " \
            " Left Join BKLELEMENTS      On      ST.CONTAINERELEMENTCODE = BKLELEMENTS.CODE " \
            " Left Join LOGICALWAREHOUSE bklLogic ON      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = bklLogic.CODE  " \
            " Left Join Costcenter                 On      bklLogic.COSTCENTERCODE = Costcenter.CODE" \
            " where ST.TRANSACTIONDATE between '"+startdate+"' and '"+enddate+"'" \
            " and LOGICALWAREHOUSE.CODE = '"+Warehouse+" '" \
            " and Plant.Code = '"+Company+" '" \
            " and Product.AbsUniqueid = '"+Item+" '" \
            " and ST.TemplateCode in ('M01','M02','M03','M04','M05') " \
            " Group By Plant.Longdescription " \
            " , Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  " \
            " ,Costcenter.SHORTDESCRIPTION " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.ProductionOrderCode) End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End " \
            " Union All" \
            " Select  Plant.Longdescription as Company" \
            " , Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  as StType" \
            " ,PoBp.LEGALNAME1 as Dept" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(MD.MRNHEADERCODE) End as TxnNo" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
            " ,SUM(cast(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End as decimal(18,2)))  as OpBal" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2))) as RecQty" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2)))  as IssQty" \
            " ,SUM(cast(Case When ST.TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,2)))  as BalQty" \
            " From    StockTransaction ST" \
            " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN    FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
            " AND     COALESCE(ST.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
            " AND     COALESCE(ST.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
            " AND     COALESCE(ST.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
            " AND     COALESCE(ST.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
            " AND     COALESCE(ST.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
            " AND     COALESCE(ST.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
            " AND     COALESCE(ST.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
            " AND     COALESCE(ST.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
            " AND     COALESCE(ST.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
            " AND     COALESCE(ST.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
            " Join Product                    On      ST.ITEMTYPECODE           = Product.ITEMTYPECODE" \
            " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Left Join PurchaseOrder PO      On      ST.OrderCode = PO.Code" \
            " Left Join MrnDetail MD On PO.Code = MD.PURCHASEORDERCODE" \
            " AND PO.CounterCode = MD.PURCHASEORDERCOUNTERCODE " \
            " AND ST.TRANSACTIONNUMBER  = MD.TRANSACTIONNUMBER " \
            " Left Join ORDERPARTNER PoOrpn    ON     PO.ORDPRNCUSTOMERSUPPLIERCODE = PoOrpn.CUSTOMERSUPPLIERCODE " \
            " And PoOrpn.CUSTOMERSUPPLIERTYPE = 1 " \
            " Left Join BUSINESSPARTNER PoBp    On      PoOrpn.ORDERBUSINESSPARTNERNUMBERID = PoBp.NUMBERID " \
            " where ST.TRANSACTIONDATE between '"+startdate+"' and '"+enddate+"'" \
            " and LOGICALWAREHOUSE.CODE = '"+Warehouse+" '" \
            " and Plant.Code = '"+Company+" '" \
            " and Product.AbsUniqueid = '"+Item+" '" \
            " and ST.TemplateCode in ('101','110','G01') " \
            " Group By Plant.Longdescription " \
            " , Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  " \
            " ,PoBp.LEGALNAME1 " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(MD.MRNHEADERCODE) End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End " \
            " Union All" \
            " Select  Plant.Longdescription as Company" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  as StType" \
            " ,SDBp.LEGALNAME1 as Dept" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.OrderCode) End as TxnNo" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
            " ,SUM(cast(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End as decimal(18,2)))  as OpBal" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2))) as RecQty" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2)))  as IssQty" \
            " ,SUM(cast(Case When ST.TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,2)))  as BalQty" \
            " From    StockTransaction ST" \
            " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN    FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
            " AND     COALESCE(ST.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
            " AND     COALESCE(ST.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
            " AND     COALESCE(ST.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
            " AND     COALESCE(ST.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
            " AND     COALESCE(ST.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
            " AND     COALESCE(ST.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
            " AND     COALESCE(ST.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
            " AND     COALESCE(ST.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
            " AND     COALESCE(ST.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
            " AND     COALESCE(ST.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
            " Join Product                    On      ST.ITEMTYPECODE           = Product.ITEMTYPECODE" \
            " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Left Join SalesDocument SD           On      ST.OrderCode = SD.ProvisionalCode" \
            " And SD.DocumentTypeType = '05'" \
            " Left Join ORDERPARTNER SDOrpn    ON     SD.ORDPRNCUSTOMERSUPPLIERCODE = SDOrpn.CUSTOMERSUPPLIERCODE " \
            " And SDOrpn.CUSTOMERSUPPLIERTYPE = 1 " \
            " Left Join BUSINESSPARTNER SDBp    On      SDOrpn.ORDERBUSINESSPARTNERNUMBERID = SDBp.NUMBERID " \
            " where ST.TRANSACTIONDATE between '"+startdate+"' and '"+enddate+"'" \
            " and LOGICALWAREHOUSE.CODE = '"+Warehouse+" '" \
            " and Plant.Code = '"+Company+" '" \
            " and Product.AbsUniqueid = '"+Item+" '" \
            " and ST.TemplateCode in ('S04') " \
            " Group By Plant.Longdescription " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  " \
            " ,SDBp.LEGALNAME1 " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.OrderCode) End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End " \
            " Union All" \
            " Select  Plant.Longdescription as Company" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  as StType" \
            " ,SOBp.LEGALNAME1 as Dept" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.TRANSACTIONNUMBER) End as TxnNo" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
            " ,SUM(cast(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End as decimal(18,2)))  as OpBal" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2))) as RecQty" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2)))  as IssQty" \
            " ,SUM(cast(Case When ST.TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,2)))  as BalQty" \
            " From    StockTransaction ST" \
            " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN    FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
            " AND     COALESCE(ST.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
            " AND     COALESCE(ST.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
            " AND     COALESCE(ST.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
            " AND     COALESCE(ST.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
            " AND     COALESCE(ST.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
            " AND     COALESCE(ST.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
            " AND     COALESCE(ST.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
            " AND     COALESCE(ST.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
            " AND     COALESCE(ST.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
            " AND     COALESCE(ST.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
            " Join Product                    On      ST.ITEMTYPECODE           = Product.ITEMTYPECODE" \
            " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Left Join SalesOrder SO              On      ST.Projectcode = SO.Code" \
            " Left Join ORDERPARTNER SOOrpn    ON     SO.ORDPRNCUSTOMERSUPPLIERCODE = SOOrpn.CUSTOMERSUPPLIERCODE " \
            " And SOOrpn.CUSTOMERSUPPLIERTYPE = 1 " \
            " Left Join BUSINESSPARTNER SOBp    On      SOOrpn.ORDERBUSINESSPARTNERNUMBERID = SOBp.NUMBERID " \
            " where ST.TRANSACTIONDATE between '"+startdate+"' and '"+enddate+"'" \
            " and LOGICALWAREHOUSE.CODE = '"+Warehouse+" '" \
            " and Plant.Code = '"+Company+" '" \
            " and Product.AbsUniqueid = '"+Item+" '" \
            " and ST.TemplateCode in ('S05') " \
            " Group By Plant.Longdescription " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  " \
            " ,SOBp.LEGALNAME1 " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else Varchar(ST.TRANSACTIONNUMBER) End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End " \
            " Union All" \
            " Select  Plant.Longdescription as Company" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  as StType" \
            " ,Costcenter.SHORTDESCRIPTION as Dept" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End as TxnDate" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ID.PROVISIONALCOUNTERCODE ||' '|| VARCHAR(ID.PROVISIONALCODE) End as TxnNo" \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End as TxnType" \
            " ,SUM(cast(Case When ST.TRANSACTIONDATE < '"+startdate+"' Then ST.USERPRIMARYQUANTITY Else 0 End * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End as decimal(18,2)))  as OpBal" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 1 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2))) as RecQty" \
            " ,SUM(cast(Case When STTemplate.OnHandUpdate = 2 And ST.TransactionDate Between '"+startdate+"' And '"+enddate+"' Then ST.UserPrimaryQuantity Else 0 End as decimal(18,2)))  as IssQty" \
            "  ,SUM(cast(Case When ST.TransactionDate <= '"+enddate+"' Then UserPrimaryQuantity * Case When STTemplate.OnHandUpdate = 1 Then 1 Else -1 End Else 0 End as decimal(18,2)))  as BalQty" \
            " From    StockTransaction ST" \
            " JOIN    StockTransactionTemplate STTemplate      ON      ST.TEMPLATECODE = STTemplate.Code" \
            " JOIN    FullItemKeyDecoder FIKD    ON      ST.ITEMTYPECODE    = FIKD.ITEMTYPECODE" \
            " AND     COALESCE(ST.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
            " AND     COALESCE(ST.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
            " AND     COALESCE(ST.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
            " AND     COALESCE(ST.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
            " AND     COALESCE(ST.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
            " AND     COALESCE(ST.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
            " AND     COALESCE(ST.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
            " AND     COALESCE(ST.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
            " AND     COALESCE(ST.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
            " AND     COALESCE(ST.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
            " Join Product                    On      ST.ITEMTYPECODE           = Product.ITEMTYPECODE" \
            " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
            " Join LOGICALWAREHOUSE           On      ST.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
            " Join Plant                      On      LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
            " Left Join InternalDocument ID        ON      ST.OrderCode = ID.PROVISIONALCODE" \
            " Join LOGICALWAREHOUSE IdLogical On      ID.DESTINATIONWAREHOUSECODE = IdLogical.CODE " \
            " Left Join Costcenter                 On      IdLogical.COSTCENTERCODE = Costcenter.CODE" \
            " where ST.TRANSACTIONDATE between '"+startdate+"' and '"+enddate+"'" \
             " and LOGICALWAREHOUSE.CODE = '"+Warehouse+" '" \
            " and Plant.Code = '"+Company+" '" \
            " and Product.AbsUniqueid = '"+Item+" '" \
            " and ST.TemplateCode in ('201','209','210','215','310','311','FFO','I03','I04') " \
            " Group By Plant.Longdescription " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.TEMPLATECODE  End  " \
            " ,Costcenter.SHORTDESCRIPTION " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '"+startdate+"' Else ST.TRANSACTIONDATE End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ID.PROVISIONALCOUNTERCODE ||' '|| Varchar(ID.PROVISIONALCODE) End " \
            " ,Case When ST.TRANSACTIONDATE < '"+startdate+"' Then '' Else ST.STOCKTRANSACTIONTYPE End " \
            " ) as Production" \
            " order by Production.Company,Production.TxnDate,Production.TxnNo "
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    startdate = datetime(int(startdate[0:4]), int(startdate[5:7]), int(startdate[8:]))
    enddate = datetime(int(enddate[0:4]), int(enddate[5:7]), int(enddate[8:]))
    stdt = startdate.strftime("%d %B %Y")
    etdt = enddate.strftime("%d %B %Y")
    # print(stdt,etdt)
    if result == False:
        return render(request, 'ProductLedgerDetail.html',
                      {'GDataProductLedgerDetail': GDataProductLedgerDetail, "Company": PlantName, "Item": ItemName,
                       "OpBal": OpBal, 'Warehouse': Warehouse, 'Dept':Dept
                          , "startdate": stdt, "enddate": etdt})

    Company = result['COMPANY']
    # Item = result['PRODUCTNAME']
    close = close + float(OpBal)
    RecivedQnty = 0
    IssueQnty = 0
    while result != False:
        close = close - float(result['ISSQTY']) + float(result['RECQTY'])
        RecivedQnty += float(result['RECQTY'])
        IssueQnty += float(result['ISSQTY'])
        result['CL'] = round(close,2)
        GDataProductLedgerDetail.append(result)
        result = con.db.fetch_both(stmt)
    return render(request, 'ProductLedgerDetail.html',
                  {'GDataProductLedgerDetail': GDataProductLedgerDetail,"Company":Company,"Item":ItemName,"OpBal":OpBal, 'Dept':Dept,
                      'Warehouse': Warehouse,"startdate":stdt,"enddate":etdt, 'RecivedQnty':str('{0:1.2f}'.format(RecivedQnty))
    , 'IssueQnty':str('{0:1.2f}'.format(IssueQnty))})
