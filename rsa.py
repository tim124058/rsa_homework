#!/usr/bin/env python3
import random
from tkinter import *

#用Square-and-Multiply計算(a**b)%m
def SandM(a,b,m):
    result = a
    for i in bin(b)[3:]:
        result = (result*result) % m
        if i == '1':
            result = (result*a) % m
    return result

#產生n bit的奇數
def rnd_n_bit(n):
    a = 1
    for i in range(n-2):
        a*=2
        if random.randint(0,1)==1:
            a+=1
    a = a*2+1
    return a

#測試是否不是質數，n為要測試的數，t為測試的次數
def MillerRabin(n,t):
    if n < 2: return False
    if n==2 or n==3:return True
    if n%2==0 or n%5==0:return False
    k,m=0,n-1
    while ((m%2)==0):       #找出k 和 m
        k+=1
        m//=2

    for i in range(0,t):
        a = random.randint(2,n-2)
        b = SandM(a,m,n)
        if (b != 1) and (b != n-1):
            for j in range(1,k):
                b = (b*b) %n
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


#找e在mod m下的反函數(d)
def modInv(e,m):
    #歐幾里德擴展公式
    def Ext_Euclid(a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = Ext_Euclid(b % a, a)
            return g, x - (b // a) * y, y
    return Ext_Euclid(e,m)[1] % m


#CRT加速
def CRT(x,p,q,d,n,Cp,Cq):
    Yp = SandM(x % p, d % (p-1), p)
    Yq = SandM(x % q, d % (q-1), q)
    return (Cp*Yp+Cq*Yq) % n


##輸入bit
#while True:
    #bit = input("請輸入rsa的bit數：")
    #try:
        #bit = int(bit)
        #if(bit%256 == 0):
            #print("輸入成功....\n")
            #break
        #else:
            #print("請輸入256的倍數!\n")
    #except ValueError:
        #print("只能輸入數字！請重新輸入\n")

##產生p,q
#print("正在產生p,q....")
#while True:
    #p = PrimeGenerator(bit//2,30)
    #q = PrimeGenerator(bit//2,30)
    #n = p * q
    #phi_n = (p-1) * (q-1)
    #e = 65537
    #if phi_n % e != 0:
        #d = modInv(e,phi_n) 
        #break

#Cp = SandM(q,p-2,p) * q
#Cq = SandM(p,q-2,q) * p
#print("p = ",p)
#print("q = ",q)
#print("n = ",n)
#print("phi_n = ",phi_n)
#print("e = ",e)
#print("d = ",d)



#while True:
    #plaintext = int(input("\n\n請輸入明文 : "))

    #cipher = SandM(plaintext,e,n)
    #print("Ciphertext : ",cipher)


    #plain = CRT(cipher,p,q,d,n,Cp,Cq)
    #print("Plaintext : ",plain)






############################
#      ____ _   _ ___      #
#     / ___| | | |_ _|     #
#    | |  _| | | || |      #
#    | |_| | |_| || |      #
#     \____|\___/|___|     #
#                          #
############################

root = Tk()
root.title("RSA")

Bit_Label = Lable(root,width=10,height=5,text="請輸入RSA bit數(n的bit數) : ")
Bit_Label.grid(row=0,column=0)
bit=IntVar()
Bit_Entry = Entry(root,width=20,font=("Purisa", 10),textvariable=bit)
Bit_Entry.focus_set()
Bit_Entry.grid(row=0,column=1,columnspan=6,padx=(10,40))

Generate_button = Button(root,text ="產生加密資料" )




root.mainloop()


