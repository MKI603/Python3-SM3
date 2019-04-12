# -*-coding:utf-8-*-
"""
author: Mki603
date: 2019/04/12
about: SM3
"""

def Fill(text):
    """
    消息填充
    """
    text_bin = ''
    # text to bin
    for ch in text:
        ascii_ch = ord(ch)
        text_bin = text_bin + '0' + bin(ascii_ch)[2:]

    # add 1
    length = len(text_bin)

    text_bin = text_bin + '1'

    # add 0
    while len(text_bin)%512!=448:
        text_bin += '0'
    length_bin = bin(length)[2:]

    while len(length_bin)<64:
            length_bin = '0' + length_bin

    text_bin = text_bin + length_bin

    return text_bin


def Iteration(m,w):
    """
    消息迭代
    """
    IV = {}
    IV[0] = '7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
    length = len(m)
    n = length//512
    b = {}
    for i in range(n):
        b[i] = m[512*i:512*(i+1)]
        w = Expand(b[i])
        IV[i+1] = Compress(w,IV[i])
    # print(b)
    return IV[n]



def Mod32(a,b):
    """
    + mod32算术加 Done
    """
    c = (a + b)
    d = c%(2**32)
    ans = str(d)
    return ans



def Move(text, num):
    """
    循环左移函数 done
    Move('1234567',3)
    """
    text = str(text)
    return (text[num:] + text[:num])



def Xor(a,b):
    """
    位异或函数 done
    """
    result =''
    if len(a)!=len(b):
        print('len(a)!=len(b)')
        return False
    for i in range(len(a)):
        if a[i]==b[i]:
            result += '0'
        else:
            result += '1'
    return result


def Xor3(a,b,c):
    """
    三个值进行异或 Done
    """
    return Xor(Xor(a,b),c)


def Or(a,b):
    """
    位或函数
    """
    result =''
    if len(a)!=len(b):
        print('len(a)!=len(b)')
        return False
    for i in range(len(a)):
        if (a[i]=='1')|(b[i]=='1'):
            result += '1'
        else:
            result += '0'
    return result

def Or3(a,b,c):
    return Or(Or(a,b),c)


def And(a,b):
    """
    位与函数
    """
    result =''
    if len(a)!=len(b):
        print('len(a)!=len(b)')
        return False
    for i in range(len(a)):
        if (a[i]=='1')&(b[i]=='1'):
            result += '1'
        else:
            result += '0'
    return result

def And3(a,b,c):
    return And(And(a,b),c)


def Not(a):
    """
    非函数
    """
    result = ''
    for ch in a:
        if ch == '1':
            result = result + '0'
        else:
            result = result + '1'
    return result



def Substitute(x, mode):
    """
    置换函数 done
    """
    if mode == 0:
        ans = Xor3(x,Move(x,9),Move(x,17))
    else:
        ans = Xor3(x,Move(x,15),Move(x,23))
    return ans


def ZtoH(text):
    """
    给Expand函数用的进制转换
    """
    text = str(text)
    while len(text)<32:
        text = '0' + text
    text_16 = ''
    for i in range(8):
        tmp = hex(int(text[4*i:4*(i+1)],base = 2))[2:]
        text_16 = text_16 + tmp   
    return text_16

def BtoH(text):
    text = str(text)
    while len(text)<32:
        text = '0' + text
    text_16 = ''
    for i in range(len(text)//4):
        tmp = hex(int(text[4*i:4*(i+1)],base = 2))[2:]
        text_16 = text_16 + tmp
    return text_16

# 16进制转2进制
def HtoB(text):
    text_2 = ''
    text = str(text)
    for ch in text:
        tmp = bin(int(ch ,base = 16))[2:]
        for i in range(4):
            if len(tmp)%4!=0:
                tmp = '0' + tmp
        text_2 = text_2 + tmp   
    while len(text_2)<32:
        text_2 = '0' + text_2      
    return text_2

# 10进制转2进制
def OtoB(text):
    text_10 = ''
    text = str(text)
    tmp = bin(int(text ,base = 10))[2:]
    text_10 = text_10 + tmp  
    while len(text_10)<32:
        text_10 = '0' + text_10      
    return text_10

def OtoH(text):
    text_10 = ''
    text = str(text)
    tmp = hex(int(text ,base = 10))[2:]
    text_10 = text_10 + tmp     
    while len(text_10)<8:
        text_10 = '0' + text_10   
    return text_10



def Expand(b):
    """
    消息拓展 done
    """
    w = {}
    for i in range(16):
        w[i] = b[i*32:(i+1)*32]
    for j in range(16, 68):
        tmp = Xor3(w[j-16],w[j-9],Move(w[j-3],15))
        tmp = Substitute(tmp, 1) 
        w[j] = Xor3(tmp, Move(w[j-13],7), w[j-6])
    for j in range(64):
        w[j+68] = Xor(w[j],w[j+4])
    for i in w:
        w[i] = ZtoH(w[i])
    return w


"""
布尔函数FF GG
"""
def FF(x,y,z,j):
    if((j>=0)&(j<=15)):
        ans = Xor3(x,y,z)
    else:
        ans = Or3(And(x,y),And(x,z),And(y,z))
    return ans


def GG(x,y,z,j):
    if((j>=0)&(j<=15)):
        ans = Xor3(x,y,z)
    else:
        ans = Or(And(x,y),And(Not(x),z))
    return ans



def Compress(w,IV):
    """
    消息压缩
    """
    A = IV[0:8]
    B = IV[8:16]
    C = IV[16:24]
    D = IV[24:32]
    E = IV[32:40]
    F = IV[40:48]
    G = IV[48:56]
    H = IV[56:64]

    SS1 = ''
    SS2 = ''
    TT1 = ''
    TT2 = ''
    
    for j in range(64):
        if int(j)<=15:
            T = '79cc4519' 
        else:
            T = '7a879d8a'

        tmp = int(Move(HtoB(A),12), 2) + int(HtoB(E), 2) + int(Move(HtoB(T),j%32), 2) 
        tmp = Mod32(tmp, 0)
        SS1 = Move(OtoB(tmp), 7)
        SS2 = Xor(SS1, Move(HtoB(A),12))


        tmp = int(FF(HtoB(A),HtoB(B),HtoB(C),j),2) + int(HtoB(D),2) + int(SS2,2) + int(HtoB(w[j+68]),2)
        tmp = Mod32(tmp,0)
        TT1 = int(tmp,10)


        tmp = int(GG(HtoB(E),HtoB(F),HtoB(G),j),2) + int(HtoB(H),2) + int(SS1,2) + int(HtoB(w[j]),2)
        tmp = Mod32(tmp,0)
        TT2 = int(tmp,10)

        D = C

        C = ZtoH(Move(HtoB(B),9))

        B = A

        A = OtoH(TT1)

        H = G

        G = ZtoH(Move(HtoB(F),19))

        F = E

        E = ZtoH(Substitute(OtoB(TT2),0))

    r = A+B+C+D+E+F+G+H
    r = HtoB(r)
    v = HtoB(IV)
    return BtoH(Xor(r,v))

if __name__ == "__main__":
    c = 'abc' # 要加密的内容
    m = Fill(c)
    w = Expand(m)
    b = Iteration(m,w)
    print(b)




