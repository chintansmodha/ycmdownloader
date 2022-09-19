import os
from datetime import datetime
from PrintPDF import ContractProgressShade_PrintPDF as pdfCP
from Global_Files import Connection_String as con
from ProcessSelection import ContractProgress_ProcessSelection as CPPS

counter = 0

def ContractProgress_PrintPDF(LSBroker, LCBroker, LSYarn, LCYarn, LSItem, LCItem, LSShade, LCShade, LSParty, LCParty, LDStartDate,LDEndDate):


    Broker = str(LSBroker)
    Brokers = '(' + Broker[1:-1] + ')'

    Yarn = str(LSYarn)
    Yarns = '(' + Yarn[1:-1] + ')'

    Item = str(LSItem)
    Items = '(' + Item[1:-1] + ')'

    Shade = str(LSShade)
    Shades = '(' + Shade[1:-1] + ')'

    Party = str(LSParty)
    Parties = '(' + Party[1:-1] + ')'

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"

    if not LSBroker and not LCBroker:
        LSBrokers = " "
    elif LCBroker:
        LSBrokers = " "
    elif LSBroker:
        LSBrokers = "AND AGENT.CODE in " + str(Brokers)

    if not LSYarn and not LCYarn:
        LSYarns = " "
    elif LCYarn:
        LSYarns = " "
    elif LSYarn:
        LSYarns = "AND ContSol.ITEMTYPEAFICODE in " + str(Yarns)

    if not LSItem and not LCItem:
        LSItems = " "
    elif LCItem:
        LSItems = " "
    elif LSItem:
        LSItems = "AND FIKD.ItemUniqueId in " + str(Items)

    if not LSShade and not LCShade:
        LSShades = " "
    elif LCShade:
        LSShades = " "
    elif LSShade:
        LSShades = "AND UGG.Code in " + str(Shades)

    if not LSParty and not LCParty:
        LSParties = " "
    elif LCParty:
        LSParties = " "
    elif LSParty:
        LSParties = "AND BP.NUMBERID in " + str(Parties)


    sql = "Select   PLANT.LONGDESCRIPTION As Company " \
          ", COALESCE(AGENT.LONGDESCRIPTION,'Agent Not Entered') As Broker " \
          ", ContOrder.CODE As ContNo " \
          ", ContOrder.ORDERDATE As ContDt " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QUALITYLEVEL.LONGDESCRIPTION,'') As Item " \
          ", COALESCE(UGG.LONGDESCRIPTION,'') As Shade " \
          ", Cast(ContSOL.USERPRIMARYQUANTITY-ContSOL.CANCELLEDUSERPRIMARYQUANTITY AS DEcimal(20,3)) As ContQty " \
          ", Cast(ContSOL.USERPRIMARYQUANTITY-ContSOL.CANCELLEDUSERPRIMARYQUANTITY-ContSOD.USEDUSERPRIMARYQUANTITY  AS DEcimal(20,3)) As ContPendQty " \
          ", COALESCE(Cast(ContRate.CalculatedValuerCC AS DEcimal(20,2)),0) As ContractRate       " \
          ", Case ContSOL.PROGRESSSTATUS When 0 Then 'Entered' When 1 Then 'ParUsed' when 2 Then 'Closed' End As ContStatus " \
          ", DespOrder.CODE As OrdNo " \
          ", DespOrder.ORDERDATE As OrdDt " \
          ", Case DespOrdSOL.PROGRESSSTATUS When 0 Then 'Entered' When 1 Then 'ParUsed' when 2 Then 'Closed' End As OrdStatus " \
          ", Cast(DespOrdSOL.USERPRIMARYQUANTITY-DespOrdSOL.CANCELLEDUSERPRIMARYQUANTITY AS DEcimal(20,3)) As OrdQty " \
          ", Cast(DespOrdSOL.USERPRIMARYQUANTITY-DespOrdSOL.CANCELLEDUSERPRIMARYQUANTITY-DespOrdSOD.USEDUSERPRIMARYQUANTITY  AS DEcimal(20,3)) As OrdPndQty " \
          ", ChallanSD.PROVISIONALCODE As ChalNo " \
          ", ChallanSD.PROVISIONALDOCUMENTDATE As ChalDt " \
          ", '' As ChalLot " \
          ", Cast(SDL.USERPRIMARYQUANTITY AS DEcimal(20,3)) As ChalQty " \
          "From                            SALESORDER ForCast " \
          "Join SALESORDER     ContOrder              On      Forcast.Code = ContOrder.PreviousCode " \
          "AND     Forcast.COUNTERCode = ContOrder.PreviousCOUNTERCODE " \
          "AND     ContOrder.DOCUMENTTYPETYPE = '02' " \
          "join ORDERPARTNER  ContOP                   On      ContOrder.ORDPRNCUSTOMERSUPPLIERCODE = ContOP.CUSTOMERSUPPLIERCODE " \
          "And     ContOP.CUSTOMERSUPPLIERTYPE = 1 " \
          "Join BUSINESSPARTNER  BP                On      ContOP.ORDERBUSINESSPARTNERNUMBERID = BP.NUMBERID " \
          "Left Join AGENT                   On      ContOrder.AGENT1CODE = AGENT.CODE " \
          "Join SALESORDERLINE ContSOL                 On      ContOrder.CODE = ContSOL.SALESORDERCODE " \
          "And     ContOrder.COUNTERCODE = ContSOL.SALESORDERCOUNTERCODE  " \
          "And     ContOrder.DOCUMENTTYPETYPE = ContSOL.DOCUMENTTYPETYPE " \
          "Join LOGICALWAREHOUSE                      On      ContSOL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Join PLANT                                 On      LOGICALWAREHOUSE.PLANTCODE = PLANT.CODE  " \
          "Join SALESORDERDELIVERY ContSOD    On      ContSOL.SALESORDERCODE= ContSOD.SALESORDERLINESALESORDERCODE " \
          "And     ContSOL.SALESORDERCOUNTERCODE = ContSOD.SALORDLINESALORDERCOUNTERCODE " \
          "And     ContSOL.OrderLine = ContSOD.SalesOrderLineOrderLine " \
          "join FULLITEMKEYDECODER FIKD            ON      ContSOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(ContSOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(ContSOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(ContSOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(ContSOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(ContSOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(ContSOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(ContSOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(ContSOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(ContSOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(ContSOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join PRODUCT                            On      ContSOL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left JOIN IndTaxDETAIL ContRate              ON      ContSOL.AbsUniqueId = ContRate.ABSUNIQUEID " \
          "AND     ContRate.ITaxCode = 'INR' " \
          "Left JOIN ItemSubcodeTemplate IST    ON      ContSOL.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN USERGENERICGROUP UGG       On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode  " \
          "AND     Case IST.Position When 1 Then ContSOL.SUBCODE01 When 2 Then ContSOL.SUBCODE02 When 3 Then ContSOL.SUBCODE03 When 4 Then ContSOL.SUBCODE04 When 5 Then ContSOL.SUBCODE05  " \
          "When 6 Then ContSOL.SUBCODE06 When 7 Then ContSOL.SUBCODE07 When 8 Then ContSOL.SUBCODE08 When 9 Then ContSOL.SUBCODE09 When 10 Then ContSOL.SUBCODE10 End = UGG.Code " \
          "JOIN QUALITYLEVEL                       ON      ContSOL.QUALITYCODE = QUALITYLEVEL.CODE " \
          "AND     ContSOL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
          "left Join SALESORDERLINE DespOrdSOL          On      ContOrder.CODE = DespOrdSOL.PreviousCODE " \
          "And     ContOrder.COUNTERCODE = DespOrdSOL.PreviousCOUNTERCODE   " \
          "And     DespOrdSOL.DOCUMENTTYPETYPE ='03' " \
          "And     ContSOL.OrderLine = DespOrdSOL.PREVIOUSORDERLINE " \
          "Left Join SALESORDER DespOrder          On      DespOrdSOL.SalesOrderCODE = DespOrder.CODE " \
          "AND     DespOrdSOL.SalesOrderCOUNTERCODE = DespOrder.COUNTERCODE " \
          "And     DespOrdSOL.DOCUMENTTYPETYPE = DespOrder.DOCUMENTTYPETYPE " \
          "Left Join SALESORDERDELIVERY DespOrdSOD On      DespOrdSOL.SalesOrderCODE = DespOrdSOD.SALESORDERLINESALESORDERCODE " \
          "And     DespOrdSOL.SalesOrderCOUNTERCODE = DespOrdSOD.SALORDLINESALORDERCOUNTERCODE " \
          "And     DespOrdSOL.OrderLine = DespOrdSOD.SalesOrderLineOrderLine " \
          "Left Join SALESDOCUMENTLINE SDL         ON      DespOrdSod.SALESORDERLINESALESORDERCODE = SDL.DLVSALORDERLINESALESORDERCODE " \
          "And     DespOrdSod.SALORDLINESALORDERCOUNTERCODE = SDL.DLVSALORDLINESALORDCNTCODE " \
          "And     SDL.DOCUMENTTYPETYPE = '05' " \
          "AND     DespOrdSod.SALESORDERLINEOrderLine = SDL.DLVSALESORDERLINEORDERLINE " \
          "Left Join SALESDOCUMENT ChallanSD       On      SDL.SALESDOCUMENTPROVISIONALCODE = ChallanSD.PROVISIONALCODE " \
          "And     SDL.SALDOCPROVISIONALCOUNTERCODE = ChallanSD.PROVISIONALCOUNTERCODE " \
          "And     SDL.DOCUMENTTYPETYPE = ChallanSD.DOCUMENTTYPETYPE  " \
          "Where           ContOrder.ORDERDATE     Between         "+startdate+"    And     "+enddate+" " \
          "And             Forcast.DOCUMENTTYPETYPE In ('00') " \
          "And             ForCast.PreviousCode is null "+LSBrokers+" "+LSYarns+" "+LSItems+" "+LSShades+" "+LSParties+" " \
          "union Select                          PLANT.LONGDESCRIPTION As Company " \
          ", COALESCE(AGENT.LONGDESCRIPTION,'Agent Not Entered') As Broker " \
          ", ContOrder.CODE As ContNo " \
          ", ContOrder.ORDERDATE As ContDt " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QUALITYLEVEL.LONGDESCRIPTION,'') As Item " \
          ", COALESCE(UGG.LONGDESCRIPTION,'') As Shade " \
          ", Cast(ContSOL.USERPRIMARYQUANTITY-ContSOL.CANCELLEDUSERPRIMARYQUANTITY AS DEcimal(20,3)) As ContQty " \
          ", Cast(ContSOL.USERPRIMARYQUANTITY-ContSOL.CANCELLEDUSERPRIMARYQUANTITY-ContSOD.USEDUSERPRIMARYQUANTITY  AS DEcimal(20,3)) As ContPendQty " \
          ", COALESCE(Cast(ContRate.CalculatedValuerCC AS DEcimal(20,2)),0) As ContractRate " \
          ", Case ContSOL.PROGRESSSTATUS When 0 Then 'Entered' When 1 Then 'ParUsed' when 2 Then 'Closed' End As ContStatus " \
          ", DespOrder.CODE As OrdNo " \
          ", DespOrder.ORDERDATE As OrdDt " \
          ", Case DespOrdSOL.PROGRESSSTATUS When 0 Then 'Entered' When 1 Then 'ParUsed' when 2 Then 'Closed' End As OrdStatus " \
          ", Cast(DespOrdSOL.USERPRIMARYQUANTITY-DespOrdSOL.CANCELLEDUSERPRIMARYQUANTITY AS DEcimal(20,3)) As OrdQty " \
          ", Cast(DespOrdSOL.USERPRIMARYQUANTITY-DespOrdSOL.CANCELLEDUSERPRIMARYQUANTITY-DespOrdSOD.USEDUSERPRIMARYQUANTITY  AS DEcimal(20,3)) As OrdPndQty " \
          ", ChallanSD.PROVISIONALCODE As ChalNo " \
          ", ChallanSD.PROVISIONALDOCUMENTDATE As ChalDt " \
          ", '' As ChalLot  " \
          ", Cast(SDL.USERPRIMARYQUANTITY AS DEcimal(20,3)) As ChalQty " \
          "From                            SALESORDER ContOrder " \
          "join ORDERPARTNER  ContOP                   On      ContOrder.ORDPRNCUSTOMERSUPPLIERCODE = ContOP.CUSTOMERSUPPLIERCODE " \
          "And     ContOP.CUSTOMERSUPPLIERTYPE = 1 " \
          "Join BUSINESSPARTNER  BP                On      ContOP.ORDERBUSINESSPARTNERNUMBERID = BP.NUMBERID " \
          "Left Join AGENT                         On      ContOrder.AGENT1CODE = AGENT.CODE " \
          "Join SALESORDERLINE ContSOL                 On      ContOrder.CODE = ContSOL.SALESORDERCODE " \
          "And     ContOrder.COUNTERCODE = ContSOL.SALESORDERCOUNTERCODE " \
          "And     ContOrder.DOCUMENTTYPETYPE = ContSOL.DOCUMENTTYPETYPE " \
          "Join LOGICALWAREHOUSE                      On      ContSOL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Join PLANT                                 On      LOGICALWAREHOUSE.PLANTCODE = PLANT.CODE  " \
          "Left Join SALESORDERDELIVERY ContSOD    On      ContSOL.SALESORDERCODE= ContSOD.SALESORDERLINESALESORDERCODE " \
          "And     ContSOL.SALESORDERCOUNTERCODE = ContSOD.SALORDLINESALORDERCOUNTERCODE " \
          "And     ContSOL.OrderLine = ContSOD.SalesOrderLineOrderLine " \
          "join FULLITEMKEYDECODER FIKD            ON      ContSOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(ContSOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(ContSOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(ContSOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(ContSOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(ContSOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(ContSOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(ContSOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(ContSOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(ContSOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(ContSOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join PRODUCT                            On      ContSOL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left JOIN IndTaxDETAIL ContRate              ON      ContSOL.AbsUniqueId = ContRate.ABSUNIQUEID " \
          "AND     ContRate.ITaxCode = 'INR' " \
          "Left JOIN ItemSubcodeTemplate IST    ON      ContSOL.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN USERGENERICGROUP UGG       On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then ContSOL.SUBCODE01 When 2 Then ContSOL.SUBCODE02 When 3 Then ContSOL.SUBCODE03 When 4 Then ContSOL.SUBCODE04 When 5 Then ContSOL.SUBCODE05 " \
          "When 6 Then ContSOL.SUBCODE06 When 7 Then ContSOL.SUBCODE07 When 8 Then ContSOL.SUBCODE08 When 9 Then ContSOL.SUBCODE09 When 10 Then ContSOL.SUBCODE10 End = UGG.Code " \
          "JOIN QUALITYLEVEL                       ON      ContSOL.QUALITYCODE = QUALITYLEVEL.CODE " \
          "AND     ContSOL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
          "left Join SALESORDERLINE DespOrdSOL          On      ContOrder.CODE = DespOrdSOL.PreviousCODE " \
          "And     ContOrder.COUNTERCODE = DespOrdSOL.PreviousCOUNTERCODE " \
          "And     DespOrdSOL.DOCUMENTTYPETYPE ='03' " \
          "And     ContSOL.OrderLine = DespOrdSOL.PREVIOUSORDERLINE " \
          "Left Join SALESORDER DespOrder          On      DespOrdSOL.SalesOrderCODE = DespOrder.CODE " \
          "AND     DespOrdSOL.SalesOrderCOUNTERCODE = DespOrder.COUNTERCODE " \
          "And     DespOrdSOL.DOCUMENTTYPETYPE = DespOrder.DOCUMENTTYPETYPE " \
          "Left Join SALESORDERDELIVERY DespOrdSOD On      DespOrdSOL.SalesOrderCODE = DespOrdSOD.SALESORDERLINESALESORDERCODE " \
          "And     DespOrdSOL.SalesOrderCOUNTERCODE = DespOrdSOD.SALORDLINESALORDERCOUNTERCODE " \
          "And     DespOrdSOL.OrderLine = DespOrdSOD.SalesOrderLineOrderLine " \
          "Left Join SALESDOCUMENTLINE SDL         ON      DespOrdSod.SALESORDERLINESALESORDERCODE = SDL.DLVSALORDERLINESALESORDERCODE " \
          "And     DespOrdSod.SALORDLINESALORDERCOUNTERCODE = SDL.DLVSALORDLINESALORDCNTCODE " \
          "And     SDL.DOCUMENTTYPETYPE = '05' " \
          "AND     DespOrdSod.SALESORDERLINEOrderLine = SDL.DLVSALESORDERLINEORDERLINE " \
          "Left Join SALESDOCUMENT ChallanSD       On      SDL.SALESDOCUMENTPROVISIONALCODE = ChallanSD.PROVISIONALCODE " \
          "And     SDL.SALDOCPROVISIONALCOUNTERCODE = ChallanSD.PROVISIONALCOUNTERCODE " \
          "And     SDL.DOCUMENTTYPETYPE = ChallanSD.DOCUMENTTYPETYPE " \
          "AND     DespOrdSod.SalesOrderLineOrderLine = SDL.DLVSALESORDERLINEORDERLINE  " \
          "Where           ContOrder.ORDERDATE     Between         "+startdate+"    And     "+enddate+" " \
          "And             ContOrder.DOCUMENTTYPETYPE In ('02') " \
          "AND             ContOrder.PREVIOUSCODE Is  Null "+LSBrokers+" "+LSYarns+" "+LSItems+" "+LSShades+" "+LSParties+" " \
          "Union Select                          PLANT.LONGDESCRIPTION As Company " \
          ", COALESCE(AGENT.LONGDESCRIPTION,'Agent Not Entered') As Broker " \
          ", null As ContNo " \
          ", null As ContDt " \
          ", PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QUALITYLEVEL.LONGDESCRIPTION,'') As Item " \
          ", COALESCE(UGG.LONGDESCRIPTION,'') As Shade " \
          ", null As ContQty " \
          ", null As ContPendQty " \
          ", null As ContractRate " \
          ", null As ContStatus " \
          ", DespSO.CODE As OrdNo " \
          ", DespSO.ORDERDATE As OrdDt " \
          ", Case ContSol.PROGRESSSTATUS When 0 Then 'Entered' When 1 Then 'ParUsed' when 2 Then 'Closed' End As OrdStatus " \
          ", Cast(ContSol.USERPRIMARYQUANTITY-ContSol.CANCELLEDUSERPRIMARYQUANTITY AS DEcimal(20,3)) As OrdQty " \
          ", Cast(ContSol.USERPRIMARYQUANTITY-ContSol.CANCELLEDUSERPRIMARYQUANTITY-DespSOD.USEDUSERPRIMARYQUANTITY  AS DEcimal(20,3)) As OrdPndQty " \
          ", Challan.PROVISIONALCODE As ChalNo " \
          ", Challan.PROVISIONALDOCUMENTDATE As ChalDt " \
          ", '' As ChalLot " \
          ", Cast(ChallanSDL.USERPRIMARYQUANTITY AS DEcimal(20,3)) As ChalQty  " \
          "From                            SALESORDER DespSo " \
          "join ORDERPARTNER  DespOP               On      DespSo.ORDPRNCUSTOMERSUPPLIERCODE = DespOP.CUSTOMERSUPPLIERCODE " \
          "AND     DespOP.CUSTOMERSUPPLIERTYPE = 1 " \
          "Join BUSINESSPARTNER  BP            On      DespOP.ORDERBUSINESSPARTNERNUMBERID = BP.NUMBERID " \
          "Left Join AGENT                On      DespSo.AGENT1CODE = AGENT.CODE " \
          "Join SALESORDERLINE ContSol             On      DespSo.CODE = ContSol.SALESORDERCODE " \
          "And     DespSo.COUNTERCODE = ContSol.SALESORDERCOUNTERCODE " \
          "And     DespSo.DOCUMENTTYPETYPE = ContSol.DOCUMENTTYPETYPE " \
          "Join LOGICALWAREHOUSE                      On      ContSOL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Join PLANT                                 On      LOGICALWAREHOUSE.PLANTCODE = PLANT.CODE  " \
          "Join SALESORDERDELIVERY DespSoD         On      ContSol.SALESORDERCODE= DespSoD.SALESORDERLINESALESORDERCODE " \
          "And     ContSol.SALESORDERCOUNTERCODE = DespSoD.SALORDLINESALORDERCOUNTERCODE " \
          "And     ContSol.OrderLine = DespSoD.SalesOrderLineOrderLine " \
          "join FULLITEMKEYDECODER FIKD            ON      ContSol.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(ContSol.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(ContSol.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(ContSol.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(ContSol.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(ContSol.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(ContSol.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(ContSol.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(ContSol.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(ContSol.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(ContSol.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join PRODUCT                            On      ContSol.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Left JOIN IndTaxDETAIL ContRate              ON      ContSol.AbsUniqueId = ContRate.ABSUNIQUEID " \
          "AND     ContRate.ITaxCode = 'INR' " \
          "Left JOIN ItemSubcodeTemplate IST       ON      ContSol.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN USERGENERICGROUP UGG      On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then ContSol.SUBCODE01 When 2 Then ContSol.SUBCODE02 When 3 Then ContSol.SUBCODE03 When 4 Then ContSol.SUBCODE04 When 5 Then ContSol.SUBCODE05 " \
          "When 6 Then ContSol.SUBCODE06 When 7 Then ContSol.SUBCODE07 When 8 Then ContSol.SUBCODE08 When 9 Then ContSol.SUBCODE09 When 10 Then ContSol.SUBCODE10 End = UGG.Code " \
          "JOIN QUALITYLEVEL                       ON      ContSol.QUALITYCODE = QUALITYLEVEL.CODE " \
          "AND     ContSol.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
          "Left Join SALESDOCUMENTLINE ChallanSDL         ON      DespSod.SALESORDERLINESALESORDERCODE = ChallanSDL.DLVSALORDERLINESALESORDERCODE " \
          "And     DespSod.SALORDLINESALORDERCOUNTERCODE = ChallanSDL.DLVSALORDLINESALORDCNTCODE " \
          "And     ChallanSDL.DOCUMENTTYPETYPE = '05' " \
          "AND     DespSod.SALESORDERLINEOrderLine = ChallanSDL.DLVSALESORDERLINEORDERLINE " \
          "Left Join SALESDOCUMENT Challan       On      ChallanSDL.SALESDOCUMENTPROVISIONALCODE = Challan.PROVISIONALCODE " \
          "And     ChallanSDL.SALDOCPROVISIONALCOUNTERCODE = Challan.PROVISIONALCOUNTERCODE " \
          "And     ChallanSDL.DOCUMENTTYPETYPE = Challan.DOCUMENTTYPETYPE " \
          "Where   DespSO.ORDERDATE     Between         "+startdate+"    And     "+enddate+" " \
          "AND     DespSO.DOCUMENTTYPETYPE = '03' " \
          "AND     DespSO.PREVIOUSCODE Is  Null "+LSBrokers+" "+LSYarns+" "+LSItems+" "+LSShades+" "+LSParties+" " \
          "Order BY Company, Shade, ContNo, Broker, OrdNo, OrdQty"
          # "Order BY      Party, ItmTyp, Item, Broker, OrdNo, ORDDT DESC, ContNo, ORDDT DESC "

    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfCP.textsize(pdfCP.c, result, pdfCP.d,stdt,etdt)
        pdfCP.d=pdfCP.dvalue()
        result = con.db.fetch_both(stmt)

        # if pdfCP.d<20 :
        #     # pdfCP.d=735
        #     pdfCP.k = pdfCP.k + 1
        #     pdfCP.c.setPageSize(pdfCP.landscape(pdfCP.A3))
        #     pdfCP.c.showPage()
        #     pdfCP.d = pdfCP.dvalues(stdt,etdt,pdfCP.divisioncode)
        #     pdfCP.header(stdt,etdt,pdfCP.divisioncode)
        #     pdfCP.fonts(7)


    if result == False:
        if counter > 0:
            pdfCP.d = pdfCP.dvalues(stdt,etdt,pdfCP.divisioncode)
            pdfCP.d = pdfCP.dvalues(stdt, etdt, pdfCP.divisioncode)
            pdfCP.PrintTotalDespatch(pdfCP.c, result, pdfCP.d, stdt,etdt)

            CPPS.Exceptions = ""
            counter = 0
        elif counter==0:
            CPPS.Exceptions="Note: No Report Form For Given Criteria"
            return


    pdfCP.c.setPageSize(pdfCP.landscape(pdfCP.A3))
    pdfCP.c.showPage()
    pdfCP.c.save()
    pdfCP.newrequest()
    pdfCP.d = pdfCP.newpage()