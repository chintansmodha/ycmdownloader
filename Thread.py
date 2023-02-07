import threading
Response=[]
def read_file(file_name):
    with open(file_name,'r') as f:
        Response.append(f.read())

file_names=['TextFile1.txt','TextFile2.txt','TextFile3.txt','TextFile4.txt','TextFile5.txt','TextFile6.txt','TextFile7.txt','TextFile8.txt','TextFile9.txt','TextFile10.txt']

threads=[]
for filename in file_names:
    thread = threading.Thread(target=read_file,args=(filename,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(Response)