from datetime import datetime
from this import d
from Global_Files import Connection_String as con
from PrintPDF import ExciseRegister_ChallanTypeWise_PrintPDF as pdfrpt1
from PrintPDF import ExciseRegister_ChallanTypeWiseItemShade_PrintPDF as pdfrpt2
from PrintPDF import ExciseRegister_InvNoWise_PrintPDF as pdfrpt3
from PrintPDF import ExciseRegisterDepartmentWise_PrintPDF as pdfrpt
from FormLoad import ExciseRegister_FormLoad as views
counter=0



def ExciseRegister_GetData(LSCompany,LSChallanType,LSParty,LSCharges,LSAllCompanies,LSAllChallanTypes,
    LSAllParties,LSAllCharges,LSDepartment,LSItemType,LSChallanCategory,LSAllDepartments,LSAllItemTypes,LSAllChallanCategories,LDStartDate,
    LDEndDate,LSLotType):
	print(LSCompany)
	if not LSAllCompanies and not LSCompany or LSAllCompanies:
		LSCompany = ""
	elif LSCompany:
		LSCompany = " And Plant.Code in ("+str(LSCompany)[1:-1]+")"

	if not LSAllChallanTypes and not LSChallanType or LSAllChallanTypes:
		LSChallanType = ""
	elif LSChallanType:
		LSChallanType = " And pi.TAXTEMPLATECODE in ("+str(LSChallanType)[1:-1]+")"
	
	if not LSAllParties and not LSParty or LSAllParties:
		LSParty = ""
	elif LSParty:
		LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

	if not LSAllCharges and not LSCharges or LSAllCharges:
		LSCharges = ""
	elif LSCharges:
		LSCharges = " And Itax.Code in ("+str(LSCharges)[1:-1]+")"

	if not LSAllDepartments and not LSDepartment or LSAllDepartments:
		LSDepartment = ""
	elif LSDepartment:
		LSDepartment = " And Costcenter.Code in ("+str(LSDepartment)[1:-1]+")"

	if not LSAllItemTypes and not LSItemType or LSAllItemTypes:
		LSItemType = ""
	elif LSItemType:
		LSItemType = " And Itemtype.Code in ("+str(LSItemType)[1:-1]+")"

	if not LSAllChallanCategories and not LSChallanCategory or LSAllChallanCategories:
		LSChallanCategory = ""
	elif LSChallanCategory:
		LSChallanCategory = " And pi.TAXTEMPLATECODE in ("+str(LSChallanCategory)[1:-1]+")"

	print(LSCompany,LSChallanCategory,LSChallanType,LSCharges,LSParty,LSItemType,LSDepartment,LDEndDate,LDStartDate)
	sql=("Select  plant.longdescription as company "
                " ,SDL.PREVIOUSCODE as challanno "
	         " ,PI.code as invno "
	         " ,PI.INVOICEDATE as invdate "
	         " ,PI.TOTALQUANTITY as qty "
	         " ,PI.GROSSVALUE as invamt "
	         " ,SDL.PRICE as Rate "
	         " ,BP.Legalname1 as Party "
	         " ,IGST.CALCULATEDVALUE as IGST "
	         " ,CGST.CALCULATEDVALUE as CGST "
	         " ,UTGST.CALCULATEDVALUE as UTGST "
	         " ,BC.CALCULATEDVALUE as OTHCH "
	         " ,DR.CALCULATEDVALUE as GST "
	         " ,FRT.CALCULATEDVALUE as FRT "
	         " ,IC.CALCULATEDVALUE as INS "
	         " ,TCS.CALCULATEDVALUE as TCS "
			 ",COSTCENTER.LONGDESCRIPTION AS COST"
			 ",pi.TAXTEMPLATECODE AS CHALT"
 	 " from PlantInvoice PI "
 	 " Join Plant   ON PI.FactoryCode = Plant.code "
	 " Join SalesDocument SD           ON    PI.CODE = SD.PROVISIONALCODE "
	                                 " And SD.DOCUMENTTYPETYPE = '06' "
	 " JOIN SalesDocumentLine SDL      ON SD.PROVISIONALCODE=SDL.SALESDOCUMENTPROVISIONALCODE "
	                                 " AND  SD.PROVISIONALCOUNTERCODE=SDL.SALDOCPROVISIONALCOUNTERCODE "
	 " Join OrderPartner As OP         on SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode "
	                                " And OP.CustomerSupplierType = 1 "
	 " Join BusinessPartner BP ON OP.OrderBusinessPartnerNumberId = BP.NumberId "
	 " join LOGICALWAREHOUSE               On      plant.CODE  =      LOGICALWAREHOUSE.PlantCode  "
	 " Join PLANTINVOICELINE PIL               ON      PI.CODE = PIL.PLANTINVOICECODE  "
         " Left Join    COSTCENTER             On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE  "
	 " Left JOIN IndTaxDETAIL IGST              ON      PI.AbsUniqueId = IGST.ABSUNIQUEID    "
	 " AND     IGST.ITaxCode in('IG3','IG1','IG0','12G','IG2','IG8','IGS') "
	 " Left JOIN IndTaxDETAIL CGST              ON      PI.AbsUniqueId = CGST.ABSUNIQUEID    "
	 " AND     CGST.ITaxCode in('GCS','S14','CG3','CG2','CG6','SG6','CG1','CG9') "
	 " Left JOIN IndTaxDETAIL UTGST              ON      PI.AbsUniqueId = UTGST.ABSUNIQUEID    "
	 " AND     UTGST.ITaxCode in('SCG','T14','UG3','TG6','UG2','UG6','UC9','UG1') "
	 " Left Join IndTaxDETAIL    FRT                   ON      PI.AbsUniqueId = FRT.ABSUNIQUEID    "
	 " AND     FRT.ITaxCode = 'GFR'    "
	 " Left Join IndTaxDETAIL       IC                ON      PI.AbsUniqueId = IC.ABSUNIQUEID    "
	 " AND     IC.ITaxCode = 'GIN'    "
	 " Left Join IndTaxDETAIL    BC                   ON      PI.AbsUniqueId = BC.ABSUNIQUEID    "
	 " AND     BC.ITAXCODE = 'ROF'    "
	 " Left Join IndTaxDETAIL    DR                   ON      PI.AbsUniqueId = DR.ABSUNIQUEID    "
	 " AND     DR.TAXCATEGORYCODE = 'GST'   "
	 " Left Join IndTaxDETAIL    TCS                   ON      PI.AbsUniqueId = TCS.ABSUNIQUEID    "
	 " AND     TCS.TAXCATEGORYCODE = 'TCS'   "
	 " Left Join Itax on pi.ABSUNIQUEID = Itax.ABSUNIQUEID "
	 " where pi.invoicedate between '"+str(LDStartDate)+"' and '"+str(LDEndDate)+"' "+LSChallanCategory+LSChallanType+LSCharges+LSCompany+LSParty+LSDepartment+LSParty +" "
	 "order by company,cost,chalt"
	 
	 )
	
	stmt = con.db.prepare(con.conn, sql)
	stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
	etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
	

	con.db.execute(stmt)
	result = con.db.fetch_both(stmt)
	print(result)
	abc=[]
	while result != False:
		global counter
		counter = counter + 1
		pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
		pdfrpt.d = pdfrpt.dvalue()
		abc.append(result)
		result = con.db.fetch_both(stmt)
	print(abc)	

	if pdfrpt.d < 20:
		pdfrpt.d = 740
		pdfrpt.c.showPage()
		pdfrpt.header(stdt, etdt, pdfrpt.divisioncode)

		
	
	if result == False:
		global Exceptions
	if counter>0:
		pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
		pdfrpt.fonts(7)
		pdfrpt.c.drawString(10, pdfrpt.d, str(pdfrpt.divisioncode[-2]) + " TOTAL : ")
		# pdfrpt.c.drawAlignedString(570, pdfrpt.d, str("%.2f" % float(pdfrpt.CompanyAmountTotal)))
		pdfrpt.companyclean()
		views.Exceptions = ""
	elif counter == 0:
		views.Exceptions = "Note: Please Select Valid Credentials"
		return
	
	pdfrpt.c.setPageSize(pdfrpt.landscape(pdfrpt.A3))
	pdfrpt.c.showPage()
	pdfrpt.c.save()





