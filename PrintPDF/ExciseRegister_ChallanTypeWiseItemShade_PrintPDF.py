import textwrap
from reportlab.lib.pagesizes import landscape, A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from babel.numbers import format_number , format_currency , format_decimal

pdfmetrics.registerFont(TTFont('MyOwnArial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('MyOwnArialBold', 'arialbd.ttf'))

c = canvas.Canvas("1.pdf")