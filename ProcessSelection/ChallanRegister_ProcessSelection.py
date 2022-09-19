# function to generate report
import os
from datetime import datetime
from babel.numbers import format_currency
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.static import serve

from PrintPDF import ChallanRegister_PrintPDF as pdfrpt
from FormLoad import ChallanRegister_FormLoad as views
from Global_Files import Connection_String as con
from django.http import FileResponse
# from . import views
Exceptions= ""
counter = 0

def ChallanRegister(request):
    LSName =datetime.now()
    LSstring =str(LSName)
    sqlwhere=''
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Challan Register/",
    #                          LSFileName)
    save_name = os.path.join(os.path.expanduser("~"), LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    # pdfrpt.c = pdfrpt.canvas.Canvas(LSFileName + ".pdf")
    LSselcompany = request.GET.getlist('selcompany')
    LSselparty = request.GET.getlist('selparty')
    LSsellotno = request.GET.getlist('sellotno')
    LSselquality = request.GET.getlist('selquality')
    LSselfromdepartment = request.GET.getlist('selfromdepartment')
    LSseltodepartment = request.GET.getlist('seltodepartment')
    LSselwindingtype = request.GET.getlist('selwindingtype')
    LSselagent = request.GET.getlist('selagent')
    LSselshade = request.GET.getlist('selshade')

    try:
        LSallcompany = str(request.GET['allcompany'])
    except:
        LSallcompany=False
    try:
        LSallparty = str(request.GET['allparty'])
    except:
        LSallparty=False
    try:
        LSalllotno = str(request.GET['alllotno'])
    except:
        LSalllotno=False
    try:
        LSallquality = str(request.GET['allquality'])
    except:
        LSallquality=False
    try:
        LSallfromdepartment = str(request.GET['allfromdepartment'])
    except:
        LSallfromdepartment=False
    try:
        LSalltodepartment = str(request.GET['alltodepartment'])
    except:
        LSalltodepartment=False
    try:
        LSallwindingtype = str(request.GET['allwindingtype'])
    except:
        LSallwindingtype=False
    try:
        LSallagent = str(request.GET['allagent'])
    except:
        LSallagent=False
    try:
        LSallshade = str(request.GET['allshade'])
    except:
        LSallshade=False
    try:
        if LSallcompany == 'None' and len(LSselcompany) != 0 or str(LSallcompany) == 'False':
            company = str(LSselcompany)
            LSCompanycode = '(' + company[1:-1] + ')'
            sqlwhere += ' AND  BUnit.CODE IN ' + LSCompanycode

        if LSallparty == 'None' and len(LSselparty) != 0 or str(LSallparty) == 'False':
            party = str(LSselparty)
            LSPartycode = '(' + party[1:-1] + ')'
            sqlwhere += ' AND BusinessPartner.NumberID IN ' + LSPartycode

        if LSallquality == 'None' and len(LSselquality) != 0 or str(LSallquality) == 'False':
            quanlity = str(LSselquality)
            LSqualitycode = '(' + quanlity[1:-1] + ')'
            sqlwhere += ' AND QUALITYLEVEL.CODE IN ' + LSqualitycode

        if LSallfromdepartment == 'None' and len(LSselfromdepartment) != 0 or str(LSallfromdepartment) == 'False':
            fromdepartment = str(LSselfromdepartment)
            LSfromdepartmentcode = '(' + fromdepartment[1:-1] + ')'
            sqlwhere += ' AND COSTCENTER.CODE IN ' + LSfromdepartmentcode

        if LSalltodepartment == 'None' and len(LSseltodepartment) != 0 or str(LSalltodepartment) == 'False':
            todepartment = str(LSseltodepartment)
            LStodepartmentcode = '(' + todepartment[1:-1] + ')'
            sqlwhere += ' AND COSTCENTER.CODE IN ' + LStodepartmentcode
        #
        # if LSallwindingtype == 'None' and len(LSselwindingtype) != 0 or str(LSallwindingtype) == 'False':
        #     windingcode = str(LSselwindingtype)
        #     LSwinding = '(' + windingcode[1:-1] + ')'
        #     sqlwhere += ' AND ORDERPARTNER.CUSTOMERSUPPLIERCODE IN ' + LSwinding

        # if LSalllotno == 'None' and len(LSsellotno) != 0 or str(LSalllotno) == 'False':
        #     lotno = str(LSsellotno)
        #     LSlotnocode = '(' + lotno[1:-1] + ')'
        #     sqlwhere += ' AND  ' + LSlotnocode
        #

        if LSallagent == 'None' and len(LSselagent) != 0 or str(LSallagent) == 'False':
            agent = str(LSselagent)
            LSagentcode = '(' + agent[1:-1] + ')'
            sqlwhere += ' AND AGENT.CODE IN ' + LSagentcode

        if LSallshade == 'None' and len(LSselshade) != 0 or str(LSallshade) == 'False':
            shade = str(LSselshade)
            LSshadecode = '(' + shade[1:-1] + ')'
            sqlwhere += ' AND UGG.CODE IN ' + LSshadecode
    except:
        pass

    LSRegistertype=str(request.GET['CboRegisterType'])
    LDStartDate=str(request.GET['startdate'])
    LDEndDate=str(request.GET['enddate'])

    if LSRegistertype == '0':
        LSFileName="Challan Reg. Details & Summary "+LSFileName
        ChallanDetailSummary(LSselcompany,LSselparty,LSsellotno,LSselquality,LSselfromdepartment,LSseltodepartment,
                         LSselwindingtype,LSselagent,LSselshade,LSallcompany, LSallparty, LSalllotno, LSallquality,
                         LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent, LSallshade,
                         LDStartDate,LDEndDate,LSFileName,sqlwhere)
    elif LSRegistertype == '1':
        LSFileName = "Challan Reg. Summary " + LSFileName
        ChallanRegisterSummary(LSselcompany, LSselparty, LSsellotno, LSselquality, LSselfromdepartment, LSseltodepartment,
                           LSselwindingtype, LSselagent, LSselshade, LSallcompany, LSallparty, LSalllotno, LSallquality,
                           LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent, LSallshade,
                           LDStartDate, LDEndDate, LSFileName,sqlwhere)
    elif LSRegistertype == '2':
        LSFileName = "Agent Party Item-wise Summary " + LSFileName
        stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
        etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
        sql = "SELECT   COSTCENTER.LONGDESCRIPTION AS DeptName " \
              "        , SALESDOCUMENT.PROVISIONALCODE AS CHALLANNUMBER " \
              "        , SALESDOCUMENT.PROVISIONALDOCUMENTDATE AS CHALLANDATE " \
              "        , Agent.LongDescription As AGENT " \
              "        , trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS PRODUCT " \
              "        , SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS QUANTITY " \
              "        , Int((SALESDOCUMENTLINE.USERPRIMARYQUANTITY * COALESCE(IndTaxDetail.calculatedvalue,0))+0.50) As InvoiceAmount " \
              "        , UGG.Code As ShadeCode " \
              "        , BusinessPartner.LEGALNAME1  AS CUSTOMER " \
              "        , count(*) over(partition by Product.LONGDESCRIPTION)  as ITEMCOUNT " \
              "FROM SALESDOCUMENT " \
              "join OrderPartner       On      SALESDOCUMENT.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode " \
              "                                And     OrderPartner.CustomerSupplierType = 1 " \
              "join BusinessPartner    On      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
              "JOIN Agent                      ON SALESDOCUMENT.Agent1Code                             = Agent.Code  " \
              "JOIN BusinessUnitVsCompany BUC  ON SalesDocument.DivisionCode   = BUC.DivisionCode " \
              "JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode = BUnit.Code And BUnit.GroupFlag = 0 " \
              "JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code And Company.GroupFlag = 1 " \
              "JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE " \
              "									AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE  = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
              "JOIN LOGICALWAREHOUSE           ON SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE " \
              "									AND LOGICALWAREHOUSE.plantcode                          = BUC.factorycode " \
              "JOIN ITEMTYPE                   ON SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = ITEMTYPE.CODE " \
              "JOIN COSTCENTER                 ON SALESDOCUMENTLINE.COSTCENTERCODE                     = COSTCENTER.CODE " \
              "JOIN QUALITYLEVEL               ON SALESDOCUMENTLINE.QUALITYCODE                        = QUALITYLEVEL.CODE " \
              "                                AND SALESDOCUMENTLINE.ITEMTYPEAFICODE                   = QUALITYLEVEL.ITEMTYPECODE " \
              "LEFT JOIN INDTAXDETAIL          ON salesdocumentline.absuniqueid                        = INDTAXDETAIL.absuniqueid " \
              "                                AND INDTAXDETAIL.ITaxCOde = 'INR' " \
              "                                And INDTAXDETAIL.TaxCategoryCode = 'OTH' " \
              "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = IST.ItemTypeCode " \
              "									AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
              "JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
              "                                    AND     Case IST.Position  " \
              "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03  " \
              "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06  " \
              "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09  " \
              "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code " \
              "join         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
              "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
              "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
              "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
              "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
              "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
              "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
              "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
              "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
              "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
              "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
              "Join Product            On      SALESDOCUMENTLINE.ITEMTYPEAFICODE = Product.ITEMTYPECODE  " \
              "                                And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
              " WHERE SALESDOCUMENT.PROVISIONALDOCUMENTDATE between '" + str(stdt) + "' and '" + str(etdt) + "' " + sqlwhere + " " \
            " ORDER BY COSTCENTER.LONGDESCRIPTION ,SALESDOCUMENT.PROVISIONALDOCUMENTDATE "
        AgentPartyItemWiseRegisterSummary(LSselcompany, LSselparty, LSsellotno, LSselquality, LSselfromdepartment,
                               LSseltodepartment,
                               LSselwindingtype, LSselagent, LSselshade, LSallcompany, LSallparty, LSalllotno,
                               LSallquality,
                               LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent, LSallshade,
                               LDStartDate, LDEndDate, LSFileName,sqlwhere,sql)
    elif LSRegistertype == '3':
        LSFileName = "Party Agent Item-wise Summary " + LSFileName
        PartyAgentItemWiseRegisterSummary(LSselcompany, LSselparty, LSsellotno, LSselquality, LSselfromdepartment,
                                          LSseltodepartment,
                                          LSselwindingtype, LSselagent, LSselshade, LSallcompany, LSallparty,
                                          LSalllotno,
                                          LSallquality,
                                          LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent,
                                          LSallshade,
                                          LDStartDate, LDEndDate, LSFileName,sqlwhere)
    elif LSRegistertype == '4':
        # LSFileName = "Item Agent Party-wise Summary " + LSFileName

        ItemAgentPartyWiseRegisterSummary(LSselcompany, LSselparty, LSsellotno, LSselquality, LSselfromdepartment,
                                          LSseltodepartment,
                                          LSselwindingtype, LSselagent, LSselshade, LSallcompany, LSallparty,
                                          LSalllotno,
                                          LSallquality,
                                          LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent,
                                          LSallshade,
                                          LDStartDate, LDEndDate, LSFileName,sqlwhere)
#     elif LSRegistertype== '5':
#         # LSFileName = "Challan Reg. Summary " + LSFileName
#         ChallanRegisterTransporterwiseSummary(LSselcompany, LSselparty, LSsellotno, LSselquality, LSselfromdepartment, LSseltodepartment,
#                            LSselwindingtype, LSselagent, LSselshade, LSallcompany, LSallparty, LSalllotno, LSallquality,
#                            LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent, LSallshade,
#                            LDStartDate, LDEndDate, LSFileName)
#
    #
    # return render(request, 'ChallanRegister.html',
    #               {'company': views.company, 'party': views.party, 'lot': views.lot, 'quality': views.quality, 'department': views.department,
    #                'agent': views.agent, 'winding': views.winding, 'shade': views.shade})
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'ChallanRegister.html',
                      {'company': views.company, 'party': views.party, 'lot': views.lot, 'quality': views.quality,
                       'department': views.department,'agent': views.agent, 'winding': views.winding, 'shade': views.shade})

    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response

