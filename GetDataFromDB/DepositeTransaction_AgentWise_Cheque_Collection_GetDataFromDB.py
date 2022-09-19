from django.http import HttpResponse
from django.shortcuts import render
from django.views.static import serve

from FormLoad import Diposite_Transaction_AgentWise_cheque_Collection_FormLoad as views
from PrintPDF import Diposite_Transaction_Agent_Wise_Cheque_Collection_PrintPDF as pdfrpt
from Global_Files import Connection_String as con
import os
from datetime import datetime
from ProcessSelection import DepositeTransaction_AgentWise_Cheque_Collection_ProcessSelection as PRV


def AgentWise_Cheque_Collection_Transation(LSallbroker, LSallcompany, LSselbroker, LSselcompany, LDStartDate, LDEndDate, request,LSReporttype):
    LSName = datetime.now()
    LSstring = str(LSName)
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]

    print("Report type : "+LSReporttype)
    sql = "SELECT  Company.LONGDESCRIPTION                                         AS COMPANYNAME " \
          "        , COALESCE(AGENT.Longdescription,'')                            AS AGENTNAME " \
          "        , BankMaster.LongDescription                                    As BankName " \
          "        , ADS_SLipNo.ValueString                                        AS VOUCHERNUMBER " \
          "        , VARCHAR_FORMAT(FINDOC.FinanceDocumentDate,'DD/MM/YYYY')       AS VOUCHERDATE  " \
          "        , AgGrp.Longdescription                                         AS BrokerGroupName " \
          "        , agent.Longdescription                                         AS BrokerName " \
          "        , Sum(CAST(FINDOC.DOCUMENTAMOUNT AS DECIMAL(20,2)))             AS AMOUNT " \
          "FROM FINDOCUMENT FINDOC " \
          "LEFT JOIN AGENT                 ON      FINDOC.AGENT1CODE               = AGENT.CODE " \
          "Join AgentsGroupDetail AGD      On      FINDOC.Agent1Code               = AGD.AgentCode " \
          "Join AgentsGroup AgGrp          On      AGD.AgentsGroupCode             = AgGrp.Code  " \
          "JOIN FinBusinessUnit BUnit      ON      FINDOC.BusinessUnitCODE         = Bunit.CODE And BUnit.GroupFlag = 0 " \
          "JOIN FinBusinessUnit As Company ON      Bunit.GroupBUCode               = Company.Code And Company.GroupFlag = 1 " \
          "JoiN    GLMaster As BankMaster  On      FINDOC.GLCODE                   = BankMaster.Code  " \
          "JOIN    AdStorage ADS_SlipNo    ON      FINDOC.AbsUniqueId              = ADS_SlipNo.UniqueId " \
          "                                AND     ADS_SlipNo.NameEntityNAme       ='FINDocument' And ADS_SlipNo.FieldName = 'IssuesSlipNO' " \
          "JOIN    AdStorage ADS_IssSlipStatus    ON  FINDOC.AbsUniqueId           = ADS_IssSlipStatus.UniqueId " \
          "                                AND     ADS_IssSlipStatus.NameEntityNAme  ='FINDocument' " \
          "                                And     ADS_IssSlipStatus.FieldName     = 'IssueSlipStatus' " \
          "                                AND     ADS_IssSlipStatus.ValueString   = '2' " \
          "WHERE FINDOC.DOCUMENTTYPECODE IN('BR','CR') " \
          "        AND FINDOC.CURRENTSTATUS = 1 " \
          "        AND FINDOC.FINANCEDOCUMENTDATE BETWEEN '"+LDStartDate+"' AND '"+LDEndDate+"' " \
          "        AND FINDOC.DOCUMENTTEMPLATECODE In ('B12','B18') " \
          "Group By Company.LONGDESCRIPTION " \
          "        , AGENT.Longdescription " \
          "        , AgGrp.Longdescription " \
          "        , AGENT.Longdescription " \
          "        , BankMaster.LongDescription " \
          "        , ADS_SLipNo.ValueString   " \
          "        , FINDOC.FinanceDocumentDate " \
          "Order by CompanyName " \
          "        , AgentName " \
          "        , FINDOC.FinanceDocumentDate "

    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    # Explicitly bind parameters
    # con.db.bind_param(stmt, 1, stdt)
    # con.db.bind_param(stmt, 2, etdt)
    # print(sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    pdfrpt.newrequest()
    # print(result)
    global counter
    counter = 0
    if result != False:
        while result != False:
            if LSReporttype == '0':
                pdfrpt.textsizeBoth(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
            elif LSReporttype=='1':
                pdfrpt.textsizeAdjusted(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
            elif LSReporttype=='2':
                pdfrpt.textsizeUnAdjusted(pdfrpt.c, result, pdfrpt.d, stdt, etdt)
            # pdfrpt.d=pdfrpt.dvalue()
            # print(result)
            result = con.db.fetch_both(stmt)
            counter = counter + 1
            if pdfrpt.d < 20:
                pdfrpt.d = 765
                pdfrpt.c.showPage()
                pdfrpt.header("stdt", "etdt", pdfrpt.divisioncode)
        pdfrpt.d=pdfrpt.dvalue()
        pdfrpt.printotal()

        if result == False:
            if counter > 0:
                # pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
                pdfrpt.fonts(7)
                PRV.Exception = ""
            elif counter == 0:
                PRV.Exception = "Note: Please Select Valid Credentials"
                return

        pdfrpt.c.showPage()
        pdfrpt.c.save()
        pdfrpt.newrequest()
        pdfrpt.d = pdfrpt.newpage()
    else:
        PRV.Exception = "Note: Please Select Valid Credentials"
        return
    print("*-*-*-*-*-*-*-* end *-*-*-*-*-*---*")

    # result=""
