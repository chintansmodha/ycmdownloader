from django.shortcuts import render
from GetDataFromDB import MISBrokerWiseOS_GetDataFromDB as MISBGDDB
from Global_Files import Connection_String as con

def ChequeDetailTab(request):
    Company = request.GET['comp']
    Broker = request.GET['brk']
    FinCode = request.GET['fincode']
    Company = " And company.Code = '"+Company+"'"
    Broker = " And AgGrp.Code = '" + Broker + "'"
    FinCode = " And FD.Code = '"+FinCode+"'"
    Sql = "Select company.LONGDESCRIPTION as Company" \
          ",BU.LONGDESCRIPTION as Branch" \
          ",GLmaster.LONGDESCRIPTION as Bank" \
          ",FD.Code as Vchno" \
          ",VARCHAR_FORMAT(FD.PostingDate, 'YYYY-MM-DD') As VchDate" \
          ",COALESCE(FD.CHEQUENUMBER,CHQN.Valuestring,'') As ChqNo" \
          ",VARCHAR_FORMAT(COALESCE(FD.CHEQUEDATE,CHQD.ValueDate,'01-01-1990'),'YYYY-MM-DD') As ChqDate" \
          ",BP.legalname1 as Party" \
          ",AgGrp.LONGDESCRIPTION as Broker" \
          ", Case When ISST.ValueString = '1' then 'Not Confirmed' when ISST.ValueString = '2' then 'Confirmed' End as SlipStatus" \
          ", Case When CHHD.ValueString = '0' then 'Not Deposited' when ISST.ValueString = '1' then 'Deposited' End as ChequeDep" \
          ",ISSN.ValueString as SlipNo" \
          ",cast(FD.DocumentAmount as decimal(18,2)) as chqamt" \
          ",'' as sliptype" \
          ",'' partybank" \
          ",'' as nar" \
          ",'NO' as writeoff" \
          ",'NO' as Bounce" \
          " from Findocument AS FD" \
          " Join    FinBusinessUnit BU on FD.BusinessUnitcode = BU.Code" \
          " Join    FinBusinessUnit Company On BU.GroupbuCode = Company.Code" \
          " JOIN    AgentsGroupDetail AGD           ON FD.Agent1Code = AGD.AgentCode" \
          " JOIN    AgentsGroup AgGrp               ON AGD.AgentsGroupCode = AgGrp.Code" \
          " Left Join GLmaster On FD.GLCODE=GLMASTER.code" \
          " LEFT JOIN AdStorage AS CHQN               ON  FD.AbsUniqueId = CHQN.UniqueId" \
          " AND CHQN.NameEntityName = 'FINDocument'" \
          " And CHQN.NameName = 'CustomerCheque'" \
          " And CHQN.FieldName = 'CustomerCheque'" \
          " Left JOIN OrderPartner AS OP ON COALESCE(FD.CUSTOMERCODE,FD.SUPPLIERCODE,'') = OP.CUSTOMERSUPPLIERCODE" \
          " And COALESCE(FD.CUSTOMERType,FD.SUPPLIERType,'') = OP.CUSTOMERSUPPLIERTYPE" \
          " Left JOIN BusinessPartner AS BP           ON OP.ORDERBUSINESSPARTNERNUMBERID = BP.NumberID" \
          " LEFT JOIN AdStorage AS CHQD               ON  FD.AbsUniqueId = CHQD.UniqueId" \
          " AND CHQD.NameEntityName = 'FINDocument'" \
          " And CHQD.NameName = 'ChequeDate' And CHQD.FieldName = 'ChequeDate'" \
          " Left JOIN AdStorage AS ISST               ON  FD.AbsUniqueId = ISST.UniqueId" \
          " And ISST.NameEntityNAme ='FINDocument' And ISST.FieldName = 'IssueSlipStatus'" \
          " LEFT JOIN AdStorage AS ISSN               ON  FD.AbsUniqueId = ISSN.UniqueId" \
          " And ISSN.NameEntityNAme ='FINDocument' And ISSN.FieldName = 'IssuesSlipNO'" \
          " LEFT JOIN AdStorage AS CHHD               ON  FD.AbsUniqueId = CHHD.UniqueId" \
          " AND  CHHD.NameEntityNAme ='FINDocument' And CHHD.FieldName = 'ChequeDeposited'" \
          " Where FD.COMPANYCODE = '100' "+Company+Broker+FinCode+""
    stmt = con.db.prepare(con.conn, Sql)
    con.db.execute(stmt)
    result = con.db.fetch_both(stmt)
    print(result)
    if result != False:
        print("jigar")
        return render(request, "BrokerWiseOSUnadjustedChequeDetail.html",{"result":result})
    else:
        return render(request, "BrokerWiseOSUnadjustedChequeDetail.html", {"result": result})