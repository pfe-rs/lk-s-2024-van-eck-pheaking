# import usbtmc
# import pylab
import numpy as np
# from biblioteka import *
import time
import socket
import matplotlib.pyplot as plt
def IsStart(data_pair,i):
    if(i!=0):
        print(data_pair[i])
        if(data_pair[i][0]==0 and data_pair[i][1]==1):
            if(data_pair[i-1][1]>=8):
                return True
    return False
def findMessage(data_list,start):
    curr_message=[]
    n=0
    i=0
    niz=[]
    while n<8: 
        if (start+i<len(data_list)):
            if(i!=0):
                br=data_list[start+i][1]
                if(n+br>8):
                    for j in range(8-n):
                        niz.append(data_list[start+i][0])
                    n=8
                else:
                    for j in range(br):
                        niz.append(data_list[start+i][0])
                    n=n+br

        i=i+1
    print(niz)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('192.168.50.60', 3000))

    # sock.setblocking(1)
    # sock.settimeout(2)

    # sock.sendall(b'*RST\r\n')
    sock.sendall(b':DATA:WAVE:SCREEN:HEAD?\r\n')
    time.sleep(2)
    data = sock.recv(2048)
    print(data)
    sock.sendall(b':DATA:WAVE:SCREEN:CH2?\r\n')
    time.sleep(4)
    data = sock.recv(10000)
    #print(data)

    print(data)
    #print(len(data))

  

    data_ = []

    for c1, c2 in zip(data[0::2], data[1::2]):
        data_.append(c2 + 2**8 * c1)

    
    d=len(data_)
    numeracija= []




    data_s=[]
    for i in range(d):
        data_s.append(data_[i])
    data_s.sort()
    print (data_)
    #print (data_s)

    mini=data_s[50]
    print(mini)
    maks=data_s[d-50-1]
    #summ=0
    #summa=0
    #for i in range(100):
     #   summ=data_s[i]+summ
    #mini=sum/100

    #for i in range(100):
     #  summa=data_s[d-i-1]+summa
    #maks=summa/100

    print (maks)
    print (mini)

    #print(d)
    #print(data_s)
    
    for i in range(d):
        data_[i]=data_[i]-mini
    
    #print(data_s)
    
    for i in range(d):
        if (data_[i]>=maks-mini):
            data_[i]=5
        elif (data_[i]<=0):
            data_[i]=0
        else:
            data_[i]=data_[i]*5/(maks-mini)
    
    print(data_)

    for i in range(d):
        if(data_[i]<=2):
            data_[i]=0
        else:
            data_[i]=5

    zeros=0
    ones=0
    num_of_data=[]
    prev=data_[0]    
    
    #print(data_)

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
    fixed=[]
    print (num_of_data)
    #print(IsStart(num_of_data,8))
    for i in range(len(num_of_data)):
        if(num_of_data[i][1]>10):
            fixed.append(num_of_data[i])
    #findMessage(num_of_data,8)
    print("NakonFilteraGreske",)
    print(fixed)  

    for i in range(d):
        numeracija.append(i)


    for i in range(len(data_)):
        if (data_[i]==0):
            data_[i]=5
        else:
            data_[i]=0


            
    plt.plot(numeracija,data_ )


    sock.close()

#plt.hist(data_)


plt.savefig("pfe2.png")
    



