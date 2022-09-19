import os
from datetime import datetime

from django.shortcuts import render
from django.views.static import serve

from FormLoad import PrintProformaInv_Formload as views

from Global_Files import Connection_String as con
from PrintPDF import PrintProformaInv_PrintPDF as pdfrpt
save_name=""

Exceptions=""

counter=0


def PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate):
    global Exceptions
    sql = "Select     Comp.LONGDESCRIPTION As Company  " \
          ", 'CORP.OFF.:'||' '||COALESCE(CORP_ADDRESS.ADDRESSEE ,'') ||', '||  COALESCE(CORP_ADDRESS.ADDRESSLINE1, '') " \
          "||', '|| COALESCE(CORP_ADDRESS.ADDRESSLINE2, '') ||', '|| COALESCE(CORP_ADDRESS.ADDRESSLINE3, '') ||', '|| COALESCE(CORP_ADDRESS.ADDRESSLINE4, '') " \
          "||', '|| COALESCE(CORP_ADDRESS.ADDRESSLINE5, '') ||', '|| RTRIM(COALESCE(CORP_ADDRESS.POSTALCODE, '')) ||', '|| COALESCE(CORP_ADDRESS.TOWN, '') " \
          "||', '|| 'GSTIN:' ||' '|| '27AAACB2976M1ZB' as CorporateAdd " \
          ", 'TEL.NO. : '||' '||CORP_ADDRESS.ADDRESSPHONENUMBER as CorporatTelNo " \
          ", FACTORYGST.GSTINNUMBER as CORPGstIn " \
          ", 'Regd.Off.:'||' '||COALESCE(REGD_ADDRESS.ADDRESSEE ,'') ||', '||  COALESCE(REGD_ADDRESS.ADDRESSLINE1, '') " \
          "||', '|| COALESCE(REGD_ADDRESS.ADDRESSLINE2, '') ||', '|| COALESCE(REGD_ADDRESS.ADDRESSLINE3, '') ||', '|| COALESCE(REGD_ADDRESS.ADDRESSLINE4, '') " \
          "||', '|| COALESCE(REGD_ADDRESS.ADDRESSLINE5, '') ||', '|| RTRIM(COALESCE(REGD_ADDRESS.POSTALCODE, '')) ||', '|| COALESCE(REGD_ADDRESS.TOWN, '') " \
          "||', '|| 'GSTIN:' ||' '|| FACTORYGST.GSTINNUMBER as RegdAdd  " \
          ", FACTORYGST.GSTINNUMBER as RegdGstIn " \
          ", BP.LEGALNAME1 As Buyer " \
          ", Case When BPAdd.UNIQUEID is not null Then COALESCE(BPAdd.ADDRESSEE ,'') ||' '||  COALESCE(BPAdd.ADDRESSLINE1, '') " \
          "||' '|| COALESCE(BPAdd.ADDRESSLINE2, '') ||' '|| COALESCE(BPAdd.ADDRESSLINE3, '') ||' '|| COALESCE(BPAdd.ADDRESSLINE4, '') " \
          "||' '|| RTRIM(COALESCE(BPAdd.ADDRESSLINE5, '')) ||' '|| RTRIM(COALESCE(BPAdd.POSTALCODE, '')) ||' '|| RTRIM(COALESCE(BPAdd.TOWN, '')) " \
          "||' '|| COALESCE(BPAdd.DISTRICT, '') Else COALESCE(BP.ADDRESSLINE1, '') ||' '|| COALESCE(BP.ADDRESSLINE2, '') " \
          "||' '|| COALESCE(BP.ADDRESSLINE3, '') ||' '|| COALESCE(BP.ADDRESSLINE4, '') ||' '|| RTRIM(COALESCE(BP.ADDRESSLINE5, '')) " \
          "||' '|| RTRIM(COALESCE(BP.POSTALCODE, '')) ||' '|| RTRIM(COALESCE(BP.TOWN, '')) " \
          "||' '|| COALESCE(BP.DISTRICT, '') End As BuyerAdd " \
          ", COALESCE(NotifyBP.LEGALNAME1, BP.LEGALNAME1) as NotifyingPrty " \
          ", Case When NotifyBP.LEGALNAME1 is not null Then (Case When NotifyBPAdd.UNIQUEID is not null Then COALESCE(NotifyBPAdd.ADDRESSEE ,'') " \
          "||' '||  COALESCE(NotifyBPAdd.ADDRESSLINE1, '') ||' '|| COALESCE(NotifyBPAdd.ADDRESSLINE2, '') ||' '|| COALESCE(NotifyBPAdd.ADDRESSLINE3, '') " \
          "||' '|| COALESCE(NotifyBPAdd.ADDRESSLINE4, '') ||' '|| RTRIM(COALESCE(NotifyBPAdd.ADDRESSLINE5, '')) ||' '|| RTRIM(COALESCE(NotifyBPAdd.POSTALCODE, '')) " \
          "||' '|| RTRIM(COALESCE(NotifyBPAdd.TOWN, '')) ||' '|| COALESCE(NotifyBPAdd.DISTRICT, '') Else COALESCE(NotifyBP.ADDRESSLINE1, '') ||' '|| COALESCE(NotifyBP.ADDRESSLINE2, '') " \
          "||' '|| COALESCE(NotifyBP.ADDRESSLINE3, '') ||' '|| COALESCE(NotifyBP.ADDRESSLINE4, '') ||' '|| RTRIM(COALESCE(NotifyBP.ADDRESSLINE5, '')) " \
          "||' '|| RTRIM(COALESCE(NotifyBP.POSTALCODE, '')) ||' '|| RTRIM(COALESCE(NotifyBP.TOWN, '')) " \
          "||' '|| COALESCE(NotifyBP.DISTRICT, '') End) Else (Case When BPAdd.UNIQUEID is not null Then COALESCE(BPAdd.ADDRESSEE ,'') ||' '||  COALESCE(BPAdd.ADDRESSLINE1, '') " \
          "||' '|| COALESCE(BPAdd.ADDRESSLINE2, '') ||' '|| COALESCE(BPAdd.ADDRESSLINE3, '') ||' '|| COALESCE(BPAdd.ADDRESSLINE4, '') " \
          "||' '|| RTRIM(COALESCE(BPAdd.ADDRESSLINE5, '')) ||' '|| RTRIM(COALESCE(BPAdd.POSTALCODE, '')) ||' '|| RTRIM(COALESCE(BPAdd.TOWN, '')) " \
          "||' '|| COALESCE(BPAdd.DISTRICT, '') Else COALESCE(BP.ADDRESSLINE1, '') ||' '|| COALESCE(BP.ADDRESSLINE2, '') " \
          "||' '|| COALESCE(BP.ADDRESSLINE3, '') ||' '|| COALESCE(BP.ADDRESSLINE4, '') ||' '|| RTRIM(COALESCE(BP.ADDRESSLINE5, '')) " \
          "||' '|| RTRIM(COALESCE(BP.POSTALCODE, '')) ||' '|| RTRIM(COALESCE(BP.TOWN, '')) " \
          "||' '|| COALESCE(BP.DISTRICT, '') End) End   as NotifyingPrtyAdd " \
          ", SO.CODE As InvoiceNo " \
          ", SO.ORDERDATE As InvoiceDt " \
          ", COALESCE(VSOL.YOURREFERENCE, '') As RefNo " \
          ", COALESCE(COUNTRY.LONGDESCRIPTION, '') as CountryOfOrigin " \
          ", COALESCE(FinalDestn.LONGDESCRIPTION,Destn.LONGDESCRIPTION, '') as CountryOfDstn " \
          ", COALESCE(portLoads.LONGDESCRIPTION,portLoad.LONGDESCRIPTION, '') as PortOfLod " \
          ", COALESCE(portDiss.LONGDESCRIPTION, PortDis.LONGDESCRIPTION, '') as PortOfDis " \
          ", SO.TERMSOFDELIVERYCODE ||' '|| COALESCE(portDiss.LONGDESCRIPTION, PortDis.LONGDESCRIPTION, '') as ShipmentTerm " \
          ", CONCAT(ITEMTYPE.LONGDESCRIPTION, ' (' || ITEMTYPE.CODE  ||')') As itmTyp " \
          ", PRODUCT.LONGDESCRIPTION As Item " \
          ", 'H.S.N CODE ' ||'  '|| COALESCE(PRODUCTIE.TARIFFCODE,'') As HsnCode " \
          ", COALESCE(UGG.LONGDESCRIPTION,'') ||' - ' || COALESCE(UGG.CODE,'') as Shade " \
          ", Cast(SOL.USERPRIMARYQUANTITY AS DEcimal(20,3)) As Quantity " \
          ", '('||SOL.USERPRIMARYUOMCODE||')' as Unit " \
          ", COALESCE(Cast(SOL.PRICE AS DEcimal(20,3)),0) as Rate  " \
          ", Cast(SOL.NETVALUEINCLUDINGTAX AS DEcimal(20,2)) As Amount " \
          ", SO.CURRENCYCODE As CURRENCY " \
          ", (SELECT COALESCE(CAST(Sum(IndTaxDetail.VALUE) AS DECIMAL(20,2)),0.00) FROM IndTaxDetail " \
          "JOIN ITax               ON     IndTaxDetail.ITaxCode    = Itax.Code " \
          "WHERE (IndTaxDetail.TaxCategoryCode IN('FRT') Or (Itax.Code = 'GFR')) " \
          "AND INDTAXDETAIL.AbsUniqueID = SO.AbsUniqueID) As FreighttValue " \
          ", (SELECT COALESCE(CAST(Sum(IndTaxDetail.VALUE) AS DECIMAL(20,2)),0.00) FROM IndTaxDetail " \
          "JOIN ITax               ON     IndTaxDetail.ITaxCode    = Itax.Code " \
          "WHERE (IndTaxDetail.TaxCategoryCode IN('INS') Or (ITax.TaxCategoryCode = 'GIN')) " \
          "AND INDTAXDETAIL.AbsUniqueID = SO.AbsUniqueID) As Insurance " \
          ", CAST(SO.ONORDERTOTALAMOUNT - (SELECT Sum(IndTaxDetail.VALUE) FROM IndTaxDetail " \
          "JOIN ITax               ON     IndTaxDetail.ITaxCode    = Itax.Code " \
          "WHERE (IndTaxDetail.TaxCategoryCode IN('FRT','INS') Or (ITax.TaxCategoryCode = 'GIN' And Itax.Code = 'GFR')) " \
          "AND INDTAXDETAIL.AbsUniqueID = SO.AbsUniqueID) AS DECIMAL(20,2)) AS FobValue " \
          ", 'PAYMENT :' ||' '||PAYMENTMETHOD.LONGDESCRIPTION As PAYMENTMET " \
          ", COALESCE(VARCHAR(NOTE.NOTE),'') as Remarks  " \
          ", 'BENEFICIARY : '||' '||COMPANYBANK.ACCOUNTOWNER AS COMPACOWNER " \
          ", 'ACCOUNT : ' ||' '|| COMPANYBANK.CURRENTACCOUNTID AS COMACNO " \
          ", 'COMPANY BANK: '||' '|| COALESCE(SoCompBank.LONGDESCRIPTION ||'  '|| SoCompBank.BANKBRANCHADDRESS , BANK.LONGDESCRIPTION " \
          "||'  '|| BANK.BANKBRANCHADDRESS) As COMPANYBANK " \
          ", 'SWIFT CODE : '||' '|| COALESCE(SoCompBank.BIC, BANK.BIC) As COMPSWFTCD " \
          ", PartnerBank.LONGDESCRIPTION ||'  '|| PartnerBank.BANKBRANCHADDRESS As ParnerBnk " \
          ", 'SWIFT CODE : ' ||' '|| PartnerBank.BIC As SwftCode " \
          "From    SALESORDER SO  " \
          "Join DIVISION                           On      SO.DIVISIONCODE = DIVISION.CODE " \
          "JOIN ADDRESS CORP_ADDRESS               ON      Division.AbsUniqueId = CORP_ADDRESS.UniqueId " \
          "And     CORP_ADDRESS.Code = 'CORP' " \
          "JOIN ADDRESS REGD_ADDRESS               ON      Division.AbsUniqueId = REGD_ADDRESS.UniqueId " \
          "And     REGD_ADDRESS.Code = 'REGD' " \
          "Join ORDERPARTNER OP                    On      SO.ORDPRNCUSTOMERSUPPLIERCODE = OP.CUSTOMERSUPPLIERCODE " \
          "And     OP.CUSTOMERSUPPLIERTYPE = 1 " \
          "Join BUSINESSPARTNER BP                 On      OP.ORDERBUSINESSPARTNERNUMBERID = BP.NUMBERID " \
          "Join ORDERPARTNERIE OPIE                On      SO.ORDPRNCUSTOMERSUPPLIERCODE = OPIE.CUSTOMERSUPPLIERCODE " \
          "And     OPIE.CUSTOMERSUPPLIERTYPE = 1 " \
          "Left Join PORT  PortLoad                On      OPIE.PORTOFLOADINGCODE = PortLoad.CODE " \
          "Left Join PORT  PortDis                 On      OPIE.PORTOFDISCHARGECODE = PortDis.CODE " \
          "Join COUNTRY Destn                      On      BP.COUNTRYCODE = Destn.CODE " \
          "Left Join ADSTORAGE ADSFinalDst         On      SO.AbsUniqueId = ADSFinalDst.UNIQUEID " \
          "And     ADSFinalDst.NameEntityName = 'SalesOrder' " \
          "And     ADSFinalDst.NAmeName ='Countryoffinaldestination' " \
          "And     ADSFinalDst.FieldName = 'CountryoffinaldestinationCode' " \
          "Left Join COUNTRY FinalDestn            On      ADSFinalDst.VALUESTRING = FinalDestn.CODE " \
          "Left Join ADDRESS BPAdd                 On      SO.DELIVERYPOINTUNIQUEID = BPAdd.UNIQUEID " \
          "And     SO.DELIVERYPOINTCODE = BPAdd.CODE " \
          "Left Join ADSTORAGE                     On      SO.AbsUniqueId = ADSTORAGE.UNIQUEID " \
          "And     ADSTORAGE.NameEntityName = 'SalesOrder' " \
          "And     ADSTORAGE.NAmeName ='NotifyParty1' " \
          "And     ADSTORAGE.FieldName = 'NotifyParty1Code' " \
          "Left Join ORDERPARTNER notifyOP         On      ADSTORAGE.VALUESTRING = notifyOP.CUSTOMERSUPPLIERCODE " \
          "And     notifyOP.CUSTOMERSUPPLIERTYPE = 1 " \
          "Left Join BUSINESSPARTNER NotifyBP   On      notifyOP.ORDERBUSINESSPARTNERNUMBERID = NotifyBP.NUMBERID " \
          "Left Join ADDRESS NotifyBPAdd                 On      SO.DELIVERYPOINTUNIQUEID = NotifyBPAdd.UNIQUEID " \
          "And     SO.DELIVERYPOINTCODE = NotifyBPAdd.CODE " \
          "Left Join ADSTORAGE  ADSportLoad        On      SO.AbsUniqueId = ADSportLoad.UNIQUEID " \
          "And     ADSportLoad.NameEntityName = 'SalesOrder' " \
          "And     ADSportLoad.NAmeName ='Port' " \
          "And     ADSportLoad.FieldName = 'PortCode' " \
          "Left Join  Port  portLoads              On      ADSportLoad.VALUESTRING = portLoads.CODE " \
          "Left Join ADSTORAGE  ADSportDis         On      SO.AbsUniqueId = ADSportDis.UNIQUEID " \
          "And     ADSportDis.NameEntityName = 'SalesOrder' " \
          "And     ADSportDis.NAmeName ='Ports' " \
          "And     ADSportDis.FieldName = 'PortsCode' " \
          "Left Join  Port  portDiss               On      ADSportDis.VALUESTRING = portDiss.CODE " \
          "Join PAYMENTMETHOD                      On      SO.PAYMENTMETHODCODE = PAYMENTMETHOD.CODE " \
          "Left JOIN COMPANYBANK                   ON	   SO.COMPANYCODE = COMPANYBANK.COMPANYCODE " \
          "And      SO.COMPANYBANKIDIDENTIFIER = COMPANYBANK.IDENTIFIER " \
          "left Join Bank                          ON      CompanyBank.BANKBANKCOUNTRYCODE = Bank.BANKCOUNTRYCODE " \
          "And     CompanyBank.BANKCODE = Bank.CODE " \
          "AND     CompanyBank.BankBranchCode = Bank.BranchCode " \
          "Left Join BANK SoCompBank               ON      SO.COMPANYBANKBANKCOUNTRYCODE = SoCompBank.BANKCOUNTRYCODE " \
          "AND     SO.COMPANYBANKCODE = SoCompBank.CODE " \
          "AND     SO.COMPANYBANKBRANCHCODE = SoCompBank.BranchCode " \
          "Left Join Bank PartnerBank              On      SO.BANKBANKCOUNTRYCODE = PartnerBank.BANKCOUNTRYCODE " \
          "AND     SO.BANKCODE = PartnerBank.CODE " \
          "AND     SO.BANKBRANCHCODE = PartnerBank.BranchCode " \
          "Join SALESORDERLINE SOL                 On      SO.CODE = SOL.SALESORDERCODE " \
          "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE " \
          "And     SO.DOCUMENTTYPETYPE = SOL.DOCUMENTTYPETYPE " \
          "Join LOGICALWAREHOUSE                   On      SOL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Join BUSINESSUNITVSCOMPANY BUC          On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE  " \
          "Join FINBUSINESSUNIT                    On      BUC.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "And     FINBUSINESSUNIT.GROUPFLAG = 0 " \
          "Join FINBUSINESSUNIT Comp               On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
          "And     Comp.GROUPFLAG = 1  " \
          "Join PLANT                              On      BUC.FACTORYCODE = PLANT.CODE " \
          "Join FACTORY                            On      BUC.FACTORYCODE = FACTORY.CODE " \
          "Join ADDRESSGST FACTORYGST              On      FACTORY.ABSUNIQUEID = FACTORYGST.UNIQUEID " \
          "Join COUNTRY                            On      PLANT.COUNTRYCODE = COUNTRY.CODE " \
          "Join ITEMTYPE                           On      SOL.ITEMTYPEAFICODE = ITEMTYPE.CODE " \
          "join FULLITEMKEYDECODER FIKD            ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')  " \
          "AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join PRODUCT                            On      SOL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
          "Join PRODUCTIE                          ON      PRODUCT.ITEMTYPECODE = PRODUCTIE.ITEMTYPECODE  " \
          "AND     COALESCE(PRODUCT.SubCode01, '') = COALESCE(PRODUCTIE.SubCode01, '') " \
          "AND     COALESCE(PRODUCT.SubCode02, '') = COALESCE(PRODUCTIE.SubCode02, '') " \
          "AND     COALESCE(PRODUCT.SubCode03, '') = COALESCE(PRODUCTIE.SubCode03, '') " \
          "AND     COALESCE(PRODUCT.SubCode04, '') = COALESCE(PRODUCTIE.SubCode04, '') " \
          "AND     COALESCE(PRODUCT.SubCode05, '') = COALESCE(PRODUCTIE.SubCode05, '') " \
          "AND     COALESCE(PRODUCT.SubCode06, '') = COALESCE(PRODUCTIE.SubCode06, '') " \
          "AND     COALESCE(PRODUCT.SubCode07, '') = COALESCE(PRODUCTIE.SubCode07, '') " \
          "AND     COALESCE(PRODUCT.SubCode08, '') = COALESCE(PRODUCTIE.SubCode08, '') " \
          "AND     COALESCE(PRODUCT.SubCode09, '') = COALESCE(PRODUCTIE.SubCode09, '') " \
          "AND     COALESCE(PRODUCT.SubCode10, '') = COALESCE(PRODUCTIE.SubCode10, '') " \
          "Left JOIN ItemSubcodeTemplate IST       ON      SOL.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN USERGENERICGROUP UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then SOL.SUBCODE01 When 2 Then SOL.SUBCODE02 When 3 Then SOL.SUBCODE03 When 4 Then SOL.SUBCODE04 When 5 Then SOL.SUBCODE05 " \
          "When 6 Then SOL.SUBCODE06 When 7 Then SOL.SUBCODE07 When 8 Then SOL.SUBCODE08 When 9 Then SOL.SUBCODE09 When 10 Then SOL.SUBCODE10 End = UGG.Code  " \
          "Join VIEWSALESORDERLINE VSOL            On      SO.CODE =VSOL.SALESORDERCODE " \
          "And     SO.COUNTERCODE = VSOL.SALESORDERCOUNTERCODE " \
          "And     SOL.ORDERLINE = VSOL.ORDERLINE  " \
          "Left Join NOTE                          On      SO.ABSUNIQUEID = NOTE.FATHERID " \
          "Where "+InvoiceNos+" " \
          "Order By Company, InvoiceNo,Buyer, itmTyp, Item, SOL.ORDERLINE "

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

        if pdfrpt.d < 250:
            pdfrpt.d = 520
            pdfrpt.c.showPage()
            pdfrpt.header(pdfrpt.divisioncode, result)

    if result == False:
        if counter > 0:

              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.c.drawCentredString(80, pdfrpt.d, pdfrpt.hsncode[-1])
              pdfrpt.boldfonts(8)
              # pdfrpt.c.drawAlignedString(470, 190, "Total")
              pdfrpt.c.drawAlignedString(560, 190, str('{0:1.2f}'.format(pdfrpt.amount)))
              pdfrpt.c.drawAlignedString(560, 70, 'For ' + pdfrpt.divisioncode[-1])
              pdfrpt.c.drawAlignedString(560, 20, "Authorised  Signatory")
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