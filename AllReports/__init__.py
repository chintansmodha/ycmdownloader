" Select  PI.Code as INVNO"
"        ,VARCHAR_FORMAT(PI.INVOICEDATE, 'DD-MM-YYYY') as InvoiceDate"
"        ,cast(FOD.AMOUNTINCC as decimal(18,2)) AS INVAMT"
"        ,cast((FOD.AmountinCC-FOD.CLEAREDAMOUNT) as decimal(18,2)) As OSAMT"
"        ,BusinessPartner.legalname1 As Party"
"        ,Company.Longdescription As Company "
"        ,AgGrp.Longdescription AS Broker"
"       From FinOpendocuments as FOD"
"        JOIN FINBUSINESSUNIT UNIT       ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"        JOIN FINBUSINESSUNIT Company    ON      UNIT.GROUPBUCODE=Company.CODE"
"        Join PlantInvoice PI            on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                        And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                        And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                        And FOD.CODE = PI.FINDOCCODE "
"        Join    AgentsGroupDetail AGD   On      PI.Agent1Code = AGD.AgentCode "
"        Join    AgentsGroup AgGrp    On      AGD.AgentsGroupCode = AgGrp.Code "
"        join OrderPartner As OrderPartner         on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode"
"        And                                     FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType"
"        Join BusinessPartner ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId"
"        Where  FOD.postingdate <= '2022-11-01'"
"        And    FOD.FINANCIALYEARCODE = '2023'"
"        And    FOD.DOCUMENTTEMPLATECODE = 'S01'"
"        And    (FOD.AmountinCC-FOD.CLEAREDAMOUNT) > 0"

" Union All     "
"        "
" Select  PI.Code as INVNO"
"        ,VARCHAR_FORMAT(PI.INVOICEDATE, 'DD-MM-YYYY') as InvoiceDate"
"        ,cast(FOD.AMOUNTINCC as decimal(18,2)) AS INVAMT"
"        ,cast((FODT.CLEAREDAMOUNT) as decimal(18,2)) As OSAMT"
"        ,BusinessPartner.legalname1 As Party"
"        ,Company.Longdescription As Company "
"        ,AgGrp.Longdescription AS Broker"
" From    FinOpendocuments as FOD"
"        JOIN FINBUSINESSUNIT UNIT               ON      FOD.BUSINESSUNITCODE=UNIT.CODE"
"        JOIN FINBUSINESSUNIT Company            ON      UNIT.GROUPBUCODE=Company.CODE"
"        Join PlantInvoice PI                    on FOD.BUSINESSUNITCODE=PI.FINDOCBUSINESSUNITCODE "
"                                                And  FOD.FINANCIALYEARCODE=PI.FINDOCFINANCIALYEARCODE"
"                                                And FOD.DOCUMENTTEMPLATECODE = PI.FINDOCTEMPLATECODE "
"                                                And FOD.CODE = PI.FINDOCCODE "
"        Join    AgentsGroupDetail AGD           On      PI.Agent1Code = AGD.AgentCode "
"        Join    AgentsGroup AgGrp               On      AGD.AgentsGroupCode = AgGrp.Code "
"        join OrderPartner As OrderPartner       on FOD.ORDERPARTNERCODE = OrderPartner.CustomerSupplierCode"
"                                                And FOD.ORDERPARTNERTYPE = OrderPartner.CustomerSupplierType"
"        Join BusinessPartner                    ON OrderPartner.OrderBusinessPartnerNumberId = BusinessPartner.NumberId"
"        Join FinopendocumentsTransactions as FODT"
"                                                ON      FOD.BUSINESSUNITCODE=FODT.ORIGINBUSINESSUNITCODE"
"                                                And     FOD.FINANCIALYEARCODE=FODT.ORIGINFINANCIALYEARCODE"
"                                                And     FOD.DOCUMENTTEMPLATECODE=FODT.ORIGINDOCUMENTTEMPLATECODE"
"                                                And     FOD.CODE=FODT.ORIGINCODE"
" Where  FODT.TRANSACTIONDATE > '2022-11-01'"
" and     FOD.postingdate <= '2022-11-01'"


# "# Invoice 01-Nov-2022     50000"
# "# Payment 10-Nov-2022     45000"
# "# 15-Nov-2022     30000 for Above Invoice"
# "# 18-Nov-2022     30000 Actually Clearing Done in NOW System"