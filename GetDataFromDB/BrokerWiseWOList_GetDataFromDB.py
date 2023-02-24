from datetime import datetime
from Global_Files import Connection_String as con
from FormLoad import BrokerWiseWOList_FormLoad as views
from PrintPDF import BrokerWiseWOList_PrintPDF as pdfrpt

def BrokerWiseWOList_GetData(LSCompany,LSAllCompanies,LSBrokerGroup,LSAllBrokerGroup,LDEndDate,LDStartDate):
    if not LSAllCompanies and not LSCompany or LSAllCompanies:
        LSCompany = ""
    elif LSCompany:
        LSCompany = " And UNIT.Code in ("+str(LSCompany)[1:-1]+")"
    if not LSAllBrokerGroup and not LSBrokerGroup or LSAllBrokerGroup:
        LSBrokerGroup = ""
    elif LSBrokerGroup:
        LSBrokerGroup = " And AgGrp.code in ("+str(LSBrokerGroup)[1:-1]+")"
    
    sql=("Select  COALESCE(FDORI.INVOICENO,'') as Breakup "
        " ,FDORI.PostingDate as issdate "
        " ,cast(sum(FDDEST.DOCUMENTAMOUNT) as decimal(18,2)) as chqamt "
        " ,COALESCE(FDDEST.CHEQUENUMBER,'') as chqno "
        " ,cast(sum(FODT.CLEAREDAMOUNT) as decimal(18,2)) as adjamt "
        " ,FODT.TRANSACTIONDATE as vchdate "
        " ,UNIT.Longdescription as company "
        " ,AgGrp.LONGDESCRIPTION as agentGroup "
        " ,Agent.LONGDESCRIPTION as agent "
        " from FinOpenDocumentsTransactions as FODT "
" Join Findocument as FDDEST      On FDDEST.CODE = FODT.DESTCODE "
                                " And FDDEST.DOCUMENTTEMPLATECODE = FODT.DESTDOCUMENTTEMPLATECODE "
                                " And FDDEST.FINANCIALYEARCODE = FODT.DESTFINANCIALYEARCODE "
                                " And FDDEST.BUSINESSUNITCODE = FODT.DESTBUSINESSUNITCODE "
" Join Findocument as FDORI       On FODT.ORIGINCODE = FDORI.CODE "
                                " And FODT.ORIGINDOCUMENTTEMPLATECODE = FDORI.DOCUMENTTEMPLATECODE "
                                " And FODT.ORIGINFINANCIALYEARCODE = FDORI.FINANCIALYEARCODE "
                                " And FODT.ORIGINBUSINESSUNITCODE = FDORI.BUSINESSUNITCODE  "
" JOIN FINBUSINESSUNIT UNIT       ON      FDDEST.BUSINESSUNITCODE=UNIT.CODE "
" JOIN    AgentsGroupDetail AGD    On      FDDEST.Agent1Code = AGD.AgentCode "
" JOIN    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code "
" Join    Agent                   On      AGD.AGENTCODE = Agent.code "
" Where FODT.TRANSACTIONDATE between '"+LDStartDate+"' and '"+LDEndDate+"'"+LSCompany+LSBrokerGroup+""
" Group by  UNIT.Longdescription,AgGrp.LONGDESCRIPTION,Agent.LONGDESCRIPTION,FODT.TRANSACTIONDATE,FDDEST.CHEQUENUMBER,FDORI.PostingDate,FDORI.INVOICENO"
" Order by company,agentGroup,agent")

    print(sql)
    stmt = con.db.prepare(con.conn, sql)
    stdt = datetime.strptime(LDStartDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        pdfrpt.textsize(pdfrpt.c,result, pdfrpt.d, stdt, etdt)
        pdfrpt.d = pdfrpt.dvalue(stdt, etdt, pdfrpt.transporter)
        result = con.db.fetch_both(stmt)  
    if pdfrpt.d < 20:
        pdfrpt.d = 740
        pdfrpt.c.showPage()
        pdfrpt.header(stdt, etdt, pdfrpt.transporter)
    if result == False:
        pdfrpt.boldfonts(8)
        pdfrpt.d = pdfrpt.dlocvalue(pdfrpt.d)
        pdfrpt.partytotalprint(pdfrpt.d, stdt, etdt)
        pdfrpt.companyclean()

    pdfrpt.c.setPageSize(pdfrpt.A4)
    pdfrpt.c.showPage()
    pdfrpt.c.save()
