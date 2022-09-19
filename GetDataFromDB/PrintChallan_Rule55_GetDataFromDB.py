import os
from datetime import datetime

from django.shortcuts import render
from django.views.static import serve

from FormLoad import PrintYarnChallan_FormLoad as views
from ProcessSelection import PrintYarnChallan_ProcessSelection as PrintChallan_Views

from Global_Files import Connection_String as con
from PrintPDF import PrintChallanRule55_PrintPDF as pdfrpt
from django.http import FileResponse

save_name=""

counter=0

def PrintChallan_Rule55_PDF(request):
    global save_name
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[17:19] + LSstring[20:]
    LSFileName = "PrintChallan_Rule55" + LSFileName
    # save_name = os.path.join(os.path.expanduser("~"),"D:/Report Development/Generated Reports/Print Challan_Rule55/", LSFileName)

    save_name = os.path.join(os.path.expanduser("~"), LSFileName)

    pdfrpt.c = pdfrpt.canvas.Canvas(save_name + ".pdf")

    LSChallanNo = request.GET.getlist('challanno')
    LSChallanDate = request.GET.getlist('challandt')
    LSLotNo = request.GET.getlist('lotno')
    LSLrNo = request.GET.getlist('lrno')
    LSLrDt = request.GET.getlist('lrdt')
    LSQuantity = request.GET.getlist('qty')
    LSBoxes = request.GET.getlist('box')
    Company=''
    Party=''

    LSChallanNo = " AND SD.PROVISIONALCODE in "+"("+str(LSChallanNo)[1:-1]+")"
    LSChallanDate = " AND VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') in  "+"("+str(LSChallanDate)[1:-1]+")"

    PrintPDF(LSChallanNo,LSChallanDate,LSLotNo,LSLrNo,LSLrDt,LSQuantity,LSBoxes,Company,Party)

    filepath = save_name + ".pdf"
    if not os.path.isfile(filepath):
        return render(request, 'PrintChallanTable.html',{'GDataPrintChallan': PrintChallan_Views.GDataPrintChallan,'Exception':PrintChallan_Views.Exceptions})
    # return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    response = FileResponse(open(filepath, 'rb'))
    response['Content-Disposition'] = "attachment; filename=%s" % filepath
    return response

