from django.http import HttpResponse
import json
from Global_Files import Connection_String as con
from FormLoad import StockLedger_FormLoad as STFL
GDataItemCode=[]



def itemLoad(request):
    global GDataItemCode
    GDataItemCode=[]
    if request.method == 'GET':
        itemGroupList= request.GET.getlist('param')
        itemGroupList = str(itemGroupList).replace("[","")
        itemGroupList = str(itemGroupList).replace("]","")
        itemGroupList = str(itemGroupList).replace("'","")
        itemGroupList = itemGroupList.split(",")

        stmt = con.db.exec_immediate(con.conn,"select ABSUNIQUEID, LONGDESCRIPTION from Product Where ITEMTYPECODE in ("+str(itemGroupList)[1:-1]+") order by LONGDESCRIPTION")
        result = con.db.fetch_both(stmt)
        while result != False:
            if result not in GDataItemCode:
                GDataItemCode.append(result)
            result = con.db.fetch_both(stmt)

        response_data ={"user": GDataItemCode}
        print(response_data)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
        

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def fetchItem(request):
    print("jigar")
    global GDataItemCode
    GDataItemCode=[]
    if request.method == 'GET':
        response_data ={"user": STFL.GDataItemCode}
        print(response_data)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )