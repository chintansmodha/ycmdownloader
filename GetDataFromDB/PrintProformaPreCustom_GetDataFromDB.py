import os
from datetime import datetime

from django.shortcuts import render
from django.views.static import serve

from FormLoad import PrintProformaInv_Formload as views

from Global_Files import Connection_String as con
from PrintPDF import PrintProformaPreCustom_PrintPDF as pdfrpt
save_name=""

Exceptions=""

counter=0

goods = []


def PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate):
    global Exceptions, goods
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
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE2,'') " \
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
          ", Coalesce(BusinessPartner.ADDRESSLINE1,'') " \
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
          "Else Coalesce(BP_NotifyPrty.ADDRESSLINE1,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE2,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE3,'') || Coalesce(','||BP_NotifyPrty.ADDRESSLINE4,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE5,'') " \
          "|| Coalesce(',Postal Code : ' || BP_NotifyPrty.POSTALCODE,'') End  as NotifyPrtyADDRESS " \
          ", Coalesce(FACTORY.ECCNO,'') as IecBranch " \
          ", TermsOfShipping.LONGDESCRIPTION AS TermsOfDelv " \
          ", PAYMENTMETHOD.LONGDESCRIPTION As Payment " \
          ", CountryOrgnGoods.LONGDESCRIPTION as CountryOfOriginOfGoods " \
          ", CountryDestn.LONGDESCRIPTION as CountryOfDestn	" \
          ", portOfLoad.LONGDESCRIPTION  As PortOfLoading " \
          ", portOfDIS.LONGDESCRIPTION As PortOfDischarge " \
          ", finalDstn.LONGDESCRIPTION As FinalDestination " \
          ", COALESCE(PLANTINVOICE.VESSELFLIGHTNO,'') As VesselFlightNo " \
          ", TRIM(COALESCE(CUSTOMINVOICE.AWBNOCODE,PLANTINVOICE.BLNUMBER,'')) AS BlNo " \
          ", Trim(COALESCE(Varchar_FORMAT(CUSTOMINVOICE.AWBDATE,'DD-MM-YYYY'),Varchar_FORMAT(PLANTINVOICE.BLDATE,'DD-MM-YYYY'),'')) AS BlDt " \
          ", Trim(COALESCE(EXPORTSHIPPING.CODE,'')) As SBNo " \
          ", Trim(COALESCE(VARCHAR_FORMAT(EXPORTSHIPPING.SHIPPINGBILLDATE,'DD-MM-YYYY'),'')) As SbDt " \
          ", COALESCE(PLANTINVOICE.CONTAINERSIZE, '') As ContSize " \
          ", COALESCE(CUSTOMINVOICE.CONTAINERNO, '') As ContNO " \
          ", TRIM(COALESCE(PlantInvoice.CUSTOMERBOTTLESEALNO, '')) As SealNo " \
          ", COALESCE(PlantInvoice.BOTTLESEALNO, '') As ESealNo " \
          ", COALESCE(CUSTOMINVOICE.PRECARRIAGEBY, '') As Measure " \
          ", CUSTOMINVOICE.TOTALNUMBEROFBALES As Packages " \
          ", ITEMTYPE.LONGDESCRIPTION ||' (' || ITEMTYPE.CODE ||')' As ItmTyp " \
          ", trim (Product.LONGDESCRIPTION || ' ' || COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| QualityLevel.ShortDescriptiON) AS ITEM " \
          ", CIL.TARIFFCODE AS HSNCODE " \
          ", CUSTOMINVOICE.CODE ||'  DT:   '|| VARCHAR_FORMAT(CUSTOMINVOICE.INVOICEDATE,'DD-MM-YYYY') As InvoiceNoAndDt " \
          ", PLANTINVOICE.CODE AS INVOICENO " \
          ", Varchar_Format(PLANTINVOICE.INVOICEDATE,'DD-MM-YYYY') AS INVOICEDt	" \
          ", STXN.LOTCODE As LotNo " \
          ", COALESCE(BKLELEMENTS.ACTUALUNITCODE,'') As WtUnit " \
          ", CAST((SUM(BKLELEMENTS.ACTUALGROSSWT )) As DECIMAL(10,3)) As GROSSWt " \
          ", CAST((SUM(BKLELEMENTS.ACTUALNETWT)) As DECIMAL(10,3)) As NetWt " \
          ", CAST((Count(stxn.TRANSACTIONNUMBER)) As INT) As Boxes " \
          ", COUNTRY.LONGDESCRIPTION as CountryOfOrigin " \
          ", CIL.NUMBEROFBALES As  ItmPackages " \
          ", PlantInvoice.CATEGORY As MasterExpNo " \
          ", PlantInvoice.INVOICEDATE As MasterExpDt " \
          ", 'AD CODE: '||''||BANK.BRANCHCODE ||' '|| BANK.LONGDESCRIPTION||' '||BANK.BANKBRANCHADDRESS  As AdCode " \
          ", 'Stuffing Of Container At :'||'  GSTIN:  '|| ADGSTIN.GSTINNUMBER As StuffingGt " \
          ", 'GSTIN: ' ||' '|| ADGSTIN.GSTINNUMBER As StuffingExmGt " \
          ", FINBUSINESSUNIT.LONGDESCRIPTION " \
          "||' '|| Coalesce(PLANT.addressline1,'') " \
          "|| Coalesce(','||PLANT.addressline2,'') " \
          "|| Coalesce(','||PLANT.addressline3,'') " \
          "|| Coalesce(','||PLANT.addressline4,'') " \
          "|| Coalesce(','||PLANT.addressline5,'') As StuffingOfContainerAt " \
          ", Trim(CUSTOMINVOICE.BUYERSPOREFNO) ||'  DT:   '|| Trim(VARCHAR_FORMAT(CUSTOMINVOICE.CONTRACTDATE,'DD-MM-YYYY')) As RefNoAndDt " \
          ", CAST(CIL.PRIMARYQTY As DECIMAL(20,3)) As PRIMARYQTY " \
          ", Trim(CIL.PRIMARYUMCODE) as PRIMARYUMCODE   " \
          ", SUM(STXN.USERPRIMARYQUANTITY) As Quantity " \
          ", CAST(SDL.PRICE AS DECIMAL(10, 3)) As Rate " \
          ", CUSTOMINVOICE.INVOICECURRENCYCODE AS CURRENCY " \
          ", CAST(CIL.BASICVALUE As DECIMAL(20,4)) As AMOUNT " \
          ", CAST(CUSTOMINVOICE.EXCHANGERATEOFCONTRACT AS DECIMAL(10,2)) As ExRate " \
          ", CAST((CUSTOMINVOICE.GROSSVALUE * CUSTOMINVOICE.EXCHANGERATEOFCONTRACT) AS DECIMAL(20,2)) As GstInvValueINR " \
          ", (Select COALESCE(CAST(Sum(gstVal.Value) AS DECIMAL(10,2)),0.00) ||' '|| '%' From INDTAXDETAIL gstVal " \
          "where CUSTOMINVOICE.ABSUNIQUEID = gstVal.FABSUNIQUEID " \
          "And     gstVal.TAXCATEGORYCODE = 'GST' " \
          "And     gstVal.CALCULATIONTYPE = 2) As GSTinINR " \
          ", EXPORTSHIPPING.FOBVALUEFC As FobValue " \
          ", EXPORTSHIPPING.FREIGHTAMTFC + EXPORTSHIPPING.DISCOUNTAMTFC + EXPORTSHIPPING.PACKINGAMTFC + EXPORTSHIPPING.OTHERDEDUCTIONAMTFC + " \
          "EXPORTSHIPPING.COMMISSIONAMTFC As Freight " \
          ", EXPORTSHIPPING.INSURANCEAMTFC As insurance " \
          ", EXPORTSHIPPING.FOBVALUEFC + EXPORTSHIPPING.FREIGHTAMTFC + EXPORTSHIPPING.DISCOUNTAMTFC + EXPORTSHIPPING.PACKINGAMTFC " \
          "+ EXPORTSHIPPING.OTHERDEDUCTIONAMTFC +  EXPORTSHIPPING.COMMISSIONAMTFC As CfrValue " \
          ", EXPORTSHIPPING.FOBVALUEFC + EXPORTSHIPPING.FREIGHTAMTFC + EXPORTSHIPPING.DISCOUNTAMTFC + EXPORTSHIPPING.PACKINGAMTFC " \
          "+ EXPORTSHIPPING.OTHERDEDUCTIONAMTFC + EXPORTSHIPPING.COMMISSIONAMTFC + EXPORTSHIPPING.INSURANCEAMTFC As CifValue " \
          ", CUSTOMINVOICE.COMMERCIALINVOICECODE ||' DT: '|| VARCHAR_FORMAT(CUSTOMINVOICE.INVOICEDATE,'DD-MM-YYYY') as COMMERCIALinvNo " \
          ", PLANT.TOWN As Place " \
          ", COALESCE(SCHEMETYPE.LONGDESCRIPTION, '') AS SCHEME " \
          ",COALESCE(VARCHAR(CIL.EPCGLICENSENO), VARCHAR(EPCGAPP.CODE),'') As EPCGLICENSE " \
          ",COALESCE(VARCHAR_FORMAT(CIL.EPCGLICENSEDATE,'DD-MM-YYYY'),'') As EPCGLICENSEDATE " \
          ", CIL.ADVANCELICENSENO As ADVLICENSE " \
          ", VARCHAR_FORMAT(CIL.ADVANCELICENSEDATE,'DD-MM-YYYY') As ADVLICENSEDATE " \
          ", SSL_Desc.ValueString As SLL_Description " \
          ", ERT_Desc.ValueString As CircularNo " \
          "From PlantInvoice " \
          "Join CUSTOMINVOICE                      On      PlantInvoice.CUSTOMINVOICECODE = CUSTOMINVOICE.CODE  " \
          "And     PlantInvoice.CUSTOMINVOICETYPECODE = CUSTOMINVOICE.INVOICETYPECODE " \
          "join OrderPartner                       ON      CUSTOMINVOICE.BUYERIFOTCCUSTOMERSUPPLIERCODE = OrderPartner.CustomerSupplierCode " \
          "AND     CUSTOMINVOICE.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OrderPartner.CustomerSupplierType " \
          "join BusinessPartner                    ON      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
          "Left join OrderPartner OP_CONsig        ON      CUSTOMINVOICE.CONSIGNEECUSTOMERSUPPLIERCODE = OP_CONsig.CustomerSupplierCode " \
          "AND     CUSTOMINVOICE.CONSIGNEECUSTOMERSUPPLIERTYPE = OP_CONsig.CustomerSupplierType " \
          "Left join BusinessPartner BP_CONsig     ON      OP_CONsig.OrderbusinessPartnerNumberId 	= BP_CONsig.NumberID " \
          "LEFT JOIN Address ADDRESS_CONsignee     ON      BP_CONsig.ABSUNIQUEID = ADDRESS_CONsignee.UNIQUEID " \
          "AND     CUSTOMINVOICE.DELIVERYPOINTCODE = ADDRESS_CONsignee.CODE " \
          "Left Join OrderPartner OP_NotifyPrty    On      CUSTOMINVOICE.NOTIFYPARTYCSMSUPPLIERCODE = OP_NotifyPrty.CustomerSupplierCode " \
          "AND     CUSTOMINVOICE.NOTIFYPARTYCSMSUPPLIERTYPE = OP_NotifyPrty.CustomerSupplierType " \
          "Left join BusinessPartner BP_NotifyPrty ON      OP_NotifyPrty.OrderbusinessPartnerNumberId 	= BP_NotifyPrty.NumberID " \
          "LEFT JOIN Address ADDRESS_NotifyPrty    ON      BP_NotifyPrty.ABSUNIQUEID = ADDRESS_NotifyPrty.UNIQUEID " \
          "AND     CUSTOMINVOICE.DELIVERYPOINTCODE = ADDRESS_NotifyPrty.CODE " \
          "Join PAYMENTMETHOD                      On      CUSTOMINVOICE.TERMSOFPAYMENTCODE = PAYMENTMETHOD.CODE " \
          "Left Join COUNTRY CountryDestn          On      CUSTOMINVOICE.DESTINATIONCOUNTRYCODE = CountryDestn.CODE " \
          "Left Join COUNTRY CountryOrgnGoods      On      CUSTOMINVOICE.GOODSORIGINCOUNTRYCODE = CountryOrgnGoods.CODE " \
          "Left Join PORT portOfLoad               On      CUSTOMINVOICE.PORTOFLOADINGCODE = portOfLoad.CODE " \
          "Left Join PORT portOfDIS                On      CUSTOMINVOICE.PORTOFDISCHARGECODE = portOfDIS.CODE " \
          "Left Join DESTINATION finalDstn         On      CUSTOMINVOICE.FINALDESTINATIONCODE = finalDstn.CODE " \
          "JOIN TermsOfShipping                    ON      CUSTOMINVOICE.TERMSOFSHIPPINGCODE = TermsOfShipping.CODE " \
          "JOIN FIRM                               ON      CUSTOMINVOICE.DIVISIONCODE = FIRM.CODE " \
          "JOIN DIVISION                           ON 	CUSTOMINVOICE.DIVISIONCODE = DIVISION.CODE " \
          "JOIN ADDRESS REGD_ADDRESS               ON 	DivisiON.AbsUniqueId = REGD_ADDRESS.UniqueId " \
          "AND 	REGD_ADDRESS.Code = 'REGD' " \
          "JOIN ADDRESS CORP_ADDRESS               ON 	DivisiON.AbsUniqueId = CORP_ADDRESS.UniqueId " \
          "AND 	CORP_ADDRESS.Code = 'CORP' " \
          "Left Join SCHEMETYPE                    On      CUSTOMINVOICE.COMPANYCODE = SCHEMETYPE.COMPANYCODE " \
          "And     CUSTOMINVOICE.SCHEMETYPECODE = SCHEMETYPE.CODE " \
          "JOIN CUSTOMINVOICELINE  CIL             ON 	CUSTOMINVOICE.CODE = CIL.CUSTOMINVOICECODE " \
          "AND 	CUSTOMINVOICE.DIVISIONCODE = CIL.CUSTOMINVOICEDIVISIONCODE " \
          "Join ITEMTYPE                           ON      CIL.ITEMTYPECODE = ITEMTYPE.CODE " \
          "JOIN FullItemKeyDecoder FIKD            ON      CIL.ITEMTYPECODE = FIKD.ITEMTYPECODE " \
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
          "AND     FIKD.ItemUniqueId   = Product.AbsUniqueId  " \
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
          "Join COUNTRY                            On      PLANT.COUNTRYCODE = COUNTRY.CODE " \
          "Left Join EXPORTSHIPPING                On      CUSTOMINVOICE.EXPORTSHIPPINGBILLCODE = EXPORTSHIPPING.CODE " \
          "JOIN SALESDOCUMENTLINE SDL              ON      PlantInvoice.SALESINVOICEPROVISIONALCODE = SDL.SALESDOCUMENTPROVISIONALCODE " \
          "And     PlantInvoice.SALINVOICEPRVCOUNTERCODE = SDL.SALDOCPROVISIONALCOUNTERCODE " \
          "AND     CIL.ITEMTYPECODE = SDL.ITEMTYPEAFICODE " \
          "AND     COALESCE(CIL.SubCode1, '') = COALESCE(SDL.SubCode01, '') " \
          "AND     COALESCE(CIL.SubCode2, '') = COALESCE(SDL.SubCode02, '') " \
          "AND     COALESCE(CIL.SubCode3, '') = COALESCE(SDL.SubCode03, '') " \
          "AND     COALESCE(CIL.SubCode4, '') = COALESCE(SDL.SubCode04, '') " \
          "AND     COALESCE(CIL.SubCode5, '') = COALESCE(SDL.SubCode05, '') " \
          "AND     COALESCE(CIL.SubCode6, '') = COALESCE(SDL.SubCode06, '') " \
          "AND     COALESCE(CIL.SubCode7, '') = COALESCE(SDL.SubCode07, '') " \
          "AND     COALESCE(CIL.SubCode8, '') = COALESCE(SDL.SubCode08, '') " \
          "AND     COALESCE(CIL.SubCode9, '') = COALESCE(SDL.SubCode09, '') " \
          "AND     COALESCE(CIL.SubCode10, '') = COALESCE(SDL.SubCode10, '') " \
          "AND     CIL.QUALITYLEVELCODE = SDL.QUALITYCODE " \
          "AND 	SDL.DocumentTypeType = '06' " \
          "Join STOCKTRANSACTION STXN              On      SDL.PREVIOUSCODE = STXN.ORDERCODE " \
          "AND     SDL.PREVIOUSCOUNTERCODE = STXN.ORDERCOUNTERCODE " \
          "AND     SDL.PREVIOUSORDERLINE = STXN.ORDERLINE " \
          "LEFT JOIN BKLELEMENTS                        ON      STXN.CONTAINERELEMENTCODE = BKLELEMENTS.CODE " \
          "Left JOIN BANK                          ON      PLANTINVOICE.FIRMBANKBANKCOUNTRYCODE = BANK.BANKCOUNTRYCODE " \
          "And     PLANTINVOICE.FIRMBANKCODE = BANK.CODE " \
          "And     PLANTINVOICE.FIRMBANKBRANCHCODE = BANK.BRANCHCODE " \
          "LEFT JOIN COMPANYBANK                   ON	Bank.BANKCOUNTRYCODE = COMPANYBANK.BANKBANKCOUNTRYCODE " \
          "And   Bank.CODE = COMPANYBANK.BANKCODE " \
          "And   Bank.BRANCHCODE = COMPANYBANK.BANKBRANCHCODE  " \
          "Left Join EPCGAPPLICATION EPCGAPP       ON      CUSTOMINVOICE.EPCGEPCGAPPLICATIONCODE = EPCGAPP.CODE " \
          "Left Join  UserGenericGroup As SSL_Ugg        On      SSL_Ugg.USERGENERICGROUPTYPECODE = 'SSL' " \
          "Left Join  AdStorage SSL_Plant                On      LOGICALWAREHOUSE.PlantCode = SSL_Plant.Valuestring " \
          "And     SSL_Plant.NameEntityName = 'UserGenericGroup' " \
          "And     SSL_Plant.FieldName = 'PlantCodeCode' " \
          "And     SSl_Ugg.AbsUniqueId = SSL_Plant.UniqueId " \
          "Join  AdStorage SSl_Startingdt                On      SSl_Startingdt.NameEntityName = 'UserGenericGroup' " \
          "And     SSl_Startingdt.FieldName = 'StartingDate' " \
          "And     CUSTOMINVOICE.INVOICEDATE >= SSl_Startingdt.ValueDate " \
          "And     SSL_Plant.UniqueId = SSl_Startingdt.UniqueId " \
          "Join  AdStorage SSl_Endingdt                  On      SSl_Endingdt.NameEntityName = 'UserGenericGroup' " \
          "And     SSl_Endingdt.FieldName = 'EndDate' " \
          "And     CUSTOMINVOICE.INVOICEDATE <= SSl_Endingdt.ValueDate " \
          "And     SSL_Plant.UniqueId = SSl_Endingdt.UniqueId " \
          "And     SSl_Startingdt.UniqueId = SSl_Endingdt.UniqueId " \
          "Join  AdStorage  SSl_Desc                     On      SSl_Endingdt.UniqueId = SSl_Desc.UniqueId " \
          "And     SSl_Startingdt.UniqueId = SSl_Desc.UniqueId " \
          "And     SSl_Desc.NameEntityName = 'UserGenericGroup' " \
          "And     SSl_Desc.FieldName = 'Description' " \
          "Left Join  UserGenericGroup As ERT_Ugg        On      ERT_Ugg.USERGENERICGROUPTYPECODE = 'ERT' " \
          "Left Join  AdStorage ERT_Plant                On      LOGICALWAREHOUSE.PlantCode = ERT_Plant.Valuestring " \
          "And     ERT_Plant.NameEntityName = 'UserGenericGroup' " \
          "And     ERT_Plant.FieldName = 'PlantCodeCode' " \
          "And     ERT_Ugg.AbsUniqueId = ERT_Plant.UniqueId " \
          "Left Join  AdStorage ERT_Startingdt           On      ERT_Startingdt.NameEntityName = 'UserGenericGroup' " \
          "And     ERT_Startingdt.FieldName = 'StartingDate' " \
          "And     CUSTOMINVOICE.INVOICEDATE >= ERT_Startingdt.ValueDate " \
          "And     ERT_Plant.UniqueId = ERT_Startingdt.UniqueId " \
          "Left Join  AdStorage ERT_Endingdt             On      ERT_Endingdt.NameEntityName = 'UserGenericGroup' " \
          "And     ERT_Endingdt.FieldName = 'EndDate' " \
          "And     CUSTOMINVOICE.INVOICEDATE <= ERT_Endingdt.ValueDate " \
          "And     ERT_Plant.UniqueId = ERT_Endingdt.UniqueId " \
          "And     ERT_Startingdt.UniqueId = ERT_Endingdt.UniqueId " \
          "Left Join  AdStorage  ERT_Desc                On      ERT_Endingdt.UniqueId = ERT_Desc.UniqueId " \
          "And     ERT_Startingdt.UniqueId = ERT_Desc.UniqueId " \
          "And     ERT_Desc.NameEntityName = 'UserGenericGroup' " \
          "And     ERT_Desc.FieldName = 'Description' " \
          "Where"+InvoiceNos+" " \
          "Group By Comp.LONGDESCRIPTION " \
          ", 'FACTORY: '||' '|| Coalesce(PLANT.addressline1,'') " \
          "|| Coalesce(','||PLANT.addressline2,'') " \
          "|| Coalesce(','||PLANT.addressline3,'') " \
          "|| Coalesce(','||PLANT.addressline4,'') " \
          "|| Coalesce(','||PLANT.addressline5,'') " \
          "|| RTRIM(Coalesce(','||PLANT.postalcode,'')) ||'   GSTIN : '|| ADGSTIN.GSTINNUMBER " \
          ", 'REGD. OFF: '||' '||Coalesce(REGD_ADDRESS.ADDRESSEE,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline1,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline2,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline3,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline4,'') " \
          "|| Coalesce(','||REGD_ADDRESS.addressline5,'') " \
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
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE2,'') " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE3,'') " \
          "|| Coalesce(','||ADDRESS_CONsignee.ADDRESSLINE4,'') " \
          "||','|| Coalesce(ADDRESS_CONsignee.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(ADDRESS_CONsignee.POSTALCODE,'') " \
          "Else Coalesce(BP_CONsig.ADDRESSLINE1,'') || Coalesce(','||BP_CONsig.ADDRESSLINE2,'') " \
          "|| Coalesce(','||BP_CONsig.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BP_CONsig.ADDRESSLINE4,'') " \
          "||','|| Coalesce(BP_CONsig.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(BP_CONsig.POSTALCODE,'') End " \
          ", BusinessPartner.LEGALNAME1 " \
          ", Coalesce(BusinessPartner.ADDRESSLINE1,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE2,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BusinessPartner.ADDRESSLINE4,'') " \
          "||','|| Coalesce(BusinessPartner.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(BusinessPartner.POSTALCODE,'') " \
          ", COALESCE(BP_NotifyPrty.LEGALNAME1,'') " \
          ", CASE When ADDRESS_NotifyPrty.UNIQUEID is Not Null Then Coalesce(ADDRESS_NotifyPrty.ADDRESSEE,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE1,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE2,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE3,'') " \
          "|| Coalesce(','||ADDRESS_NotifyPrty.ADDRESSLINE4,'') " \
          "||','|| Coalesce(ADDRESS_NotifyPrty.ADDRESSLINE5,'') " \
          "||', Postal Code : '||Coalesce(ADDRESS_NotifyPrty.POSTALCODE,'') " \
          "Else Coalesce(BP_NotifyPrty.ADDRESSLINE1,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE2,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE3,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE4,'') " \
          "|| Coalesce(','||BP_NotifyPrty.ADDRESSLINE5,'') " \
          "|| Coalesce(',Postal Code : ' || BP_NotifyPrty.POSTALCODE,'') End " \
          ", TermsOfShipping.LONGDESCRIPTION " \
          ", PAYMENTMETHOD.LONGDESCRIPTION " \
          ", CountryOrgnGoods.LONGDESCRIPTION " \
          ", CountryDestn.LONGDESCRIPTION " \
          ", portOfLoad.LONGDESCRIPTION " \
          ", portOfDIS.LONGDESCRIPTION " \
          ", finalDstn.LONGDESCRIPTION " \
          ", COALESCE(PLANTINVOICE.VESSELFLIGHTNO,'') " \
          ", TRIM(COALESCE(CUSTOMINVOICE.AWBNOCODE,PLANTINVOICE.BLNUMBER,'')) " \
          ", Trim(COALESCE(Varchar_FORMAT(CUSTOMINVOICE.AWBDATE,'DD-MM-YYYY'),Varchar_FORMAT(PLANTINVOICE.BLDATE,'DD-MM-YYYY'),'')) " \
          ", EXPORTSHIPPING.CODE " \
          ", EXPORTSHIPPING.SHIPPINGBILLDATE " \
          ", COALESCE(PlantInvoice.CONTAINERSIZE, '') " \
          ", COALESCE(CUSTOMINVOICE.CONTAINERNO, '') " \
          ", TRIM(COALESCE(PlantInvoice.CUSTOMERBOTTLESEALNO, '')) " \
          ", COALESCE(PlantInvoice.BOTTLESEALNO, '') " \
          ", COALESCE(CUSTOMINVOICE.PRECARRIAGEBY, '') " \
          ", CUSTOMINVOICE.TOTALNUMBEROFBALES " \
          ", ITEMTYPE.LONGDESCRIPTION ||' (' || ITEMTYPE.CODE ||')' " \
          ", trim (Product.LONGDESCRIPTION || ' ' || COALESCE(UGG.LONGDESCRIPTION,'') ||' '|| QualityLevel.ShortDescriptiON) " \
          ", CIL.TARIFFCODE " \
          ", CUSTOMINVOICE.CODE, CUSTOMINVOICE.INVOICEDATE " \
          ", PLANTINVOICE.CODE " \
          ", PLANTINVOICE.INVOICEDATE " \
          ", STXN.LOTCODE " \
          ", COUNTRY.LONGDESCRIPTION " \
          ", CIL.NUMBEROFBALES " \
          ", PlantInvoice.CATEGORY " \
          ", PlantInvoice.INVOICEDATE " \
          ", 'AD CODE: '||''||BANK.BRANCHCODE ||' '|| BANK.LONGDESCRIPTION||' '||BANK.BANKBRANCHADDRESS " \
          ", 'Stuffing Of Container At :'||'  GSTIN:  '|| ADGSTIN.GSTINNUMBER " \
          ", 'GSTIN: ' ||' '|| ADGSTIN.GSTINNUMBER " \
          ", FINBUSINESSUNIT.LONGDESCRIPTION " \
          "||' '|| Coalesce(PLANT.addressline1,'') " \
          "|| Coalesce(','||PLANT.addressline2,'') " \
          "|| Coalesce(','||PLANT.addressline3,'') " \
          "|| Coalesce(','||PLANT.addressline4,'') " \
          "|| Coalesce(','||PLANT.addressline5,'') " \
          ", Trim(CUSTOMINVOICE.BUYERSPOREFNO) ||'  DT:   '|| Trim(VARCHAR_FORMAT(CUSTOMINVOICE.CONTRACTDATE,'DD-MM-YYYY')) " \
          ", SDL.PRICE " \
          ", CUSTOMINVOICE.INVOICECURRENCYCODE " \
          ", CUSTOMINVOICE.EXCHANGERATEOFCONTRACT " \
          ", CIL.PRIMARYQTY " \
          ", PlantInvoice.AbsUniqueID " \
          ", EXPORTSHIPPING.FOBVALUEFC " \
          ", EXPORTSHIPPING.FREIGHTAMTFC + EXPORTSHIPPING.DISCOUNTAMTFC + EXPORTSHIPPING.PACKINGAMTFC + EXPORTSHIPPING.OTHERDEDUCTIONAMTFC + " \
          "EXPORTSHIPPING.COMMISSIONAMTFC " \
          ", EXPORTSHIPPING.FOBVALUEFC + EXPORTSHIPPING.FREIGHTAMTFC + EXPORTSHIPPING.DISCOUNTAMTFC + EXPORTSHIPPING.PACKINGAMTFC " \
          "+ EXPORTSHIPPING.OTHERDEDUCTIONAMTFC + EXPORTSHIPPING.COMMISSIONAMTFC " \
          ", EXPORTSHIPPING.FOBVALUEFC + EXPORTSHIPPING.FREIGHTAMTFC + EXPORTSHIPPING.DISCOUNTAMTFC + EXPORTSHIPPING.PACKINGAMTFC " \
          "+ EXPORTSHIPPING.OTHERDEDUCTIONAMTFC + EXPORTSHIPPING.COMMISSIONAMTFC + EXPORTSHIPPING.INSURANCEAMTFC " \
          ", EXPORTSHIPPING.INSURANCEAMTFC " \
          ", COALESCE(BKLELEMENTS.ACTUALUNITCODE,'') " \
          ", Trim(CIL.PRIMARYUMCODE) " \
          ", CUSTOMINVOICE.COMMERCIALINVOICECODE " \
          ", PLANT.TOWN " \
          ", CIL.BASICVALUE " \
          ", COALESCE(SCHEMETYPE.LONGDESCRIPTION, '') " \
          ",COALESCE(VARCHAR(CIL.EPCGLICENSENO), VARCHAR(EPCGAPP.CODE),'') " \
          ",COALESCE(VARCHAR_FORMAT(CIL.EPCGLICENSEDATE,'DD-MM-YYYY'),'') " \
          ", CIL.ADVANCELICENSENO " \
          ", VARCHAR_FORMAT(CIL.ADVANCELICENSEDATE,'DD-MM-YYYY') " \
          ", CUSTOMINVOICE.GROSSVALUE " \
          ", CUSTOMINVOICE.ABSUNIQUEID " \
          ", FACTORY.ECCNO " \
          ", SSL_Desc.ValueString " \
          ", ERT_Desc.ValueString " \
          "Order By Company, INVOICENOandDt,Buyer, itmTyp, LotNo, Item "
    # Where"+InvoiceNos+"

    stmt = con.db.prepare(con.conn, sql)
    # Explicitly bind parameters
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    goods = []
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result,goods,pdfrpt.D,pdfrpt.sr)
        pdfrpt.d = pdfrpt.dvalue()
        if result not in goods:
              goods.append(str(result['ITEM']))
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 150:
            pdfrpt.d = 435
            pdfrpt.c.setPageSize(pdfrpt.portrait(pdfrpt.A4))
            pdfrpt.c.showPage()
            pdfrpt.header(pdfrpt.divisioncode, result)

    if result == False:
        if counter > 0:

              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.c.drawString(155, pdfrpt.d, "LOTNO. :  " + pdfrpt.lotno[-1])
              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.c.drawString(155, pdfrpt.d, "HSNCODE :  " + pdfrpt.hsncode[-1])
              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.d = pdfrpt.dvalue()
              pdfrpt.c.drawString(155, pdfrpt.d, "COUNTRY OF ORIGIN:  " + str(pdfrpt.countryofOrigin[-1]).upper())
              # pdfrpt.c.line(400, 115, 580, 115)
              pdfrpt.c.drawString(490, 118, "<--Total ")
              pdfrpt.c.drawAlignedString(405, 118, str(pdfrpt.packages))
              pdfrpt.c.drawAlignedString(465, 118, str('{0:1.3f}'.format(pdfrpt.quantity)))
              pdfrpt.c.drawAlignedString(560, 110, str('{0:1.4f}'.format(pdfrpt.amount)))
              pdfrpt.c.drawAlignedString(85, 420, str('{0:1.3f}'.format(pdfrpt.grosswt)))
              pdfrpt.c.drawAlignedString(85, 410, str('{0:1.3f}'.format(pdfrpt.netwt)))
              pdfrpt.c.drawString(85, 390, str(pdfrpt.packages))
              pdfrpt.c.drawAlignedString(175, 450, str(pdfrpt.packages))  # No Of Cartons
              # Amounts in words
              str1 = str(
                    pdfrpt.num2words(str('{0:1.4f}'.format(pdfrpt.amount)), lang='en', to='currency', separator=' and', cents=True,
                              currency=str(pdfrpt.currency[-1]).strip())).replace(',','')
              pdfrpt.wrap(str(pdfrpt.currency[-1]).strip() + ' ' + str1, pdfrpt.c.drawString, 55, 140, 117)
              pdfrpt.c.showPage()
              #****************************************************************
              pdfrpt.ExminationReport(pdfrpt.Goods,pdfrpt.D,pdfrpt.sr)
              pdfrpt.NewRequest()
              pdfrpt.c.drawString(170, 665, ': ' + pdfrpt.invoiceno[-1])
              pdfrpt.c.drawString(170, pdfrpt.Y, ': ' + str(pdfrpt.grosswt))
              pdfrpt.c.drawString(170, pdfrpt.Y - 10, ': ' + str(pdfrpt.netwt))
              pdfrpt.c.drawString(170, pdfrpt.Y - 20, ': ' + str(pdfrpt.packages))
              pdfrpt.TotalClean()

              Exceptions = ""
              counter = 0
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria "
            return

    pdfrpt.c.setPageSize(pdfrpt.portrait(pdfrpt.A4))
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.d = pdfrpt.newpage()
    pdfrpt.i = 0
    pdfrpt.TotalClean()
    pdfrpt.newrequest()
    pdfrpt.updateDvalue()
    pdfrpt.sr = pdfrpt.SetSerialNo()
    pdfrpt.NewRequest()