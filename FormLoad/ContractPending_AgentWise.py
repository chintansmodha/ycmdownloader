import json
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import render
from Global_Files import Connection_String as con
GDataItemGroup=[]
GDataItemDetail=[]
GDataItemType=[]
GDataItemSubDetail=[]
sumcontractqty=0
sumdespnotgn=0
sumgoodnotgn=0
sumtotal=0
detcontractqty=0
detdespnotgn=0
detgoodnotgn=0
dettotal = 0
item=''
LSItemCode=''
ItemType=''
Item=[]
def ContractPending_AgentWise(request):
      global GDataItemGroup
      global GDataItemType
      global sumdespnotgn
      global sumgoodnotgn
      global sumcontractqty
      global sumtotal
      global item
      global LSItemCode
      sumcontractqty = 0
      sumdespnotgn = 0
      sumgoodnotgn = 0
      sumtotal = 0
      GDataItemGroup = []
      GDataItemType = []
      sql1 = "Select " \
             " Distinct Product.ITEMTYPECODE as ItemType" \
             " from SalesOrder SO" \
             " Join Division           On      SO.DIVISIONCODE = Division.Code" \
             " Join Agent              on      SO.Agent1Code = Agent.code" \
             " join OrderPartner       On      SO.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode" \
             " And     OrderPartner.CustomerSupplierType = 1" \
             " join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId=BusinessPartner.NumberID" \
             " JOIN SalesOrderLine SOL      ON         SO.CODE                 = SOL.SalesOrderCODE" \
             " AND        SO.COUNTERCODE          = SOL.SalesOrderCOUNTERCODE" \
             " And        SO.DocumentTypeType     = SOL.DocumentTypeType" \
             " JOIN FullItemKeyDecoder FIKD ON      SOL.ITEMTYPEAFICODE    = FIKD.ITEMTYPECODE" \
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
             " Join Product                On      SOL.ITEMTYPEAFICODE           = Product.ITEMTYPECODE" \
             " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
             " Join QualityLevel           On      SOL.QualityCode               = QualityLevel.Code" \
             " And     SOL.ITEMTYPEAFICODE           = QualityLevel.ItemTypeCode" \
             " Join SalesOrderDelivery SOD  On     SOL.SalesOrderCODE            = SOD.SalesOrderLineSalesOrderCODE" \
             " AND    SOL.SalesOrderCOUNTERCODE     = SOD.SalOrdLineSalOrderCOUNTERCODE" \
             " AND    SOL.OrderLine               = SOD.SalesOrderLineOrderLine" \
             " Left JOIN ItemSubcodeTemplate IST ON     SOL.ITEMTYPEAFICODE = IST.ItemTypeCode" \
             " AND     IST.GroupTypeCode In ('MB4','P09','B07')" \
             " Left JOIN UserGenericGroup UGG ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
             " AND     Case IST.Position When 1 Then SOL.SubCode01 When 2 Then SOL.SubCode02 When 3 Then SOL.SubCode03 When 4 Then SOL.SubCode04 When 5 Then SOL.SubCode05" \
             " When 6 Then SOL.SubCode06 When 7 Then SOL.SubCode07 When 8 Then SOL.SubCode08 When 9 Then SOL.SubCode09 When 10 Then SOL.SubCode10 End = UGG.Code" \
             " where SOL.PROGRESSSTATUS in(0,1)" \
             " and SO.DOCUMENTTYPETYPE in ('00','02','03')" \
             " order by ItemType"

      stmt1 = con.db.prepare(con.conn, sql1)
      con.db.execute(stmt1)
      result1 = con.db.fetch_both(stmt1)
      while result1 != False:
          GDataItemType.append(result1['ITEMTYPE'])
          result1 = con.db.fetch_both(stmt1)


      sql = "Select " \
            "Agent.Longdescription as Agent" \
            ", sum(cast(Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End as decimal(18,2)))  As PendContractQty " \
            ", sum(cast(Case When SO.DOCUMENTTYPETYPE = '03' Then SOL.UserPrimaryQuantity Else 0 End as decimal(18,2)))  As DespOrderQty" \
            ", sum(cast(Case When SO.DOCUMENTTYPETYPE = '03' Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End as decimal(18,2)))  As PendDespOrderQty " \
            ", sum(cast(Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOL.UserPrimaryQuantity Else 0 End as decimal(18,2)))  As ContractQty " \
            " from SalesOrder SO" \
            " Join Division           On      SO.DIVISIONCODE = Division.Code" \
            " Join Agent              on      SO.Agent1Code = Agent.code" \
            " join OrderPartner       On      SO.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode" \
            " And     OrderPartner.CustomerSupplierType = 1" \
            " join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId=BusinessPartner.NumberID" \
            " JOIN SalesOrderLine SOL      ON         SO.CODE                 = SOL.SalesOrderCODE" \
            " AND        SO.COUNTERCODE          = SOL.SalesOrderCOUNTERCODE" \
            " And        SO.DocumentTypeType     = SOL.DocumentTypeType" \
            " JOIN FullItemKeyDecoder FIKD ON      SOL.ITEMTYPEAFICODE    = FIKD.ITEMTYPECODE" \
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
            " Join Product                On      SOL.ITEMTYPEAFICODE           = Product.ITEMTYPECODE" \
            " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
            " Join QualityLevel           On      SOL.QualityCode               = QualityLevel.Code" \
            " And     SOL.ITEMTYPEAFICODE           = QualityLevel.ItemTypeCode" \
            " Join SalesOrderDelivery SOD  On     SOL.SalesOrderCODE            = SOD.SalesOrderLineSalesOrderCODE" \
            " AND    SOL.SalesOrderCOUNTERCODE     = SOD.SalOrdLineSalOrderCOUNTERCODE" \
            " AND    SOL.OrderLine               = SOD.SalesOrderLineOrderLine" \
            " Left JOIN ItemSubcodeTemplate IST ON     SOL.ITEMTYPEAFICODE = IST.ItemTypeCode" \
            " AND     IST.GroupTypeCode In ('MB4','P09','B07')" \
            " Left JOIN UserGenericGroup UGG ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
            " AND     Case IST.Position When 1 Then SOL.SubCode01 When 2 Then SOL.SubCode02 When 3 Then SOL.SubCode03 When 4 Then SOL.SubCode04 When 5 Then SOL.SubCode05" \
            " When 6 Then SOL.SubCode06 When 7 Then SOL.SubCode07 When 8 Then SOL.SubCode08 When 9 Then SOL.SubCode09 When 10 Then SOL.SubCode10 End = UGG.Code" \
            " where SOL.PROGRESSSTATUS in(0,1)" \
            " and SO.DOCUMENTTYPETYPE in ('00','02','03')" \
            " group by Agent.Longdescription"\
            " order by Agent"

      stmt = con.db.prepare(con.conn, sql)
      con.db.execute(stmt)
      result = con.db.fetch_both(stmt)
      while result != False:
            result['TOTAL'] = round(float(result['PENDCONTRACTQTY']) + float(result['PENDDESPORDERQTY']))
            sumcontractqty = round(sumcontractqty + float(result['CONTRACTQTY']))
            sumdespnotgn = round(sumdespnotgn + float(result['PENDCONTRACTQTY']))
            sumgoodnotgn = round(sumgoodnotgn + float(result['PENDDESPORDERQTY']))
            sumtotal = round(sumtotal + float(result['TOTAL']))
            GDataItemGroup.append(result)
            result = con.db.fetch_both(stmt)
      return render(request, 'ContractPending_AgentWise.html',
                    {'GDataItemGroup': GDataItemGroup,'GDataItemType':GDataItemType,
                                                  'sumcontractqty':round(sumcontractqty,2),'sumdespnotgn':round(sumdespnotgn,2)
            ,'sumgoodnotgn':round(sumgoodnotgn,2),'sumtotal':round(sumtotal,2)})

