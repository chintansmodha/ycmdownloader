import os
from datetime import datetime
from PrintPDF import DGGainLossItm__PrintPDF as pdf
from Global_Files import Connection_String as con
from ProcessSelection import DGGainLoss_ProcessSelection as DGGain

counter = 0


def DGGainLoss_PrintPDF(LSDepartmentCode, LCDepartmentCode, LDStartdate, LDEndDate):
    Departmentcode = str(LSDepartmentCode)
    LSDepartmentCodes = '(' + Departmentcode[1:-1] + ')'

    stdt = datetime.strptime(LDStartdate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    # etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    startdate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"
    #
    if not LCDepartmentCode and not LSDepartmentCode:
        Departmentcodes = " "
    elif LCDepartmentCode:
        Departmentcodes = " "
    elif LSDepartmentCode:
        Departmentcodes = "And COALESCE(COSTCENTER.CODE,'') in " + str(LSDepartmentCodes)
    # print(LSDay)

    sql = "Select                  COALESCE(COSTCENTER.LONGDESCRIPTION,'') As Department " \
          ", PRODUCT.LONGDESCRIPTION As Item " \
          ", Cast(Sum(Case When Stxn.Templatecode = '099' Then Stxn.USERPRIMARYQUANTITY Else 0 End) As Decimal(15,3)) As Gain " \
          ", Cast(Sum(Case When Stxn.Templatecode = '098' Then Stxn.USERPRIMARYQUANTITY Else 0 End) As Decimal(15,3)) As Loss " \
          "From STOCKTRANSACTION Stxn " \
          "join LOGICALWAREHOUSE               On      Stxn.LOGICALWAREHOUSECODE  =      LOGICALWAREHOUSE.Code " \
          "Left Join    COSTCENTER             On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
          "join FULLITEMKEYDECODER FIKD        ON      Stxn.ITEMTYPECODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(Stxn.DecoSubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(Stxn.DecoSubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(Stxn.DecoSubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(Stxn.DecoSubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(Stxn.DecoSubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(Stxn.DecoSubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(Stxn.DecoSubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(Stxn.DecoSubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(Stxn.DecoSubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(Stxn.DecoSubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join PRODUCT                        On      Stxn.ITEMTYPECODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
          "Where Stxn.Templatecode in ('099', '098') " \
          "And   Stxn.TRANSACTIONDATE    Between   " + startdate + "    And     " + enddate + " " \
                                                                                              " " + Departmentcodes + " " \
                                                                                                                      "Group By COALESCE(COSTCENTER.LONGDESCRIPTION,'') " \
                                                                                                                      ", PRODUCT.LONGDESCRIPTION " \
                                                                                                                      "Order By Department, Item "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)

    while result != False:
        global counter
        counter = counter + 1

        pdf.textsize(pdf.c, result, pdf.d, stdt, etdt)
        pdf.d = pdf.dvalue(stdt, etdt, result, pdf.divisioncode)
        result = con.db.fetch_both(stmt)

    if result == False:
        if counter > 0:

            pdf.d = pdf.dvalue(stdt, etdt, result, pdf.divisioncode)
            pdf.PrintGrandTotal()

            DGGain.Exceptions = ""
            counter = 0
        elif counter == 0:
            DGGain.Exceptions = "Note: No Report Form For Given Criteria"
            return

    # pdf.c.setPageSize(pdf.landscape(pdf.A4))
    # print(pdf.pageSize)
    # if pdf.pageSize == 3:
    # pdf.c.setPageSize(pdf.landscape(pdf.A4))
    pdf.c.showPage()
    pdf.c.save()

    pdf.newrequest()
    pdf.d = pdf.newpage()