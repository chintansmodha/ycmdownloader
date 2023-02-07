List1=[]
for i in range(1,1000001):
    List1.append("This is line no - "+str(i)+"\n")

file1 = open("TextFile1.txt", "w")
file1.writelines(List1[0:100000])
file1.close()

file1 = open("TextFile2.txt", "w")
file1.writelines(List1[100000:200000])
file1.close()

file1 = open("TextFile3.txt", "w")
file1.writelines(List1[200000:300000])
file1.close()

file1 = open("TextFile4.txt", "w")
file1.writelines(List1[300000:400000])
file1.close()

file1 = open("TextFile5.txt", "w")
file1.writelines(List1[400000:500000])
file1.close()

file1 = open("TextFile6.txt", "w")
file1.writelines(List1[500000:600000])
file1.close()

file1 = open("TextFile7.txt", "w")
file1.writelines(List1[600000:700000])
file1.close()

file1 = open("TextFile8.txt", "w")
file1.writelines(List1[700000:800000])
file1.close()

file1 = open("TextFile9.txt", "w")
file1.writelines(List1[800000:900000])
file1.close()

file1 = open("TextFile10.txt", "w")
file1.writelines(List1[900000:1000000])
file1.close()
