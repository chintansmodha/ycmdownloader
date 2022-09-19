from django.shortcuts import render
from Global_Files import Connection_String as con
# Create your views here.
GDataCompany=[]
GDataParty=[]
GDataDespatch=[]
GDataSummary = []

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from Finbusinessunit where GROUPFLAG=0 order by LONGDESCRIPTION")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select NUMBERID,LEGALNAME1 from BUSINESSPARTNER order by LEGALNAME1")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataParty:
        GDataParty.append(result)
    result = con.db.fetch_both(stmt)

stmt = con.db.exec_immediate(con.conn,"select CODE,LONGDESCRIPTION from TRANSPORTZONE order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataDespatch:
        GDataDespatch.append(result)
    result = con.db.fetch_both(stmt)

def PrintChallanAdviceHTML(request):
    return render(request, 'PrintChallanAdvice.html',{'GDataCompany':GDataCompany,'GDataParty':GDataParty, 'GDataDespatch':GDataDespatch})

# VALUE IN GRID
def PrintChallanAdviceTableHTML(request):
    global GDataSummary

    GDataSummary = []
    LSCompanyUnitCode = request.GET.getlist('comp')
    LCCompanyUnitCode = request.GET.getlist('allcomp')

    LSParty = request.GET.getlist('party')
    LCParty = request.GET.getlist('allparty')

    LSDespatch = request.GET.getlist('desp')
    LCDespatch = request.GET.getlist('alldesp')

    LDStartDate = "'" + str(request.GET['startdate']) + "'"
    LDEndDate = "'" + str(request.GET['enddate']) + "'"

    companyunitcodes = str(LSCompanyUnitCode)
    LSCompanyUnitCodes = '(' + companyunitcodes[1:-1] + ')'

    parties = str(LSParty)
    party = '(' + parties[1:-1] + ')'

    Despatches = '(' + str(LSDespatch)[1:-1] + ')'

    if not LCCompanyUnitCode and not LSCompanyUnitCode:
        companyunitcode = " "
    elif LCCompanyUnitCode:
        companyunitcode = " "
    elif LSCompanyUnitCode:
        companyunitcode = "And BUC.BusinessUnitcode in " + str(LSCompanyUnitCodes)

    if not LSDespatch and not LCDespatch:
        Desp = " "
    elif LCDespatch:
        Desp = " "
    elif LSDespatch:
        Desp = "And BP.TRANSPORTZONECODE in " + str(Despatches)

    if not LCParty and not LSParty:
        Party = " "
    elif LCParty:
        Party = " "
    elif LSParty:
        Party = "And BP.NumberId in " + str(party)


    sql = "Select   SalesDocument.PROVISIONALCODE As ChallanNo " \
          ", VARCHAR_FORMAT(SalesDocument.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') As ChallanDate " \
          ", COALESCE(TRANSPORTZONE.LONGDESCRIPTION, '') As Despatch " \
          ", Stxn.LotCode As LotNo " \
          ", CAST(Sum(BKLELEMENTS.ACTUALNETWT) As DECIMAL(10,3)) As Quantity " \
          ", COALESCE(SalesDocument.EXTERNALREFERENCE,'-') As LRNO " \
          ", COUNT(Stxn.CONTAINERELEMENTCODE)  As Boxes " \
          "from SalesDocument " \
          "join SalesDocumentLine  AS SDL          on      SalesDocument.PROVISIONALCOUNTERCODE = SDL.SALDOCPROVISIONALCOUNTERCODE  " \
          "AND     SalesDocument.PROVISIONALCODE = SDL.SALESDOCUMENTPROVISIONALCODE " \
          "JOIN LOGICALWAREHOUSE                   ON      SDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "JOIN BusinessUnitVsCompany BUC          ON      LOGICALWAREHOUSE.PLANTCODE   = BUC.FACTORYCODE " \
          "JOIN STOCKTRANSACTION Stxn              ON      SalesDocument.PROVISIONALCODE = Stxn.ORDERCODE " \
          "AND     SalesDocument.PROVISIONALCOUNTERCODE = Stxn.ORDERCOUNTERCODE " \
          "AND     Stxn.TEMPLATECODE = 'S04' " \
          "AND     SDL.ITEMTYPEAFICODE = Stxn.ITEMTYPECODE " \
          "AND     COALESCE(SDL.SubCode01, '') = COALESCE(Stxn.DECOSUBCODE01, '')  " \
          "AND     COALESCE(SDL.SubCode02, '') = COALESCE(Stxn.DECOSUBCODE02, '')   " \
          "AND     COALESCE(SDL.SubCode03, '') = COALESCE(Stxn.DECOSUBCODE03, '')  " \
          "AND     COALESCE(SDL.SubCode04, '') = COALESCE(Stxn.DECOSUBCODE04, '')   " \
          "AND     COALESCE(SDL.SubCode05, '') = COALESCE(Stxn.DECOSUBCODE05, '')   " \
          "AND     COALESCE(SDL.SubCode06, '') = COALESCE(Stxn.DECOSUBCODE06, '')   " \
          "AND     COALESCE(SDL.SubCode07, '') = COALESCE(Stxn.DECOSUBCODE07, '')    " \
          "AND     COALESCE(SDL.SubCode08, '') = COALESCE(Stxn.DECOSUBCODE08, '')   " \
          "AND     COALESCE(SDL.SubCode09, '') = COALESCE(Stxn.DECOSUBCODE09, '')   " \
          "AND     COALESCE(SDL.SubCode10, '') = COALESCE(Stxn.DECOSUBCODE10, '') " \
          "AND     Stxn.CONTAINERITEMTYPECODE = 'CNT' " \
          "Join BKLELEMENTS                        ON      Stxn.CONTAINERELEMENTCODE = BKLELEMENTS.CODE " \
          "join OrderPartner As OP                 on      SalesDocument.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode " \
          "And     OP.CustomerSupplierType = 1 " \
          "join BusinessPartner As BP              On      OP.ORDERBUSINESSPARTNERNUMBERID = BP.NumberID " \
          "Left JOIn TRANSPORTZONE                 ON      BP.TRANSPORTZONECODE = TRANSPORTZONE.CODE " \
          "where SalesDocument.DOCUMENTTYPETYPE='05' " \
          "And SalesDocument.PROVISIONALDOCUMENTDATE BETWEEN "+LDStartDate+"    AND     "+LDEndDate+" "+ companyunitcode +" " + Party+" "+Desp+" " \
          "Group By SalesDocument.PROVISIONALCODE " \
          ", VARCHAR_FORMAT(SalesDocument.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') " \
          ", COALESCE(SalesDocument.EXTERNALREFERENCE,'-')  " \
          ", Stxn.LotCode " \
          ", SalesDocument.PROVISIONALDOCUMENTDATE " \
          ", COALESCE(TRANSPORTZONE.LONGDESCRIPTION, ''), CAST((SDL.USERPRIMARYQUANTITY) As DECIMAL(10,3)) " \
          "order by SalesDocument.PROVISIONALDOCUMENTDATE DESC, ChallanNo, LotNo "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        GDataSummary.append(result)
        result = con.db.fetch_both(stmt)


    if GDataSummary == []:
        global Exceptions
        Exceptions = "Note: No Result found on given criteria "
        return render(request, 'PrintChallanAdvice.html',{'GDataCompany':GDataCompany,'GDataParty':GDataParty, 'GDataDespatch':GDataDespatch,
                                                          'Exception':Exceptions})
    else:
        return render(request, 'PrintChallanAdvice_Table.html',
                  {'GDataSummary': GDataSummary})