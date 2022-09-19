import os
import pandas as pd
from django.views.static import serve

from ProcessSelection import Export_Invoice_ProcessSelection as EIV
from Global_Files import Connection_String as con
from PrintPDF import Export_Invoice_PrintPDF as pdfrpt
from CreateXLS import Export_Invoice_Without_Shipping_Billno as xlsrpt
from datetime import datetime
import ctypes

counter = 0
LSFileName=''

def ExportInvoicePrintPDF(LSallParty, LSallCompany, LSParty, LSCompany, LDStartDate,
                                 LDEndDate, LSReportType, LSFileName):
    sqlwhere = ''

    allparty = str(LSallParty)
    if allparty == 'None' and len(LSParty) != 0:
        if sqlwhere != '':
            sqlwhere += ' AND '
        party = str(LSParty)
        LSParty = '(' + party[1:-1] + ')'
        sqlwhere += ' AND PLANT.CODE IN  ' + LSParty

    allcompany = str(LSallCompany)
    if allcompany == 'None' and len(LSCompany) != 0:
        # if sqlwhere != '':
        #     sqlwhere += ' AND '
        company = str(LSCompany)
        LSCompany = '(' + company[1:-1] + ')'

        sqlwhere += ' AND BusinessPartner.NUMBERID IN ' + LSCompany + ''
    if LSReportType=='1':

        sql =""
        sql = " Select  PLANT.LONGDESCRIPTION As Company    " \
            "         , DespOrder.CODE As OrdNo_03 " \
            "        , DespOrder.ORDERDATE As OrdDt_03 " \
            "        , ContBP.LEGALNAME1 As Party " \
            "		 , ContOrder.CODE As ContNo_02 " \
            "        , ContOrder.ORDERDATE As ContDt_02       " \
            "        , Cast(ContSOL.USERPRIMARYQUANTITY-ContSOL.CANCELLEDUSERPRIMARYQUANTITY AS DEcimal(20,3)) As ContQty " \
            "        , Cast(DespOrdSOL.USERPRIMARYQUANTITY-DespOrdSOL.CANCELLEDUSERPRIMARYQUANTITY AS DEcimal(20,3)) As OrdQty " \
            "        , Cast(SDL.USERPRIMARYQUANTITY AS DEcimal(20,3)) As ChalQty " \
            "        , ChallanSDinvoice.PROVISIONALDOCUMENTDATE as invoicedate " \
            "        , ChallanSDinvoice.provisionalcode as invoiceno " \
            "        , ContSOD.CONFIRMEDDELIVERYDATE AS COMMITEMENTDATE " \
            "        , days (ContSOD.CONFIRMEDDELIVERYDATE) - days (DespOrder.ORDERDATE)  AS COMMITEDDAYS " \
            "        , days (ChallanSDinvoice.PROVISIONALDOCUMENTDATE) - days (ContSOD.CONFIRMEDDELIVERYDATE) AS DELAYDAYS " \
            " From  SALESORDER ContOrder " \
            " join ORDERPARTNER  ContOP           On      ContOrder.ORDPRNCUSTOMERSUPPLIERCODE = ContOP.CUSTOMERSUPPLIERCODE " \
            "                                    And     ContOP.CUSTOMERSUPPLIERTYPE = 1 " \
            "Join BUSINESSPARTNER  ContBP        On      ContOP.ORDERBUSINESSPARTNERNUMBERID = ContBP.NUMBERID " \
            "Join AGENT  ContAgent               On      ContOrder.AGENT1CODE = ContAGENT.CODE       " \
            "Join SALESORDERLINE ContSOL         On      ContOrder.CODE = ContSOL.SALESORDERCODE " \
            "									And     ContOrder.COUNTERCODE = ContSOL.SALESORDERCOUNTERCODE  " \
            "									And     ContOrder.DOCUMENTTYPETYPE = ContSOL.DOCUMENTTYPETYPE " \
            "Join LOGICALWAREHOUSE               On      ContSOL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
            "Join PLANT                          On      LOGICALWAREHOUSE.PLANTCODE = PLANT.CODE " \
            "Join SALESORDERDELIVERY ContSOD     On      ContSOL.SALESORDERCODE= ContSOD.SALESORDERLINESALESORDERCODE " \
            "									And     ContSOL.SALESORDERCOUNTERCODE = ContSOD.SALORDLINESALORDERCOUNTERCODE " \
            "									And     ContSOL.OrderLine = ContSOD.SalesOrderLineOrderLine " \
            "Join SALESORDER DespOrder           On      ContOrder.CODE = DespOrder.PreviousCODE   " \
            "                                    AND     ContOrder.COUNTERCODE = DespOrder.PreviousCOUNTERCODE " \
            "                                    And     DespOrder.DOCUMENTTYPETYPE = '03' " \
            "                                    and     DespOrder.code <> 'null' " \
            "Join SALESORDERLINE DespOrdSOL      On      DespOrder.CODE = DespOrdSOL.SalesOrderCODE " \
            "                                    And     DespOrder.COUNTERCODE = DespOrdSOL.SalesOrderCOUNTERCODE  " \
            "                                    And     DespOrder.DOCUMENTTYPETYPE = DespOrdSOL.DOCUMENTTYPETYPE " \
            "                                    And     ContSOL.OrderLine = DespOrdSOL.PREVIOUSORDERLINE " \
            "Join SALESORDERDELIVERY DespOrdSOD  On      DespOrdSOL.SalesOrderCODE = DespOrdSOD.SALESORDERLINESALESORDERCODE " \
            "                                    And     DespOrdSOL.SalesOrderCOUNTERCODE = DespOrdSOD.SALORDLINESALORDERCOUNTERCODE " \
            "                                    And     DespOrdSOL.OrderLine = DespOrdSOD.SalesOrderLineOrderLine " \
            "Join SALESDOCUMENTLINE SDL          ON      DespOrdSod.SALESORDERLINESALESORDERCODE = SDL.DLVSALORDERLINESALESORDERCODE " \
            "                                    And     DespOrdSod.SALORDLINESALORDERCOUNTERCODE = SDL.DLVSALORDLINESALORDCNTCODE " \
            "                                    And     SDL.DOCUMENTTYPETYPE = '05' " \
            "                                    AND     DespOrdSod.SALESORDERLINEOrderLine = SDL.DLVSALESORDERLINEORDERLINE    " \
            "Join SALESDOCUMENT ChallanSD        On      SDL.SALESDOCUMENTPROVISIONALCODE = ChallanSD.PROVISIONALCODE " \
            "                                    And     SDL.SALDOCPROVISIONALCOUNTERCODE = ChallanSD.PROVISIONALCOUNTERCODE " \
            "                                    And     SDL.DOCUMENTTYPETYPE = ChallanSD.DOCUMENTTYPETYPE   " \
            "Join SALESDOCUMENTLINE SDLinvoice   ON      DespOrdSod.SALESORDERLINESALESORDERCODE = SDLinvoice.DLVSALORDERLINESALESORDERCODE " \
            "                                    And     DespOrdSod.SALORDLINESALORDERCOUNTERCODE = SDLinvoice.DLVSALORDLINESALORDCNTCODE " \
            "                                    And     SDLinvoice.DOCUMENTTYPETYPE = '06' " \
            "                                    AND     DespOrdSod.SALESORDERLINEOrderLine = SDL.DLVSALESORDERLINEORDERLINE  " \
            "left Join SALESDOCUMENT ChallanSDinvoice       On      SDLinvoice.SALESDOCUMENTPROVISIONALCODE = ChallanSDinvoice.PROVISIONALCODE " \
            "                                    And     SDLinvoice.SALDOCPROVISIONALCOUNTERCODE = ChallanSDinvoice.PROVISIONALCOUNTERCODE " \
            "                                    And     SDLinvoice.DOCUMENTTYPETYPE = ChallanSDinvoice.DOCUMENTTYPETYPE  " \
            "left JOIN PlantInvoice    pi        ON  ChallanSDinvoice.PROVISIONALCODE = pi.CODE   " \
            "Where           ContOrder.ORDERDATE  " \
            "Between         ?    And     ?  " \
            "And             ContOrder.DOCUMENTTYPETYPE In ('02')   " \
            "AND             ContOrder.PREVIOUSCODE Is Null " \
            "order by PLANT.LONGDESCRIPTION "

    elif LSReportType =='2' or LSReportType =='3' :
        sql=""
        sql="Select  PLANT.LONGDESCRIPTION As COMPANY " \
            "        , DespOrder.CODE As ORDNO_03 " \
            "        , DespOrder.ORDERDATE As ORDDT_03 " \
            "        , PRODUCT.LONGDESCRIPTION ||' '|| COALESCE(QUALITYLEVEL.LONGDESCRIPTION,'') As ITEM " \
            "        , COALESCE(UGG.LONGDESCRIPTION,'') As SHADE " \
            "        , ContBP.LEGALNAME1 As PARTY " \
            "        , ContOrder.CODE As CONTNO_02 " \
            "        , ContOrder.ORDERDATE As CONTDT_02 " \
            "        , Cast(ContSOL.USERPRIMARYQUANTITY-ContSOL.CANCELLEDUSERPRIMARYQUANTITY AS DEcimal(20,3)) As CONTQTY " \
            "        , Cast(DespOrdSOL.USERPRIMARYQUANTITY-DespOrdSOL.CANCELLEDUSERPRIMARYQUANTITY AS DEcimal(20,3)) As ORDQTY " \
            "        , Cast(SDL.USERPRIMARYQUANTITY AS DEcimal(20,3)) As CHALQTY " \
            "        , ChallanSDinvoice.PROVISIONALDOCUMENTDATE as INVOICEDATE " \
            "        , ChallanSDinvoice.provisionalcode as INVOICENO " \
            "        , ContSOD.CONFIRMEDDELIVERYDATE AS COMMITEMENTDATE " \
            "        , days (ContSOD.CONFIRMEDDELIVERYDATE) - days (DespOrder.ORDERDATE)  AS COMMITEDDAYS " \
            "        , days (ChallanSDinvoice.PROVISIONALDOCUMENTDATE) - days (ContSOD.CONFIRMEDDELIVERYDATE) AS DELAYDAYS " \
            "From  SALESORDER ContOrder " \
            "join ORDERPARTNER  ContOP               On      ContOrder.ORDPRNCUSTOMERSUPPLIERCODE = ContOP.CUSTOMERSUPPLIERCODE " \
            "                                        And     ContOP.CUSTOMERSUPPLIERTYPE = 1 " \
            "Join BUSINESSPARTNER  ContBP            On      ContOP.ORDERBUSINESSPARTNERNUMBERID = ContBP.NUMBERID  " \
            "Join AGENT  ContAgent                   On      ContOrder.AGENT1CODE = ContAGENT.CODE  " \
            "Join SALESORDERLINE ContSOL             On      ContOrder.CODE = ContSOL.SALESORDERCODE " \
            "                                        And     ContOrder.COUNTERCODE = ContSOL.SALESORDERCOUNTERCODE " \
            "                                        And     ContOrder.DOCUMENTTYPETYPE = ContSOL.DOCUMENTTYPETYPE " \
            "join FULLITEMKEYDECODER FIKD            ON      ContSOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
            "                                        AND     COALESCE(ContSOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
            "                                        AND     COALESCE(ContSOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
            "                                        AND     COALESCE(ContSOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
            "                                        AND     COALESCE(ContSOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
            "                                        AND     COALESCE(ContSOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
            "                                        AND     COALESCE(ContSOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
            "                                        AND     COALESCE(ContSOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
            "                                        AND     COALESCE(ContSOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')  " \
            "                                        AND     COALESCE(ContSOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')  " \
            "                                        AND     COALESCE(ContSOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
            "Join PRODUCT                            On      ContSOL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE   " \
            "                                        And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
            "Left JOIN ItemSubcodeTemplate IST       ON      ContSOL.ITEMTYPEAFICODE = IST.ItemTypeCode " \
            "                                        AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
            "LEFT JOIN USERGENERICGROUP UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
            "          AND     Case IST.Position When 1  " \
            "					Then ContSOL.SUBCODE01 When 2  " \
            "					Then ContSOL.SUBCODE02 When 3  " \
            "					Then ContSOL.SUBCODE03 When 4  " \
            "					Then ContSOL.SUBCODE04 When 5  " \
            "					Then ContSOL.SUBCODE05 When 6  " \
            "					Then ContSOL.SUBCODE06 When 7  " \
            "					Then ContSOL.SUBCODE07 When 8  " \
            "					Then ContSOL.SUBCODE08 When 9  " \
            "					Then ContSOL.SUBCODE09 When 10  " \
            "					Then ContSOL.SUBCODE10 End = UGG.Code " \
            "JOIN QUALITYLEVEL                       ON      ContSOL.QUALITYCODE = QUALITYLEVEL.CODE   " \
            "                                        AND     ContSOL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
            "Join LOGICALWAREHOUSE                   On      ContSOL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
            "Join PLANT                              On      LOGICALWAREHOUSE.PLANTCODE = PLANT.CODE      " \
            "Join SALESORDERDELIVERY ContSOD         On      ContSOL.SALESORDERCODE= ContSOD.SALESORDERLINESALESORDERCODE " \
            "                                        And     ContSOL.SALESORDERCOUNTERCODE = ContSOD.SALORDLINESALORDERCOUNTERCODE " \
            "                                        And     ContSOL.OrderLine = ContSOD.SalesOrderLineOrderLine " \
            "Join SALESORDER DespOrder              On      ContOrder.CODE = DespOrder.PreviousCODE   " \
            "                                        AND     ContOrder.COUNTERCODE = DespOrder.PreviousCOUNTERCODE " \
            "                                        And     DespOrder.DOCUMENTTYPETYPE = '03' " \
            "                                        and     DespOrder.code <> 'null' " \
            "Join SALESORDERLINE DespOrdSOL          On      DespOrder.CODE = DespOrdSOL.SalesOrderCODE " \
            "                                        And     DespOrder.COUNTERCODE = DespOrdSOL.SalesOrderCOUNTERCODE " \
            "                                        And     DespOrder.DOCUMENTTYPETYPE = DespOrdSOL.DOCUMENTTYPETYPE " \
            "                                        And     ContSOL.OrderLine = DespOrdSOL.PREVIOUSORDERLINE " \
            "Join SALESORDERDELIVERY DespOrdSOD      On      DespOrdSOL.SalesOrderCODE = DespOrdSOD.SALESORDERLINESALESORDERCODE " \
            "                                        And     DespOrdSOL.SalesOrderCOUNTERCODE = DespOrdSOD.SALORDLINESALORDERCOUNTERCODE " \
            "                                        And     DespOrdSOL.OrderLine = DespOrdSOD.SalesOrderLineOrderLine " \
            "Join SALESDOCUMENTLINE SDL              ON      DespOrdSod.SALESORDERLINESALESORDERCODE = SDL.DLVSALORDERLINESALESORDERCODE " \
            "                                        And     DespOrdSod.SALORDLINESALORDERCOUNTERCODE = SDL.DLVSALORDLINESALORDCNTCODE " \
            "                                        And     SDL.DOCUMENTTYPETYPE = '05' " \
            "                                        AND     DespOrdSod.SALESORDERLINEOrderLine = SDL.DLVSALESORDERLINEORDERLINE  " \
            "Join SALESDOCUMENT ChallanSD            On      SDL.SALESDOCUMENTPROVISIONALCODE = ChallanSD.PROVISIONALCODE " \
            "                                        And     SDL.SALDOCPROVISIONALCOUNTERCODE = ChallanSD.PROVISIONALCOUNTERCODE " \
            "                                        And     SDL.DOCUMENTTYPETYPE = ChallanSD.DOCUMENTTYPETYPE  " \
            "Join SALESDOCUMENTLINE SDLinvoice       ON      DespOrdSod.SALESORDERLINESALESORDERCODE = SDLinvoice.DLVSALORDERLINESALESORDERCODE " \
            "                                        And     DespOrdSod.SALORDLINESALORDERCOUNTERCODE = SDLinvoice.DLVSALORDLINESALORDCNTCODE " \
            "                                        And     SDLinvoice.DOCUMENTTYPETYPE = '06' " \
            "                                        AND     DespOrdSod.SALESORDERLINEOrderLine = SDL.DLVSALESORDERLINEORDERLINE  " \
            "left Join SALESDOCUMENT ChallanSDinvoice       On      SDLinvoice.SALESDOCUMENTPROVISIONALCODE = ChallanSDinvoice.PROVISIONALCODE " \
            "                                        And     SDLinvoice.SALDOCPROVISIONALCOUNTERCODE = ChallanSDinvoice.PROVISIONALCOUNTERCODE " \
            "                                        And     SDLinvoice.DOCUMENTTYPETYPE = ChallanSDinvoice.DOCUMENTTYPETYPE " \
            "left JOIN PlantInvoice    pi            ON  ChallanSDinvoice.PROVISIONALCODE = pi.CODE  " \
            "Where           ContOrder.ORDERDATE     Between         ?    And     ?   " \
            "And             ContOrder.DOCUMENTTYPETYPE In ('02') " \
            "AND             ContOrder.PREVIOUSCODE Is Null " \
            "order by PLANT.LONGDESCRIPTION "

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

