import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
import os.path
from Global_Files import Connection_String as con
from FormLoad import ContractsPendingMis_FormLoad as views

def ContractPendingMisView(request):
    source = request.GET.getlist('src')
    sources = str(source)[1:-1]
    # print(sources)
    contNo = request.GET.getlist('contNo')
    contNos = str(contNo)[1:-1]
    contractNumber = str(contNo)[2:-2]

    contCounter = request.GET.getlist('contCounter')
    contCounters = str(contCounter)[1:-1]
    contractCounter = " And SO.COUNTERCODE = " + contCounters
    # print(contractNumber)
    contractNo = " SO.Code = " + contNos


    GDataView = []
    sql = "Select          SO.DOCUMENTTYPETYPE As DctType  " \
          ", Comp.LONGDESCRIPTION As Company " \
          ", SO.Code as OrdNo" \
          ", SO.DOCUMENTTYPETYPE as OrdDcmTyp" \
          ", Coalesce(PrevOrder.CODE,'') As ContNo" \
          ", Coalesce(PrevOrder.DOCUMENTTYPETYPE,'') As ConDocTyp " \
          ", Bp.LEGALNAME1 AS Customer " \
          ", Coalesce(AGENT.LONGDESCRIPTION, '') As Broker " \
          ", COALESCE(DespTo.LONGDESCRIPTION, '') As Despto " \
          ", SO.CURRENCYCODE As CURRENCYCODE" \
          ", Cast(SO.ENTRYEXCHANGERATE As Decimal(10,3)) As EXRAte " \
          ", Cast(COALESCE(Freight.CALCULATEDVALUERCC,0) As Decimal(20,2)) AS Freight " \
          ", (Case SALESORDERIE.TYPEOFINVOICE When 0 Then 'Domestic' when 2 Then'Export' When 3 Then 'Deemed Export' " \
          "When 4 Then 'Jobwork' when 5 Then 'SEZ' When 6 Then 'Merchant Export' Else 'None' End) As OrdType " \
          ", COALESCE(Narrtn.NOTE, '') As Narration " \
          ", Varchar_Format(SO.ORDERDATE, 'DD-MM-YYYY') As ContDt " \
          ", SOL.ITEMTYPEAFICODE As YarnTYp " \
          ", Product.LONGDESCRIPTION As Item " \
          ", Coalesce(QUALITYLEVEL.LONGDESCRIPTION,'') As Quality " \
          ", Coalesce(UGG.Code,'') As ShadeCode " \
          ", COALESCE(UGG.LONGDESCRIPTION,'') As Shade " \
          ", COALESCE(UGG.CODE,'') As ShadeCode " \
          ", COALESCE(LotNo.VALUESTRING,'') As LotNumber " \
          ", Cast(SOD.USERPRIMARYQUANTITY As Decimal(20,3)) As Qnty " \
          ", Case When  SO.DOCUMENTTYPETYPE <> '03' Or SOL.PREVIOUSCODE is null Then 0 " \
          "Else Coalesce(CAST(PrevOrgnlContRt.CalculatedValueRcc AS Decimal(12,3)),0) End As OriginalContRate	" \
          ", Case When  SO.DOCUMENTTYPETYPE <> '03' Or SOL.PREVIOUSCODE is null Then Coalesce(CAST(ContRate.CalculatedValueRcc AS Decimal(12,3)),0) " \
          "Else Coalesce(CAST(PrevContRt.CalculatedValueRcc AS Decimal(12,3)),0) End As ContractRate " \
          ", Cast(Coalesce(INitilComm.VALUE,0) As Decimal(20,2)) As InitialCommPerc " \
          ", Coalesce(CAST(NetRate.CalculatedValueRcc AS Decimal(12,3)), 0) As NetRate	" \
          ", Cast(COALESCE(BalComm.Value,0) As Decimal(20,2)) As BalCommPerc " \
          ", Cast(Coalesce(DharaRate.VALUE, 0) As Decimal(10,2)) As DRate " \
          ", Coalesce(CAST(BillRate.CalculatedValueRcc AS Decimal(12,3)),0) As BillRate	" \
          ", COALESCE(CrossLuster.LONGDESCRIPTION,'') As CrossSection	" \
          ", '' As Luster " \
          ", Case SOLIE.PACKINGTYPE When 0 then 'None' Else 'Other' End As PkgType	" \
          ", Coalesce(Varchar(DAYS(SO.REQUIREDDUEDATE)-DAYS(SO.ORDERDATE)),'') As DelvDays " \
          ", Varchar_format(SO.ORDERDATE,'DD-MM-YYYY') As DelvSrtDt " \
          ", Coalesce(Varchar_format(SO.REQUIREDDUEDATE,'DD-MM-YYYY'),'') As DelvEndDt " \
          ", Coalesce(Case SO.PROGRESSSTATUS When 0 AND SO.DOCUMENTTYPETYPE = 02 Then 'Entered' When 1 AND SO.DOCUMENTTYPETYPE = 02 Then 'Pending' When 2 AND SO.DOCUMENTTYPETYPE = 02 Then 'Closed' End,'') As OrdStatus " \
          ", Case SO.PROGRESSSTATUS When 0 AND SO.DOCUMENTTYPETYPE <> 02 Then 'Entered' When 1 AND SO.DOCUMENTTYPETYPE <> 02 Then 'Pending' When 2 AND SO.DOCUMENTTYPETYPE <> 02 Then 'Closed' End As ContractStatus	" \
          ", Cast(SOD.USERPRIMARYQUANTITY-SOD.USEDUSERPRIMARYQUANTITY As Decimal(20,3)) As UpdtQty" \
          ", COALESCE(SO.EXTERNALREFERENCE,'') As PORefNo " \
          ", '' As PkgWt " \
          ", COALESCE(BPAddress.ADDRESSEE ||', '|| BPAddress.ADDRESSLINE1 ||', '|| Coalesce(BPAddress.ADDRESSLINE2,'') ||', '|| " \
          "Coalesce(BPAddress.ADDRESSLINE3,'') ||', '|| Coalesce(BPAddress.ADDRESSLINE4,'')||', '|| Coalesce(BPAddress.ADDRESSLINE5,'')||', '|| " \
          "Coalesce(BPAddress.POSTALCODE,'')||', '||Coalesce(BPAddress.TOWN,''), (BP.ADDRESSLINE1 ||', '|| " \
          "Coalesce(BP.ADDRESSLINE2,'') ||', '||Coalesce(BP.ADDRESSLINE3,'') ||', '|| Coalesce(BP.ADDRESSLINE4,'')||', '|| " \
          "Coalesce(BP.ADDRESSLINE5,'')||', '||Coalesce(BP.POSTALCODE,'')||', '||Coalesce(BP.TOWN,''))) As BPAddress " \
          ", pan.PANNO As PanNo " \
          ", Coalesce(BpGst.GSTINNUMBER, '') ||'  GST WEF: '||Coalesce(VARCHAR_FORMAT(BpGst.GSTDATE,'DD  Mon  YYYY'), '') As GSTNO " \
          "From SALESORDER SO " \
          "Join ORDERPARTNER OP                    On      SO.ORDPRNCUSTOMERSUPPLIERCODE = OP.CUSTOMERSUPPLIERCODE " \
          "And     OP.CUSTOMERSUPPLIERTYPE = 1  " \
          "Join  ORDERPARTNERIE pan                 ON      SO.ORDPRNCUSTOMERSUPPLIERCODE = pan.CUSTOMERSUPPLIERCODE " \
          "AND  pan.CUSTOMERSUPPLIERTYPE = 1 " \
          "Join BUSINESSPARTNER Bp                 On      OP.ORDERBUSINESSPARTNERNUMBERID = Bp.NUMBERID " \
          "Left Join ADDRESSGST BpGst              On      Bp.ABSUNIQUEID = BpGst.UNIQUEID " \
          "Left Join AGENT                         On      SO.AGENT1CODE = AGENT.CODE " \
          "And     SO.COMMISSIONLIQUIDATIONTYPE1 = AGENT.COMMISSIONLIQUIDATIONTYPE " \
          "Join    SALESORDERIE                    On      SO.CODE = SALESORDERIE.CODE " \
          "And     SO.COUNTERCODE = SALESORDERIE.COUNTERCODE " \
          "Left Join ADDRESS BPAddress                On      SO.DELIVERYPOINTUNIQUEID = BPAddress.UNIQUEID " \
          "And     SO.DELIVERYPOINTCODE = BPAddress.CODE " \
          "Left Join TRANSPORTZONE DespTo          On      Bp.TRANSPORTZONECODE = DespTo.CODE " \
          "And     Bp.COUNTRYCODE = DespTo.COUNTRYCODE  " \
          "Join    SALESORDERLINE SOL              On      SO.CODE = SOL.SALESORDERCODE  " \
          "And     SO.COUNTERCODE = SOL.SALESORDERCOUNTERCODE " \
          "Join LOGICALWAREHOUSE                   On      SOL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Join BUSINESSUNITVSCOMPANY BUC          On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE " \
          "Join FINBUSINESSUNIT                    On      BUC.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "And     FINBUSINESSUNIT.GROUPFLAG = 0 " \
          "Join FINBUSINESSUNIT Comp               On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
          "And     Comp.GROUPFLAG = 1 " \
          "Left Join ADSTORAGE LotNo               ON      SOL.ABSUNIQUEID =  LotNo.UNIQUEID " \
          "And     LotNo.NAMEENTITYNAME = 'SalesOrderLine' " \
          "And     LotNo.NAMENAME = 'Lotno' " \
          "And     LotNo.FIELDNAME = 'Lotno' " \
          "Join SALESORDERLINEIE  SOLIE            ON      SOL.SALESORDERCODE = SOLIE.SALESORDERCODE " \
          "And     SOL.SALESORDERCOUNTERCODE = SOLIE.SALESORDERCOUNTERCODE " \
          "AND     SOL.ORDERLINE = SOLIE.ORDERLINE " \
          "Left Join Note Narrtn                   On      SO.ABSUNIQUEID =  Narrtn.FATHERID  " \
          "Join    SALESORDERDELIVERY SOD          ON      SOL.SALESORDERCODE = SOD.SALESORDERLINESALESORDERCODE " \
          "And     SOL.SALESORDERCOUNTERCODE = SOD.SALORDLINESALORDERCOUNTERCODE " \
          "AND     SOL.ORDERLINE = SOD.SALESORDERLINEORDERLINE " \
          "join    FULLITEMKEYDECODER FIKD         ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(SOL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(SOL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(SOL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(SOL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(SOL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(SOL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(SOL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(SOL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(SOL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(SOL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                         ON      SOL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID  " \
          "Left Join QUALITYLEVEL                  On      SOL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
          "And     SOL.QUALITYCODE = QUALITYLEVEL.CODE " \
          "Left JOIN ItemSubcodeTemplate IST       ON      SOL.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "AND     IST.GroupTypeCode  In ('MB4','P09','B07') " \
          "LEFT JOIN USERGENERICGROUP UGG          On      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "AND     Case IST.Position When 1 Then SOL.SUBCODE01 When 2 Then SOL.SUBCODE02 When 3 Then SOL.SUBCODE03 When 4 Then SOL.SUBCODE04 When 5 Then SOL.SUBCODE05 " \
          "When 6 Then SOL.SUBCODE06 When 7 Then SOL.SUBCODE07 When 8 Then SOL.SUBCODE08 When 9 Then SOL.SUBCODE09 When 10 Then SOL.SUBCODE10 End = UGG.Code " \
          "Left JOIN ItemSubcodeTemplate CrsLstrIST ON      SOL.ITEMTYPEAFICODE = CrsLstrIST.ItemTypeCode " \
          "AND     CrsLstrIST.GroupTypeCode  In ('PO5','BO4','P05','B04') " \
          "LEFT JOIN USERGENERICGROUP CrossLuster  On      CrsLstrIST.GroupTypeCode = CrossLuster.UserGenericGroupTypeCode " \
          "AND     Case CrsLstrIST.Position When 1 Then SOL.SUBCODE01 When 2 Then SOL.SUBCODE02 When 3 Then SOL.SUBCODE03 When 4 Then SOL.SUBCODE04 When 5 Then SOL.SUBCODE05 " \
          "When 6 Then SOL.SUBCODE06 When 7 Then SOL.SUBCODE07 When 8 Then SOL.SUBCODE08 When 9 Then SOL.SUBCODE09 When 10 Then SOL.SUBCODE10 End = CrossLuster.Code " \
          "Left Join INDTAXDETAIL ContRate         ON      SOL.ABSUNIQUEID = ContRate.ABSUNIQUEID " \
          "And     ContRate.ITAXCODE = 'CNR' " \
          "And     ContRate.TAXCATEGORYCODE = 'OTH' " \
          "Left JOIN IndTaxDETAIL NetRate          ON      SOL.AbsUniqueId = NetRate.ABSUNIQUEID " \
          "AND     NetRate.ITaxCode = 'BSR' " \
          "AND     NetRate.TAXCATEGORYCODE = 'OTH' " \
          "Left Join INDTAXDETAIL DharaRate        ON      SOL.ABSUNIQUEID = DharaRate.ABSUNIQUEID " \
          "And     DharaRate.ITAXCODE = 'DRD' " \
          "And     DharaRate.TAXCATEGORYCODE = 'OTH' " \
          "Left Join INDTAXDETAIL BillRate         ON      SOL.ABSUNIQUEID = BillRate.ABSUNIQUEID " \
          "And     BillRate.ITAXCODE = 'INR' " \
          "And     BillRate.TAXCATEGORYCODE = 'OTH' " \
          "Left Join INDTAXDETAIL INitilComm       ON      SOL.ABSUNIQUEID = INitilComm.ABSUNIQUEID " \
          "And     INitilComm.ITAXCODE = 'AG1' " \
          "And     INitilComm.TAXCATEGORYCODE = 'OTH' " \
          "Left Join INDTAXDETAIL BalComm          ON      SOL.ABSUNIQUEID = BalComm.ABSUNIQUEID " \
          "And     BalComm.ITAXCODE = 'BS1' " \
          "And     BalComm.TAXCATEGORYCODE = 'OTH' " \
          "Left Join    INDTAXTOTAL Freight        ON      SO.ABSUNIQUEID = Freight.ABSUNIQUEID " \
          "And     Freight.ITAXCODE = 'FRT' " \
          "And     Freight.TAXCATEGORYCODE = 'GFR' " \
          "Left Join SALESORDER PrevOrder          On      So.PREVIOUSCODE =  PrevOrder.CODE " \
          "And     So.PREVIOUSCOUNTERCODE =  PrevOrder.COUNTERCODE " \
          "Left Join SALESORDERLINE PrevOrderLine  On      PrevOrder.CODE = PrevOrderLine.SALESORDERCODE " \
          "And     PrevOrder.COUNTERCODE = PrevOrderLine.SALESORDERCOUNTERCODE " \
          "And     SOL.PREVIOUSORDERLINE = PrevOrderLine.ORDERLINE " \
          "Left Join INDTAXDETAIL PrevOrgnlContRt  ON      PrevOrderLine.ABSUNIQUEID = PrevOrgnlContRt.ABSUNIQUEID " \
          "And     PrevOrgnlContRt.ITAXCODE = 'CNR' " \
          "And     PrevOrgnlContRt.TAXCATEGORYCODE = 'OTH' " \
          "Left JOIN IndTaxDETAIL PrevContRt       ON      PrevOrderLine.AbsUniqueId = PrevContRt.ABSUNIQUEID " \
          "AND     PrevContRt.ITaxCode = 'BSR' " \
          "AND     PrevContRt.TAXCATEGORYCODE = 'OTH'  " \
          "Where "+contractNo+" "+contractCounter+" "

    DcmtType = 0

    srNo = 0
    contractDt = ''
    Company = ''
    OrdNo = ''
    Customer = ''
    Broker = ''
    DespTo = ''
    CURRENCY = ''
    EXRAte = ''
    Freight = 0
    OrdType = ''
    Narration = ''
    BPAddress = ''
    PanNo = ''
    GstNo = ''

    # ************ for exatly only in documentype -2
    PkgWt = ''
    Quanty = 0
    contrate = 0
    initlComm = 0
    NETRATE = 0
    BALCOMMPERC = 0
    ORDTYPE = ''
    DRate = 0
    BillRate = 0
    DelvDays = 0
    DelvStDt = ''
    DelvEdDt = ''


    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        srNo += 1
        result['srNo'] = srNo
        contractDt = result['CONTDT']
        OrdNo = result['ORDNO']
        Company = result['COMPANY']
        Customer = result['CUSTOMER']
        Broker = result['BROKER']
        DespTo = result['DESPTO']
        CURRENCY = result['CURRENCYCODE']
        EXRAte = result['EXRATE']
        Freight = result['FREIGHT']
        OrdType = result['ORDTYPE']
        Narration = result['NARRATION']
        BPAddress = result['BPADDRESS']
        PanNo = result['PANNO']
        GstNo = result['GSTNO']
        DcmtType = result['DCTTYPE']
        GDataView.append(result)
        # ************ for exatly omly in documentype -2
        PkgWt = result['PKGWT']
        Quanty = result['QNTY']
        contrate = result['CONTRACTRATE']
        initlComm = result['INITIALCOMMPERC']
        NETRATE = result['NETRATE']
        BALCOMMPERC = result['BALCOMMPERC']
        ORDTYPE = result['ORDTYPE']
        DRate = result['DRATE']
        BillRate = result['BILLRATE']
        DelvDays = result['DELVDAYS']
        DelvStDt = result['DELVSRTDT']
        DelvEdDt = result['DELVENDDT']
        result = con.db.fetch_both(stmt)
    # print(int(DcmtType))
    # ORDTYPE = 'Export'
    titleOfPage = ''
    if int(DcmtType) != 2:
        titleOfPage = '[View Order]'
    else:
        titleOfPage = '[View Contract]'
    return render(request, 'ContractPendingMisView.html', {'titleOfPage':titleOfPage,'GDataView': GDataView, 'contractNumber': contractNumber,
                                                           'contractDt': contractDt, 'Company': Company, 'DcmtType':DcmtType,
                                                           'OrdNo': OrdNo,'Customer': Customer,
                                                           'Broker': Broker, 'DespTo': DespTo, 'CURRENCY':CURRENCY, 'EXRAte':EXRAte,
                                                           'Freight':Freight, 'OrdType': OrdType,
                                                           'Narration': Narration, 'BPAddress': BPAddress, 'PanNo':PanNo , 'GstNo':GstNo,
                                                           'sources': sources})

    # else:
    #     return render(request, 'ContractPendingMisContract.html', {'GDataView': GDataView, 'contractDt': contractDt, 'PkgWt': PkgWt,
    #                                                                'Quanty': Quanty, 'contrate':contrate, 'initlComm':initlComm,
    #                                                                'NETRATE': NETRATE, 'BALCOMMPERC': BALCOMMPERC,
    #                                                                'GDataOrderType':views.GDataOrderType, 'ORDTYPE': ORDTYPE,
    #                                                                'DRate':DRate, 'BillRate':BillRate , 'DespTo': DespTo, 'DelvDays':DelvDays ,
    #                                                                'DelvStDt': DelvStDt, 'DelvEdDt':DelvEdDt, 'Narration': Narration,
    #                                                                'sources': sources})