def ContractPending_AgentItemDetail(request):
      global GDataItemDetail
      global detcontractqty
      global detdespnotgn
      global detgoodnotgn
      global dettotal
      global item
      global LSItemCode
      global ItemType
      detcontractqty = 0
      detdespnotgn = 0
      detgoodnotgn = 0
      dettotal = 0
      GDataItemDetail = []
      ItemType=''
      itemtype = request.GET['itemtype']
      LSItemCode=request.GET['itemcode']
      for i in range(0,len(itemtype)+1,4):
          if i+3 < len(itemtype)+1:
              a = itemtype[i:i+3]
              b= ''+a+''
              Item.append(b)
      print(Item)

      if not itemtype:
          ItemType=''
      else:
          ItemType="and Product.ItemTypeCode in("+str(Item)[1:-1]+")"

      sql = "Select  Product.LONGDESCRIPTION as Item" \
            ", sum(cast(Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End as decimal(18,2)))  As PendContractQty" \
            ", sum(cast(Case When SO.DOCUMENTTYPETYPE = '03' Then SOL.UserPrimaryQuantity Else 0 End as decimal(18,2)))  As DespOrderQty" \
            ", sum(cast(Case When SO.DOCUMENTTYPETYPE = '03' Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End as decimal(18,2)))  As PendDespOrderQty" \
            ", sum(cast(Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOL.UserPrimaryQuantity Else 0 End as decimal(18,2)))  As ContractQty" \
            " from SalesOrder SO" \
            " Join Division           On      SO.DIVISIONCODE = Division.Code" \
            " Join Agent              on      SO.Agent1Code = Agent.code" \
            " join OrderPartner       On      SO.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode" \
            " And     OrderPartner.CustomerSupplierType = 1" \
            " join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId=BusinessPartner.NumberID" \
            " JOIN SalesOrderLine SOL      ON         SO.CODE                 = SOL.SalesOrderCODE" \
            " AND        SO.COUNTERCODE          = SOL.SalesOrderCOUNTERCODE" \
            " And        SO.DocumentTypeType     = SOL.DocumentTypeType" \
            " JOIN FullItemKeyDecoder FIKD ON      SOL.ITEMTYPEAFICODE    = FIKD.ITEMTYPECODE" \
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
            " Join Product                On      SOL.ITEMTYPEAFICODE           = Product.ITEMTYPECODE" \
            " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
            " Join QualityLevel           On      SOL.QualityCode               = QualityLevel.Code" \
            " And     SOL.ITEMTYPEAFICODE           = QualityLevel.ItemTypeCode" \
            " Join SalesOrderDelivery SOD  On     SOL.SalesOrderCODE            = SOD.SalesOrderLineSalesOrderCODE" \
            " AND    SOL.SalesOrderCOUNTERCODE     = SOD.SalOrdLineSalOrderCOUNTERCODE" \
            " AND    SOL.OrderLine               = SOD.SalesOrderLineOrderLine" \
            " Left JOIN ItemSubcodeTemplate IST ON     SOL.ITEMTYPEAFICODE = IST.ItemTypeCode" \
            " AND     IST.GroupTypeCode In ('MB4','P09','B07')" \
            " Left JOIN UserGenericGroup UGG ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
            " AND     Case IST.Position When 1 Then SOL.SubCode01 When 2 Then SOL.SubCode02 When 3 Then SOL.SubCode03 When 4 Then SOL.SubCode04 When 5 Then SOL.SubCode05" \
            " When 6 Then SOL.SubCode06 When 7 Then SOL.SubCode07 When 8 Then SOL.SubCode08 When 9 Then SOL.SubCode09 When 10 Then SOL.SubCode10 End = UGG.Code" \
            " where SOL.PROGRESSSTATUS in(0,1) " \
            " and SO.DOCUMENTTYPETYPE in ('00','02','03')" \
            " and Agent.LONGDESCRIPTION='"+LSItemCode+"'"+ItemType+"" \
            "group by Product.LONGDESCRIPTION " \
            " order by Item"
      print(sql)
      stmt = con.db.prepare(con.conn, sql)
      con.db.execute(stmt)
      result = con.db.fetch_both(stmt)
      while result != False:
            result['TOTAL'] = float(result['PENDCONTRACTQTY']) + float(result['DESPORDERQTY'])
            detcontractqty = detcontractqty + float(result['CONTRACTQTY'])
            detdespnotgn = detdespnotgn + float(result['PENDCONTRACTQTY'])
            detgoodnotgn = detgoodnotgn + float(result['DESPORDERQTY'])
            dettotal = dettotal + float(result['TOTAL'])
            GDataItemDetail.append(result)
            result = con.db.fetch_both(stmt)
      return render(request, 'ContractPending_AgentWise.html',
                    {'GDataItemGroup': GDataItemGroup,'GDataItemDetail': GDataItemDetail,'GDataItemType':GDataItemType,
                     'sumcontractqty': round(sumcontractqty, 2), 'sumdespnotgn': round(sumdespnotgn, 2)
                          , 'sumgoodnotgn': round(sumgoodnotgn, 2), 'sumtotal': round(sumtotal, 2)
                     ,'detcontractqty': round(detcontractqty, 2), 'detdespnotgn': round(detdespnotgn, 2)
                          , 'detgoodnotgn': round(detgoodnotgn, 2), 'dettotal': round(dettotal, 2),'itemgroup':LSItemCode,"ItemType":Item})

