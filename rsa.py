#!/usr/bin/env python3
import random

#產生n bit的奇數
def rnd_n_bit(n):
    a="1"
    for i in range(n-2):
        a+=str(random.randint(0,1))
    a+="1"
    return int(a,2)

#測試是否不是質數，n為要測試的數，t為測試的次數
def MillerRabin(n,t):
    if n < 2: return False
    if n==2 or n==3:return True
    if n%2==0:return False
    k,m=0,n-1
    while ((m%2)==0):       #找出k 和 m
        k+=1
        m>>=1

    for i in range(0,t):
        a = random.randint(2,n-2)
        b = pow(a,m,n)
        if (b != 1) and (b != n-1):
            for j in range(1,k):
                b = (b**2) % n
                if b == 1: return False
                elif(b == n-1): break
            else:
                return False
    return True

#產生b bit的質數，測試次數為t
def PrimeGenerator(b,t):
    while True:
        rnd = rnd_n_bit(b)
        if MillerRabin(rnd,t) == True:
            return rnd


#輸入bit
while True:
    bit = input("請輸入rsa的bit數：")
    try:
        bit = int(bit)
        if(bit%256 == 0):
            print("輸入成功....")
            break
        else:
            print("請輸入256的倍數!\n")
    except ValueError:
        print("只能輸入數字喔！請重新輸入\n")

#產生p,q
p = PrimeGenerator(bit//2,4)
q = PrimeGenerator(bit//2,4)
n = p * q
phi_n = (p-1) * (q-1)
print("p = ",p)
print("q = ",q)
print("n = ",n)
