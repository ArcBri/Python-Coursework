import sys

ipbit=sys.argv[1]

ipbit1 = ipbit[0:8]
ipbit2 = ipbit[8:16]
ipbit3 = ipbit[16:24]
ipbit4 = ipbit[24:]
def ipconvert(f):
    f=(int(f[0])*128)+(int(f[1])*64)+(int(f[2])*32)+(int(f[3])*16)+(int(f[4])*8)+(int(f[5])*4)+(int(f[6])*2)+(int(f[7])*1)
    return f

ipbit1 = ipconvert(ipbit1)
ipbit2 = ipconvert(ipbit2)
ipbit3 = ipconvert(ipbit3)
ipbit4 = ipconvert(ipbit4)

s=".";
seq=(str(ipbit1),str(ipbit2),str(ipbit3),str(ipbit4));
ipadd=s.join(seq)
print(ipadd)