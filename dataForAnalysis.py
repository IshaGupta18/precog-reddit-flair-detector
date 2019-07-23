filehandle2=open("browniedata.txt","r")
list2=filehandle2.readlines()
actualLabels={'AMA':[0,0,0,0,0,0],'AskIndia':[0,0,0,0,0,0],'Business/Finance':[0,0,0,0,0,0],'Entertainment':[0,0,0,0,0,0],'Food':[0,0,0,0,0,0],'Lifehacks':[0,0,0,0,0,0],'Non-Political':[0,0,0,0,0,0],'Photography':[0,0,0,0,0,0],'Policy/Economy':[0,0,0,0,0,0],'Politics':[0,0,0,0,0,0],'Science/Technology':[0,0,0,0,0,0],'Sports':[0,0,0,0,0,0],'[R]eddiquette':[0,0,0,0,0,0]}
for i in list2:
    # i.strip("\n")
    record=i.split(";")
    # print(record)
    flair=record[0]
    for j in range(1,7):
        if j==4 or j==6:
            record[j].strip("\n")
            if record[j]=="False" or record[j]=="False\n":
                actualLabels[flair][j-1]+=1
        else:
            actualLabels[flair][j-1]+=float(record[j])
actualLabels[flair][2]=actualLabels[flair][2]//len(list2)
print(actualLabels)
