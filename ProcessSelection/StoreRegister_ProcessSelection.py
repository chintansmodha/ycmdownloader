import os
from datetime import datetime

from babel.numbers import format_currency
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.static import serve

from GetDataFromDB import StoreRegister_GetDataFromDB as SR
from PrintPDF import StoreRegister_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
from FormLoad import  StoreRegister_FormLoad as views

Exceptions = ""

counter = 0
GRetunable=[]

GChallanno=[]
GChallanDate=[]
GQuantity=[]
save_name = ''

def StoreRegister(request):
    global save_name
    # LSName = datetime.now()
    # LSstring = str(LSName)
    # LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
    #                                                                                                   17:19] + LSstring[
    #                                                                                                            20:]
    # save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Store Register/",
    #                          LSFileName)
    # pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    LSItemTypecode = request.GET.getlist('selitemtype')
    LSCostcentercode = request.GET.getlist('selcostcenter')
    LSPartycode = request.GET.getlist('selparty')
    LSUnitcode = request.GET.getlist('selunit')
    LDStartDate = str(request.GET['startdate'])
    LDEndDate = str(request.GET['enddate'])


    global GChallanno
    global GChallanDate
    global GQuantity

    Retunablelist(LSCostcentercode,LSPartycode,LSUnitcode,LDStartDate,LDEndDate,request)
    return  render(request,'StoreRegister_Returnable_Table.html',{'GChallanno':GChallanno,'GChallanDate':GChallanDate,'GQuantity':GQuantity,'GRetunable':GRetunable})

def Retunablelist(LSUnitcode,LSPartycode,LSItemTypecode,LDStartDate,LDEndDate,request):
    Costcenter = str(LSUnitcode)
    Costcenter = '(' + Costcenter[1:-1] + ')'
    Partycode = str(LSPartycode)
    Partycode = '(' + Partycode[1:-1] + ')'
    Itemcode = str(LSItemTypecode)
    Itemcode='('+Itemcode[1:-1]+')'

    print("costcenter : " + str(LSUnitcode))
    print("Party code : " + str(LSPartycode))
    print("Item code : " + str(LSItemTypecode))

    StartDate = "'" + LDStartDate + "'"
    EndDate = "'" + LDEndDate + "'"
    counter = 0
    if not LSUnitcode:
        Costcenter = " "
    elif LSUnitcode:
        Costcenter = " And Company.Code in " + Costcenter
    if not LSPartycode:
        Partycode = " "
    elif LSPartycode:
        Partycode = " And BusinessPartner.NumberId in " + Partycode
    if not LSItemTypecode:
        Itemcode=" "
    elif LSItemTypecode:
        Itemcode =" and INTERNALDOCUMENTLINE.ITEMTYPEAFICODE " + Itemcode

    print("costcenter : "+str(Costcenter))
    print("Party code : "+str(Partycode))
    print("Item code : "+str(Itemcode))
    SQLWHERE = " AND ID.PROVISIONALDOCUMENTDATE BETWEEN "+ str(StartDate) + " and " + str(EndDate) + " " + Costcenter + Partycode+ Itemcode


    sql = ""
    sql = " SELECT " \
    "        DIVISION.LONGDESCRIPTION AS DIVISION  " \
    "        , ID.PROVISIONALCODE AS CHALLANNO  " \
    "        , ID.PROVISIONALDOCUMENTDATE AS CHALLANDATE  " \
    "        , COALESCE(PLANT.ADDRESSLINE1,'') AS COMPANYADDRESS " \
    "        , BP.LEGALNAME1 AS SUPPLIERNAME " \
    "        , ADGSTIN.GSTINNUMBER AS COMPANYGST " \
    "        , IDL.ITEMDESCRIPTION AS ITEMNAME " \
    "        , COALESCE(PIE.TARIFFCODE,'') AS HSNNO " \
    "        , COALESCE(CAST(IDL.USERPRIMARYQUANTITY AS DECIMAL(20,3)) ||' ' || IDL.USERPRIMARYUOMCODE ,'') AS QUANTITY " \
    "        , COALESCE(ITEM_REMARK.NOTE,'') AS ITEMREMARK " \
    "        , COALESCE(DOC_REMARK.NOTE,'') AS DOCREMARK " \
    " FROM    INTERNALDOCUMENT        ID " \
    " JOIN    DIVISION                                ON      DIVISION.CODE                   = ID.DIVISIONCODE " \
    " JOIN    ORDERPARTNER            OP              ON      ID.ORDPRNCUSTOMERSUPPLIERCODE   = OP.CUSTOMERSUPPLIERCODE " \
    " JOIN    BUSINESSPARTNER         BP              ON      OP.ORDERBUSINESSPARTNERNUMBERID = BP.NUMBERID " \
    " JOIN    AddressGst              CGSTIN          ON      CGSTIN.UniqueID                 = BP.AbsUniqueId " \
    " JOIN    LOGICALWAREHOUSE        LWH             ON      ID.WAREHOUSECODE                = LWH.CODE " \
    " JOIN    PLANT                                   ON      LWH.PLANTCODE                   = PLANT.CODE " \
    " JOIN    FACTORY                                 ON      PLANT.CODE                      = FACTORY.CODE " \
    " LEFT JOIN ADDRESSGST            ADGSTIN         ON      FACTORY.ABSUNIQUEID             = ADGSTIN.UNIQUEID " \
    " LEFT JOIN    NOTE               DOC_REMARK      ON      DOC_REMARK.FATHERID             = ID.ABSUNIQUEID " \
    " JOIN    INTERNALDOCUMENTLINE    IDL             ON      IDL.INTDOCUMENTPROVISIONALCODE  = ID.PROVISIONALCODE " \
    " LEFT JOIN    NOTE               ITEM_REMARK     ON      ITEM_REMARK.FATHERID            = IDL.ABSUNIQUEID " \
    " JOIN FullItemKeyDecoder FIKD                    ON      IDL.ITEMTYPEAFICODE             = FIKD.ITEMTYPECODE  " \
    "                            AND     COALESCE(IDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')   " \
    "                            AND     COALESCE(IDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '')   " \
    "                            AND     COALESCE(IDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')   " \
    "                            AND     COALESCE(IDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '')   " \
    "                            AND     COALESCE(IDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '')   " \
    "                            AND     COALESCE(IDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '')   " \
    "                            AND     COALESCE(IDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')   " \
    "                            AND     COALESCE(IDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '')   " \
    "                            AND     COALESCE(IDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '')   " \
    "                            AND     COALESCE(IDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '')   " \
    " LEFT Join PRODUCTIE             PIE               On      IDL.ITEMTYPEAFICODE           = PIE.ITEMTYPECODE " \
    "                            And     FIKD.ItemUniqueId                           = PIE.AbsUniqueId " \
    " WHERE ID.TEMPLATECODE IN ('I02','I08','I09','IB2','IB8','IB9') "

    sql+=SQLWHERE

    # print("query for the Store table list")
    print(sql)
    GRetunable.clear()
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    if result != False:
        while result != False:
            GRetunable.append(result)
            # print(result['CHALLANNUMBER'])
            result = con.db.fetch_both(stmt)
    else:
        # return render(request, 'StoreRegister.html',
        #               {'unit': unit, 'costcenter': costcenter, 'party': party, 'itemtype': itemtype, 'code': code,
        #                'ccode': ccode})
        Exceptions = "Note: Please Select Valid Credentials"
        return
