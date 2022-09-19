import os
from datetime import datetime

from django.shortcuts import render
from django.views.static import serve

from FormLoad import PrintProformaInv_Formload as views

from Global_Files import Connection_String as con
from PrintPDF import PrintProformaAnx_PrintPDF as pdfrpt
save_name=""

Exceptions=""

counter=0


def PrintPDF(InvoiceNos, InvoiceDts, startdate, enddate):
    global Exceptions
    sql = "SELECT        Comp.LONGDESCRIPTION As Shiper " \
          ", Firm.IECODE As ShiperIecNo " \
          ", COALESCE(PLANTINVOICE.CONTAINERSIZE, '') As ContSize " \
          ", COALESCE(PLANTINVOICE.CONTAINERNO, '') As ContNO " \
          ", PlantInvoice.CODE As InvoiceNo " \
          ", Coalesce(Firm.IECODEISSUINGAUTHORITY,'') As EXCISEOFFICERNAME " \
          ", Coalesce(BpWeighParty.TAXREGISTRATIONNUMBER,'') As RegNo " \
          ", BpWeighParty.LEGALNAME1 As WeighPartyName " \
          ", COALESCE(BpWeighParty.ADDRESSLINE1, '') ||'   '|| COALESCE(BpWeighParty.ADDRESSLINE2, '') ||'   '|| COALESCE(BpWeighParty.ADDRESSLINE3, '') " \
          "||'   '|| COALESCE(BpWeighParty.ADDRESSLINE4, '') ||'   '|| COALESCE(BpWeighParty.ADDRESSLINE5, '') ||' - '|| COALESCE(BpWeighParty.POSTALCODE, '') As WeighPartyNameAdd " \
          ", ContWt.VALUESTRING As ContWt " \
          ", CargoWt.VALUESTRING As CargoWt " \
          ", DateWeigh.VALUESTRING As DateOfWeigh " \
          ", TypeCargo.VALUESTRING As TypeOfCargo " \
          ", SD.PROVISIONALCODE As GSTInvoiceNo " \
          ", Coalesce(PlantInvoice.CATEGORY,'') As MasterExpNo " \
          ", EXO_Desc.ValueString As ExOfficeName " \
          "From PlantInvoice " \
          "JOIN FIRM                               ON      plantinvoice.DIVISIONCODE = FIRM.CODE " \
          "JOIN PLANTINVOICELINE  PIL              ON 	PIL.PLANTINVOICECODE = PLANTINVOICE.CODE " \
          "AND 	PIL.PLANTINVOICEDIVISIONCODE = PLANTINVOICE.DIVISIONCODE " \
          "Join LOGICALWAREHOUSE                   On      PIL.LOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Join BUSINESSUNITVSCOMPANY BUC          On      LOGICALWAREHOUSE.PLANTCODE = BUC.FACTORYCODE " \
          "Join FINBUSINESSUNIT                    On      BUC.BUSINESSUNITCODE = FINBUSINESSUNIT.CODE " \
          "And     FINBUSINESSUNIT.GROUPFLAG = 0 " \
          "Join FINBUSINESSUNIT Comp               On      FINBUSINESSUNIT.GROUPBUCODE = Comp.CODE " \
          "Left Join CUSTOMINVOICE                       On      PLANTINVOICE.CUSTOMINVOICECODE = CUSTOMINVOICE.CODE " \
          "And     PLANTINVOICE.CUSTOMINVOICETYPECODE = CUSTOMINVOICE.INVOICETYPECODE " \
          "Left Join AdStorage AdWeighParty              On      CUSTOMINVOICE.ABSUNIQUEID = AdWeighParty.UNIQUEID " \
          "AND     AdWeighParty.NameEntityName = 'CustomInvoice' " \
          "And     AdWeighParty.FieldName = 'WeighPartyName' " \
          "Left Join ORDERPARTNER OpWeighParty           On      AdWeighParty.VALUESTRING = OpWeighParty.CUSTOMERSUPPLIERCODE " \
          "And     OpWeighParty.CUSTOMERSUPPLIERTYPE = 2 " \
          "Left Join BUSINESSPARTNER BpWeighParty        On      OpWeighParty.ORDERBUSINESSPARTNERNUMBERID = BpWeighParty.NUMBERID " \
          "Left Join AdStorage DateWeigh                 On      CUSTOMINVOICE.ABSUNIQUEID = DateWeigh.UNIQUEID " \
          "AND     DateWeigh.NameEntityName = 'CustomInvoice'  " \
          "And     DateWeigh.FieldName = 'DateandTimeofWeighing' " \
          "Left Join AdStorage TypeCargo                 On      CUSTOMINVOICE.ABSUNIQUEID = TypeCargo.UNIQUEID " \
          "AND     TypeCargo.NameEntityName = 'CustomInvoice' " \
          "And     TypeCargo.FieldName = 'TypeOfCargo' " \
          "Left Join AdStorage ContWt                    On      CUSTOMINVOICE.ABSUNIQUEID = ContWt.UNIQUEID " \
          "AND     ContWt.NameEntityName = 'CustomInvoice' " \
          "And     ContWt.FieldName = 'ContainerTareWeight' " \
          "Left Join AdStorage CargoWt                   On      CUSTOMINVOICE.ABSUNIQUEID = CargoWt.UNIQUEID  " \
          "AND     CargoWt.NameEntityName = 'CustomInvoice' " \
          "And     CargoWt.FieldName = 'TotalcargoGrossWeight' " \
          "Left Join SALESDOCUMENT SD                    On      plantinvoice.SALESINVOICEPROVISIONALCODE = SD.PROVISIONALCODE " \
          "And     plantinvoice.SALINVOICEPRVCOUNTERCODE = SD.PROVISIONALCOUNTERCODE " \
          "And     SD.DOCUMENTTYPETYPE = '06' " \
          "Left Join  UserGenericGroup As EXO_Ugg        On      EXO_Ugg.USERGENERICGROUPTYPECODE = 'EXO' " \
          "Left Join  AdStorage EXO_Startingdt           On      EXO_Ugg.AbsUniqueId = EXO_Startingdt.UniqueId " \
          "And     EXO_Startingdt.NameEntityName = 'UserGenericGroup' " \
          "And     EXO_Startingdt.FieldName = 'StartingDate' " \
          "And     EXO_Startingdt.ValueDate <= PLANTINVOICE.INVOICEDATE " \
          "Left Join  AdStorage EXO_Endingdt             On      EXO_Ugg.AbsUniqueId = EXO_Endingdt.UniqueId " \
          "And     EXO_Endingdt.NameEntityName = 'UserGenericGroup' " \
          "And     EXO_Endingdt.FieldName = 'EndDate' " \
          "And     EXO_Endingdt.ValueDate >= PLANTINVOICE.INVOICEDATE " \
          "Left Join  AdStorage EXO_Plant                On      EXO_Ugg.AbsUniqueId = EXO_Plant.UniqueId " \
          "And     EXO_Plant.NameEntityName = 'UserGenericGroup' " \
          "And     EXO_Plant.FieldName = 'PlantCodeCode' " \
          "And     LOGICALWAREHOUSE.PlantCode = Exo_Plant.Valuestring " \
          "Left Join  AdStorage  EXO_Desc                On      EXO_Ugg.AbsUniqueId = EXO_Desc.UniqueId " \
          "And     EXO_Desc.NameEntityName = 'UserGenericGroup' " \
          "And     EXO_Desc.FieldName = 'Description' " \
          "Where  "+InvoiceNos+" " \
          "Order By Shiper, InvoiceNo "
    # try:
    stmt = con.db.prepare(con.conn, sql)
    # Explicitly bind parameters
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1
        pdfrpt.textsize(pdfrpt.c, result)
        pdfrpt.d = pdfrpt.dvalue()
        result = con.db.fetch_both(stmt)

        if pdfrpt.d < 130:
            pdfrpt.d = 435
            pdfrpt.c.showPage()
            pdfrpt.header(pdfrpt.divisioncode, result,pdfrpt.Yordno)

    if result == False:
        if counter > 0:

              pdfrpt.d = pdfrpt.dvalue()
              # pdfrpt.c.drawString(155, pdfrpt.d, "Lot No. :   " + str(pdfrpt.lotno[-1]))
              # pdfrpt.d = pdfrpt.dvalue()
              # pdfrpt.d = pdfrpt.dvalue()
              # pdfrpt.c.drawString(155, pdfrpt.d, "HSNCODE :  " + pdfrpt.hsncode[-1])
              # pdfrpt.d = pdfrpt.dvalue()
              # pdfrpt.d = pdfrpt.dvalue()
              # pdfrpt.c.drawString(155, pdfrpt.d, "COUNTRY OF ORIGIN:  " + str(pdfrpt.countryofOrigin[-1]).upper())
              # pdfrpt.c.line(400, 115, 580, 115)
              # pdfrpt.c.drawString(380, 105, "Total ")
              # pdfrpt.c.drawAlignedString(448, 105, str(pdfrpt.packages))
              # pdfrpt.c.drawAlignedString(500, 105, str('{0:1.3f}'.format(pdfrpt.grosswt)))
              # pdfrpt.c.drawAlignedString(565, 105, str('{0:1.3f}'.format(pdfrpt.netwt)))
              # # ************** groos wt and nt wt at shipping marks ,packages
              # pdfrpt.c.drawString(85, 420, str('{0:1.3f}'.format(pdfrpt.grosswt)))
              # pdfrpt.c.drawString(85, 410, str('{0:1.3f}'.format(pdfrpt.netwt)))
              # pdfrpt.c.drawString(85, 390, str(pdfrpt.packages))
              # pdfrpt.boldfonts(6)
              # pdfrpt.c.drawAlignedString(175, 450, str(pdfrpt.packages))  # No Of Cartons
              pdfrpt.fonts(7)
              pdfrpt.TotalClean()

              Exceptions = ""
              counter = 0
        elif counter == 0:
            Exceptions = "Note: No Result found according to your selected criteria "
            return


    pdfrpt.c.showPage()
    pdfrpt.c.save()
    pdfrpt.d = pdfrpt.newpage()
    pdfrpt.i = 0
    pdfrpt.TotalClean()
    pdfrpt.newrequest()
    # except:
    #       raise Exception("Please Run the Server Again ")