def ContractPending_AgentItemSubDetail(request):
      global GDataItemSubDetail
      global GDataItemDetail
      global GDataItemGroup
      global GDataItemType
      global item
      global LSItemCode
      GDataItemSubDetail=[]
      LSItem=request.GET['itemcode']
      item = LSItem
      global ItemType
      ItemType = ''
      itemtype = request.GET['itemtype']
      LSItemCode = request.GET['itemcode']
      for i in range(0, len(itemtype) + 1, 4):
          if i + 3 < len(itemtype) + 1:
              a = itemtype[i:i + 3]
              b = '' + a + ''
              Item.append(b)
      print(Item)

      if not itemtype:
          ItemType = ''
      else:
          ItemType = "and Product.ItemTypeCode in(" + str(Item)[1:-1] + ")"
      sql="Select cast(sum(Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End+Case When SO.DOCUMENTTYPETYPE = '03' Then SOL.UserPrimaryQuantity Else 0 End) as decimal(18,2)) as baldesp," \
          "SO.CODE,VARCHAR_FORMAT(SO.ORDERDATE, 'DD-MM-YYYY') as ORDERDATE" \
          ", BusinessPartner.LegalName1 As Customer" \
          ", COALESCE(UGG.LongDescription,'') As ShadeName" \
          ", Product.LongDescription As Product" \
          ", COALESCE(UGG.Code,'') As ShadeCode" \
          ", QualityLevel.ShortDescription As Quality" \
          ", SO.EXTERNALREFERENCE as EXTERNALREFERENCE," \
          " SO.DOCUMENTTYPETYPE as DocType" \
          ",Agent.LongDescription as Broker" \
          ", cast(Sum(Case When ITaxCode = 'BSR' Then ITD.CalculatedValue Else 0 End) as decimal(18)) As RateWithoutDhara" \
          ", cast(Sum(Case When ITaxCode = 'DRD' Then ITD.CalculatedValue Else 0 End) as decimal(18)) As DharaRate " \
          ", cast(Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOL.UserPrimaryQuantity Else 0 End as decimal(18,2)) As ContractQty" \
          ", cast(Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End as decimal(18,2)) As PendContractQty" \
          ", cast(Case When SO.DOCUMENTTYPETYPE = '03' Then SOL.UserPrimaryQuantity Else 0 End as decimal(18,2)) As DespOrderQty" \
          ", cast(Case When SO.DOCUMENTTYPETYPE = '03' Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End as decimal(18,2)) As PendDespOrderQty" \
          ", Agent.LongDescription As AgentName" \
          " from SalesOrder SO" \
          " Join Division           On      SO.DIVISIONCODE = Division.Code" \
          " Join Agent              on      SO.Agent1Code = Agent.code" \
          " join OrderPartner       On      SO.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode" \
          " And     OrderPartner.CustomerSupplierType = 1" \
          " join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId=BusinessPartner.NumberID" \
          " JOIN SalesOrderLine SOL      ON         SO.CODE                 = SOL.SalesOrderCODE" \
          " AND        SO.COUNTERCODE          = SOL.SalesOrderCOUNTERCODE" \
          " And        SO.DocumentTypeType     = SOL.DocumentTypeType" \
          " JOIN FullItemKeyDecoder FIKD ON      SOL.ITEMTYPEAFICODE    = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
          " AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          " AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          " AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          " AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          " AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          " AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          " AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          " AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          " Join Product                On      SOL.ITEMTYPEAFICODE           = Product.ITEMTYPECODE " \
          " And     FIKD.ItemUniqueId             = Product.AbsUniqueID" \
          " Left JOIN IndTaxDetail ITD        ON      SOL.AbsUniqueId = ITD.AbsUniqueId" \
          " And TaxCategoryCode = 'OTH' And ITaxCode In ('INR','DRD','BSR')" \
          " Join QualityLevel           On      SOL.QualityCode               = QualityLevel.Code" \
          " And     SOL.ITEMTYPEAFICODE           = QualityLevel.ItemTypeCode" \
          " Join SalesOrderDelivery SOD  On     SOL.SalesOrderCODE            = SOD.SalesOrderLineSalesOrderCODE" \
          " AND    SOL.SalesOrderCOUNTERCODE     = SOD.SalOrdLineSalOrderCOUNTERCODE" \
          " AND    SOL.OrderLine               = SOD.SalesOrderLineOrderLine" \
          " Left JOIN ItemSubcodeTemplate IST ON     SOL.ITEMTYPEAFICODE = IST.ItemTypeCode" \
          " AND     IST.GroupTypeCode In ('MB4','P09','B07')" \
          " Left JOIN UserGenericGroup UGG ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
          " AND     Case IST.Position When 1 Then SOL.SubCode01 When 2 Then SOL.SubCode02 When 3 Then SOL.SubCode03 When 4 Then SOL.SubCode04 When 5 Then SOL.SubCode05" \
          " When 6 Then SOL.SubCode06 When 7 Then SOL.SubCode07 When 8 Then SOL.SubCode08 When 9 Then SOL.SubCode09 When 10 Then SOL.SubCode10 End = UGG.Code" \
          " where SOL.PROGRESSSTATUS in(0,1)" \
          " and SO.DOCUMENTTYPETYPE in ('00','02','03')" \
          " and Product.LongDescription='"+LSItem+"'"+ItemType+"" \
          " group by SO.CODE,SO.ORDERDATE" \
          " , BusinessPartner.LegalName1,UGG.LongDescription,Product.LongDescription,UGG.Code,QualityLevel.ShortDescription," \
          " Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOL.UserPrimaryQuantity Else 0 End," \
          " Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End" \
          " , Case When SO.DOCUMENTTYPETYPE = '03' Then SOL.UserPrimaryQuantity Else 0 End" \
          " , Case When SO.DOCUMENTTYPETYPE = '03' Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End" \
          " , Agent.LongDescription,SO.DOCUMENTTYPETYPE,SO.EXTERNALREFERENCE"
      stmt = con.db.prepare(con.conn, sql)
      con.db.execute(stmt)
      result = con.db.fetch_both(stmt)
      print(result)
      while result != False:
            GDataItemSubDetail.append(result)
            result = con.db.fetch_both(stmt)
      return render(request, 'ContractPending_AgentWise.html',
                    {'GDataItemSubDetail':GDataItemSubDetail,'GDataItemGroup': GDataItemGroup, 'GDataItemDetail': GDataItemDetail,
                     'GDataItemType': GDataItemType,
                     'sumcontractqty': round(sumcontractqty, 2), 'sumdespnotgn': round(sumdespnotgn, 2)
                          , 'sumgoodnotgn': round(sumgoodnotgn, 2), 'sumtotal': round(sumtotal, 2)
                          , 'detcontractqty': round(detcontractqty, 2), 'detdespnotgn': round(detdespnotgn, 2)
                          , 'detgoodnotgn': round(detgoodnotgn, 2), 'dettotal': round(dettotal, 2),'item':item,'itemgroup':LSItemCode,"ItemType":Item})


