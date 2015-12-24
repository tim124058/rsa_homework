#!/usr/bin/env python3
import random

def rnd_n_bit(n):
    a="1"
    for i in range(n-2):
        a+=str(random.randint(0,1))
    return a+"1"


def MillerRabin(n,t):
    """
    n為要測試的數
    t為要測試幾次
    """
    if n==2:return True
    if n%2==0:return False
    k,m=0,n-1
    while ((m%2)==0):       #找出k 和 m
        k=k+1
        m=int(m/2)

    for i in range(0,t):
        a = random.randint(2,n-2)
        b = pow(a,m,n)
        if (b != 1) and (b != n-1):
            for j in range(1,k):
                b = (b**2) % n
                if (b == 1) return False
                elif (b == n-1) break
            else:
                return False
    return True

rsaLen = int(input("請輸入rsa的bit數 : "))

