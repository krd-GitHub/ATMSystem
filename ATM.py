#!/usr/bin/python3
#-*- coding : utf-8 -*-
# krd-dsc   作者
# 2019/7/23  19:42  当前时间
import random
import json
import fileinput
'''
ATM系统
卡：卡号，密码，金额，锁
用户：name，idcard，phonenum，card
ATM系统：
属性：用户列表  登录状态
行为： 1.登陆   2.开户     3.查询   4.取款     5.存款   0.退出
6.转账   7.改密     8.锁卡   9.解锁
'''
class Card:
    def __init__(self,cardNum,Password,money,boolOne=False):
        self.cardNum = cardNum
        self.__Password = Password
        self.__money = money
        self.boolOne = boolOne

    @property
    def Password(self):
        return self.__Password

    @Password.setter
    def Password(self,Password):
        self.__Password = Password

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, money):

        self.__money = money



class User:
    def __init__(self,name,idcard,phonenum,card):
        self.name = name
        self.idcard = idcard
        self.phonenum = phonenum
        self.card = card

def User2dict(User):
    return User.__dict__
def User2User(b):
    return User(b["name"],b["idcard"],b["phonenum"],Card(b["card"]["cardNum"],b["card"]["_Card__Password"],
                                                         b["card"]["_Card__money"],b["card"]["boolOne"]))
def UserA(Num):
    with open("User.txt","r",encoding="utf-8") as f:
        for line in f.readlines():
            dict1 = json.loads(line)
            x = User2User(dict1)
            # print(x.__dict__)
            # print(x.card.__dict__)
            if x.card.cardNum == Num:
                return x
        else:
            return None
def delLine(cardNum1):
    for line in fileinput.input("User.txt",inplace=True):
        if cardNum1 in line:
            pass
        else:
            print(line.rstrip())
