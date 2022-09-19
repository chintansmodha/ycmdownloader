from django.shortcuts import render
from Global_Files import Connection_String as con

GDataCompany=[]
GDOrderSummary = []

Exceptions = ''

stmt = con.db.exec_immediate(con.conn,"select code,longdescription from FinBusinessUnit where GROUPFLAG=0  order by CODE")
result = con.db.fetch_both(stmt)
while result != False:
    if result not in GDataCompany:
        GDataCompany.append(result)
    result = con.db.fetch_both(stmt)


def PurchaseOrderHtml(request):
    return render(request, 'PurchaseOrder.html',
                  {'GDataCompany': GDataCompany })

#Data in Grid/Table
def PurchaseOrderTableHtml(request):
    global GDOrderSummary
    GDOrderSummary= []

    LSCompanyUnitCode = request.GET.getlist('comp')
    LDStartDate = "'" + str(request.GET['startdate']) + "'"
    LDEndDate = "'" + str(request.GET['enddate']) + "'"

    companyunitcodes = str(LSCompanyUnitCode)
    LSCompanyUnitCodes = '(' + companyunitcodes[1:-1] + ')'

    companyunitcode = "AND BUSINESSUNITVSCOMPANY.BUSINESSUNITCODE In " + str(LSCompanyUnitCodes)

    sql = "Select                            DISTINCT(PURCHASEORDER.CODE) As PoNo " \
          ", Varchar_Format(PURCHASEORDER.ORDERDATE, 'DD-MM-YYYY') As PoDt " \
          ", Cast(PURCHASEORDER.ONORDERTOTALAMOUNT As Decimal(18,3)) As Amount " \
          "From    PURCHASEORDER " \
          "Join PURCHASEORDERLINE          On      PURCHASEORDER.CODE = PURCHASEORDERLINE.PURCHASEORDERCODE " \
          "And     PURCHASEORDER.COUNTERCODE = PURCHASEORDERLINE.PURCHASEORDERCOUNTERCODE " \
          "Join    LOGICALWAREHOUSE        On      LOGICALWAREHOUSE.CODE = PURCHASEORDERLINE.WAREHOUSECODE " \
          "Join    BUSINESSUNITVSCOMPANY   On      LOGICALWAREHOUSE.PLANTCODE =  BUSINESSUNITVSCOMPANY.FACTORYCODE " \
          "Where   PURCHASEORDER.ORDERDATE Between " + LDStartDate + "    AND     " + LDEndDate + " " + companyunitcode + " " \
          "And Cast(PURCHASEORDER.ONORDERTOTALAMOUNT As Decimal(18,3)) <> 0.000 " \
          "Order   By      PoNo "

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        GDOrderSummary.append(result)
        result = con.db.fetch_both(stmt)

    if GDOrderSummary == []:
        global Exceptions
        Exceptions = "Note: No Result found on given criteria "
        return render(request, 'PurchaseOrder.html',
                      {'GDataCompany': GDataCompany, 'Exception': Exceptions})

    return render(request, 'PurchaseOrderTable.html',
                  {'GDOrderSummary': GDOrderSummary})