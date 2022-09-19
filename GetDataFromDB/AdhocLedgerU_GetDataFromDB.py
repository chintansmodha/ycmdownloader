from Global_Files import Connection_String as con
from cgitb import reset
from unittest import result
from PrintPDF import AdhocLedgerU_PrintPDF as pdfrpt
def adhocLedgerU_GerData(Year,startdate,enddate,LSCompany,LCCompany,LSParty,LCParty,LSAccount,LCAccount,Narration,Eject):
    cumamt=0
    if not LCCompany and not LSCompany or LCCompany:
        LSCompany = " "
    elif LSCompany:
        LSCompany = "AND FINBUSINESSUNIT.CODE in (" + str(LSCompany)[1:-1] + ")"

    if not LCParty and not LSParty or LCParty:
        LSParty = " "
    elif LSParty:
        LSParty = "AND BUSINESSPARTNER.NUMBERID in (" + str(LSParty)[1:-1] + ")"

    if not LCAccount and not LSAccount or LCAccount:
        LSAccount = " "
    elif LSParty:
        LSAccount = "AND GLMASTER.CODE in (" + str(LSAccount)[1:-1] + ")"

    sql =" Select  Company.LongDescription as DIVCODE"\
        " ,FOD.Code as vchno"\
        " ,FOD.PostingDate as vchdate"\
        " ,FOD.DOCUMENTTYPECODE as txn"\
        " ,COALESCE(FD.CHEQUENUMBER,CHQN.Valuestring,'') As ChqNo"\
        " ,cast(COALESCE(case when FOD.CREDITLINE='1' then FOD.AMOUNTINCC End,0)as decimal(18,2)) as credit"\
        " ,cast(COALESCE(case when FOD.CREDITLINE='0' then FOD.AMOUNTINCC End,0)as decimal(18,2)) as debit"\
        ", COALESCE(nt.NOTE,'') as remarks"\
        " from FinOpenDocuments FOD "\
        " JOIN FinDocument FD            on FOD.BUSINESSUNITCODE=FD.BUSINESSUNITCODE  "\
                                        "And  FOD.FINANCIALYEARCODE=FD.FINANCIALYEARCODE "\
                                        "And FOD.DOCUMENTTEMPLATECODE = FD.DOCUMENTTEMPLATECODE  "\
                                        "And FOD.CODE = FD.CODE "\
        " JOIN FinBusinessUnit  unit        ON FOD.BUSINESSUNITCODE = Unit.Code"\
        " JOin FinBusinessUnit Company    ON    unit.GROUPBUCODE = Company.Code"\
        " JOIN    GLMASTER                ON      FOD.GLCODE = GLMASTER.CODE"\
        " Left join orderpartner on  FOD.ORDERPARTNERTYPE =orderpartner.CUSTOMERSUPPLIERTYPE "\
                                        " AND FOD.ORDERPARTNERCODE = orderpartner.CUSTOMERSUPPLIERCODE "\
        " Left join businesspartner on ORDERPARTNER.ORDERBUSINESSPARTNERNUMBERID = BUSINESSPARTNER.NUMBERID "\
        " LEFT JOIN AdStorage AS CHQN               ON  FOD.AbsUniqueId = CHQN.UniqueId"\
                " AND CHQN.NameEntityName = 'FINDocument' "\
                " And CHQN.NameName = 'CustomerCheque' "\
                "  And CHQN.FieldName = 'CustomerCheque' "\
        " Left Join Note as nt    on      FD.absuniqueid = nt.fatherid"\
        " Where FOD.PostingDate between '"+startdate+"' and '"+enddate+"'"+LSCompany+LSParty+LSAccount+""\
            " order by divcode,vchdate,vchno,txn,chqno"

    
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    while result != False:
        cumamt=cumamt + float(result['DEBIT'])-float(result['CREDIT'])
        result['CUMAMT'] = cumamt
        pdfrpt.textsize(pdfrpt.c,result,pdfrpt.d,startdate,enddate)
        result = con.db.fetch_both(stmt)
    pdfrpt.c.showPage()
    pdfrpt.c.save()

    pdfrpt.newrequest()
    pdfrpt.d = pdfrpt.newpage()