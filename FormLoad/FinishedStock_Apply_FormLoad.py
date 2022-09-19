from django.shortcuts import render
from Global_Files import Connection_String as con
from datetime import date

GDataItemTypeCode = []
GDataQualityLevelCode = []
GDataPlantCode = []
GDataDetail = []
GDataPlantDetail = []
site = []
plantclcopstotal = 0
plantclboxestotal = 0
plantopnqtytotal = 0
plantrecqtytotal = 0
plantissqtytotal = 0
plantisscopstotal = 0
plantclqtytotal = 0
plantordpendqtytotal = 0

itemopenqtytotal = 0
itemrecqtytotal = 0
itemissqtytotal = 0
itemisscopstotal = 0
itemclqtytotal = 0
itemorderpendqtytotal = 0
itemclcopstotal = 0
itemclboxestotal = 0

itemdetailclqtytotal = 0
itemdetailorderpendqtytotal = 0
itemdetailclcopstotal = 0
itemdetailclboxestotal = 0


def Apply(request):
    global GDataItemTypeCode
    global GDataQualityLevelCode
    global GDataPlantCode
    global GDataDetail
    global GDataPlantDetail
    global plantclqtytotal
    global plantordpendqtytotal
    global itemclcopstotal
    global itemclboxestotal
    global itemclqtytotal
    global itemorderpendqtytotal
    global plantclboxestotal
    global plantclcopstotal
    global plantordpendqtytotal
    global plantisscopstotal
    global plantissqtytotal
    global plantrecqtytotal
    global plantopnqtytotal
    global itemrecqtytotal
    global itemissqtytotal
    global itemisscopstotal
    global itemopenqtytotal
    plantclqtytotal = 0
    plantordpendqtytotal = 0
    plantopnqtytotal = 0
    plantrecqtytotal = 0
    plantissqtytotal = 0
    plantisscopstotal = 0
    plantclcopstotal = 0
    plantclqtytotal = 0
    plantclboxestotal = 0
    itemopenqtytotal = 0
    itemrecqtytotal = 0
    itemissqtytotal = 0
    itemisscopstotal = 0
    itemclqtytotal = 0
    itemorderpendqtytotal = 0
    itemclcopstotal = 0
    itemclboxestotal = 0
    GDataQualityLevelCode = []
    GDataItemTypeCode = []
    GDataPlantCode = []
    GDataDetail = []
    GDataPlantDetail = []
    startdate = str(request.GET['datenow'])
    print("jigar",startdate)
    plantclqtytotal = 0
    plantordpendqtytotal = 0
    itemclqtytotal = 0
    itemorderpendqtytotal = 0
    itemclcopstotal = 0
    itemclboxestotal = 0
    GDataQualityLevelCode = []
    GDataItemTypeCode = []
    GDataPlantCode = []
    GDataDetail = []
    GDataPlantDetail = []
    site = []
    grade = []

    if request.GET.getlist('site'):
        Site = request.GET.getlist('site')
        for i in Site:
            site.append(i[0:3])
        QuerySite = "and Plant.Code in (" + str(site)[1:-1] + ")"
    else:
        Site = ''
        QuerySite = ''

    if request.GET.getlist('grade'):
        Grade = request.GET.getlist('grade')
        for i in Grade:
            grade.append(i[1:])
        QueryGrade = " and QualityLevel.code in (" + str(grade)[1:-1] + ")"
    else:
        Grade = ''
        QueryGrade = ''

    if request.GET.getlist('itemtype'):
        ItemType = request.GET.getlist('itemtype')
        QueryItemType = "and ITEMTYPE.CODE in (" + str(request.GET.getlist('itemtype'))[1:-1] + ")"

    else:
        ItemType = ''
        QueryItemType = ''

    print(QuerySite, QueryItemType, QueryGrade)

    sql = " Select Distinct  ITEMTYPE.CODE As ItemType " \
          "From    ITEMTYPE Order By ItemType"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        GDataItemTypeCode.append(result)
        result = con.db.fetch_both(stmt)

    sql = " Select       distinct   QualityLevel.code as Code " \
          " From    QualityLevel Order By QualityLevel.Code"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        GDataQualityLevelCode.append(result)
        result = con.db.fetch_both(stmt)

    sql = " Select    Distinct    Plant.Code as Code,  Plant.LONGDESCRIPTION As Plant" \
          " From    Plant " \
          " Order By Plant"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        GDataPlantCode.append(result)
        result = con.db.fetch_both(stmt)

    sql = "    Select  FinStk.Site,FinStk.Qlt, FinStk.Plant, FinStk.ID,FinStk.ItemCode,FinStk.ItmType" \
          ",FinStk.Product" \
          ",Sum(FinStk.OpCops) as OpCops" \
          ",Sum(FinStk.OpNetWt) as OpNetWT" \
          ",Sum(FinStk.OpBoxes) as OpBoxes" \
          ",Sum(FinStk.PCops) as PCops" \
          ",Sum(FinStk.PNetWt) as PNetWt" \
          ",Sum(FinStk.PBoxes) as PBoxes" \
          ",Sum(FinStk.IssueCops) as IssueCops" \
          ",Sum(FinStk.IssueNetWt) as IssueNetWt" \
          ",Sum(FinStk.IssueBoxes) as IssueBoxes" \
          ",Sum(FinStk.ClCops) as ClCops" \
          ",Sum(FinStk.ClNetWt) as ClNetWt" \
          ",Sum(FinStk.ClBoxes) as ClBoxes" \
          ",Sum(FinStk.OrdPenQty) as OrdPenQty" \
          " From(" \
          " Select          Plant.ShortDescription as Site,QualityLevel.ShortDescription as Qlt,COALESCE(Plant.LONGDESCRIPTION,'') As Plant,Plant.Code as ID,PRODUCT.ABSUNIQUEID as ItemCode" \
          ",ITEMTYPE.CODE As ItmType" \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Product" \
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE >= '"+startdate+"') Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3  "\
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8  "\
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13  "\
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) As INT) As OpCops  "\
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE >= '"+startdate+"') Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As OpNetWt  "\
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE >= '"+startdate+"') Then BKLELEMENTS.TOTALBOXES ELSE 0 END) As INT) As OpBoxes  "\
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE = '"+startdate+"'  "\
          " Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3  "\
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8  "\
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13  "\
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) AS INT) As PCops  "\
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE = '"+startdate+"' Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As PNetWt  "\
          ", CAST((SUM(CASE WHEN ELEMENTS.ENTRYDATE = '"+startdate+"' THEN BKLELEMENTS.TOTALBOXES ELSE 0 END)) As INT) As PBoxes  "\
          ", CAST(SUM (Case When Desp.TRANSACTIONDATE = '"+startdate+"' Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3   "\
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8  "\
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13  "\
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) AS INT) As IssueCops  "\
          ", CAST(SUM (Case When Desp.TRANSACTIONDATE = '"+startdate+"' Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As IssueNetWt  "\
          ", CAST((SUM(CASE WHEN Desp.TRANSACTIONDATE = '"+startdate+"' Then BKLELEMENTS.TOTALBOXES ELSE 0 END)) As INT) As IssueBoxes  "\
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE > '"+startdate+"') Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3   "\
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8  "\
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13  "\
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End)) AS DECIMAL(18,3)) As ClCops  "\
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE > '"+startdate+"') Then (BKLELEMENTS.ACTUALNETWT) Else 0 End)) As DECIMAL(18,3)) As ClNetWt  "\
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE > '"+startdate+"') Then (BKLELEMENTS.TOTALBOXES) Else 0 End)) As DECIMAL(18,3)) As ClBoxes  "\
",0 as OrdPenQty "\
 "From    BKLELEMENTS  "\
          "JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE = FIKD.ITEMTYPECODE  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')  "\
          "Join    PRODUCT                         On      BKLELEMENTS.LOTITEMTYPECODE = PRODUCT.ITEMTYPECODE   "\
          "And     FIKD.ItemUniqueId = Product.AbsUniqueId  "\
          ""\
          "Left Join      QualityLevel             On      BKLELEMENTS.QUALITYLEVELCODE = QUALITYLEVEL.CODE  "\
          "And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE  "\
          "Left JOIN    ItemSubcodeTemplate IST    ON      BKLELEMENTS.LOTITEMTYPECODE = IST.ItemTypeCode  "\
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07')  "\
          "LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode  "\
          "AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01 When 2 Then BKLELEMENTS.LOTDECOSUBCODE02 When 3 Then BKLELEMENTS.LOTDECOSUBCODE03 When 4 Then BKLELEMENTS.LOTDECOSUBCODE04 When 5 Then BKLELEMENTS.LOTDECOSUBCODE05  "\
          "When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code  "\
          "Join    ITEMTYPE                        On      BKLELEMENTS.LOTITEMTYPECODE = ITEMTYPE.CODE  "\
          "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE  "\
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY  "\
          "And     BKLELEMENTS.ITEMTYPECODE = ELEMENTS.ITEMTYPECODE  "\
          "And     ELEMENTS.ENTRYDATE       <=     '"+startdate+"'"+QuerySite+QueryItemType+QueryGrade+"" \
          "Join  Plant       ON           Plant.code = ELEMENTS.PLANTCODE "\
          "Left Join    StockTransaction Desp      On      BKLELEMENTS.CODE = Desp.CONTAINERELEMENTCODE  "\
          "AND     Desp.TEMPLATECODE in ('S04','I04')  "\
 "Where  BKLELEMENTS.ITEMTYPECODE = 'CNT' "\
 "Group BY COALESCE(Plant.LONGDESCRIPTION,''),Plant.ShortDescription,Plant.Code,QualityLevel.ShortDescription,PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '') "\
 ",PRODUCT.ABSUNIQUEID,ITEMTYPE.CODE,QualityLevel.CODE "\
 "Having  CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE > '"+startdate+"') Then (BKLELEMENTS.ACTUALNETWT) Else 0 End)) As DECIMAL(18,3)) <> 0.000  "\
          "Or CAST(SUM (Case When Desp.TRANSACTIONDATE = '"+startdate+"' Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) <> 0.000  "\
          "Or CAST(SUM (Case When ELEMENTS.ENTRYDATE = '"+startdate+"' Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) <> 0.000  "\
          "Or CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE >= '"+startdate+"') Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) <> 0.000  "\
          " Union All" \
          " Select Plant.ShortDescription as Site,QualityLevel.ShortDescription as Qlt ,COALESCE(Plant.LONGDESCRIPTION,'') As Plant,Plant.Code as ID,PRODUCT.ABSUNIQUEID as ItemCode" \
          ", CONCAT(COALESCE(ProdGrp.LONGDESCRIPTION,'Production And Stock Group Not Assign'), ' ('|| ITEMTYPE.CODE ||')') As ItmType" \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Product,0 as OpCops,0 as OpNetWt" \
          ",0 as OpBoxes,0 as PCops,0 as PNetWt,0 as PBoxes,0 as IssueCops,0 as IssueNetWt,0 as IssueBoxes,0 as ClCops,0 as ClNetWt,0 as ClBoxes" \
          ", cast(Sum(SOD.BASEPRIMARYQUANTITY - SOD.USEDUSERPRIMARYQUANTITY)as decimal(18,3)) As OrdPenQty" \
          " From    SalesOrderLine as SOL" \
          " JOIN FullItemKeyDecoder FIKD    ON      SOL.ITEMTYPEAFICODE    = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
          " AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
          " AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
          " AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
          " AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
          " AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
          " AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
          " Join Product                    On      SOL.ITEMTYPEAFICODE           = Product.ITEMTYPECODE" \
          " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
          " JOIN LogicalWareHouse On SOL.WAREHOUSECODE=LogicalWareHouse.CODE" \
          " JOIN Plant ON LogicalWareHouse.PLANTCODE = Plant.Code" \
          " Join SalesOrderDelivery SOD     On      SOL.SALESORDERCOUNTERCODE=SOD.SALORDLINESALORDERCOUNTERCODE" \
          " AND     SOL.SALESORDERCODE=SOD.SALESORDERLINESALESORDERCODE" \
          " AND     SOL.ORDERSUBLINE=SOD.SALESORDERLINEORDERSUBLINE" \
          " Left Join    USERGENERICGROUP ProdGrp   On      PRODUCT.SNDUSERGRPUSERGENGRPTYPECODE = ProdGrp.USERGENERICGROUPTYPECODE" \
          " And     PRODUCT.SECONDUSERGRPCODE = ProdGrp.CODE" \
          " And     ProdGrp.USERGENERICGROUPTYPECODE = 'PRG'" \
          " Join    ITEMTYPE                        On      Product.ITEMTYPECODE = ITEMTYPE.CODE" \
          " Join      QualityLevel             On      SOD.QUALITYCODE = QUALITYLEVEL.CODE" \
          " group by COALESCE(Plant.LONGDESCRIPTION,''),Plant.Code,Plant.ShortDescription,PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')" \
          " ,PRODUCT.ABSUNIQUEID,CONCAT(COALESCE(ProdGrp.LONGDESCRIPTION,'Production And Stock Group Not Assign'), ' ('|| ITEMTYPE.CODE ||')'),QualityLevel.Shortdescription" \
          " Union All" \
          " Select          Plant.ShortDescription as Site,QualityLevel.ShortDescription as Qlt,COALESCE(Plant.LONGDESCRIPTION,'') As Plant,Plant.Code as ID,PRODUCT.ABSUNIQUEID as ItemCode" \
          ", CONCAT(COALESCE(ProdGrp.LONGDESCRIPTION,'Production And Stock Group Not Assign'), ' ('|| ITEMTYPE.CODE ||')') As ItmType" \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Product" \
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (ID.PROVISIONALDOCUMENTDATE Is Null" \
          " Or ID.PROVISIONALDOCUMENTDATE >= '"+startdate+"') Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3" \
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8" \
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13" \
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) As INT) As OpCops" \
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (ID.PROVISIONALDOCUMENTDATE Is Null" \
          " Or ID.PROVISIONALDOCUMENTDATE >= '"+startdate+"') Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As OpNetWt" \
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (ID.PROVISIONALDOCUMENTDATE Is Null" \
          " Or ID.PROVISIONALDOCUMENTDATE >= '"+startdate+"') Then BKLELEMENTS.TOTALBOXES ELSE 0 END) As INT) As OpBoxes" \
          ", CAST(SUM (Case When Prod.TRANSACTIONDATE = '"+startdate+"'" \
          "Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3" \
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8" \
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13" \
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) AS INT) As PCops " \
          ", CAST(SUM (Case When Prod.TRANSACTIONDATE = '"+startdate+"' Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As PNetWt" \
          ", CAST((SUM(CASE WHEN Prod.TRANSACTIONDATE = '"+startdate+"' THEN BKLELEMENTS.TOTALBOXES ELSE 0 END)) As INT) As PBoxes" \
          ", CAST(SUM (Case When ID.PROVISIONALDOCUMENTDATE = '"+startdate+"' Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3" \
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8" \
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13" \
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) AS INT) As IssueCops" \
          ", CAST(SUM (Case When ID.PROVISIONALDOCUMENTDATE = '"+startdate+"' Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As IssueNetWt" \
          ", CAST((SUM(CASE WHEN ID.PROVISIONALDOCUMENTDATE = '"+startdate+"' Then BKLELEMENTS.TOTALBOXES ELSE 0 END)) As INT) As IssueBoxes" \
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (ID.PROVISIONALDOCUMENTDATE Is Null Or ID.PROVISIONALDOCUMENTDATE > '"+startdate+"') Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3" \
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8" \
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13" \
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End)) AS INT)*-1 As ClCops" \
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (ID.PROVISIONALDOCUMENTDATE Is Null Or ID.PROVISIONALDOCUMENTDATE > '"+startdate+"') Then (BKLELEMENTS.ACTUALNETWT) Else 0 End)) As DECIMAL(18,3))*-1 As ClNetWt" \
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (ID.PROVISIONALDOCUMENTDATE Is Null Or ID.PROVISIONALDOCUMENTDATE > '"+startdate+"') Then (BKLELEMENTS.TOTALBOXES) Else 0 End)) As INT)*-1 As ClBoxes" \
          ",0 as OrdPenQty" \
          " From InternalDocument ID" \
          " Join StockTransaction Desp        ON      ID.PROVISIONALCODE = Desp.OrderCode" \
          " Join BKLELEMENTS                On      Desp.ContainerElementCode = BKLELEMENTS.Code" \
          " JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')" \
          " Join    PRODUCT                         On      BKLELEMENTS.LOTITEMTYPECODE = PRODUCT.ITEMTYPECODE" \
          " And     FIKD.ItemUniqueId = Product.AbsUniqueId" \
           " Left Join    USERGENERICGROUP ProdGrp   On      PRODUCT.SNDUSERGRPUSERGENGRPTYPECODE = ProdGrp.USERGENERICGROUPTYPECODE" \
          " And     PRODUCT.SECONDUSERGRPCODE = ProdGrp.CODE" \
          " And     ProdGrp.USERGENERICGROUPTYPECODE = 'PRG'" \
          " Join      QualityLevel             On      BKLELEMENTS.QUALITYLEVELCODE = QUALITYLEVEL.CODE" \
          " And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE" \
          " Left JOIN    ItemSubcodeTemplate IST    ON      BKLELEMENTS.LOTITEMTYPECODE = IST.ItemTypeCode" \
          " AND     IST.GroupTypeCode  In ('MB4','P09','B07')" \
          " LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
          " AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01 When 2 Then BKLELEMENTS.LOTDECOSUBCODE02 When 3 Then BKLELEMENTS.LOTDECOSUBCODE03 When 4 Then BKLELEMENTS.LOTDECOSUBCODE04 When 5 Then BKLELEMENTS.LOTDECOSUBCODE05" \
          " When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code" \
          " Join    Lot                             On      BKLELEMENTS.LOTITEMTYPECODE = LOT.ITEMTYPECODE And     BKLELEMENTS.LOTCODE = LOT.CODE" \
          " Left Join    AdStorage Ads                   On      Lot.ABSUNIQUEID = Ads.UNIQUEID And     NameEntityName = 'Lot' And FieldName = 'SaleLot'" \
          " Join    ITEMTYPE                        On      BKLELEMENTS.LOTITEMTYPECODE = ITEMTYPE.CODE" \
          " Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE" \
          " And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY" \
          " And     BKLELEMENTS.ITEMTYPECODE = ELEMENTS.ITEMTYPECODE" \
          " And     ELEMENTS.ENTRYDATE       <=     '"+startdate+"'" \
          " Left Join    StockTransaction Prod      On      BKLELEMENTS.CODE = Prod.CONTAINERELEMENTCODE" \
          " AND     Prod.TEMPLATECODE = 'M01'" \
          " Join    LOGICALWAREHOUSE                On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
          " Join    Plant                           On            LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
          " Where ID.TemplateCode = 'I04' and BKLELEMENTS.ITEMTYPECODE = 'CNT'" \
          " And ID.PROVISIONALDOCUMENTDATE <= '"+startdate+"'"+QuerySite+QueryItemType+QueryGrade+"" \
          " Group  By COALESCE(Plant.LONGDESCRIPTION,''),Plant.ShortDescription,Plant.Code,PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')" \
          ",PRODUCT.ABSUNIQUEID,CONCAT(COALESCE(ProdGrp.LONGDESCRIPTION,'Production And Stock Group Not Assign'), ' ('|| ITEMTYPE.CODE ||')'),QualityLevel.Shortdescription" \
          " )" \
          " As FinStk" \
          " Group by FinStk.Site,FinStk.Plant, FinStk.ID,FinStk.Product,FinStk.ItemCode,FinStk.ItmType,FinStk.Qlt" \
          " Order By FinStk.Plant, FinStk.ID,FinStk.Product,FinStk.ItemCode,FinStk.ItmType,FinStk.Qlt"
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        itemopenqtytotal = itemopenqtytotal + float(result['OPNETWT'])
        itemorderpendqtytotal = itemorderpendqtytotal + float(result['ORDPENQTY'])
        itemclqtytotal = itemclqtytotal + float(result['CLNETWT'])
        itemclcopstotal = itemclcopstotal + float(result['CLCOPS'])
        itemclboxestotal = itemclboxestotal + float(result['CLBOXES'])
        itemrecqtytotal = itemrecqtytotal + float(result['PNETWT'])
        itemissqtytotal = itemissqtytotal + float(result['ISSUENETWT'])
        itemisscopstotal = itemisscopstotal + float(result['ISSUECOPS'])
        GDataDetail.append(result)
        result = con.db.fetch_both(stmt)

    sql = "    Select  FinStk.Site," \
          " Sum(FinStk.OpCops) as OpCops" \
          ",Sum(FinStk.OpNetWt) as OpNetWT" \
          ",Sum(FinStk.OpBoxes) as OpBoxes" \
          ",Sum(FinStk.PCops) as PCops" \
          ",Sum(FinStk.PNetWt) as PNetWt" \
          ",Sum(FinStk.PBoxes) as PBoxes" \
          ",Sum(FinStk.IssueCops) as IssueCops" \
          ",Sum(FinStk.IssueNetWt) as IssueNetWt" \
          ",Sum(FinStk.IssueBoxes) as IssueBoxes" \
          ",Sum(FinStk.ClCops) as ClCops" \
          ",Sum(FinStk.ClNetWt) as ClNetWt" \
          ",Sum(FinStk.ClBoxes) as ClBoxes" \
          ",Sum(FinStk.OrdPenQty) as OrdPenQty" \
          " From(" \
          " Select          Plant.ShortDescription as Site,QualityLevel.ShortDescription as Qlt,COALESCE(Plant.LONGDESCRIPTION,'') As Plant,Plant.Code as ID,PRODUCT.ABSUNIQUEID as ItemCode" \
          ",ITEMTYPE.CODE As ItmType" \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Product" \
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE >= '"+startdate+"') Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3  "\
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8  "\
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13  "\
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) As INT) As OpCops  "\
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE >= '"+startdate+"') Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As OpNetWt  "\
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE >= '"+startdate+"') Then BKLELEMENTS.TOTALBOXES ELSE 0 END) As INT) As OpBoxes  "\
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE = '"+startdate+"'  "\
          " Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3  "\
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8  "\
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13  "\
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) AS INT) As PCops  "\
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE = '"+startdate+"' Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As PNetWt  "\
          ", CAST((SUM(CASE WHEN ELEMENTS.ENTRYDATE = '"+startdate+"' THEN BKLELEMENTS.TOTALBOXES ELSE 0 END)) As INT) As PBoxes  "\
          ", CAST(SUM (Case When Desp.TRANSACTIONDATE = '"+startdate+"' Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3   "\
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8  "\
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13  "\
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) AS INT) As IssueCops  "\
          ", CAST(SUM (Case When Desp.TRANSACTIONDATE = '"+startdate+"' Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As IssueNetWt  "\
          ", CAST((SUM(CASE WHEN Desp.TRANSACTIONDATE = '"+startdate+"' Then BKLELEMENTS.TOTALBOXES ELSE 0 END)) As INT) As IssueBoxes  "\
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE > '"+startdate+"') Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3   "\
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8  "\
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13  "\
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End)) AS DECIMAL(18,3)) As ClCops  "\
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE > '"+startdate+"') Then (BKLELEMENTS.ACTUALNETWT) Else 0 End)) As DECIMAL(18,3)) As ClNetWt  "\
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE > '"+startdate+"') Then (BKLELEMENTS.TOTALBOXES) Else 0 End)) As DECIMAL(18,3)) As ClBoxes  "\
",0 as OrdPenQty "\
 "From    BKLELEMENTS  "\
          "JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE = FIKD.ITEMTYPECODE  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')  "\
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')  "\
          "Join    PRODUCT                         On      BKLELEMENTS.LOTITEMTYPECODE = PRODUCT.ITEMTYPECODE   "\
          "And     FIKD.ItemUniqueId = Product.AbsUniqueId  "\
          ""\
          "Left Join      QualityLevel             On      BKLELEMENTS.QUALITYLEVELCODE = QUALITYLEVEL.CODE  "\
          "And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE  "\
          "Left JOIN    ItemSubcodeTemplate IST    ON      BKLELEMENTS.LOTITEMTYPECODE = IST.ItemTypeCode  "\
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07')  "\
          "LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode  "\
          "AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01 When 2 Then BKLELEMENTS.LOTDECOSUBCODE02 When 3 Then BKLELEMENTS.LOTDECOSUBCODE03 When 4 Then BKLELEMENTS.LOTDECOSUBCODE04 When 5 Then BKLELEMENTS.LOTDECOSUBCODE05  "\
          "When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code  "\
          "Join    ITEMTYPE                        On      BKLELEMENTS.LOTITEMTYPECODE = ITEMTYPE.CODE  "\
          "Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE  "\
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY  "\
          "And     BKLELEMENTS.ITEMTYPECODE = ELEMENTS.ITEMTYPECODE  "\
          "And     ELEMENTS.ENTRYDATE       <=     '"+startdate+"'"+QuerySite+QueryItemType+QueryGrade+"" \
          "Join  Plant       ON           Plant.code = ELEMENTS.PLANTCODE "\
          "Left Join    StockTransaction Desp      On      BKLELEMENTS.CODE = Desp.CONTAINERELEMENTCODE  "\
          "AND     Desp.TEMPLATECODE in ('S04','I04')  "\
 "Where  BKLELEMENTS.ITEMTYPECODE = 'CNT' "\
 "Group BY COALESCE(Plant.LONGDESCRIPTION,''),Plant.ShortDescription,Plant.Code,QualityLevel.ShortDescription,PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '') "\
 ",PRODUCT.ABSUNIQUEID,ITEMTYPE.CODE,QualityLevel.CODE "\
 "Having  CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE > '"+startdate+"') Then (BKLELEMENTS.ACTUALNETWT) Else 0 End)) As DECIMAL(18,3)) <> 0.000  "\
          "Or CAST(SUM (Case When Desp.TRANSACTIONDATE = '"+startdate+"' Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) <> 0.000  "\
          "Or CAST(SUM (Case When ELEMENTS.ENTRYDATE = '"+startdate+"' Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) <> 0.000  "\
          "Or CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (Desp.TRANSACTIONDATE Is Null Or Desp.TRANSACTIONDATE >= '"+startdate+"') Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) <> 0.000  "\
          " Union All" \
          " Select Plant.ShortDescription as Site,QualityLevel.ShortDescription as Qlt ,COALESCE(Plant.LONGDESCRIPTION,'') As Plant,Plant.Code as ID,PRODUCT.ABSUNIQUEID as ItemCode" \
          ", CONCAT(COALESCE(ProdGrp.LONGDESCRIPTION,'Production And Stock Group Not Assign'), ' ('|| ITEMTYPE.CODE ||')') As ItmType" \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Product,0 as OpCops,0 as OpNetWt" \
          ",0 as OpBoxes,0 as PCops,0 as PNetWt,0 as PBoxes,0 as IssueCops,0 as IssueNetWt,0 as IssueBoxes,0 as ClCops,0 as ClNetWt,0 as ClBoxes" \
          ", cast(Sum(SOD.BASEPRIMARYQUANTITY - SOD.USEDUSERPRIMARYQUANTITY)as decimal(18,3)) As OrdPenQty" \
          " From    SalesOrderLine as SOL" \
          " JOIN FullItemKeyDecoder FIKD    ON      SOL.ITEMTYPEAFICODE    = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
          " AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
          " AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
          " AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
          " AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
          " AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
          " AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
          " Join Product                    On      SOL.ITEMTYPEAFICODE           = Product.ITEMTYPECODE" \
          " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
          " JOIN LogicalWareHouse On SOL.WAREHOUSECODE=LogicalWareHouse.CODE" \
          " JOIN Plant ON LogicalWareHouse.PLANTCODE = Plant.Code" \
          " Join SalesOrderDelivery SOD     On      SOL.SALESORDERCOUNTERCODE=SOD.SALORDLINESALORDERCOUNTERCODE" \
          " AND     SOL.SALESORDERCODE=SOD.SALESORDERLINESALESORDERCODE" \
          " AND     SOL.ORDERSUBLINE=SOD.SALESORDERLINEORDERSUBLINE" \
          " Left Join    USERGENERICGROUP ProdGrp   On      PRODUCT.SNDUSERGRPUSERGENGRPTYPECODE = ProdGrp.USERGENERICGROUPTYPECODE" \
          " And     PRODUCT.SECONDUSERGRPCODE = ProdGrp.CODE" \
          " And     ProdGrp.USERGENERICGROUPTYPECODE = 'PRG'" \
          " Join    ITEMTYPE                        On      Product.ITEMTYPECODE = ITEMTYPE.CODE" \
          " Join      QualityLevel             On      SOD.QUALITYCODE = QUALITYLEVEL.CODE" \
          " group by COALESCE(Plant.LONGDESCRIPTION,''),Plant.Code,Plant.ShortDescription,PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')" \
          " ,PRODUCT.ABSUNIQUEID,CONCAT(COALESCE(ProdGrp.LONGDESCRIPTION,'Production And Stock Group Not Assign'), ' ('|| ITEMTYPE.CODE ||')'),QualityLevel.Shortdescription" \
          " Union All" \
          " Select          Plant.ShortDescription as Site,QualityLevel.ShortDescription as Qlt,COALESCE(Plant.LONGDESCRIPTION,'') As Plant,Plant.Code as ID,PRODUCT.ABSUNIQUEID as ItemCode" \
          ", CONCAT(COALESCE(ProdGrp.LONGDESCRIPTION,'Production And Stock Group Not Assign'), ' ('|| ITEMTYPE.CODE ||')') As ItmType" \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '') As Product" \
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (ID.PROVISIONALDOCUMENTDATE Is Null" \
          " Or ID.PROVISIONALDOCUMENTDATE >= '"+startdate+"') Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3" \
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8" \
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13" \
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) As INT) As OpCops" \
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (ID.PROVISIONALDOCUMENTDATE Is Null" \
          " Or ID.PROVISIONALDOCUMENTDATE >= '"+startdate+"') Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As OpNetWt" \
          ", CAST(SUM (Case When ELEMENTS.ENTRYDATE < '"+startdate+"' AND (ID.PROVISIONALDOCUMENTDATE Is Null" \
          " Or ID.PROVISIONALDOCUMENTDATE >= '"+startdate+"') Then BKLELEMENTS.TOTALBOXES ELSE 0 END) As INT) As OpBoxes" \
          ", CAST(SUM (Case When Prod.TRANSACTIONDATE = '"+startdate+"'" \
          "Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3" \
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8" \
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13" \
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) AS INT) As PCops " \
          ", CAST(SUM (Case When Prod.TRANSACTIONDATE = '"+startdate+"' Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As PNetWt" \
          ", CAST((SUM(CASE WHEN Prod.TRANSACTIONDATE = '"+startdate+"' THEN BKLELEMENTS.TOTALBOXES ELSE 0 END)) As INT) As PBoxes" \
          ", CAST(SUM (Case When ID.PROVISIONALDOCUMENTDATE = '"+startdate+"' Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3" \
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8" \
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13" \
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End) AS INT) As IssueCops" \
          ", CAST(SUM (Case When ID.PROVISIONALDOCUMENTDATE = '"+startdate+"' Then (BKLELEMENTS.ACTUALNETWT) Else 0 End) As DECIMAL(18,3)) As IssueNetWt" \
          ", CAST((SUM(CASE WHEN ID.PROVISIONALDOCUMENTDATE = '"+startdate+"' Then BKLELEMENTS.TOTALBOXES ELSE 0 END)) As INT) As IssueBoxes" \
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (ID.PROVISIONALDOCUMENTDATE Is Null Or ID.PROVISIONALDOCUMENTDATE > '"+startdate+"') Then (BKLELEMENTS.COPSQUANTITY1 + BKLELEMENTS.COPSQUANTITY2 + BKLELEMENTS.COPSQUANTITY3" \
          "+ BKLELEMENTS.COPSQUANTITY4 + BKLELEMENTS.COPSQUANTITY5 + BKLELEMENTS.COPSQUANTITY6 + BKLELEMENTS.COPSQUANTITY7 + BKLELEMENTS.COPSQUANTITY8" \
          "+ BKLELEMENTS.COPSQUANTITY9 + BKLELEMENTS.COPSQUANTITY10 + BKLELEMENTS.COPSQUANTITY11 + BKLELEMENTS.COPSQUANTITY12 + BKLELEMENTS.COPSQUANTITY13" \
          "+ BKLELEMENTS.COPSQUANTITY14 + BKLELEMENTS.COPSQUANTITY15) Else 0 End)) AS INT)*-1 As ClCops" \
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (ID.PROVISIONALDOCUMENTDATE Is Null Or ID.PROVISIONALDOCUMENTDATE > '"+startdate+"') Then (BKLELEMENTS.ACTUALNETWT) Else 0 End)) As DECIMAL(18,3))*-1 As ClNetWt" \
          ", CAST((SUM (Case When ELEMENTS.ENTRYDATE <= '"+startdate+"' AND (ID.PROVISIONALDOCUMENTDATE Is Null Or ID.PROVISIONALDOCUMENTDATE > '"+startdate+"') Then (BKLELEMENTS.TOTALBOXES) Else 0 End)) As INT)*-1 As ClBoxes" \
          ",0 as OrdPenQty" \
          " From InternalDocument ID" \
          " Join StockTransaction Desp        ON      ID.PROVISIONALCODE = Desp.OrderCode" \
          " Join BKLELEMENTS                On      Desp.ContainerElementCode = BKLELEMENTS.Code" \
          " JOIN    FULLITEMKEYDECODER FIKD         ON      BKLELEMENTS.LOTITEMTYPECODE = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '')" \
          " AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '')" \
          " Join    PRODUCT                         On      BKLELEMENTS.LOTITEMTYPECODE = PRODUCT.ITEMTYPECODE" \
          " And     FIKD.ItemUniqueId = Product.AbsUniqueId" \
           " Left Join    USERGENERICGROUP ProdGrp   On      PRODUCT.SNDUSERGRPUSERGENGRPTYPECODE = ProdGrp.USERGENERICGROUPTYPECODE" \
          " And     PRODUCT.SECONDUSERGRPCODE = ProdGrp.CODE" \
          " And     ProdGrp.USERGENERICGROUPTYPECODE = 'PRG'" \
          " Join      QualityLevel             On      BKLELEMENTS.QUALITYLEVELCODE = QUALITYLEVEL.CODE" \
          " And     BKLELEMENTS.LOTITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE" \
          " Left JOIN    ItemSubcodeTemplate IST    ON      BKLELEMENTS.LOTITEMTYPECODE = IST.ItemTypeCode" \
          " AND     IST.GroupTypeCode  In ('MB4','P09','B07')" \
          " LEFT JOIN UserGenericGroup UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
          " AND     Case IST.Position When 1 Then BKLELEMENTS.LOTDECOSUBCODE01 When 2 Then BKLELEMENTS.LOTDECOSUBCODE02 When 3 Then BKLELEMENTS.LOTDECOSUBCODE03 When 4 Then BKLELEMENTS.LOTDECOSUBCODE04 When 5 Then BKLELEMENTS.LOTDECOSUBCODE05" \
          " When 6 Then BKLELEMENTS.LOTDECOSUBCODE06 When 7 Then BKLELEMENTS.LOTDECOSUBCODE07 When 8 Then BKLELEMENTS.LOTDECOSUBCODE08 When 9 Then BKLELEMENTS.LOTDECOSUBCODE09 When 10 Then BKLELEMENTS.LOTDECOSUBCODE10 End = UGG.Code" \
          " Join    Lot                             On      BKLELEMENTS.LOTITEMTYPECODE = LOT.ITEMTYPECODE And     BKLELEMENTS.LOTCODE = LOT.CODE" \
          " Left Join    AdStorage Ads                   On      Lot.ABSUNIQUEID = Ads.UNIQUEID And     NameEntityName = 'Lot' And FieldName = 'SaleLot'" \
          " Join    ITEMTYPE                        On      BKLELEMENTS.LOTITEMTYPECODE = ITEMTYPE.CODE" \
          " Join    ELEMENTS                        On      BKLELEMENTS.CODE = ELEMENTS.CODE" \
          " And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY" \
          " And     BKLELEMENTS.ITEMTYPECODE = ELEMENTS.ITEMTYPECODE" \
          " And     ELEMENTS.ENTRYDATE       <=     '"+startdate+"'" \
          " Left Join    StockTransaction Prod      On      BKLELEMENTS.CODE = Prod.CONTAINERELEMENTCODE" \
          " AND     Prod.TEMPLATECODE = 'M01'" \
          " Join    LOGICALWAREHOUSE                On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
          " Join    Plant                           On            LOGICALWAREHOUSE.PLANTCODE = Plant.Code" \
          " Where ID.TemplateCode = 'I04' and BKLELEMENTS.ITEMTYPECODE = 'CNT'" \
          " And ID.PROVISIONALDOCUMENTDATE <= '"+startdate+"'"+QuerySite+QueryItemType+QueryGrade+"" \
          " Group  By COALESCE(Plant.LONGDESCRIPTION,''),Plant.ShortDescription,Plant.Code,PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QualityLevel.ShortDescription, '')" \
          ",PRODUCT.ABSUNIQUEID,CONCAT(COALESCE(ProdGrp.LONGDESCRIPTION,'Production And Stock Group Not Assign'), ' ('|| ITEMTYPE.CODE ||')'),QualityLevel.Shortdescription" \
          " )" \
          " As FinStk" \
          " Group by FinStk.Site" \
          " Order By FinStk.Site"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        plantclqtytotal = plantclqtytotal + float(result['CLNETWT'])
        plantordpendqtytotal = plantordpendqtytotal + float(result['ORDPENQTY'])
        plantopnqtytotal = plantopnqtytotal + float(result['OPNETWT'])
        plantrecqtytotal = plantrecqtytotal + float(result['PNETWT'])
        plantissqtytotal = plantissqtytotal + float(result['ISSUENETWT'])
        plantisscopstotal = plantisscopstotal + float(result['ISSUECOPS'])
        plantclboxestotal = plantclboxestotal + float(result['CLBOXES'])
        plantclcopstotal = plantclcopstotal + float(result['CLCOPS'])
        GDataPlantDetail.append(result)
        result = con.db.fetch_both(stmt)

    return render(request, 'FinishedStock.html',
                  {'GDataItemTypeCode': GDataItemTypeCode, "GDataQualityLevelCode": GDataQualityLevelCode,
                   "GDataPlantCode": GDataPlantCode, "GDataDetail": GDataDetail,
                   "GDataPlantDetail": GDataPlantDetail, "ItemType": ItemType, "Grade": Grade, "Site": Site
                      , "plantclqtytotal": round(plantclqtytotal), "plantordpendqtytotal": round(plantordpendqtytotal),
                   'plantopnqtytotal': round(plantopnqtytotal)
                      , 'plantissqtytotal': round(plantissqtytotal), 'plantisscopstotal': round(plantisscopstotal)
                      , 'plantrecqtytotal': round(plantrecqtytotal), 'plantclcopstotal': round(plantclcopstotal),
                   'plantclboxestotal': round(plantclboxestotal)
                      , "itemclqtytotal": round(itemclqtytotal), "itemorderpendqtytotal": round(itemorderpendqtytotal),
                   "itemclcopstotal": round(itemclcopstotal)
                      , "itemclboxestotal": round(itemclboxestotal), 'itemrecqtytotal': round(itemrecqtytotal),
                   'itemissqtytotal': round(itemissqtytotal)
                      , 'itemisscopstotal': round(itemisscopstotal), 'itemopenqtytotal': round(itemopenqtytotal),
                   'startdate': startdate})
