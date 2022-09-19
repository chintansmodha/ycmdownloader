import os
from datetime import datetime
from PrintPDF import MachineWiseProduction_PrintPDF as pdf
from Global_Files import Connection_String as con
from ProcessSelection import MachineWiseProduction_ProcessSelection as MWP

counter = 0


def MachineWiseProduction_PrintPDF(LSDepartmentCode, LCDepartmentCode, LDProductionDate, LDEndDate):
    Departmentcode = str(LSDepartmentCode)
    LSDepartmentCodes = '(' + Departmentcode[1:-1] + ')'

    stdt = datetime.strptime(LDProductionDate, '%Y-%m-%d').date()
    etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    # etdt = datetime.strptime(LDEndDate, '%Y-%m-%d').date()
    productiondate = "'" + str(stdt) + "'"
    enddate = "'" + str(etdt) + "'"
    #
    beginproductiondate = "'" + f'{stdt.year}-{stdt.month}-01' + "'"
    day = f'{stdt.day}'
    # print(day)


    if not LCDepartmentCode and not LSDepartmentCode:
        Departmentcodes = " "
    elif LCDepartmentCode:
        Departmentcodes = " "
    elif LSDepartmentCode:
        Departmentcodes = "And COALESCE(COSTCENTER.CODE,'') in " + str(LSDepartmentCodes)
    # print(LSDay)

    sql = "Select          COALESCE(COSTCENTER.LONGDESCRIPTION, Case When BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE is Null " \
          "Then 'Plant Not Entered' Else 'Department Not Entered' End ) As Department" \
          ", Cast( BKLELEMENTS.LOTCODE AS VARCHAR(4)) As Machine " \
          ", PRODUCT.LONGDESCRIPTION as Item   " \
          ", Cast(SUM(Case When Qlty.Code = '1' And ELEMENTS.ENTRYDATE = "+productiondate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) As Decimal(20,3)) As ToDay_1stQty  " \
          ", Cast(SUM(Case When Qlty.Code = '2' And ELEMENTS.ENTRYDATE = "+productiondate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) As Decimal(20,3)) As ToDay_PQQty " \
          ", Cast(SUM(Case When Qlty.Code = '3' And ELEMENTS.ENTRYDATE = "+productiondate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) As Decimal(20,3)) As ToDay_SSQty " \
          ", Cast(SUM(Case When Qlty.Code not in ('1','2','3') And ELEMENTS.ENTRYDATE = "+productiondate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) As Decimal(20,3)) As ToDay_OtheresQty " \
          ", Cast(SUM(Case When ELEMENTS.ENTRYDATE = "+productiondate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) As Decimal(20,3)) As ToDay_TotalQty " \
          ", CAST(COALESCE(((SUM(Case When Qlty.Code not in ('1','2','3') And ELEMENTS.ENTRYDATE = "+productiondate+" Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
          "NULLIF(SUM(Case When ELEMENTS.ENTRYDATE = "+productiondate+" Then BKLELEMENTS.ACTUALNETWT else 0 End),0)),0) As DECIMAL(5,2)) As ToDay_IIndPerc " \
          ", Cast(SUM(Case When Qlty.Code = '1' Then BKLELEMENTS.ACTUALNETWT else 0 End) As Decimal(20,3)) As Mth_1stQty " \
          ", Cast(SUM(Case When Qlty.Code = '2' Then BKLELEMENTS.ACTUALNETWT else 0 End) As Decimal(20,3)) As Mth_PQQty " \
          ", Cast(SUM(Case When Qlty.Code = '3' Then BKLELEMENTS.ACTUALNETWT else 0 End) As Decimal(20,3)) As Mth_SSQty " \
          ", Cast(SUM(Case When Qlty.Code not in ('1','2','3') Then BKLELEMENTS.ACTUALNETWT else 0 End) As Decimal(20,3)) As Mth_OthersQty " \
          ", Cast(SUM(BKLELEMENTS.ACTUALNETWT) As Decimal(20,3)) As Mth_TotalQty " \
          ", CAST(COALESCE(((SUM(Case When Qlty.Code not in ('1','2','3') Then BKLELEMENTS.ACTUALNETWT else 0 End) * 100) / " \
          "NULLIF(SUM(BKLELEMENTS.ACTUALNETWT),0)),0) As DECIMAL(5,2)) As Mth_IIndPerc " \
          ", Cast(Round(SUM(BKLELEMENTS.ACTUALNETWT)/"+day+",3) As Decimal(20,3)) As Mth_AvgPro " \
          "From BKLELEMENTS " \
          "JOIN    FULLITEMKEYDECODER FIKD                ON      BKLELEMENTS.LOTITEMTYPECODE = FIKD.ITEMTYPECODE " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE01, '') = COALESCE(FIKD.SubCode01, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE02, '') = COALESCE(FIKD.SubCode02, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE03, '') = COALESCE(FIKD.SubCode03, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE04, '') = COALESCE(FIKD.SubCode04, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE05, '') = COALESCE(FIKD.SubCode05, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE06, '') = COALESCE(FIKD.SubCode06, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE07, '') = COALESCE(FIKD.SubCode07, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE08, '') = COALESCE(FIKD.SubCode08, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE09, '') = COALESCE(FIKD.SubCode09, '') " \
          "AND     COALESCE(BKLELEMENTS.LOTDECOSUBCODE10, '') = COALESCE(FIKD.SubCode10, '') " \
          "Join    PRODUCT                                On      BKLELEMENTS.LOTITEMTYPECODE = PRODUCT.ITEMTYPECODE " \
          "And     FIKD.ItemUniqueId = Product.AbsUniqueId " \
          "Left Join QUALITYLEVEL Qlty                    On      BKLELEMENTS.LOTITEMTYPECODE = Qlty.ITEMTYPECODE " \
          "And     BKLELEMENTS.QUALITYLEVELCODE = Qlty.CODE " \
          "left Join LOGICALWAREHOUSE                     On      BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE = LOGICALWAREHOUSE.CODE " \
          "Left Join COSTCENTER                           On      LOGICALWAREHOUSE.COSTCENTERCODE = COSTCENTER.CODE " \
          "Join    ELEMENTS                               On      BKLELEMENTS.CODE = ELEMENTS.CODE " \
          "And     BKLELEMENTS.SUBCODEKEY = ELEMENTS.SUBCODEKEY " \
          "Where   ELEMENTS.ENTRYDATE Between "+beginproductiondate+" and "+productiondate+"  And     BKLELEMENTS.ACTUALNETWT  > 0 " \
          " "+Departmentcodes+" " \
          "Group by  COALESCE(COSTCENTER.LONGDESCRIPTION, Case When BKLELEMENTS.WAREHOUSELOGICALWAREHOUSECODE is Null " \
          "Then 'Plant Not Entered' Else 'Department Not Entered' End ) " \
          ", PRODUCT.LONGDESCRIPTION " \
          ", Cast( BKLELEMENTS.LOTCODE AS VARCHAR(4)) " \
          "Order By Department, Machine, Item "

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
            pdf.c.setDash(2, 3)
            pdf.c.line(30, pdf.d, 1170, pdf.d)
            pdf.c.setDash([], 0)
            pdf.d = pdf.dvalue(stdt, etdt, result, pdf.divisioncode)
            pdf.d = pdf.dvalue(stdt, etdt, result, pdf.divisioncode)
            pdf.PrintDepartmentTotal()

            MWP.Exceptions = ""
            counter = 0
        elif counter == 0:
            MWP.Exceptions = "Note: No Report Form For Given Criteria"
            return

    # pdf.c.setPageSize(pdf.landscape(pdf.A4))
    # print(pdf.pageSize)
    # if pdf.pageSize == 3:
    pdf.c.setPageSize(pdf.landscape(pdf.A3))
    pdf.c.showPage()
    pdf.c.save()

    pdf.newrequest()
    pdf.d = pdf.newpage()