def ExciseRegister_InovNoWise_PrintPDF(LSCompany,LSChallanType,LSParty,LSCharges,LSAllCompanies,LSAllChallanTypes,
        LSAllParties,LSAllCharges,LSDepartment,LSItemType,LSChallanCategory,LSAllDepartments,LSAllItemTypes,LSAllChallanCategories,LDStartDate,
        LDEndDate,LSLotType):
	if not LSAllCompanies and not LSCompany or LSAllCompanies:
		LSCompany = ""
	elif LSCompany:
		LSCompany = " And Plant.Code in ("+str(LSCompany)[1:-1]+")"

	if not LSAllChallanTypes and not LSChallanType or LSAllChallanTypes:
		LSChallanType = ""
	elif LSChallanType:
		LSChallanType = " And pi.TAXTEMPLATECODE in ("+str(LSChallanType)[1:-1]+")"
	
	if not LSAllParties and not LSParty or LSAllParties:
		LSParty = ""
	elif LSParty:
		LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

	if not LSAllCharges and not LSCharges or LSAllCharges:
		LSCharges = ""
	elif LSCharges:
		LSCharges = " And Itax.Code in ("+str(LSCharges)[1:-1]+")"

	if not LSAllDepartments and not LSDepartment or LSAllDepartments:
		LSDepartment = ""
	elif LSDepartment:
		LSDepartment = " And Costcenter.Code in ("+str(LSDepartment)[1:-1]+")"

	if not LSAllItemTypes and not LSItemType or LSAllItemTypes:
		LSItemType = ""
	elif LSItemType:
		LSItemType = " And Itemtype.Code in ("+str(LSItemType)[1:-1]+")"

	if not LSAllChallanCategories and not LSChallanCategory or LSAllChallanCategories:
		LSChallanCategory = ""
	elif LSChallanCategory:
		LSChallanCategory = " And pi.TAXTEMPLATECODE in ("+str(LSChallanCategory)[1:-1]+")"

	print(LSCompany,LSChallanCategory,LSChallanType,LSCharges,LSParty,LSItemType,LSDepartment)
	sql=("Select  plant.longdescription as company "
                " ,SDL.PREVIOUSCODE as challanno "
	         " ,PI.code as invno "
	         " ,PI.INVOICEDATE as invdate "
	         " ,PI.TOTALQUANTITY as qty "
	         " ,PI.GROSSVALUE as invamt "
	         " ,SDL.PRICE as Rate "
	         " ,BP.Legalname1 as Party "
	         " ,IGST.CALCULATEDVALUE as IGST "
	         " ,CGST.CALCULATEDVALUE as CGST "
	         " ,UTGST.CALCULATEDVALUE as UTGST "
	         " ,BC.CALCULATEDVALUE as OTHCH "
	         " ,DR.CALCULATEDVALUE as GST "
	         " ,FRT.CALCULATEDVALUE as FRT "
	         " ,IC.CALCULATEDVALUE as INS "
	         " ,TCS.CALCULATEDVALUE as TCS "
 	 " from PlantInvoice PI "
 	 " Join Plant   ON PI.FactoryCode = Plant.code "
	 " Join SalesDocument SD           ON    PI.CODE = SD.PROVISIONALCODE "
	                                 " And SD.DOCUMENTTYPETYPE = '06' "
	 " JOIN SalesDocumentLine SDL      ON SD.PROVISIONALCODE=SDL.SALESDOCUMENTPROVISIONALCODE "
	                                 " AND  SD.PROVISIONALCOUNTERCODE=SDL.SALDOCPROVISIONALCOUNTERCODE "
	 " Join OrderPartner As OP         on SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode "
	                                " And OP.CustomerSupplierType = 1 "
	 " Join BusinessPartner BP ON OP.OrderBusinessPartnerNumberId = BP.NumberId "
	 " join LOGICALWAREHOUSE               On      plant.CODE  =      LOGICALWAREHOUSE.PlantCode  "
	 " Join PLANTINVOICELINE PIL               ON      PI.CODE = PIL.PLANTINVOICECODE  "
         " Left Join    COSTCENTER             On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE  "
	 " Left JOIN IndTaxDETAIL IGST              ON      PI.AbsUniqueId = IGST.ABSUNIQUEID    "
	 " AND     IGST.ITaxCode in('IG3','IG1','IG0','12G','IG2','IG8','IGS') "
	 " Left JOIN IndTaxDETAIL CGST              ON      PI.AbsUniqueId = CGST.ABSUNIQUEID    "
	 " AND     CGST.ITaxCode in('GCS','S14','CG3','CG2','CG6','SG6','CG1','CG9') "
	 " Left JOIN IndTaxDETAIL UTGST              ON      PI.AbsUniqueId = UTGST.ABSUNIQUEID    "
	 " AND     UTGST.ITaxCode in('SCG','T14','UG3','TG6','UG2','UG6','UC9','UG1') "
	 " Left Join IndTaxDETAIL    FRT                   ON      PI.AbsUniqueId = FRT.ABSUNIQUEID    "
	 " AND     FRT.ITaxCode = 'GFR'    "
	 " Left Join IndTaxDETAIL       IC                ON      PI.AbsUniqueId = IC.ABSUNIQUEID    "
	 " AND     IC.ITaxCode = 'GIN'    "
	 " Left Join IndTaxDETAIL    BC                   ON      PI.AbsUniqueId = BC.ABSUNIQUEID    "
	 " AND     BC.ITAXCODE = 'ROF'    "
	 " Left Join IndTaxDETAIL    DR                   ON      PI.AbsUniqueId = DR.ABSUNIQUEID    "
	 " AND     DR.TAXCATEGORYCODE = 'GST'   "
	 " Left Join IndTaxDETAIL    TCS                   ON      PI.AbsUniqueId = TCS.ABSUNIQUEID    "
	 " AND     TCS.TAXCATEGORYCODE = 'TCS'   "
	 " Left Join Itax on pi.ABSUNIQUEID = Itax.ABSUNIQUEID "
	 " where pi.invoicedate between "+str(LDStartDate)+" and "+str(LDEndDate)+" "+LSChallanCategory+LSChallanType+LSCharges+LSCompany+LSParty+LSDepartment+LSParty +" "
	 
	 
	 )
	
	stmt = con.db.prepare(con.conn, sql)
	stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
	etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
	

	con.db.execute(stmt)
	result = con.db.fetch_both(stmt)
	while result != False:
		global counter
		counter = counter + 1
		pdfrpt1.textsize(pdfrpt1.c, result, pdfrpt1.d, stdt, etdt)
		pdfrpt1.d = pdfrpt1.dvalue()
		result = con.db.fetch_both(stmt)

	if pdfrpt1.d < 20:
		pdfrpt1.d = 730
		pdfrpt1.c.showPage()
		pdfrpt1.header(stdt, etdt, pdfrpt1.divisioncode)

	if result == False:
		global Exceptions
	if counter>0:
		pdfrpt1.d = pdfrpt1.dlocvalue(pdfrpt1.d)
		pdfrpt1.fonts(7)
		pdfrpt1.c.drawString(10, pdfrpt1.d, str(pdfrpt1.divisioncode[-2]) + " TOTAL : ")
		pdfrpt1.c.drawAlignedString(570, pdfrpt1.d, str("%.2f" % float(pdfrpt1.CompanyAmountTotal)))
		pdfrpt1.companyclean()
		views.Exceptions = ""
	elif counter == 0:
		views.Exceptions = "Note: Please Select Valid Credentials"
		return
	
	pdfrpt1.c.setPageSize(pdfrpt1.landscape(pdfrpt1.A4))
	pdfrpt1.c.showPage()
	pdfrpt1.c.save()
        

