#***REZULTATI OVOG PROGRAMA SU SLIKE IMENA BBB_...***
#***REZULTAT OCITAVANJE INFORMACIJE ODLICAN***



# import pylab
import numpy as np
import time
import socket
import matplotlib.pyplot as plt

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

    print("***RAW DATA***")
    print(data_)
        

    numeracija= []
    for i in range(d):
        numeracija.append(i)

    plt.plot(numeracija,data_, )


    data_s=[]
    for i in range(d):
        data_s.append(data_[i])
    data_s.sort()

    mini=data_s[10]
    print(mini)
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
    print("***SKALIRANA DATA***")
    print(data_)

    for i in range(d):
        if(data_[i]<=2):
            data_[i]=0
        else:
            data_[i]=5

    print("***ZAOKRUZENA DATA***")
    print(data_)

    zeros=0
    ones=0
    num_of_data=[]
    prev=data_[0]    

    for i in range(d):
        if (prev!=data_[i]):
            if (prev==0):
                num_of_data.append([0,zeros+1])
                zeros=0
            else:
                num_of_data.append([1,ones+1])
                ones=0
        elif(i!=0):
            if(prev==0):
                zeros=zeros+1
            else:
                ones=ones+1
        prev=data_[i]

    print("***PAROVI OBLIKA [BIT,BROJ_PONAVLJANJA]***")
    print (num_of_data)


    sock.close()


plt.savefig("pfe3.png")
 