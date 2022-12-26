
from Global_Files import Connection_String as con
from django.shortcuts import render

def BankCashVoucherHtml(request):
    return render(request, 'BankCashVoucherPDF.html')