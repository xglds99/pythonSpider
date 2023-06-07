from socket import *
from sys import *
import time
import signal
import random

##### DECLARATIONS #####
byte = 8
letter = [byte]
sequence_number = [32]
data_packet = []
data_packet_size = len(data_packet)+len(sequence_number)
timeout = 0.5
holder = 0
max_seq = 2**32


##### SENDER #####
def sender(sp, pp, ws, tt, tv):
    ### Declarations
    seq_index = 0

    ### sock init
    sa = ('localhost',sp)
    ra = ('localhost', pp)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(sa)
    buffer_len = ws
    buffer = []

    total = 0
    dead = 0
    while True:
        hold, addr = sock.recvfrom(1024)
        h = hold.decode()
        if h == "alive":
            break

    msg = input("sender> ")
    test3 = []
    for i in msg:
        test3.append(i)
    t3h = 0
    while t3h < len(test3):
        bi = 0
        while len(buffer) < buffer_len:
            seq_index += 1
            if seq_index > max_seq-1:
                seq_index = 1
            m = make(seq_index, msg[i])
            buffer.append(m)
            sock.sendto(m.encode(), ra)
            time.sleep(0.02)
    nah = b"finito"
    sock.sendto(nah, ra)
    print("[Summary] %d/%d packets discarded, loss rate = %f%%"%(dead, total, float((dead/total)*100)))
    

def receiver(rp, pp, ws, tt, tv):
    seq_index = 0

    ### sock init
    sa = ('localhost',pp)
    ra = ('localhost', rp)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ra)
    buffer = [None] * 1

    ## test 1 ##
    print("sending to: ", sa)
    print("Test1")
    hi = b"alive"
    sock.sendto(hi, sa)
    
    dead = 0
    total = 0
    exp_pkg = 1
    while True:
        a, b = sock.recvfrom(1024)
        total += 1
        if(a.decode() == "finito"):
            print("[Summary] %d/%d packets dropped, loss rate = %f%%"%(dead, total, float((dead/total)*100)))
            break
        else:
            decoded = a.decode()
            seq = decoded[0:32]
            packet = decoded[32:40]
            
            fs = bto(seq, False)
            fd = bto(packet, True)
            print("packet %d %s received"%(fs-1, fd))
            # ADD PROBABILITY HERE
            #dead += 1
            sock.sendto(seq.encoded(), sa)
            print("ACK%d sent, expecting packet%d"%(fs-1,fs))


def bto(bi, isData): #bts
    print("this is so frustrating: ", type(bi), bi)
    if not isData:
        returner = int(bi, 2)
    elif isData:
        inp_str = int(bi, 2)
        inp_char = inp_str.to_bytes(1, "big")
        returner = inp_char.decode()
    return returner

def otb(st, isData): #stb
    #st = ord(st)
    if not isData:
        binary = bin(st)[2:].zfill(32)
    elif isData:
        ia = st.encode()
        ba = int.from_bytes(ia, "big")
        binary = bin(ba)[2:].zfill(8)
    return binary

def make(seq, data):
    d = otb(data, True)
    s = otb(seq, False)
    ret = ""
    ret= s + d
    return ret

if __name__ == "__main__":
    sp = int(argv[1])
    pp = int(argv[2])
    ws = int(argv[3])
    pt = argv[4]
    pn = float(argv[5])

    mp = int((sp + pp)/ 2)
    s = socket(AF_INET, SOCK_DGRAM)
    time.sleep(0.5)
    try:
        print("attempting bind...")
        s.bind(('localhost',mp))
        print("no sender yet")
        sender(sp,pp,ws,pt,pn)
    except OSError as e:
        print("sender already alive")
        s.close()
        time.sleep(5)
        receiver(sp,pp,ws,pt,pn)