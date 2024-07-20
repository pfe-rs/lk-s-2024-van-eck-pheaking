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
    
    #ucitavanje podataka VanEck
    sock.sendall(b':DATA:WAVE:SCREEN:CH1?\r\n')
    time.sleep(4)
    data = sock.recv(10000)

    #ucitavanje podataka Direkt
    sock.sendall(b':DATA:WAVE:SCREEN:CH2?\r\n')
    time.sleep(4)
    data2 = sock.recv(10000)


    data_ = []
    data1 = []
    data2 = []

    data_c2 = []
    data1c2 = []
    data2c2 = []


    for c1, c2 in zip(data[10::2], data[11::2]):
        data_.append(c1 + 2**8 * c2)
        data1.append(c1)
        data2.append(c2)
    print(len(data))
    data_ = np.array(data_)
    data_ = np.where(data_ < 2**15, 2**16+data_ , data_) - 2**16
    data_ = -data_

    for c1, c2 in zip(data2[10::2], data2[11::2]):
        data_c2.append(c1 +  2**8 * c2)
        data1c2.append(c1)
        data2c2.append(c2)
    print("data2" ,len(data2))

    data_c2 = np.array(data_c2)
    data_c2 = np.where(data_c2 < 2**15, 2**16+data_c2 , data_c2) - 2**16
    data_c2 = -data_c2
    
    d=len(data_)
    numeracija = []
    for i in range(d):
        numeracija.append(i)
    numeracija2 = []
    for i in range(d//2-1):
        numeracija2.append(i)
    print(len(data_c2))

    fig1,(g1,g2,g,g1c2,g2c2,gc2)= plt.subplots(6)
    g1.plot(numeracija,data1)
    g2.plot(numeracija,data2)
    g.plot(numeracija,data_)
    g1c2.plot(numeracija2,data1c2)
    g2c2.plot(numeracija2,data2c2)
    gc2.plot(numeracija2,data_c2)


    data_s=[]
    for i in range(d):
        data_s.append(data_[i])
    data_s.sort()

    #plt.plot(numeracija, filterd_data)

    sock.close()


plt.savefig("Knali.png")
 