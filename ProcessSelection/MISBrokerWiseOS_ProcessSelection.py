from urllib import request
from django.shortcuts import render
from datetime import datetime
import locale

locale.setlocale(locale.LC_MONETARY, "en_IN")
from babel.numbers import format_currency
from django.shortcuts import render
from Global_Files import Connection_String as con

GDataBrokerWiseOS = []
GDataCompany = []
GDataTotal = []
GDataTotalCompany = []
GDataYear=[]
total = 0
upto15 = 0
range16 = 0
over30 = 0
dnamt = 0
advance = 0
unbilled = 0
unadj = 0
olddays = 0

TOTAL = 0

# Create your views here.
def BrokerWiseOS(request):
    b = 0
    t = 0
    u = 0
    r = 0
    o = 0
    d = 0
    un = 0
    od = 0
    una = 0

    global total
    global upto15
    global range16
    global over30
    global dnamt
    global advance
    global unbilled
    global unadj
    global olddays
    global TOTAL
    global i
    total = 0
    upto15 = 0
    range16 = 0
    over30 = 0
    dnamt = 0
    advance = 0
    unbilled = 0
    unadj = 0
    olddays = 0
    TOTAL = 0

    global GDataBrokerWiseOS
    global GDataCompany
    global GDataTotal
    global GDataYear
    GDataBrokerWiseOS = []
    GDataCompany = []
    GDataTotal = []
    GDataYear=[]
    year="2023"
    sql = "Select CODE from FINFINANCIALYEAR order by CODE desc"
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        GDataYear.append(result)
        result = con.db.fetch_both(stmt)
    sql = (
        "Select BrokerGrpOS.Company, BrokerGrpOS.BrokerGrp,BrokerGrpOS.CompanyCode,BrokerGrpOS.BrokerCode,"
"         Sum(BrokerGrpOS.Upto15) As Upto15,Sum(BrokerGrpOS.Range16) As Range16,Sum(BrokerGrpOS.Over30) As Over30"
"         , Sum(BrokerGrpOS.DNAmt) As DNAmt,Sum(BrokerGrpOS.UnBilledAmt) As UnBilledAmt,Sum(BrokerGrpOS.UnAdjusted) As UnAdjusted"
"         From ("

" Select  Company.LongDescription As Company"
"        ,AgGrp.LongDescription As BrokerGrp"
"        ,Company.Code As CompanyCode"
"        ,AgGrp.Code As BrokerCode"
"        ,cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as Upto15"
"        ,cast(0 as decimal(18,2)) as Range16"
"        ,cast(0 as decimal(18,2)) as Over30"
"        ,cast(0 as decimal(18,2)) as DNamt"
"        ,cast(0 as decimal(18,2)) as UnBilledAmt"
"        ,cast(0 as decimal(18,2)) as UnAdjusted"
" from FinOpendocuments as FOD"
"   JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"   JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"   JOIN PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                 And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                 And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                 And FOD.CODE = PI.FINDOCCODE      "
"   JOIN    AgentsGroupDetail AGD    On      PI.Agent1Code = AGD.AgentCode"
"   JOIN    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code"

" Where DocumentTypeCode in('SD')"
"                                AND FinancialYearCode ='2023'"
"                                And AmountinCC-ClearedAmount>0"
"                                AND days (current date) - days (POSTINGDATE) <=15"
" Group By Company.LongDescription,Company.Code,AgGrp.LongDescription,AgGrp.Code"

" Union All"

" Select  Company.LongDescription As Company"
"        ,AgGrp.LongDescription As BrokerGrp"
"        ,Company.Code As CompanyCode"
"        ,AgGrp.Code As BrokerCode"
"        ,cast(0 as decimal(18,2)) as Upto15"
"        ,cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as Range16"
"        ,cast(0 as decimal(18,2)) as Over30"
"        ,cast(0 as decimal(18,2)) as DNamt"
"        ,cast(0 as decimal(18,2)) as UnBilledAmt"
"        ,cast(0 as decimal(18,2)) as UnAdjusted"
" from FinOpendocuments as FOD"
"  JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"  JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"  JOIN PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                 And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                 And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                 And FOD.CODE = PI.FINDOCCODE      "
"  JOIN    AgentsGroupDetail AGD    On      PI.Agent1Code = AGD.AgentCode"
"  JOIN    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code"

" Where DocumentTypeCode in('SD')"
"                                AND FinancialYearCode ='2023'"
"                                And AmountinCC-ClearedAmount>0"
"                                AND days (current date) - days (POSTINGDATE) between 16 and 30"
" Group By Company.LongDescription,Company.Code,AgGrp.LongDescription,AgGrp.Code"

" Union All"


" Select  Company.LongDescription As Company"
"        ,AgGrp.LongDescription As BrokerGrp"
"        ,Company.Code As CompanyCode"
"        ,AgGrp.Code As BrokerCode"
"        ,cast(0 as decimal(18,2)) as Upto15"
"        ,cast(0 as decimal(18,2)) as Range16"
"        ,cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as Over30"
"        ,cast(0 as decimal(18,2)) as DNamt"
"        ,cast(0 as decimal(18,2)) as UnBilledAmt"
"        ,cast(0 as decimal(18,2)) as UnAdjusted"
" from FinOpendocuments as FOD"
"   JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"   JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"   JOIN PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                 And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                 And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                 And FOD.CODE = PI.FINDOCCODE      "
"  JOIN    AgentsGroupDetail AGD    On      PI.Agent1Code = AGD.AgentCode"
"  JOIN    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code"

" Where DocumentTypeCode in('SD')"
"                                AND FinancialYearCode ='2023'"
"                                And AmountinCC-ClearedAmount>0"
"                                AND days (current date) - days (POSTINGDATE)> 30"
" Group By Company.LongDescription,Company.Code,AgGrp.LongDescription,AgGrp.Code"

" Union All"

" Select  Company.LongDescription As Company"
"        ,AgGrp.LongDescription As BrokerGrp"
"        ,Company.Code As CompanyCode"
"        ,AgGrp.Code As BrokerCode"
"        ,cast(0 as decimal(18,2)) as Upto15"
"        ,cast(0 as decimal(18,2)) as Range16"
"        ,cast(0 as decimal(18,2)) as Over30"
"        ,cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as DNamt"
"        ,cast(0 as decimal(18,2)) as UnBilledAmt"
"        ,cast(0 as decimal(18,2)) as UnAdjusted"
" from FinOpendocuments as FOD"
"  JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"  JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"  JOIN PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                 And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                 And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                 And FOD.CODE = PI.FINDOCCODE      "
"  JOIN    AgentsGroupDetail AGD    On      PI.Agent1Code = AGD.AgentCode"
"  JOIN    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code"

" Where DocumentTypeCode in('CD')"
"                                AND FinancialYearCode ='2023'"
"                                And AmountinCC-ClearedAmount>0"
" Group By Company.LongDescription,Company.Code,AgGrp.LongDescription,AgGrp.Code"

" Union ALl"

" Select  Company.LongDescription As Company"
"        ,AgGrp.LongDescription As BrokerGrp"
"        ,Company.Code As CompanyCode"
"        ,AgGrp.Code As BrokerCode"
"        ,cast(0 as decimal(18,2)) as Upto15"
"        ,cast(0 as decimal(18,2)) as Range16"
"        ,cast(0 as decimal(18,2)) as Over30"
"        ,cast(0 as decimal(18,2)) as DNamt"
"        ,cast(Sum(SD.ONDOCUMENTTOTALAMOUNT -0)as decimal(18,2))  aS UnBilledAmt"
"        ,cast(0 as decimal(18,2)) as UnAdjusted"
" From    SalesDocument SD"
"           JOIN BusinessUnitVsCompany BUC  ON      SD.DivisionCode   = BUC.DivisionCode"
"  JOIN FINBUSINESSUNIT UNIT       ON      BUC.BusinessUnitcode=UNIT.CODE "
"                                And UNIT.GroupFlag = 0"
"  JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"                                And Company.GroupFlag = 1"
"           JOIN    AgentsGroupDetail AGD   On      SD.AGENT1CODE = AGD.AgentCode"
"           JOIN    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code"
"         Where   SD.DOCUMENTTYPETYPE In ('05') "
"         And SD.INVOICEEVOLUTIONTYPE = '1'"

" Group By Company.LongDescription,Company.Code,AgGrp.LongDescription,AgGrp.Code"

" Union All"

" Select  Company.LongDescription As Company"
"        ,AgGrp.LongDescription As BrokerGrp"
"        ,Company.Code As CompanyCode"
"        ,AgGrp.Code As BrokerCode"
"        ,cast(0 as decimal(18,2)) as Upto15"
"        ,cast(0 as decimal(18,2)) as Range16"
"        ,cast(0 as decimal(18,2)) as Over30"
"        ,cast(0 as decimal(18,2)) as DNamt"
"        ,cast(0 as decimal(18,2)) as UnBilledAmt"
"        ,cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as UnAdjusted"
" from FinOpendocuments as FOD"
"  JOIN FINBUSINESSUNIT Company    ON      FOD.BUSINESSUNITCODE=Company.CODE"
"  JOIN PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                 And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                 And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                 And FOD.CODE = PI.FINDOCCODE      "
"  JOIN    AgentsGroupDetail AGD    On      PI.Agent1Code = AGD.AgentCode"
"  JOIN    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code"
" Where FOD.AMOUNTINCC > 0"
"         AND FOD.AMOUNTINCC - FOD.ClearedAmount <> 0"
"         And FOD.DOCUMENTTYPECODE In ('BR','CR') "
"         And FOD.DOCUMENTTEMPLATECODE In ('B12','B18')"
"         AND FinancialYearCode ='2023'"
" Group By Company.LongDescription,Company.Code,AgGrp.LongDescription,AgGrp.Code"


") As BrokerGrpOS "
"         Group By BrokerGrpOS.Company, BrokerGrpOS.BrokerGrp,BrokerGrpOS.CompanyCode,BrokerGrpOS.BrokerCode"
"         Order by BrokerGrp"
    )

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        new = (
            float("%.2f" % float(result["UPTO15"]))
            + float("%.2f" % float(result["RANGE16"]))
            + float("%.2f" % float(result["OVER30"]))
            + float("%.2f" % float(result["DNAMT"]))
            + float("%.2f" % float(result["UNBILLEDAMT"]))
            - float("%.2f" % float(result["UNADJUSTED"]))
        )
        result["TOTAL"] = round(float(new) / 100000, 2)
        result["UPTO15"] = round(float(result["UPTO15"]) / 100000, 2)
        result["RANGE16"] = round(float(result["RANGE16"]) / 100000, 2)
        result["OVER30"] = round(float(result["OVER30"]) / 100000, 2)
        result["DNAMT"] = round(float(result["DNAMT"]) / 100000, 2)
        result["UNBILLEDAMT"] = round(float(result["UNBILLEDAMT"]) / 100000, 2)
        result["UNADJUSTED"] = round(float(result["UNADJUSTED"]) / 100000, 2)
        # result["ABOVEODDAYS"] = round(float(result["ABOVEODDAYS"]) / 100000, 2)
        GDataBrokerWiseOS.append(result)
        total = total + (float("%.2f" % float(result["TOTAL"])))
        upto15 = upto15 + (float("%.2f" % float(result["UPTO15"])))
        range16 = range16 + (float("%.2f" % float(result["RANGE16"])))
        over30 = over30 + (float("%.2f" % float(result["OVER30"])))
        dnamt = dnamt + (float("%.2f" % float(result["DNAMT"])))
        advance = advance + (float("%.2f" % float(result["UNBILLEDAMT"])))
        unbilled = unbilled + (float("%.2f" % float(result["UNBILLEDAMT"])))
        unadj = unadj + (float("%.2f" % float(result["UNADJUSTED"])))
        # olddays = olddays + (float("%.2f" % float(result["ABOVEODDAYS"])))
        result = con.db.fetch_both(stmt)

    for i in GDataBrokerWiseOS:
        if i["BROKERGRP"] not in GDataCompany:
            GDataCompany.append(i["BROKERGRP"])
    for j in GDataCompany:
        for k in GDataBrokerWiseOS:
            if j == k["BROKERGRP"]:
                b = k["BROKERGRP"]
                t = t + float(k["TOTAL"])
                u = u + float(k["UPTO15"])
                r = r + float(k["RANGE16"])
                o = o + float(k["OVER30"])
                d = d + float(k["DNAMT"])
                un = un + float(k["UNBILLEDAMT"])
                una = una + +float(k["UNADJUSTED"])
                # od = od + float(k["ABOVEODDAYS"])

            else:
                if b != 0:
                    resultset = {
                        "BROKER": b,
                        "TOTAL": float("%.2f" % t),
                        "UPTO15": float("%.2f" % u),
                        "RANGE16":float("%.2f" % r),
                        "OVER30": float("%.2f" % o),
                        "DNAMT": float("%.2f" % d),
                        "UNBILLEDAMT": float("%.2f" % un),
                        "UNADJUSTED": float("%.2f" % una),
                        # "ABOVEODDAYS": float("%.2f" % od),
                    }
                    GDataTotal.append(resultset)
                    b = 0
                    t = 0
                    u = 0
                    r = 0
                    o = 0
                    d = 0
                    un = 0
                    una = 0
                    od = 0

    return render(
        request,
        "BrokerWiseOS.html",
        {
            "GDataBrokerWiseOS": GDataBrokerWiseOS,
            "GDataCompany": GDataCompany,
            "GDataTotal": GDataTotal,
            "s": 0,
            "total": str(
                format_currency((float("%.2f" % float(total))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "upto15": str(
                format_currency((float("%.2f" % float(upto15))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "range16": str(
                format_currency((float("%.2f" % float(range16))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "over30": str(
                format_currency((float("%.2f" % float(over30))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "dnamt": str(
                format_currency((float("%.2f" % float(dnamt))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "advance": str(
                format_currency((float("%.2f" % float(advance))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "unbilled": str(
                format_currency(
                    (float("%.2f" % float(unbilled))), "INR", locale="en_IN"
                )
            ).replace("₹", ""),
            "unadj": str(
                format_currency((float("%.2f" % float(unadj))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "olddays": str(
                format_currency((float("%.2f" % float(olddays))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "TOTAL": str(
                format_currency((float("%.2f" % float(TOTAL))), "INR", locale="en_IN")
            ).replace("₹", ""),"GDataYear":GDataYear,"year":year
            # 'startdate': stdt.strftime("%d %B %Y"),
            # 'enddate': etdt.strftime("%d %B %Y")}
        },
    )


def updateYear(request):
    year = request.GET['year']
    b = 0
    t = 0
    u = 0
    r = 0
    o = 0
    d = 0
    un = 0
    od = 0
    una = 0

    global total
    global upto15
    global range16
    global over30
    global dnamt
    global advance
    global unbilled
    global unadj
    global olddays
    global TOTAL
    global i
    total = 0
    upto15 = 0
    range16 = 0
    over30 = 0
    dnamt = 0
    advance = 0
    unbilled = 0
    unadj = 0
    olddays = 0
    TOTAL = 0

    global GDataBrokerWiseOS
    global GDataCompany
    global GDataTotal
    global GDataYear
    GDataBrokerWiseOS = []
    GDataCompany = []
    GDataTotal = []
    GDataYear=[]

    sql = "Select CODE from FINFINANCIALYEAR order by CODE desc"
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        GDataYear.append(result)
        result = con.db.fetch_both(stmt)
    sql = (
        "Select BrokerGrpOS.Company, BrokerGrpOS.BrokerGrp,BrokerGrpOS.CompanyCode,BrokerGrpOS.BrokerCode,"
"         Sum(BrokerGrpOS.Upto15) As Upto15,Sum(BrokerGrpOS.Range16) As Range16,Sum(BrokerGrpOS.Over30) As Over30"
"         , Sum(BrokerGrpOS.DNAmt) As DNAmt,Sum(BrokerGrpOS.UnBilledAmt) As UnBilledAmt,Sum(BrokerGrpOS.UnAdjusted) As UnAdjusted"
"         From ("

" Select  Company.LongDescription As Company"
"        ,AgGrp.LongDescription As BrokerGrp"
"        ,Company.Code As CompanyCode"
"        ,AgGrp.Code As BrokerCode"
"        ,cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as Upto15"
"        ,cast(0 as decimal(18,2)) as Range16"
"        ,cast(0 as decimal(18,2)) as Over30"
"        ,cast(0 as decimal(18,2)) as DNamt"
"        ,cast(0 as decimal(18,2)) as UnBilledAmt"
"        ,cast(0 as decimal(18,2)) as UnAdjusted"
" from FinOpendocuments as FOD"
"   JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"   JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"   JOIN PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                 And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                 And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                 And FOD.CODE = PI.FINDOCCODE      "
"   JOIN    AgentsGroupDetail AGD    On      PI.Agent1Code = AGD.AgentCode"
"   JOIN    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code"

" Where DocumentTypeCode in('SD')"
"                                AND FinancialYearCode ='"+year+"'"
"                                And AmountinCC-ClearedAmount>0"
"                                AND days (current date) - days (POSTINGDATE) <=15"
" Group By Company.LongDescription,Company.Code,AgGrp.LongDescription,AgGrp.Code"

" Union All"

" Select  Company.LongDescription As Company"
"        ,AgGrp.LongDescription As BrokerGrp"
"        ,Company.Code As CompanyCode"
"        ,AgGrp.Code As BrokerCode"
"        ,cast(0 as decimal(18,2)) as Upto15"
"        ,cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as Range16"
"        ,cast(0 as decimal(18,2)) as Over30"
"        ,cast(0 as decimal(18,2)) as DNamt"
"        ,cast(0 as decimal(18,2)) as UnBilledAmt"
"        ,cast(0 as decimal(18,2)) as UnAdjusted"
" from FinOpendocuments as FOD"
"  JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"  JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"  JOIN PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                 And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                 And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                 And FOD.CODE = PI.FINDOCCODE      "
"  JOIN    AgentsGroupDetail AGD    On      PI.Agent1Code = AGD.AgentCode"
"  JOIN    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code"

" Where DocumentTypeCode in('SD')"
"                                AND FinancialYearCode ='"+year+"'"
"                                And AmountinCC-ClearedAmount>0"
"                                AND days (current date) - days (POSTINGDATE) between 16 and 30"
" Group By Company.LongDescription,Company.Code,AgGrp.LongDescription,AgGrp.Code"

" Union All"


" Select  Company.LongDescription As Company"
"        ,AgGrp.LongDescription As BrokerGrp"
"        ,Company.Code As CompanyCode"
"        ,AgGrp.Code As BrokerCode"
"        ,cast(0 as decimal(18,2)) as Upto15"
"        ,cast(0 as decimal(18,2)) as Range16"
"        ,cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as Over30"
"        ,cast(0 as decimal(18,2)) as DNamt"
"        ,cast(0 as decimal(18,2)) as UnBilledAmt"
"        ,cast(0 as decimal(18,2)) as UnAdjusted"
" from FinOpendocuments as FOD"
"   JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"   JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"   JOIN PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                 And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                 And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                 And FOD.CODE = PI.FINDOCCODE      "
"  JOIN    AgentsGroupDetail AGD    On      PI.Agent1Code = AGD.AgentCode"
"  JOIN    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code"

" Where DocumentTypeCode in('SD')"
"                                AND FinancialYearCode ='"+year+"'"
"                                And AmountinCC-ClearedAmount>0"
"                                AND days (current date) - days (POSTINGDATE)> 30"
" Group By Company.LongDescription,Company.Code,AgGrp.LongDescription,AgGrp.Code"

" Union All"

" Select  Company.LongDescription As Company"
"        ,AgGrp.LongDescription As BrokerGrp"
"        ,Company.Code As CompanyCode"
"        ,AgGrp.Code As BrokerCode"
"        ,cast(0 as decimal(18,2)) as Upto15"
"        ,cast(0 as decimal(18,2)) as Range16"
"        ,cast(0 as decimal(18,2)) as Over30"
"        ,cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as DNamt"
"        ,cast(0 as decimal(18,2)) as UnBilledAmt"
"        ,cast(0 as decimal(18,2)) as UnAdjusted"
" from FinOpendocuments as FOD"
"  JOIN FINBUSINESSUNIT UNIT    ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"  JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"  JOIN FinDocument FD            on FOD.BUSINESSUNITCODE=FD.BUSINESSUNITCODE " 
"                                 And  FOD.FINANCIALYEARCODE=FD.FINANCIALYEARCODE"
"                                 And FOD.DOCUMENTTEMPLATECODE = FD.DOCUMENTTEMPLATECODE "
"                                 And FOD.CODE = FD.CODE      "
"  JOIN    AgentsGroupDetail AGD    On      FD.Agent1Code = AGD.AgentCodE"
"  JOIN    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code"

" Where FOD.DocumentTypeCode in('CD')"
"                                AND FOD.FinancialYearCode ='"+year+"'"
"                                And FOD.AmountinCC-FOD.ClearedAmount>0"
" Group By Company.LongDescription,Company.Code,AgGrp.LongDescription,AgGrp.Code"

" Union ALl"

" Select  Company.LongDescription As Company"
"        ,AgGrp.LongDescription As BrokerGrp"
"        ,Company.Code As CompanyCode"
"        ,AgGrp.Code As BrokerCode"
"        ,cast(0 as decimal(18,2)) as Upto15"
"        ,cast(0 as decimal(18,2)) as Range16"
"        ,cast(0 as decimal(18,2)) as Over30"
"        ,cast(0 as decimal(18,2)) as DNamt"
"        ,cast(Sum(SD.ONDOCUMENTTOTALAMOUNT -0)as decimal(18,2))  aS UnBilledAmt"
"        ,cast(0 as decimal(18,2)) as UnAdjusted"
" From    SalesDocument SD"
"           JOIN BusinessUnitVsCompany BUC  ON      SD.DivisionCode   = BUC.DivisionCode"
"  JOIN FINBUSINESSUNIT UNIT       ON      BUC.BusinessUnitcode=UNIT.CODE "
"                                And UNIT.GroupFlag = 0"
"  JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"                                And Company.GroupFlag = 1"
"           JOIN    AgentsGroupDetail AGD   On      SD.AGENT1CODE = AGD.AgentCode"
"           JOIN    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code"
"         Where   SD.DOCUMENTTYPETYPE In ('05') "
"         And SD.INVOICEEVOLUTIONTYPE = '1'"

" Group By Company.LongDescription,Company.Code,AgGrp.LongDescription,AgGrp.Code"

" Union All"

" Select  Company.LongDescription As Company"
"        ,AgGrp.LongDescription As BrokerGrp"
"        ,Company.Code As CompanyCode"
"        ,AgGrp.Code As BrokerCode"
"        ,cast(0 as decimal(18,2)) as Upto15"
"        ,cast(0 as decimal(18,2)) as Range16"
"        ,cast(0 as decimal(18,2)) as Over30"
"        ,cast(0 as decimal(18,2)) as DNamt"
"        ,cast(0 as decimal(18,2)) as UnBilledAmt"
"        ,cast(Sum(AMOUNTINCC-CLEAREDAMOUNT) as decimal(18,2)) as UnAdjusted"
" from FinOpendocuments as FOD"
"  JOIN FINBUSINESSUNIT Company    ON      FOD.BUSINESSUNITCODE=Company.CODE"
"  JOIN PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                 And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                 And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                 And FOD.CODE = PI.FINDOCCODE      "
"  JOIN    AgentsGroupDetail AGD    On      PI.Agent1Code = AGD.AgentCode"
"  JOIN    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code"
" Where FOD.AMOUNTINCC > 0"
"         AND FOD.AMOUNTINCC - FOD.ClearedAmount <> 0"
"         And FOD.DOCUMENTTYPECODE In ('BR','CR') "
"         And FOD.DOCUMENTTEMPLATECODE In ('B12','B18')"
"         AND FinancialYearCode ='"+year+"'"
" Group By Company.LongDescription,Company.Code,AgGrp.LongDescription,AgGrp.Code"


") As BrokerGrpOS "
"         Group By BrokerGrpOS.Company, BrokerGrpOS.BrokerGrp,BrokerGrpOS.CompanyCode,BrokerGrpOS.BrokerCode"
"         Order by BrokerGrp"
    )
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        new = (
            float("%.2f" % float(result["UPTO15"]))
            + float("%.2f" % float(result["RANGE16"]))
            + float("%.2f" % float(result["OVER30"]))
            + float("%.2f" % float(result["DNAMT"]))
            + float("%.2f" % float(result["UNBILLEDAMT"]))
            - float("%.2f" % float(result["UNADJUSTED"]))
        )
        result["TOTAL"] = round(float(new) / 100000, 2)
        result["UPTO15"] = round(float(result["UPTO15"]) / 100000, 2)
        result["RANGE16"] = round(float(result["RANGE16"]) / 100000, 2)
        result["OVER30"] = round(float(result["OVER30"]) / 100000, 2)
        result["DNAMT"] = round(float(result["DNAMT"]) / 100000, 2)
        result["UNBILLEDAMT"] = round(float(result["UNBILLEDAMT"]) / 100000, 2)
        result["UNADJUSTED"] = round(float(result["UNADJUSTED"]) / 100000, 2)
        # result["ABOVEODDAYS"] = round(float(result["ABOVEODDAYS"]) / 100000, 2)
        GDataBrokerWiseOS.append(result)
        total = total + (float("%.2f" % float(result["TOTAL"])))
        upto15 = upto15 + (float("%.2f" % float(result["UPTO15"])))
        range16 = range16 + (float("%.2f" % float(result["RANGE16"])))
        over30 = over30 + (float("%.2f" % float(result["OVER30"])))
        dnamt = dnamt + (float("%.2f" % float(result["DNAMT"])))
        advance = advance + (float("%.2f" % float(result["UNBILLEDAMT"])))
        unbilled = unbilled + (float("%.2f" % float(result["UNBILLEDAMT"])))
        unadj = unadj + (float("%.2f" % float(result["UNADJUSTED"])))
        # olddays = olddays + (float("%.2f" % float(result["ABOVEODDAYS"])))
        result = con.db.fetch_both(stmt)

    for i in GDataBrokerWiseOS:
        if i["BROKERGRP"] not in GDataCompany:
            GDataCompany.append(i["BROKERGRP"])
    for j in GDataCompany:
        for k in GDataBrokerWiseOS:
            if j == k["BROKERGRP"]:
                b = k["BROKERGRP"]
                t = t + float(k["TOTAL"])
                u = u + float(k["UPTO15"])
                r = r + float(k["RANGE16"])
                o = o + float(k["OVER30"])
                d = d + float(k["DNAMT"])
                un = un + float(k["UNBILLEDAMT"])
                una = una + +float(k["UNADJUSTED"])
                # od = od + float(k["ABOVEODDAYS"])

            else:
                if b != 0:
                    resultset = {
                        "BROKER": b,
                        "TOTAL": float("%.2f" % t),
                        "UPTO15": float("%.2f" % u),
                        "RANGE16":float("%.2f" % r),
                        "OVER30": float("%.2f" % o),
                        "DNAMT": float("%.2f" % d),
                        "UNBILLEDAMT": float("%.2f" % un),
                        "UNADJUSTED": float("%.2f" % una),
                        # "ABOVEODDAYS": float("%.2f" % od),
                    }
                    GDataTotal.append(resultset)
                    b = 0
                    t = 0
                    u = 0
                    r = 0
                    o = 0
                    d = 0
                    un = 0
                    una = 0
                    od = 0

    return render(
        request,
        "BrokerWiseOS.html",
        {
            "GDataBrokerWiseOS": GDataBrokerWiseOS,
            "GDataCompany": GDataCompany,
            "GDataTotal": GDataTotal,
            "s": 0,
            "total": str(
                format_currency((float("%.2f" % float(total))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "upto15": str(
                format_currency((float("%.2f" % float(upto15))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "range16": str(
                format_currency((float("%.2f" % float(range16))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "over30": str(
                format_currency((float("%.2f" % float(over30))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "dnamt": str(
                format_currency((float("%.2f" % float(dnamt))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "advance": str(
                format_currency((float("%.2f" % float(advance))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "unbilled": str(
                format_currency(
                    (float("%.2f" % float(unbilled))), "INR", locale="en_IN"
                )
            ).replace("₹", ""),
            "unadj": str(
                format_currency((float("%.2f" % float(unadj))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "olddays": str(
                format_currency((float("%.2f" % float(olddays))), "INR", locale="en_IN")
            ).replace("₹", ""),
            "TOTAL": str(
                format_currency((float("%.2f" % float(TOTAL))), "INR", locale="en_IN")
            ).replace("₹", ""),"GDataYear":GDataYear,"year":year
            # 'startdate': stdt.strftime("%d %B %Y"),
            # 'enddate': etdt.strftime("%d %B %Y")}
        },
    )
