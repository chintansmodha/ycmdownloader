from urllib import request

from django.shortcuts import render
from Global_Files import Connection_String as con


def home(request):
    return render(request,'index.html')

def DispatchDetail(request):
    # print("From Dispatch Detail List ")
    return render(request,'DispatchDetailRegister.html')