def ChallanDetailSummary(LSselcompany,LSselparty,LSsellotno,LSselquality,LSselfromdepartment,LSseltodepartment,
                         LSselwindingtype,LSselagent,LSselshade,LSallcompany, LSallparty, LSalllotno, LSallquality,
                         LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent, LSallshade,
                         LDStartDate,LDEndDate,LSFileName,sqlwhere):
    sqlwhere=''

    if LSallcompany == 'None' and len(LSselcompany) != 0 or str(LSallcompany) == 'False':
        company = str(LSselcompany)
        LSCompanycode = '(' + company[1:-1] + ')'
        sqlwhere += ' AND  BUnit.CODE IN ' + LSCompanycode


    if LSallparty == 'None' and len(LSselparty) != 0 or str(LSallparty) == 'False':
        party = str(LSselparty)
        LSPartycode = '(' + party[1:-1] + ')'
        sqlwhere += ' AND BusinessPartner.NumberID IN ' + LSPartycode

    if LSallquality == 'None' and len(LSselquality) != 0 or str(LSallquality) == 'False':
        quanlity = str(LSselquality)
        LSqualitycode = '(' + quanlity[1:-1] + ')'
        sqlwhere += ' AND QUALITYLEVEL.CODE IN ' + LSqualitycode

    if LSallfromdepartment == 'None' and len(LSselfromdepartment) != 0 or str(LSallfromdepartment) == 'False':
        fromdepartment = str(LSselfromdepartment)
        LSfromdepartmentcode = '(' + fromdepartment[1:-1] + ')'
        sqlwhere += ' AND COSTCENTER.CODE IN ' + LSfromdepartmentcode

    if LSalltodepartment == 'None' and len(LSseltodepartment) != 0 or str(LSalltodepartment) == 'False':
        todepartment = str(LSseltodepartment)
        LStodepartmentcode = '(' + todepartment[1:-1] + ')'
        sqlwhere += ' AND COSTCENTER.CODE IN ' + LStodepartmentcode
    #
    # if LSallwindingtype == 'None' and len(LSselwindingtype) != 0 or str(LSallwindingtype) == 'False':
    #     windingcode = str(LSselwindingtype)
    #     LSwinding = '(' + windingcode[1:-1] + ')'
    #     sqlwhere += ' AND ORDERPARTNER.CUSTOMERSUPPLIERCODE IN ' + LSwinding

    # if LSalllotno == 'None' and len(LSsellotno) != 0 or str(LSalllotno) == 'False':
    #     lotno = str(LSsellotno)
    #     LSlotnocode = '(' + lotno[1:-1] + ')'
    #     sqlwhere += ' AND  ' + LSlotnocode
    #

    if LSallagent == 'None' and len(LSselagent) != 0 or str(LSallagent) == 'False':
        agent = str(LSselagent)
        LSagentcode = '(' + agent[1:-1] + ')'
        sqlwhere += ' AND AGENT.CODE IN ' + LSagentcode

    if LSallshade == 'None' and len(LSselshade) != 0 or str(LSallshade) == 'False':
        shade = str(LSselshade)
        LSshadecode = '(' + shade[1:-1] + ')'
        sqlwhere += ' AND UGG.CODE IN ' + LSshadecode


    # sqlwhere=''
    print("------------------")
    print (sqlwhere)
    print("------------------")
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    sql="SELECT   COSTCENTER.LONGDESCRIPTION AS DeptName " \
        "        , SALESDOCUMENT.PROVISIONALCODE AS CHALLANNUMBER " \
        "        , SALESDOCUMENT.PROVISIONALDOCUMENTDATE AS CHALLANDATE " \
        "        , Product.LONGDESCRIPTION As Product " \
        "        , SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS QUANTITY " \
        "        , SALESDOCUMENTLINE.PRICE " \
        "        , Agent.LongDescription As AGENT " \
        "        , UGG.Code As ShadeCode " \
        "        , BusinessPartner.LEGALNAME1  AS CUSTOMER " \
        "FROM SALESDOCUMENT " \
        "join OrderPartner       On      SALESDOCUMENT.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode " \
        "                                And     OrderPartner.CustomerSupplierType = 1 " \
        "join BusinessPartner    On      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
        "JOIN Agent                      ON SALESDOCUMENT.Agent1Code                             = Agent.Code  " \
        "JOIN BusinessUnitVsCompany BUC  ON SalesDocument.DivisionCode   = BUC.DivisionCode " \
        "JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode = BUnit.Code And BUnit.GroupFlag = 0 " \
        "JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code And Company.GroupFlag = 1 " \
        "JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE " \
        "									AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE  = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
        "JOIN LOGICALWAREHOUSE           ON SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE " \
        "									AND LOGICALWAREHOUSE.plantcode                          = BUC.factorycode " \
        "JOIN ITEMTYPE                   ON SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = ITEMTYPE.CODE " \
        "JOIN COSTCENTER                 ON SALESDOCUMENTLINE.COSTCENTERCODE                     = COSTCENTER.CODE " \
        "JOIN QUALITYLEVEL               ON SALESDOCUMENTLINE.QUALITYCODE                        = QUALITYLEVEL.CODE " \
        "                                AND SALESDOCUMENTLINE.ITEMTYPEAFICODE                   = QUALITYLEVEL.ITEMTYPECODE " \
        "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = IST.ItemTypeCode " \
        "									AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
        "JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
        "                                    AND     Case IST.Position  " \
        "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03  " \
        "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06  " \
        "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09  " \
        "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code " \
        "join         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
        "Join Product            On      SALESDOCUMENTLINE.ITEMTYPEAFICODE = Product.ITEMTYPECODE  " \
        "                                And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
        " WHERE SALESDOCUMENT.PROVISIONALDOCUMENTDATE between '" + str(stdt) + "' and '" + str(etdt) + "' " + sqlwhere + " " \
                                                                                                                         " ORDER BY COSTCENTER.LONGDESCRIPTION ,SALESDOCUMENT.PROVISIONALDOCUMENTDATE "

    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        global counter
        counter=counter+1
        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 14:
            pdfrpt.d = 730
            pdfrpt.c.showPage()
            pdfrpt.header(stdt, etdt, pdfrpt.divisioncode)
            pdfrpt.d = pdfrpt.d - 20
            # pdfrpt.productname(result, pdfrpt.d)
    pdfrpt.printcustomertotal(pdfrpt.d)
    pdfrpt.printagenttotal(pdfrpt.d)
    pdfrpt.printdepartmenttotal(pdfrpt.d)

    # print("after while")
    if result == False:
        if counter >= 0:
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(8)
            Exceptions = ""
            pdfrpt.c.drawAlignedString(225, pdfrpt.d, str("%.3f" % float(pdfrpt.CompanyQuentityTotal)))
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria"
            return

    if counter==0:
        Exceptions = "Note: No Result found according to your selected criteria "
    else:
        pdfrpt.c.showPage()
        pdfrpt.c.save()
        # url = "file:///D:/Reports/ReportDevelopment/" + LSFileName + ".pdf"
        # os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()
    # print("counter")
    # print(counter)


