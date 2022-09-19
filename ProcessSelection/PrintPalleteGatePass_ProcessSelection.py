from datetime import datetime
from django.shortcuts import render
from Global_Files import Connection_String as con
from FormLoad import PrintPalleteGatePass_FormLoad as PPGP_FL
Company=[]
Party=[]
Exceptions=""
save_name=""
LSFileName=""
GDataPrintPalleteGatePass=[]
def PrintPalleteGatePass_PrintPDF(LSCompany,LSParty,LDStartDate,LDEndDate,LSTemplateType,request):
    global LSFileName
    global save_name
    global Company
    global Party
    global GDataPrintPalleteGatePass
    GDataPrintPalleteGatePass=[]
    if LSTemplateType==1:
        PrintPalleteGatePass(LSCompany,LSParty,LDStartDate,LDEndDate,LSTemplateType,request)
        return render(request, 'PrintPalleteGatePassTable.html',
                      {'GDataPrintPalleteGatePass': GDataPrintPalleteGatePass})
    elif LSTemplateType==2:
        PrintPalleteGatePassPMC(LSCompany,LSParty,LDStartDate,LDEndDate,LSTemplateType,request)
        return render(request, 'PrintPalleteGatePassTable_PMC.html',
                      {'GDataPrintPalleteGatePass': GDataPrintPalleteGatePass})
    # return PrintPalleteGatePass(request)

def PrintPalleteGatePass(LSCompany,LSParty,LDStartDate,LDEndDate,LSTemplateType,request):
    global save_name
    global GDataPrintPalleteGatePass
    GDataPrintPalleteGatePass=[]
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSCompany = request.GET.getlist('dept')
    Company = str(LSCompany)
    Company = '(' + Company[1:-1] + ')'
    Party = str(LSParty)
    Party = '(' + Party[1:-1] + ')'
    LDStartDate = "'" + request.GET['startdate'] + "'"
    LDEndDate = "'" + request.GET['enddate'] + "'"
    LSStartNo = request.GET.getlist('stno')
    LSEndNo = request.GET.getlist('endno')

    if not LSCompany:
        Company = " "
    else:
        Company = " And BUnit.Code in " + Company
        print(Company)

    if not LSParty:
        Party = " "
    else:
        Party = " And BP.NumberId in " + Party

    if not LSStartNo:
        StartNo=" "
    else:
        StartNo = "" + str(LSStartNo)

    if not LSEndNo:
        EndNo=" "
    else:
        EndNo = "" + str(LSEndNo)

    sql="SELECT  ID.PROVISIONALCODE AS GATEPASSNO" \
        " ,VARCHAR_FORMAT(ID.PROVISIONALDOCUMENTDATE,'DD-MM-YYYY') AS GATEPASSDATE" \
        " ,BP.LEGALNAME1 as SUPPLIER" \
        " FROM INTERNALDOCUMENT AS ID" \
        " JOIN InternalDocumentLine As IDL        ON      ID.PROVISIONALCODE = IDL.INTDOCUMENTPROVISIONALCODE" \
        " AND     ID.PROVISIONALCOUNTERCODE = IDL.INTDOCPROVISIONALCOUNTERCODE" \
        " JOIN LOGICALWAREHOUSE           AS LWH                         ON      IDL.WAREHOUSECODE = LWH.CODE" \
        " JOIN BUSINESSUNITVSCOMPANY      AS BUC                         ON      ID.DIVISIONCODE = BUC.DIVISIONCODE" \
        " AND     LWH.PLANTCODE = BUC.FACTORYCODE" \
        " JOIN FINBUSINESSUNIT            AS BUnit                       ON      BUC.BusinessUnitcode = BUnit.Code" \
        " AND     BUnit.GroupFlag = 0" \
        " JOIN FINBUSINESSUNIT            AS Company                     ON      Bunit.GroupBUCode = Company.Code" \
        " AND     Company.GroupFlag = 1" \
        " JOIN INTERNALORDERTEMPLATE      AS IOT                          ON      ID.TemplateCode = IOT.Code" \
        " JOIN ORDERPARTNER               AS OP                           ON      ID.ORDPRNCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode" \
        " AND     IOT.DESTINATIONTYPE = OP.CustomerSupplierType" \
        " JOIN BUSINESSPARTNER            AS BP                           ON      OP.OrderBusinessPartnerNumberId = BP.NumberId" \
        " WHERE ID.DocumentTypeType = '05'  AND ID.PROVISIONALCOUNTERCODE='PMS'AND ID.PROVISIONALDOCUMENTDATE BETWEEN" \
        " " + LDStartDate + "AND" + LDEndDate +""+ Company+" "+ Party+"" \
        " GROUP BY ID.PROVISIONALDOCUMENTDATE, ID.PROVISIONALCODE,BP.LEGALNAME1"

    stmt = con.db.prepare(con.conn, sql)
    # stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    # etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(sql)

    while result != False:
        GDataPrintPalleteGatePass.append(result)
        result = con.db.fetch_both(stmt)

