from django.shortcuts import render
from Global_Files import Connection_String as con

def PurchaseItemWiseHtml(request):
    return render(request,'PurchaseItemWise.html')