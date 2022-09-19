import os
from datetime import datetime
from PrintPDF import AgentLiftingItem_PrintPDF as pdfAGL
from Global_Files import Connection_String as con
from ProcessSelection import AgentLiftingDetailsProcessSelection as AGLPS

counter = 0

def AgentLifting_PrintPDF(LSBrokerGrp, LCBrokerGrp, LSBroker, LCBroker, LSPlant, LCPlant, LSParty, LCParty,
                                     LSItem, LCItem, LSYarn, LCYarn, LSQuality, LCQuality, LDStartDate, LDEndDate, LSMergePlant, LSSummary):


    BrokerGrp = str(LSBrokerGrp)
    BrokerGrps = '(' + BrokerGrp[1:-1] + ')'

    Broker = str(LSBroker)
    Brokers = '(' + Broker[1:-1] + ')'

    Plant = str(LSPlant)
    Plants = '(' + Plant[1:-1] + ')'

    Party = str(LSParty)
    Parties = '(' + Party[1:-1] + ')'

    Item = str(LSItem)
    Items = '(' + Item[1:-1] + ')'

    Yarn = str(LSYarn)
    Yarns = '(' + Yarn[1:-1] + ')'

    Quality = str(LSQuality)
    Qualities = '(' + Quality[1:-1] + ')'

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"

    if not LSBrokerGrp and not LCBrokerGrp:
        LSBrokerGrps = " "
    elif LCBrokerGrp:
        LSBrokerGrps = " "
    elif LSBrokerGrp:
        LSBrokerGrps = "AND AgGrp.CODE in " + str(BrokerGrps)

    if not LSBroker and not LCBroker:
        LSBrokers = " "
    elif LCBroker:
        LSBrokers = " "
    elif LSBroker:
        LSBrokers = "AND Agent.CODE in " + str(Brokers)

    if not LSPlant and not LCPlant:
        LSPlants = " "
    elif LCPlant:
        LSPlants = " "
    elif LSPlant:
        LSPlants = "AND PLANT.CODE in " + str(Plants)

    if not LSParty and not LCParty:
        LSParties = " "
    elif LCParty:
        LSParties = " "
    elif LSParty:
        LSParties = "AND BP.NUMBERID in " + str(Parties)

    if not LSItem and not LCItem:
        LSItems = " "
    elif LCItem:
        LSItems = " "
    elif LSItem:
        LSItems = "AND FIKD.ItemUniqueId in " + str(Items)

    if not LSYarn and not LCYarn:
        LSYarns = " "
    elif LCYarn:
        LSYarns = " "
    elif LSYarn:
        LSYarns = "AND PIL.ITEMTYPECODE in " + str(Yarns)

    if not LSQuality and not LCQuality:
        LSQualities = " "
    elif LCQuality:
        LSQualities = " "
    elif LSQuality:
        LSQualities = "AND QUALITYLEVEL.LONGDESCRIPTION in " + str(Qualities)


    sql = "Select          'Beekaylon Group Of Companies' As Company " \
          ", Plant.LONGDESCRIPTION AS Plant " \
          ", BP.LEGALNAME1 As Party " \
          ", Coalesce(Agent.LONGDESCRIPTION, 'Broker Name Not Entered') As Agent " \
          ", Coalesce(AgGrp.LONGDESCRIPTION, 'BrokerGroup Name Not Entered') As Agentgrp " \
          ", PI.CODE As InvNo " \
          ", PI.INVOICEDATE As BillDt " \
          ", Product.LONGDESCRIPTION ||' '|| Coalesce(UGG.LONGDESCRIPTION, '') ||' '|| Coalesce(QUALITYLEVEL.LONGDESCRIPTION,'')  As Item " \
          ", Cast(Coalesce(BaseRate.CALCULATEDVALUERCC, 0) As Decimal(10,2)) As Rate " \
          ", Cast(Pil.PRIMARYQTY As Decimal(20,3)) As Quantity " \
          ", Cast(Coalesce(Amount.Value, Pil.BASICVALUE, 0) As Decimal(20,3)) As Amount " \
          "From PLANTINVOICE PI " \
          "Join PLANT                              On      PI.FACTORYCODE = PLANT.CODE " \
          "join OrderPartner OP                    ON      PI.BUYERIFOTCCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode " \
          "AND     PI.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OP.CustomerSupplierType " \
          "join BusinessPartner BP                 ON      OP.OrderbusinessPartnerNumberId =  BP.NumberID " \
          "Left Join Agent                         On      PI.AGENT1CODE = Agent.CODE " \
          "Left JOIN AgentsGroupDetail AGD         ON      PI.Agent1Code = AGD.AgentCode " \
          "Left JOIN AgentsGroup AgGrp             ON      AGD.AgentsGroupCode = AgGrp.Code " \
          "Join PLANTINVOICELINE PIL               ON      PI.CODE = PIL.PLANTINVOICECODE " \
          "JOIN FullItemKeyDecoder FIKD            ON      PIL.ITEMTYPECODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(PIL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(PIL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(PIL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(PIL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(PIL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(PIL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(PIL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(PIL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(PIL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(PIL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join Product                            ON      PIL.ITEMTYPECODE  = Product.ITEMTYPECODE " \
          "AND     FIKD.ItemUniqueId   = Product.AbsUniqueId " \
          "Left JOIN ItemSubcodeTemplate IST       ON      PIL.ITEMTYPECODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN USERGENERICGROUP UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then PIL.SUBCODE01 When 2 Then PIL.SUBCODE02 When 3 Then PIL.SUBCODE03 When 4 Then PIL.SUBCODE04 When 5 Then PIL.SUBCODE05 " \
          "When 6 Then PIL.SUBCODE06 When 7 Then PIL.SUBCODE07 When 8 Then PIL.SUBCODE08 When 9 Then PIL.SUBCODE09 When 10 Then PIL.SUBCODE10 End = UGG.Code " \
          "JOIN QUALITYLEVEL                       ON      PIL.QUALITYLEVELCODE = QUALITYLEVEL.CODE " \
          "AND     PIL.ITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          "Left Join INDTAXDETAIL BaseRate         ON      PIL.ABSUNIQUEID = BaseRate.ABSUNIQUEID " \
          "And     BaseRate.ITAXCODE = 'INR' " \
          "And     BaseRate.TAXCATEGORYCODE = 'OTH' " \
          "Left Join INDTAXDETAIL Amount           ON      PIL.ABSUNIQUEID = Amount.ABSUNIQUEID " \
          "And     Amount.ITAXCODE = '999' " \
          "And     Amount.TAXCATEGORYCODE = 'OTH' " \
          "Where PI.INVOICEDATE Between "+startdate+" And "+enddate+" " \
          " "+LSBrokerGrps+" "+LSBrokers+" "+LSPlants+" "+LSParties+" "+LSItems+" "+LSYarns+" "+LSQualities+" " \
          "Order BY Agentgrp, Agent, Plant, Item, InvNo, BillDt Desc"

    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfAGL.textsize(pdfAGL.c, result, pdfAGL.d,stdt,etdt, LSMergePlant)
        pdfAGL.d=pdfAGL.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfAGL.d<65 :
            # pdfAGL.d=735
            pdfAGL.k = pdfAGL.k + 1
            pdfAGL.c.setPageSize(pdfAGL.portrait(pdfAGL.A4))
            pdfAGL.c.showPage()
            pdfAGL.dvalueset()
            pdfAGL.header(stdt,etdt,pdfAGL.divisioncode)
            pdfAGL.fonts(7)


    if result == False:
        if counter > 0:

            pdfAGL.boldfonts(7)
            pdfAGL.d = pdfAGL.dvalues(pdfAGL.c, stdt, etdt, pdfAGL.divisioncode)
            pdfAGL.c.drawString(300, pdfAGL.d, "Item Total: ")
            pdfAGL.ItemTotalPrint()
            pdfAGL.d = pdfAGL.dvalues(pdfAGL.c, stdt, etdt, pdfAGL.divisioncode)
            pdfAGL.d = pdfAGL.dvalues(pdfAGL.c, stdt, etdt, pdfAGL.divisioncode)
            if pdfAGL.Plant[-1] != '':
                pdfAGL.c.drawString(300, pdfAGL.d, "Company Total: ")
                pdfAGL.PlantTotalPrint()
                pdfAGL.d = pdfAGL.dvalues(pdfAGL.c, stdt, etdt, pdfAGL.divisioncode)
                pdfAGL.d = pdfAGL.dvalues(pdfAGL.c, stdt, etdt, pdfAGL.divisioncode)
            pdfAGL.c.drawString(300, pdfAGL.d, "Broker Total: ")
            pdfAGL.BrokerTotalPrint()
            pdfAGL.d = pdfAGL.dvalues(pdfAGL.c, stdt, etdt, pdfAGL.divisioncode)
            pdfAGL.d = pdfAGL.dvalues(pdfAGL.c, stdt, etdt, pdfAGL.divisioncode)
            pdfAGL.c.drawString(300, pdfAGL.d, "Broker Group Total: ")
            pdfAGL.BrokerGroupTotalPrint()
            pdfAGL.d = pdfAGL.dvalues(pdfAGL.c, stdt, etdt, pdfAGL.divisioncode)
            pdfAGL.d = pdfAGL.dvalues(pdfAGL.c, stdt, etdt, pdfAGL.divisioncode)
            pdfAGL.c.drawString(300, pdfAGL.d, "Grand Total: ")
            pdfAGL.GrandTotalPrint()
            pdfAGL.boldfonts(7)

            AGLPS.Exceptions = ""
            counter = 0
        elif counter==0:
            AGLPS.Exceptions="Note: No Report Form For Given Criteria"
            return


    pdfAGL.c.setPageSize(pdfAGL.portrait(pdfAGL.A4))
    pdfAGL.c.showPage()
    pdfAGL.c.save()
    pdfAGL.newrequest()
    pdfAGL.d = pdfAGL.newpage()