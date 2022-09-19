import os
import pandas as pd
from django.views.static import serve

from ProcessSelection import BrokerWiseRD_ProcessSelection as BWRD
from Global_Files import Connection_String as con
from CreateXLS import BrokerWiseRDEXL_CreateXLS  as xlsrpt
from datetime import datetime
import ctypes

counter = 0
LSFileName=''

def BrokerWiseRDEXL_CreateXLS(LSCompanyCode, LCCompanyCode, LMCompanyCode, LSBranch, LCBranch, LSBrokerGroup, LCBrokerGroup,
                                      LSBroker, LCBroker, LSParty, LCParty, LSYarntype, LCYarntype, LDStartDate, LDEndDate, request):
    xlsrpt.filename()
    LSName = datetime.now()
    LSstring = str(LSName)
    global LSFileName, counter
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "Broker Wise RD " + LSFileName + ".xlsx"

    Branch = str(LSCompanyCode)
    Branches = '(' + Branch[1:-1] + ')'

    BrokerGrp = str(LSBrokerGroup)
    BrokerGrps = '(' + BrokerGrp[1:-1] + ')'

    Broker = str(LSBroker)
    Brokers = '(' + Broker[1:-1] + ')'

    Party = str(LSParty)
    Parties = '(' + Party[1:-1] + ')'

    Yarntype = str(LSYarntype)
    Yarntypes = '(' + Yarntype[1:-1] + ')'

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"

    if not LCCompanyCode and not LSCompanyCode:
        LSBranches = " "
    elif LCCompanyCode:
        LSBranches = " "
    elif LSCompanyCode:
        LSBranches = "AND BU.Code in " + str(Branches)

    if not LSBrokerGroup and not LCBrokerGroup:
        LSBrokerGroups = " "
    elif LCBrokerGroup:
        LSBrokerGroups = " "
    elif LSBrokerGroup:
        LSBrokerGroups = "AND AgGrp.Code in " + str(BrokerGrps)

    if not LSBroker and not LCBroker:
        LSBrokers = " "
    elif LCBroker:
        LSBrokers = " "
    elif LSBroker:
        LSBrokers = "AND AGENT.CODE in " + str(Brokers)

    if not LSParty and not LCParty:
        LSParties = " "
    elif LCParty:
        LSParties = " "
    elif LSParty:
        LSParties = "AND BP.NUMBERID in " + str(Parties)

    if not LSYarntype and not LCYarntype:
        LSYarntypes = " "
    elif LCYarntype:
        LSYarntypes = " "
    elif LSYarntype:
        LSYarntypes = "AND PIL.ITEMTYPECODE in " + str(Yarntypes)


    sql = "Select          Company.LONGDESCRIPTION As Company " \
          ", BP.LEGALNAME1 As Party " \
          ", AgGrp.LONGDESCRIPTION As Brokergrp " \
          ", PI.CODE As InvoiceNo " \
          ", PI.INVOICEDATE As IssueDt " \
          ", Cast(COALESCE(Freight.Value,0) As Int) AS Freight " \
          ", Cast(GST.CALCULATEDVALUE As Decimal(20,2)) As Gst " \
          ", Cast(COALESCE(Ins.Value,0) As Int) As Insur " \
          ", Cast(PIL.PRIMARYQTY As Decimal(20,2)) As Qty " \
          ", Cast(BaseRate.CALCULATEDVALUE As Decimal(20, 2)) As BaseRt " \
          ", Cast(BaseRate.CALCULATEDVALUE * PIL.PRIMARYQTY As Decimal(20, 2)) As BaseAmt " \
          ", Cast(InvRate.CALCULATEDVALUE As Decimal(20, 2)) As InvRt " \
          ", Cast(PIL.PRICE As Decimal(20, 2)) AS invRate " \
          ", Cast(DharaRate.VALUE As Decimal(20, 2)) As DhRt " \
          ", Cast(DharaAmt.CALCULATEDVALUE As Decimal(20, 2)) As DhAmt " \
          ", 0 As DhPaid " \
          ", 0 As DisAll " \
          ", PIL.ITEMTYPECODE As YarnType " \
          ", Cast(IntialCom.Value As Int) As intialComPer " \
          ", Cast(BalanceCom.Value As Int) As BalanceComPer " \
          "From    PLANTINVOICE AS PI " \
          "JOIN    BUSINESSUNITVSCOMPANY BC        ON      PI.FACTORYCODE = BC.FACTORYCODE " \
          "JOIN    FinBusinessUnit BU              ON      BC.BUSINESSUNITCODE = BU.Code " \
          "And     BU.GROUPFLAG = 0 " \
          "JOIN    FinBusinessUnit Company         ON      BU.GroupbuCode = Company.Code " \
          "And     Company.GROUPFLAG = 1 " \
          "JOIN    Agent                           ON      PI.AGENT1CODE = Agent.CODE " \
          "JOIN    AgentsGroupDetail AGD           ON      PI.Agent1Code = AGD.AgentCode " \
          "JOIN    AgentsGroup AgGrp               ON      AGD.AgentsGroupCode = AgGrp.Code " \
          "Join    SALESDOCUMENT SD                ON      PI.SALESINVOICEPROVISIONALCODE = SD.PROVISIONALCODE " \
          "And     SD.DocumentTypeType = '06'  " \
          "AND     PI.SALINVOICEPRVCOUNTERCODE = SD.PROVISIONALCOUNTERCODE " \
          "JOIN     OrderPartner As OP             ON      SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode " \
          "AND     OP.CustomerSupplierType = 1 " \
          "JOIN    BusinessPartner BP              ON      OP.OrderBusinessPartnerNumberId = BP.NumberId " \
          "Join    PLANTINVOICELINE PIL            ON      PI.CODE = PIL.PLANTINVOICECODE " \
          "Left Join    INDTAXDETAIL Freight       ON      PIL.ABSUNIQUEID = Freight.ABSUNIQUEID " \
          "And     Freight.ITAXCODE = 'FRT' " \
          "And     Freight.TAXCATEGORYCODE = 'GFR' " \
          "Join    INDTAXDETAIL GST                ON      PIL.ABSUNIQUEID = GST.ABSUNIQUEID " \
          "And     GST.TAXCATEGORYCODE = 'GST' " \
          "Left Join    INDTAXDETAIL Ins           ON      PIL.ABSUNIQUEID = Ins.ABSUNIQUEID " \
          "And     Ins.TAXCATEGORYCODE = 'INS' " \
          "Join    INDTAXDETAIL BaseRate           ON      PIL.ABSUNIQUEID = BaseRate.ABSUNIQUEID " \
          "And     BaseRate.ITAXCODE = 'BSR' " \
          "And     BaseRate.TAXCATEGORYCODE = 'OTH' " \
          "Join    INDTAXDETAIL InvRate            ON      PIL.ABSUNIQUEID = InvRate.ABSUNIQUEID " \
          "And     InvRate.ITAXCODE = 'INR' " \
          "And     InvRate.TAXCATEGORYCODE = 'OTH' " \
          "Join    INDTAXDETAIL DharaRate          ON      PIL.ABSUNIQUEID = DharaRate.ABSUNIQUEID " \
          "And     DharaRate.ITAXCODE = 'DRD' " \
          "And     DharaRate.Value > 0 " \
          "And     DharaRate.TAXCATEGORYCODE = 'OTH' " \
          "Join    INDTAXDETAIL DharaAmt           ON      PIL.ABSUNIQUEID = DharaAmt.ABSUNIQUEID " \
          "And     DharaAmt.ITAXCODE = 'DRA' " \
          "And     DharaAmt.TAXCATEGORYCODE = 'OTH' " \
          "Join    INDTAXDETAIL IntialCom          ON      PIL.ABSUNIQUEID = IntialCom.ABSUNIQUEID " \
          "And     IntialCom.ITAXCODE = 'AG1' " \
          "And     IntialCom.TAXCATEGORYCODE = 'OTH' " \
          "Join    INDTAXDETAIL BalanceCom         ON      PIL.ABSUNIQUEID = BalanceCom.ABSUNIQUEID " \
          "And     BalanceCom.ITAXCODE = 'BS1' " \
          "And     BalanceCom.TAXCATEGORYCODE = 'OTH' " \
          "Where   PI.INVOICEDATE Between "+startdate+" AND "+enddate+" " \
          ""+LSBranches+" "+LSBrokerGroups+" "+LSBrokers+" "+LSParties+" "+LSYarntypes+" " \
          "Order By Company, Brokergrp, Party, InvoiceNo "
          # "Order BY      Party, ItmTyp, Item, Broker, OrdNo, ORDDT DESC, ContNo, ORDDT DESC "

    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    # xlsrpt.xmlheader()

    while result != False:
        counter = counter + 1

        xlsrpt.textsize( result,  stdt, etdt)
        result = con.db.fetch_both(stmt)

    if result == False:
        if counter > 0:
            xlsrpt.row = xlsrpt.row + 1
            xlsrpt.BrokerTotalPrint(xlsrpt.row)

            BWRD.Exceptions = ""
        elif counter == 0:
            BWRD.Exceptions = "Note: No Result found according to your selected criteria"
            return BWRD.Exception(request)

    xlsrpt.workbook.close()
    xlsrpt.newrequest()
    counter = 0