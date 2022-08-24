import os
import json


info = {}

def clearScreen():
    print(str(os.system("cls" if os.system == "nt" else "clear"))[0:0], end="")

ROUTES1 = {
    "香港 -> 珠海": "HKGZHO",
    "珠海 -> 香港": "ZHOHKG",
    "香港 -> 澳门": "HKGMAC",
    "澳门 -> 香港": "MACHKG"
}

ROUTES2 = {
    "HKGZHO": "香港 -> 珠海",
    "ZHOHKG": "珠海 -> 香港",
    "HKGMAC": "香港 -> 澳门",
    "MACHKG": "澳门 -> 香港"
}

def validate_email(email):
    if "@" in email and "." in email:
        return True
    return False

def validate_date(date_):
    date = str(date_)
    if len(date) == 10:
        for char in date:
            if (not char in "1234567890-"):
                return False
        if len(date.split("-")) == 3 and (date[4] == "-" and date[7] == "-"):
            return True
        else:
            return False
    else:
        return False

uname = ""
pwd = ""
route = ""
date = ""
passengers = []
mysendemail = ""
emailreceivers = []
smtppwd = ""
smtphost = ""
smtpport = None
track = ""

myChoice = None

while myChoice != "7":
    clearScreen()
    print("="*20+"金 巴 抢 票 机 器 人 设 置 主 菜 单"+"="*20+'''
    0. 从 文 件 导 入
    1. 显 示 信 息
    2. 添 加 乘 客 （ 同 行 人 ）
    3. 设 置 账 号 登 录 信 息
    4. 设 置 SMTP 信 息 和 电 邮 接 收 人
    5. 设 置 出 发 日 期
    6. 设 置 路 线
    7. 保 存 并 退 出
    8. 输 入 轨 迹
    
    请 输 入 您 的 选 择：''', end="")
    myChoice = input()
    if myChoice == "0":
        clearScreen()
        print("="*20 + "从 文 件 导 入" + "="*20)
        try:
            info = json.loads(open("info.json", "r").read())
            uname = info["uname"]
            pwd = info["pwd"]
            date = info["date"]
            route = info["route"]
            passengers = info["passengers"]
            mysendemail = info["mysendemail"]
            emailreceivers = info["emailreceivers"]
            smtphost = info["smtphost"]
            smtpport = info["smtpport"]
            smtppwd = info["smtppwd"]
            track = info.get("track", "")
            print("        文 件 导 入 成 功！")
            input("按 【 回 车 】 键 返 回 ...")
        except Exception:
            print("        文 件 导 入 失 败！")
            input("按 【 回 车 】 键 返 回 ...")
    if myChoice == "1":
        clearScreen()
        uname2 = "暂 无" if (not validate_email(uname)) else uname
        pwd2 = "暂 无" if pwd == "" else pwd
        route2 = "暂 无" if route == "" else ROUTES2[route]
        date2 = "暂 无" if (not validate_date(date)) else date
        passengers2 = "暂 无"
        if len(passengers) > 0:
            passengers2 = "\n"
            for passenger in passengers:
                passengers2 += "        "
                passengers2 += passenger["userName"] + "    "
                passengers2 += passenger["idCard"] + "    "
                if passenger["ticketType"] == "00":
                    passengers2 += " （成 人 票）"
                elif passenger["ticketType"] == "01":
                    passengers2 += " （优 惠 票）"
                passengers2 += "\n"
        mysendemail2 = "暂 无" if (not validate_email(mysendemail)) else mysendemail
        emailreceivers2 = emailreceivers
        for i in range(len(emailreceivers2)):
            if not validate_email(emailreceivers2[i]):
                emailreceivers2[i] == "暂 无"
        emailreceivers2 = "，".join(emailreceivers2)
        emailreceivers2 = "暂 无" if emailreceivers2 == "" else emailreceivers2
        smtppwd2 = "暂 无" if smtppwd == "" else smtppwd
        smtphost2 = "暂 无" if smtphost == "" else smtphost
        smtpport2 = "暂 无" if smtpport == None else smtpport
        track2 = "暂 无" if track == "" else track
        print("="*20+"信 息" + "="*20+f'''
        请 确 认 以 下 所 有 信 息 完 全 正 确 无 误 ，
        否 则 可 能 无 法 购 票 / 被 拒 登 车 ！

        金 巴 登 录 电 邮： {uname2}
        金 巴 登 录 密 码：{pwd2}
        金 巴 路 线：{route2}
        出 发 日 期：{date2}
        金 巴 乘 客：{passengers2}
        SMTP 发 送 电 邮：{mysendemail2}
        SMTP 接 收 人 电 邮：{emailreceivers2}
        SMTP 密 码：{smtppwd2}
        SMTP 端 口：{smtpport2}
        验 证 码 轨 迹：{track2}
        ''')
        input("按 【 回 车 】 键 返 回 ...")
    if myChoice == "2":
        clearScreen()
        print("="*20 + "添 加 乘 客 （同 行 人）" + "="*20)
        ticketType = None
        while ticketType == None:
            ticketType = input('''
        请 输 入 乘 客 年 龄。
        （00） ： 成 人
        （01） ： 儿 童 / 长 者
        请 输 入 您 的 选 择：''')
            if ticketType != "00" and ticketType != "01":
                ticketType = None
        userName = None
        while userName == None:
            userName = input('''        请 输 入 乘 客 名 称：''')
        idCard = None
        while idCard == None:
            idCard = input('''        请 输 入 乘 客 证 件 号 码：''')
        passengers.append({
          "ticketType": ticketType,
          "idCard": idCard,
          "idType": 1,
          "userName": userName,
          "telNum": ""
        })
    if myChoice == "6":
        myRouteChosen = None
        while myRouteChosen == None:
            try:
                clearScreen()
                print("="*20 + "设 置 路 线" + "="*20)
                myRoutes = list(range(1, len(list(ROUTES1.keys()))+1))
                # print(myRoutes)
                print("        请 选 择 路 线：")
                for routeIndex in myRoutes:
                    myRoute = list(ROUTES1.keys())[routeIndex-1]
                    print(f"        {routeIndex}.    {myRoute}")
                route = int(input("        请 输 入 您 的 选 择："))
                if (not route in myRoutes):
                    myRouteChosen = None
                else:
                    myRouteChosen = ROUTES1[list(ROUTES1.keys())[route-1]]
            except Exception:
                myRouteChosen = None
        route = myRouteChosen
    if myChoice == "3":
        clearScreen()
        print("="*20+"设 置 账 号 登 录 信 息" + "="*20)
        uname = None
        while uname == None:
            uname = input("        请 输 入 金 巴 登 录 电 邮：")
            if not validate_email(uname):
                uname = None
        pwd = None
        while pwd == None:
            pwd = input("        请 输 入 金 巴 登 录 密 码：")
    if myChoice == "4":
        clearScreen()
        print("="*20 + "设 置 SMTP 信 息 和 电 邮 接 收 人" + "="*20)
        smtphost = None
        while smtphost == None:
            smtphost = input("        请 输 入 SMTP 服 务 器：")
        smtpport = None
        while smtpport == None:
            smtpport = int(input("        请 输 入 SMTP 端 口："))
        mysendemail = None
        while mysendemail == None:
            mysendemail = input("        请 输 入 SMTP 发 送 电 邮：")
            if not validate_email(mysendemail):
                mysendemail = None
        smtppwd = None
        while smtppwd == None:
            smtppwd = input("        请 输 入 SMTP 密 码：")
        myemailadd = None
        while myemailadd != "quit":
            myemailadd = input("        请 输 入 电 邮 接 收 人（quit 为退出）：")
            if (not validate_email(myemailadd) and myemailadd != "quit"):
                myemailadd = None
            else:
                if myemailadd != None and myemailadd != "quit":
                    emailreceivers.append(myemailadd)
    if myChoice == "5":
        clearScreen()
        print("="*20 + "设 置 出 发 日 期" + "="*20)
        date = None
        while date == None:
            date = input("        请 输 入 出 发 日 期 （格 式 ：YYYY-MM-DD）：")
            if not validate_date(date):
                date = None
    if myChoice == "7":
        info = {
                "uname": uname,
                "pwd": pwd,
                "route": route,
                "date": date,
                "passengers": passengers,
                "mysendemail": mysendemail,
                "emailreceivers": emailreceivers,
                "smtppwd": smtppwd,
                "smtphost": smtphost,
                "smtpport": smtpport,
                "track": track
            }
        info_json = json.dumps(info, indent=2, ensure_ascii=False)
        with open("info.json", "w") as myinfofile:
            myinfofile.write(info_json)
    if myChoice == "8":
        clearScreen()
        print("="*20 + "导 入 轨 迹" + "="*20)
        track = input("        请 输 入 轨 迹 （可 从 guiji.html 获 取）:")