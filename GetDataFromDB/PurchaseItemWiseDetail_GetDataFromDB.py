from Global_Files import Connection_String as con
from PrintPDF import PurchaseItemWiseDetail_PrintPDF as pdfrpt,PurchaseItemWiseSummary_PrintPDF as pdfrpt1
from datetime import datetime
def PurchaseItemWiseDetailSummary_GetData(LSCompany, LSItem, LSQuality,LCCompany,LCItem,LCQuality,LDStartDate, LDEndDate, LSFileName,LSReportType):
    if not LCCompany and not LSCompany or LCCompany:
        LSCompany=" "
    elif LSCompany:
        LSCompany = "AND FINBUSINESSUNIT.CODE in (" + str(LSCompany)[1:-1]+")"

    if not LCItem and not LSItem or LCItem:
        LSItem=" "
    elif LSItem:
        LSItem = "AND PRODUCT.ABSUNIQUEID in (" + str(LSItem)[1:-1]+")"

    if not LCQuality and not LSQuality or LCItem:
        LSQuality=" "
    elif LSQuality:
        LSQuality = "AND QualityLevel.CODE in (" + str(LSQuality)[1:-1]+")"

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    
    sql =  "Select FINBUSINESSUNIT.LONGDESCRIPTION AS DIVCODE "\
        ", Sum(MRNDETAIL.INVOICEQUANTITY) AS QUANTITY "\
        ", Sum(MRNDETAIL.BASICVALUE) AS BASICVALUE "\
        ", PRODUCT.LONGDESCRIPTION AS ITEM "\
        ", Sum(PURCHASEINVOICE.INVOICEAMOUNT) AS BILLAMOUNT"\
        ", FINDOCUMENT.CODE AS FINNO "\
        ", BUSINESSPARTNER.LEGALNAME1 AS SUPPLIER "\
        " FROM MRNHEADER JOIN    DIVISION        ON      MRNHEADER.DIVISIONCODE = DIVISION.CODE  "\
        " JOIN    PURCHASEINVOICE ON      PURCHASEINVOICE.COMPANYCODE=MRNHEADER.COMPANYCODE  "\
        " AND PURCHASEINVOICE.DIVISIONCODE=MRNHEADER.DIVISIONCODE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERTYPE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE  "\
        " AND PURCHASEINVOICE.CODE=MRNHEADER.PURCHASEINVOICECODE "\
        " AND PURCHASEINVOICE.INVOICEDATE= MRNHEADER.PURCHASEINVOICEINVOICEDATE  "\
        " JOIN ORDERPARTNER ON PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE = ORDERPARTNER.CUSTOMERSUPPLIERTYPE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE  "\
        " JOIN BUSINESSPARTNER ON ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID  "\
        " JOIN    FINDOCUMENT     ON      FINDOCUMENT.COMPANYCODE=PURCHASEINVOICE.COMPANYCODE  "\
        " AND FINDOCUMENT.BUSINESSUNITCODE=PURCHASEINVOICE.FINDOCBUSINESSUNITCODE  "\
        " AND FINDOCUMENT.FINANCIALYEARCODE=PURCHASEINVOICE.FINDOCFINANCIALYEARCODE  "\
        " AND FINDOCUMENT.DOCUMENTTEMPLATECODE=PURCHASEINVOIcE.FINDOCTEMPLATECODE  "\
        " AND FINDOCUMENT.CODE=PURCHASEINVOICE.FINDOCCODE  "\
        " JOIN FINBUSINESSUNIT ON FINDOCUMENT.BUSINESSUNITCODE=FINBUSINESSUNIT.CODE"\
        " JOIN    MRNDETAIL       ON      MRNHEADER.COMPANYCODE = MRNDETAIL.MRNHEADERCOMPANYCODE  "\
        " AND MRNHEADER.DIVISIONCODE = MRNDETAIL.MRNHEADERDIVISIONCODE  "\
        " AND MRNHEADER.MRNPREFIXCODE = MRNDETAIL.MRNHEADERMRNPREFIXCODE  "\
        " AND MRNHEADER.CODE =  MRNDETAIL.MRNHEADERCODE  "\
        " JOIN    FullItemKeyDecoder FIKD         ON      MRNDETAIL.ITEMTYPEAFICODE  = FIKD.ITEMTYPECODE  "\
        " AND     COALESCE(MrnDetail.SubCode01, '') = COALESCE(FIKD.SubCode01, '') "\
        " AND     COALESCE(MrnDetail.SubCode02, '') = COALESCE(FIKD.SubCode02, '') "\
        " AND     COALESCE(MrnDetail.SubCode03, '') = COALESCE(FIKD.SubCode03, '') "\
        " AND     COALESCE(MrnDetail.SubCode04, '') = COALESCE(FIKD.SubCode04, '') "\
        " AND     COALESCE(MrnDetail.SubCode05, '') = COALESCE(FIKD.SubCode05, '') "\
        " AND     COALESCE(MrnDetail.SubCode06, '') = COALESCE(FIKD.SubCode06, '') "\
        " AND     COALESCE(MrnDetail.SubCode07, '') = COALESCE(FIKD.SubCode07, '') "\
        " AND     COALESCE(MrnDetail.SubCode08, '') = COALESCE(FIKD.SubCode08, '') "\
        " AND     COALESCE(MrnDetail.SubCode09, '') = COALESCE(FIKD.SubCode09, '') "\
        " AND     COALESCE(MrnDetail.SubCode10, '') = COALESCE(FIKD.SubCode10, '') "\
        " JOIN    PRODUCT                 ON MRNDETAIL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE "\
        " AND FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID  "\
        " Join QualityLevel On Product.QUALITYGROUPCODE = QualityLevel.Code"\
        " And Product.ITEMTYPECODE = QualityLevel.ITEMTYPECODE"\
        " WHERE  FINDOCUMENT.FINANCEDOCUMENTDATE between '"+LDStartDate+"' and '"+LDEndDate+"' " + LSCompany + " " + LSItem + " "+LSQuality+" " \
        " GROUP BY FINBUSINESSUNIT.LONGDESCRIPTION,PRODUCT.LONGDESCRIPTION,BUSINESSPARTNER.LEGALNAME1,FINDOCUMENT.CODE"\
        " ORDER BY DIVCODE,ITEM,SUPPLIER"
    
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(sql)
    if result==False:
        return
    while result != False:
        pdfrpt.sumtextsize(pdfrpt.c, result, pdfrpt.d,stdt,etdt)
        pdfrpt.d=pdfrpt.sumdvalue(stdt,etdt,pdfrpt.sumdivisioncode)
        result = con.db.fetch_both(stmt)
    pdfrpt.boldfonts(9)
    pdfrpt.c.drawString(200,pdfrpt.d, "Item Total : ")
    pdfrpt.c.drawAlignedString(480, pdfrpt.d, str("%.2f" % float(pdfrpt.SumItemQuantityTotal)))
    pdfrpt.c.drawAlignedString(580, pdfrpt.d, str("%.2f" % float(pdfrpt.SumItemAmountTotal)))
    pdfrpt.SumItemAmountTotal=0
    pdfrpt.SumItemQuantityTotal=0
    pdfrpt.d = pdfrpt.dvalue(stdt,etdt,pdfrpt.sumdivisioncode)
    pdfrpt.c.drawString(200, pdfrpt.d, "Grand Total : ")
    pdfrpt.c.drawAlignedString(480, pdfrpt.d, str("%.2f" % float(pdfrpt.SumGrandQuantityTotal)))
    pdfrpt.c.drawAlignedString(580,pdfrpt. d, str("%.2f" % float(pdfrpt.SumGrandAmountTotal)))
    SumGrandQuantityTotal=0
    SumGrandAmountTotal=0
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    # url="file:///D:/Report Development/Generated Reports/Purchase Register/"+LSFileName+".pdf"
    # os.startfile(url)
    pdfrpt.sumnewrequest()
    pdfrpt.d=pdfrpt.newpage()

