from django.http import HttpResponse
from django.shortcuts import render
from django.views.static import serve

from FormLoad import Diposite_Transaction_FormLoad as views
from PrintPDF import Diposite_Transaction_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
import os
from datetime import datetime
from ProcessSelection import PackingRegister_ProcessSelection as PRV


def AgentWise_Transation(LSallbroker, LSallcompany, LSselbroker, LSselcompany, LDStartDate, LDEndDate, request,LSReporttype):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]

    if LSReporttype=='0':
        sql = "SELECT " \
              "         COALESCE(AGENT.Longdescription,' Agent Not Defined in Fin Document')  AS AGENTNAME " \
              "        , Sum(CAST(FINDOC.DOCUMENTAMOUNT AS DECIMAL(20,2)))         AS AMOUNT " \
              "FROM FINDOCUMENT FINDOC " \
              "LEFT JOIN AGENT                 ON FINDOC.AGENT1CODE    = AGENT.CODE " \
              "JOIN FinBusinessUnit BUnit      ON FINDOC.BusinessUnitCODE  = Bunit.CODE " \
              "								   And BUnit.GroupFlag = 0 " \
              "JOIN FinBusinessUnit As Company ON Bunit.GroupBUCode = Company.Code  " \
              "								   And Company.GroupFlag = 1 " \
              "WHERE FINDOC.DOCUMENTTYPECODE IN('BR','CR') " \
              "AND FINDOC.CURRENTSTATUS = 1 " \
              "AND FINDOC.FINANCEDOCUMENTDATE BETWEEN '"+LDStartDate+"' AND '"+LDEndDate+"' " \
              "AND FINDOC.DOCUMENTTEMPLATECODE In ('B12','B18') " \
              "Group By   COALESCE(AGENT.Longdescription,' Agent Not Defined in Fin Document') " \
              "Order by  AgentName"
    elif LSReporttype=='1':
        sql = "SELECT Company.LONGDESCRIPTION           AS COMPANYNAME " \
              "       , COALESCE(AGENT.Longdescription,' Agent Not Defined in Fin Document')         as AGENTNAME " \
              "       , Sum(CAST(FINDOC.DOCUMENTAMOUNT AS DECIMAL(20,2)))         AS AMOUNT " \
              "FROM FINDOCUMENT FINDOC " \
              "LEFT JOIN AGENT                 ON      FINDOC.AGENT1CODE    = AGENT.CODE " \
              "JOIN FinBusinessUnit BUnit      ON      FINDOC.BusinessUnitCODE  = Bunit.CODE And BUnit.GroupFlag = 0 " \
              "JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode = Company.Code And Company.GroupFlag = 1 " \
              "WHERE FINDOC.DOCUMENTTYPECODE IN('BR','CR') " \
              "AND FINDOC.CURRENTSTATUS = 1 " \
              "AND FINDOC.FINANCEDOCUMENTDATE BETWEEN '"+LDStartDate+"' AND '"+LDEndDate+"' " \
              "AND FINDOC.DOCUMENTTEMPLATECODE In ('B12','B18') " \
              "Group By Company.LONGDESCRIPTION,  COALESCE(AGENT.Longdescription, ' Agent Not Defined in Fin Document') " \
              "Order by  Company.LONGDESCRIPTION, AgentName "

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
            if LSReporttype == '0':
                pdfrpt.textsizeYes(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
            elif LSReporttype=='1':
                pdfrpt.textsizeNo(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
            # pdfrpt.d=pdfrpt.dvalue()
            result = con.db.fetch_both(stmt)
            counter = counter + 1
            if pdfrpt.d < 20:
                pdfrpt.d = 765
                pdfrpt.c.showPage()
                pdfrpt.header("stdt", "etdt", pdfrpt.divisioncode)
        pdfrpt.d=pdfrpt.dvalue()
        if LSReporttype=='0':
            pdfrpt.printotalconsolidation()
        else:
            pdfrpt.printtotalnoconsolidation()

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
