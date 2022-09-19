from django.http import HttpResponse
from django.shortcuts import render
from django.views.static import serve

from PrintPDF import StoreRegister_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
from FormLoad import  StoreRegister_FormLoad as views
import os
from  datetime import datetime
from ProcessSelection import StoreRegister_ProcessSelection as PRV
counter=0
def StoreRegisterPrintPDF(request) :
    print("start")
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    save_name = os.path.join(os.path.expanduser("~"), "D:/Report Development/Generated Reports/Store Register/",
                             LSFileName)
    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")
    LSChallanNo = request.GET.getlist('challanno')
    LSChallanDate = request.GET.getlist('challandt')
    # StartDate = "'" + LDStartDate + "'"
    # EndDate = "'" + LDEndDate + "'"
    # where = " AND ELEMENTS.ENTRYDATE BETWEEN " +StartDate +" AND "+EndDate
    # where=""
    sql=""

    result=""
    sql=" SELECT " \
    "        DIVISION.LONGDESCRIPTION AS DIVISION  " \
    "        , ID.PROVISIONALCODE AS CHALLANNO   " \
    "        , ID.PROVISIONALDOCUMENTDATE AS CHALLANDATE   " \
    "        , COALESCE(PLANT.ADDRESSLINE1,'') AS COMPANYADDRESS " \
    "        , BP.LEGALNAME1 AS PARTY " \
    "        , Coalesce(BP.ADDRESSLINE1,'') " \
    "       || Coalesce(','||BP.ADDRESSLINE2,'') " \
    "       || Coalesce(','||BP.ADDRESSLINE3,'') " \
    "       || Coalesce(','||BP.ADDRESSLINE4,'') " \
    "       ||','|| Coalesce(BP.ADDRESSLINE5,'') " \
    "       ||', Postal Code : '||Coalesce(BP.POSTALCODE,'') as PARTYRADDRESS" \
    "        , ADGSTIN.GSTINNUMBER AS COMPANYGST " \
    "        , IDL.ITEMDESCRIPTION AS ITEMNAME " \
    "        , COALESCE(PIE.TARIFFCODE,'') AS HSNNO " \
    "        , COALESCE(CAST(IDL.USERPRIMARYQUANTITY AS DECIMAL(20,3)),'')  AS ITEMQTY " \
    "        , IDL.USERPRIMARYUOMCODE AS ITEMUNIT " \
    "        , COALESCE(ITEM_REMARK.NOTE,'') AS ITEMREMARK " \
    "        , COALESCE(DOC_REMARK.NOTE,'') AS DOCREMARK " \
    "        , CGSTIN.GSTINNumber AS CUSTOMERGST " \
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
    " WHERE ID.TEMPLATECODE IN ('I02','I08','I09','IB2','IB8','IB9') order by CHALLANNO" \
    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    # stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    # etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    print("start 2")
    # Explicitly bind parameters
    # con.db.bind_param(stmt, 1, stdt)
    # con.db.bind_param(stmt, 2, etdt)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # except:
    #     PRV.Exceptions = "Database Connection Lost"
    #     return
    print("start 3 ")
    pdfrpt.newrequest()
    print("start 4 ")
    print(result)
    global  counter
    if result!=False:
        while result != False:
            pdfrpt.textsize(pdfrpt.c, result)
            # pdfrpt.d=pdfrpt.dvalue()
            result = con.db.fetch_both(stmt)
            counter=counter+1

            if pdfrpt.d<20:
                pdfrpt.d=630
                pdfrpt.c.showPage()
                pdfrpt.header("stdt","etdt",pdfrpt.divisioncode,result)
        pdfrpt.printdocremark()
        print("start 5")

        # pdfrpt.printasttotal()
        # pdfrpt.dvalue()
        # pdfrpt.printpallettotal()
        # pdfrpt.printdepertmenttotal()
        if result == False:
            print("start 5.1")
            if counter>0:
                pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
                pdfrpt.fonts(7)
                pdfrpt.companyclean()
                PRV.Exceptions=""
                print("start 5.1.1")
            elif counter==0:
                print(" forom Exceprition")
                PRV.Exceptions="Note: Please Select Valid Credentials"
                return
        print("start 6")

        # pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A4))
        # pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A3))
        pdfrpt.c.showPage()
        pdfrpt.c.save()
        # url="file:///D:/Report Development/Generated Reports/Purchase Register/"+LSFileName+".pdf"
        # os.startfile(url)
        pdfrpt.newrequest()
        pdfrpt.d=pdfrpt.newpage()
        print("start 7")
    else:
        PRV.Exceptions = "Note: Please Select Valid Credentials"
        return
    print("*-*-*-*-*-*-*-* end *-*-*-*-*-*---*")
    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'StoreRegister_Returnable_Table.html',
                      {'unit': views.unit, 'costcenter': views.costcenter, 'party': views.party,
                       'itemtype': views.itemtype,
                       'code': views.code, 'ccode': views.ccode, 'Exception': PRV.Exceptions})
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    # result=""