from Global_Files import Connection_String as con
#from SummerizedBankBalance_Printing import SummerizedBankBalance_PDF as SBBP
GDataRecivedFrom=[]
GDataPaidTo=[]
def RecievedFrom(StartDate,EndDate,Company,Bank,c,d):
    global GDataRecivedFrom
    GDataRecivedFrom=[]
    StartDate = "'"+StartDate+"'"
    EndDate = "'" + EndDate + "'"
    sql = " Select  Company.LongDescription As BUSINESSUNITName, BankMaster.LongDescription As BankName," \
          " 0 As OpBal, Sum(Case When FinDocument.FinanceDocumentDate >= "+StartDate+"" \
          " And FinDocument.DocumentTypeCode In ('BR','CR') Then FinDocument.DocumentAmount Else 0 End) as Receipts " \
          " ,0 as Payments,Case When FinDocument.FinanceDocumentDate >= "+StartDate+"" \
          " And FinDocument.DocumentTypeCode In ('BR','CR') Then COALESCE(BPCustomer.legalname1,'') Else '' End as RecievedFrom" \
          " ,'' as PaidTo, Company.Code, FinDocument.GLCODE As BankCode, 2 As SortOrder" \
          " From    FinDocument " \
          " Join    FinBusinessUnit         On      FinDocument.BUSINESSUNITCODE = FinBusinessUnit.CODE " \
          " Join    FinBusinessUnit As Company On FinBusinessUnit.GroupbuCode = Company.Code " \
          " Join    GLMaster As BankMaster  On      FinDocument.GLCODE = BankMaster.Code " \
          " Left Join OrderPartner As OPCustomer On  findocument.CUSTOMERCODE = OPCustomer.CUSTOMERSUPPLIERCODE" \
          " and findocument.CUSTOMERTYPE = OPCustomer.CUSTOMERSUPPLIERTYPE" \
          " Left Join businesspartner As BPCustomer On OPCustomer.ORDERBUSINESSPARTNERNUMBERID = BPCustomer.NUMBERID " \
          " Left Join OrderPartner As OPSupplier On findocument.SupplierCODE = OPSupplier.CUSTOMERSUPPLIERCODE " \
          " and findocument.SupplierTYPE = OPSupplier.CUSTOMERSUPPLIERTYPE" \
          " Left Join businesspartner BPSupplier On  OPSupplier.ORDERBUSINESSPARTNERNUMBERID = BPSupplier.NUMBERID" \
          " Where   FinDocument.FinanceDocumentDate <= "+EndDate+"" \
          " And     FinDocument.DocumentTypeCode In ('BR','CR') " \
          "And Company.Code = "+"'"+Company+"'"+"" \
          "And FinDocument.GLCODE ="+"'"+Bank+"'"+"" \
          " Group By company.LongDescription, BankMaster.LongDescription " \
          " , Case When FinDocument.FinanceDocumentDate >= "+StartDate+" And FinDocument.DocumentTypeCode In ('BR','CR') Then COALESCE(BPCustomer.legalname1,'') Else '' End " \
          " , Case When FinDocument.FinanceDocumentDate >= "+StartDate+" And FinDocument.DocumentTypeCode In ('BP','CP') Then COALESCE(BPSupplier.legalname1,'') Else '' End" \
          " , Company.Code, FinDocument.GLCODE"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result!=False:
        GDataRecivedFrom.append(result)
        result = con.db.fetch_both(stmt)
    return GDataRecivedFrom


def PaidTo(StartDate,EndDate,Company,Bank,c,d):
    global GDataPaidTo
    GDataPaidTo=[]
    StartDate = "'"+StartDate+"'"
    EndDate = "'" + EndDate + "'"
    sql = " Select  Company.LongDescription As BUSINESSUNITName, BankMaster.LongDescription As BankName,0 As OpBal, 0 as Receipts " \
          " , Sum(Case When FinDocument.FinanceDocumentDate >= "+StartDate+"" \
          " And FinDocument.DocumentTypeCode In ('BP','CP') Then FinDocument.DocumentAmount Else 0 End) as Payments " \
          " ,'' as RecievedFrom " \
          " ,Case When FinDocument.FinanceDocumentDate >= "+StartDate+"" \
          " And FinDocument.DocumentTypeCode In ('BP','CP') Then COALESCE(BPSupplier.legalname1,'') Else '' End as PaidTo " \
          " ,Company.Code, FinDocument.GLCODE As BankCode, 2 As SortOrder From    FinDocument" \
          " Join    FinBusinessUnit         On      FinDocument.BUSINESSUNITCODE = FinBusinessUnit.CODE " \
          " Join    FinBusinessUnit As Company On FinBusinessUnit.GroupbuCode = Company.Code " \
          " Join    GLMaster As BankMaster  On      FinDocument.GLCODE = BankMaster.Code" \
          " Left Join OrderPartner As OPCustomer On  findocument.CUSTOMERCODE = OPCustomer.CUSTOMERSUPPLIERCODE" \
          " and findocument.CUSTOMERTYPE = OPCustomer.CUSTOMERSUPPLIERTYPE" \
          " Left Join businesspartner As BPCustomer On OPCustomer.ORDERBUSINESSPARTNERNUMBERID = BPCustomer.NUMBERID" \
          " Left Join OrderPartner As OPSupplier On findocument.SupplierCODE = OPSupplier.CUSTOMERSUPPLIERCODE " \
          " and findocument.SupplierTYPE = OPSupplier.CUSTOMERSUPPLIERTYPE" \
          " Left Join businesspartner BPSupplier On  OPSupplier.ORDERBUSINESSPARTNERNUMBERID = BPSupplier.NUMBERID" \
          " Where   FinDocument.FinanceDocumentDate <= "+EndDate+"" \
          " And     FinDocument.DocumentTypeCode In ('BP','CP') " \
          "And Company.Code = " + "'" + Company + "'" + "" \
          "And FinDocument.GLCODE =" + "'" + Bank + "'" + "" \
          " Group By company.LongDescription, BankMaster.LongDescription" \
          " , Case When FinDocument.FinanceDocumentDate >= "+StartDate+" And FinDocument.DocumentTypeCode In ('BR','CR') Then COALESCE(BPCustomer.legalname1,'') Else '' End " \
          " , Case When FinDocument.FinanceDocumentDate >= "+StartDate+" And FinDocument.DocumentTypeCode In ('BP','CP') Then COALESCE(BPSupplier.legalname1,'') Else '' End" \
          " , Company.Code, FinDocument.GLCODE"
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result!=False:
        GDataPaidTo.append(result)
        result = con.db.fetch_both(stmt)
    return GDataPaidTo
