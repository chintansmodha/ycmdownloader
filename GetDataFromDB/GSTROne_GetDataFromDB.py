from datetime import datetime
from Global_Files import Connection_String as con
from PrintPDF import GSTRONE_XLSX as xlsrpt

def GSTRONE_GetData(LSCompany,LCCompany,LDStartDate,LDEndDate):
    xlsrpt.filename()
    LSName = datetime.now()
    LSstring = str(LSName)
    global LSFileName
    LSFileName = LSstring[0:4] + LSstring[5:7] + LSstring[8:10] + LSstring[11:13] + LSstring[14:16] + LSstring[
                                                                                                      17:19] + LSstring[
                                                                                                               20:]
    LSFileName = " GSTROne " + LSFileName + ".xlsx"


    if not LCCompany and not LSCompany or LCCompany:
        LSCompany = " "
    elif LSCompany:
        LSCompany = " AND plant.CODE in (" + str(LSCompany)[1:-1] + ")"


    stdt = datetime.strptime(LDStartDate, "%Y-%m-%d").date()
    etdt = datetime.strptime(LDEndDate, "%Y-%m-%d").date()

    sql = (
    " select distinct PlantInv.InvoiceDate "
", Left(PlantInv.Code, 3) || '-' || substring(Trim(PlantInv.Code),4,10) || '/' || Right(Year(FY.FromDate),2) || '-' || Right(Year(FY.ToDate),2) As InvNo "
", BusiPartner.LegalName1 As CustomerName, COALESCE(CustGST.GSTInNumber,  '') As CustomerGSTNo "
", COALESCE(CustGST.StateCode, '') || '-' || COALESCE(GSTState.LongDescription,'') As PlaceOfSupply "
", 'G' As ItemGoodsOrServices, Trim(PlantInvLine.LongDescription) As ItemDescription, Rtrim(PlantInvLine.TariffCode) As HSNCode "
", PlantInvLine.BasePrimaryQty As ItemQuantity, Trim(UOM.ShortDescription) As ItemUnitOfMeasurement "
", PlantInvLine.Price As ItemRate, 0 As TotalItemDiscountAmount "
", cast(PlantInv.Basicvalue as decimal(18)) As ItemTaxableValue "
", ITaxCGS.Value As CGSTRate, IndTaxTotCGS.CalculatedValueRTC As CGSTAmount "
", ITaxUGS.Value As UTGSTRate, IndTaxTotUGS.CalculatedValueRTC As UTGSTAmount "
", ITaxIGS.Value As IGSTRate, IndTaxTotIGS.CalculatedValueRTC As IGSTAmount "
", 0.0 As CESSRate, 0.0 As CESSAmount, 'Y' As BillofSupply, 'N' As ReverseCharge, 'N' As NillRatedItem "
", '' As OriginalInvDate, '' As OriginalInvNumber, '' As OriginalInvCustomer, '' As GSTINOfECommerce "
", '' As DateOfLinkedAdvanceReceipt, '' As VoucherNumberOfLinkedAdvanceReceipt, 0 As AdvanceAdjAmount "
", '' As TypeOfExport "
", '' As ShippingPortCodeExport, '' As ShippingBillNumberExport, '' As ShippingBillDateExport "
", 'N' As HasGST_IDT_TDS_Deducted, 'N' As IsThisDocumentCancelled "
", '' As TCSAmount "
"From plantinvoice PlantInv "
"Join PlantInvoiceLine PlantInvLine      On      PlantInv.Code                           = PlantInvLine.PlantInvoiceCode "
"Join Plant                              ON      PlantInv.FactoryCode                    = Plant.code "
"Join FINFinancialYear FY                On      PlantInv.CompanyCode                    = FY.CompanyCode "
                                        "And     PlantInv.InvoiceDate Between FY.FromDate and FY.ToDate "
 "Join OrderPartner Customer              On      PlantInv.BuyerIfOTCCustomerSupplierCode = Customer.CustomerSupplierCode "
                                        "And     PlantInv.BuyerIfOTCCustomerSupplierType = Customer.CustomerSupplierType "
"Join BusinessPartner BusiPartner        On      Customer.OrderBusinessPartnerNumberId   = BusiPartner.NumberId "
"Join UnitOfMeasure UOM                  On      PlantInvLine.PrimaryUMCode              = UOM.Code "
"Join FullItemKeyDeCoder ItemMaster      On      PlantInvLine.itemtypecode = ItemMaster.ITEMTYPECODE "
                                        "And     Coalesce(PlantInvLine.SubCode01, '')       = Coalesce(ItemMaster.SubCode01, '') "
                                        "And     Coalesce(PlantInvLine.SubCode02, '')       = Coalesce(ItemMaster.SubCode02, '') "
                                        "And     Coalesce(PlantInvLine.SubCode03, '')       = Coalesce(ItemMaster.SubCode03, '') "
                                        "And     Coalesce(PlantInvLine.SubCode04, '')       = Coalesce(ItemMaster.SubCode04, '') "
                                        "And     Coalesce(PlantInvLine.SubCode05, '')       = Coalesce(ItemMaster.SubCode05, '') "
                                        "And     Coalesce(PlantInvLine.SubCode06, '')       = Coalesce(ItemMaster.SubCode06, '') "
                                        "And     Coalesce(PlantInvLine.SubCode07, '')       = Coalesce(ItemMaster.SubCode07, '') "
                                        "And     Coalesce(PlantInvLine.SubCode08, '')       = Coalesce(ItemMaster.SubCode08, '') "
                                        "And     Coalesce(PlantInvLine.SubCode09, '')       = Coalesce(ItemMaster.SubCode09, '') "
                                        "And     Coalesce(PlantInvLine.SubCode10, '')       = Coalesce(ItemMaster.SubCode10, '') "
"Join PRODUCT                            ON      PlantInvLine.ITEMTYPECODE                  = PRODUCT.ITEMTYPECODE "
                                        "AND     ItemMaster.ItemUniqueId = Product.AbsUniqueId "
"JOIN IndTaxtotal                        ON      PlantInv.AbsUniqueID                       = IndTaxtotal.AbsUniqueID  "
                                        "And     IndTaxtotal.CALCULATEDVALUERTC  <> 0  "
"Join ITAX                               on      IndTaxtotal.ITAXCODE                       = ITAX.CODE   "
"Left JOIN IndTaxtotal IndTaxTotIGS      ON      PlantInv.AbsUniqueID                       = IndTaxTotIGS.AbsUniqueID  "
                                        "And     IndTaxTotIGS.CALCULATEDVALUERTC  <> 0  "
                                        "And     IndTaxTotIGS.TaxCategoryCode = 'GST' "
"Left Join ITAX ITaxIGS                  on      IndTaxTotIGS.ITaxCode                       = ITaxIGS.CODE   "
                                        "And     ITaxIGS.FormTypeCode = 'IGS' "
"Left JOIN IndTaxtotal IndTaxTotCGS      ON      PlantInv.AbsUniqueID                       = IndTaxTotCGS.AbsUniqueID  "
                                        "And     IndTaxTotCGS.CALCULATEDVALUERTC  <> 0  "
                                        "And     IndTaxTotCGS.TaxCategoryCode = 'GST' "
"Left Join ITAX ITaxCGS                  on      IndTaxTotCGS.ITaxCode                       = ITaxCGS.CODE   "
                                        "And     ITaxCGS.FormTypeCode = 'CGS' "
"Left JOIN IndTaxtotal IndTaxTotUGS      ON      PlantInv.AbsUniqueID                       = IndTaxTotUGS.AbsUniqueID  "
                                        "And     IndTaxTotUGS.CALCULATEDVALUERTC  <> 0  "
                                        "And     IndTaxTotUGS.TaxCategoryCode = 'GST' "
"Left Join ITAX ITaxUGS                  on      IndTaxTotUGS.ITaxCode                       = ITaxUGS.CODE   "
                                        "And     ITaxUGS.FormTypeCode = 'SGS' "
"Left Join AddressGST CustGST            On      BusiPartner.AbsUniqueId                    = CustGST.UniqueId "
"Left Join State GSTState                On      CustGST.StateCode                          = GSTState.Code "
"Where PlantInv.InvoiceDate Between '"+LDStartDate+"' and '"+LDEndDate+"'"+LSCompany+""
"Order by InvNo "
    )
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    if result == False:
        return
    while result != False:
        xlsrpt.textsize( result, stdt, etdt)
        result = con.db.fetch_both(stmt)
    xlsrpt.workbook.close()