def Xg(cardNum1,key,value):
    with open("User.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            dict1 = json.loads(line)
            x = User2User(dict1)
            if x.card.cardNum ==cardNum1:
                dict1["card"][key] = value
                x2 = User2User(dict1)
                return x2
        else:
            return None
# def addObj(cls, obj):
#     with open(cls.path, "a", encoding="utf-8") as f:
#         json.dump(obj, f, default=User2dict)
#         f.write("\n")
class ATM:
    index = 0
    islogin = None
    ATMDict = {}
    path = "User.txt"
    @classmethod
    def getcardnum(cls):
        while True:
            cardnum = ""
            for x in range(6):
                cardnum += str(random.randrange(0,10))
            if cardnum not in cls.ATMDict:
                return cardnum

    @staticmethod
    def welcome():
        print('''
           **********************
           *                    *
           *  welcome to bank   *
           *                    *
           **********************
           ''')

    @staticmethod
    def select():
        print('''
           **********************
           *  1.登陆   2.开户    *
           *  3.查询   4.取款    *
           *  5.存款   0.退出    *
           *  6.转账   7.改密    *
           *  8.锁卡   9.解锁    *
           **********************
           ''')
        num = input("请选择服务项目：")
        return num

    @classmethod
    def addObj(cls, obj):
        with open(cls.path, "a", encoding="utf-8") as f:
            json.dump(obj, f, default=User2dict)
            f.write("\n")

    @classmethod
    def OpenAccount(cls):
        name = input("请输入你的姓名：")
        idcard = input("请输入你的身份证号码：")
        phonenum = input("请输入你的电话号码：")
        password = input("请输入你的银行卡密码：")
        password1 = input("请确认你的银行卡密码：")
        if password == password1:
            cardnum = cls.getcardnum()
            Card1 = Card(cardnum,password1,money=0,boolOne=False)
            User1 = User(name,idcard,phonenum,Card1)
            cls.ATMDict[cardnum] = User1
            cls.addObj(User1)
            print("开户成功！你的卡号为%s,请牢记！"%cardnum)
        else:
            print("开户失败")
    @classmethod
    def Deposit(cls):
        if cls.islogin:
            print("您当前的余额为%d" % UserA(cls.islogin).card.money)
            num = input("请输入存款金额：")
            # UserA(cls.islogin).card.money += int(num)
            Num=UserA(cls.islogin).card.money+int(num)
            m = Xg(UserA(cls.islogin).card.cardNum, "_Card__money",Num)
            delLine(UserA(cls.islogin).card.cardNum)
            ATM.addObj(m)
            print("存款成功！")
        else:
            print("请登陆后存款")

    @classmethod
    def Withdrawal(cls):
        if cls.islogin:
            print("您当前的余额为%d" % UserA(cls.islogin).card.money)
            num = input("请输入取款金额：")
            if UserA(cls.islogin).card.money > int(num):
                # UserA(cls.islogin).card.money -= int(num)
                Num = UserA(cls.islogin).card.money - int(num)
                m = Xg(UserA(cls.islogin).card.cardNum, "_Card__money", Num)
                delLine(UserA(cls.islogin).card.cardNum)
                ATM.addObj(m)
                print("取款成功！")
            else:
                print("余额不足，请重新选择！")
        else:
            print("请登陆后取款")

    @classmethod
    def ChangePassword(cls):
        if cls.islogin:
            psd = input("请输入修改的密码：")
            psd1 = input("请确认修改的密码：")
            if psd == psd1:
                # cls.ATMDict.get(cls.islogin).card.Password = psd1
                m = Xg(UserA(cls.islogin).card.cardNum, "_Card__Password", psd1)
                delLine(UserA(cls.islogin).card.cardNum)
                ATM.addObj(m)
                print("改密成功！")
            else:
                print("改密失败")
        else:
            print("请登陆后改密")



    @classmethod
    def Login(cls):
        cardnum = input("        账号名：")
        user = UserA(cardnum)
        if user:
            if user.card.boolOne == False:
                if user:
                    psd = input("        密码:")
                    if psd == user.card.Password:
                        print("        登陆成功!")
                        cls.islogin = user.card.cardNum
                    else:
                        cls.index += 1
                        if cls.index ==3:
                            print("        你的卡号已经被锁，请联系管理员解锁")
                            m=Xg(user.card.cardNum,"boolOne",True)
                            delLine(user.card.cardNum)
                            ATM.addObj(m)
                        else:
                            print("        登陆失败!你还有%d次机会登陆" % (3 - cls.index))
            else:
                print("        你的卡号已经被锁，请联系管理员解锁")
        else:
            print("        账号名密码错误！")

    @classmethod
    def LockCard(cls):
        if cls.islogin:
            cardnum = input("        请输入你需要锁卡的账号名：")
            user = UserA(cardnum)
            if user:
                m = Xg(user.card.cardNum, "boolOne", True)
                delLine(user.card.cardNum)
                ATM.addObj(m)
                print("        锁卡成功")
            else:
                print("        不存在此卡号！！！")
        else:
            print("请登陆后进行锁卡操作")

    @classmethod
    def UnLock(cls):
        cardnum = input("        请输入你需要解锁的账号名：")
        user = UserA(cardnum)
        if user:
            m = Xg(user.card.cardNum, "boolOne", False)
            delLine(user.card.cardNum)
            ATM.addObj(m)
            print("        解锁成功")
        else:
            print("        不存在此卡号！！！")

    @classmethod
    def search(cls):

        if cls.islogin:
            print("        您当前的余额为%d"%UserA(cls.islogin).card.money)
        else:
            print("        请登陆后查询")

    @classmethod
    def Transfer(cls):
        if cls.islogin:
            cardnum =input("请输入你的转账账户：")
            if UserA(cardnum):
                num = input("请输入转账金额：")

                x=UserA(cls.islogin).card.money - int(num)
                m = Xg(UserA(cls.islogin).card.cardNum, "_Card__money", x)
                delLine(UserA(cls.islogin).card.cardNum)
                ATM.addObj(m)


                x1=UserA(cardnum).card.money + int(num)
                i = Xg(UserA(cardnum).card.cardNum, "_Card__money", x1)
                delLine(UserA(cardnum).card.cardNum)
                ATM.addObj(i)
                print("转账成功")

            else:
                print("不好意思没有此卡信息！")
        else:
            print("        请登陆后进行转账操作")




if __name__ == '__main__':
    ATM1 = ATM()
    ATM1.welcome()
    # try:
    #     with open("User.txt","rb") as f:
    #         ATM1.ATMDict = pickle.load(f)
    # except:
    #     pass
    while True:
        num = ATM1.select()
        if num == "1":
            print("********欢迎进入ATM登陆窗口********")
            ATM1.Login()
        elif num == "2":
            print("        开户")
            ATM1.OpenAccount()
        elif num == "3":
            print("        查询")
            ATM1.search()
        elif num == "4":
            print("        取款")
            ATM1.Withdrawal()
        elif num == "5":
            print("        存款")
            ATM1.Deposit()
        elif num == "6":
            print("        转款")
            ATM1.Transfer()
        elif num == "7":
            print("        改密")
            ATM1.ChangePassword()
        elif num == "8":
            print("        锁卡")
            ATM.LockCard()
        elif num == "9":
            print("        解锁")
            ATM1.UnLock()
        elif num == "0":
            print("退出")
            break
        else:
            print("选择有误，请重新选择...")