#####################################################################################################################################################################################
#####################################################################################################################################################################################
#####################################################################################################################################################################################
#####################################################################################################################################################################################
##################################################################################################################################################################################### 

def PurchaseItemWiseDetail_GetData(LSCompany, LSItem, LSQuality,LCCompany,LCItem,LCQuality,LDStartDate, LDEndDate, LSFileName,LSReportType):
    
    if not LCCompany and not LSCompany or LCCompany:
        LSCompany=" "
    elif LSCompany:
        LSCompany = "AND FINBUSINESSUNIT.CODE in (" + str(LSCompany)[1:-1]+")"

    if not LCItem and not LSItem or LCItem:
        LSItem=" "
    elif LSItem:
        LSItem = "AND PRODUCT.ABSUNIQUEID in (" + str(LSItem)[1:-1]+")"

    if not LCQuality and not LSQuality or LCItem:
        LSQuality=" "
    elif LSQuality:
        LSQuality = "AND QualityLevel.CODE in (" + str(LSQuality)[1:-1]+")"

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    
    sql =  "Select FINBUSINESSUNIT.LONGDESCRIPTION AS DIVCODE "\
        " , MRNDETAIL.INVOICEQUANTITY AS QUANTITY "\
        ", MRNDETAIL.UNITPRICE AS RATE  "\
        ", MRNDETAIL.BASICVALUE AS BASICVALUE "\
        ", MRNHEADER.CODE AS MRNNO "\
        ", MRNDETAIL.ABSUNIQUEID AS ID "\
        ", MRNHEADER.MRNDATE AS MRNDATE "\
        ", PRODUCT.LONGDESCRIPTION AS ITEM "\
        ", PURCHASEINVOICE.INVOICEDATE AS BILLDATE"\
        ", PURCHASEINVOICE.CODE AS BILLNO "\
        ", PURCHASEINVOICE.INVOICEAMOUNT AS BILLAMOUNT"\
        ", FINDOCUMENT.CODE AS FINNO "\
        ", FINDOCUMENT.FINANCEDOCUMENTDATE AS FINDATE "\
        ", BUSINESSPARTNER.LEGALNAME1 AS SUPPLIER "\
        " FROM MRNHEADER JOIN    DIVISION        ON      MRNHEADER.DIVISIONCODE = DIVISION.CODE  "\
        " JOIN    PURCHASEINVOICE ON      PURCHASEINVOICE.COMPANYCODE=MRNHEADER.COMPANYCODE  "\
        " AND PURCHASEINVOICE.DIVISIONCODE=MRNHEADER.DIVISIONCODE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERTYPE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE  "\
        " AND PURCHASEINVOICE.CODE=MRNHEADER.PURCHASEINVOICECODE "\
        " AND PURCHASEINVOICE.INVOICEDATE= MRNHEADER.PURCHASEINVOICEINVOICEDATE  "\
        " JOIN ORDERPARTNER ON PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE = ORDERPARTNER.CUSTOMERSUPPLIERTYPE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE  "\
        " JOIN BUSINESSPARTNER ON ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID  "\
        " JOIN    FINDOCUMENT     ON      FINDOCUMENT.COMPANYCODE=PURCHASEINVOICE.COMPANYCODE  "\
        " AND FINDOCUMENT.BUSINESSUNITCODE=PURCHASEINVOICE.FINDOCBUSINESSUNITCODE  "\
        " AND FINDOCUMENT.FINANCIALYEARCODE=PURCHASEINVOICE.FINDOCFINANCIALYEARCODE  "\
        " AND FINDOCUMENT.DOCUMENTTEMPLATECODE=PURCHASEINVOIcE.FINDOCTEMPLATECODE  "\
        " AND FINDOCUMENT.CODE=PURCHASEINVOICE.FINDOCCODE  "\
        " JOIN FINBUSINESSUNIT ON FINDOCUMENT.BUSINESSUNITCODE=FINBUSINESSUNIT.CODE"\
        " JOIN    MRNDETAIL       ON      MRNHEADER.COMPANYCODE = MRNDETAIL.MRNHEADERCOMPANYCODE  "\
        " AND MRNHEADER.DIVISIONCODE = MRNDETAIL.MRNHEADERDIVISIONCODE  "\
        " AND MRNHEADER.MRNPREFIXCODE = MRNDETAIL.MRNHEADERMRNPREFIXCODE  "\
        " AND MRNHEADER.CODE =  MRNDETAIL.MRNHEADERCODE  "\
        " JOIN    FullItemKeyDecoder FIKD         ON      MRNDETAIL.ITEMTYPEAFICODE  = FIKD.ITEMTYPECODE  "\
        " AND     COALESCE(MrnDetail.SubCode01, '') = COALESCE(FIKD.SubCode01, '') "\
        " AND     COALESCE(MrnDetail.SubCode02, '') = COALESCE(FIKD.SubCode02, '') "\
        " AND     COALESCE(MrnDetail.SubCode03, '') = COALESCE(FIKD.SubCode03, '') "\
        " AND     COALESCE(MrnDetail.SubCode04, '') = COALESCE(FIKD.SubCode04, '') "\
        " AND     COALESCE(MrnDetail.SubCode05, '') = COALESCE(FIKD.SubCode05, '') "\
        " AND     COALESCE(MrnDetail.SubCode06, '') = COALESCE(FIKD.SubCode06, '') "\
        " AND     COALESCE(MrnDetail.SubCode07, '') = COALESCE(FIKD.SubCode07, '') "\
        " AND     COALESCE(MrnDetail.SubCode08, '') = COALESCE(FIKD.SubCode08, '') "\
        " AND     COALESCE(MrnDetail.SubCode09, '') = COALESCE(FIKD.SubCode09, '') "\
        " AND     COALESCE(MrnDetail.SubCode10, '') = COALESCE(FIKD.SubCode10, '') "\
        " JOIN    PRODUCT                 ON MRNDETAIL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE "\
        " AND FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID  "\
        " Join QualityLevel On Product.QUALITYGROUPCODE = QualityLevel.Code"\
        " And Product.ITEMTYPECODE = QualityLevel.ITEMTYPECODE"\
        " WHERE  FINDOCUMENT.FINANCEDOCUMENTDATE between '"+LDStartDate+"' and '"+LDEndDate+"' " + LSCompany + " " + LSItem + " "+LSQuality+" " \
        " ORDER BY DIVCODE,ITEM,BILLDATE,SUPPLIER"
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    if result==False:
        return
    while result != False:
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d,stdt,etdt)
        pdfrpt.d=pdfrpt.dvalue(stdt,etdt,pdfrpt.divisioncode)
        result = con.db.fetch_both(stmt)
    pdfrpt.boldfonts(9)
    pdfrpt.c.drawString(200,pdfrpt.d, "Item Total : ")
    pdfrpt.c.drawAlignedString(480, pdfrpt.d, str("%.2f" % float(pdfrpt.ItemQuantityTotal)))
    pdfrpt.c.drawAlignedString(580, pdfrpt.d, str("%.2f" % float(pdfrpt.ItemAmountTotal)))
    pdfrpt.ItemAmountTotal=0
    pdfrpt.ItemQuantityTotal=0
    pdfrpt.d = pdfrpt.dvalue(stdt,etdt,pdfrpt.divisioncode)
    pdfrpt.c.drawString(200, pdfrpt.d, "Grand Total : ")
    pdfrpt.c.drawAlignedString(480, pdfrpt.d, str("%.2f" % float(pdfrpt.GrandQuantityTotal)))
    pdfrpt.c.drawAlignedString(580,pdfrpt. d, str("%.2f" % float(pdfrpt.GrandAmountTotal)))
    GrandQuantityTotal=0
    GrandAmountTotal=0
    pdfrpt.c.showPage()
    pdfrpt.c.save()
    # url="file:///D:/Report Development/Generated Reports/Purchase Register/"+LSFileName+".pdf"
    # os.startfile(url)
    pdfrpt.newrequest()
    pdfrpt.d=pdfrpt.newpage()

