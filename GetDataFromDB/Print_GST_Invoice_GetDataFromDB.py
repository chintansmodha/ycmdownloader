import os
from datetime import datetime

from django.shortcuts import render
from django.views.static import serve

from FormLoad import PrintYarnChallan_FormLoad as views
from ProcessSelection import PrintYarnChallan_ProcessSelection as PrintChallan_Views
# from PrintPDF import PrintYeanChallanBoxNoWisePDF as pdfrptgstinvoice
# from PrintPDF import PrintYeanChallanBoxNoWisePDF as pdfrptgstinvoice
from PrintPDF import PrintChallan_GST_Invoice_PDF as pdfrptgstinvoice
from Global_Files import Connection_String as con
from PrintPDF import PrintChallanRule55_PrintPDF as pdfrpt
from  ProcessSelection import PrintYarnChallan_ProcessSelection as ps
save_name=""
LSInvoiceChallanNo=""
counter1=0
def PrintChallan_GST_Invoice_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintChallan" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Print Yarn Challan GST INVOICE/",
                             LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSChallanNo = request.GET.getlist('challanno')
    LSChallanDate = request.GET.getlist('challandt')
    LSLotNo = request.GET.getlist('lotno')
    LSLrNo = request.GET.getlist('lrno')
    LSLrDt = request.GET.getlist('lrdt')
    LSQuantity = request.GET.getlist('qty')
    LSBoxes = request.GET.getlist('box')
    Company = ''
    Party = ''

    LSInvoiceChallanNo = " PLANTINVOICE.CODE in " + "(" + str(LSChallanNo)[1:-1] + ")"
    # LSChallanNo = " AND SALESDOCUMENT.PROVISIONALCODE in " + "(" + str(LSChallanNo)[1:-1] + ")"
    LSChallanDate = " AND VARCHAR_FORMAT(SALESDOCUMENT.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') in  " + "(" + str(LSChallanDate)[
                                                                                                            1:-1] + ")"

    save_name = ''
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = "PrintYeanChallan_GST_INVOICE" + LSFileName
    save_name = os.path.join(os.path.expanduser("~"),
                             "D:/Report Development/Generated Reports/Print Yarn Challan GST INVOICE/",
                             LSFileName)
    print("file path : " + save_name)

    pdfrptgstinvoice.c = pdfrptgstinvoice.canvas.Canvas(save_name + ".pdf")
    PrintChallan_GST_Invoice(LSInvoiceChallanNo,request,LSChallanNo)
    filepath =save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PrintChallan_Boxes_No_Wise_Table.html',
                      {'GDataPrintChallan': ps.GDataPrintChallan})

    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))