def ChallanRegisterSummary(LSselcompany, LSselparty, LSsellotno, LSselquality, LSselfromdepartment, LSseltodepartment,
                           LSselwindingtype, LSselagent, LSselshade, LSallcompany, LSallparty, LSalllotno,
                           LSallquality,
                           LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent, LSallshade,
                           LDStartDate, LDEndDate, LSFileName,sqlwhere):


    print("------------------")
    print(sqlwhere)
    print("------------------")
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    sql = "SELECT   COSTCENTER.LONGDESCRIPTION AS DeptName " \
          "        , SALESDOCUMENT.PROVISIONALCODE AS CHALLANNUMBER " \
          "        , SALESDOCUMENT.PROVISIONALDOCUMENTDATE AS CHALLANDATE " \
          "        , Product.LONGDESCRIPTION As Product " \
          "        , SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS QUANTITY " \
          "        , SALESDOCUMENTLINE.PRICE " \
          "        , Agent.LongDescription As AGENT " \
          "        , UGG.Code As ShadeCode " \
          "        , BusinessPartner.LEGALNAME1  AS CUSTOMER " \
          "FROM SALESDOCUMENT " \
          "join OrderPartner       On      SALESDOCUMENT.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode " \
          "                                And     OrderPartner.CustomerSupplierType = 1 " \
          "join BusinessPartner    On      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
          "JOIN Agent                      ON SALESDOCUMENT.Agent1Code                             = Agent.Code  " \
          "JOIN BusinessUnitVsCompany BUC  ON SalesDocument.DivisionCode   = BUC.DivisionCode " \
          "JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode = BUnit.Code And BUnit.GroupFlag = 0 " \
          "JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code And Company.GroupFlag = 1 " \
          "JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE " \
          "									AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE  = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
          "JOIN LOGICALWAREHOUSE           ON SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE " \
          "									AND LOGICALWAREHOUSE.plantcode                          = BUC.factorycode " \
          "JOIN ITEMTYPE                   ON SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = ITEMTYPE.CODE " \
          "JOIN COSTCENTER                 ON SALESDOCUMENTLINE.COSTCENTERCODE                     = COSTCENTER.CODE " \
          "JOIN QUALITYLEVEL               ON SALESDOCUMENTLINE.QUALITYCODE                        = QUALITYLEVEL.CODE " \
          "                                AND SALESDOCUMENTLINE.ITEMTYPEAFICODE                   = QUALITYLEVEL.ITEMTYPECODE " \
          "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "									AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
          "JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "                                    AND     Case IST.Position  " \
          "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03  " \
          "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06  " \
          "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09  " \
          "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code " \
          "join         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join Product            On      SALESDOCUMENTLINE.ITEMTYPEAFICODE = Product.ITEMTYPECODE  " \
          "                                And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
          " WHERE SALESDOCUMENT.PROVISIONALDOCUMENTDATE between '" + str(stdt) + "' and '" + str(
        etdt) + "' " + sqlwhere + " " \
                                  " ORDER BY COSTCENTER.LONGDESCRIPTION ,SALESDOCUMENT.PROVISIONALDOCUMENTDATE "

    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize1(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 14:
            pdfrpt.d = 730
            pdfrpt.c.showPage()
            pdfrpt.header1(stdt, etdt, pdfrpt.divisioncode)
            pdfrpt.d = pdfrpt.d - 20
            # pdfrpt.productname(result, pdfrpt.d)
    pdfrpt.printregistersummarytotal(pdfrpt.d)


    # print("after while")
    if result == False:
        if counter >= 0:
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(8)
            Exceptions = ""
            pdfrpt.c.drawAlignedString(225, pdfrpt.d, str("%.3f" % float(pdfrpt.CompanyQuentityTotal)))
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria"
            return

    if counter == 0:
        Exceptions = "Note: No Result found according to your selected criteria "
    else:
        pdfrpt.c.showPage()
        pdfrpt.c.save()
        url = "file:///D:/Reports/ReportDevelopment/" + LSFileName + ".pdf"
        os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()

def AgentPartyItemWiseRegisterSummary(LSselcompany,LSselparty,LSsellotno,LSselquality,LSselfromdepartment,LSseltodepartment,
                         LSselwindingtype,LSselagent,LSselshade,LSallcompany, LSallparty, LSalllotno, LSallquality,
                         LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent, LSallshade,
                         LDStartDate,LDEndDate,LSFileName,sqlwhere,sql):
    print("------------------")
    print(sqlwhere)
    print("------------------")
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    # sql = "SELECT   COSTCENTER.LONGDESCRIPTION AS DeptName " \
    #       "        , SALESDOCUMENT.PROVISIONALCODE AS CHALLANNUMBER " \
    #       "        , SALESDOCUMENT.PROVISIONALDOCUMENTDATE AS CHALLANDATE " \
    #       "        , Product.LONGDESCRIPTION As Product " \
    #       "        , SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS QUANTITY " \
    #       "        , SALESDOCUMENTLINE.PRICE " \
    #       "        , Agent.LongDescription As AGENT " \
    #       "        , UGG.Code As ShadeCode " \
    #       "        , BusinessPartner.LEGALNAME1  AS CUSTOMER " \
    #       "FROM SALESDOCUMENT " \
    #       "join OrderPartner       On      SALESDOCUMENT.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode " \
    #       "                                And     OrderPartner.CustomerSupplierType = 1 " \
    #       "join BusinessPartner    On      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
    #       "JOIN Agent                      ON SALESDOCUMENT.Agent1Code                             = Agent.Code  " \
    #       "JOIN BusinessUnitVsCompany BUC  ON SalesDocument.DivisionCode   = BUC.DivisionCode " \
    #       "JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode = BUnit.Code And BUnit.GroupFlag = 0 " \
    #       "JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code And Company.GroupFlag = 1 " \
    #       "JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE " \
    #       "									AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE  = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
    #       "JOIN LOGICALWAREHOUSE           ON SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE " \
    #       "									AND LOGICALWAREHOUSE.plantcode                          = BUC.factorycode " \
    #       "JOIN ITEMTYPE                   ON SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = ITEMTYPE.CODE " \
    #       "JOIN COSTCENTER                 ON SALESDOCUMENTLINE.COSTCENTERCODE                     = COSTCENTER.CODE " \
    #       "JOIN QUALITYLEVEL               ON SALESDOCUMENTLINE.QUALITYCODE                        = QUALITYLEVEL.CODE " \
    #       "                                AND SALESDOCUMENTLINE.ITEMTYPEAFICODE                   = QUALITYLEVEL.ITEMTYPECODE " \
    #       "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = IST.ItemTypeCode " \
    #       "									AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
    #       "JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
    #       "                                    AND     Case IST.Position  " \
    #       "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03  " \
    #       "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06  " \
    #       "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09  " \
    #       "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code " \
    #       "join         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
    #       "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
    #       "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
    #       "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
    #       "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
    #       "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
    #       "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
    #       "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
    #       "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
    #       "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
    #       "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
    #       "Join Product            On      SALESDOCUMENTLINE.ITEMTYPEAFICODE = Product.ITEMTYPECODE  " \
    #       "                                And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
    #       " WHERE SALESDOCUMENT.PROVISIONALDOCUMENTDATE between '" + str(stdt) + "' and '" + str(
    #     etdt) + "' " + sqlwhere + " " \
    #                               " ORDER BY COSTCENTER.LONGDESCRIPTION ,SALESDOCUMENT.PROVISIONALDOCUMENTDATE "

    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize2(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 14:
            pdfrpt.d = 730
            pdfrpt.c.showPage()
            pdfrpt.header2(stdt, etdt, pdfrpt.divisioncode)
            pdfrpt.d = pdfrpt.d - 20


    pdfrpt.printtotal2(pdfrpt.d)
    pdfrpt.printdepartmenttotal2(pdfrpt.d)
    print("before result")
    print(result)
    # # print("after while")
    if result == False:
        # global counter
        if counter >= 0:
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(8)
            Exceptions = ""
            pdfrpt.c.drawAlignedString(225, pdfrpt.d, str("%.3f" % float(pdfrpt.CompanyQuentityTotal)))
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria"
            return

    if counter==0:
        Exceptions = "Note: No Result found according to your selected criteria "
    else:
        pdfrpt.c.showPage()
        pdfrpt.c.save()
        url = "file:///D:/Reports/ReportDevelopment/" + LSFileName + ".pdf"
        os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()


def PartyAgentItemWiseRegisterSummary(LSselcompany,LSselparty,LSsellotno,LSselquality,LSselfromdepartment,LSseltodepartment,
                         LSselwindingtype,LSselagent,LSselshade,LSallcompany, LSallparty, LSalllotno, LSallquality,
                         LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent, LSallshade,
                         LDStartDate,LDEndDate,LSFileName,sqlwhere):

    # sqlwhere=''
    print("------------------")
    print (sqlwhere)
    print("------------------")
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()


    sql="SELECT   COSTCENTER.LONGDESCRIPTION AS DeptName " \
        "        , SALESDOCUMENT.PROVISIONALCODE AS CHALLANNUMBER " \
        "        , SALESDOCUMENT.PROVISIONALDOCUMENTDATE AS CHALLANDATE " \
        "        , Agent.LongDescription As AGENT " \
        "        , trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS PRODUCT " \
        "        , SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS QUANTITY " \
        "        , Int((SALESDOCUMENTLINE.USERPRIMARYQUANTITY * COALESCE(IndTaxDetail.calculatedvalue,0))+0.50) As InvoiceAmount " \
        "        , UGG.Code As ShadeCode " \
        "        , BusinessPartner.LEGALNAME1  AS CUSTOMER " \
        "        , count(*) over(partition by Product.LONGDESCRIPTION)  as ITEMCOUNT " \
        "FROM SALESDOCUMENT " \
        "join OrderPartner       On      SALESDOCUMENT.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode " \
        "                                And     OrderPartner.CustomerSupplierType = 1 " \
        "join BusinessPartner    On      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
        "JOIN Agent                      ON SALESDOCUMENT.Agent1Code                             = Agent.Code  " \
        "JOIN BusinessUnitVsCompany BUC  ON SalesDocument.DivisionCode   = BUC.DivisionCode " \
        "JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode = BUnit.Code And BUnit.GroupFlag = 0 " \
        "JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code And Company.GroupFlag = 1 " \
        "JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE " \
        "									AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE  = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
        "JOIN LOGICALWAREHOUSE           ON SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE " \
        "									AND LOGICALWAREHOUSE.plantcode                          = BUC.factorycode " \
        "JOIN ITEMTYPE                   ON SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = ITEMTYPE.CODE " \
        "JOIN COSTCENTER                 ON SALESDOCUMENTLINE.COSTCENTERCODE                     = COSTCENTER.CODE " \
        "JOIN QUALITYLEVEL               ON SALESDOCUMENTLINE.QUALITYCODE                        = QUALITYLEVEL.CODE " \
        "                                AND SALESDOCUMENTLINE.ITEMTYPEAFICODE                   = QUALITYLEVEL.ITEMTYPECODE " \
        "LEFT JOIN INDTAXDETAIL          ON salesdocumentline.absuniqueid                        = INDTAXDETAIL.absuniqueid " \
        "                                AND INDTAXDETAIL.ITaxCOde = 'INR' " \
        "                                And INDTAXDETAIL.TaxCategoryCode = 'OTH' " \
        "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = IST.ItemTypeCode " \
        "									AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
        "JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
        "                                    AND     Case IST.Position  " \
        "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03  " \
        "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06  " \
        "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09  " \
        "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code " \
        "join         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
        "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
        "Join Product            On      SALESDOCUMENTLINE.ITEMTYPEAFICODE = Product.ITEMTYPECODE  " \
        "                                And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
        " WHERE SALESDOCUMENT.PROVISIONALDOCUMENTDATE between '" + str(stdt) + "' and '" + str(etdt) + "' " + sqlwhere + " " \
                                                                                                                         " ORDER BY COSTCENTER.LONGDESCRIPTION ,SALESDOCUMENT.PROVISIONALDOCUMENTDATE "
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        global counter
        counter=counter+1
        pdfrpt.textsize3(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 14:
            pdfrpt.d = 730
            pdfrpt.c.showPage()
            pdfrpt.header3(stdt, etdt, pdfrpt.divisioncode)
            pdfrpt.d = pdfrpt.d - 20
            # pdfrpt.productname(result, pdfrpt.d)
    pdfrpt.printtotal3(pdfrpt.d)
    pdfrpt.printdepartmenttotal3(pdfrpt.d)
    # pdfrpt.printagenttotal(pdfrpt.d)
    # pdfrpt.printdepartmenttotal(pdfrpt.d)

    # print("after while")
    if result == False:
        if counter >= 0:
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(8)
            Exceptions = ""
            pdfrpt.c.drawAlignedString(225, pdfrpt.d, str("%.3f" % float(pdfrpt.CompanyQuentityTotal)))
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria"
            return

    if counter==0:
        Exceptions = "Note: No Result found according to your selected criteria "
    else:
        pdfrpt.c.showPage()
        pdfrpt.c.save()
        url = "file:///D:/Reports/ReportDevelopment/" + LSFileName + ".pdf"
        os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()
    # print("counter")
    # print(counter)

def ItemAgentPartyWiseRegisterSummary(LSselcompany,LSselparty,LSsellotno,LSselquality,LSselfromdepartment,LSseltodepartment,
                         LSselwindingtype,LSselagent,LSselshade,LSallcompany, LSallparty, LSalllotno, LSallquality,
                         LSallfromdepartment, LSalltodepartment, LSallwindingtype, LSallagent, LSallshade,
                         LDStartDate,LDEndDate,LSFileName,sqlwhere):
    print("------------------")
    print(sqlwhere)
    print("------------------")
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()

    sql = "SELECT   COSTCENTER.LONGDESCRIPTION AS DeptName " \
          "        , SALESDOCUMENT.PROVISIONALCODE AS CHALLANNUMBER " \
          "        , SALESDOCUMENT.PROVISIONALDOCUMENTDATE AS CHALLANDATE " \
          "        , Agent.LongDescription As AGENT " \
          "        , trim (Product.LONGDESCRIPTION || ' ' ||  QualityLevel.ShortDescription) AS PRODUCT " \
          "        , SALESDOCUMENTLINE.USERPRIMARYQUANTITY AS QUANTITY " \
          "        , Int((SALESDOCUMENTLINE.USERPRIMARYQUANTITY * COALESCE(IndTaxDetail.calculatedvalue,0))+0.50) As InvoiceAmount " \
          "        , UGG.Code As ShadeCode " \
          "        , BusinessPartner.LEGALNAME1  AS CUSTOMER " \
          "        , count(*) over(partition by Product.LONGDESCRIPTION)  as ITEMCOUNT " \
          "FROM SALESDOCUMENT " \
          "join OrderPartner       On      SALESDOCUMENT.OrdPrnCustomerSupplierCode = OrderPartner.CustomerSupplierCode " \
          "                                And     OrderPartner.CustomerSupplierType = 1 " \
          "join BusinessPartner    On      OrderPartner.OrderbusinessPartnerNumberId = BusinessPartner.NumberID " \
          "JOIN Agent                      ON SALESDOCUMENT.Agent1Code                             = Agent.Code  " \
          "JOIN BusinessUnitVsCompany BUC  ON SalesDocument.DivisionCode   = BUC.DivisionCode " \
          "JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode = BUnit.Code And BUnit.GroupFlag = 0 " \
          "JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code And Company.GroupFlag = 1 " \
          "JOIN SALESDOCUMENTLINE          ON SALESDOCUMENTLINE.SALESDOCUMENTPROVISIONALCODE       = SALESDOCUMENT.PROVISIONALCODE " \
          "									AND     SALESDOCUMENTLINE.SALDOCPROVISIONALCOUNTERCODE  = SALESDOCUMENT.PROVISIONALCOUNTERCODE " \
          "JOIN LOGICALWAREHOUSE           ON SALESDOCUMENTLINE.WAREHOUSECODE                      = LOGICALWAREHOUSE.CODE " \
          "									AND LOGICALWAREHOUSE.plantcode                          = BUC.factorycode " \
          "JOIN ITEMTYPE                   ON SALESDOCUMENTLINE.ITEMTYPEAFICODE                    = ITEMTYPE.CODE " \
          "JOIN COSTCENTER                 ON SALESDOCUMENTLINE.COSTCENTERCODE                     = COSTCENTER.CODE " \
          "JOIN QUALITYLEVEL               ON SALESDOCUMENTLINE.QUALITYCODE                        = QUALITYLEVEL.CODE " \
          "                                AND SALESDOCUMENTLINE.ITEMTYPEAFICODE                   = QUALITYLEVEL.ITEMTYPECODE " \
          "LEFT JOIN INDTAXDETAIL          ON salesdocumentline.absuniqueid                        = INDTAXDETAIL.absuniqueid " \
          "                                AND INDTAXDETAIL.ITaxCOde = 'INR' " \
          "                                And INDTAXDETAIL.TaxCategoryCode = 'OTH' " \
          "JOIN ItemSubcodeTemplate IST    ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = IST.ItemTypeCode " \
          "									AND     IST.GroupTypeCode In ('MB4','P09','B07') " \
          "JOIN UserGenericGroup UGG       ON      IST.GroupTypeCode = UGG.UserGenericGroupTypeCode " \
          "                                    AND     Case IST.Position  " \
          "When 1 Then SALESDOCUMENTLINE.SubCode01 When 2 Then SALESDOCUMENTLINE.SubCode02 When 3 Then SALESDOCUMENTLINE.SubCode03  " \
          "When 4 Then SALESDOCUMENTLINE.SubCode04 When 5 Then SALESDOCUMENTLINE.SubCode05 When 6 Then SALESDOCUMENTLINE.SubCode06  " \
          "When 7 Then SALESDOCUMENTLINE.SubCode07 When 8 Then SALESDOCUMENTLINE.SubCode08 When 9 Then SALESDOCUMENTLINE.SubCode09  " \
          "When 10 Then SALESDOCUMENTLINE.SubCode10 End = UGG.Code " \
          "join         FullItemKeyDecoder FIKD     ON      SALESDOCUMENTLINE.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "                                AND     COALESCE(SALESDOCUMENTLINE.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join Product            On      SALESDOCUMENTLINE.ITEMTYPEAFICODE = Product.ITEMTYPECODE  " \
          "                                And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
          " WHERE SALESDOCUMENT.PROVISIONALDOCUMENTDATE between '" + str(stdt) + "' and '" + str(
        etdt) + "' " + sqlwhere + " " \
                                  " ORDER BY COSTCENTER.LONGDESCRIPTION ,SALESDOCUMENT.PROVISIONALDOCUMENTDATE "
    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize4(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 14:
            pdfrpt.d = 730
            pdfrpt.c.showPage()
            pdfrpt.header4(stdt, etdt, pdfrpt.divisioncode)
            pdfrpt.d = pdfrpt.d - 20
            # pdfrpt.productname(result, pdfrpt.d)
    pdfrpt.printtotal4(pdfrpt.d)
    pdfrpt.printdepartmenttotal4(pdfrpt.d)
    pdfrpt.printcompanytotal4(pdfrpt.d)

    # print("after while")
    if result == False:
        if counter >= 0:
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(7)
            pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
            pdfrpt.fonts(8)
            Exceptions = ""
            pdfrpt.c.drawAlignedString(225, pdfrpt.d, str("%.3f" % float(pdfrpt.CompanyQuentityTotal)))
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria"
            return

    if counter == 0:
        Exceptions = "Note: No Result found according to your selected criteria "
    else:
        pdfrpt.c.showPage()
        pdfrpt.c.save()
        url = "file:///D:/Reports/ReportDevelopment/" + LSFileName + ".pdf"
        os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()

    # pdfrpt.printtotal4(pdfrpt.d)
    # pdfrpt.printdepartmenttotal4(pdfrpt.d)
    # pdfrpt.printcompanytotal4(pdfrpt.d)
    # # pdfrpt.printagenttotal(pdfrpt.d)
    # # pdfrpt.printdepartmenttotal(pdfrpt.d)
    #
    # # print("after while")
    # if result == False:
    #     global counter
    #     if counter >= 0:
    #         pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
    #         pdfrpt.fonts(7)
    #         pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
    #         pdfrpt.fonts(8)
    #         Exceptions = ""
    #         # pdfrpt.c.drawAlignedString(225, pdfrpt.d, str("%.3f" % float(pdfrpt.CompanyQuentityTotal)))
    #     elif counter == 0:
    #         Exceptions = "Note: No Result found according to your selected criteria"
    #         return
    #
    # if counter==0:
    #     Exceptions = "Note: No Result found according to your selected criteria "
    # else:
    #     pdfrpt.c.showPage()
    #     pdfrpt.c.save()
    #     url = "file:///D:/Reports/ReportDevelopment/" + LSFileName + ".pdf"
    #     os.startfile(url)
    #     pdfrpt.newrequest()
    #     pdfrpt.d = pdfrpt.newpage()
    # # print("counter")
    # print(counter)