#####################################################################################################################################################################################
#####################################################################################################################################################################################
#####################################################################################################################################################################################
#####################################################################################################################################################################################
##################################################################################################################################################################################### 

def PurchaseItemGrpWiseItemSummary_GetData(LSCompany, LSItem, LSQuality,LSPUItemGroup,LCCompany,LCItem,LCQuality,LCPUItemGroup,LDStartDate, LDEndDate, LSFileName,LSReportType):
    
    if not LCCompany and not LSCompany or LCCompany:
        LSCompany=" "
    elif LSCompany:
        LSCompany = "AND FINBUSINESSUNIT.CODE in (" + str(LSCompany)[1:-1]+")"

    if not LCItem and not LSItem or LCItem:
        LSItem=" "
    elif LSItem:
        LSItem = "AND PRODUCT.ABSUNIQUEID in (" + str(LSItem)[1:-1]+")"

    if not LCQuality and not LSQuality or LCItem:
        LSQuality=" "
    elif LSQuality:
        LSQuality = "AND QualityLevel.CODE in (" + str(LSQuality)[1:-1]+")"

    if not LCPUItemGroup and not LSPUItemGroup or LCPUItemGroup:
        LSPUItemGroup=" "
    elif LSPUItemGroup:
        LSPUItemGroup = "AND AdStorage.UNIQUEID in (" + str(LSPUItemGroup)[1:-1]+")"

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    sql = "Select ADStorage.ValueString as ItemGroup,FINBUSINESSUNIT.LONGDESCRIPTION AS DIVCODE "\
        " , sum(MRNDETAIL.INVOICEQUANTITY) AS QUANTITY, DIVISION.Longdescription as Plant"\
        ", Sum(MRNDETAIL.UNITPRICE) AS RATE  "\
        ", sum(MRNDETAIL.BASICVALUE) AS BASICVALUE "\
        ", PRODUCT.LONGDESCRIPTION AS ITEM "\
        " FROM MRNHEADER JOIN    DIVISION        ON      MRNHEADER.DIVISIONCODE = DIVISION.CODE  "\
        " JOIN    PURCHASEINVOICE ON      PURCHASEINVOICE.COMPANYCODE=MRNHEADER.COMPANYCODE  "\
        " AND PURCHASEINVOICE.DIVISIONCODE=MRNHEADER.DIVISIONCODE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERTYPE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE  "\
        " AND PURCHASEINVOICE.CODE=MRNHEADER.PURCHASEINVOICECODE "\
        " AND PURCHASEINVOICE.INVOICEDATE= MRNHEADER.PURCHASEINVOICEINVOICEDATE  "\
        " JOIN ORDERPARTNER ON PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE = ORDERPARTNER.CUSTOMERSUPPLIERTYPE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE  "\
        " JOIN BUSINESSPARTNER ON ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID  "\
        " JOIN    FINDOCUMENT     ON      FINDOCUMENT.COMPANYCODE=PURCHASEINVOICE.COMPANYCODE  "\
        " AND FINDOCUMENT.BUSINESSUNITCODE=PURCHASEINVOICE.FINDOCBUSINESSUNITCODE  "\
        " AND FINDOCUMENT.FINANCIALYEARCODE=PURCHASEINVOICE.FINDOCFINANCIALYEARCODE  "\
        " AND FINDOCUMENT.DOCUMENTTEMPLATECODE=PURCHASEINVOIcE.FINDOCTEMPLATECODE  "\
        " AND FINDOCUMENT.CODE=PURCHASEINVOICE.FINDOCCODE  "\
        " JOIN FINBUSINESSUNIT ON FINDOCUMENT.BUSINESSUNITCODE=FINBUSINESSUNIT.CODE"\
        " JOIN    MRNDETAIL       ON      MRNHEADER.COMPANYCODE = MRNDETAIL.MRNHEADERCOMPANYCODE  "\
        " AND MRNHEADER.DIVISIONCODE = MRNDETAIL.MRNHEADERDIVISIONCODE  "\
        " AND MRNHEADER.MRNPREFIXCODE = MRNDETAIL.MRNHEADERMRNPREFIXCODE  "\
        " AND MRNHEADER.CODE =  MRNDETAIL.MRNHEADERCODE  "\
        " JOIN    FullItemKeyDecoder FIKD         ON      MRNDETAIL.ITEMTYPEAFICODE  = FIKD.ITEMTYPECODE  "\
        " AND     COALESCE(MrnDetail.SubCode01, '') = COALESCE(FIKD.SubCode01, '') "\
        " AND     COALESCE(MrnDetail.SubCode02, '') = COALESCE(FIKD.SubCode02, '') "\
        " AND     COALESCE(MrnDetail.SubCode03, '') = COALESCE(FIKD.SubCode03, '') "\
        " AND     COALESCE(MrnDetail.SubCode04, '') = COALESCE(FIKD.SubCode04, '') "\
        " AND     COALESCE(MrnDetail.SubCode05, '') = COALESCE(FIKD.SubCode05, '') "\
        " AND     COALESCE(MrnDetail.SubCode06, '') = COALESCE(FIKD.SubCode06, '') "\
        " AND     COALESCE(MrnDetail.SubCode07, '') = COALESCE(FIKD.SubCode07, '') "\
        " AND     COALESCE(MrnDetail.SubCode08, '') = COALESCE(FIKD.SubCode08, '') "\
        " AND     COALESCE(MrnDetail.SubCode09, '') = COALESCE(FIKD.SubCode09, '') "\
        " AND     COALESCE(MrnDetail.SubCode10, '') = COALESCE(FIKD.SubCode10, '') "\
        " JOIN    PRODUCT                 ON MRNDETAIL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE "\
        " AND FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID  "\
        " Join QualityLevel On Product.QUALITYGROUPCODE = QualityLevel.Code"\
        " And Product.ITEMTYPECODE = QualityLevel.ITEMTYPECODE"\
        " Join ADStorage ON Product.Absuniqueid = ADStorage.uniqueid"\
        " And ADStorage.FIELDNAME = 'AutogeneratedName'"\
        " WHERE  FINDOCUMENT.FINANCEDOCUMENTDATE between '"+LDStartDate+"' and '"+LDEndDate+"' " + LSCompany + " " + LSItem + " "+LSQuality+" "+LSPUItemGroup+"" \
        " GROUP BY DIVISION.Longdescription,FINBUSINESSUNIT.LONGDESCRIPTION,ADStorage.ValueString,PRODUCT.LONGDESCRIPTION"\
        " ORDER BY DIVCODE,Plant,ITEMgroup,Item"
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    if result==False:
        return
    while result != False:
        pdfrpt1.textsize(pdfrpt1.c, result, pdfrpt1.d,stdt,etdt)
        pdfrpt1.d=pdfrpt1.dvalue(stdt,etdt,pdfrpt1.divisioncode)
        result = con.db.fetch_both(stmt)
    pdfrpt1.boldfonts(9)
    pdfrpt1.c.drawString(200,pdfrpt1.d, "Item Total : ")
    pdfrpt1.c.drawAlignedString(460, pdfrpt1.d, str("%.2f" % float(pdfrpt1.ItemQuantityTotal)))
    pdfrpt1.c.drawAlignedString(540, pdfrpt1.d, str("%.2f" % float(pdfrpt1.ItemAmountTotal)))
    pdfrpt1.ItemAmountTotal=0
    pdfrpt1.ItemQuantityTotal=0
    pdfrpt1.d = pdfrpt1.dvalue(stdt,etdt,pdfrpt1.divisioncode)
    pdfrpt1.c.drawString(200, pdfrpt1.d, "Grand Total : ")
    pdfrpt1.c.drawAlignedString(460, pdfrpt1.d, str("%.2f" % float(pdfrpt1.GrandQuantityTotal)))
    pdfrpt1.c.drawAlignedString(540,pdfrpt1. d, str("%.2f" % float(pdfrpt1.GrandAmountTotal)))
    pdfrpt1.GrandQuantityTotal=0
    pdfrpt1.GrandAmountTotal=0
    pdfrpt1.c.showPage()
    pdfrpt1.c.save()
    # url="file:///D:/Report Development/Generated Reports/Purchase Register/"+LSFileName+".pdf"
    # os.startfile(url)
    pdfrpt1.newrequest()
    pdfrpt1.d=pdfrpt1.newpage()

