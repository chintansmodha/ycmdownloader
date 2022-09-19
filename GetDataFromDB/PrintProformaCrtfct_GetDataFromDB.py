import os
from datetime import datetime

from django.shortcuts import render
from django.views.static import serve

from FormLoad import PrintProformaInv_Formload as views

from Global_Files import Connection_String as con
from PrintPDF import PrintProformaCrtfct_PrintPDF as pdfrpt
save_name=""

Exceptions=""

counter=0


def PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate):
    global Exceptions
    sql = "SELECT  Comp.LONGDESCRIPTION As Company " \
          ", 'CORP. OFF: '||' '||Coalesce(CORP_ADDRESS.ADDRESSEE,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline1,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline2,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline3,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline4,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline5,'') " \
          "|| Coalesce(','||CORP_ADDRESS.postalcode,'') ||' (India)                 '|| ' GSTIN : 27AAACB2976M1ZB ' " \
          "||'        '|| 'TAX ID NO.: '||''||FIRM.PANNO ||'  '|| 'IEC.NO.: ' ||''|| Firm.IECODE " \
          "||'        '|| 'CIN: '||''||Firm.TINNo As CORP_ADDRESS " \
          ", BusinessPartner.LEGALNAME1 AS Buyer " \
          ", Coalesce(BusinessPartner.ADDRESSLINE1,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE2,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE4,'') " \
          "||','|| Coalesce(BusinessPartner.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(BusinessPartner.POSTALCODE,'') as BuyerAddress " \
          ", 'FROM  '||''|| portOfLoad.LONGDESCRIPTION ||',  '|| TermsOfShipping.LONGDESCRIPTION As PortOfLoading " \
          ", portOfDIS.LONGDESCRIPTION As PortOfDischarge " \
          ", COUNTRY.LONGDESCRIPTION as CountryOfOrigin " \
          ", CountryDestn.LONGDESCRIPTION as CountryOfDestn " \
          ", COALESCE(PLANTINVOICE.CONTAINERNO, '') As ContNO " \
          ", TRIM(COALESCE(PLANTINVOICE.CUSTOMERBOTTLESEALNO, '')) As SealNo " \
          ", COALESCE(PLANTINVOICE.BOTTLESEALNO, '') As ESealNo " \
          ", CAST((Count(stxn.TRANSACTIONNUMBER)) As INT) As Boxes " \
          ", COALESCE(PLANTINVOICE.WEIGHTUMCODE,'') As Unit " \
          ", CAST(PLANTINVOICE.GROSSWEIGHT AS DECIMAL(20,3)) As GrWt " \
          ", CAST(PLANTINVOICE.NETTWEIGHT AS DECIMAL(20,3)) As NetWt " \
          ", ITEMTYPE.LONGDESCRIPTION ||' (' || ITEMTYPE.CODE ||')' As ItmTyp " \
          ", trim (Product.LONGDESCRIPTION || ' ' || COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| QualityLevel.ShortDescriptiON) AS Item " \
          ", STXN.LOTCODE As LotNo " \
          ", PIL.TARIFFCODE AS HSNCODE " \
          ", PLANTINVOICE.CODE AS INVOICENO " \
          ", PLANTINVOICE.INVOICEDATE AS INVOICENOandDt  " \
          ", PAYMENTMETHOD.LONGDESCRIPTION As Payment " \
          ", 'IMC  ' ||' ' || COALESCE(FIRM.DEPBENROLLMENTNO, '') AS IMCNO " \
          ", PLANTINVOICE.INVOICEDATE As InvDt " \
          "From PlantInvoice " \
          "join OrderPartner                       ON      PlantInvoice.BUYERIFOTCCUSTOMERSUPPLIERCODE = OrderPartner.CustomerSupplierCode " \
          "AND     PlantInvoice.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OrderPartner.CustomerSupplierType " \
          "join BusinessPartner                    ON      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
          "Join SALESORDER   SO                    On      PLANTINVOICE.CONTRACTNOCODE = SO.CODE " \
          "AND     PLANTINVOICE.CONTRACTNOCOUNTERCODE = SO.COUNTERCODE " \
          "Join PAYMENTMETHOD                      On      PLANTINVOICE.TERMSOFPAYMENTCODE = PAYMENTMETHOD.CODE " \
          "Left Join COUNTRY CountryDestn          On      PLANTINVOICE.DESTINATIONCOUNTRYCODE = CountryDestn.CODE " \
          "Left Join COUNTRY CountryOrgnGoods      On      PLANTINVOICE.GOODSORIGINCOUNTRYCODE = CountryOrgnGoods.CODE " \
          "Left Join PORT portOfLoad               On      PLANTINVOICE.PORTOFLOADINGCODE = portOfLoad.CODE " \
          "Left Join PORT portOfDIS                On      PLANTINVOICE.PORTOFDISCHARGECODE = portOfDIS.CODE " \
          "Left Join DESTINATION finalDstn         On      PLANTINVOICE.FINALDESTINATIONCODE = finalDstn.CODE " \
          "Left Join ADDRESS PlaDelvAdd            On      PLANTINVOICE.DELIVERYPOINTUNIQUEID = PlaDelvAdd.UNIQUEID " \
          "AND     PLANTINVOICE.DELIVERYPOINTCODE = PlaDelvAdd.CODE " \
          "Left Join DESTINATION PlaceDelv         On      PlaDelvAdd.CODE = PlaceDelv.CODE " \
          "JOIN PLANTINVOICELINE  PIL              ON 	PIL.PLANTINVOICECODE = PLANTINVOICE.CODE " \
          "AND 	PIL.PLANTINVOICEDIVISIONCODE = PLANTINVOICE.DIVISIONCODE " \
          "Join ITEMTYPE                           ON      PIL.ITEMTYPECODE = ITEMTYPE.CODE " \
          "JOIN TermsOfShipping                    ON      PLANTINVOICE.TERMSOFSHIPPINGCODE = TermsOfShipping.CODE " \
          "JOIN FIRM                               ON      plantinvoice.DIVISIONCODE = FIRM.CODE " \
          "JOIN DIVISION                           ON 	PLANTINVOICE.DIVISIONCODE = DIVISION.CODE " \
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
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
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
          "JOIN FACTORY                            ON      BUC.FACTORYCODE = FACTORY.CODE  " \
          "LEFT JOIN ADDRESSGST ADGSTIN            ON      FACTORY.ABSUNIQUEID = ADGSTIN.UNIQUEID " \
          "Join COUNTRY                            On      FACTORY.COUNTRYCODE = COUNTRY.CODE " \
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
          "Where   "+InvoiceNos+"           " \
          "Group By                Comp.LONGDESCRIPTION " \
          ", 'CORP. OFF: '||' '||Coalesce(CORP_ADDRESS.ADDRESSEE,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline1,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline2,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline3,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline4,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline5,'') " \
          "|| Coalesce(','||CORP_ADDRESS.postalcode,'') ||' (India)                 '|| ' GSTIN : 27AAACB2976M1ZB ' " \
          "||'        '|| 'TAX ID NO.: '||''||FIRM.PANNO ||'  '|| 'IEC.NO.: ' ||''|| Firm.IECODE " \
          "||'        '|| 'CIN: '||''||Firm.TINNo " \
          ", BusinessPartner.LEGALNAME1 " \
          ", Coalesce(BusinessPartner.ADDRESSLINE1,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE2,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE4,'') " \
          "||','|| Coalesce(BusinessPartner.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(BusinessPartner.POSTALCODE,'') " \
          ", 'FROM  '||''|| portOfLoad.LONGDESCRIPTION ||',  '|| TermsOfShipping.LONGDESCRIPTION " \
          ", portOfDIS.LONGDESCRIPTION " \
          ", COUNTRY.LONGDESCRIPTION " \
          ", CountryDestn.LONGDESCRIPTION " \
          ", COALESCE(PLANTINVOICE.CONTAINERNO, '') " \
          ", TRIM(COALESCE(PLANTINVOICE.CUSTOMERBOTTLESEALNO, '')) " \
          ", COALESCE(PLANTINVOICE.BOTTLESEALNO, '') " \
          ", PLANTINVOICE.WEIGHTUMCODE " \
          ", PLANTINVOICE.GROSSWEIGHT " \
          ", PLANTINVOICE.NETTWEIGHT " \
          ", ITEMTYPE.LONGDESCRIPTION ||' (' || ITEMTYPE.CODE ||')' " \
          ", trim (Product.LONGDESCRIPTION || ' ' || COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| QualityLevel.ShortDescriptiON) " \
          ", STXN.LOTCODE " \
          ", PIL.TARIFFCODE " \
          ", PLANTINVOICE.CODE , PLANTINVOICE.INVOICEDATE " \
          ", PAYMENTMETHOD.LONGDESCRIPTION " \
          ", FIRM.DEPBENROLLMENTNO " \
          "Order   By      Company, InvoiceNo,  itmTyp, LOTNO, Item "
          # "Order By Company, INVOICENOandDt, Buyer, OrdNOandDt, itmTyp, Item "
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

        if pdfrpt.d < 130:
            pdfrpt.d = 520
            pdfrpt.c.showPage()
            pdfrpt.header(pdfrpt.divisioncode, result,pdfrpt.Yordno)

    if result == False:
        if counter > 0:

              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.c.drawString(95, pdfrpt.d,'Lot No. : ' + pdfrpt.lotno[-1])
              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.c.drawString(95, pdfrpt.d, 'HSNCODE : ' + pdfrpt.hsncode[-1])
              pdfrpt.fonts(7)

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
    pdfrpt.sr = 1
    # except:
    #       raise Exception("Please Run the Server Again ")