import os
from datetime import datetime

from django.shortcuts import render
from django.views.static import serve

from FormLoad import PrintProformaInv_Formload as views

from Global_Files import Connection_String as con
from PrintPDF import PrintProformaCommercial_PrintPDF as pdfrpt
save_name=""

Exceptions=""

counter=0


def PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate):
    global Exceptions
    sql = "SELECT Comp.LONGDESCRIPTION As Company " \
          ", 'FACTORY: '||' '|| Coalesce(PLANT.addressline1,'') " \
          "|| Coalesce(','||PLANT.addressline2,'') " \
          "|| Coalesce(','||PLANT.addressline3,'') " \
          "|| Coalesce(','||PLANT.addressline4,'') " \
          "|| Coalesce(','||PLANT.addressline5,'') " \
          "|| RTRIM(Coalesce(','||PLANT.postalcode,'')) ||'   GSTIN : '|| ADGSTIN.GSTINNUMBER AS Fac_ADDRESS " \
          ", 'REGD. OFF: '||' '||Coalesce(REGD_ADDRESS.ADDRESSEE,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline1,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline2,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline3,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline4,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline5,'') " \
          "|| Coalesce(','||REGD_ADDRESS.postalcode,'') AS REGD_ADDRESS " \
          ", 'CIN: '||''||Firm.TINNo AS CINNO " \
          ", 'CORP. OFF: '||' '||Coalesce(CORP_ADDRESS.ADDRESSEE,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline1,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline2,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline3,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline4,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline5,'') " \
          "|| Coalesce(','||CORP_ADDRESS.postalcode,'') AS CORP_ADDRESS " \
          ", 'GSTIN : 27AAACB2976M1ZB ' As CORP_GSTIN " \
          ", 'TAX ID NO.: '||''||FIRM.PANNO As TAXID " \
          ", 'IEC.NO.: ' ||''||Firm.IECODE As IecNo " \
          ", COALESCE(BP_CONsig.LEGALNAME1,'') AS CONSIGNEEname " \
          ", CASE When ADDRESS_CONsignee.UNIQUEID is Not Null Then Coalesce(ADDRESS_CONsignee.ADDRESSEE,'') " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE1,'') " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE2,'')  " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE3,'') " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE4,'') " \
          "||','|| Coalesce(ADDRESS_CONsignee.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(ADDRESS_CONsignee.POSTALCODE,'') " \
          "Else Coalesce(BP_CONsig.ADDRESSLINE1,'') " \
          "|| Coalesce(','||BP_CONsig.ADDRESSLINE2,'') " \
          "|| Coalesce(','||BP_CONsig.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BP_CONsig.ADDRESSLINE4,'') " \
          "||','|| Coalesce(BP_CONsig.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(BP_CONsig.POSTALCODE,'') End  as CONSIGNEEADDRESS " \
          ", BusinessPartner.LEGALNAME1 AS Buyer " \
          ", Coalesce(BusinessPartner.ADDRESSLINE1,'')  " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE2,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE4,'') " \
          "||','|| Coalesce(BusinessPartner.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(BusinessPartner.POSTALCODE,'') as BuyerAddress " \
          ", COALESCE(BP_NotifyPrty.LEGALNAME1,'') AS NotifyPrtyname " \
          ", CASE When ADDRESS_NotifyPrty.UNIQUEID is Not Null Then Coalesce(ADDRESS_NotifyPrty.ADDRESSEE,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE1,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE2,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE3,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE4,'') " \
          "||','|| Coalesce(ADDRESS_NotifyPrty.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(ADDRESS_NotifyPrty.POSTALCODE,'') " \
          "Else Coalesce(BP_NotifyPrty.ADDRESSLINE1,'')  " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE2,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE4,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE5,'') " \
          "|| Coalesce(',Postal Code : ' || BP_NotifyPrty.POSTALCODE,'') End  as NotifyPrtyADDRESS " \
          ", TermsOfShipping.LONGDESCRIPTION AS TermsOfDelv " \
          ", PAYMENTMETHOD.LONGDESCRIPTION As Payment " \
          ", CountryOrgnGoods.LONGDESCRIPTION as CountryOfOriginOfGoods " \
          ", CountryDestn.LONGDESCRIPTION as CountryOfDestn	 " \
          ", portOfLoad.LONGDESCRIPTION  As PortOfLoading " \
          ", portOfDIS.LONGDESCRIPTION As PortOfDischarge " \
          ", finalDstn.LONGDESCRIPTION As FinalDestination " \
          ", COALESCE(COMMERCIALINVOICE.VESSELFLIGHTNO,'') As VesselFlightNo " \
          ", COALESCE(PLANTINVOICE.BLNUMBER,'') AS BlNo " \
          ", COALESCE(Varchar_FORMAT(PLANTINVOICE.BLDATE,'DD-MM-YYYY'),'') AS BlDt  " \
          ", Coalesce(EXPORTSHIPPING.CODE,'') As SBNo " \
          ", COALESCE(VARCHAR_FORMAT(EXPORTSHIPPING.SHIPPINGBILLDATE,'DD-MM-YYYY'),'') As SbDt  " \
          ", COALESCE(PLANTINVOICE.CONTAINERSIZE, '') As ContSize " \
          ", COALESCE(COMMERCIALINVOICE.CONTAINERNO, '') As ContNO " \
          ", TRIM(COALESCE(PlantInvoice.CUSTOMERBOTTLESEALNO, '')) As SealNo " \
          ", COALESCE(PlantInvoice.BOTTLESEALNO, '') As ESealNo " \
          ", CAST(CIL.WIDTH AS INT) As Measure " \
          ", COMMERCIALINVOICE.TOTALNUMBEROFBALES As Packages " \
          ", ITEMTYPE.LONGDESCRIPTION ||' (' || ITEMTYPE.CODE ||')' As ItmTyp " \
          ", trim (Product.LONGDESCRIPTION || ' ' || COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| QualityLevel.ShortDescriptiON) AS ITEM " \
          ", CIL.TARIFFCODE AS HSNCODE " \
          ", COMMERCIALINVOICE.CODE ||'  DT:   '|| VARCHAR_FORMAT(COMMERCIALINVOICE.INVOICEDATE,'DD-MM-YYYY') As InvoiceNoAndDt " \
          ", PLANTINVOICE.CODE AS INVOICENO " \
          ", PLANTINVOICE.INVOICEDATE AS INVOICEDt " \
          ", COMMERCIALINVOICE.CONTRACTNOCODE||'  DT:   '|| VARCHAR_FORMAT(COMMERCIALINVOICE.CONTRACTDATE,'DD-MM-YYYY') As OrdNoAndDt " \
          ", STXN.LOTCODE As LotNo " \
          ", COALESCE(BKLELEMENTS.ACTUALUNITCODE,'') As WtUnit " \
          ", CAST((SUM(BKLELEMENTS.ACTUALGROSSWT )) As DECIMAL(10,3)) As GROSSWt " \
          ", CAST((SUM(BKLELEMENTS.ACTUALNETWT)) As DECIMAL(10,3)) As NetWt " \
          ", CAST((Count(stxn.TRANSACTIONNUMBER)) As INT) As Boxes " \
          ", COUNTRY.LONGDESCRIPTION as CountryOfOrigin " \
          ", CIL.NUMBEROFBALES As  ItmPackages " \
          ", PlantInvoice.CATEGORY As MasterExpNo " \
          ", PlantInvoice.INVOICEDATE As MasterExpDt " \
          ", Cast(CIL.PRIMARYQTY As Decimal(20,3)) As Quantity " \
          ", CIL.PRIMARYUMCODE As UNIT " \
          ", CAST(SDL.PRICE AS DECIMAL(10, 3)) As Rate " \
          ", COMMERCIALINVOICE.INVOICECURRENCYCODE AS CURRENCY " \
          ", CAST(CIL.BASICVALUE As DECIMAL(20,4)) As AMOUNT " \
          ", COMMERCIALINVOICE.EXCHANGERATEOFCONTRACT As ExRate " \
          ", Sum(IndTax.CalculatedValue) As GstInvValueINR " \
          ", Sum(IndTax.Value) As GSTinINR " \
          ", Cast(EXPORTSHIPPING.FOBVALUEFC As Decimal(20,2)) As FobValue " \
          ", Cast(EXPORTSHIPPING.FREIGHTAMTFC + EXPORTSHIPPING.DISCOUNTAMTFC + EXPORTSHIPPING.PACKINGAMTFC + EXPORTSHIPPING.OTHERDEDUCTIONAMTFC + " \
          "EXPORTSHIPPING.COMMISSIONAMTFC As Decimal(20,2)) As Freight " \
          ", CAST(EXPORTSHIPPING.INSURANCEAMTFC AS DECIMAL(20,2)) As insurance " \
          ", CAST(EXPORTSHIPPING.FOBVALUEFC + EXPORTSHIPPING.FREIGHTAMTFC + EXPORTSHIPPING.DISCOUNTAMTFC + EXPORTSHIPPING.PACKINGAMTFC + EXPORTSHIPPING.OTHERDEDUCTIONAMTFC + " \
          "EXPORTSHIPPING.COMMISSIONAMTFC  AS DECIMAL(20,2)) As CfrValue " \
          ", CAST(EXPORTSHIPPING.FOBVALUEFC + EXPORTSHIPPING.FREIGHTAMTFC + EXPORTSHIPPING.DISCOUNTAMTFC + EXPORTSHIPPING.PACKINGAMTFC + EXPORTSHIPPING.OTHERDEDUCTIONAMTFC + " \
          "EXPORTSHIPPING.COMMISSIONAMTFC + EXPORTSHIPPING.INSURANCEAMTFC AS DECIMAL(20,3)) As CifValue " \
          ", 'BENEFICIARY : '||' '||COMPANYBANK.ACCOUNTOWNER AS COMPACOWNER " \
          ", 'ACCOUNT : ' ||' '|| COMPANYBANK.CURRENTACCOUNTID AS COMACNO " \
          ", 'COMPANY BANK: '||' '||BANK.LONGDESCRIPTION ||'  '|| BANK.BANKBRANCHADDRESS As COMPANYBANK " \
          ", 'SWIFT CODE : '||' '|| BANK.BIC As COMPSWFTCD " \
          ", PartnerBank.LONGDESCRIPTION ||'  '|| PartnerBank.BANKBRANCHADDRESS As ParnerBnk " \
          ", 'SWIFT CODE : ' ||' '|| PartnerBank.BIC As SwftCode " \
          "From PlantInvoice " \
          "JOIN COMMERCIALINVOICELINE  CIL         ON 	PlantInvoice.CODE = CIL.PLANTINVOICECODE " \
          "Join ITEMTYPE                           ON      CIL.ITEMTYPECODE = ITEMTYPE.CODE " \
          "JOIN FullItemKeyDecoder FIKD            ON      CIL.ITEMTYPECODE = FIKD.ITEMTYPECODE  " \
          "AND     COALESCE(CIL.SubCode1, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(CIL.SubCode2, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(CIL.SubCode3, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(CIL.SubCode4, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(CIL.SubCode5, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(CIL.SubCode6, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(CIL.SubCode7, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(CIL.SubCode8, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(CIL.SubCode9, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(CIL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join Product                            ON      CIL.ITEMTYPECODE  = Product.ITEMTYPECODE " \
          "AND     FIKD.ItemUniqueId   = Product.AbsUniqueId " \
          "Left JOIN ItemSubcodeTemplate IST       ON      CIL.ITEMTYPECODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN USERGENERICGROUP UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then CIL.SubCode1 When 2 Then CIL.SubCode2 When 3 Then CIL.SubCode3 When 4 Then CIL.SubCode4 When 5 Then CIL.SubCode5 " \
          "When 6 Then CIL.SubCode6 When 7 Then CIL.SubCode7 When 8 Then CIL.SubCode8 When 9 Then CIL.SubCode9 When 10 Then CIL.SUBCODE10 End = UGG.Code " \
          "JOIN QUALITYLEVEL                       ON      CIL.QUALITYLEVELCODE = QUALITYLEVEL.CODE " \
          "AND     CIL.ITEMTYPECODE = QUALITYLEVEL.ITEMTYPECODE " \
          "Join LOGICALWAREHOUSE                   On      CIL.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Join BUSINESSUNITVSCOMPANY BUC          On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE " \
          "Join FINBUSINESSUNIT                    On      BUC.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "And     FINBUSINESSUNIT.GROUPFLAG = 0 " \
          "Join FINBUSINESSUNIT Comp               On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
          "And     Comp.GROUPFLAG = 1 " \
          "JOIN PLANT                              ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE " \
          "JOIN FACTORY                            ON      PLANT.CODE = FACTORY.CODE " \
          "LEFT JOIN ADDRESSGST ADGSTIN            ON      FACTORY.ABSUNIQUEID = ADGSTIN.UNIQUEID " \
          "Join COUNTRY                            On      PLANT.COUNTRYCODE = COUNTRY.CODE	" \
          "JOIN SALESDOCUMENTLINE SDL              ON      CIL.PLANTINVOICECODE = SDL.SALESDOCUMENTPROVISIONALCODE " \
          "AND     CIL.ITEMTYPECODE = SDL.ITEMTYPEAFICODE  " \
          "AND     COALESCE(CIL.SubCode1, '') = COALESCE(SDL.SubCode01, '')  " \
          "AND     COALESCE(CIL.SubCode2, '') = COALESCE(SDL.SubCode02, '')  " \
          "AND     COALESCE(CIL.SubCode3, '') = COALESCE(SDL.SubCode03, '')  " \
          "AND     COALESCE(CIL.SubCode4, '') = COALESCE(SDL.SubCode04, '')  " \
          "AND     COALESCE(CIL.SubCode5, '') = COALESCE(SDL.SubCode05, '')  " \
          "AND     COALESCE(CIL.SubCode6, '') = COALESCE(SDL.SubCode06, '')  " \
          "AND     COALESCE(CIL.SubCode7, '') = COALESCE(SDL.SubCode07, '')  " \
          "AND     COALESCE(CIL.SubCode8, '') = COALESCE(SDL.SubCode08, '')  " \
          "AND     COALESCE(CIL.SubCode9, '') = COALESCE(SDL.SubCode09, '')  " \
          "AND     COALESCE(CIL.SubCode10, '') = COALESCE(SDL.SubCode10, '') " \
          "AND     CIL.QUALITYLEVELCODE = SDL.QUALITYCODE " \
          "JOIN SALESDOCUMENT SD   		ON      SDL.SALESDOCUMENTPROVISIONALCODE = SD.PROVISIONALCODE " \
          "AND 	SD.DocumentTypeType = '06' " \
          "AND     SDL.SALDOCPROVISIONALCOUNTERCODE = SD.PROVISIONALCOUNTERCODE " \
          "Join STOCKTRANSACTION STXN              On      SDL.PREVIOUSCODE = STXN.ORDERCODE " \
          "AND     SDL.PREVIOUSCOUNTERCODE = STXN.ORDERCOUNTERCODE " \
          "AND     SDL.PREVIOUSORDERLINE = STXN.ORDERLINE " \
          "LEFT JOIN BKLELEMENTS                        ON      STXN.CONTAINERELEMENTCODE = BKLELEMENTS.CODE " \
          "Left JOIN IndTaxDetail IndTax           ON      CIL.AbsUniqueID = IndTax.AbsUniqueID " \
          "AND     IndTax.TaxCategoryCode = 'GST' " \
          "Join COMMERCIALINVOICE                  ON 	CIL.COMMERCIALINVOICECODE = COMMERCIALINVOICE.CODE " \
          "AND 	CIL.COMMERCIALINVOICEDIVISIONCODE = COMMERCIALINVOICE.DIVISIONCODE " \
          "join OrderPartner                       ON      COMMERCIALINVOICE.BUYERIFOTCCUSTOMERSUPPLIERCODE = OrderPartner.CustomerSupplierCode " \
          "AND     COMMERCIALINVOICE.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OrderPartner.CustomerSupplierType " \
          "join BusinessPartner                    ON      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID  " \
          "Left join OrderPartner OP_CONsig        ON      COMMERCIALINVOICE.CONSIGNEECUSTOMERSUPPLIERCODE = OP_CONsig.CustomerSupplierCode " \
          "AND     COMMERCIALINVOICE.CONSIGNEECUSTOMERSUPPLIERTYPE = OP_CONsig.CustomerSupplierType " \
          "Left join BusinessPartner BP_CONsig     ON      OP_CONsig.OrderbusinessPartnerNumberId 	= BP_CONsig.NumberID " \
          "LEFT JOIN Address ADDRESS_CONsignee     ON      BP_CONsig.ABSUNIQUEID = ADDRESS_CONsignee.UNIQUEID " \
          "AND     COMMERCIALINVOICE.DELIVERYPOINTCODE = ADDRESS_CONsignee.CODE " \
          "Left Join OrderPartner OP_NotifyPrty    On      COMMERCIALINVOICE.NOTIFYPARTYCSMSUPPLIERCODE = OP_NotifyPrty.CustomerSupplierCode " \
          "AND     COMMERCIALINVOICE.NOTIFYPARTYCSMSUPPLIERTYPE = OP_NotifyPrty.CustomerSupplierType " \
          "Left join BusinessPartner BP_NotifyPrty ON      OP_NotifyPrty.OrderbusinessPartnerNumberId 	= BP_NotifyPrty.NumberID " \
          "LEFT JOIN Address ADDRESS_NotifyPrty    ON      BP_NotifyPrty.ABSUNIQUEID = ADDRESS_NotifyPrty.UNIQUEID " \
          "AND     COMMERCIALINVOICE.DELIVERYPOINTCODE = ADDRESS_NotifyPrty.CODE " \
          "Join PAYMENTMETHOD                      On      COMMERCIALINVOICE.TERMSOFPAYMENTCODE = PAYMENTMETHOD.CODE " \
          "Left Join COUNTRY CountryDestn          On      COMMERCIALINVOICE.DESTINATIONCOUNTRYCODE = CountryDestn.CODE " \
          "Left Join COUNTRY CountryOrgnGoods      On      COMMERCIALINVOICE.GOODSORIGINCOUNTRYCODE = CountryOrgnGoods.CODE " \
          "Left Join PORT portOfLoad               On      COMMERCIALINVOICE.PORTOFLOADINGCODE = portOfLoad.CODE " \
          "Left Join PORT portOfDIS                On      COMMERCIALINVOICE.PORTOFDISCHARGECODE = portOfDIS.CODE " \
          "Left Join DESTINATION finalDstn         On      COMMERCIALINVOICE.FINALDESTINATIONCODE = finalDstn.CODE  " \
          "JOIN TermsOfShipping                    ON      COMMERCIALINVOICE.TERMSOFSHIPPINGCODE = TermsOfShipping.CODE " \
          "JOIN FIRM                               ON      COMMERCIALINVOICE.DIVISIONCODE = FIRM.CODE " \
          "JOIN DIVISION                           ON 	COMMERCIALINVOICE.DIVISIONCODE = DIVISION.CODE " \
          "JOIN ADDRESS REGD_ADDRESS               ON 	DivisiON.AbsUniqueId = REGD_ADDRESS.UniqueId " \
          "AND 	REGD_ADDRESS.Code = 'REGD' " \
          "JOIN ADDRESS CORP_ADDRESS               ON 	DivisiON.AbsUniqueId = CORP_ADDRESS.UniqueId " \
          "AND 	CORP_ADDRESS.Code = 'CORP' " \
          "Left JOIN COMPANYBANK                        ON	COMMERCIALINVOICE.COMPANYCODE = COMPANYBANK.COMPANYCODE " \
          "Left JOIN BANK                          ON      COMPANYBANK.BANKCODE = BANK.CODE " \
          "AND     CompanyBank.BankBranchCode = Bank.BranchCode " \
          "Left Join BANK PartnerBank              ON      COMMERCIALINVOICE.BUYERSBANKBRANCHCODE = PartnerBank.BRANCHCODE " \
          "AND     COMMERCIALINVOICE.BUYERSBANKCODE = PartnerBank.CODE " \
          "Left Join EXPORTSHIPPING                On      COMMERCIALINVOICE.EXPORTSHIPPINGBILLCODE = EXPORTSHIPPING.CODE " \
          "Where "+InvoiceNos+" " \
          "Group By Comp.LONGDESCRIPTION " \
          ", 'FACTORY: '||' '|| Coalesce(PLANT.addressline1,'') " \
          "|| Coalesce(','||PLANT.addressline2,'') " \
          "|| Coalesce(','||PLANT.addressline3,'') " \
          "|| Coalesce(','||PLANT.addressline4,'') " \
          "|| Coalesce(','||PLANT.addressline5,'')  " \
          "|| RTRIM(Coalesce(','||PLANT.postalcode,'')) ||'   GSTIN : '|| ADGSTIN.GSTINNUMBER " \
          ", 'REGD. OFF: '||' '||Coalesce(REGD_ADDRESS.ADDRESSEE,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline1,'')  " \
          "|| Coalesce(','||REGD_ADDRESS.addressline2,'')  " \
          "|| Coalesce(','||REGD_ADDRESS.addressline3,'')  " \
          "|| Coalesce(','||REGD_ADDRESS.addressline4,'')  " \
          "|| Coalesce(','||REGD_ADDRESS.addressline5,'')  " \
          "|| Coalesce(','||REGD_ADDRESS.postalcode,'') " \
          ", 'CIN: '||''||Firm.TINNo " \
          ", 'CORP. OFF: '||' '||Coalesce(CORP_ADDRESS.ADDRESSEE,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline1,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline2,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline3,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline4,'') " \
          "|| Coalesce(','||CORP_ADDRESS.addressline5,'') " \
          "|| Coalesce(','||CORP_ADDRESS.postalcode,'') " \
          ", 'GSTIN : 27AAACB2976M1ZB ' " \
          ", 'TAX ID NO.: '||''||FIRM.PANNO " \
          ", 'IEC.NO.: ' ||''||Firm.IECODE " \
          ", COALESCE(BP_CONsig.LEGALNAME1,'') " \
          ", CASE When ADDRESS_CONsignee.UNIQUEID is Not Null Then Coalesce(ADDRESS_CONsignee.ADDRESSEE,'') " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE1,'') " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE2,'')  " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE3,'') " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE4,'') " \
          "||','|| Coalesce(ADDRESS_CONsignee.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(ADDRESS_CONsignee.POSTALCODE,'') " \
          "Else Coalesce(BP_CONsig.ADDRESSLINE1,'')  " \
          "|| Coalesce(','||BP_CONsig.ADDRESSLINE2,'') " \
          "|| Coalesce(','||BP_CONsig.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BP_CONsig.ADDRESSLINE4,'') " \
          "||','|| Coalesce(BP_CONsig.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(BP_CONsig.POSTALCODE,'') End " \
          ", BusinessPartner.LEGALNAME1 " \
          ", Coalesce(BusinessPartner.ADDRESSLINE1,'')   " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE2,'')   " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE3,'')  " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE4,'')  " \
          "||','|| Coalesce(BusinessPartner.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(BusinessPartner.POSTALCODE,'') " \
          ", COALESCE(BP_NotifyPrty.LEGALNAME1,'') " \
          ", CASE When ADDRESS_NotifyPrty.UNIQUEID is Not Null Then Coalesce(ADDRESS_NotifyPrty.ADDRESSEE,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE1,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE2,'')  " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE3,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE4,'') " \
          "||','|| Coalesce(ADDRESS_NotifyPrty.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(ADDRESS_NotifyPrty.POSTALCODE,'') " \
          "Else Coalesce(BP_NotifyPrty.ADDRESSLINE1,'')  " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE2,'')  " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE4,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE5,'')" \
          "|| Coalesce(',Postal Code : ' || BP_NotifyPrty.POSTALCODE,'') End " \
          ", TermsOfShipping.LONGDESCRIPTION  " \
          ", PAYMENTMETHOD.LONGDESCRIPTION  " \
          ", CountryOrgnGoods.LONGDESCRIPTION  " \
          ", CountryDestn.LONGDESCRIPTION  " \
          ", portOfLoad.LONGDESCRIPTION " \
          ", portOfDIS.LONGDESCRIPTION  " \
          ", finalDstn.LONGDESCRIPTION  " \
          ", COALESCE(COMMERCIALINVOICE.VESSELFLIGHTNO,'')  " \
          ", COALESCE(PLANTINVOICE.BLNUMBER,'')  " \
          ", COALESCE(Varchar_FORMAT(PLANTINVOICE.BLDATE,'DD-MM-YYYY'),'')  " \
          ", EXPORTSHIPPING.CODE " \
          ", EXPORTSHIPPING.SHIPPINGBILLDATE " \
          ", COALESCE(PlantInvoice.CONTAINERSIZE, '') " \
          ", COALESCE(COMMERCIALINVOICE.CONTAINERNO, '') " \
          ", TRIM(COALESCE(PlantInvoice.CUSTOMERBOTTLESEALNO, '')) " \
          ", COALESCE(PlantInvoice.BOTTLESEALNO, '') " \
          ", COMMERCIALINVOICE.TOTALNUMBEROFBALES " \
          ", ITEMTYPE.LONGDESCRIPTION ||' (' || ITEMTYPE.CODE ||')' " \
          ", trim (Product.LONGDESCRIPTION || ' ' || COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| QualityLevel.ShortDescriptiON) " \
          ", CIL.TARIFFCODE " \
          ", COMMERCIALINVOICE.CODE, COMMERCIALINVOICE.INVOICEDATE " \
          ", PLANTINVOICE.CODE " \
          ", PLANTINVOICE.INVOICEDATE " \
          ", STXN.LOTCODE " \
          ", COUNTRY.LONGDESCRIPTION " \
          ", CIL.NUMBEROFBALES " \
          ", SDL.PRICE " \
          ", COMMERCIALINVOICE.INVOICECURRENCYCODE " \
          ", COMMERCIALINVOICE.EXCHANGERATEOFCONTRACT " \
          ", CIL.PRIMARYQTY " \
          ", PlantInvoice.AbsUniqueID " \
          ", EXPORTSHIPPING.FOBVALUEFC  " \
          ", EXPORTSHIPPING.FREIGHTAMTFC + EXPORTSHIPPING.DISCOUNTAMTFC + EXPORTSHIPPING.PACKINGAMTFC + EXPORTSHIPPING.OTHERDEDUCTIONAMTFC + " \
          "EXPORTSHIPPING.COMMISSIONAMTFC " \
          ", EXPORTSHIPPING.INSURANCEAMTFC " \
          ", COALESCE(BKLELEMENTS.ACTUALUNITCODE,'')  " \
          ", EXPORTSHIPPING.FOBVALUEFC + EXPORTSHIPPING.FREIGHTAMTFC + EXPORTSHIPPING.DISCOUNTAMTFC + EXPORTSHIPPING.PACKINGAMTFC + EXPORTSHIPPING.OTHERDEDUCTIONAMTFC + " \
          "EXPORTSHIPPING.COMMISSIONAMTFC " \
          ", EXPORTSHIPPING.FOBVALUEFC + EXPORTSHIPPING.FREIGHTAMTFC + EXPORTSHIPPING.DISCOUNTAMTFC + EXPORTSHIPPING.PACKINGAMTFC + EXPORTSHIPPING.OTHERDEDUCTIONAMTFC + " \
          "EXPORTSHIPPING.COMMISSIONAMTFC + EXPORTSHIPPING.INSURANCEAMTFC " \
          ", COMMERCIALINVOICE.CONTRACTNOCODE||'  DT:   '|| VARCHAR_FORMAT(COMMERCIALINVOICE.CONTRACTDATE,'DD-MM-YYYY')  " \
          ", CIL.BASICVALUE " \
          ", CIL.WIDTH " \
          ", CIL.GROSSWEIGHT " \
          ", CIL.NETTWEIGHT " \
          ", CIL.PRIMARYUMCODE " \
          ", 'BENEFICIARY : '||' '||COMPANYBANK.ACCOUNTOWNER " \
          ", 'ACCOUNT : ' ||' '|| COMPANYBANK.CURRENTACCOUNTID  " \
          ", 'COMPANY BANK: '||' '||BANK.LONGDESCRIPTION ||'  '|| BANK.BANKBRANCHADDRESS " \
          ", 'SWIFT CODE : '||' '|| BANK.BIC " \
          ", PartnerBank.LONGDESCRIPTION ||'  '|| PartnerBank.BANKBRANCHADDRESS " \
          ", 'SWIFT CODE : ' ||' '|| PartnerBank.BIC " \
          ", PlantInvoice.CATEGORY " \
          ", PlantInvoice.INVOICEDATE " \
          "Order By Company, INVOICENOandDt, Buyer, itmTyp, Item "
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
              # pdfrpt.c.line(400, 115, 580, 115) Total
              pdfrpt.c.drawAlignedString(405, 123, str(pdfrpt.packages))
              pdfrpt.c.drawAlignedString(455, 123, str('{0:1.3f}'.format(pdfrpt.quantity)))
              pdfrpt.c.drawAlignedString(560, 70, str('{0:1.4f}'.format(pdfrpt.amount)))
              # Amounts in words
              str1 = str(
                    pdfrpt.num2words(str('{0:1.4f}'.format(pdfrpt.amount)), lang='en', to='currency', separator=' and',
                                     cents=True,
                                     currency=str(pdfrpt.currency[-1]).strip())).replace(',', '')
              pdfrpt.wrap(str1, pdfrpt.c.drawString,70, 55, 60)
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