def ContractPending_ApplyType(request):
    global GDataItemGroup
    global GDataItemType
    global sumdespnotgn
    global sumgoodnotgn
    global sumcontractqty
    global sumtotal
    global ItemType
    global Item
    sumcontractqty = 0
    sumdespnotgn = 0
    sumgoodnotgn = 0
    sumtotal = 0
    GDataItemGroup = []
    Item=[]
    item=request.GET.getlist('itemtype')
    ItemType = ""
    itemtype = ""
    if request.GET.getlist('itemtype'):
        itemtype = request.GET.getlist('itemtype')
        ItemType = " and SOL.ITEMTYPEAFICODE in" + "(" + str(request.GET.getlist('itemtype'))[1:-1] + ")"
    else:
        ItemType = ""

    sql = "Select " \
          "Agent.Longdescription as Agent" \
          ", sum(cast(Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End as decimal(18,2)))  As PendContractQty " \
          ", sum(cast(Case When SO.DOCUMENTTYPETYPE = '03' Then SOL.UserPrimaryQuantity Else 0 End as decimal(18,2)))  As DespOrderQty" \
          ", sum(cast(Case When SO.DOCUMENTTYPETYPE = '03' Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End as decimal(18,2)))  As PendDespOrderQty " \
          ", sum(cast(Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOL.UserPrimaryQuantity Else 0 End as decimal(18,2)))  As ContractQty " \
          " from SalesOrder SO" \
          " Join Division           On      SO.DIVISIONCODE = Division.Code" \
          " Join Agent              on      SO.Agent1Code = Agent.code" \
          " join OrderPartner       On      SO.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode" \
          " And     OrderPartner.CustomerSupplierType = 1" \
          " join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId=BusinessPartner.NumberID" \
          " JOIN SalesOrderLine SOL      ON         SO.CODE                 = SOL.SalesOrderCODE" \
          " AND        SO.COUNTERCODE          = SOL.SalesOrderCOUNTERCODE" \
          " And        SO.DocumentTypeType     = SOL.DocumentTypeType" \
          " JOIN FullItemKeyDecoder FIKD ON      SOL.ITEMTYPEAFICODE    = FIKD.ITEMTYPECODE" \
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
          " Join Product                On      SOL.ITEMTYPEAFICODE           = Product.ITEMTYPECODE" \
          " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
          " Join QualityLevel           On      SOL.QualityCode               = QualityLevel.Code" \
          " And     SOL.ITEMTYPEAFICODE           = QualityLevel.ItemTypeCode" \
          " Join SalesOrderDelivery SOD  On     SOL.SalesOrderCODE            = SOD.SalesOrderLineSalesOrderCODE" \
          " AND    SOL.SalesOrderCOUNTERCODE     = SOD.SalOrdLineSalOrderCOUNTERCODE" \
          " AND    SOL.OrderLine               = SOD.SalesOrderLineOrderLine" \
          " Left JOIN ItemSubcodeTemplate IST ON     SOL.ITEMTYPEAFICODE = IST.ItemTypeCode" \
          " AND     IST.GroupTypeCode In ('MB4','P09','B07')" \
          " Left JOIN UserGenericGroup UGG ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
          " AND     Case IST.Position When 1 Then SOL.SubCode01 When 2 Then SOL.SubCode02 When 3 Then SOL.SubCode03 When 4 Then SOL.SubCode04 When 5 Then SOL.SubCode05" \
          " When 6 Then SOL.SubCode06 When 7 Then SOL.SubCode07 When 8 Then SOL.SubCode08 When 9 Then SOL.SubCode09 When 10 Then SOL.SubCode10 End = UGG.Code" \
          " where SOL.PROGRESSSTATUS in(0,1)" \
          " and SO.DOCUMENTTYPETYPE in ('00','02','03')" + ItemType + "" \
          " group by Agent.Longdescription" \
          " order by Agent"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        result['TOTAL'] = float(result['PENDCONTRACTQTY']) + float(result['DESPORDERQTY'])
        sumcontractqty = sumcontractqty + float(result['CONTRACTQTY'])
        sumdespnotgn = sumdespnotgn + float(result['PENDCONTRACTQTY'])
        sumgoodnotgn = sumgoodnotgn + float(result['DESPORDERQTY'])
        sumtotal = sumtotal + float(result['TOTAL'])
        GDataItemGroup.append(result)
        result = con.db.fetch_both(stmt)
    return render(request, 'ContractPending_AgentWise.html', {'GDataItemGroup': GDataItemGroup, 'GDataItemType': GDataItemType,
                                                    'sumcontractqty': round(sumcontractqty, 2),
                                                    'sumdespnotgn': round(sumdespnotgn, 2)
        , 'sumgoodnotgn': round(sumgoodnotgn, 2), 'sumtotal': round(sumtotal, 2),"ItemType":item})
