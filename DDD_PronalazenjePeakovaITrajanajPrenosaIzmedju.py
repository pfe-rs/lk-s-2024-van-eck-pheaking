#***REZULTATI OVOG PROGRAMA SU SLIKE IMENA DDD_...***
#***REZULTAT OCITAVANJE INFORMACIJE ODLICAN***



# import pylab
import numpy as np
import time
import socket
import matplotlib.pyplot as plt
import scipy


def to_decimal(x):
    a=1
    rez=0
    for i in range(0, len(x)):
        if x[i]=='1':
            rez+=a
        a*=2
    return rez

def find_encoded_word(bits):
    # Convert the bit sequence to a string for easier manipulation
    bit_string = ''.join(map(str, bits))
    bit_string = '0' + bit_string + '111'
    
    #print(bit_string)
    # Length of a complete block
    block_length = 12
    
    longest_word = []

    # Loop over the bit string to find the pattern
    for start in range(len(bit_string) - block_length + 1):
        current_word = []
        #print(start)
        for i in range(start,len(bit_string) - block_length + 1, 12):
            print(start, i, bit_string[i], bit_string[i+9:i+12])
            if bit_string[i]!='0':
                break
            if bit_string[i+9:i+12]!='111':
                break
            current_word.append(bit_string[i+1:i+9])
        if len(current_word) > len(longest_word):
            longest_word=current_word

    print(longest_word)    
    final_string=""
    for letter in longest_word:
        final_string+= chr(to_decimal(letter))
    return final_string


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
    for c1, c2 in zip(data[4::2], data[5::2]):
        data_.append(c1 + 2**8 * c2)

    #d je broj poslatih informacije 1520+2
    d=len(data_)
    
    #print("***RAW DATA***")
    print(data_)
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
        if(data_[i]>1.8 and data_[i]<3.2):
            data_[i]=2.5
       
    print(data_)
    pikovi=[]
    j=0
    i=0
    while(i<d):
        if(data_[i]!=2.5):
            j=i
            num_of_prev=0
            while(num_of_prev!=5 and j<d):
                if(data_[j]==2.5):
                    num_of_prev=num_of_prev+1
                else:
                    num_of_prev=0
                j=j+1
            pikovi.append([i,j-4-1])
            i=j
        else:
            i=i+1
    print(pikovi)


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


    print("***PAROVI[MAKSIMALANI_POZITIVNI_PIK,MAKSIMALNI_NEGATIVNI_PIK]***")
    print(rastojanja)
    print("***PAROVI[POZICIJA_MPP,POZICIJA_MNP]***")
    print(pozicije)

    #znam da moze od jednom ali ovako je lakse za debagovanje raw date
    #print("***DATA SA IZBRISANIM MANJIM PIKOM***")
    for mesto in pozicije:
        print(mesto)
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
    if (rastojanja[0][0]>rastojanja[0][1]):
        if(duzina[0]>=19):
            kombo.append([0,duzina[0]])
    else:
        if(duzina[1]>=19):
            kombo.append([1,duzina[1]])
    
    for par in rastojanja:
        if(par[0]>par[1]):
            #print(duzina[k])
            #k=k+1
            #print("UP")
            if(k<len(duzina)):
                if(duzina[k]>=19):
                    kombo.append([1,duzina[k]])
            k=k+1
            visina.append("UP")
        else:
            #print(duzina[k])
            #k=k+1
            #print("DOWN")
            if(k<len(duzina)):
                if(duzina[1]>=19):
                    kombo.append([0,duzina[k]])
            k=k+1
            visina.append("DOWN")
    #print(kombo)
    #print(data_)
    patern1=[]
    patern2=[]
    for i in range(len(kombo)):
        if (i%2==1):
            patern1.append(0)
        else:
            patern1.append(1)
    for i in range(len(kombo)):
        if (i%2==1):
            patern2.append(1)
        else:
            patern2.append(0)
    


    ok=0
    for i in range(len(kombo)):
        if (kombo[i][1]>190):
            if (patern1[i]==1):
                for j in range(len(kombo)):
                    kombo[j][0]=patern1[j]
            else:
                for j in range(len(kombo)):
                    kombo[j][0]=patern2[j]
            ok=1

    if (ok!=1):
        greska1=0
        greska2=0
        for i in range(len(kombo)):
            if (kombo[i][0]!=patern1[i]):
                greska1=greska1+1

        for i in range(len(kombo)):
            if (kombo[i][0]!=patern2[i]):
                greska2=greska1+2
        print(greska2,greska1)
        if (greska1>greska2):
            for i in range(len(kombo)):
                kombo[i][0]=patern1[i]
        else:
            for i in range(len(kombo)):
                kombo[i][0]=patern2[i]

    #print("PROMENA SMERA UP - SA 0 NA 1 ---- DOWN - SA 1 NA 0")
    #print(visina)


    print(kombo)            

    #SADA IZ DATA_ OSTAVIMO SAMO VECI PIK

    for i in range (d):
        if (data_[i]=='a'):
            data_[i]=2.5
    
    #print(data_)

    rezultat=[]
    for par in kombo:
        brpn=par[1]/19.9
        i=1
        if(brpn<6):
            if(brpn>5):
                brpn=par[i]/20.2
            while (i<brpn):
                rezultat.append(par[0])
                i=i+1
        else:
            print(brpn)
            print(par[1]/21.0)
            if(par[1]/21.0>6):
                while(i<par[1]/21):
                    rezultat.append(par[0])
                    i=i+1
            else:
                while(i<=5):
                    rezultat.append(par[0])
                    i=i+1
            
        
    print(rezultat)

    rec=find_encoded_word(rezultat)

    print(rec)
    r=[]
    for i in kombo:
        j=0
        while(j<i[1]):
            if(i[0]==1):
                r.append(5)
            else:
                r.append(0)
            j=j+1
        
    numeracija2=[]
    for i in range(len(r)):
        numeracija2.append(i)
    plt.plot(numeracija2,r)


    p=[]
    for par in kombo:
        j=0
        if (par[0]==1):
            p.append(4)
        else:
            p.append(1)
        while(j<par[1]-1):
            p.append(2.5)
            j=j+1

    numeracija3=[]
    for i in range(len(p)):
        numeracija3.append(i)
    
    plt.plot(numeracija3,p)
    plt.title(rec)


    zeros=0
    ones=0
    num_of_data=[]
    prev=data_[0]    


    sock.close()


print("plotuje ga")
plt.savefig("test.png")
#plt.savefig("DDD_sava_dekodovano.png")
 