# Explicitly bind parameters

    con.db.bind_param(stmt, 1, stdt)
    con.db.bind_param(stmt, 2, etdt)

    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        # print("LSReportType" +str(LSReportType))
        global counter
        counter = counter + 1
        # print(result)

        if LSReportType=='1':
            pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        elif LSReportType=='2':
            pdfrpt.textsize2(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        elif LSReportType=='3':
            pdfrpt.textsize3(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)
        # print(result)
        # print("counter : "+str(counter))
        if pdfrpt.d < 40:
            # pdfrpt.d = 730
            pdfrpt.d = 505
            pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
            pdfrpt.c.showPage()
            if LSReportType == '1':
                pdfrpt.header(stdt, etdt, pdfrpt.divisioncode)
            elif LSReportType=='2':
                pdfrpt.header2(stdt, etdt, pdfrpt.divisioncode)
            elif LSReportType=='3':
                pdfrpt.header3(stdt, etdt, pdfrpt.divisioncode)

            pdfrpt.d = pdfrpt.d - 20

    # if pdfrpt.d < 14:
    #     pdfrpt.d = 730
    #     pdfrpt.c.showPage()
    #     pdfrpt.header(stdt, etdt, pdfrpt.divisioncode)
    #     pdfrpt.d = pdfrpt.d - 20
    #     pdfrpt.itemcodes(result, pdfrpt.d)

    if result == False:
        if counter > 0:
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(8)
            EIV.Exceptions = ""
        elif counter == 0:
            EIV.Exceptions = "Note: No Result found according to your selected criteria"
            return

    if counter==0:
        EIV.Exceptions = "Note: No Result found according to your selected criteria "
    else:
        pdfrpt.c.showPage()
        pdfrpt.c.save()
        # url = "file:///D:/Reports/ReportDevelopment/" + LSFileName + ".pdf"
        # os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()


def ExportInvoiceXLS(LSallParty, LSallCompany, LSParty, LSCompany, LDStartDate,
                                 LDEndDate, LSReportType):
    xlsrpt.filename(LSReportType)
    LSName = datetime.now()
    LSstring = str(LSName)
    global LSFileName
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = " Invoice Without Shipping Bill No Register " + LSFileName + ".xlsx"

    sqlwhere = ''

    allparty = str(LSallParty)
    if allparty == 'None' and len(LSParty) != 0:
        if sqlwhere != '':
            sqlwhere += ' AND '
        party = str(LSParty)
        LSParty = '(' + party[1:-1] + ')'
        sqlwhere += ' AND PLANT.CODE IN  ' + LSParty

    allcompany = str(LSallCompany)
    if allcompany == 'None' and len(LSCompany) != 0:
        # if sqlwhere != '':
        #     sqlwhere += ' AND '
        company = str(LSCompany)
        LSCompany = '(' + company[1:-1] + ')'

        sqlwhere += ' AND BusinessPartner.NUMBERID IN ' + LSCompany + ''
    if LSReportType == '4':
        print("from 4 - - - - - -")
        sql = ""
        sql = "SELECT " \
                "        CI.CODE  as INVCODE " \
                "        , CI.INVOICEDATE as INVDATE " \
                "        , CI.EXPORTSHIPPINGBILLCODE as EXPORTINVNO " \
                "        , BusinessPartner.LEGALNAME1 AS CUSTOMER " \
                "        , COUNTRY.LONGDESCRIPTION as EXPORTCOUNTRY " \
                "        , trim (Product.LONGDESCRIPTION) AS PRODUCT " \
                "        , CLI.TARIFFCODE AS HSNCODE " \
                "        , CLI.PRIMARYQTY AS QTY " \
                "        , CLI.PRICE AS RATE " \
                "        , CURRENCY.LONGDESCRIPTION as INVOICECURRENCY " \
                "        , CAST((CI.EXCHANGERATEOFCONTRACT) AS DECIMAL(18,2)) AS EXCHANGERATE " \
                "        , CLI.GROSSVALUE AS INVOICEVALUEINCURRENCY " \
                "        , cast((CLI.GROSSVALUE*CI.EXCHANGERATEOFCONTRACT) as decimal(18,2)) AS INVOICEVALUEOFINR " \
                "        , IT.TypeOfInvoice as INVOICETYPE " \
                "FROM CUSTOMINVOICE CI " \
                "JOIN CUSTOMINVOICELINE CLI      ON CI.CODE = CLI.CUSTOMINVOICECODE " \
                "JOIN EXPORTSHIPPING ES          ON CI.EXPORTSHIPPINGBILLCODE = ES.CODE " \
                "JOIN COUNTRY                    ON CI.DESTINATIONCOUNTRYCODE = COUNTRY.CODE " \
                "Join    InvoiceType IT  On      ci.InvoiceTypeCode = IT.Code  " \
                "JOIN FullItemKeyDecoder FIKD     ON      CLI.ITEMTYPECODE = FIKD.ITEMTYPECODE " \
                "                            AND     COALESCE(CLI.SubCode1, '') = COALESCE(FIKD.SubCode01, '')  " \
                "                            AND     COALESCE(CLI.SubCode2, '') = COALESCE(FIKD.SubCode02, '')  " \
                "                            AND     COALESCE(CLI.SubCode3, '') = COALESCE(FIKD.SubCode03, '')  " \
                "                            AND     COALESCE(CLI.SubCode4, '') = COALESCE(FIKD.SubCode04, '')  " \
                "                            AND     COALESCE(CLI.SubCode5, '') = COALESCE(FIKD.SubCode05, '')  " \
                "                            AND     COALESCE(CLI.SubCode6, '') = COALESCE(FIKD.SubCode06, '')  " \
                "                            AND     COALESCE(CLI.SubCode7, '') = COALESCE(FIKD.SubCode07, '')  " \
                "                            AND     COALESCE(CLI.SubCode8, '') = COALESCE(FIKD.SubCode08, '')  " \
                "                            AND     COALESCE(CLI.SubCode9, '') = COALESCE(FIKD.SubCode09, '')  " \
                "                            AND     COALESCE(CLI.SubCode10, '') = COALESCE(FIKD.SubCode10, '')  " \
                "JOIN Product                On      CLI.ITEMTYPECODE           = Product.ITEMTYPECODE " \
                "                            And     FIKD.ItemUniqueId                           = Product.AbsUniqueId " \
                "JOIN CURRENCY               ON CI.INVOICECURRENCYCODE = CURRENCY.CODE " \
                "JOIN OrderPartner               On      CI.BUYERIFOTCCUSTOMERSUPPLIERCODE = OrderPartner.CustomerSupplierCode " \
                "                                And     CI.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OrderPartner.CustomerSupplierType " \
                "JOIN BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
              "Where           CI.INVOICEDATE  " \
              "Between         ?    And     ?  "

    elif  LSReportType == '5':
        sql = ""
        sql = "SELECT  CI.CODE  as INVCODE " \
            "        , CI.INVOICEDATE as INVDATE " \
            "        , CI.EXPORTSHIPPINGBILLCODE as EXPORTINVNO " \
            "        , BusinessPartner.LEGALNAME1 AS CUSTOMER " \
            "        , COUNTRY.LONGDESCRIPTION as EXPORTCOUNTRY " \
            "        , trim (Product.LONGDESCRIPTION) AS PRODUCT " \
            "        , CLI.TARIFFCODE AS HSNCODE " \
            "        , CAST((CLI.PRIMARYQTY) AS DECIMAL(18,3)) AS QTY " \
            "        , CAST((CLI.PRICE)AS DECIMAL(18,2)) AS RATE " \
            "        , CURRENCY.LONGDESCRIPTION as INVOICECURRENCY " \
            "        , CAST((CI.EXCHANGERATEOFCONTRACT) AS DECIMAL(18,2)) AS EXCHANGERATE " \
            "        , CAST((CLI.GROSSVALUE) AS DECIMAL(18,2)) AS INVOICEVALUEINCURRENCY " \
            "        , CAST((CLI.GROSSVALUE*CI.EXCHANGERATEOFCONTRACT) as decimal(18,2)) AS INVOICEVALUEOFINR " \
            "        , CI.AWBDATE " \
            "        , CI.PORTOFLOADINGCODE " \
            "        , PORT.LONGDESCRIPTION AS SHIPPINGPORTCODEEXPORT " \
            "        , EXPORTSHIPPING.CODE AS SHIPPINGBILLNUMBEREXPORT " \
            "        , EXPORTSHIPPING.SHIPPINGBILLDATE AS SHIPPINGBILLDATEEXPORT " \
            "        , EXPORTSHIPPING.FOBVALUEINCC  AS FOBVALUEINCC" \
            "        , EXPORTSHIPPING.FOBVALUEINR AS FOBVALUEINR" \
            " FROM CUSTOMINVOICE CI " \
            "JOIN CUSTOMINVOICELINE CLI      ON CI.CODE 					 = CLI.CUSTOMINVOICECODE " \
            "JOIN EXPORTSHIPPING ES          ON CI.EXPORTSHIPPINGBILLCODE = ES.CODE " \
            "JOIN COUNTRY                    ON CI.DESTINATIONCOUNTRYCODE = COUNTRY.CODE " \
            "Join InvoiceType IT  			ON CI.InvoiceTypeCode 		 = IT.Code " \
            "JOIN FullItemKeyDecoder FIKD    ON      CLI.ITEMTYPECODE = FIKD.ITEMTYPECODE  " \
            "                                AND     COALESCE(CLI.SubCode1, '') = COALESCE(FIKD.SubCode01, '') " \
            "                                AND     COALESCE(CLI.SubCode2, '') = COALESCE(FIKD.SubCode02, '')  " \
            "                                AND     COALESCE(CLI.SubCode3, '') = COALESCE(FIKD.SubCode03, '')  " \
            "                                AND     COALESCE(CLI.SubCode4, '') = COALESCE(FIKD.SubCode04, '')  " \
            "                                AND     COALESCE(CLI.SubCode5, '') = COALESCE(FIKD.SubCode05, '')   " \
            "                                AND     COALESCE(CLI.SubCode6, '') = COALESCE(FIKD.SubCode06, '')   " \
            "                                AND     COALESCE(CLI.SubCode7, '') = COALESCE(FIKD.SubCode07, '')   " \
            "                                AND     COALESCE(CLI.SubCode8, '') = COALESCE(FIKD.SubCode08, '')   " \
            "                                AND     COALESCE(CLI.SubCode9, '') = COALESCE(FIKD.SubCode09, '')   " \
            "                                AND     COALESCE(CLI.SubCode10, '') = COALESCE(FIKD.SubCode10, '')  " \
            "JOIN Product                On  CLI.ITEMTYPECODE           		= Product.ITEMTYPECODE " \
            "                            And FIKD.ItemUniqueId               = Product.AbsUniqueId " \
            "JOIN CURRENCY               ON  CI.INVOICECURRENCYCODE 		    = CURRENCY.CODE   " \
            "JOIN OrderPartner           On  CI.BUYERIFOTCCUSTOMERSUPPLIERCODE = OrderPartner.CustomerSupplierCode " \
            "                            And CI.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OrderPartner.CustomerSupplierType " \
            "JOIN BusinessPartner        On  OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID  " \
            "JOIN PORT                   ON  CI.PORTOFLOADINGCODE	= PORT.CODE   " \
            "JOIN INDTAXDETAIL           ON  CI.ABSUNIQUEID          = INDTAXDETAIL.ABSUNIQUEID " \
            "                            AND CI.TAXTEMPLATECODE IN ('SH1') " \
            "LEFT JOIN EXPORTSHIPPINGLINE    ON CI.EXPORTSHIPPINGBILLCODE = EXPORTSHIPPINGLINE.CUSTOMINVOICECODE    " \
            "LEFT JOIN EXPORTSHIPPING        ON EXPORTSHIPPINGLINE.EXPORTSHIPPINGCODE = EXPORTSHIPPING.CODE  " \
              "Where           CI.INVOICEDATE  " \
              "Between         ?    And     ?  "

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    # Explicitly bind parameters

    con.db.bind_param(stmt, 1, stdt)
    con.db.bind_param(stmt, 2, etdt)

    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print("after result")
    # xlsrpt.createxls()
    # xlsrpt.xlsxwriter.Workbook("test.xlsx")
    # xlsrpt.workbook.add_worksheet()
    if LSReportType == '4':
        xlsrpt.xmlheader()
    elif LSReportType == '5':
        xlsrpt.xmlheader5()
    print("after header")
    while result != False:
        # print("LSReportType" +str(LSReportType))
        global counter
        counter = counter + 1
        # print(result)

        if LSReportType == '4':
            xlsrpt.textsize( result, stdt, etdt)
        elif LSReportType == '5':
            print("calling 5")

            xlsrpt.textsize5( result,  stdt, etdt)
        # xlsrpt.d = xlsrpt.dvalue()
        result = con.db.fetch_both(stmt)
        # print(result)
        # print("counter : "+str(counter))
        # if pdfrpt.d < 40:
        #     # pdfrpt.d = 730
        #     pdfrpt.d = 505
        #     pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
        #     pdfrpt.c.showPage()
        #     if LSReportType == '1':
        #         pdfrpt.header(stdt, etdt, pdfrpt.divisioncode)
        #     elif LSReportType == '2':
        #         pdfrpt.header2(stdt, etdt, pdfrpt.divisioncode)
        #     elif LSReportType == '3':
        #         pdfrpt.header3(stdt, etdt, pdfrpt.divisioncode)
        #
        #     pdfrpt.d = pdfrpt.d - 20

    # if pdfrpt.d < 14:
    #     pdfrpt.d = 730
    #     pdfrpt.c.showPage()
    #     pdfrpt.header(stdt, etdt, pdfrpt.divisioncode)
    #     pdfrpt.d = pdfrpt.d - 20
    #     pdfrpt.itemcodes(result, pdfrpt.d)

    if result == False:
        if counter > 0:
            # xlsrpt.d = xlsrpt.dlocvalue(xlsrpt.d)
            # xlsrpt.fonts(7)
            # xlsrpt.d = xlsrpt.dlocvalue(xlsrpt.d)
            # xlsrpt.fonts(8)
            EIV.Exceptions = ""
        elif counter == 0:
            EIV.Exceptions = "Note: No Result found according to your selected criteria"
            return

    if counter == 0:
        EIV.Exceptions = "Note: No Result found according to your selected criteria "
    else:
        xlsrpt.workbook.close()

        print("after closing workbook")
    #     xlsrpt.c.showPage()
    #     xlsrpt.c.save()
    #     # url = "file:///D:/Reports/ReportDevelopment/" + LSFileName + ".pdf"
    #     # os.startfile(url)
        xlsrpt.newrequest()
    #     xlsrpt.d = xlsrpt.newpage()