def ExciseRegister_ChallanTypeWiseItemShade_PrintPDF(LSCompany,LSChallanType,LSParty,LSCharges,LSAllCompanies,LSAllChallanTypes,
        LSAllParties,LSAllCharges,LSDepartment,LSItemType,LSChallanCategory,LSAllDepartments,LSAllItemTypes,LSAllChallanCategories,LDStartDate,
        LDEndDate,LSLotType):
	if not LSAllCompanies and not LSCompany or LSAllCompanies:
		LSCompany = ""
	elif LSCompany:
		LSCompany = " And Plant.Code in ("+str(LSCompany)[1:-1]+")"

	if not LSAllChallanTypes and not LSChallanType or LSAllChallanTypes:
		LSChallanType = ""
	elif LSChallanType:
		LSChallanType = " And pi.TAXTEMPLATECODE in ("+str(LSChallanType)[1:-1]+")"
	
	if not LSAllParties and not LSParty or LSAllParties:
		LSParty = ""
	elif LSParty:
		LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

	if not LSAllCharges and not LSCharges or LSAllCharges:
		LSCharges = ""
	elif LSCharges:
		LSCharges = " And Itax.Code in ("+str(LSCharges)[1:-1]+")"

	if not LSAllDepartments and not LSDepartment or LSAllDepartments:
		LSDepartment = ""
	elif LSDepartment:
		LSDepartment = " And Costcenter.Code in ("+str(LSDepartment)[1:-1]+")"

	if not LSAllItemTypes and not LSItemType or LSAllItemTypes:
		LSItemType = ""
	elif LSItemType:
		LSItemType = " And Itemtype.Code in ("+str(LSItemType)[1:-1]+")"

	if not LSAllChallanCategories and not LSChallanCategory or LSAllChallanCategories:
		LSChallanCategory = ""
	elif LSChallanCategory:
		LSChallanCategory = " And pi.TAXTEMPLATECODE in ("+str(LSChallanCategory)[1:-1]+")"

	print(LSCompany,LSChallanCategory,LSChallanType,LSCharges,LSParty,LSItemType,LSDepartment)
	sql=("Select  plant.longdescription as company "
                " ,SDL.PREVIOUSCODE as challanno "
	         " ,PI.code as invno "
	         " ,PI.INVOICEDATE as invdate "
	         " ,PI.TOTALQUANTITY as qty "
	         " ,PI.GROSSVALUE as invamt "
	         " ,SDL.PRICE as Rate "
	         " ,BP.Legalname1 as Party "
	         " ,IGST.CALCULATEDVALUE as IGST "
	         " ,CGST.CALCULATEDVALUE as CGST "
	         " ,UTGST.CALCULATEDVALUE as UTGST "
	         " ,BC.CALCULATEDVALUE as OTHCH "
	         " ,DR.CALCULATEDVALUE as GST "
	         " ,FRT.CALCULATEDVALUE as FRT "
	         " ,IC.CALCULATEDVALUE as INS "
	         " ,TCS.CALCULATEDVALUE as TCS "
 	 " from PlantInvoice PI "
 	 " Join Plant   ON PI.FactoryCode = Plant.code "
	 " Join SalesDocument SD           ON    PI.CODE = SD.PROVISIONALCODE "
	                                 " And SD.DOCUMENTTYPETYPE = '06' "
	 " JOIN SalesDocumentLine SDL      ON SD.PROVISIONALCODE=SDL.SALESDOCUMENTPROVISIONALCODE "
	                                 " AND  SD.PROVISIONALCOUNTERCODE=SDL.SALDOCPROVISIONALCOUNTERCODE "
	 " Join OrderPartner As OP         on SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode "
	                                " And OP.CustomerSupplierType = 1 "
	 " Join BusinessPartner BP ON OP.OrderBusinessPartnerNumberId = BP.NumberId "
	 " join LOGICALWAREHOUSE               On      plant.CODE  =      LOGICALWAREHOUSE.PlantCode  "
	 " Join PLANTINVOICELINE PIL               ON      PI.CODE = PIL.PLANTINVOICECODE  "
         " Left Join    COSTCENTER             On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE  "
	 " Left JOIN IndTaxDETAIL IGST              ON      PI.AbsUniqueId = IGST.ABSUNIQUEID    "
	 " AND     IGST.ITaxCode in('IG3','IG1','IG0','12G','IG2','IG8','IGS') "
	 " Left JOIN IndTaxDETAIL CGST              ON      PI.AbsUniqueId = CGST.ABSUNIQUEID    "
	 " AND     CGST.ITaxCode in('GCS','S14','CG3','CG2','CG6','SG6','CG1','CG9') "
	 " Left JOIN IndTaxDETAIL UTGST              ON      PI.AbsUniqueId = UTGST.ABSUNIQUEID    "
	 " AND     UTGST.ITaxCode in('SCG','T14','UG3','TG6','UG2','UG6','UC9','UG1') "
	 " Left Join IndTaxDETAIL    FRT                   ON      PI.AbsUniqueId = FRT.ABSUNIQUEID    "
	 " AND     FRT.ITaxCode = 'GFR'    "
	 " Left Join IndTaxDETAIL       IC                ON      PI.AbsUniqueId = IC.ABSUNIQUEID    "
	 " AND     IC.ITaxCode = 'GIN'    "
	 " Left Join IndTaxDETAIL    BC                   ON      PI.AbsUniqueId = BC.ABSUNIQUEID    "
	 " AND     BC.ITAXCODE = 'ROF'    "
	 " Left Join IndTaxDETAIL    DR                   ON      PI.AbsUniqueId = DR.ABSUNIQUEID    "
	 " AND     DR.TAXCATEGORYCODE = 'GST'   "
	 " Left Join IndTaxDETAIL    TCS                   ON      PI.AbsUniqueId = TCS.ABSUNIQUEID    "
	 " AND     TCS.TAXCATEGORYCODE = 'TCS'   "
	 " Left Join Itax on pi.ABSUNIQUEID = Itax.ABSUNIQUEID "
	 " where pi.invoicedate between "+str(LDStartDate)+" and "+str(LDEndDate)+" "+LSChallanCategory+LSChallanType+LSCharges+LSCompany+LSParty+LSDepartment+LSParty +" "
	 
	 
	 )
	
	stmt = con.db.prepare(con.conn, sql)
	stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
	etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
	

	con.db.execute(stmt)
	result = con.db.fetch_both(stmt)
	while result != False:
		global counter
		counter = counter + 1
		pdfrpt2.textsize(pdfrpt2.c, result, pdfrpt2.d, stdt, etdt)
		pdfrpt2.d = pdfrpt2.dvalue()
		result = con.db.fetch_both(stmt)

	if pdfrpt2.d < 20:
		pdfrpt2.d = 730
		pdfrpt2.c.showPage()
		pdfrpt2.header(stdt, etdt, pdfrpt2.divisioncode)

	if result == False:
		global Exceptions
	if counter>0:
		pdfrpt2.d = pdfrpt2.dlocvalue(pdfrpt2.d)
		pdfrpt2.fonts(7)
		pdfrpt2.c.drawString(10, pdfrpt2.d, str(pdfrpt2.divisioncode[-2]) + " TOTAL : ")
		pdfrpt2.c.drawAlignedString(570, pdfrpt2.d, str("%.2f" % float(pdfrpt2.CompanyAmountTotal)))
		pdfrpt2.companyclean()
		views.Exceptions = ""
	elif counter == 0:
		views.Exceptions = "Note: Please Select Valid Credentials"
		return
	
	pdfrpt2.c.setPageSize(pdfrpt2.landscape(pdfrpt2.A4))
	pdfrpt2.c.showPage()
	pdfrpt2.c.save()
       