def PrintPalleteGatePassPMC(LSCompany,LSParty,LDStartDate,LDEndDate,LSTemplateType,request):
    global save_name
    global GDataPrintPalleteGatePass
    GDataPrintPalleteGatePass = []
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSCompany = request.GET.getlist('dept')
    Company = str(LSCompany)
    Company = '(' + Company[1:-1] + ')'
    Party = str(LSParty)
    Party = '(' + Party[1:-1] + ')'
    LDStartDate = "'" + request.GET['startdate'] + "'"
    LDEndDate = "'" + request.GET['enddate'] + "'"
    LSStartNo = request.GET.getlist('stno')
    LSEndNo = request.GET.getlist('endno')

    if not LSCompany:
        Company = " "
    else:
        Company = " And BUnit.Code in " + Company

    if not LSParty:
        Party = " "
    else:
        Party = " And BP.NumberId in " + Party

    if not LSStartNo:
        StartNo = " "
    else:
        StartNo = "" + str(LSStartNo)

    if not LSEndNo:
        EndNo = " "
    else:
        EndNo = "" + str(LSEndNo)

    sql="SELECT  ID.PROVISIONALCODE AS GATEPASSNO" \
        " ,VARCHAR_FORMAT(ID.PROVISIONALDOCUMENTDATE,'DD-MM-YYYY') AS GATEPASSDATE" \
        " ,BP.LEGALNAME1 as SUPPLIER" \
        " FROM INTERNALDOCUMENT AS ID" \
        " JOIN InternalDocumentLine As IDL                                ON      ID.PROVISIONALCODE = IDL.INTDOCUMENTPROVISIONALCODE" \
        " AND     ID.PROVISIONALCOUNTERCODE = IDL.INTDOCPROVISIONALCOUNTERCODE" \
        " JOIN LOGICALWAREHOUSE           AS LWH                          ON      IDL.WAREHOUSECODE = LWH.CODE" \
        " JOIN BUSINESSUNITVSCOMPANY      AS BUC                          ON      ID.DIVISIONCODE = BUC.DIVISIONCODE" \
        " AND     LWH.PLANTCODE = BUC.FACTORYCODE" \
        " JOIN FINBUSINESSUNIT            AS BUnit                        ON      BUC.BusinessUnitcode = BUnit.Code" \
        " AND     BUnit.GroupFlag = 0" \
        " JOIN FinBusinessUnit            As Company                      ON      Bunit.GroupBUCode = Company.Code" \
        " AND     Company.GroupFlag = 1" \
        " JOIN INTERNALORDERTEMPLATE      AS IOT                          ON      ID.TemplateCode = IOT.Code" \
        " JOIN ORDERPARTNER               AS OP                           ON      ID.ORDPRNCUSTOMERSUPPLIERCODE = OP.CustomerSupplierCode" \
        " AND     IOT.DESTINATIONTYPE = OP.CustomerSupplierType" \
        " JOIN BUSINESSPARTNER            AS BP                           ON      OP.OrderBusinessPartnerNumberId = BP.NumberId" \
        " WHERE ID.DocumentTypeType = '05'  AND ID.PROVISIONALCOUNTERCODE='PMC' AND ID.PROVISIONALDOCUMENTDATE BETWEEN" \
        " " + LDStartDate + "AND" + LDEndDate + "" + Company + " " + Party + "" \
        " GROUP BY ID.PROVISIONALDOCUMENTDATE, ID.PROVISIONALCODE,BP.LEGALNAME1"

    stmt = con.db.prepare(con.conn, sql)
    # stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    # etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        GDataPrintPalleteGatePass.append(result)
        result = con.db.fetch_both(stmt)