def PrintPDF(LSChallanNo,LSChallanDate,LSLotNo,LSLrNo,LSLrDt,LSQuantity,LSBoxes,Company,Party):
    sql = " select BUnit.LONGDESCRIPTION AS Unit, Plant.ADDRESSLINE1 As Address, SD.PROVISIONALCODE As ChallanNo," \
          " PRODUCTIE.TARIFFCODE As HSNCD,  ADG.GSTINNUMBER As GSTIN,COALESCE(Plant.POSTALCODE,'') As PINCODE," \
          " ADG.STATECODE As STATECODE, FIRM.PANNO As PAN, " \
          " COALESCE(ADDRESS.ADDRESSLINE1, '') As ADDRESS1," \
          " COALESCE(ADDRESS.ADDRESSLINE2, '') As ADDRESS2," \
          " COALESCE(ADDRESS.ADDRESSLINE3, '') As ADDRESS3," \
          " COALESCE(ADDRESS.ADDRESSLINE4, '') As ADDRESS4," \
          " COALESCE(ADDRESS.ADDRESSLINE5, '') As ADDRESS5," \
          " COALESCE(ADDRESS.POSTALCODE, '') As POSTALCODE," \
          " COALESCE(ADDRESS.TOWN, '') As TOWN," \
          " COALESCE(ADDRESS.DISTRICT,'') As DISTRICT," \
          " COALESCE(ADDRESSGST.GSTINNUMBER,'') As PARTYGSTINNUMBER," \
          " ADDRESSGST.PROVISIONALGSTINNUMBER,COALESCE(ADDRESSGST.STATECODE, '') As PARTYSTATECODE," \
          " COALESCE(ADDRESS.ADDRESSEE, '') As PARTYNAME," \
          " NOTE.NOTE As REMARKS,COALESCE(SD.NUMBERPLATE, '') As VEHICLENO," \
          " VARCHAR_FORMAT(SD.PROVISIONALDOCUMENTDATE, 'DD-MM-YYYY') As ChallanDate," \
          " 0 As LotNO,COALESCE(SD.EXTERNALREFERENCE, '') As LRNO, SD.EXTERNALREFERENCEDATE As LRDATE," \
          " cast(SDL.USERPRIMARYQUANTITY as decimal(18,3)) As Quantity," \
          " 0 As Boxes,0 As Cops, BP.LegalName1 As Party," \
          " COALESCE(TD.LongDescription,'') As TruckDriver," \
          " COALESCE(TD.DrivingLicence,'') As TruckDriverLicenceNo," \
          " COALESCE(BP_Trpt1.LegalName1,'') As TransporterName1," \
          " COALESCE(BP_Trpt2.LegalName1,'') As TransporterName2," \
          " COALESCE(BP_Trpt3.LegalName1,'') As TransporterName3," \
          " BP.ADDRESSLINE1, BP.ADDRESSLINE2, BP.ADDRESSLINE3," \
          " Product.Longdescription || ' ' || COALESCE(QualityLevel.ShortDescription,'') as Item" \
          " from SalesDocument As SD" \
          " JOIN BusinessUnitVsCompany BUC  ON      SD.DivisionCode   = BUC.DivisionCode " \
          " JOIN FinBusinessUnit BUnit      ON      BUC.BusinessUnitcode = BUnit.Code " \
          " And BUnit.GroupFlag = 0" \
          " JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code " \
          " And Company.GroupFlag = 1" \
          " join OrderPartner As OP         on SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode" \
          " And OP.CustomerSupplierType = 1" \
          " Join BusinessPartner As BP  On OP.ORDERBUSINESSPARTNERNUMBERID = BP.NumberID" \
          " Left Join TruckDriver TD     On      SD.TruckDriverCode = TD.Code" \
          " Left Join OrderPartner As OP_Trpt1      On      SD.FirstCarrierCode = OP_Trpt1.CustomerSupplierCode" \
          " And     SD.FirstCarrierType = OP_Trpt1.CustomerSupplierType" \
          " Left Join BusinessPartner As BP_Trpt1   On      OP_Trpt1.OrderBusinessPartnerNumberId = BP_Trpt1.NumberId" \
          " Left Join OrderPartner As OP_Trpt2      On      SD.SecondCarrierCode = OP_Trpt2.CustomerSupplierCode" \
          " And     SD.SecondCarrierType = OP_Trpt2.CustomerSupplierType" \
          " Left Join BusinessPartner As BP_Trpt2   On      OP_Trpt2.OrderBusinessPartnerNumberId = BP_Trpt2.NumberId" \
          " Left Join OrderPartner As OP_Trpt3      On      SD.ThirdCarrierCode = OP_Trpt3.CustomerSupplierCode" \
          " And     SD.ThirdCarrierType = OP_Trpt3.CustomerSupplierType" \
          " Left Join BusinessPartner As BP_Trpt3   On      OP_Trpt3.OrderBusinessPartnerNumberId = BP_Trpt3.NumberId" \
          " LEFT JOIN ADDRESSGST On BP.ABSUNIQUEID = ADDRESSGST.UNIQUEID" \
          " JOIN    FIRM ON SD.DIVISIONCODE = FIRM.CODE" \
          " LEFT JOIN ADDRESS       ON  BP.ABSUNIQUEID = ADDRESS.UNIQUEID" \
          " AND SD.DELIVERYPOINTCODE = ADDRESS.CODE" \
          " LEFT JOIN NOTE ON SD.ABSUNIQUEID = NOTE.FATHERID" \
          " join SalesDocumentLine  AS SDL  on SD.PROVISIONALCOUNTERCODE = SDL.SALDOCPROVISIONALCOUNTERCODE" \
          " AND SD.PROVISIONALCODE = SDL.SALESDOCUMENTPROVISIONALCODE" \
          " JOIN LOGICALWAREHOUSE   ON SDL.WAREHOUSECODE = LOGICALWAREHOUSE.CODE" \
          " AND     BUC.factorycode = LOGICALWAREHOUSE.plantcode" \
          " JOIN PLANT              ON      LOGICALWAREHOUSE.plantcode = PLANT.CODE" \
          " JOIN FACTORY            ON      PLANT.CODE = FACTORY.CODE" \
          " LEFT JOIN ADDRESSGST ADG ON     FACTORY.ABSUNIQUEID = ADG.UNIQUEID" \
          " join         FullItemKeyDecoder FIKD     ON      SDL.ITEMTYPEAFICODE = FIKD.ITEMTYPECODE" \
          " AND     COALESCE(SDL.SubCode01, '') = COALESCE(FIKD.SubCode01, '')" \
          " AND     COALESCE(SDL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          " AND     COALESCE(SDL.SubCode03, '') = COALESCE(FIKD.SubCode03, '')" \
          " AND     COALESCE(SDL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          " AND     COALESCE(SDL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          " AND     COALESCE(SDL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          " AND     COALESCE(SDL.SubCode07, '') = COALESCE(FIKD.SubCode07, '')  " \
          " AND     COALESCE(SDL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          " AND     COALESCE(SDL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          " AND     COALESCE(SDL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          " Join         Product            On      SDL.ITEMTYPEAFICODE = Product.ITEMTYPECODE " \
          " And     FIKD.ItemUniqueId = Product.ABSUNIQUEID " \
          " JOIN PRODUCTIE ON PRODUCT.ITEMTYPECODE = PRODUCTIE.ITEMTYPECODE " \
          " AND COALESCE(PRODUCT.SubCode01, '') = COALESCE(PRODUCTIE.SubCode01, '')" \
          " AND     COALESCE(PRODUCT.SubCode02, '') = COALESCE(PRODUCTIE.SubCode02, '') " \
          " AND     COALESCE(PRODUCT.SubCode03, '') = COALESCE(PRODUCTIE.SubCode03, '')" \
          " AND     COALESCE(PRODUCT.SubCode04, '') = COALESCE(PRODUCTIE.SubCode04, '') " \
          " AND     COALESCE(PRODUCT.SubCode05, '') = COALESCE(PRODUCTIE.SubCode05, '')" \
          " AND     COALESCE(PRODUCT.SubCode06, '') = COALESCE(PRODUCTIE.SubCode06, '') " \
          " AND     COALESCE(PRODUCT.SubCode07, '') = COALESCE(PRODUCTIE.SubCode07, '')" \
          " AND     COALESCE(PRODUCT.SubCode08, '') = COALESCE(PRODUCTIE.SubCode08, '') " \
          " AND     COALESCE(PRODUCT.SubCode09, '') = COALESCE(PRODUCTIE.SubCode09, '') " \
          " AND     COALESCE(PRODUCT.SubCode10, '') = COALESCE(PRODUCTIE.SubCode10, '') " \
          " JOIN QUALITYLEVEL ON PRODUCT.QUALITYGROUPCODE = QUALITYLEVEL.CODE " \
          " AND SDL.ITEMTYPEAFICODE = QUALITYLEVEL.ITEMTYPECODE " \
          " Where SD.DOCUMENTTYPETYPE='05' "+LSChallanNo+"" \
          " Order by ChallanNo"


    stmt = con.db.prepare(con.conn, sql)
    # Explicitly bind parameters
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, '', '')
        pdfrpt.d = pdfrpt.dvalue('', '',result,pdfrpt.divisioncode)
        result = con.db.fetch_both(stmt)

        # pdfrpt.c.line(0, 12, 600, 12)
        if pdfrpt.d < 20:
            pdfrpt.d = 560
            pdfrpt.c.showPage()
            pdfrpt.header('', '',result, pdfrpt.divisioncode)
            # pdfrpt.d=pdfrpt.d-20
            # pdfrpt.itemcodes(result, pdfrpt.d)

    if result == False:

        if counter > 0:
            # pdfrpt.signature(pdfrpt.d - 20)
            pdfrpt.fonts(9)
            pdfrpt.d = pdfrpt.dvalue('', '', result, pdfrpt.divisioncode)
            pdfrpt.printtotal('', '', result, pdfrpt.d)
            pdfrpt.companyclean()
            PrintChallan_Views.Exceptions = ""
        elif counter == 0:
            PrintChallan_Views.Exceptions = "Note: No Result found according to your selected criteria "
            return

    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.newrequest()
    counter = 0
    pdfrpt.d = pdfrpt.newpage()
