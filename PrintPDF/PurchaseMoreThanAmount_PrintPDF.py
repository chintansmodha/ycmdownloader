from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from GetDataFromDB import PurchaseMoreThanAmount_GetDataFromDB

pdfmetrics.registerFont(TTFont("MyOwnArial", "arial.ttf"))

c = canvas.Canvas("1.pdf")
d = 730

divisioncode = []
ItemQuantityTotal = 0
CompanyAmountTotal = 0
pageno = 0


def page():
    global pageno
    pageno = pageno + 1
    return pageno


def boldfonts(size):
    global c
    c.setFont("MyOwnArialBold", size)


def fonts(size):
    global c
    c.setFont("MyOwnArial", size)


def dvalue(stdt, etdt, divisioncode):
    global d
    if d > 40:
        d = d - 10
        return d
    else:
        d = newpage()
        c.showPage()
        header(stdt, etdt, divisioncode)
        return d


def header(stdt, etdt, divisioncode):
    boldfonts(15)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(300, 800, divisioncode[-1])
    boldfonts(9)
    c.drawCentredString(
        300,
        780,
        "SupplierWise Purchases >="
        + PurchaseMoreThanAmount_GetDataFromDB.LNamount
        + " From "
        + str(stdt.strftime("%d-%m-%Y"))
        + " To "
        + str(etdt.strftime("%d-%m-%Y")),
    )
    p = page()
    c.drawString(540, 780, "Page No." + str(p))
    c.line(0, 770, 600, 770)
    c.line(0, 740, 600, 740)
    # Upperline in header
    c.drawString(10, 755, "SUPPLIER")
    c.drawString(400, 755, "PANNO")
    c.drawString(540, 755, "AMOUNT")
    fonts(7)


def data(result, d):
    fonts(7)
    c.drawString(10, d, result["SUPPLIER"])
    c.drawString(400, d, result["PANNO"])
    c.drawAlignedString(570, d, str(("%.2f" % float(result["BILLAMOUNT"]))))
    d = d - 10
    c.drawString(10, d, result["ADDRESS"])
    total(result)


def total(result):
    global CompanyAmountTotal
    global ItemQuantityTotal
    CompanyAmountTotal = CompanyAmountTotal + (
        float("%.2f" % float(result["BILLAMOUNT"]))
    )
    ItemQuantityTotal = ItemQuantityTotal + (
        float("%.2f" % float(result["BILLAMOUNT"]))
    )


def logic(result):
    divisioncode.append(result["DIVCODE"])


def dlocvalue(d):
    d = d - 20
    return d


def newpage():
    global d
    d = 730
    return d


def newrequest():
    global divisioncode
    global pageno
    divisioncode = []
    pageno = 0


def companyclean():
    global CompanyAmountTotal
    CompanyAmountTotal = 0


def textsize(c, result, d, stdt, etdt):
    d = dvalue(stdt, etdt, divisioncode)
    d = dvalue(stdt, etdt, divisioncode)
    logic(result)
    if len(divisioncode) == 1:
        header(stdt, etdt, divisioncode)
        data(result, d)

    elif divisioncode[-1] == divisioncode[-2]:
        data(result, d)

    elif divisioncode[-1] != divisioncode[-2]:
        boldfonts(9)
        c.drawString(400, d, " Total : ")
        c.drawAlignedString(570, d, str("%.2f" % float(CompanyAmountTotal)))
        companyclean()
        c.showPage()
        fonts(7)
        header(stdt, etdt, divisioncode)
        d = newpage()
        d = dvalue(stdt, etdt, divisioncode)
        data(result, d)