#####################################################################################################################################################################################
#####################################################################################################################################################################################
#####################################################################################################################################################################################
#####################################################################################################################################################################################
##################################################################################################################################################################################### 

def ProductionItemGrpWiseSummary_GetData(LSCompany, LSItem, LSQuality,LSPRItemGroup,LCCompany,LCItem,LCQuality,LCPRItemGroup,LDStartDate, LDEndDate, LSFileName,LSReportType):
    if not LCCompany and not LSCompany or LCCompany:
        LSCompany=" "
    elif LSCompany:
        LSCompany = "AND FINBUSINESSUNIT.CODE in (" + str(LSCompany)[1:-1]+")"

    if not LCItem and not LSItem or LCItem:
        LSItem=" "
    elif LSItem:
        LSItem = "AND PRODUCT.ABSUNIQUEID in (" + str(LSItem)[1:-1]+")"

    if not LCQuality and not LSQuality or LCItem:
        LSQuality=" "
    elif LSQuality:
        LSQuality = "AND QualityLevel.CODE in (" + str(LSQuality)[1:-1]+")"

    if not LCPRItemGroup and not LSPRItemGroup or LCPRItemGroup:
        LSPRItemGroup=" "
    elif LSPRItemGroup:
        LSPRItemGroup = "AND AdStorage.UNIQUEID in (" + str(LSPRItemGroup)[1:-1]+")"

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    sql = "Select ADStorage.ValueString as ItemGroup,DIVISION.LONGDESCRIPTION AS DIVCODE "\
        " , sum(MRNDETAIL.INVOICEQUANTITY) AS QUANTITY"\
        ", Avg(MRNDETAIL.UNITPRICE) AS RATE  "\
        ", sum(MRNDETAIL.BASICVALUE) AS BASICVALUE "\
        ", BUSINESSPARTNER.LEGALNAME1 AS SUPPLIER "\
        " FROM MRNHEADER JOIN    DIVISION        ON      MRNHEADER.DIVISIONCODE = DIVISION.CODE  "\
        " JOIN    PURCHASEINVOICE ON      PURCHASEINVOICE.COMPANYCODE=MRNHEADER.COMPANYCODE  "\
        " AND PURCHASEINVOICE.DIVISIONCODE=MRNHEADER.DIVISIONCODE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERTYPE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE  "\
        " AND PURCHASEINVOICE.CODE=MRNHEADER.PURCHASEINVOICECODE "\
        " AND PURCHASEINVOICE.INVOICEDATE= MRNHEADER.PURCHASEINVOICEINVOICEDATE  "\
        " JOIN ORDERPARTNER ON PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE = ORDERPARTNER.CUSTOMERSUPPLIERTYPE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE  "\
        " JOIN BUSINESSPARTNER ON ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID  "\
        " JOIN    FINDOCUMENT     ON      FINDOCUMENT.COMPANYCODE=PURCHASEINVOICE.COMPANYCODE  "\
        " AND FINDOCUMENT.BUSINESSUNITCODE=PURCHASEINVOICE.FINDOCBUSINESSUNITCODE  "\
        " AND FINDOCUMENT.FINANCIALYEARCODE=PURCHASEINVOICE.FINDOCFINANCIALYEARCODE  "\
        " AND FINDOCUMENT.DOCUMENTTEMPLATECODE=PURCHASEINVOIcE.FINDOCTEMPLATECODE  "\
        " AND FINDOCUMENT.CODE=PURCHASEINVOICE.FINDOCCODE  "\
        " JOIN FINBUSINESSUNIT ON FINDOCUMENT.BUSINESSUNITCODE=FINBUSINESSUNIT.CODE"\
        " JOIN    MRNDETAIL       ON      MRNHEADER.COMPANYCODE = MRNDETAIL.MRNHEADERCOMPANYCODE  "\
        " AND MRNHEADER.DIVISIONCODE = MRNDETAIL.MRNHEADERDIVISIONCODE  "\
        " AND MRNHEADER.MRNPREFIXCODE = MRNDETAIL.MRNHEADERMRNPREFIXCODE  "\
        " AND MRNHEADER.CODE =  MRNDETAIL.MRNHEADERCODE  "\
        " JOIN    FullItemKeyDecoder FIKD         ON      MRNDETAIL.ITEMTYPEAFICODE  = FIKD.ITEMTYPECODE  "\
        " AND     COALESCE(MrnDetail.SubCode01, '') = COALESCE(FIKD.SubCode01, '') "\
        " AND     COALESCE(MrnDetail.SubCode02, '') = COALESCE(FIKD.SubCode02, '') "\
        " AND     COALESCE(MrnDetail.SubCode03, '') = COALESCE(FIKD.SubCode03, '') "\
        " AND     COALESCE(MrnDetail.SubCode04, '') = COALESCE(FIKD.SubCode04, '') "\
        " AND     COALESCE(MrnDetail.SubCode05, '') = COALESCE(FIKD.SubCode05, '') "\
        " AND     COALESCE(MrnDetail.SubCode06, '') = COALESCE(FIKD.SubCode06, '') "\
        " AND     COALESCE(MrnDetail.SubCode07, '') = COALESCE(FIKD.SubCode07, '') "\
        " AND     COALESCE(MrnDetail.SubCode08, '') = COALESCE(FIKD.SubCode08, '') "\
        " AND     COALESCE(MrnDetail.SubCode09, '') = COALESCE(FIKD.SubCode09, '') "\
        " AND     COALESCE(MrnDetail.SubCode10, '') = COALESCE(FIKD.SubCode10, '') "\
        " JOIN    PRODUCT                 ON MRNDETAIL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE "\
        " AND FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID  "\
        " Join QualityLevel On Product.QUALITYGROUPCODE = QualityLevel.Code"\
        " And Product.ITEMTYPECODE = QualityLevel.ITEMTYPECODE"\
        " Join ADStorage ON Product.Absuniqueid = ADStorage.uniqueid"\
        " And ADStorage.FIELDNAME = 'AutogeneratedName'"\
        " WHERE  FINDOCUMENT.FINANCEDOCUMENTDATE between '"+LDStartDate+"' and '"+LDEndDate+"' " + LSCompany + " " + LSItem + " "+LSQuality+" "+LSPRItemGroup+"" \
        " GROUP BY DIVISION.Longdescription,BUSINESSPARTNER.LEGALNAME1,ADStorage.ValueString"\
        " ORDER BY DIVCODE,ITEMgroup"
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    if result==False:
        return
    while result != False:
        pdfrpt1.prtextsize(pdfrpt1.c, result, pdfrpt1.d,stdt,etdt)
        pdfrpt1.d=pdfrpt1.prdvalue(stdt,etdt,pdfrpt1.prdivisioncode)
        result = con.db.fetch_both(stmt)
    pdfrpt1.boldfonts(9)
    pdfrpt1.c.drawString(200, pdfrpt1.d, "Company Total : ")
    pdfrpt1.c.drawAlignedString(440, pdfrpt1.d, str("%.2f" % float(pdfrpt1.PrCompanyQuantityTotal)))
    pdfrpt1.c.drawAlignedString(520, pdfrpt1.d, str("%.2f" % float(pdfrpt1.PrCompanyAmountTotal)))
    pdfrpt1.c.drawAlignedString(570, pdfrpt1.d, str("%.2f" % float(pdfrpt1.PrItemAmountTotal/pdfrpt1.prcounter)))
    pdfrpt1.d=pdfrpt1.prdvalue(stdt,etdt,pdfrpt1.prdivisioncode)
    pdfrpt1.c.drawString(200, pdfrpt1.d, "Grand Total : ")
    pdfrpt1.c.drawAlignedString(440, pdfrpt1.d, str("%.2f" % float(pdfrpt1.PrGrandQuantityTotal)))
    pdfrpt1.c.drawAlignedString(520,pdfrpt1. d, str("%.2f" % float(pdfrpt1.PrGrandAmountTotal)))
    pdfrpt1.c.drawAlignedString(570, pdfrpt1.d, str("%.2f" % float(pdfrpt1.PrItemQuantityTotal/len(pdfrpt1.prunit))))
    print(pdfrpt1.PrItemQuantityTotal,len(pdfrpt1.prunit))
    pdfrpt1.PrGrandQuantityTotal=0
    pdfrpt1.PrGrandAmountTotal=0
    pdfrpt1.prcounter=0
    pdfrpt1.c.showPage()
    pdfrpt1.c.save()
    # url="file:///D:/Report Development/Generated Reports/Purchase Register/"+LSFileName+".pdf"
    # os.startfile(url)
    pdfrpt1.prnewrequest()
    pdfrpt1.d=pdfrpt1.newpage()

