import os
from datetime import datetime

from django.shortcuts import render
from django.views.static import serve

from FormLoad import PrintProformaInv_Formload as views

from Global_Files import Connection_String as con
from PrintPDF import PrintProformaPrePackLis_PrintPDF as pdfrpt
save_name=""

Exceptions=""

counter=0


def PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate):
    global Exceptions
    sql = "SELECT Comp.LONGDESCRIPTION As Company " \
          ", 'FACTORY: '||' '||Coalesce(PLANT.addressline1,'') " \
          "|| Coalesce(','||PLANT.addressline2,'') || Coalesce(','||PLANT.addressline3,'') " \
          "|| Coalesce(','||PLANT.addressline4,'') || Coalesce(','||PLANT.addressline5,'') " \
          "|| RTRIM(Coalesce(','||PLANT.postalcode,'')) ||'   GSTIN : '|| ADGSTIN.GSTINNUMBER AS Fac_ADDRESS " \
          ", 'REGD. OFF: '||' '||Coalesce(REGD_ADDRESS.addressline1,'') || Coalesce(','||REGD_ADDRESS.addressline2,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline3,'') || Coalesce(','||REGD_ADDRESS.addressline4,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline5,'') || Coalesce(','||REGD_ADDRESS.postalcode,'') AS REGD_ADDRESS " \
          ", 'CIN: '||''||Firm.TINNo AS CINNO " \
          ", 'CORP. OFF: '||' '||Coalesce(CORP_ADDRESS.addressline1,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline2,'') || Coalesce(','||CORP_ADDRESS.addressline3,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline4,'') || Coalesce(','||CORP_ADDRESS.addressline5,'') " \
          "|| Coalesce(','||CORP_ADDRESS.postalcode,'') AS CORP_ADDRESS " \
          ", 'GSTIN : 27AAACB2976M1ZB ' As CORP_GSTIN " \
          ", 'TAX ID NO.: '||''||FIRM.PANNO As TAXID " \
          ", 'IEC.NO.: ' ||''||Firm.IECODE As IecNo " \
          ", PLANTINVOICE.CODE ||'             DT :   '|| VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') AS INVOICENOandDt " \
          ", SO.CODE ||'             DT :   '|| VARCHAR_FORMAT(SO.ORDERDATE,'DD-MM-YYYY') AS OrdNOandDt " \
          ", COALESCE(BP_CONsig.LEGALNAME1,'') AS CONSIGNEEname " \
          ", CASE When ADDRESS_CONsignee.UNIQUEID is Not Null Then Coalesce(ADDRESS_CONsignee.ADDRESSEE,'') " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE1,'') || Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE2,'') " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE3,'') || Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE4,'') " \
          "||','|| Coalesce(ADDRESS_CONsignee.ADDRESSLINE5,'') ||', Postal Code : '||Coalesce(ADDRESS_CONsignee.POSTALCODE,'') " \
          "Else Coalesce(BP_CONsig.ADDRESSLINE1,'') || Coalesce(','||BP_CONsig.ADDRESSLINE2,'') " \
          "|| Coalesce(','||BP_CONsig.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BP_CONsig.ADDRESSLINE4,'') ||','|| Coalesce(BP_CONsig.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(BP_CONsig.POSTALCODE,'') End  as CONSIGNEEADDRESS " \
          ", BusinessPartner.LEGALNAME1 AS Buyer " \
          ", Coalesce(BusinessPartner.ADDRESSLINE1,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE2,'') || Coalesce(','||BusinessPartner.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE4,'') ||','|| Coalesce(BusinessPartner.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(BusinessPartner.POSTALCODE,'') as BuyerAddress " \
          ", COALESCE(BP_NotifyPrty.LEGALNAME1,'') AS NotifyPrtyname " \
          ", CASE When ADDRESS_NotifyPrty.UNIQUEID is Not Null Then Coalesce(ADDRESS_NotifyPrty.ADDRESSEE,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE1,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE2,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE3,'') || Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE4,'') " \
          "||','|| Coalesce(ADDRESS_NotifyPrty.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(ADDRESS_NotifyPrty.POSTALCODE,'') Else Coalesce(BP_NotifyPrty.ADDRESSLINE1,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE2,'') || Coalesce(','||BP_NotifyPrty.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE4,'') || Coalesce(','||BP_NotifyPrty.ADDRESSLINE5,'') " \
          "|| Coalesce(',Postal Code : ' || BP_NotifyPrty.POSTALCODE,'') End  as NotifyPrtyADDRESS " \
          ", TermsOfShipping.LONGDESCRIPTION AS TermsOfDelv " \
          ", PAYMENTMETHOD.LONGDESCRIPTION As Payment " \
          ", CountryOrgnGoods.LONGDESCRIPTION as CountryOfOriginOfGoods " \
          ", CountryDestn.LONGDESCRIPTION as CountryOfDestn	" \
          ", COALESCE(portOfLoad.LONGDESCRIPTION,'')  As PortOfLoading " \
          ", COALESCE(portOfDIS.LONGDESCRIPTION,'') As PortOfDischarge " \
          ", COALESCE(finalDstn.LONGDESCRIPTION,'') As FinalDestination " \
          ", COALESCE(PLANTINVOICE.VESSELFLIGHTNO,'') As VesselFlightNo " \
          ", COALESCE(PLANTINVOICE.BLNUMBER,'') AS BlNo " \
          ", COALESCE(VARCHAR_FORMAT(PLANTINVOICE.BLDATE,'DD-MM-YYYY'),'') AS BlDt " \
          ", '' As SBNo " \
          ", '' As SbDt " \
          ", COALESCE(PLANTINVOICE.CONTAINERSIZE, '') As ContSize " \
          ", COALESCE(PLANTINVOICE.CONTAINERNO, '') As ContNO " \
          ", TRIM(COALESCE(PLANTINVOICE.CUSTOMERBOTTLESEALNO, '')) As SealNo " \
          ", COALESCE(PLANTINVOICE.BOTTLESEALNO, '') As ESealNo " \
          ", COALESCE(BKLELEMENTS.ACTUALUNITCODE,'') As WtUnit " \
          ", CAST(PLANTINVOICE.GROSSWEIGHT As Decimal(20,3)) As GrWt " \
          ", Cast(PLANTINVOICE.NETTWEIGHT As Decimal(20,3)) As NetWt " \
          ", '' As Measure " \
          ", PlantInvoice.TOTALNUMBEROFBALES As Packages " \
          ", ITEMTYPE.LONGDESCRIPTION ||' (' || ITEMTYPE.CODE ||')' As ItmTyp " \
          ", trim (Product.LONGDESCRIPTION || ' ' || COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| QualityLevel.ShortDescriptiON) AS Item " \
          ", PIL.TARIFFCODE AS HSNCODE " \
          ", STXN.LOTCODE As LotNo " \
          ", Cast(PIL.GROSSWEIGHT As Decimal(20,3)) As GrossWt " \
          ", Cast(PIL.NETTWEIGHT As Decimal(20,3)) As NetWt " \
          ", CAST((SUM(BKLELEMENTS.ACTUALGROSSWT )) As DECIMAL(10,3)) As ItmGrossWt " \
          ", CAST((SUM(BKLELEMENTS.ACTUALNETWT)) As DECIMAL(10,3)) As ItmNetWt " \
          ", CAST((Count(stxn.TRANSACTIONNUMBER)) As INT) As ItmPackages " \
          ", COUNTRY.LONGDESCRIPTION as CountryOfOrigin " \
          ", PIL.NUMBEROFBALES As  ItemPackages " \
          ", PlantInvoice.CATEGORY As MasterExpNo " \
          ", PlantInvoice.INVOICEDATE As MasterExpDt " \
          "From PlantInvoice " \
          "join OrderPartner                       ON      PlantInvoice.BUYERIFOTCCUSTOMERSUPPLIERCODE = OrderPartner.CustomerSupplierCode " \
          "AND     PlantInvoice.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OrderPartner.CustomerSupplierType " \
          "join BusinessPartner                    ON      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
          "Left join OrderPartner OP_CONsig        ON      PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERCODE = OP_CONsig.CustomerSupplierCode " \
          "AND     PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERTYPE = OP_CONsig.CustomerSupplierType " \
          "Left join BusinessPartner BP_CONsig     ON      OP_CONsig.OrderbusinessPartnerNumberId 	= BP_CONsig.NumberID " \
          "LEFT JOIN Address ADDRESS_CONsignee     ON      BP_CONsig.ABSUNIQUEID = ADDRESS_CONsignee.UNIQUEID " \
          "AND     PLANTINVOICE.DELIVERYPOINTCODE = ADDRESS_CONsignee.CODE " \
          "Left Join OrderPartner OP_NotifyPrty    On      PLANTINVOICE.NOTIFYPARTYCSMSUPPLIERCODE = OP_NotifyPrty.CustomerSupplierCode " \
          "AND     PLANTINVOICE.NOTIFYPARTYCSMSUPPLIERTYPE = OP_NotifyPrty.CustomerSupplierType " \
          "Left join BusinessPartner BP_NotifyPrty ON      OP_NotifyPrty.OrderbusinessPartnerNumberId 	= BP_NotifyPrty.NumberID " \
          "LEFT JOIN Address ADDRESS_NotifyPrty    ON      BP_NotifyPrty.ABSUNIQUEID = ADDRESS_NotifyPrty.UNIQUEID " \
          "AND     PLANTINVOICE.DELIVERYPOINTCODE = ADDRESS_NotifyPrty.CODE " \
          "Join SALESORDER   SO                    On      PLANTINVOICE.CONTRACTNOCODE = SO.CODE " \
          "AND     PLANTINVOICE.CONTRACTNOCOUNTERCODE = SO.COUNTERCODE " \
          "Join PAYMENTMETHOD                      On      PLANTINVOICE.TERMSOFPAYMENTCODE = PAYMENTMETHOD.CODE " \
          "Left Join COUNTRY CountryDestn          On      PLANTINVOICE.DESTINATIONCOUNTRYCODE = CountryDestn.CODE " \
          "Left Join COUNTRY CountryOrgnGoods      On      PLANTINVOICE.GOODSORIGINCOUNTRYCODE = CountryOrgnGoods.CODE " \
          "Left Join PORT portOfLoad               On      PLANTINVOICE.PORTOFLOADINGCODE = portOfLoad.CODE " \
          "Left Join PORT portOfDIS                On      PLANTINVOICE.PORTOFDISCHARGECODE = portOfDIS.CODE " \
          "Left Join DESTINATION finalDstn         On      PLANTINVOICE.FINALDESTINATIONCODE = finalDstn.CODE " \
          "JOIN PLANTINVOICELINE  PIL              ON 	PIL.PLANTINVOICECODE = PLANTINVOICE.CODE " \
          "AND 	PIL.PLANTINVOICEDIVISIONCODE = PLANTINVOICE.DIVISIONCODE " \
          "Join ITEMTYPE                           ON      PIL.ITEMTYPECODE = ITEMTYPE.CODE " \
          "JOIN TermsOfShipping                    ON      PLANTINVOICE.TERMSOFSHIPPINGCODE = TermsOfShipping.CODE " \
          "JOIN FIRM                               ON      plantinvoice.DIVISIONCODE = FIRM.CODE " \
          "JOIN DIVISION                           ON 	PLANTINVOICE.DIVISIONCODE = DIVISION.CODE " \
          "JOIN ADDRESS REGD_ADDRESS               ON 	DivisiON.AbsUniqueId = REGD_ADDRESS.UniqueId " \
          "AND 	REGD_ADDRESS.Code = 'REGD' " \
          "JOIN ADDRESS CORP_ADDRESS               ON 	DivisiON.AbsUniqueId = CORP_ADDRESS.UniqueId " \
          "AND 	CORP_ADDRESS.Code = 'CORP' " \
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
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07')  " \
          "LEFT JOIN USERGENERICGROUP UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then PIL.SUBCODE01 When 2 Then PIL.SUBCODE02 When 3 Then PIL.SUBCODE03 When 4 Then PIL.SUBCODE04 When 5 Then PIL.SUBCODE05 " \
          "When 6 Then PIL.SUBCODE06 When 7 Then PIL.SUBCODE07 When 8 Then PIL.SUBCODE08 When 9 Then PIL.SUBCODE09 When 10 Then PIL.SUBCODE10 End = UGG.Code " \
          "JOIN QUALITYLEVEL                       ON      PIL.QUALITYLEVELCODE = QUALITYLEVEL.CODE " \
          "AND     PIL.ITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          "Join LOGICALWAREHOUSE                   On      PIL.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Join BUSINESSUNITVSCOMPANY BUC          On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE " \
          "Join FINBUSINESSUNIT                    On      BUC.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "And     FINBUSINESSUNIT.GROUPFLAG = 0 " \
          "Join FINBUSINESSUNIT Comp               On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
          "And     Comp.GROUPFLAG = 1 " \
          "JOIN PLANT                              ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE " \
          "JOIN FACTORY                            ON      PLANT.CODE = FACTORY.CODE " \
          "LEFT JOIN ADDRESSGST ADGSTIN            ON      FACTORY.ABSUNIQUEID = ADGSTIN.UNIQUEID " \
          "Join COUNTRY                            On      PLANT.COUNTRYCODE = COUNTRY.CODE " \
          "JOIN SALESDOCUMENTLINE SDL              ON      PIL.PLANTINVOICECODE = SDL.SALESDOCUMENTPROVISIONALCODE " \
          "AND     PIL.ITEMTYPECODE = SDL.ITEMTYPEAFICODE " \
          "AND     COALESCE(PIL.SubCode01, '') = COALESCE(SDL.SubCode01, '') " \
          "AND     COALESCE(PIL.SubCode02, '') = COALESCE(SDL.SubCode02, '') " \
          "AND     COALESCE(PIL.SubCode03, '') = COALESCE(SDL.SubCode03, '') " \
          "AND     COALESCE(PIL.SubCode04, '') = COALESCE(SDL.SubCode04, '') " \
          "AND     COALESCE(PIL.SubCode05, '') = COALESCE(SDL.SubCode05, '') " \
          "AND     COALESCE(PIL.SubCode06, '') = COALESCE(SDL.SubCode06, '') " \
          "AND     COALESCE(PIL.SubCode07, '') = COALESCE(SDL.SubCode07, '') " \
          "AND     COALESCE(PIL.SubCode08, '') = COALESCE(SDL.SubCode08, '') " \
          "AND     COALESCE(PIL.SubCode09, '') = COALESCE(SDL.SubCode09, '') " \
          "AND     COALESCE(PIL.SubCode10, '') = COALESCE(SDL.SubCode10, '') " \
          "AND     PIL.QUALITYLEVELCODE = SDL.QUALITYCODE " \
          "Join STOCKTRANSACTION STXN              On      SDL.PREVIOUSCODE = STXN.ORDERCODE " \
          "AND     SDL.PREVIOUSCOUNTERCODE = STXN.ORDERCOUNTERCODE " \
          "AND     SDL.PREVIOUSORDERLINE = STXN.ORDERLINE " \
          "Left JOIN BKLELEMENTS                        ON      STXN.CONTAINERELEMENTCODE = BKLELEMENTS.CODE " \
          "Where "+InvoiceNos+" " \
          "GROUP BY Comp.LONGDESCRIPTION " \
          ", 'FACTORY: '||' '||Coalesce(PLANT.addressline1,'') " \
          "|| Coalesce(','||PLANT.addressline2,'') || Coalesce(','||PLANT.addressline3,'') " \
          "|| Coalesce(','||PLANT.addressline4,'') || Coalesce(','||PLANT.addressline5,'') " \
          "|| RTRIM(Coalesce(','||PLANT.postalcode,'')) ||'   GSTIN : '|| ADGSTIN.GSTINNUMBER " \
          ", 'REGD. OFF: '||' '||Coalesce(REGD_ADDRESS.addressline1,'') || Coalesce(','||REGD_ADDRESS.addressline2,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline3,'') || Coalesce(','||REGD_ADDRESS.addressline4,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline5,'') || Coalesce(','||REGD_ADDRESS.postalcode,'') " \
          ", 'CIN: '||''||Firm.TINNo " \
          ", 'CORP. OFF: '||' '||Coalesce(CORP_ADDRESS.addressline1,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline2,'') || Coalesce(','||CORP_ADDRESS.addressline3,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline4,'') || Coalesce(','||CORP_ADDRESS.addressline5,'') " \
          "|| Coalesce(','||CORP_ADDRESS.postalcode,'') " \
          ", 'GSTIN : 27AAACB2976M1ZB ' " \
          ", 'TAX ID NO.: '||''||FIRM.PANNO " \
          ", 'IEC.NO.: ' ||''||Firm.IECODE " \
          ", PLANTINVOICE.CODE ||'             DT :   '|| VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') " \
          ", SO.CODE ||'             DT :   '|| VARCHAR_FORMAT(SO.ORDERDATE,'DD-MM-YYYY') " \
          ", COALESCE(BP_CONsig.LEGALNAME1,'') " \
          ", CASE When ADDRESS_CONsignee.UNIQUEID is Not Null Then Coalesce(ADDRESS_CONsignee.ADDRESSEE,'') " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE1,'') || Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE2,'') " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE3,'') || Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE4,'') " \
          "||','|| Coalesce(ADDRESS_CONsignee.ADDRESSLINE5,'') ||', Postal Code : '||Coalesce(ADDRESS_CONsignee.POSTALCODE,'') " \
          "Else Coalesce(BP_CONsig.ADDRESSLINE1,'') || Coalesce(','||BP_CONsig.ADDRESSLINE2,'') " \
          "|| Coalesce(','||BP_CONsig.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BP_CONsig.ADDRESSLINE4,'') ||','|| Coalesce(BP_CONsig.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(BP_CONsig.POSTALCODE,'') End " \
          ", BusinessPartner.LEGALNAME1 " \
          ", Coalesce(BusinessPartner.ADDRESSLINE1,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE2,'') || Coalesce(','||BusinessPartner.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE4,'') ||','|| Coalesce(BusinessPartner.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(BusinessPartner.POSTALCODE,'') " \
          ", COALESCE(BP_NotifyPrty.LEGALNAME1,'') " \
          ", CASE When ADDRESS_NotifyPrty.UNIQUEID is Not Null Then Coalesce(ADDRESS_NotifyPrty.ADDRESSEE,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE1,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE2,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE3,'') || Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE4,'') " \
          "||','|| Coalesce(ADDRESS_NotifyPrty.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(ADDRESS_NotifyPrty.POSTALCODE,'') Else Coalesce(BP_NotifyPrty.ADDRESSLINE1,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE2,'') || Coalesce(','||BP_NotifyPrty.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE4,'') || Coalesce(','||BP_NotifyPrty.ADDRESSLINE5,'') " \
          "|| Coalesce(',Postal Code : ' || BP_NotifyPrty.POSTALCODE,'') End " \
          ", TermsOfShipping.LONGDESCRIPTION " \
          ", PAYMENTMETHOD.LONGDESCRIPTION " \
          ", CountryOrgnGoods.LONGDESCRIPTION " \
          ", CountryDestn.LONGDESCRIPTION " \
          ", COALESCE(portOfLoad.LONGDESCRIPTION,'') " \
          ", COALESCE(portOfDIS.LONGDESCRIPTION,'') " \
          ", COALESCE(finalDstn.LONGDESCRIPTION,'') " \
          ", COALESCE(PLANTINVOICE.VESSELFLIGHTNO,'') " \
          ", COALESCE(PLANTINVOICE.BLNUMBER,'') " \
          ", COALESCE(VARCHAR_FORMAT(PLANTINVOICE.BLDATE,'DD-MM-YYYY'),'') " \
          ", '' " \
          ", '' " \
          ", COALESCE(PLANTINVOICE.CONTAINERSIZE, '') " \
          ", COALESCE(PLANTINVOICE.CONTAINERNO, '') " \
          ", TRIM(COALESCE(PLANTINVOICE.CUSTOMERBOTTLESEALNO, '')) " \
          ", COALESCE(PLANTINVOICE.BOTTLESEALNO, '') " \
          ", COALESCE(BKLELEMENTS.ACTUALUNITCODE,'') " \
          ", CAST(PLANTINVOICE.GROSSWEIGHT As Decimal(20,3)) " \
          ", Cast(PLANTINVOICE.NETTWEIGHT As Decimal(20,3)) " \
          ", '' " \
          ", PlantInvoice.TOTALNUMBEROFBALES " \
          ", ITEMTYPE.LONGDESCRIPTION ||' (' || ITEMTYPE.CODE ||')' " \
          ", trim (Product.LONGDESCRIPTION || ' ' || COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| QualityLevel.ShortDescriptiON) " \
          ", PIL.TARIFFCODE " \
          ", STXN.LOTCODE " \
          ", Cast(PIL.GROSSWEIGHT As Decimal(20,3)) " \
          ", Cast(PIL.NETTWEIGHT As Decimal(20,3)) " \
          ", COUNTRY.LONGDESCRIPTION " \
          ", PIL.NUMBEROFBALES " \
          ", PlantInvoice.CATEGORY " \
          ", PlantInvoice.INVOICEDATE " \
          "Order By Company, INVOICENOandDt, Buyer, OrdNOandDt, itmTyp, Item "
    # try:
    stmt = con.db.prepare(con.conn, sql)
    # Explicitly bind parameters
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 150:
            pdfrpt.d = 435
            pdfrpt.c.showPage()
            pdfrpt.header(pdfrpt.divisioncode, result,pdfrpt.Yordno)

    if result == False:
        if counter > 0:

              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.c.drawString(155, pdfrpt.d, "Lot No. :   " + str(pdfrpt.lotno[-1]))
              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.c.drawString(155, pdfrpt.d, "HSNCODE :  " + pdfrpt.hsncode[-1])
              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.c.drawString(155, pdfrpt.d, "COUNTRY OF ORIGIN:  " + str(pdfrpt.countryofOrigin[-1]).upper())
              pdfrpt.c.drawString(380, 105, "Total ")
              pdfrpt.c.drawAlignedString(448, 105, str(pdfrpt.packages))
              pdfrpt.c.drawAlignedString(500, 105, str('{0:1.3f}'.format(pdfrpt.grosswt)))
              pdfrpt.c.drawAlignedString(565, 105, str('{0:1.3f}'.format(pdfrpt.netwt)))
              # ************** groos wt and nt wt at shipping marks ,packages
              pdfrpt.c.drawString(85, 420, str('{0:1.3f}'.format(pdfrpt.grosswt)))
              pdfrpt.c.drawString(85, 410, str('{0:1.3f}'.format(pdfrpt.netwt)))
              pdfrpt.c.drawString(85, 390, str(pdfrpt.packages))
              pdfrpt.boldfonts(6)
              pdfrpt.c.drawAlignedString(175, 450, str(pdfrpt.packages))  # No Of Cartons
              pdfrpt.fonts(7)
              pdfrpt.TotalClean()

              Exceptions = ""
              counter = 0
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria "
            return


    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.d = pdfrpt.newpage()
    pdfrpt.i = 0
    pdfrpt.TotalClean()
    pdfrpt.newrequest()
    # except:
    #       raise Exception("Please Run the Server Again ")