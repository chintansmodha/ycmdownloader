from django.http import HttpResponse
from django.shortcuts import render
from django.views.static import serve

from FormLoad import Diposite_Transaction_Bank_Company_Collection_FormLoad as views
from PrintPDF import Diposite_Transaction_Bank_Company_Collection_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
import os
from datetime import datetime
from ProcessSelection import DepositeTransaction_BankWise_Company_Collection_ProcessSelection as PRV


def BankWise_Transation(sqlwhere,LDStartDate,LDEndDate,request):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]

    LDStartDate=str(LDStartDate)
    LDEndDate=str(LDEndDate)
    sql = " Select  Company.LongDescription                          As BUSINESSUNITName " \
          ",BankMaster.LongDescription                                   As BankName " \
          ",ADS_SLipNo.ValueString                                       AS VOUCHERNUMBER " \
          ",VARCHAR_FORMAT(FinDocument.FinanceDocumentDate,'DD/MM/YYYY') AS VOUCHERDATE " \
          ",Sum(CAST(FinDocument.DOCUMENTAMOUNT AS DECIMAL(20,2)))       AS AMOUNT " \
          ",count(FinDocument.Code)                            			 AS CHEQUE " \
          "From    FinDocument " \
          "Join    FinBusinessUnit         On      FinDocument.BUSINESSUNITCODE 	= FinBusinessUnit.CODE  " \
          "Join    FinBusinessUnit As Company On 	FinBusinessUnit.GroupbuCode 	= Company.Code " \
          "JoiN    GLMaster As BankMaster  On      	FinDocument.GLCODE 				= BankMaster.Code  " \
          "left JOIN    AdStorage ADS_SlipNo    ON  		FinDocument.AbsUniqueId 		= ADS_SlipNo.UniqueId " \
          "                                AND   	ADS_SlipNo.NameEntityNAme 		='FINDocument'  " \
          "								   And      ADS_SlipNo.FieldName 			= 'IssuesSlipNO' " \
          "JOIN    AdStorage ADS_IssSlipStatus    ON  FinDocument.AbsUniqueId 		= ADS_IssSlipStatus.UniqueId " \
          "                                AND 		ADS_IssSlipStatus.NameEntityNAme ='FINDocument' " \
          "                                And      ADS_IssSlipStatus.FieldName 	= 'IssueSlipStatus' " \
          "                                AND      ADS_IssSlipStatus.ValueString 	= '2' " \
          "Where   FinDocument.FinanceDocumentDate BETWEEN '"+LDStartDate+"' AND '"+LDEndDate+"' " \
          "         And     FinDocument.DocumentTypeCode In ('BR','CR') "+sqlwhere+" " \
          "Group By company.LongDescription " \
          "        , BankMaster.LongDescription " \
          "        , ADS_SLipNo.ValueString " \
          "        , FinDocument.FinanceDocumentDate " \
          "order by company.LongDescription " \
          "      , BankMaster.LongDescription "


    # print(sql)
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    # Explicitly bind parameters
    # con.db.bind_param(stmt, 1, stdt)
    # con.db.bind_param(stmt, 2, etdt)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    pdfrpt.newrequest()
    # print(result)
    global counter
    counter = 0
    if result != False:
        while result != False:
            pdfrpt.textsize(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
            # pdfrpt.d=pdfrpt.dvalue()
            result = con.db.fetch_both(stmt)
            counter = counter + 1
            if pdfrpt.d < 20:
                pdfrpt.d = 765
                pdfrpt.c.showPage()
                pdfrpt.header("stdt", "etdt", pdfrpt.divisioncode)
        pdfrpt.d=pdfrpt.dvalue()
        pdfrpt.printbanktotal()
        pdfrpt.prinCompanytotal()

        if result == False:
            if counter > 0:
                # pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
                pdfrpt.fonts(7)
                PRV.Exceptions = ""
            elif counter == 0:
                PRV.Exceptions = "Note: Please Select Valid Credentials"
                return

        pdfrpt.c.showPage()
        pdfrpt.c.save()
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()
    else:
        PRV.Exceptions = "Note: Please Select Valid Credentials"
        return
    print("*-*-*-*-*-*-*-* end *-*-*-*-*-*---*")

    # result=""
