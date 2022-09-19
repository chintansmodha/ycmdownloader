import os
from datetime import datetime
from django.shortcuts import render
from django.views.static import serve
import os.path
from Global_Files import Connection_String as con
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')
from babel.numbers import format_currency

TotalAmtExDhara = 0
TotalInvoiceAmout = 0


# function of intersection
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


# ****************************** Load Lifting Summary ***********************
def LiftingngSummarytMis(request):
    itemtypeOpt = str(request.GET.getlist('optionValue'))
    if len(itemtypeOpt) >4:
        itemtypeOpt = str(itemtypeOpt)[2:-2]
        itemtypeOptSelected = itemtypeOpt.replace("'","")
        if len(itemtypeOpt) == 32:
            itemtypeOptSelected = "0"
    else:
        itemtypeOptSelected = "0"
    return render(request, 'LiftingSummary.html',{'itemtypeOptSelected':itemtypeOptSelected,})


def LiftingSummaryProcessSummFunction(request):
    global TotalAmtExDhara , TotalInvoiceAmout
    GDataAgentHeaderGroup = []
    GDataAgentColumnGroup = []
    itemtypeOpt = str(request.GET.getlist('optionValue'))
    # itemtypeOptSelected = str(request.GET.getlist('optionValue'))
    print(len(itemtypeOpt))
    if len(itemtypeOpt) >4:
        itemtypeOpt = str(itemtypeOpt)[2:-2]
        itemtypeOptSelected = itemtypeOpt.replace("'","")
        itemtypeOpt = " And PIL.ITEMTYPECODE in ( " + itemtypeOpt + ") "
        if len(itemtypeOpt) == 32:
            itemtypeOpt = " "
            itemtypeOptSelected = "0"
    else:
        itemtypeOpt = " "
        itemtypeOptSelected = "0"
    # print(itemtypeOpt)
    StartDate =  str(request.GET['startdate'])
    EndDate = str(request.GET['enddate'])

    syear = StartDate[0:4]
    smonth = StartDate[5:7]
    sday = StartDate[8:10]

    eyear = EndDate[0:4]
    emonth = EndDate[5:7]
    eday = EndDate[8:10]

    StartDate = "'" + str(StartDate)[0:-1] + "'"
    EndDate = "'" + str(EndDate)[0:10] + "'"
    # print(StartDate,EndDate)
    #   ############# COLUMMN TYPE QUERY ###############
    sql = "Select          '' As Broker " \
          ", Cast(Sum(Round(PI.GROSSVALUE,0)) As Decimal(30,2)) As TotalInvoiceAmout " \
          ", 0 As POYQnty " \
          ", 0 As FDYQnty " \
          ", 0 As MOYQnty " \
          ", 0 As MONQnty " \
          ", 0 As DTYQnty " \
          ", 0 As ATYQnty " \
          ", 0 As TWDQnty " \
          ", 0 As BCFQnty " \
          ", 0 As CABQnty " \
          ", 0 As HSTQnty " \
          ", 0 As PLYQnty " \
          ", 0 As POYAmt " \
          ", 0 As FDYAmt " \
          ", 0 As MOYAmt " \
          ", 0 As MONAmt " \
          ", 0 As DTYAmt " \
          ", 0 As ATYAmt " \
          ", 0 As TWDAmt " \
          ", 0 As BCFAmt " \
          ", 0 As CABAmt " \
          ", 0 As HSTAmt " \
          ", 0 As PLYAmt " \
          "From PLANTINVOICE PI " \
          "jOIN SALESDOCUMENT SD                   ON      PI.code = SD.DEFINITIVECODE " \
          "Where   PI.INVOICEDATE Between "+StartDate+" And "+EndDate+" " \
          "And Sd.DOCUMENTTYPETYPE = '06' " \
          "And PI.code In " \
          "(Select PIL.PLANTINVOICECODE " \
          "From PLANTINVOICELINE PIL " \
          "Where PIL.ITEMTYPECODE in ('POY', 'FDY', 'MOY', 'MON', 'DTY', 'ATY', 'TWD', 'BCF', 'CAB', 'HST', 'PLY') "+itemtypeOpt+" ) " \
          " Union All " \
          "Select          Coalesce(AGENT.LONGDESCRIPTION, 'Broker Name Not Entered') as Broker " \
          ", 0  As  TotalInvoiceAmout " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'POY' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As POYQnty " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'FDY' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As FDYQnty " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'MOY' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As MOYQnty " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'MON' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As MONQnty " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'DTY' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As DTYQnty " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'ATY' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As ATYQnty " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'TWD' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As TWDQnty " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'BCF' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As BCFQnty " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'CAB' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As CABQnty " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'HST' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As HSTQnty " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'PLY' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As PLYQnty " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'POY' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As POYAmt " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'FDY' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As FDYAmt " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'MOY' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As MOYAmt " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'MON' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As MONAmt " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'DTY' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As DTYAmt " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'ATY' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As ATYAmt " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'TWD' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As TWDAmt " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'BCF' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As BCFAmt " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'CAB' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As CABAmt " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'HST' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As HSTAmt " \
          ", Cast(Sum(Case When PIL.ITEMTYPECODE = 'PLY' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As PLYAmt " \
          "From PlantInvoice PI " \
          "Join PLANTINVOICELINE PIL               On      PI.CODE = PIL.PLANTINVOICECODE " \
          "jOIN SALESDOCUMENT SD                   ON      PI.code = SD.DEFINITIVECODE " \
          "Left Join AGENT                         On      SD.AGENT1CODE = Agent.code " \
          "Left Join INDTAXDETAIL invAmt                ON      PIL.ABSUNIQUEID = invAmt.ABSUNIQUEID " \
          "And     PIL.TAXTEMPLATECODE = invAmt.TAXTEMPLATECODE " \
          "And     PIL.TAXTEMPLATETEMPLATETYPE = invAmt.TAXTEMPLATETEMPLATETYPE " \
          "AND     invAmt.ITAXCODE = 'PPU' " \
          "Left Join    INDTAXDETAIL DharaAmt      ON      PIL.ABSUNIQUEID = DharaAmt.ABSUNIQUEID " \
          "And     DharaAmt.ITAXCODE = 'DRA' " \
          "And     DharaAmt.TAXCATEGORYCODE = 'OTH' " \
          "Where   PI.INVOICEDATE Between "+StartDate+" And "+EndDate+" " \
          "And PIL.ITEMTYPECODE in ('POY', 'FDY', 'MOY', 'MON', 'DTY', 'ATY', 'TWD', 'BCF', 'CAB', 'HST', 'PLY') " \
          "And Sd.DOCUMENTTYPETYPE = '06'  "+itemtypeOpt+" " \
          "Group   By   AGENT.LONGDESCRIPTION " \
          "Order   By   Broker "

    # Calculate total Quantity As Per Item Type
    POYQnty = 0
    FDYQnty = 0
    MOYQnty = 0
    MONQnty = 0
    DTYQnty = 0
    ATYQnty = 0
    TWDQnty = 0
    BCFQnty = 0
    CABQnty = 0
    HSTQnty = 0
    PLYQnty = 0
    TOTALQnty = 0

    # Calculate total amount As Per Item Type
    POYAmnt = 0
    FDYAmnt = 0
    MOYAmnt = 0
    MONAmnt = 0
    DTYAmnt = 0
    ATYAmnt = 0
    TWDAmnt = 0
    BCFAmnt = 0
    CABAmnt = 0
    HSTAmnt = 0
    PLYAmnt = 0
    TotalAmtExDhara = 0
    TotalInvoiceAmout = 0

    # stmt1 = con.db.prepare(con.conn, sql)
    # con.db.execute(stmt1)
    # result1 = con.db.fetch_both(stmt1)
    #
    # while result1 != False:
    #     # Calculate total amount As Per Item Type
    #     if str(result1['BROKER']) != '':
    #         AtyQnty += int(result1['ATYQNTY'])
    #         BcfQnty += int(result1['BCFQNTY'])
    #         CabQnty += int(result1['CABQNTY'])
    #         DtyQnty += int(result1['DTYQNTY'])
    #         FdyQnty += int(result1['FDYQNTY'])
    #         HSTQnty += int(result1['HSTQNTY'])
    #         MonQnty += int(result1['MONQNTY'])
    #         MoyQnty += int(result1['MOYQNTY'])
    #         PlyQnty += int(result1['PLYQNTY'])
    #         PoyQnty += int(result1['POYQNTY'])
    #         TwdQnty += int(result1['TWDQNTY'])
    #         TOTALQnty += int(result1['ATYQNTY']) + int(result1['BCFQNTY']) + int(result1['CABQNTY']) + \
    #                      int(result1['DTYQNTY']) + \
    #                      int(result1['HSTQNTY']) + int(result1['MONQNTY']) + int(result1['MOYQNTY']) + \
    #                      int(result1['PLYQNTY']) + int(result1['POYQNTY']) + int(result1['TWDQNTY'])
    #         # Calculate total amount As Per Item Type
    #         AtyAmnt += int(result1['ATYAMT'])
    #         BcfAmnt += int(result1['BCFAMT'])
    #         CabAmnt += int(result1['CABAMT'])
    #         DtyAmnt += int(result1['DTYAMT'])
    #         FdyAmnt += int(result1['FDYAMT'])
    #         HSTAmnt += int(result1['HSTAMT'])
    #         MonAmnt += int(result1['MONAMT'])
    #         MoyAmnt += int(result1['MOYAMT'])
    #         PlyAmnt += int(result1['PLYAMT'])
    #         PoyAmnt += int(result1['POYAMT'])
    #         TwdAmnt += int(result1['TWDAMT'])
    #         TotalAmtExDhara += int(result1['ATYAMT']) + int(result1['BCFAMT']) + int(result1['CABAMT']) + \
    #                            int(result1['DTYAMT']) + int(result1['FDYAMT']) + \
    #                            int(result1['HSTAMT']) + int(result1['MONAMT']) + int(result1['MOYAMT']) + \
    #                            int(result1['PLYAMT']) + int(result1['POYAMT']) + int(result1['TWDAMT'])
    #     else:
    #         TotalInvoiceAmout += float(result1['TOTALINVOICEAMOUT'])
    #     result1 = con.db.fetch_both(stmt1)


    # Calculate Average Rate in Process Summary Mis
    TOTALAvgRate = 0
    POYAvgRate = 0
    FDYAvgRate = 0
    MOYAvgRate = 0
    MONAvgRate = 0
    DTYAvgRate = 0
    ATYAvgRate = 0
    TWDAvgRate = 0
    BCFAvgRate = 0
    CABAvgRate = 0
    HSTAvgRate = 0
    PLYAvgRate = 0
    # if AtyQnty != 0:
    #     AtyAvgRate = AtyAmnt/AtyQnty
    # if BcfQnty != 0:
    #     BcfAvgRate = BcfAmnt/BcfQnty
    # if CabQnty != 0:
    #     CabAvgRate = CabAmnt/CabQnty
    # if DtyQnty != 0:
    #     DtyAvgRate = DtyAmnt/DtyQnty
    # if FdyQnty != 0:
    #     FdyAvgRate = FdyAmnt/FdyQnty
    # if HSTQnty != 0:
    #     HSTAvgRate = HSTAmnt/HSTQnty
    # if MonQnty != 0:
    #     MonAvgRate = MonAmnt/MonQnty
    # if MoyQnty != 0:
    #     MoyAvgRate = MoyAmnt/MoyQnty
    # if PlyQnty != 0:
    #     PlyAvgRate = PlyAmnt/PlyQnty
    # if PoyQnty != 0:
    #     PoyAvgRate = PoyAmnt/PoyQnty
    # if TwdQnty != 0:
    #     TwdAvgRate = TwdAmnt/TwdQnty
    # if TOTALQnty != 0:
    #     TOTALAvgRate = TotalAmtExDhara/TOTALQnty
    # print(TwdAmnt, TwdQnty, TwdAvgRate)
    refHeader=['POY', 'FDY', 'MOY', 'MON', 'DTY', 'ATY', 'TWD', 'BCF', 'CAB', 'HST', 'PLY']
    columnHeader = []
    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    # print(result)
    while result != False:
        if str(result['BROKER']) != '':
            if int(result['ATYQNTY']) != 0 :
                if 'ATY' not in columnHeader :
                    columnHeader.append('ATY')
            if int(result['BCFQNTY']) != 0 :
                if 'BCF' not in columnHeader :
                    columnHeader.append('BCF')
            if int(result['CABQNTY']) != 0:
                if 'CAB' not in columnHeader:
                    columnHeader.append('CAB')
            if int(result['DTYQNTY']) != 0:
                if 'DTY' not in columnHeader:
                    columnHeader.append('DTY')
            if int(result['FDYQNTY']) != 0:
                if 'FDY' not in columnHeader:
                    columnHeader.append('FDY')
            if int(result['HSTQNTY']) != 0:
                if 'HST' not in columnHeader:
                    columnHeader.append('HST')
            if int(result['MONQNTY']) != 0:
                if 'MON' not in columnHeader:
                    columnHeader.append('MON')
            if int(result['MOYQNTY']) != 0:
                if 'MOY' not in columnHeader:
                    columnHeader.append('MOY')
            if int(result['PLYQNTY']) != 0:
                if 'PLY' not in columnHeader:
                    columnHeader.append('PLY')
            if int(result['POYQNTY']) != 0:
                if 'POY' not in columnHeader:
                    columnHeader.append('POY')
            if int(result['TWDQNTY']) != 0:
                if 'TWD' not in columnHeader:
                    columnHeader.append('TWD')
            POYQnty += int(result['POYQNTY'])
            FDYQnty += int(result['FDYQNTY'])
            MOYQnty += int(result['MOYQNTY'])
            MONQnty += int(result['MONQNTY'])
            DTYQnty += int(result['DTYQNTY'])
            ATYQnty += int(result['ATYQNTY'])
            TWDQnty += int(result['TWDQNTY'])
            BCFQnty += int(result['BCFQNTY'])
            CABQnty += int(result['CABQNTY'])
            HSTQnty += int(result['HSTQNTY'])
            PLYQnty += int(result['PLYQNTY'])
            TOTALQnty += int(result['ATYQNTY']) + int(result['BCFQNTY']) + int(result['CABQNTY']) + \
                         int(result['DTYQNTY']) + \
                         int(result['HSTQNTY']) + int(result['MONQNTY']) + int(result['MOYQNTY']) + \
                         int(result['PLYQNTY']) + int(result['POYQNTY']) + int(result['TWDQNTY'])
            # Calculate total amount As Per Item Type
            POYAmnt += int(result['POYAMT'])
            FDYAmnt += int(result['FDYAMT'])
            MOYAmnt += int(result['MOYAMT'])
            MONAmnt += int(result['MONAMT'])
            DTYAmnt += int(result['DTYAMT'])
            ATYAmnt += int(result['ATYAMT'])
            TWDAmnt += int(result['TWDAMT'])
            BCFAmnt += int(result['BCFAMT'])
            CABAmnt += int(result['CABAMT'])
            HSTAmnt += int(result['HSTAMT'])
            PLYAmnt += int(result['PLYAMT'])
            TotalAmtExDhara += int(result['ATYAMT']) + int(result['BCFAMT']) + int(result['CABAMT']) + \
                               int(result['DTYAMT']) + int(result['FDYAMT']) + \
                               int(result['HSTAMT']) + int(result['MONAMT']) + int(result['MOYAMT']) + \
                               int(result['PLYAMT']) + int(result['POYAMT']) + int(result['TWDAMT'])
            result['TOTALQTY'] = int(result['ATYQNTY']) + int(result['BCFQNTY']) + int(result['CABQNTY']) + \
                               int(result['DTYQNTY']) + \
                               int(result['HSTQNTY']) + int(result['MONQNTY']) + int(result['MOYQNTY']) + \
                               int(result['PLYQNTY']) + int(result['POYQNTY']) + int(result['TWDQNTY'])
            GDataAgentColumnGroup.append(result)
        else:
            if result['TOTALINVOICEAMOUT'] != None:
                TotalInvoiceAmout += float(result['TOTALINVOICEAMOUT'])
            # pass
        result = con.db.fetch_both(stmt)

    # print(GDataAgentColumnGroup)
    # str('{0:1.2f}'.format(gst))
    # print(intersection(refHeader,columnHeader))
    if POYQnty != 0:
        POYAvgRate = POYAmnt/POYQnty
    if FDYQnty != 0:
        FDYAvgRate = FDYAmnt/FDYQnty
    if MOYQnty != 0:
        MOYAvgRate = MOYAmnt/MOYQnty
    if MONQnty != 0:
        MONAvgRate = MONAmnt/MONQnty
    if DTYQnty != 0:
        DTYAvgRate = DTYAmnt/DTYQnty
    if ATYQnty != 0:
        ATYAvgRate = ATYAmnt/ATYQnty
    if TWDQnty != 0:
        TWDAvgRate = TWDAmnt/TWDQnty
    if BCFQnty != 0:
        BCFAvgRate = BCFAmnt/BCFQnty
    if CABQnty != 0:
        CABAvgRate = CABAmnt/CABQnty
    if HSTQnty != 0:
        HSTAvgRate = HSTAmnt/HSTQnty
    if PLYQnty != 0:
        PLYAvgRate = PLYAmnt/PLYQnty
    if TOTALQnty != 0:
        TOTALAvgRate = TotalAmtExDhara/TOTALQnty
    # print(itemtypeOptSelected)
    if GDataAgentColumnGroup != []:
        return render(request, 'LiftingSummaryProcessSumm.html', {'Syear':syear ,'Smonth':smonth , 'Sday':sday,
                                                                  'Eyear':eyear ,'Emonth':emonth , 'Eday':eday,
                                                                  'itemtypeOptSelected':itemtypeOptSelected,
                                                                   'columnHeader':intersection(refHeader,columnHeader),
                                                                  'GDataAgentColumnGroup':GDataAgentColumnGroup,
                                                                  'TOTALQNTY': TOTALQnty,
                                                                  'POYQnty':POYQnty,
                                                                  'FDYQnty':FDYQnty,
                                                                  'MOYQnty':MOYQnty,
                                                                  'MONQnty':MONQnty,
                                                                  'DTYQnty':DTYQnty,
                                                                  'ATYQnty':ATYQnty,
                                                                  'TWDQnty':TWDQnty,
                                                                  'BCFQnty':BCFQnty,
                                                                  'CABQnty':CABQnty,
                                                                  'HSTQnty':HSTQnty,
                                                                  'PLYQnty':PLYQnty,

                                                                  'TOTALAvgRate': str('{0:1.2f}'.format(TOTALAvgRate)),
                                                                  'POYAvgRate': str('{0:1.2f}'.format(POYAvgRate)),
                                                                  'FDYAvgRate': str('{0:1.2f}'.format(FDYAvgRate)),
                                                                  'MOYAvgRate': str('{0:1.2f}'.format(MOYAvgRate)),
                                                                  'MONAvgRate': str('{0:1.2f}'.format(MONAvgRate)),
                                                                  'DTYAvgRate': str('{0:1.2f}'.format(DTYAvgRate)),
                                                                  'ATYAvgRate': str('{0:1.2f}'.format(ATYAvgRate)),
                                                                  'TWDAvgRate': str('{0:1.2f}'.format(TWDAvgRate)),
                                                                  'BCFAvgRate': str('{0:1.2f}'.format(BCFAvgRate)),
                                                                  'CABAvgRate': str('{0:1.2f}'.format(CABAvgRate)),
                                                                  'HSTAvgRate': str('{0:1.2f}'.format(HSTAvgRate)),
                                                                  'PLYAvgRate': str('{0:1.2f}'.format(PLYAvgRate )),
                                                                  'TotalAmtExDhara': str(format_currency(float(TotalAmtExDhara), '', locale='en_IN')),
                                                                  'TotalInvoiceAmount': str(format_currency(float(TotalInvoiceAmout), '',locale='en_IN'))
                                                                  })

    else:
        Exception = 'Record Not Found'
        itemtypeOpt = str(request.GET.getlist('optionValue'))
        if len(itemtypeOpt) > 4:
            itemtypeOpt = str(itemtypeOpt)[2:-2]
            itemtypeOptSelected = itemtypeOpt.replace("'", "")
            if len(itemtypeOpt) == 32:
                itemtypeOptSelected = "0"
        else:
            itemtypeOptSelected = "0"
        return render(request, 'LiftingSummary.html', {'itemtypeOptSelected': itemtypeOptSelected,'Exception': Exception})

# Lifting Summary Details*******************************


def LiftingSummaryDetailsMis(request):
    GDataDetailHeader = []
    StartDate = str(request.GET['startdate'])
    EndDate = str(request.GET['enddate'])
    Broker = str(request.GET['broker'])
    Itemtype = str(request.GET['yarnType'])
    # TotalAmtExDhara = str(request.GET['invAmtExDhara'])
    # TotalInvoiceAmount = int(request.GET['InvAmt'])
    # print(TotalAmtExDhara, '   ', TotalInvoiceAmout)

    syear = StartDate[0:4]
    smonth = StartDate[5:7]
    sday = StartDate[8:10]

    eyear = EndDate[0:4]
    emonth = EndDate[5:7]
    eday = EndDate[8:10]
    # print(Broker, '  ', Itemtype)

    StartDate = "'" + str(StartDate)[0:-1] + "'"
    EndDate = "'" + str(EndDate)[0:10] + "'"

    # ********** Header in details
    sql="WITH months(i, d) AS ( VALUES (1, DATE("+StartDate+")) " \
        "UNION ALL " \
        "SELECT i + 1, d + 1 MONTH " \
        "FROM months " \
        "WHERE i < 10000 " \
        "AND d + 1 MONTH <= DATE("+EndDate+")) " \
        "SELECT date(d) as date" \
        ", monthname(d) as monthname FROM months"

    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        # GDataDetailHeader.append(result)
        result = con.db.fetch_both(stmt)
    # print(GDataDetailHeader)


    GDataDetailsColumn = []
    sql="Select  PRODUCT.LONGDESCRIPTION As Item " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'January' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As JanQnty " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'February' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As FebQnty " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'March' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As MarQnty " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'April' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As AprQnty " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'May' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As mayQnty " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'june' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As JuneQnty " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'July' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As JulQnty " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'August' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As AugQnty " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'September' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As SepQnty " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'October' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As OctQnty " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'November' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As NovQnty " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'December' Then Round(PIL.PRIMARYQTY,0) Else 0 End) As Decimal(30,0)) As DecQnty " \
        " , CAST(Sum(Case When monthname(PI.INVOICEDATE) = 'January' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As JanAmnt " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'February' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As FebAmnt " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'March' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As MarAmnt " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'April' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As AprAmnt " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'May' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As mayAmnt " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'june' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As JuneAmnt " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'July' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As JulAmnt " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'August' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As AugAmnt " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'September' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As SepAmnt " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'October' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As OctAmnt " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'November' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As NovAmnt " \
        ", Cast(Sum(Case When monthname(PI.INVOICEDATE) = 'December' Then Round(Coalesce(invAmt.BASEVALUE,PIL.BASICVALUE)-Coalesce(DharaAmt.value,0),0) Else 0 End) As Decimal(30,0)) As DecAmnt " \
        "From   PlantInvoice PI " \
        "Join PLANTINVOICELINE PIL               On      PI.CODE = PIL.PLANTINVOICECODE " \
        "jOIN SALESDOCUMENT SD                   ON      PI.code = SD.DEFINITIVECODE " \
        "Left Join AGENT                         On      SD.AGENT1CODE = Agent.code " \
          "Left Join INDTAXDETAIL invAmt                ON      PIL.ABSUNIQUEID = invAmt.ABSUNIQUEID " \
          "And     PIL.TAXTEMPLATECODE = invAmt.TAXTEMPLATECODE " \
          "And     PIL.TAXTEMPLATETEMPLATETYPE = invAmt.TAXTEMPLATETEMPLATETYPE " \
          "AND     invAmt.ITAXCODE = 'PPU' " \
          "Left Join    INDTAXDETAIL DharaAmt      ON      PIL.ABSUNIQUEID = DharaAmt.ABSUNIQUEID " \
          "And     DharaAmt.ITAXCODE = 'DRA' " \
          "And     DharaAmt.TAXCATEGORYCODE = 'OTH' " \
        "join    FULLITEMKEYDECODER FIKD         ON      PIL.ITEMTYPECODE = FIKD.ITEMTYPECODE " \
        "AND     COALESCE(PIL.SubCode01, '') = COALESCE(FIKD.SubCode01, '') " \
        "AND     COALESCE(PIL.SubCode02, '') = COALESCE(FIKD.SubCode02, '') " \
        "AND     COALESCE(PIL.SubCode03, '') = COALESCE(FIKD.SubCode03, '') " \
        "AND     COALESCE(PIL.SubCode04, '') = COALESCE(FIKD.SubCode04, '') " \
        "AND     COALESCE(PIL.SubCode05, '') = COALESCE(FIKD.SubCode05, '') " \
        "AND     COALESCE(PIL.SubCode06, '') = COALESCE(FIKD.SubCode06, '') " \
        "AND     COALESCE(PIL.SubCode07, '') = COALESCE(FIKD.SubCode07, '') " \
        "AND     COALESCE(PIL.SubCode08, '') = COALESCE(FIKD.SubCode08, '') " \
        "AND     COALESCE(PIL.SubCode09, '') = COALESCE(FIKD.SubCode09, '') " \
        "AND     COALESCE(PIL.SubCode10, '') = COALESCE(FIKD.SubCode10, '') " \
        "Join    PRODUCT                         ON      PIL.ITEMTYPECODE = PRODUCT.ITEMTYPECODE " \
        "And     FIKD.ItemUniqueId = PRODUCT.ABSUNIQUEID " \
        "Where   SD.DOCUMENTTYPETYPE = '06' And Coalesce(AGENT.LONGDESCRIPTION, 'Broker Name Not Entered') = '"+Broker+"' " \
        "And PIL.ITEMTYPECODE = '"+Itemtype+"'  " \
        "And PI.INVOICEDATE Between "+StartDate+" And "+EndDate+" " \
        "Group By  PRODUCT.LONGDESCRIPTION " \
        "Order By Item"

    totalJan = 0
    totalFeb = 0
    totalMar = 0
    totalApr = 0
    totalMay = 0
    totalJun = 0
    totalJul = 0
    totalAug = 0
    totalSep = 0
    totalOct = 0
    totalNov = 0
    totalDec = 0
    TotalQntity = 0

    #
    totalJanAmt = 0
    totalFebAmt = 0
    totalMarAmt = 0
    totalAprAmt = 0
    totalMayAmt = 0
    totalJunAmt = 0
    totalJulAmt = 0
    totalAugAmt = 0
    totalSepAmt = 0
    totalOctAmt = 0
    totalNovAmt = 0
    totalDecAmt = 0
    totalAmount = 0

    # total row average rate
    AvgJan = 0
    AvgFeb = 0
    AvgMar = 0
    AvgApr = 0
    AvgMay = 0
    AvgJun = 0
    AvgJul = 0
    AvgAug = 0
    AvgSep = 0
    AvgOct = 0
    AvgNov = 0
    AvgDec = 0


    stmt = con.db.prepare(con.conn, sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    while result != False:
        totalJan += int(result['JANQNTY'])
        totalFeb += int(result['FEBQNTY'])
        totalMar += int(result['MARQNTY'])
        totalApr += int(result['APRQNTY'])
        totalMay += int(result['MAYQNTY'])
        totalJun += int(result['JUNEQNTY'])
        totalJul += int(result['JULQNTY'])
        totalAug += int(result['AUGQNTY'])
        totalSep += int(result['SEPQNTY'])
        totalOct += int(result['OCTQNTY'])
        totalNov += int(result['NOVQNTY'])
        totalDec += int(result['DECQNTY'])

        totalJanAmt += int(result['JANAMNT'])
        totalFebAmt += int(result['FEBAMNT'])
        totalMarAmt += int(result['MARAMNT'])
        totalAprAmt += int(result['APRAMNT'])
        totalMayAmt += int(result['MAYAMNT'])
        totalJunAmt += int(result['JUNEAMNT'])
        totalJulAmt += int(result['JULAMNT'])
        totalAugAmt += int(result['AUGAMNT'])
        totalSepAmt += int(result['SEPAMNT'])
        totalOctAmt += int(result['OCTAMNT'])
        totalNovAmt += int(result['NOVAMNT'])
        totalDecAmt += int(result['DECAMNT'])

        # total Amnt as Monthwise

        result['TOTAL'] = int(result['JANQNTY']) + int(result['FEBQNTY']) + int(result['MARQNTY']) + \
                          int(result['APRQNTY']) + int(result['MAYQNTY']) + int(result['JUNEQNTY']) + \
                          int(result['JULQNTY']) + int(result['AUGQNTY']) + int(result['SEPQNTY']) + \
                          int(result['OCTQNTY']) + int(result['NOVQNTY']) + int(result['DECQNTY'])
        TotalQntity += int(result['JANQNTY']) + int(result['FEBQNTY']) + int(result['MARQNTY']) + \
                          int(result['APRQNTY']) + int(result['MAYQNTY']) + int(result['JUNEQNTY']) + \
                          int(result['JULQNTY']) + int(result['AUGQNTY']) + int(result['SEPQNTY']) + \
                          int(result['OCTQNTY']) + int(result['NOVQNTY']) + int(result['DECQNTY'])
        if int(result['JANQNTY']) != 0:
            result['AvgJan'] = str('{0:1.2f}'.format(int(result['JANAMNT'])/int(result['JANQNTY'])))
        else:
            result['AvgJan'] = 0
        if int(result['FEBQNTY']) != 0:
            result['AvgFeb'] = str('{0:1.2f}'.format(int(result['FEBAMNT'])/int(result['FEBQNTY'])))
        else:
            result['AvgFeb'] = 0
        if int(result['MARQNTY']) != 0:
            result['AvgMar'] = str('{0:1.2f}'.format(int(result['MARAMNT'])/int(result['MARQNTY'])))
        else:
            result['AvgMar'] = 0
        if int(result['APRQNTY']) != 0:
            result['AvgApr'] = str('{0:1.2f}'.format(int(result['APRAMNT'])/int(result['APRQNTY'])))
        else:
            result['AvgApr'] = 0
        if int(result['MAYQNTY']) != 0:
            result['AvgMay'] = str('{0:1.2f}'.format(int(result['MAYAMNT'])/int(result['MAYQNTY'])))
        else:
            result['AvgMay'] = 0
        if int(result['JUNEQNTY']) != 0:
            result['AvgJun'] = str('{0:1.2f}'.format(int(result['JUNEAMNT'])/int(result['JUNEQNTY'])))
        else:
            result['AvgJun'] = 0
        if int(result['JULQNTY']) != 0:
            result['AvgJul'] = str('{0:1.2f}'.format(int(result['JULAMNT'])/int(result['JULQNTY'])))
        else:
            result['AvgJul'] = 0
        if int(result['AUGQNTY']) != 0:
            result['AvgAug'] = str('{0:1.2f}'.format(int(result['AUGAMNT'])/int(result['AUGQNTY'])))
        else:
            result['AvgAug'] = 0
        if int(result['SEPQNTY']) != 0:
            result['AvgSep'] = str('{0:1.2f}'.format(int(result['SEPAMNT'])/int(result['SEPQNTY'])))
        else:
            result['AvgSep'] = 0
        if int(result['OCTQNTY']) != 0:
            result['AvgOct'] = str('{0:1.2f}'.format(int(result['OCTAMNT'])/int(result['OCTQNTY'])))
        else:
            result['AvgOct'] = 0
        if int(result['NOVQNTY']) != 0:
            result['AvgNov'] = str('{0:1.2f}'.format(int(result['NOVAMNT'])/int(result['NOVQNTY'])))
        else:
            result['AvgNov'] = 0
        if int(result['DECQNTY']) != 0:
            result['AvgDec'] = str('{0:1.2f}'.format(int(result['DECAMNT'])/int(result['DECQNTY'])))
        else:
            result['AvgDec'] = 0

        GDataDetailsColumn.append(result)
        result = con.db.fetch_both(stmt)

    # print(Broker,Itemtype)
    # AVG RATE
    if totalJan !=0:
        AvgJan = str('{0:1.2f}'.format(int(totalJanAmt)/int(totalJan)))
        GDataDetailHeader.append('January')
    if totalFeb !=0:
        AvgFeb = str('{0:1.2f}'.format(int(totalFebAmt)/int(totalFeb)))
        GDataDetailHeader.append('February')
    if totalMar !=0:
        AvgMar = str('{0:1.2f}'.format(int(totalMarAmt)/int(totalMar)))
        GDataDetailHeader.append('March')
    if totalApr !=0:
        AvgApr = str('{0:1.2f}'.format(int(totalAprAmt)/int(totalApr)))
        GDataDetailHeader.append('April')
    if totalMay !=0:
        AvgMay = str('{0:1.2f}'.format(int(totalMayAmt)/int(totalMay)))
        GDataDetailHeader.append('May')
    if totalJun !=0:
        AvgJun = str('{0:1.2f}'.format(int(totalJunAmt)/int(totalJun)))
        GDataDetailHeader.append('june')
    if totalJul !=0:
        AvgJul = str('{0:1.2f}'.format(int(totalJulAmt)/int(totalJul)))
        GDataDetailHeader.append('July')
    if totalAug !=0:
        AvgAug = str('{0:1.2f}'.format(int(totalAugAmt)/int(totalAug)))
        GDataDetailHeader.append('August')
    if totalSep !=0:
        AvgSep = str('{0:1.2f}'.format(int(totalSepAmt)/int(totalSep)))
        GDataDetailHeader.append('September')
    if totalOct !=0:
        AvgOct = str('{0:1.2f}'.format(int(totalOctAmt)/int(totalOct)))
        GDataDetailHeader.append('October')
    if totalNov !=0:
        AvgNov = str('{0:1.2f}'.format(int(totalNovAmt)/int(totalNov)))
        GDataDetailHeader.append('November')
    if totalDec !=0:
        AvgDec = str('{0:1.2f}'.format(int(totalDecAmt)/int(totalDec)))
        GDataDetailHeader.append('December')

    return render(request, 'LiftingSummaryDetails.html', {'Syear':syear ,'Smonth':smonth , 'Sday':sday,
                                                        'Eyear':eyear ,'Emonth':emonth , 'Eday':eday,
                                                          'GDataDetailHeader': GDataDetailHeader, 'GDataDetailsColumn': GDataDetailsColumn,
                                                          'Broker':Broker , 'Itemtype':Itemtype ,
                                                          'TotalAmtExDhara': str(format_currency(float(TotalAmtExDhara), '',locale='en_IN')),
                                                          'TotalInvoiceAmount': str(format_currency(float(TotalInvoiceAmout), '',locale='en_IN')),
                                                          'totalJan': totalJan,
                                                          'totalFeb': totalFeb,
                                                          'totalMar': totalMar,
                                                          'totalApr': totalApr,
                                                          'totalMay': totalMay,
                                                          'totalJun': totalJun,
                                                          'totalJul': totalJul,
                                                          'totalAug': totalAug,
                                                          'totalSep': totalSep,
                                                          'totalOct': totalOct,
                                                          'totalNov': totalNov,
                                                          'totalDec': totalDec,
                                                          'TotalQntity':TotalQntity,
                                                          'AvgJan': AvgJan,
                                                          'AvgFeb': AvgFeb,
                                                          'AvgMar': AvgMar,
                                                          'AvgApr': AvgApr,
                                                          'AvgMay': AvgMay,
                                                          'AvgJun': AvgJun,
                                                          'AvgJul': AvgJul,
                                                          'AvgAug': AvgAug,
                                                          'AvgSep': AvgSep,
                                                          'AvgOct': AvgOct,
                                                          'AvgNov': AvgNov,
                                                          'AvgDec': AvgDec,
                                                          })