#***REZULTATI OVOG PROGRAMA SU SLIKE IMENA DDD_...***
#***REZULTAT OCITAVANJE INFORMACIJE ODLICAN***



# import pylab
import numpy as np
import time
import socket
import matplotlib.pyplot as plt
import scipy


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('192.168.50.60', 3000))

    # sock.setblocking(1)
    # sock.settimeout(2)

    # sock.sendall(b'*RST\r\n')
    sock.sendall(b':DATA:WAVE:SCREEN:HEAD?\r\n')
    time.sleep(2)
    data = sock.recv(2048)
    print(data)
    sock.sendall(b':DATA:WAVE:SCREEN:CH1?\r\n')
    time.sleep(4)
    data = sock.recv(10000)

    #data_ je niz dekodovane informacije poslate sa osciloskopa
    data_ = []

    #krece da cita 2. i 3. bit jer prva dva nose informaciju o granicama 
    for c1, c2 in zip(data[10::2], data[11::2]):
        data_.append(c1 + 2**8 * c2)

    #d je broj poslatih informacije 1520+2
    d=len(data_)
    
    #print("***RAW DATA***")

    data_s=[]
    for i in range(d):
        data_s.append(data_[i])
    data_s.sort()

    mini=data_s[10]
    #print(mini)
    maks=data_s[d-10-1]
    
    for i in range(d):
        data_[i]=data_[i]-mini

    for i in range(d):
        if (data_[i]>=maks-mini):
            data_[i]=5
        elif (data_[i]<=0):
            data_[i]=0
        else:
            data_[i]=data_[i]*5/(maks-mini)
    #print("***SKALIRANA DATA***")
    #print(data_)
        

    numeracija= []
    for i in range(d):
        numeracija.append(i)

    for i in range(d):
        if(data_[i]>1.8 and data_[i]<3):
            data_[i]=2.5
       
    #print(data_)

    pikovi=[]
    j=0
    i=0
    while(i<d):
        if(data_[i]!=2.5):
            start=i
            j=i
            num_of_prev=0
            while(num_of_prev!=4):
                if(data_[j]==2.5):
                    num_of_prev=num_of_prev+1
                else:
                    num_of_prev=0
                j=j+1
            pikovi.append([i,j-4-1])
            i=j
        else:
            i=i+1
    
    #print(pikovi)


    #data_=np.array(data_)
    #plt.hist(np.diff(data_))

    for i in range(d):
        if(data_[i]==2.5):
            data_[i]='a'

    rastojanja=[]
    pozicije=[]
    for par in pikovi:
        i=par[0]
        maks=0
        mini=0
        while (i!=par[1]+1):
            if(data_[i]!='a'):
                if (data_[i]>2.5):
                    maks=max(maks,data_[i]-2.5)
                elif(data_[i]<2.5):
                    mini=max(mini,2.5-data_[i])
            i=i+1
        
        
        i=par[0]
        rastojanja.append([maks,mini])
        while(i!=par[1]+1):
            if(data_[i]!='a'):
                if (data_[i]>2.5):
                    if (data_[i]-2.5!=maks):
                        data_[i]='a'
                    else:
                        p1=i
                elif(data_[i]<2.5):
                    if (2.5-data_[i]!=mini):
                        data_[i]='a'
                    else:
                        p2=i

            i=i+1
        pozicije.append([p1,p2])


    #print("***PAROVI[MAKSIMALANI_POZITIVNI_PIK,MAKSIMALNI_NEGATIVNI_PIK]***")
    #print(rastojanja)
    #print("***PAROVI[POZICIJA_MPP,POZICIJA_MNP]***")
    #print(pozicije)

    #znam da moze od jednom ali ovako je lakse za debagovanje raw date
    #print("***DATA SA IZBRISANIM MANJIM PIKOM***")
    for mesto in pozicije:
        if(data_[mesto[0]]-2.5>2.5-data_[mesto[1]]):
            data_[mesto[1]]='a'
        else:
            data_[mesto[0]]='a'

    
    duzina=[]
    i=0
    while (i<d):
        if(data_[i]!='a'):
            j=i+1
            while(j<d and data_[j]=='a'):
                j=j+1
            duzina.append(j-i-1)
            i=j
        else:
            i=i+1
    
    #print(duzina)
        



    visina=[]
    k=1
    kombo=[]
    for par in rastojanja:
        if(par[0]>par[1]):
            #print(duzina[k])
            #k=k+1
            #print("UP")
            if(k<len(duzina)):
                kombo.append([1,duzina[k]])
            k=k+1
            visina.append("UP")
        else:
            #print(duzina[k])
            #k=k+1
            #print("DOWN")
            if(k<len(duzina)):
                kombo.append([0,duzina[k]])
            k=k+1
            visina.append("DOWN")

    #print(data_)
    print(kombo)

    #print("PROMENA SMERA UP - SA 0 NA 1 ---- DOWN - SA 1 NA 0")
    #print(visina)            

    #SADA IZ DATA_ OSTAVIMO SAMO VECI PIK

    for i in range (d):
        if (data_[i]=='a'):
            data_[i]=2.5
    
    #print(data_)

    plt.plot(numeracija,data_)




    zeros=0
    ones=0
    num_of_data=[]
    prev=data_[0]    


    sock.close()


plt.savefig("DDD_DetekcijaPEakova_2.png")
 