def ExciseRegister_ChallanTypeWise_PrintPDF(LSCompany,LSChallanType,LSParty,LSCharges,LSAllCompanies,LSAllChallanTypes,
        LSAllParties,LSAllCharges,LSDepartment,LSItemType,LSChallanCategory,LSAllDepartments,LSAllItemTypes,LSAllChallanCategories,LDStartDate,
        LDEndDate,LSLotType):
	if not LSAllCompanies and not LSCompany or LSAllCompanies:
		LSCompany = ""
	elif LSCompany:
		LSCompany = " And Plant.Code in ("+str(LSCompany)[1:-1]+")"

	if not LSAllChallanTypes and not LSChallanType or LSAllChallanTypes:
		LSChallanType = ""
	elif LSChallanType:
		LSChallanType = " And pi.TAXTEMPLATECODE in ("+str(LSChallanType)[1:-1]+")"
	
	if not LSAllParties and not LSParty or LSAllParties:
		LSParty = ""
	elif LSParty:
		LSParty = " And BP.NUMBERID in ("+str(LSParty)[1:-1]+")"

	if not LSAllCharges and not LSCharges or LSAllCharges:
		LSCharges = ""
	elif LSCharges:
		LSCharges = " And Itax.Code in ("+str(LSCharges)[1:-1]+")"

	if not LSAllDepartments and not LSDepartment or LSAllDepartments:
		LSDepartment = ""
	elif LSDepartment:
		LSDepartment = " And Costcenter.Code in ("+str(LSDepartment)[1:-1]+")"

	if not LSAllItemTypes and not LSItemType or LSAllItemTypes:
		LSItemType = ""
	elif LSItemType:
		LSItemType = " And Itemtype.Code in ("+str(LSItemType)[1:-1]+")"

	if not LSAllChallanCategories and not LSChallanCategory or LSAllChallanCategories:
		LSChallanCategory = ""
	elif LSChallanCategory:
		LSChallanCategory = " And pi.TAXTEMPLATECODE in ("+str(LSChallanCategory)[1:-1]+")"

	print(LSCompany,LSChallanCategory,LSChallanType,LSCharges,LSParty,LSItemType,LSDepartment)
	sql=("Select  plant.longdescription as company "
                " ,SDL.PREVIOUSCODE as challanno "
	         " ,PI.code as invno "
	         " ,PI.INVOICEDATE as invdate "
	         " ,PI.TOTALQUANTITY as qty "
	         " ,PI.GROSSVALUE as invamt "
	         " ,SDL.PRICE as Rate "
	         " ,BP.Legalname1 as Party "
	         " ,IGST.CALCULATEDVALUE as IGST "
	         " ,CGST.CALCULATEDVALUE as CGST "
	         " ,UTGST.CALCULATEDVALUE as UTGST "
	         " ,BC.CALCULATEDVALUE as OTHCH "
	         " ,DR.CALCULATEDVALUE as GST "
	         " ,FRT.CALCULATEDVALUE as FRT "
	         " ,IC.CALCULATEDVALUE as INS "
	         " ,TCS.CALCULATEDVALUE as TCS "
 	 " from PlantInvoice PI "
 	 " Join Plant   ON PI.FactoryCode = Plant.code "
	 " Join SalesDocument SD           ON    PI.CODE = SD.PROVISIONALCODE "
	                                 " And SD.DOCUMENTTYPETYPE = '06' "
	 " JOIN SalesDocumentLine SDL      ON SD.PROVISIONALCODE=SDL.SALESDOCUMENTPROVISIONALCODE "
	                                 " AND  SD.PROVISIONALCOUNTERCODE=SDL.SALDOCPROVISIONALCOUNTERCODE "
	 " Join OrderPartner As OP         on SD.OrdPrnCustomerSupplierCode = OP.CustomerSupplierCode "
	                                " And OP.CustomerSupplierType = 1 "
	 " Join BusinessPartner BP ON OP.OrderBusinessPartnerNumberId = BP.NumberId "
	 " join LOGICALWAREHOUSE               On      plant.CODE  =      LOGICALWAREHOUSE.PlantCode  "
	 " Join PLANTINVOICELINE PIL               ON      PI.CODE = PIL.PLANTINVOICECODE  "
         " Left Join    COSTCENTER             On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE  "
	 " Left JOIN IndTaxDETAIL IGST              ON      PI.AbsUniqueId = IGST.ABSUNIQUEID    "
	 " AND     IGST.ITaxCode in('IG3','IG1','IG0','12G','IG2','IG8','IGS') "
	 " Left JOIN IndTaxDETAIL CGST              ON      PI.AbsUniqueId = CGST.ABSUNIQUEID    "
	 " AND     CGST.ITaxCode in('GCS','S14','CG3','CG2','CG6','SG6','CG1','CG9') "
	 " Left JOIN IndTaxDETAIL UTGST              ON      PI.AbsUniqueId = UTGST.ABSUNIQUEID    "
	 " AND     UTGST.ITaxCode in('SCG','T14','UG3','TG6','UG2','UG6','UC9','UG1') "
	 " Left Join IndTaxDETAIL    FRT                   ON      PI.AbsUniqueId = FRT.ABSUNIQUEID    "
	 " AND     FRT.ITaxCode = 'GFR'    "
	 " Left Join IndTaxDETAIL       IC                ON      PI.AbsUniqueId = IC.ABSUNIQUEID    "
	 " AND     IC.ITaxCode = 'GIN'    "
	 " Left Join IndTaxDETAIL    BC                   ON      PI.AbsUniqueId = BC.ABSUNIQUEID    "
	 " AND     BC.ITAXCODE = 'ROF'    "
	 " Left Join IndTaxDETAIL    DR                   ON      PI.AbsUniqueId = DR.ABSUNIQUEID    "
	 " AND     DR.TAXCATEGORYCODE = 'GST'   "
	 " Left Join IndTaxDETAIL    TCS                   ON      PI.AbsUniqueId = TCS.ABSUNIQUEID    "
	 " AND     TCS.TAXCATEGORYCODE = 'TCS'   "
	 " Left Join Itax on pi.ABSUNIQUEID = Itax.ABSUNIQUEID "
	 " where pi.invoicedate between "+str(LDStartDate)+" and "+str(LDEndDate)+" "+LSChallanCategory+LSChallanType+LSCharges+LSCompany+LSParty+LSDepartment+LSParty +" "
	 
	 
	 )
	
	stmt = con.db.prepare(con.conn, sql)
	stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
	etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
	

	con.db.execute(stmt)
	result = con.db.fetch_both(stmt)
	while result != False:
		global counter
		counter = counter + 1
		pdfrpt3.textsize(pdfrpt3.c, result, pdfrpt3.d, stdt, etdt)
		pdfrpt3.d = pdfrpt3.dvalue()
		result = con.db.fetch_both(stmt)

	if pdfrpt3.d < 20:
		pdfrpt3.d = 730
		pdfrpt3.c.showPage()
		pdfrpt3.header(stdt, etdt, pdfrpt3.divisioncode)

	if result == False:
		global Exceptions
	if counter>0:
		pdfrpt3.d = pdfrpt3.dlocvalue(pdfrpt3.d)
		pdfrpt3.fonts(7)
		pdfrpt3.c.drawString(10, pdfrpt3.d, str(pdfrpt3.divisioncode[-2]) + " TOTAL : ")
		pdfrpt3.c.drawAlignedString(570, pdfrpt3.d, str("%.2f" % float(pdfrpt3.CompanyAmountTotal)))
		pdfrpt3.companyclean()
		views.Exceptions = ""
	elif counter == 0:
		views.Exceptions = "Note: Please Select Valid Credentials"
		return
	
	pdfrpt3.c.setPageSize(pdfrpt3.landscape(pdfrpt3.A4))
	pdfrpt3.c.showPage()
	pdfrpt3.c.save()
        



    