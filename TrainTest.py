import random
filehandle=open("database.txt","r")
filehandle2=open("databaseTrain.txt","w")
filehandle3=open("databaseTest.txt","w")
l=filehandle.readlines()
count=int(len(l)*0.2)
for i in range(count):
    x=random.randint(0,len(l)-1)
    filehandle3.write(l[x])
filehandle3.close()
filehandle4=open("databaseTest.txt","r")
l2=filehandle4.readlines()
for i in range(len(l)):
    if l[i] not in l2:
        filehandle2.write(l[i])
filehandle2.close()
filehandle.close()