#
# def ContractPending_AgentWise(request):
#     global GDataItemGroup
#     global GDataItemType
#     global sumdespnotgn
#     global sumgoodnotgn
#     global sumcontractqty
#     global sumtotal
#     global item
#     global LSItemCode
#     sumcontractqty = 0
#     sumdespnotgn = 0
#     sumgoodnotgn = 0
#     sumtotal = 0
#     GDataItemGroup = []
#     GDataItemType = []
#     sql = "Select " \
#           "Product.ITEMTYPECODE as ItemType" \
#           ", sum(cast(Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End as decimal(18,2)))  As PendContractQty " \
#           ", sum(cast(Case When SO.DOCUMENTTYPETYPE = '03' Then SOL.UserPrimaryQuantity Else 0 End as decimal(18,2)))  As DespOrderQty" \
#           ", sum(cast(Case When SO.DOCUMENTTYPETYPE = '03' Then SOD.UserPrimaryQuantity - SOD.UsedUserPrimaryQuantity Else 0 End as decimal(18,2)))  As PendDespOrderQty " \
#           ", sum(cast(Case When SO.DOCUMENTTYPETYPE In ('00','02') Then SOL.UserPrimaryQuantity Else 0 End as decimal(18,2)))  As ContractQty " \
#           " from SalesOrder SO" \
#           " Join Division           On      SO.DIVISIONCODE = Division.Code" \
#           " Join Agent              on      SO.Agent1Code = Agent.code" \
#           " join OrderPartner       On      SO.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode" \
#           " And     OrderPartner.CustomerSupplierType = 1" \
#           " join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId=BusinessPartner.NumberID" \
#           " JOIN SalesOrderLine SOL      ON         SO.CODE                 = SOL.SalesOrderCODE" \
#           " AND        SO.COUNTERCODE          = SOL.SalesOrderCOUNTERCODE" \
#           " And        SO.DocumentTypeType     = SOL.DocumentTypeType" \
#           " JOIN FullItemKeyDecoder FIKD ON      SOL.ITEMTYPEAFICODE    = FIKD.ITEMTYPECODE" \
#           " AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
#           " AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')" \
#           " AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
#           " AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')" \
#           " AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')" \
#           " AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')" \
#           " AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')" \
#           " AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')" \
#           " AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')" \
#           " AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')" \
#           " Join Product                On      SOL.ITEMTYPEAFICODE           = Product.ITEMTYPECODE" \
#           " And     FIKD.ItemUniqueId             = Product.AbsUniqueId" \
#           " Join QualityLevel           On      SOL.QualityCode               = QualityLevel.Code" \
#           " And     SOL.ITEMTYPEAFICODE           = QualityLevel.ItemTypeCode" \
#           " Join SalesOrderDelivery SOD  On     SOL.SalesOrderCODE            = SOD.SalesOrderLineSalesOrderCODE" \
#           " AND    SOL.SalesOrderCOUNTERCODE     = SOD.SalOrdLineSalOrderCOUNTERCODE" \
#           " AND    SOL.OrderLine               = SOD.SalesOrderLineOrderLine" \
#           " Left JOIN ItemSubcodeTemplate IST ON     SOL.ITEMTYPEAFICODE = IST.ItemTypeCode" \
#           " AND     IST.GroupTypeCode In ('MB4','P09','B07')" \
#           " Left JOIN UserGenericGroup UGG ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode" \
#           " AND     Case IST.Position When 1 Then SOL.SubCode01 When 2 Then SOL.SubCode02 When 3 Then SOL.SubCode03 When 4 Then SOL.SubCode04 When 5 Then SOL.SubCode05" \
#           " When 6 Then SOL.SubCode06 When 7 Then SOL.SubCode07 When 8 Then SOL.SubCode08 When 9 Then SOL.SubCode09 When 10 Then SOL.SubCode10 End = UGG.Code" \
#           " where SOL.PROGRESSSTATUS in(0,1)" \
#           " and SO.DOCUMENTTYPETYPE in ('00','02','03')" \
#           " group by Product.ITEMTYPECODE" \
#           " order by ItemType"
#
#     stmt = con.db.prepare(con.conn, sql)
#     con.db.execute(stmt)
#     result = con.db.fetch_both(stmt)
#     while result != False:
#         if result['ITEMTYPE'] not in GDataItemType:
#             GDataItemType.append(result['ITEMTYPE'])
#         result['TOTAL'] = float(result['PENDCONTRACTQTY']) + float(result['DESPORDERQTY'])
#         sumcontractqty = sumcontractqty + float(result['CONTRACTQTY'])
#         sumdespnotgn = sumdespnotgn + float(result['PENDCONTRACTQTY'])
#         sumgoodnotgn = sumgoodnotgn + float(result['DESPORDERQTY'])
#         sumtotal = sumtotal + float(result['TOTAL'])
#         GDataItemGroup.append(result)
#         result = con.db.fetch_both(stmt)
#     return render(request, 'ContractPending.html', {'GDataItemGroup': GDataItemGroup, 'GDataItemType': GDataItemType,
#                                                     'sumcontractqty': round(sumcontractqty, 2),
#                                                     'sumdespnotgn': round(sumdespnotgn, 2)
#         , 'sumgoodnotgn': round(sumgoodnotgn, 2), 'sumtotal': round(sumtotal, 2)})