def PrintChallan_GST_Invoice(LSInvoiceChallanNo,request,LSChallanNo):
    print("from Local GST Invoice")
    sql=""
    # sql = " SELECT     Coalesce(REGD_ADDRESS.addressline1,'') " \
    #       "           || Coalesce(','||REGD_ADDRESS.addressline2,'') " \
    #       "           || Coalesce(','||REGD_ADDRESS.addressline3,'')  " \
    #       "           || Coalesce(','||REGD_ADDRESS.addressline4,'')   " \
    #       "           || Coalesce(','||REGD_ADDRESS.addressline5,'')   " \
    #       "           || Coalesce(','||REGD_ADDRESS.postalcode,'') AS REGD_ADDRESS  " \
    #       "           , Coalesce(CORP_ADDRESS.addressline1,'')   " \
    #       "           || Coalesce(','||CORP_ADDRESS.addressline2,'') " \
    #       "           || Coalesce(','||CORP_ADDRESS.addressline3,'') " \
    #       "           || Coalesce(','||CORP_ADDRESS.addressline4,'') " \
    #       "           || Coalesce(','||CORP_ADDRESS.addressline5,'') " \
    #       "           || Coalesce(','||CORP_ADDRESS.postalcode,'') AS CORP_ADDRESS " \
    #       "            , PLANTINVOICE.CODE AS INVOICENO   " \
    #       "             , VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE, 'DD-MM-YYYY')    AS INVOICEDATE  " \
    #       "            , COALESCE(PLANTINVOICE.CONTRACTNOCODE,'') AS REFERANCECODE " \
    #       "            , COALESCE(salesdocument.INTERNALREFERENCE,'') AS OURREFERANCEVALUE " \
    #       "            , COALESCE(plantinvoice.EXPORTERREFNO,'') AS EXPORTERREFERANCENUMBER" \
    #       "            , PlantInvoice.TIMEOFREMOVALOFGOODS AS SUPPLYDATE  " \
    #       "            , VARCHAR_FORMAT(PLANTINVOICE.INVOICEISSUETIME, 'DD-MM-YYYY')    AS INVOICEISSUEDATE " \
    #       "            , PlantInvoice.INVOICEISSUETIME AS DATEOFREMOVALOFGOODS " \
    #       "            , COMPANY.LONGDESCRIPTION AS  companyname  " \
    #       "            , SALESDOCUMENTLINE.PreviousCode AS CHALLANNUMBER  " \
    #       "            , agent.LONGDESCRIPTION AS BROKERNAME   " \
    #       "            , trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS PRODUCT  " \
    #       "            , TRIM (UGG.Code)  ||' / '||UGG.LONGDESCRIPTION As ShadeCode  " \
    #       "                , BusinessPartner.LEGALNAME1 AS CUSTOMER   " \
    #       "            , Coalesce(BusinessPartner.ADDRESSLINE1,'')  " \
    #       "    		|| Coalesce(','||BusinessPartner.ADDRESSLINE2,'')  " \
    #       "    		|| Coalesce(','||BusinessPartner.ADDRESSLINE3,'') " \
    #       "    		|| Coalesce(','||BusinessPartner.ADDRESSLINE4,'')   " \
    #       "    		||','|| Coalesce(BusinessPartner.ADDRESSLINE5,'')  " \
    #       "    		||', Postal Code : '||Coalesce(BusinessPartner.POSTALCODE,'') as CustomerAddress  " \
    #       "           , COALESCE(BP_Consig.LEGALNAME1,'') AS CONSIGNEEname  " \
    #       "            , Coalesce(ADDRESS_Consignee.ADDRESSLINE1,'') " \
    #       "    		|| Coalesce(','||ADDRESS_Consignee.ADDRESSLINE2,'')  " \
    #       "    		|| Coalesce(','||ADDRESS_Consignee.ADDRESSLINE3,'') " \
    #       "    		|| Coalesce(','||ADDRESS_Consignee.ADDRESSLINE4,'') " \
    #       "    		||','|| Coalesce(ADDRESS_Consignee.ADDRESSLINE5,'')  " \
    #       "    		||', Postal Code : '||Coalesce(ADDRESS_Consignee.POSTALCODE,'') as CONSIGNEEADDRESS  " \
    #       "            , Coalesce(PLANTINVOICE.LRNO,'')as LRNO  " \
    #       "            , Coalesce(TZ_DespFrom.LONGDESCRIPTION,'') as DespFRom  " \
    #       "            , Coalesce(TZ_DespTo.LONGDESCRIPTION,'') as DespTO  " \
    #       "            , Plant.AddressLine1 AS PlantAddress " \
    #       "            , Coalesce(ABS_LRNO.ValueString,'') AS LRNO   " \
    #       "            , Coalesce(ABS_LRDATE.ValueString,'') AS  LRDATE  " \
    #       "             , COALESCE(St.LotCode,'') AS LOTNUMBER " \
    #       "             , Coalesce(ADS_SaleLot.ValueString,'') As SALELOT " \
    #       "            , Firm.TINNo AS CINNO " \
    #       "            , ADGSTIN.GSTINNUMBER AS COMPANYGSTINNO  " \
    #       "            , FIRM.PANNO As COMPANYPANNO  " \
    #       "            , FIRM.EmailAddress AS COMPANYEMAIL " \
    #       "            , FIRM.ADDRESSFAXNUMBER As COMPANYWebUrl " \
    #       "            , Coalesce(COMMISSIONERATE,'') as CUSTOMERPAN    " \
    #       "            , CUSTOMERGSTIN.GSTINNumber AS CUSTOMERGST  " \
    #       "            , CUSTOMERGSTIN.STATECODE AS GSTSTATECODE  " \
    #       "            , STATEGST.LONGDESCRIPTION AS GSTSTATE   " \
    #       "            , PLANTINVOICELINE.TARIFFCODE AS HSNCODE  " \
    #       "            , Coalesce(PLANTINVOICE.TRUCKNO,'') AS TRUCKNO   " \
    #       "            , Coalesce(plantinvoice.BUYERSPOREFNO,'')  AS BUYERREFFERANCEVALUE  " \
    #       "            , InvRate.calculatedvalueRCC AS InvRate  " \
    #       "            , Itemamt.calculatedvalueRCC AS ItemAmount  " \
    #       "            , PLANTINVOICE.BASICVALUE as BASICVALUE  " \
    #       "            , PLANTINVOICE.NETTVALUE As InvoiceAmt  " \
    #       "            , Coalesce(PLANTINVOICE.IRN,'') as IRNVALUE  " \
    #       "            , PLANTINVOICE.ROUNDOFFVALUE   " \
    #       "            , COALESCE(PLANTINVOICE.EWBNO,'') AS EWAYBILL  " \
    #       "            , COALESCE(PLANTINVOICE.EWBDT,'') AS EWAYBILLDATE " \
    #       "            , PLANTINVOICELINE.PRIMARYQTY AS QUANTITY  " \
    #       "            , plantinvoiceLINE.PRIMARYUMCODE AS UOM " \
    #       "            , plantinvoice.TYPEFOREINVOICE as INVOICETYPE " \
    #       "            , SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS CHALLANQUANTITY   " \
    #       "            , SALESDOCUMENTLINE.USERPRIMARYUOMCODE AS CHALLANUOM  " \
    #       "            , SALESDOCUMENTLINE.PRICE AS CHALLANPRICE  " \
    #       "            , SALESDOCUMENTLINE.NETVALUE AS CHALLANNETVALUE  " \
    #       "            , BP_Trpt.Legalname1 AS TRANSPORTERNAME  " \
    #       "            , PLANTINVOICELINE.NUMBEROFBALES DIRECT_BOXES  " \
    #       "           , TermsOfShipping.LONGDESCRIPTION AS SUPPLYMODE  " \
    #       "           , DIVISION.code as DIVISIONCODE   " \
    #       "           , COALESCE(COMPANYBANK.CURRENTACCOUNTID,'') AS ACCOUNTNUMBER   " \
    #       "           , COALESCE(BANK.BIC,'') AS BANKIFSCCODE  " \
    #       "           , COALESCE(BANK.LONGDESCRIPTION,'') AS BANKNAME  " \
    #       "           , COALESCE(BANK.BANKBRANCHADDRESS,'') AS BRANCHNAME " \
    #       "           , count(*) over(partition by ST.ContainerElementCode)  as TOTALCHALLANINBOX " \
    #       "             ,sum(PLANTINVOICELINE.PRIMARYQTY) as TotalQUANTITY" \
    #       "    From PlantInvoice   " \
    #       "    JOIN SALESDOCUMENT      ON PLANTINVOICE.CODE                            = SALESDOCUMENT.PROVISIONALCODE  " \
    #       "                            and SALESDOCUMENT.DocumentTypeType = '06'  " \
    #       "    JOIN DIVISION                           ON PLANTINVOICE.DIVISIONCODE    = DIVISION.CODE  " \
    #       "    JOIN ADDRESS REGD_ADDRESS               ON Division.AbsUniqueId = REGD_ADDRESS.UniqueId And REGD_ADDRESS.Code = 'REGD'  " \
    #       "    JOIN ADDRESS CORP_ADDRESS               ON Division.AbsUniqueId = CORP_ADDRESS.UniqueId And CORP_ADDRESS.Code = 'CORP'  " \
    #       "    join OrderPartner               On      PlantInvoice.BUYERIFOTCCUSTOMERSUPPLIERCODE = OrderPartner.CustomerSupplierCode  " \
    #       "                                    And     PlantInvoice.BUYERIFOTCCUSTOMERSUPPLIERTYPE = OrderPartner.CustomerSupplierType  " \
    #       "    join BusinessPartner            On      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID   " \
    #       "    JOIN AddressGst   CUSTOMERGSTIN  ON      CUSTOMERGSTIN.UniqueID = BusinessPartner.AbsUniqueId  " \
    #       "    Left join OrderPartner OP_Consig On      PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERCODE = OP_Consig.CustomerSupplierCode  " \
    #       "                                    And     PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERTYPE = OP_Consig.CustomerSupplierType   " \
    #       "    LEFT JOIN OrderPartner OP_Customername on PLANTINVOICE.BUYERIFOTCCUSTOMERSUPPLIERCODE = OP_Customername. CustomerSupplierCode   " \
    #       "                                    AND  PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERTYPE = OP_Customername.CustomerSupplierType  " \
    #       "    Left join BusinessPartner BP_Consig On      OP_Consig.OrderbusinessPartnerNumberId = BP_Consig.NumberID    " \
    #       "    join OrderPartner CUSTOMER_PANNO         On      PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERCODE = CUSTOMER_PANNO.CustomerSupplierCode  " \
    #       "                                        And     PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERTYPE = CUSTOMER_PANNO.CustomerSupplierType  " \
    #       "    JOIN ORDERPARTNERIE                    ON ORDERPARTNERIE.CUSTOMERSUPPLIERCOMPANYCODE = CUSTOMER_PANNO.CUSTOMERSUPPLIERCOMPANYCODE " \
    #       "                                      AND  ORDERPARTNERIE.CUSTOMERSUPPLIERTYPE = CUSTOMER_PANNO.CUSTOMERSUPPLIERTYPE   " \
    #       "                                      AND  ORDERPARTNERIE.CUSTOMERSUPPLIERCODE = CUSTOMER_PANNO.CUSTOMERSUPPLIERCODE   " \
    #       "    LEFT JOIN Address ADDRESS_Consignee ON      BP_Consig.ABSUNIQUEID         = ADDRESS_Consignee.UNIQUEID   " \
    #       "                                    AND     PLANTINVOICE.DELIVERYPOINTCODE    = ADDRESS_Consignee.CODE     " \
    #       " left   JOIN STATE STATEGST              ON     CUSTOMERGSTIN.STATECODE= STATEGST.CODE   " \
    #       "    JOIN AGENT         ON PLANTINVOICE.AGENT1CODE = AGENT.CODE   " \
    #       "    Left join OrderPartner OP_Trpt     On      PLANTINVOICE.TRANSPORTERCODCSMSUPPLIERTYPE = OP_Trpt.CUSTOMERSUPPLIERTYPE   " \
    #       "                                       And     PLANTINVOICE.TRANSPORTERCODCSMSUPPLIERCODE = OP_Trpt.CUSTOMERSUPPLIERCODE   " \
    #       "    Left join BusinessPartner BP_Trpt  On      OP_Trpt.OrderbusinessPartnerNumberId = BP_Trpt.NumberID   " \
    #       "    JOIN SALESDOCUMENTLINE          ON      SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE   " \
    #       "                                    AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE      = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
    #       "    JOIN LOGICALWAREHOUSE           ON      SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE  " \
    #       "    JOIN BusinessUnitVsCompany BUC  ON      SalesDocument.DivisionCode                           = BUC.DivisionCode   " \
    #       "                                    AND     LOGICALWAREHOUSE.plantcode                          = BUC.factorycode   " \
    #       "    JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode                                 = BUnit.Code And BUnit.GroupFlag = 0   " \
    #       "    JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode                                    = Company.Code And Company.GroupFlag = 1   " \
    #       "    JOIN ITEMTYPE                   ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = ITEMTYPE.CODE   " \
    #       "    JOIN QUALITYLEVEL               ON      SALESDOCUMENTLINE.QUALITYCODE                        = QUALITYLEVEL.CODE  " \
    #       "                                    AND     SALESDOCUMENTLINE.ITEMTYPEAFICODE                   = QUALITYLEVEL.ITEMTYPECODE  " \
    #       "   left JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE               = IST.ItemTypeCode   " \
    #       "                                    AND     IST.GroupTypeCode In ('P09','B07') " \
    #       "     JOIN UserGenericGroup UGG      ON      IST.GroupTypeCode                               = UGG.UserGenericGroupTypeCode   " \
    #       "                                AND     Case IST.Position    " \
    #       "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03  " \
    #       "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06   " \
    #       "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09  " \
    #       "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code  " \
    #       "    JOIN PLANTINVOICELINE                   ON PLANTINVOICELINE.PLANTINVOICECODE = PLANTINVOICE.CODE " \
    #       "                                            AND PLANTINVOICELINE.PLANTINVOICEDIVISIONCODE = PLANTINVOICE.DIVISIONCODE   " \
    #       "    JOIN FullItemKeyDecoder FIKD     ON      plantinvoiceLINE.ITEMTYPECODE = FIKD.ITEMTYPECODE " \
    #       "                                AND     COALESCE(plantinvoiceLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '')  " \
    #       "                                AND     COALESCE(plantinvoiceLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
    #       "                                AND     COALESCE(plantinvoiceLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
    #       "                                AND     COALESCE(plantinvoiceLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
    #       "                                AND     COALESCE(plantinvoiceLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '')  " \
    #       "                                AND     COALESCE(plantinvoiceLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '')  " \
    #       "                                AND     COALESCE(plantinvoiceLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
    #       "                                AND     COALESCE(plantinvoiceLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
    #       "                                AND     COALESCE(plantinvoiceLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '')  " \
    #       "                                AND     COALESCE(plantinvoiceLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '')  " \
    #       "    Join Product                On      plantinvoiceLINE.ITEMTYPECODE           = Product.ITEMTYPECODE    " \
    #       "                                And     FIKD.ItemUniqueId                           = Product.AbsUniqueId   " \
    #       "    JOIN PLANT                   ON     LOGICALWAREHOUSE.plantcode                 = PLANT.CODE    " \
    #       "    JOIN FACTORY                 ON     PLANT.CODE = FACTORY.CODE    " \
    #       "    JOIN ADDRESSGST ADGSTIN     ON     FACTORY.ABSUNIQUEID = ADGSTIN.UNIQUEID  " \
    #       "    JOIN TermsOfShipping                    ON      PLANTINVOICE.TERMSOFSHIPPINGCODE=TermsOfShipping.CODE   " \
    #       "    left JOIN Transportzone TZ_DespTo       on      ADDRESS_Consignee.TRANSPORTZONECODE     = TZ_DespTo.code " \
    #       "    left JOIN Transportzone TZ_DespFrom     on      Plant.TRANSPORTZONECODE     = TZ_DespFrom.code  " \
    #       "    JOIN FIRM                               ON      plantinvoice.DIVISIONCODE = FIRM.CODE    " \
    #       "    left JOIN Adstorage         ABS_LRNO         ON PLANTINVOICE.ABSUNIQUEID = ABS_LRNO.ABSUNIQUEID   " \
    #       "                                            AND ABS_LRNO.NAMEENTITYNAME = 'PlantInvoice' And ABS_LRNO.NameName = 'LRNo' And ABS_LRNO.FieldName = 'LRNo'   " \
    #       "    left JOIN Adstorage         ABS_LRDATE        ON PLANTINVOICE.ABSUNIQUEID = ABS_LRDATE.ABSUNIQUEID   " \
    #       "                                            AND ABS_LRDATE.NAMEENTITYNAME = 'PlantInvoice' And ABS_LRDATE.NameName = 'LRDATE' And ABS_LRNO.FieldName = 'LRDate'  " \
    #       "    LEFT JOIN ADSTORAGE                     ON      PLANTINVOICE.ABSUNIQUEID = ADSTORAGE.ABSUNIQUEID " \
    #       "    Join SalesDocumentLine PILine      On      PILine.DocumentTypeType         = '06' " \
    #       "                                 And     PILine.SALESDOCUMENTProvisionalCode     = SALESDOCUMENT.ProvisionalCode " \
    #       "   Join StockTransaction ST        On     PILine.PreviousCode      = ST.OrderCode " \
    #       "                             And    PILine.PreviousDocumentTypeType         = '05' " \
    #       "                             And    ST.TemplateCode          = 'S04' " \
    #       "                             And     PILine.OrderLine = ST.OrderLine " \
    #       "                             and    ST.TRANSACTIONDETAILNUMBER =1 " \
    #       " Join    BKLElements Boxes    On      ST.ContainerElementCode                    = Boxes.Code " \
    #       " LEFT Join LOT                 On      St.LotCode = Lot.Code "\
    #       " LEFT Join AdStorage ADS_SaleLot     ON      Lot.AbsUniqueID = ADS_SaleLot.AbsUniqueId " \
    #       "                                 AND     ADS_SaleLot.NameEntityName = 'Lot' And ADS_SaleLot.NameName = 'SaleLot' And ADS_SaleLot.FieldName = 'SaleLot' " \
    #       "     JOIN IndTaxDetail ItemAmt               ON      PLANTINVOICELINE.AbsUniqueID = ItemAmt.AbsUniqueID  " \
    #       "                                            And     ItemAmt.ITaxCOde = 'PPU' And ItemAmt.TaxCategoryCode = 'OTH'  " \
    #       "    JOIN INDTAXDETAIL InvRate               ON PlantInvoiceLine.ABSUNIQUEID         =       InvRate.ABSUNIQUEID   " \
    #       "                                            AND InvRate.itaxcode ='DNV' AND InvRate.TAXCATEGORYCODE = 'OTH'  " \
    #       "    LEFT JOIN COMPANYBANK                   ON Cast(DIVISION.code As Int) =  COMPANYBANK.Priority   " \
    #       "    Left JOIN BANK                          ON COMPANYBANK.BANKCODE                 = BANK.CODE   " \
    #       "                                            AND CompanyBank.BankBranchCode = Bank.BranchCode   " \
    #       "WHERE SALESDOCUMENT.DocumentTypeType = '06' "+LSInvoiceChallanNo +"" \
    #       "GROUP BY REGD_ADDRESS.addressline1   , REGD_ADDRESS.addressline2    , REGD_ADDRESS.addressline3  ,COMMISSIONERATE  " \
    #      ", REGD_ADDRESS.addressline4    , REGD_ADDRESS.addressline5     , REGD_ADDRESS.postalcode  " \
    #      ", CORP_ADDRESS.addressline1    , CORP_ADDRESS.addressline2    , CORP_ADDRESS.addressline3   " \
    #      " , CORP_ADDRESS.addressline4    , CORP_ADDRESS.addressline5    , CORP_ADDRESS.postalcode " \
    #      ", PLANTINVOICE.CODE    , PLANTINVOICE.CONTRACTNOCODE    , PlantInvoice.TIMEOFREMOVALOFGOODS    " \
    #      "   , PlantInvoice.TIMEOFREMOVALOFGOODS   , COMPANY.LONGDESCRIPTION       " \
    #      ", SALESDOCUMENTLINE.PreviousCode   , agent.LONGDESCRIPTION   , Product.LONGDESCRIPTION  " \
    #      ", QualityLevel.ShortDescription  , UGG.Code , UGG.LONGDESCRIPTION  , BusinessPartner.LEGALNAME1    " \
    #      ", BusinessPartner.ADDRESSLINE1    , BusinessPartner.ADDRESSLINE2    , BusinessPartner.ADDRESSLINE3   " \
    #      " , BusinessPartner.ADDRESSLINE4    , BusinessPartner.ADDRESSLINE5   , BusinessPartner.POSTALCODE   " \
    #      ", BP_Consig.LEGALNAME1  , ADDRESS_Consignee.ADDRESSLINE1    , ADDRESS_Consignee.ADDRESSLINE2  " \
    #      " , ADDRESS_Consignee.ADDRESSLINE3    , ADDRESS_Consignee.ADDRESSLINE4    , ADDRESS_Consignee.ADDRESSLINE5  " \
    #      "  , ADDRESS_Consignee.POSTALCODE   , PLANTINVOICE.LRNO   , TZ_DespFrom.LONGDESCRIPTION   " \
    #      " , TZ_DespTo.LONGDESCRIPTION    , Plant.AddressLine1    , ABS_LRNO.ValueString    " \
    #      ", ABS_LRDATE.ValueString , St.LotCode  , ADS_SaleLot.ValueString , Firm.TINNo " \
    #      "   , ADGSTIN.GSTINNUMBER   , FIRM.PANNO    , FIRM.EmailAddress   , FIRM.ADDRESSFAXNUMBER " \
    #      " , CUSTOMERGSTIN.GSTINNumber   , CUSTOMERGSTIN.STATECODE   , STATEGST.LONGDESCRIPTION  " \
    #      " , PLANTINVOICELINE.TARIFFCODE , PLANTINVOICE.TRUCKNO    ,  InvRate.calculatedvalueRCC " \
    #      "  , Itemamt.calculatedvalueRCC   , PLANTINVOICE.NETTVALUE   , PLANTINVOICE.IRN  " \
    #      "    , PLANTINVOICE.ROUNDOFFVALUE " \
    #      "  , PLANTINVOICELINE.PRIMARYQTY      , plantinvoiceLINE.PRIMARYUMCODE    , plantinvoice.TYPEFOREINVOICE" \
    #      " , SALESDOCUMENTLINE.USERPRIMARYQUANTITY    , SALESDOCUMENTLINE.USERPRIMARYUOMCODE    , BP_Trpt.Legalname1 " \
    #      "   , PLANTINVOICELINE.NUMBEROFBALES    , TermsOfShipping.LONGDESCRIPTION    , DIVISION.code  " \
    #      "  , COMPANYBANK.CURRENTACCOUNTID    , BANK.BIC    , BANK.LONGDESCRIPTION    , BANK.BANKBRANCHADDRESS " \
    #      ", SALESDOCUMENTLINE.PRICE, PLANTINVOICE.BASICVALUE  ,plantinvoice.BUYERSPOREFNO" \
    #      ",plantinvoice.BUYERSPOREFNO ,salesdocument.INTERNALREFERENCE , plantinvoice.EXPORTERREFNO , PlantInvoice.TIMEOFREMOVALOFGOODS" \
    #      ",ST.ContainerElementCode, SALESDOCUMENTLINE.NETVALUE, PLANTINVOICE.EWBNO, PLANTINVOICE.EWBDT ,PLANTINVOICE.INVOICEDATE,PLANTINVOICE.INVOICEISSUETIME " \
    #       "ORDER BY PLANTINVOICE.CODE"
    sql = " SELECT  Coalesce(REGD_ADDRESS.addressline1,'')  " \
          "        || Coalesce(','||REGD_ADDRESS.addressline2,'') " \
          "        || Coalesce(','||REGD_ADDRESS.addressline3,'') " \
          "        || Coalesce(','||REGD_ADDRESS.addressline4,'') " \
          "        || Coalesce(','||REGD_ADDRESS.addressline5,'') " \
          "        || Coalesce(','||REGD_ADDRESS.postalcode,'') AS REGD_ADDRESS   " \
          "        , Coalesce(CORP_ADDRESS.addressline1,'') " \
          "        || Coalesce(','||CORP_ADDRESS.addressline2,'') " \
          "        || Coalesce(','||CORP_ADDRESS.addressline3,'') " \
          "        || Coalesce(','||CORP_ADDRESS.addressline4,'') " \
          "        || Coalesce(','||CORP_ADDRESS.addressline5,'') " \
          "        || Coalesce(','||CORP_ADDRESS.postalcode,'') AS CORP_ADDRESS" \
          "        , PLANTINVOICE.CODE AS INVOICENO " \
          "        , VARCHAR_FORMAT(PLANTINVOICE.INVOICEDATE, 'DD-MM-YYYY')    AS INVOICEDATE " \
          "        , Coalesce(PLANTINVOICE.CONTRACTNOCODE,'') AS REFERANCECODE   " \
          "        , Coalesce(plantinvoice.BUYERSPOREFNO,'') AS BUYERREFFERANCEVALUE " \
          "        , Coalesce(salesdocument.INTERNALREFERENCE,'') AS OURREFERANCEVALUE " \
          "        , Coalesce(plantinvoice.EXPORTERREFNO,'') AS EXPORTERREFERANCENUMBER " \
          "        , Coalesce(PlantInvoice.TIMEOFREMOVALOFGOODS,'') AS SUPPLYDATE  " \
          "        , VARCHAR_FORMAT(PLANTINVOICE.INVOICEISSUETIME, 'DD-MM-YYYY')    AS INVOICEISSUEDATE " \
          "        , PlantInvoice.INVOICEISSUETIME AS DATEOFREMOVALOFGOODS   " \
          "        ,  PLANTINVOICE.TOTALNUMBEROFBALES DIRECT_BOXES  " \
          "        , COMPANY.LONGDESCRIPTION AS  companyname   " \
          "        , SALESDOCUMENTLINE.PreviousCode AS CHALLANNUMBER  " \
          "        , agent.LONGDESCRIPTION AS BROKERNAME  " \
          "        , trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS PRODUCT   " \
          "        , TRIM (UGG.Code)  ||' / '||UGG.LONGDESCRIPTION As ShadeCode  " \
          "        , BP_Customer.LEGALNAME1 AS CUSTOMER  " \
          "       , Coalesce(BP_Customer.ADDRESSLINE1,'')  " \
          "        || Coalesce(','||BP_Customer.ADDRESSLINE2,'')    " \
          "        || Coalesce(','||BP_Customer.ADDRESSLINE3,'')    " \
          "        || Coalesce(','||BP_Customer.ADDRESSLINE4,'')    " \
          "        ||','|| Coalesce(BP_Customer.ADDRESSLINE5,'')   " \
          "        ||', Postal Code : '||Coalesce(BP_Customer.POSTALCODE,'')  as CustomerAddress   " \
          "        , COALESCE(BP_Consig.LEGALNAME1,'') AS CONSIGNEEname   " \
          "        , Case When PLANTINVOICE.DELIVERYPOINTCODE Is Null Then " \
          "        Coalesce(BP_Consig.ADDRESSLINE1,'')    " \
          "        || Coalesce(','||BP_Consig.ADDRESSLINE2,'')  " \
          "        || Coalesce(','||BP_Consig.ADDRESSLINE3,'')  " \
          "        || Coalesce(','||BP_Consig.ADDRESSLINE4,'')  " \
          "        ||','|| Coalesce(BP_Consig.ADDRESSLINE5,'')  " \
          "        ||', Postal Code : '||Coalesce(ADDRESS_Consignee.POSTALCODE,'')  " \
          "        Else " \
          "        Coalesce(ADDRESS_Consignee.ADDRESSLINE1,'')    " \
          "        || Coalesce(','||ADDRESS_Consignee.ADDRESSLINE2,'') " \
          "        || Coalesce(','||ADDRESS_Consignee.ADDRESSLINE3,'') " \
          "        || Coalesce(','||ADDRESS_Consignee.ADDRESSLINE4,'') " \
          "        ||','|| Coalesce(ADDRESS_Consignee.ADDRESSLINE5,'') " \
          "        ||', Postal Code : '||Coalesce(ADDRESS_Consignee.POSTALCODE,'')  " \
          "        End as CONSIGNEEADDRESS " \
          "        , Coalesce(TZ_DespFrom.LONGDESCRIPTION,'') as DespFRom " \
          "        , Case When PLANTINVOICE.DELIVERYPOINTCODE Is Null Then   " \
          "                 Coalesce(Coalesce(TZ_DespTo.LONGDESCRIPTION,BP_DespTo.LONGDESCRIPTION),'')  " \
          "        else " \
          "             Coalesce(BP_DespTo.LONGDESCRIPTION,'')  " \
          "        end as DespTO " \
          "        , Plant.AddressLine1 AS PlantAddress " \
          "        , Coalesce(ABS_LRNO.ValueString,'') AS LRNO  " \
          "        , Coalesce(ABS_LRDATE.ValueString,'') AS  LRDATE " \
          "        , Coalesce(ADS_SaleLot.ValueString,St.LotCode) As LOTNUMBER " \
          "        , Firm.TINNo AS CINNO  " \
          "        , ADGSTIN.GSTINNUMBER AS COMPANYGSTINNO " \
          "        , FIRM.PANNO As COMPANYPANNO  " \
          "        , FIRM.EmailAddress AS COMPANYEMAIL   " \
          "        , FIRM.ADDRESSFAXNUMBER As COMPANYWebUrl   " \
          "        , Coalesce(COMMISSIONERATE,'') as CUSTOMERPAN   " \
          "        , CUSTOMERGSTIN.GSTINNumber AS CUSTOMERGST   " \
          "        , CUSTOMERGSTIN.STATECODE AS GSTSTATECODE   " \
          "        , STATEGST.LONGDESCRIPTION AS GSTSTATE   " \
          "        , PLANTINVOICELINE.TARIFFCODE AS HSNCODE " \
          "        , PLANTINVOICELINE.PRIMARYQTY AS QUANTITY " \
          "        , plantinvoiceLINE.PRIMARYUMCODE AS UOM " \
          "        , Coalesce(PLANTINVOICE.TRUCKNO,'') AS TRUCKNO  " \
          "        , PLANTINVOICE.BASICVALUE as BASICVALUE " \
          "        , PLANTINVOICE.NETTVALUE As InvoiceAmt   " \
          "        , Coalesce(PLANTINVOICE.IRN,'') as IRNVALUE  " \
          "        , Coalesce(PLANTINVOICE.EWBNO,'') AS EWAYBILL   " \
          "        , Coalesce(PLANTINVOICE.EWBDT,'') AS EWAYBILLDATE  " \
          "        , PLANTINVOICE.ROUNDOFFVALUE  " \
          "        , plantinvoice.TYPEFOREINVOICE as INVOICETYPE   " \
          "        , SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS CHALLANQUANTITY " \
          "        , SALESDOCUMENTLINE.USERPRIMARYUOMCODE AS CHALLANUOM  " \
          "        , BP_Trpt.Legalname1 AS TRANSPORTERNAME  " \
          "        , TermsOfShipping.LONGDESCRIPTION AS SUPPLYMODE  " \
          "        , DIVISION.code as DIVISIONCODE   " \
          "        , COMPANYBANK.CURRENTACCOUNTID AS ACCOUNTNUMBER  " \
          "        , BANK.BIC AS BANKIFSCCODE   " \
          "        , BANK.LONGDESCRIPTION AS BANKNAME  " \
          "        , BANK.BANKBRANCHADDRESS AS BRANCHNAME  " \
          "    From PlantInvoice " \
          "    JOIN SALESDOCUMENT      ON PLANTINVOICE.CODE                            = SALESDOCUMENT.PROVISIONALCODE " \
          "                            and SALESDOCUMENT.DocumentTypeType = '06' " \
          "    JOIN DIVISION                           ON PLANTINVOICE.DIVISIONCODE    = DIVISION.CODE  " \
          "    JOIN ADDRESS REGD_ADDRESS               ON Division.AbsUniqueId = REGD_ADDRESS.UniqueId And REGD_ADDRESS.Code = 'REGD' " \
          "    JOIN ADDRESS CORP_ADDRESS               ON Division.AbsUniqueId = CORP_ADDRESS.UniqueId And CORP_ADDRESS.Code = 'CORP'  " \
          "    JOIN OrderPartner OP_Customername 		on PLANTINVOICE.BUYERIFOTCCUSTOMERSUPPLIERCODE = OP_Customername. CustomerSupplierCode  " \
          "											AND  PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERTYPE = OP_Customername.CustomerSupplierType   " \
          "    join BusinessPartner BP_Customer 		On      OP_Customername.OrderbusinessPartnerNumberId = BP_Customer.NumberID " \
          "    JOIN AddressGst   CUSTOMERGSTIN  		ON      CUSTOMERGSTIN.UniqueID = BP_Customer.AbsUniqueId  " \
          "    join OrderPartner OP_Consig        		 On      PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERCODE = OP_Consig.CustomerSupplierCode  " \
          "											And     PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERTYPE = OP_Consig.CustomerSupplierType   " \
          "    join BusinessPartner BP_Consig 			On      OP_Consig.OrderbusinessPartnerNumberId = BP_Consig.NumberID   " \
          "    join OrderPartner CUSTOMER_PANNO         On      PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERCODE = CUSTOMER_PANNO.CustomerSupplierCode  " \
          "											And     PLANTINVOICE.CONSIGNEECUSTOMERSUPPLIERTYPE = CUSTOMER_PANNO.CustomerSupplierType  " \
          "    JOIN ORDERPARTNERIE                    ON ORDERPARTNERIE.CUSTOMERSUPPLIERCOMPANYCODE = CUSTOMER_PANNO.CUSTOMERSUPPLIERCOMPANYCODE  " \
          "											AND  ORDERPARTNERIE.CUSTOMERSUPPLIERTYPE = CUSTOMER_PANNO.CUSTOMERSUPPLIERTYPE    " \
          "											AND  ORDERPARTNERIE.CUSTOMERSUPPLIERCODE = CUSTOMER_PANNO.CUSTOMERSUPPLIERCODE    " \
          "	left JOIN Address ADDRESS_Consignee 	ON      BP_Consig.ABSUNIQUEID         = ADDRESS_Consignee.UNIQUEID   " \
          "											AND     PLANTINVOICE.DELIVERYPOINTCODE    = ADDRESS_Consignee.CODE " \
          "	left    JOIN STATE STATEGST             ON     CUSTOMERGSTIN.STATECODE= STATEGST.CODE  " \
          "	left    JOIN AGENT         				ON PLANTINVOICE.AGENT1CODE = AGENT.CODE   " \
          "   Left join OrderPartner OP_Trpt     On      PLANTINVOICE.TRANSPORTERCODCSMSUPPLIERTYPE = OP_Trpt.CUSTOMERSUPPLIERTYPE  " \
          "                                       And     PLANTINVOICE.TRANSPORTERCODCSMSUPPLIERCODE = OP_Trpt.CUSTOMERSUPPLIERCODE  " \
          "    Left join BusinessPartner BP_Trpt  On      OP_Trpt.OrderbusinessPartnerNumberId = BP_Trpt.NumberID " \
          "    JOIN SALESDOCUMENTLINE          ON      SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE   " \
          "                                    AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE      = SALESDOCUMENT.PROVISIONALCOUNTERCODE  " \
          "                                    and     SALESDOCUMENTline.DocumentTypeType = '06'  " \
          "    join salesdocumentline sdline05 on      sdline05.salesdocumentprovisionalcode = SALESDOCUMENTLINE.PreviousCode " \
          "                                    and     sdline05.documenttypetype='05' " \
          "    Join stocktransaction ST        On      ST.OrderCode = sdline05.salesdocumentprovisionalcode " \
          "                                    And     St.TemplateCode = 'S04' " \
          "                                    And    SDLINE05.OrderLine = ST.OrderLine " \
          "                                    and    ST.TRANSACTIONDETAILNUMBER =1  " \
          "    JOIN LOGICALWAREHOUSE           ON      SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE " \
          "    JOIN BusinessUnitVsCompany BUC  ON      SalesDocument.DivisionCode                       = BUC.DivisionCode   " \
          "                                    AND     LOGICALWAREHOUSE.plantcode                       = BUC.factorycode " \
          "    JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode                             = BUnit.Code And BUnit.GroupFlag = 0   " \
          "    JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode                                = Company.Code And Company.GroupFlag = 1   " \
          "    JOIN ITEMTYPE                   ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE                = ITEMTYPE.CODE  " \
          "    JOIN QUALITYLEVEL               ON      SALESDOCUMENTLINE.QUALITYCODE                    = QUALITYLEVEL.CODE  " \
          "                                    AND     SALESDOCUMENTLINE.ITEMTYPEAFICODE                = QUALITYLEVEL.ITEMTYPECODE  " \
          "    left JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE           = IST.ItemTypeCode   " \
          "                                    AND     IST.GroupTypeCode In ('P09','B07') " \
          "    left JOIN UserGenericGroup UGG      ON      IST.GroupTypeCode                            = UGG.UserGenericGroupTypeCode  " \
          "                                AND     Case IST.Position   " \
          "        When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03  " \
          "        When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06  " \
          "        When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09  " \
          "        When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code   " \
          "    JOIN PLANTINVOICELINE                   ON PLANTINVOICELINE.PLANTINVOICECODE = PLANTINVOICE.CODE  " \
          "                                            AND PLANTINVOICELINE.PLANTINVOICEDIVISIONCODE = PLANTINVOICE.DIVISIONCODE   " \
          "                                            AND PLANTINVOICELINE.ITEMTYPECODE = SALESDOCUMENTLINE.ITEMTYPEAFICODE   " \
          "                                         AND  COALESCE(PLANTINVOICELINE.SubCode01, '') = COALESCE(SALESDOCUMENTLINE.SubCode01, '') " \
          "                                          AND     COALESCE(PLANTINVOICELINE.SubCode02, '') = COALESCE(SALESDOCUMENTLINE.SubCode02, '') " \
          "                                          AND    COALESCE(PLANTINVOICELINE.SubCode03, '') = COALESCE(SALESDOCUMENTLINE.SubCode03, '') " \
          "                                          AND    COALESCE(PLANTINVOICELINE.SubCode04, '') = COALESCE(SALESDOCUMENTLINE.SubCode04, '') " \
          "                                          AND    COALESCE(PLANTINVOICELINE.SubCode05, '') = COALESCE(SALESDOCUMENTLINE.SubCode05, '') " \
          "                                          AND    COALESCE(PLANTINVOICELINE.SubCode06, '') = COALESCE(SALESDOCUMENTLINE.SubCode06, '') " \
          "                                          AND    COALESCE(PLANTINVOICELINE.SubCode07, '') = COALESCE(SALESDOCUMENTLINE.SubCode07, '') " \
          "                                          AND    COALESCE(PLANTINVOICELINE.SubCode08, '') = COALESCE(SALESDOCUMENTLINE.SubCode08, '') " \
          "                                          AND    COALESCE(PLANTINVOICELINE.SubCode09, '') = COALESCE(SALESDOCUMENTLINE.SubCode09, '') " \
          "                                          AND    COALESCE(PLANTINVOICELINE.SubCode10, '') = COALESCE(SALESDOCUMENTLINE.SubCode10, '') " \
          "	 JOIN FullItemKeyDecoder FIKD     ON      PLANTINVOICELINE.ITEMTYPECODE = FIKD.ITEMTYPECODE  " \
          "                                AND     COALESCE(PLANTINVOICELINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "                                AND     COALESCE(PLANTINVOICELINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "                                AND     COALESCE(PLANTINVOICELINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "                                AND     COALESCE(PLANTINVOICELINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "                                AND     COALESCE(PLANTINVOICELINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "                                AND     COALESCE(PLANTINVOICELINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "                                AND     COALESCE(PLANTINVOICELINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "                                AND     COALESCE(PLANTINVOICELINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "                                AND     COALESCE(PLANTINVOICELINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "                                AND     COALESCE(PLANTINVOICELINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "    Join Product                On      PLANTINVOICELINE.ITEMTYPECODE           = Product.ITEMTYPECODE  " \
          "                                And     FIKD.ItemUniqueId                          = Product.AbsUniqueId  " \
          "    JOIN PLANT                   ON     LOGICALWAREHOUSE.plantcode                 = PLANT.CODE   " \
          "    JOIN FACTORY                 ON     PLANT.CODE = FACTORY.CODE  " \
          "   left    JOIN ADDRESSGST ADGSTIN     ON     FACTORY.ABSUNIQUEID = ADGSTIN.UNIQUEID   " \
          "    JOIN TermsOfShipping                    ON      PLANTINVOICE.TERMSOFSHIPPINGCODE=TermsOfShipping.CODE  " \
          "    left JOIN Transportzone TZ_DespTo       on      ADDRESS_Consignee.TRANSPORTZONECODE     = TZ_DespTo.code  " \
          "    left JOIN Transportzone TZ_DespFrom     on      Plant.TRANSPORTZONECODE                 = TZ_DespFrom.code  " \
          "    left JOIN Transportzone BP_DespTo       on      BP_Consig.TRANSPORTZONECODE     = BP_DespTo.code " \
          "    JOIN FIRM                               ON      plantinvoice.DIVISIONCODE = FIRM.CODE  " \
          "    left JOIN Adstorage         ABS_LRNO    ON      PLANTINVOICE.ABSUNIQUEID = ABS_LRNO.UNIQUEID   " \
          "                                            AND     ABS_LRNO.NAMEENTITYNAME = 'PlantInvoice' And ABS_LRNO.NameName = 'LRNo' And ABS_LRNO.FieldName = 'LRNo'  " \
          "    left JOIN Adstorage         ABS_LRDATE  ON      PLANTINVOICE.ABSUNIQUEID = ABS_LRDATE.UNIQUEID  " \
          "                                            AND     ABS_LRDATE.NAMEENTITYNAME = 'PlantInvoice' And ABS_LRDATE.NameName = 'LRDATE' And ABS_LRNO.FieldName = 'LRDate'   " \
          "    Join    BKLElements Boxes    On      ST.ContainerElementCode                    = Boxes.Code  " \
          "     LEFT Join LOT                 On      ST.LotCode = Lot.Code " \
          "     LEFT Join AdStorage ADS_SaleLot     ON      Lot.AbsUniqueID = ADS_SaleLot.AbsUniqueId " \
          "                                           AND     ADS_SaleLot.NameEntityName = 'Lot' And ADS_SaleLot.NameName = 'SaleLot' And ADS_SaleLot.FieldName = 'SaleLot' " \
          "    LEFT JOIN Note                          ON  PlantInvoice.AbsUniqueId            = Note.Fatherid  " \
          "    JOIN Adstorage ADCompanyBank ON PLANTINVOICE.DivisionCode = ADCompanyBank.ValueString " \
          "                        And ADCompanyBank.NameEntityNAme = 'CompanyBank'  " \
          "                        And ADCompanyBank.NameName = 'DivisionCode'  " \
          "                        And ADCompanyBank.FieldName = 'DivisionCodeCode' " \
          "    JOIN CompanyBank COMPANYBANK ON  COMPANYBANK.AbsUniqueId = ADCompanyBank.UniqueID  " \
          "    JOIN BANK               ON COMPANYBANK.BankCode = Bank.Code " \
          "                        AND COMPANYBANK.BankBranchCode = Bank.BranchCode      " \
          " WHERE    " + LSInvoiceChallanNo + " " \
          " ORDER BY PLANTINVOICE.CODE "
    print(LSInvoiceChallanNo)
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    itype=""
    # print("totalinvoiceitem : - "+str(result['TOTALINVOICEITEM']))
    if result != False:
        pdfrptgstinvoice.newrequest()

        while result != False:
            global counter1
            counter1 = counter1 + 1
            pdfrptgstinvoice.textsize(pdfrptgstinvoice.c, result)
            pdfrptgstinvoice.d = pdfrptgstinvoice.dvalue()
            # print("counter from db : "+str(counter1))
            # print(result)
            itype = str(result['INVOICETYPE'])
            # print(result['BUYERREFFERANCEVALUE'])
            result = con.db.fetch_both(stmt)
        # pdfrptgstinvoice.printlasttotal()
        pdfrptgstinvoice.getandprinttaxdeatils(pdfrptgstinvoice.invoiceno[-1],pdfrptgstinvoice.roundoff[-1])
        # pdfrptgstinvoice.getretunableitemdeails('GSD0000021')
        # itype=str(result['INVOICETYPE'])
        if itype != '2':
            pdfrptgstinvoice.getretunableitemdeails(pdfrptgstinvoice.invoiceno[-1])
        print("counter : - "+str(counter1))
        pdfrptgstinvoice.printtotalinwords()
        pdfrptgstinvoice.printtotalmain()
        pdfrptgstinvoice.d = 530

        pdfrptgstinvoice.d = pdfrptgstinvoice.d - 20
        # pdfrptgstinvoice.c.showPage()
        # pdfrptpyboxwise.print("after calling register")

        if counter1 == 0:
            Exceptions = "Note: No Result found according to your selected criteria "
            print("counter = 0")
        else:
            pdfrptgstinvoice.c.showPage()
            pdfrptgstinvoice.c.save()
            pdfrptgstinvoice.newrequest()
            pdfrptgstinvoice.d = pdfrpt.newpage()

    else:
        Exceptions = "Note: Please Select Valid Credentials"
        return

    print("at the end")


