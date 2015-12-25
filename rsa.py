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
    result = 1
    for i in range(n-2):
        result*=2
        if random.randint(0,1)==1:
            result+=1
    result = result*2+1
    return result

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




############################
#      ____ _   _ ___      #
#     / ___| | | |_ _|     #
#    | |  _| | | || |      #
#    | |_| | |_| || |      #
#     \____|\___/|___|     #
#                          #
############################


from time import sleep
class RSA_GUI(Frame):
    #按下產生加密資料按鈕(Generate_button)後，產生q,p等加解密所需資料
    def GenerateData(self):
        self.PL.set(0);self.QL.set(0);self.NL.set(0);self.Phi_nL.set(0);self.EL.set(0);self.DL.set(0);self.PlainL.set(0);self.CipherL.set(0)
        self.bit = self.Bit_Entry.get()
        try:
            self.bit = int(self.bit)
            if(self.bit%256 != 0):
                self.Message.set("請輸入256的倍數!")
                return 
        except ValueError:
            self.Message.set("只能輸入數字！請重新輸入")
            return 

        #輸入完成，開始產生p,q
        self.Message.set("正在產生p,q....")
        self.update()  
        print("正在產生p,q....")
        while True:
            self.p = PrimeGenerator(self.bit//2,30)
            self.q = PrimeGenerator(self.bit//2,30)
            self.n = self.p * self.q
            self.phi_n = (self.p-1) * (self.q-1)
            self.e = 65537
            if (self.phi_n % self.e != 0) and (self.p != self.q):
                self.d = modInv(self.e,self.phi_n) 
                break

        self.Cp = SandM(self.q,self.p-2,self.p) * self.q
        self.Cq = SandM(self.p,self.q-2,self.q) * self.p
        self.Message.set("資料產生完成！")
        self.PL.set(self.p);self.QL.set(self.q);self.NL.set(self.n);self.Phi_nL.set(self.phi_n);self.EL.set(self.e);self.DL.set(self.d)
        print("p =",self.p); print("q =",self.q); print("n =",self.n); print("phi_n =",self.phi_n); print("e =",self.e); print("d =",self.d)

    #按下加密(Encode_Button)後，開始對plaintext加密
    def EncodeMethod(self):
        if (self.n == 0):
            self.Message.set("請先產生資料！")
            return

        plaintext = self.show_Plain_Entry.get()
        try:
            plaintext = int(plaintext)
        except ValueError:
            self.Message.set("只能輸入數字！請重新輸入")
            return 

        ciphertext = SandM(plaintext,self.e,self.n)
        self.Message.set("加密完成！")
        self.CipherL.set(ciphertext)
        print("Ciphertext : ",ciphertext)

    #按下解密(Decode_Button)後，開始對ciphertext解密
    def DecodeMethod(self):
        if (self.n == 0):
            self.Message.set("請先產生資料！")
            return
        ciphertext = self.show_Cipher_Entry.get()
        try:
            ciphertext = int(ciphertext)
        except ValueError:
            self.Message.set("只能輸入數字！請重新輸入")
            return 

        plaintext = CRT(ciphertext,self.p,self.q,self.d,self.n,self.Cp,self.Cq)
        self.Message.set("解密完成！")
        self.PlainL.set(plaintext)
        print("Plaintext : ",plaintext)

    #初始化變數
    def __init__(self,master=None):
        self.bit=1024
        self.p=0;self.q=0;self.n=0;self.phi_n=0;self.e=65537;self.d=0;
        self.Cp=0;self.Cq=0;
        Frame.__init__(self,master)
        self.grid()
        self.Message = StringVar()
        self.PL = IntVar()
        self.QL = IntVar()
        self.NL = IntVar()
        self.Phi_nL = IntVar()
        self.EL = IntVar()
        self.DL = IntVar()
        self.PlainL= IntVar()
        self.CipherL = IntVar()
        self.createWidgets()

    #新增各種圖形物件
    def createWidgets(self):
        #第一排： Label Entry Button
        self.Bit_Label = Label(self,width=20,height=5,text="請輸入RSA bit數(n的bit數) : ")
        self.Bit_Label.grid(row=0,column=0)
        self.Bit_Entry = Entry(self,width=20,font=("Purisa", 10))
        self.Bit_Entry.focus_set()
        self.Bit_Entry.grid(row=0,column=2,padx=(10,10))
        self.Generate_button = Button(self,text ="產生加密資料",command = self.GenerateData)
        self.Generate_button.grid(row=0,column=4)

        #最後一排：顯示一些訊息
        self.Message_Label = Label(self,width=10,height=5,font=("Purisa",30),text = "Message : ")
        self.Message_Label.grid(row=10,column=0)
        self.showMessage_Label = Label(self,width=40,height=5,font=("Purisa",30),textvariable=self.Message)
        self.showMessage_Label.grid(row=10,column=1,columnspan=9)

        #顯示加解密需要的資料p, q, n, phi_n, e, d
        self.P_Label = Label(self,width=10,text="p = ")
        self.P_Label.grid(row=1,column=0)
        self.show_P_Entry = Entry(self,width=100,font=("Purisa",10),textvariable=self.PL)
        self.show_P_Entry.grid(row=1,column=1,columnspan=9)

        self.Q_Label = Label(self,width=10,text="q = ")
        self.Q_Label.grid(row=2,column=0)
        self.show_Q_Entry = Entry(self,width=100,font=("Purisa",10),textvariable=self.QL)
        self.show_Q_Entry.grid(row=2,column=1,columnspan=9)

        self.N_Label = Label(self,width=10,text="n = ")
        self.N_Label.grid(row=3,column=0)
        self.show_N_Entry = Entry(self,width=100,font=("Purisa",10),textvariable=self.NL)
        self.show_N_Entry.grid(row=3,column=1,columnspan=9)

        self.Phi_n_Label = Label(self,width=10,text="phi_n = ")
        self.Phi_n_Label.grid(row=4,column=0)
        self.show_Phin_Entry = Entry(self,width=100,font=("Purisa",10),textvariable=self.Phi_nL)
        self.show_Phin_Entry.grid(row=4,column=1,columnspan=9)

        self.E_Label = Label(self,width=10,text="e = ")
        self.E_Label.grid(row=5,column=0)
        self.show_E_Entry = Entry(self,width=100,font=("Purisa",10),textvariable=self.EL)
        self.show_E_Entry.grid(row=5,column=1,columnspan=9)

        self.D_Label = Label(self,width=10,text="d = ")
        self.D_Label.grid(row=6,column=0)
        self.show_D_Entry = Entry(self,width=100,font=("Purisa",10),textvariable=self.DL)
        self.show_D_Entry.grid(row=6,column=1,columnspan=9)


        #輸入明文或顯示解密後的明文
        self.Plain_Label = Label(self,width=10,text="PlainText = ")
        self.Plain_Label.grid(row=7,column=0,pady=(50,10))
        self.show_Plain_Entry = Entry(self,width=100,font=("Purisa",10),textvariable=self.PlainL)
        self.show_Plain_Entry.grid(row=7,column=1,columnspan=9,pady=(50,10))

        #輸入明文後，按的加密按鈕
        self.Encode_Button = Button(self,width=10,font=("Purisa",20),text = "加密",command = self.EncodeMethod)
        self.Encode_Button.grid(row=8,column=2,pady=(20,20))
        #輸入密文後，按的解密按鈕
        self.Decode_Button = Button(self,width=10,font=("Purisa",20),text = "解密",command = self.DecodeMethod)
        self.Decode_Button.grid(row=8,column=4,pady=(20,20))

        #輸入明文或顯示解密後的明文
        self.Cipher_Label = Label(self,width=10,text="CipherText = ")
        self.Cipher_Label.grid(row=9,column=0)
        self.show_Cipher_Entry = Entry(self,width=100,font=("Purisa",10),textvariable=self.CipherL)
        self.show_Cipher_Entry.grid(row=9,column=1,columnspan=9)



if __name__ == '__main__':
    root = Tk()
    root.title("RSA")
    app = RSA_GUI(master=root)
    app.mainloop()


