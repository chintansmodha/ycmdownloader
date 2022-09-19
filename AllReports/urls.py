from django.urls import path
from AllReports import views
# from FormLoad import *
# from FormLoad import AdhocLedger_FormLoad as AHLviews
# from ProcessSelection import AdhocLedger_ProcessSelection as AdhocLedger_Views
# from FormLoad import BankCashStatement_FormLoad as BCSviews
# from ProcessSelection import BankCashStatement_ProcessSelection as BankCashStatement_View
# from FormLoad import GSTRegister_FormLoad as GSTviews
# from ProcessSelection import GSTRegister_ProcessSelection as GSTRegister_Views
# from ProcessSelection import MISBrokerWiseOS_ProcessSelection as MBWOSviews
# from GetDataFromDB import MISBrokerWiseOS_GetDataFromDB as MISBrokerWiseOS_Views
# from ProcessSelection import MISCompany_ProcessSelection as MCWOSviews
# from FormLoad import MRNRegister_FormLoad as MRNviews
# from ProcessSelection import MRNRegister_ProcessSelection as MRNRegister_Views
# from FormLoad import PendingPurchaseRegister_FormLoad as PPRviews
# from ProcessSelection import PendingPurchaseRegister_ProcessSelection as PendingPurchaseRegister_View
# from FormLoad import PurchaseRegister_FormLoad as PRviews
# from ProcessSelection import PurchaseRegister_ProcessSelection as PurchaseRegister_Views
# from FormLoad import SalesRegister_FormLoad as SRviews
# from ProcessSelection import SalesRegister_ProcessSelection as SalesRegister_View
# from FormLoad import Store_Unbilled_GRN_FormLoad as SUGviews
# from ProcessSelection import Store_Unbilled_GRN_ProcessSelection as Store_Unbilled_GRN_View
# from FormLoad import SummerizedBankBalance_FormLoad as SBBviews
# from ProcessSelection import SummerizedBankBalance_ProcessSelection as SummerizedBankBalance_Views
# from FormLoad import PrintYarnChallan_FormLoad as PYCviews
# from GetDataFromDB import PrintYarnChallan_GetDataFromDB as PrintYarnChallan_Views
# from FormLoad import YarnIssueRegister_FormLoad as YIRviews
# from ProcessSelection import YarnIssueRegister_ProcessSelection as YarnIssueRegister_View
# from FormLoad import AdhocLedgerPdf_FormLoad as AdhocViews
# from ProcessSelection import AdhocLedgerPDF_ProcessSelection as AdhocPro
# from FormLoad import ChallanRegister_FormLoad as CRviews
# from ProcessSelection import ChallanRegister_ProcessSelection as ChallanRegister_View
# from GetDataFromDB import PrintChallan_Rule55_GetDataFromDB as PrintChallanRule55_Views
# from FormLoad import DespatchInstruction_FormLoad as DIRviews
# from ProcessSelection import DespatchInstructionRegister_ProcessSelection as DespatchInstructionRegister_View
# from FormLoad import OnlineBankBalance_FormLoad as OBBviews
# from FormLoad import BrokerWiseChallanList_FormLoad as BWCLviews
# from ProcessSelection import BrokerWiseChallanList_ProcessSelection as BrokerWiseChallanList_View
# from FormLoad import PrintDespatchInstruction_FormLoad as PDIviews
# from GetDataFromDB import PrintDespatchInstruction_GetDataFromDB as PrintDespatchInstruction_Views
# from ProcessSelection import PrintDespatchInstruction_ProcessSelection as PDI_PS
# from GetDataFromDB import PrintDespatchInstruction_WithoutRD_GetDataFromDB as PrintDespatchInstruction_WithoutRD_Views
# from GetDataFromDB import PrintChallanBoxNoWise_GetDataFromDB as PrintChallanBoxNoWise_Views
# from GetDataFromDB import DespatchReport_GetDataFromDB as DespatchReport_Views
# from FormLoad import LotNoListing_FormLoad as Lotviews
# from ProcessSelection import LotNoListing_ProcessSelection as Lot_Views
# from FormLoad import FinishedStockInHand_FormLoad as FSIH_Views
# from ProcessSelection import FinishedStockInHand_ProcessSelection as FSIH_PS
# from ProcessSelection import FinshedStockInHandAgeing_ProcessSelection as FSIH_A
# from FormLoad import PackingReport_FormLoad as PackR_Views
# from ProcessSelection import PackingReport_ProcessSelection as PackR_PS
# from FormLoad import PrintChallanAdvice_FormLoad as PCA_Views
# from GetDataFromDB import PrintChallanAdvice_GetFromDB as PrintChallanAdvGetData
# from FormLoad import PurchaseOrder_FormLoad as POrder_Views
# from GetDataFromDB import PurchaseOrder_GetFromDB as POrder
from FormLoad import FinishedStock_FormLoad as FSview
from FormLoad import FinishedStock_Apply_FormLoad as FSAview
from FormLoad import FinishedStock_Detail_FormLoad as FSDview
# from GetDataFromDB import PrintChallanBoxNoWiseInternal_GetDataFromDB as PrintChallanInternal_Views
# from FormLoad import BrokerGroupCompanyWiseOS_FormLoad as BrokerGrpviews
# from ProcessSelection import BrokerGroupCompanyWiseOS_ProcessSelection as BrokerGrp_Views
# from FormLoad import ContractProgress_FormLoad as CotractP_Views
# from ProcessSelection import ContractProgress_ProcessSelection as CotractP_Selection
from ProcessSelection import Doctype
# from GetDataFromDB import Print_GST_Invoice_GetDataFromDB as Print_GST_Invoice_Views
# from GetDataFromDB import Print_Export_GST_Invoice_GetDataFromDB as Print_Export_GST_Invoice_Views
# from FormLoad import PrintPalleteGatePass_FormLoad as PPGPviews
# from GetDataFromDB import PrintPalleteGatePass_GetDataFromDB as PrintPalleteGatePass_Views
# from GetDataFromDB import PrintPalleteGatePassPMC_GetDataFromDB as PrintPalleteGatePassPMC_Views
# from FormLoad import PackingMaterialLedger_FormLoad as PMLviews
# from ProcessSelection import PackingMaterialLedger_ProcessSelection as PackingMaterialLedger_Views
# from FormLoad import RawMaterialStock_FormLoad as RAWview
# from FormLoad import IndentRequisition_FormLoad as IRQviews
# from GetDataFromDB import IndentRequisition_GetDataFromDB as IndentRequisition_Views
# from FormLoad import Export_Invoice_FormLoad as ExportInvoiceviews
# from ProcessSelection import Export_Invoice_ProcessSelection as ExportInvoice_Views
# from FormLoad import PrintProformaInv_Formload as PrintProformaInv_Views
# from ProcessSelection import PrintProformaInv_ProcessSelection as PrintProfInv
# from FormLoad import ItemRate_FormLoad as ItmViews
# from GetDataFromDB import ItemRate_GetFromDB as ItmRate
# from FormLoad import PackingRegister_FormLoad as Packingviews
# from ProcessSelection import  PackingRegister_ProcessSelection as PackingRegister_Views
# from FormLoad import ProductLedger_FormLoad as PLviews
# from FormLoad import DailyGeneralReport_FormLoad as DGRviews
# from ProcessSelection import DailyGeneralReport_ProcessSelection
# from FormLoad import StoreRegister_FormLoad as Storeviews
# from ProcessSelection import StoreRegister_ProcessSelection as StoreRegiter_Views
# from GetDataFromDB import StoreRegister_GetDataFromDB as StoreRegister_Views
# from FormLoad import PrintGoodsReceiptNote_FormLoad as PGRN_Views
# from GetDataFromDB import PrintGoodsReceiptNote_GetDataFromDB as PrintGoodsGetData
# from FormLoad import PrintIssueSlip_FormLoad as PIS_Views
# from GetDataFromDB import PrintIssueSlip_GetDataFromDB as PrintIssueSlipGetData
# from FormLoad import ProductionAnalysis_Formload as PrdnFormLd
# from ProcessSelection import ProductionAnalysis_ProcessSelection as Prdn_Selection
# from FormLoad import BrokerWiseOrderOS_FormLoad
# from FormLoad import OSMoreThanDays_FormLoad
# from FormLoad import BrokerGroupCompanyWiseOS_FormLoad as BrokerGrpviews
# from ProcessSelection import BrokerGroupCompanyWiseOS_ProcessSelection as BrokerGrp_Views
# from ProcessSelection import BrokerWiseOrderOS_ProcessSelection as BWOOSviews
# from ProcessSelection import OSMoreThanDays_ProcessSelection as OMD_Views
# from ProcessSelection import DIspatchDetail_ProcessSelection as DispatchDetail_Views
# from FormLoad import DIspatchDetail_FormLoad as DispatchDetailviews
# from FormLoad import Diposite_Transaction_FormLoad as Depositview
# from ProcessSelection import DepositeTransaction_AgentWise_ProcessSelection as DepositsAgentwise_Views
# from FormLoad import ProductionProcessMis as Pmis
# from FormLoad import Diposite_Transaction_FormLoad as Depositview
# from ProcessSelection import DepositeTransaction_AgentWise_ProcessSelection as DepositsAgentwise_Views
# from FormLoad import Diposite_Transaction_Bank_Company_Collection_FormLoad as DepositeBankCompanyCollectionview
# from ProcessSelection import DepositeTransaction_BankWise_Company_Collection_ProcessSelection as DepositsBankCompanyCollection_Views
# from FormLoad import Diposite_Transaction_AgentWise_cheque_Collection_FormLoad as DepositeAgentWsieChequeCollectionview
# from ProcessSelection import DepositeTransaction_AgentWise_Cheque_Collection_ProcessSelection as DepositeAgentWiseChequeCollection_Views
# from FormLoad import ChequeDetailTab_FormLoad
# from FormLoad import BrokerWiseRD_FormLoad as BWRD
# from ProcessSelection import BrokerWiseRD_ProcessSelection as BWRDPr
# from FormLoad import ProductionSummary_FormLoad as PSumm_Views
# from ProcessSelection import ProductionSummary_ProcessSelection as Prodn_PS
# from FormLoad import StoresRequisition_FormLoad as SRQviews
# from GetDataFromDB import StoresRequisition_GetDataFromDB as StoresRequisition_Views
# from FormLoad import ContractsPendingMis_FormLoad as CPMIS
# from ProcessSelection import ContractPendingMisView as PCPV
# from FormLoad import ContractPending_FormLoad as CPview
# from FormLoad import ContractPending_AgentWise as CPAview
# from FormLoad import AgentLiftingDetailsFormLoad as AgntFld
# from ProcessSelection import AgentLiftingDetailsProcessSelection as AgntPro
# from FormLoad import ContractListMis_FormLoad as ContList
# from FormLoad import Liftingsummary as LSumm
# from ProcessSelection import MISBrokerWiseOS_SI_InvoiceDetails_ProcessSelection as MISBrokerWiseOS_SI_InvoiceDetails_Views
# from ProcessSelection import AgentWiseCollection_MIS_ProcessSelection  as AgentWiseCollectionMISSviews
# from FormLoad import DGGainLoss_Formload as DGG_Views
# from ProcessSelection import DGGainLoss_ProcessSelection as DGGainLoss
# from FormLoad import Challan_Register_Customer_FormLoad as ChallanRegisterCustomerviews
# from ProcessSelection import Challan_Register_Customer_ProcessSelection as ChallanRegisterCustomer_Views
# from FormLoad import POYStock_FormLoad
# from ProcessSelection import POYStock_ProcessSelection as POYSPS
# from FormLoad import GainLoss_FormLoad as gainLoss
# from ProcessSelection import GainLossReport_ProcessSelection as gainnLossR
# from FormLoad import MachineWiseProduction_Formload as MWPr_F
# from ProcessSelection import MachineWiseProduction_ProcessSelection as MWPr_PS
# from FormLoad import PurchaseItemWiseDetail_FormLoad as PIWDFL
# from ProcessSelection import PurchaseItemWiseDetail_ProcessSelection as PIWDPS
# from FormLoad import PurchaseMoreThanDays_FormLoad as PMTDFL
# from ProcessSelection import PurchaseMoreThanAmount_ProcessSelection as PMTAPS
# from FormLoad import StockLedger_FormLoad as SLFL
# from ProcessSelection import StockLedger_ProcessSelection as SLPS
# from Templates import StockLedgerItemLoad
from FormLoad import SalesOrder_FormLoad as SOFL
from ProcessSelection import SalesOrder_ProcessSelection as SOPS
from FormLoad import AdhocLedgerU_FormLOad
from ProcessSelection import AdhocLedgerU_ProcessSelection
from FormLoad import ExciseRegister_FormLoad as ERFL
urlpatterns = [
    path('', views.home, name='home'),
#     path('AdhocLedger.html', AHLviews.AdhocLedger, name="AdhocLedger"),
#     path('AdhocLedgerSummary', AHLviews.AdhocLedgerSummary, name="AdhocLedgerSummary"),
#     path('AdhocLedgerDetail', AdhocLedger_Views.AdhocLedgerDetail, name="AdhocLedgerDetail"),
    path('Doctype',Doctype.Doctype,name="Doctype"),
#     path('SalesDocumentItemGST',MISBrokerWiseOS_SI_InvoiceDetails_Views.ItemGST,name="ItemGST"),
#     path('BankCashStatement.html', BCSviews.BankCashStatementHtml,name="BankCashStatementHtml"),
#     path('BankCashStatement', BankCashStatement_View.BankCashStatement, name='BankCashStatement'),
#     path('GSTRegister.html', GSTviews.GSTRegisterHtml, name="GSTRegisterHtml"),
#     path('GSTRegister', GSTRegister_Views.GSTRegister, name="GSTRegister"),
    # path('BrokerWiseOS.html', MBWOSviews.BrokerWiseOS, name="BrokerWiseOS"),
    # path('BrokerWiseOSUpto15.html', MISBrokerWiseOS_Views.BrokerWiseOSDetail, name="BrokerWiseOSDetail"),
    # path('BrokerWiseOSRange16.html', MISBrokerWiseOS_Views.BrokerWiseOSDetail, name="BrokerWiseOSDetail"),
    # path('BrokerWiseOSOver30.html', MISBrokerWiseOS_Views.BrokerWiseOSDetail, name="BrokerWiseOSDetail"),
    # path('BrokerWiseOSDnAmt.html', MISBrokerWiseOS_Views.BrokerWiseOSDetail, name="BrokerWiseOSDetail"),
    # path('BrokerWiseOSUnbilled.html', MISBrokerWiseOS_Views.BrokerWiseOSDetail, name="BrokerWiseOSDetail"),
    # path('BrokerWiseOSAdvance.html', MISBrokerWiseOS_Views.BrokerWiseOSDetail, name="BrokerWiseOSDetail"),
    # path('BrokerWiseOSUnAdj.html', MISBrokerWiseOS_Views.BrokerWiseOSDetail, name="BrokerWiseOSDetail"),
    # path('BrokerWiseOSOdDay.html', MISBrokerWiseOS_Views.BrokerWiseOSDetail, name="BrokerWiseOSDetail"),
    # path('BrokerWiseOSUpdateYear',MBWOSviews.updateYear,name="updateYear"),
#     path('ChallanRegister.html', CRviews.challanregisterhtml,name="Challanregisterhtml"),
#     path('ChallanRegister',ChallanRegister_View.ChallanRegister,name="ChallanRegister"),
#     path('CompanyWiseOS.html', MCWOSviews.CompanyWiseOS, name="CompanyWiseOS"),
#     path('DespatchInstructionRegister.html', DIRviews.DespatchInstructionRegisterHtml,name='DespatchInstructionRegisterHtml'),
#     path('DespatchInstructionRegister', DespatchInstructionRegister_View.DespatchInstructionRegister,name='DespatchInstructionRegister'),
#     path('PendingDespatchInstruction.html', DIRviews.PendingDespatchInstructionHtml,name='PendingDespatchInstructionHtml'),
#     path('MRNRegister.html', MRNviews.MRNRegisterHtml, name="MRNRegisterHtml"),
#     path('MRNRegister', MRNRegister_Views.MRNRegister, name="MRNRegister"),
#     path('OnlineBankBalance.html', OBBviews.OnlineBankBalanceHtml, name="OnlineBankBalanceHtml"),
#     path('OnlineBankBalance', OBBviews.OnlineBankBalanceSummary, name="OnlineBankBalanceSummary"),
#     path('PendingPurchaseRegister.html', PPRviews.PendingPurchaseRegisterHtml, name="PendingPurchaseRegisterHtml"),
#     path('PendingPurchaseRegister', PendingPurchaseRegister_View.PendingPurchaseRegister, name="PendingPurchaseRegister"),
    # path('PrintChallan.html', PYCviews.PrintChallanHtml, name="PrintChallanHtml"),
    # path('PrintChallanTable', PYCviews.PrintChallanTableHtml, name="PrintChallanTableHtml"),
#     path('PrintChallanPDF', PrintYarnChallan_Views.PrintChallanPDF, name="PrintChallanPDF"),
#     path('PrintChallanRule55PDF', PrintChallanRule55_Views.PrintChallan_Rule55_PDF, name="PrintChallan_Rule55_PDF"),
#     path('PrintChallanBoxNoWisePDF', PrintChallanBoxNoWise_Views.PrintChallanBoxNoWise_PDF,name="PrintChallanBoxNoWise_PDF"),
#     path('YarnIssueRegister.html',YIRviews.YarnIssueRegisterHtml,name='YarnIssueRegisterHtml' ),
#     path('YarnIssueRegister',YarnIssueRegister_View.YarnIssueRegister,name='YarnIssueRegister' ),
#     path('AdhocLedgerPDF.html', AdhocViews.AdhocLedgerHtml, name="AdhocLedger"),
#     path('AdhocLedger',AdhocPro.AdhocLedger,name='AdhocLedger' ),
#     path('PurchaseRegister.html', PRviews.PurchaseRegisterHtml, name="PurchaseRegisterHtml"),
#     path('PurchaseRegister',PurchaseRegister_Views.PurchaseRegister,name="PurchaseRegister"),
#     path('SalesRegister.html', SRviews.SalesRegisterHtml, name="SalesRegisterHtml"),
#     path('SalesRegister',SalesRegister_View.SalesRegister,name="SalesRegister"),
#     path('Store_Unbilled_GRN.html',SUGviews.StoreUnBilled_GRNRegisterHtml,name="StoreUnBilled_GRNRegisterHtml"),
#     path('UnBilledGRNRegister', Store_Unbilled_GRN_View.UnBilled_GRN_Register,name="UnBilled_GRN_Register"),
#     path('SummerizedBankBalance.html', SBBviews.SummerizedBankBalanceHtml, name="SummerizedBankBalanceHtml"),
#     path('SummerizedBankBalance', SummerizedBankBalance_Views.SummerizedBankBalance, name="SummerizedBankBalance"),
#     path('BrokerwiseChallanList.html',BWCLviews.BrokerWiseChallanListHtml,name="BrokerWiseChallanListHtml"),
#     path('BrokerWiseChallanList',BrokerWiseChallanList_View.BrokerWiseChallanList,name="BrokerWiseChallanList"),
#     path('PrintDespatchInstruction.html',PDIviews.PrintDespatchInstructionHtml, name="PrintDespatchInstructionHtml"),
#     path('PrintDespatchInstructionTable', PDI_PS.PrintDespatch_PrintPDF, name="PrintDespatch_PrintPDF"),
#     path('PrintDespatchPDF',PrintDespatchInstruction_Views.PrintDespatchPDF, name="PrintDespatchPDF"),
#     path('PrintDespatchWithoutRDPDF',PrintDespatchInstruction_WithoutRD_Views.PrintDespatch_WithoutRD_PDF, name="PrintDespatch_WithoutRD_PDF"),
#     path('DespatchReportPDF', DespatchReport_Views.DespatchReportPDF, name="DespatchReportPDF"),
#     path('LotNoListing.html', Lotviews.LotNoListingHtml, name="LotNoListingHtml"),
#     path('LotNoListing', Lot_Views.LotNoListing, name="LotNoListing"),
#     path('hedStockInHand.html', FSIH_Views.FinishedStockInHandHTML, name='FinishedStockInHandHTML'),
    # path('FiFinisnishedStockInHand', FSIH_PS.FinishedStockInHand, name='FinishedStockInHand'),
    # path('PackingReports.html', PackR_Views.PackingReportHtml, name='PackingReportHtml'),
#     path('PackingReport', PackR_PS.PackingReport, name='PackingReport'),
#     path('PrintChallanAdvice.html', PCA_Views.PrintChallanAdviceHTML, name='PrintChallanAdviceHTML'),
#     path('PrintChallanAdviceTable', PCA_Views.PrintChallanAdviceTableHTML, name='PrintChallanAdviceTableHTML'),
#     path('PrintChallanAdvice_PDF', PrintChallanAdvGetData.PrintChallanAdvice_PDF, name='PrintChallanAdvice_PDF'),
#     path('PurchaseOrder.html', POrder_Views.PurchaseOrderHtml, name='PurchaseOrderHtml'),
#     path('PurchaseOrder', POrder_Views.PurchaseOrderTableHtml, name='PurchaseOrderTableHtml'),
#     path('PurchaseOrder_PDF', POrder.PurchaseOrder_PDF, name='PurchaseOrder_PDF'),path('FinishedStock.html',FSview.FinishedStockHtml,name="FinishedStockHtml"),
    path('FinishedStock.html', FSview.FinishedStockHtml, name="FinishedStockHtml"),
    path('FinishedStock.html', FSview.FinishedStockHtml, name="FinishedStockHtml"),
    path('FinishedStock_Apply', FSAview.Apply, name="Apply"),
    path('FinishedStock_ItemDetail_ClosingQty', FSDview.FinishedStock_ItemDetail_ClosingQty,
         name="FinishedStock_ItemDetail_ClosingQty"),
    path('FinishedStock_ItemDetail_OrdPendQty', FSDview.FinishedStock_ItemDetail_OrdPendQty,
         name="FinishedStock_ItemDetail_OrdPendQty"),
#     path('PrintChallanBoxNoWiseInternalPDF', PrintChallanInternal_Views.PrintChallanBoxNoWiseInternalPDF,name="PrintChallanBoxNoWiseInternalPDF"),
#     path('BrokerGroupCompanyWiseOS.html', BrokerGrpviews.BrokerGroupCompanyWiseOShtml, name="BrokerGroupCompanyWiseOShtml"),
#     path('BrokerGroupCompanyWiseOS', BrokerGrp_Views.BrokerGroupCompanyWiseOS, name="BrokerGroupCompanyWiseOS"),
    # path('ContractProgress.html', CotractP_Views.ContractProgressHTML, name='ContractProgressHTML'),
    # path('ContractProgress', CotractP_Selection.ContractProgress, name='ContractProgress'),
#     path('PrintChallan_GST_Invoice_PDF', Print_GST_Invoice_Views.PrintChallan_GST_Invoice_PDF,
#          name="PrintChallan_GST_Invoice_PDF"),
#     path('PrintChallan_Export_GST_Invoice_PDF', Print_Export_GST_Invoice_Views.PrintChallan_Export_GST_Invoice_PDF,
#          name="PrintChallan_Export_GST_Invoice_PDF"),
#     path('PrintPalleteGatePass.html',PPGPviews.PrintPalleteGatePassHtml,name="PrintPalleteGatePassHtml"),
#     path('PrintPalleteGatePassTable',PPGPviews.PrintPalleteGatePassTableHtml,name="PrintPalleteGatePassTableHtml"),
#     path('PrintPalleteGatePassPDF',PrintPalleteGatePass_Views.PrintPalleteGatePassPDF,name="PrintPalleteGatePassPDF"),
#     path('PrintPalleteGatePassPDFPMC',PrintPalleteGatePassPMC_Views.PrintPalleteGatePassPDFPMC,name="PrintPalleteGatePassPDFPMC"),
#     path('PackingMaterialLedger.html', PMLviews.PackingMaterialLedger, name="PackingMaterialLedger"),
#     path('PackingMaterialLedger',PackingMaterialLedger_Views.PackingMaterialLedger,name="PackingMaterialLedger"),
#     path('RawMaterialStock.html',RAWview.RawMaterialStockHTML,name="RawMaterialStockHTML"),
#     path('RawMaterialStock_ItemDetail',RAWview.RawMaterialStock_ItemDetail,name="RawMaterialStock_ItemDetail"),
#     path('RawMaterialStock_LotDetail',RAWview.RawMaterialStock_LotDetail,name="RawMaterialStock_LotDetail"),
#     path('IndentRequisition.html',IRQviews.IndentRequisitionHtml,name="IndentRequisitionHtml"),
#     path('IndentRequisitionTable',IRQviews.IndentRequisitionTableHtml,name="IndentRequisitionTableHtml"),
#     path('IndentRequisitionPDF',IndentRequisition_Views.IndentRequisitionPDF,name="IndentRequisitionPDF"),
#     path('Export_Invoice.html',ExportInvoiceviews.Export_InvoiceHtml,name="Export_InvoiceHtml"),
#     path('Export_InvoiceRegister',ExportInvoice_Views.Export_InvoiceRegister,name="Export_InvoiceRegister"),
#     path('PrintProformaInv.html', PrintProformaInv_Views.PrintProformaInvHtml, name='PrintProformaInvHtml'),
#     path('PrintProformaInvGrid', PrintProformaInv_Views.PrintProformaInvGrid, name='PrintProformaInvGrid'),
#     path('PrintProformaInv_PDF', PrintProfInv.PrintProformaInv_PDF, name='PrintProformaInv_PDF'),
#     path('PackingListPreShipProforma_PDF', PrintProfInv.PackingListPreShipProforma_PDF, name='PackingListPreShipProforma_PDF'),
#     path('PreCustom_PDF', PrintProfInv.PreCustom_PDF, name='PreCustom_PDF'),
#     path('Commercial_PDF', PrintProfInv.Commercial_PDF, name='Commercial_PDF'),
#     path('BLInstruction_PDF', PrintProfInv.BLInstruction_PDF, name='BLInstruction_PDF'),
#     path('Annex_PDF', PrintProfInv.Annex_PDF, name='Annex_PDF'),
#     path('Certificate_PDF', PrintProfInv.Certificate_PDF, name='Certificate_PDF'),
#     path('ItemRate.html',ItmViews.ItemRateHtml,name="ItemRateHtml"),
#     path('ItemRate',ItmViews.ItemRate,name="ItemRate"),
#     path('ItemRate_PDF',ItmRate.ItemRate_PDF,name="ItemRate_PDF"),
#     path('PackingRegister.html',Packingviews.PackingRegisterHtml,name="PackingRegisterHtml"),
#     path('PackingRegister',PackingRegister_Views.PackingRegister,name="PackingRegister"),
    # path('ProductLedger.html', PLviews.ProductLedger, name="ProductLedger"),
    # path('ProductLedgerSummary', PLviews.ProductLedgerSummary, name="ProductLedgerSummary"),
    # path('ProductLedgerDetail', PLviews.ProductLedgerDetail, name="ProductLedgerDetail"),
#     path('DailyGeneralReport.html', DGRviews.DailyGeneralReport, name="DailyGeneralReport"),
#     path('DailyGeneralReport', DailyGeneralReport_ProcessSelection.DailyGeneralReport, name="DailyGeneralReport"),
#     path('StoreRegister.html',Storeviews.StoreRegisterHtml,name="StoreRegisterHtml"),
#     path('StoreRegister',StoreRegiter_Views.StoreRegister,name="StoreRegister"),
#     path('StoreRegisterPrintPDF',StoreRegister_Views.StoreRegisterPrintPDF,name="StoreRegisterPrintPDF"),
#     path('ProductionAnalysis.html', PrdnFormLd.ProductionAnalysisHtml, name='ProductionAnalysisHtml'),
#     path('ProductionAnalysis', Prdn_Selection.ProductionAnalysis, name='ProductionAnalysis'),
#     path('BrokerWiseOrderOS.html', BrokerWiseOrderOS_FormLoad.BrokerWiseOrderOS, name="BrokerWiseOrderOS"),
#     path('OSMoreThanDays.html', OSMoreThanDays_FormLoad.OSMoreThanDays, name="OSMoreThanDays"),
#     path('BrokerGroupCompanyWiseOS.html', BrokerGrpviews.BrokerGroupCompanyWiseOShtml, name="BrokerGroupCompanyWiseOShtml"),
#     path('BrokerGroupCompanyWiseOS', BrokerGrp_Views.BrokerGroupCompanyWiseOS, name="BrokerGroupCompanyWiseOS"),
#     path('BrokerWiseOrderOS', BWOOSviews.BrokerWiseOrderOS, name="BrokerWiseOrderOS"),
#     path('OSMoreThanDays', OMD_Views.OSMoreThanDays, name="OSMoreThanDays"),
#     path('DispatchDetailRegister.html',DispatchDetailviews.DispatchDetail,name='DispatchDetails'),
#     path('DispatchDetail',DispatchDetail_Views.DispatchDetails,name="DispatchDetails"),
#     path('DispatchDetailList',DispatchDetail_Views.DespatchDetailItemList,name="DespatchDetailItemList"),
#     path('DespatchDetailLine',DispatchDetail_Views.DespatchDetailLine,name="DespatchDetailLine"),
#     path('Diposits_Transaction.html', Depositview.DepositsTransaction, name="DepositsTransaction"),
#     path('DepositeTransactionRegister', DepositsAgentwise_Views.DepositeTransactionRegister,name='DepositeTransactionRegister'),
#     path('ProductionProccessitm.html', Pmis.Production, name='Production'),
#     path('ProccessWisefunctions', Pmis.ProccessWisefunctions, name='ProccessWisefunctions'),
#     path('ItemMachinefunctions', Pmis.ItemWisefunction, name='ItemWisefunction'),
#     path('MachineWisefunctions', Pmis.MachineWisefunction, name='MachineWisefunction'),
#     path('Diposits_Transaction.html', Depositview.DepositsTransaction, name="DepositsTransaction"),
#     path('DepositeTransactionRegister', DepositsAgentwise_Views.DepositeTransactionRegister, name='DepositeTransactionRegister'),
#     path('Diposits_Transaction_Bank_Company_Collection.html', DepositeBankCompanyCollectionview.DepositsTransactionBankCompanyCollection, name="DepositsTransactionBankCompanyCollection"),
#     path('DepositeTransactionBankCompanyCollectionRegister', DepositsBankCompanyCollection_Views.DepositeTransactionBankCompanyCollectionRegister, name='DepositeTransactionBankCompanyCollectionRegister'),
#     path('Diposits_Transaction_AgentWise_Cheque_Register.html',  DepositeAgentWsieChequeCollectionview.DepositsTransactionAgentWiseChequeCollection, name='DepositsTransactionAgentWiseChequeCollection'),
#     path('DepositeTransactionAgentChequeCollectionRegister',  DepositeAgentWiseChequeCollection_Views.DepositeTransactionAgentChequeCollectionRegister,  name='DepositeTransactionAgentChequeCollectionRegister'),
#     path('BrokerWiseOSUnadjustedChequeDetail', ChequeDetailTab_FormLoad.ChequeDetailTab, name="ChequeDetailTab"),
#     path('BrokerWiseRD.html', BWRD.BrokerWiseRD, name='BrokerWiseRD'),
#     path('BrokerWiseRD', BWRDPr.BrokerWiseRD, name='BrokerWiseRD'),
#     path('PrintGoodsReceiptNote.html', PGRN_Views.PrintGoodsReceiptNoteHtml, name='PrintGoodsReceiptNoteHtml'),
#     path('PrintGoodsReceiptNote_table', PGRN_Views.PrintGoodsReceipt, name='PrintGoodsReceipt'),
#     path('PrintGoodsReceiptNote_PDF', PrintGoodsGetData.PrintGoodsReceiptNote_PDF, name="PrintGoodsReceiptNote_PDF"),
#     path('PrintIssueSlip.html', PIS_Views.PrintIssueSlipHtml, name='PrintIssueSlipHtml'),
#     path('PrintIssueSlip_table', PIS_Views.PrintIssueSlip, name='PrintIssueSlip'),
#     path('PrintIssueSlip_PDF', PrintIssueSlipGetData.PrintIssueSlip_PDF, name="PrintIssueSlip_PDF"),
#     path('ProductionSummary.html', PSumm_Views.ProductionSummaryHtml, name='ProductionSummaryHtml'),
#     path('ProductionSummary', Prodn_PS.ProductionSummary, name='ProductionSummary'),
#     path('StoresRequisition.html', SRQviews.StoresRequisitionHtml, name="StoresRequisitionHtml"),
#     path('StoresRequisitionTable', SRQviews.StoresRequisitionTableHtml, name="StoresRequisitionTableHtml"),
#     path('StoresRequisitionPDF', StoresRequisition_Views.StoresRequisitionPDF, name="StoresRequisitionPDF"),
#     path('ContractsPendingMis.html', CPMIS.ContractsPendingMis, name='ContractsPendingMis'),
#     path('AgentWisefunctions', CPMIS.AgentWisefunctions, name='AgentWisefunctions'),
#     path('ContractPendingMisView.html', PCPV.ContractPendingMisView, name='ContractPendingMisView'),
#     path('ContractPending.html',CPview.ContractPending_ItemGroup,name="ContractPending_ItemGroup"),
#     path('ContractPending_Item',CPview.ContractPending_ItemDetail,name="ContractPending_ItemDetail"),
#     path('ContractPending_ItemDetail',CPview.ContractPending_ItemDetail,name="ContractPending_ItemDetail"),
#     path('ContractPending_ItemSubDetail',CPview.ContractPending_ItemSubDetail,name="ContractPending_ItemSubDetail"),
#     path('ContractPending_ApplyType',CPview.ContractPending_ApplyType,name="ContractPending_ApplyType"),
#     path('ContractPending_AgentApplyType',CPAview.ContractPending_ApplyType,name="ContractPending_ApplyType"),
#     path('ContractPending_AgentWise',CPAview.ContractPending_AgentWise,name="ContractPending_AgentWise"),
#     path('ContractPending_AgentItemDetail',CPAview.ContractPending_AgentItemDetail,name="ContractPending_AgentItemDetail"),
#     path('ContractPending_AgentItemSubDetail',CPAview.ContractPending_AgentItemSubDetail,name="ContractPending_AgentItemSubDetail"),
#     path('AgentLiftingDetails.html', AgntFld.AgentLiftingHTML,name='AgentLiftingHTML'),
#     path('AgentLifting', AgntPro.AgentLifting,name='AgentLifting'),
#     path('ContractListMis.html', ContList.ContractListMis,name='ContractListMis'),
#     path('ContListItemWisefunctions', ContList.ContListItemWisefunctions,name='ContListItemWisefunctions'),
#     path('ContListAgentWisefunctions', ContList.ContListAgentWisefunctions,name='ContListAgentWisefunctions'),
#     path('LiftingSummary.html', LSumm.LiftingngSummarytMis, name='LiftingngSummarytMis'),
#     path('LiftingSummaryProcessSummFunction', LSumm.LiftingSummaryProcessSummFunction, name='LiftingSummaryProcessSummFunction'),
#     path('LiftingSummaryDetailsMis', LSumm.LiftingSummaryDetailsMis, name='LiftingSummaryDetailsMis'),
#     path('AgentWiseCollection_MIS.html', AgentWiseCollectionMISSviews.AgentWiseCollectionMIS,
#          name='AgentWiseCollectionMIS'),
#     path('AgentWiseCollectionMIS', AgentWiseCollectionMISSviews.AgentWiseCollectionMIS, name='AgentWiseCollectionMIS'),
#     path('FinishedStockInHandAgeing.html', FSIH_Views.FinishedStockInHandAgeingHTML, name='FinishedStockInHandAgeingHTML'),
#     path('FinishedStockInHandAgeing', FSIH_A.FinishedStockInHandAgeing, name='FinishedStockInHandAgeing'),
    # path('FinishedStockInHand.html', FSIH_Views.FinishedStockInHandHTML, name='FinishedStockInHandHTML'),
    # path('FinishedStockInHand', FSIH_PS.FinishedStockInHand, name='FinishedStockInHand'),
#     path('DGGainLoss.html', DGG_Views.DGGainLossHtml, name='DGGainLossHtml'),
#     path('DGGainLoss', DGGainLoss.DGGainLoss, name='DGGainLoss'),
#     path('Challan_Register_Customer.html', ChallanRegisterCustomerviews.ChallanRegisterCustomer,
#          name='ChallanRegisterCustomer'),
#     path('ChallanRegisterCustomer_Purchase', ChallanRegisterCustomer_Views.ChallanRegisterCustomer_Purchase,
#          name='ChallanRegisterCustomer_Purchase'),
    # path('POYStock.html', POYStock_FormLoad.POYStock, name="POYStock"),
    # path('POYStock', POYSPS.POYStock, name="POYStock"),
#     path('GainLossReport.html', gainLoss.GainLossHtml, name='GainLossHtml'),
#     path('GainLoss', gainnLossR.GainLoss, name='GainLoss'),
#     path('MachineWiseProduction.html', MWPr_F.MachineWiseProductionHtml, name='MachineWiseProductionHtml'),
#     path('MachineWiseProduction', MWPr_PS.MachineWiseProduction, name='MachineWiseProduction'),
#     path('PurchaseItemWiseDetail.html',PIWDFL.PurchaseItemWiseDetailHtml,name='PurchaseItemWiseDetailHtml'),
#     path('PurchaseItemWiseDetail',PIWDPS.PurchaseItemWiseDetail,name='PurchaseItemWiseDetail'),
#     path('PurchaseItemWiseSummary.html',PIWDFL.PurchaseItemWiseSummaryHtml,name='PurchaseItemWiseSummaryHtml'),
# 	path('PurchaseItemWiseSummary',PIWDPS.PurchaseItemWiseSummary,name='PurchaseItemWiseSummary'),
# path(
#         "PurchaseMoreThanDays.html",
#         PMTDFL.PurchaseMoreThanDaysHtml,
#         name="PurchaseMoreThanDaysHtml",
#     ),
#     path(
#         "PurchaseMoreThanAmount",
#         PMTAPS.PurchaseMoreThanAmount,
#         name="PurchaseMoreThanAmount",
#     ),
#     path(
#         "StockLedger.html",
#         SLFL.StockLedgerHtml,
#         name="StockLedgerHtml",
#     ),
# path(
#         "StockLedger",
#         SLPS.StockLedger,
#         name="StockLedger",
#     ),
#     path('getItem', StockLedgerItemLoad.itemLoad,name="getItem"),
#     path('fetchItem', StockLedgerItemLoad.fetchItem,name="fetchItem"),
    path("SalesOrder.html",SOFL.SalesOrderHtml,name="SalesOrder.html"),
    path("SalesOrder",SOPS.SalesOrder,name="SalesOrder"),
    path("AdhocLedgerU.html",AdhocLedgerU_FormLOad.AdhocLedgerU,name="AdhocLedgerU"),
    path("AdhocLedgerU",AdhocLedgerU_ProcessSelection.adhocLedgerU_ProcessData,name="adhocLedgerU_ProcessData"),
    path("ExciseRegister.html",ERFL.ExciseRegister,name="ExciseRegister"),


]