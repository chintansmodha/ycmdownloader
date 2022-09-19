import ibm_db as db

conn = db.connect('DATABASE=NOWTest;'
                      'HOSTNAME=192.168.0.18;'
                      'PORT=50000;'
                      'PROTOCOL=TCPIP;'
                     'UID=Db2Admin;'
                     'PWD=Sunka@2480;AUTHENTICATION=SERVER',"","")