#####################################################################################################################################################################################
#####################################################################################################################################################################################
#####################################################################################################################################################################################
#####################################################################################################################################################################################
##################################################################################################################################################################################### 

def ProductionItemGrpWiseItemSummary_GetData(LSCompany, LSItem, LSQuality,LSPRItemGroup,LCCompany,LCItem,LCQuality,LCPRItemGroup,LDStartDate, LDEndDate, LSFileName,LSReportType):
    if not LCCompany and not LSCompany or LCCompany:
        LSCompany=" "
    elif LSCompany:
        LSCompany = "AND FINBUSINESSUNIT.CODE in (" + str(LSCompany)[1:-1]+")"

    if not LCItem and not LSItem or LCItem:
        LSItem=" "
    elif LSItem:
        LSItem = "AND PRODUCT.ABSUNIQUEID in (" + str(LSItem)[1:-1]+")"

    if not LCQuality and not LSQuality or LCItem:
        LSQuality=" "
    elif LSQuality:
        LSQuality = "AND QualityLevel.CODE in (" + str(LSQuality)[1:-1]+")"

    if not LCPRItemGroup and not LSPRItemGroup or LCPRItemGroup:
        LSPRItemGroup=" "
    elif LSPRItemGroup:
        LSPRItemGroup = "AND AdStorage.UNIQUEID in (" + str(LSPRItemGroup)[1:-1]+")"

    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    sql = "Select ADStorage.ValueString as ItemGroup,DIVISION.LONGDESCRIPTION AS DIVCODE "\
        " , sum(MRNDETAIL.INVOICEQUANTITY) AS QUANTITY"\
        ", Avg(MRNDETAIL.UNITPRICE) AS RATE  "\
        ", sum(MRNDETAIL.BASICVALUE) AS BASICVALUE "\
        ", BUSINESSPARTNER.LEGALNAME1 AS SUPPLIER "\
        ", PRODUCT.LONGDESCRIPTION AS ITEM "\
        " FROM MRNHEADER JOIN    DIVISION        ON      MRNHEADER.DIVISIONCODE = DIVISION.CODE  "\
        " JOIN    PURCHASEINVOICE ON      PURCHASEINVOICE.COMPANYCODE=MRNHEADER.COMPANYCODE  "\
        " AND PURCHASEINVOICE.DIVISIONCODE=MRNHEADER.DIVISIONCODE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERTYPE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE=MRNHEADER.ORDPRNCUSTOMERSUPPLIERCODE  "\
        " AND PURCHASEINVOICE.CODE=MRNHEADER.PURCHASEINVOICECODE "\
        " AND PURCHASEINVOICE.INVOICEDATE= MRNHEADER.PURCHASEINVOICEINVOICEDATE  "\
        " JOIN ORDERPARTNER ON PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERTYPE = ORDERPARTNER.CUSTOMERSUPPLIERTYPE  "\
        " AND PURCHASEINVOICE.ORDPRNCUSTOMERSUPPLIERCODE = ORDERPARTNER.CUSTOMERSUPPLIERCODE  "\
        " JOIN BUSINESSPARTNER ON ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID  "\
        " JOIN    FINDOCUMENT     ON      FINDOCUMENT.COMPANYCODE=PURCHASEINVOICE.COMPANYCODE  "\
        " AND FINDOCUMENT.BUSINESSUNITCODE=PURCHASEINVOICE.FINDOCBUSINESSUNITCODE  "\
        " AND FINDOCUMENT.FINANCIALYEARCODE=PURCHASEINVOICE.FINDOCFINANCIALYEARCODE  "\
        " AND FINDOCUMENT.DOCUMENTTEMPLATECODE=PURCHASEINVOIcE.FINDOCTEMPLATECODE  "\
        " AND FINDOCUMENT.CODE=PURCHASEINVOICE.FINDOCCODE  "\
        " JOIN FINBUSINESSUNIT ON FINDOCUMENT.BUSINESSUNITCODE=FINBUSINESSUNIT.CODE"\
        " JOIN    MRNDETAIL       ON      MRNHEADER.COMPANYCODE = MRNDETAIL.MRNHEADERCOMPANYCODE  "\
        " AND MRNHEADER.DIVISIONCODE = MRNDETAIL.MRNHEADERDIVISIONCODE  "\
        " AND MRNHEADER.MRNPREFIXCODE = MRNDETAIL.MRNHEADERMRNPREFIXCODE  "\
        " AND MRNHEADER.CODE =  MRNDETAIL.MRNHEADERCODE  "\
        " JOIN    FullItemKeyDecoder FIKD         ON      MRNDETAIL.ITEMTYPEAFICODE  = FIKD.ITEMTYPECODE  "\
        " AND     COALESCE(MrnDetail.SubCode01, '') = COALESCE(FIKD.SubCode01, '') "\
        " AND     COALESCE(MrnDetail.SubCode02, '') = COALESCE(FIKD.SubCode02, '') "\
        " AND     COALESCE(MrnDetail.SubCode03, '') = COALESCE(FIKD.SubCode03, '') "\
        " AND     COALESCE(MrnDetail.SubCode04, '') = COALESCE(FIKD.SubCode04, '') "\
        " AND     COALESCE(MrnDetail.SubCode05, '') = COALESCE(FIKD.SubCode05, '') "\
        " AND     COALESCE(MrnDetail.SubCode06, '') = COALESCE(FIKD.SubCode06, '') "\
        " AND     COALESCE(MrnDetail.SubCode07, '') = COALESCE(FIKD.SubCode07, '') "\
        " AND     COALESCE(MrnDetail.SubCode08, '') = COALESCE(FIKD.SubCode08, '') "\
        " AND     COALESCE(MrnDetail.SubCode09, '') = COALESCE(FIKD.SubCode09, '') "\
        " AND     COALESCE(MrnDetail.SubCode10, '') = COALESCE(FIKD.SubCode10, '') "\
        " JOIN    PRODUCT                 ON MRNDETAIL.ITEMTYPEAFICODE = PRODUCT.ITEMTYPECODE "\
        " AND FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID  "\
        " Join QualityLevel On Product.QUALITYGROUPCODE = QualityLevel.Code"\
        " And Product.ITEMTYPECODE = QualityLevel.ITEMTYPECODE"\
        " Join ADStorage ON Product.Absuniqueid = ADStorage.uniqueid"\
        " And ADStorage.FIELDNAME = 'AutogeneratedName'"\
        " WHERE  FINDOCUMENT.FINANCEDOCUMENTDATE between '"+LDStartDate+"' and '"+LDEndDate+"' " + LSCompany + " " + LSItem + " "+LSQuality+" "+LSPRItemGroup+"" \
        " GROUP BY DIVISION.Longdescription,ADStorage.ValueString,Product.Longdescription,BUSINESSPARTNER.LEGALNAME1"\
        " ORDER BY DIVCODE,ITEMgroup,Item,Supplier"
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    if result==False:
        return
    while result != False:
        pdfrpt1.suptextsize(pdfrpt1.c, result, pdfrpt1.d,stdt,etdt)
        pdfrpt1.d=pdfrpt1.supdvalue(stdt,etdt,pdfrpt1.supdivisioncode)
        result = con.db.fetch_both(stmt)
    pdfrpt1.boldfonts(9)
    pdfrpt1.c.drawString(200, pdfrpt1.d, "Item Group Total : ")
    pdfrpt1.c.drawAlignedString(440, pdfrpt1.d, str("%.2f" % float(pdfrpt1.supItemQuantityTotal)))
    pdfrpt1.c.drawAlignedString(520, pdfrpt1.d, str("%.2f" % float(pdfrpt1.supItemAmountTotal)))
    pdfrpt1.c.drawAlignedString(570, pdfrpt1.d, str("%.2f" % float(pdfrpt1.supItemRateTotal/(pdfrpt1.supcounter))))
    d = pdfrpt1.supdvalue(stdt,etdt,pdfrpt1.supdivisioncode)
    pdfrpt1.c.drawString(200, pdfrpt1.d, "Company Total : ")
    pdfrpt1.c.drawAlignedString(440, pdfrpt1.d, str("%.2f" % float(pdfrpt1.supCompanyQuantityTotal)))
    pdfrpt1.c.drawAlignedString(520, pdfrpt1.d, str("%.2f" % float(pdfrpt1.supCompanyAmountTotal)))
    pdfrpt1.c.drawAlignedString(570, pdfrpt1.d, str("%.2f" % float(pdfrpt1.supCompanyRateTotal/pdfrpt1.supcounter1)))
    pdfrpt1.d=pdfrpt1.supdvalue(stdt,etdt,pdfrpt1.supdivisioncode)
    pdfrpt1.c.drawString(200, pdfrpt1.d, "Grand Total : ")
    pdfrpt1.c.drawAlignedString(440, pdfrpt1.d, str("%.2f" % float(pdfrpt1.supGrandQuantityTotal)))
    pdfrpt1.c.drawAlignedString(520,pdfrpt1. d, str("%.2f" % float(pdfrpt1.supGrandAmountTotal)))
    pdfrpt1.c.drawAlignedString(570, pdfrpt1.d, str("%.2f" % float(pdfrpt1.supGrandRateTotal/len(pdfrpt1.supunit))))
    print(pdfrpt1.supItemQuantityTotal,len(pdfrpt1.supunit))
    pdfrpt1.c.showPage()
    pdfrpt1.c.save()
    # url="file:///D:/Report Development/Generated Reports/Purchase Register/"+LSFileName+".pdf"
    # os.startfile(url)
    pdfrpt1.supnewrequest()
    pdfrpt1.d=pdfrpt1.newpage()
