######DICEBOT VER 5.3.1######
##########"PETRAM"###########
##########BY  ZTREN##########
#———————————————————————————#
#MODIIFYING OF THIS FILE IS##
#NOT ADVICED UNLESS YOU KNOW#
######WHAT YOU ARE DOING#####

from wxpy import *
from random import *
from math import *
from time import *
from re import *
from json import *
from copy import *
from threading import *

import os
import WordStr_5_3_1 as WordStr

bot = Bot(cache_path=True)
bot.enable_puid('wxpy_puid.pkl')
group = bot.groups().search(WordStr.GroupName)[0]
CRD = ['AGG','CON','DEX','APP','POW','EXP','ORG','LUK','INT','EDU','SIZ','DUR','SKL','ART']#人物卡

rpt = True#随机复读开关
pu = []#存放用户PUID
nm = []#存放用户名
pl = []#存放用户人物卡
en = []#存放敌方单位数据
rp = []#存放用户人品
dt = strftime("%Y{0}%m{1}%d{2}", localtime()).format('年','月','日')#当前时间
rgnm = False
rgid = -1
ennm = False
enid = -1
Muted = False
TimerOn = False

class pers:
    def __init__(self,AGG,CON,DEX,APP,POW,EXP,ORG,LUK,INT,EDU,SIZ,DUR,SKL,ART,RES):
        self.AGG = AGG
        self.CON = CON
        self.DEX = DEX
        self.APP = APP
        self.POW = POW
        self.EXP = EXP
        self.ORG = ORG
        self.LUK = LUK
        self.INT = INT
        self.EDU = EDU
        self.SIZ = SIZ
        self.DUR = DUR
        self.SKL = SKL
        self.ART = ART
        self.RES = RES
class enemy:
    def __init__(self,NAM,AGG,CON,DEX,RES,DUR,LTN,DMG,DMS):
        self.NAM = NAM
        self.AGG = AGG
        self.CON = CON
        self.DEX = DEX
        self.RES = RES
        self.DUR = DUR
        self.LTN = LTN
        self.DMG = DMG
        self.DMS = DMS
def WakeUp():
    if TimerOn == True:
        if strftime("%H", localtime()) in ['01','04','07']:
            group.send(WordStr.DRM[randint(0,len(WordStr.DRM)-1)] + '#梦话')#1点、4点、7点自动唤醒，避免程序自动睡眠
        Timer(3600,WakeUp).start()

group.send(WordStr.Hello)
@bot.register(group,TEXT)       
def returner(msg):
    global pl,en,rpt,rgnm,rgid,CRD,rp,dt,ennm,enid,Muted
    if (msg.text == '*EXIT*'):#正常退出‘
        TimerOn = False
        group.send(WordStr.Farewell)
        os._exit(0)
    if (msg.text == '*MUTE*'):#静言与解除静言
        Muted = True
        group.send(WordStr.Muted)
    if (msg.text == '*UNMUTE*'):
        Muted = False
        group.send(WordStr.Unmuted)
    if Muted == True:
        return
    if (msg.text == '*TIMER ON*'):#是否开启定时唤醒
        TimerOn = True
        WakeUp()
        group.send(WordStr.TimerOn)
    if (msg.text == '*TIMER OFF*'):
        TimerOn = False
        group.send(WordStr.TimerOff)
    if msg.is_at:#被at就嘤嘤嘤
        group.send(WordStr.YYY[randint(0,len(WordStr.YYY)-1)])
    f = ''
    if ('.help' in msg.text) | ('。help' in msg.text):#显示帮助
        if len(msg.text) == 5:
            temp = WordStr.hlp+'ON' if rpt else WordStr.hlp+'OFF'
            group.send(temp)
        else:
            exec('group.send(WordStr.'+msg.text[6:]+'hlp)')
    if msg.member.puid not in pu:#第一次在群中出现的人的初始化
        pu.append(msg.member.puid)
        nm.append(msg.member.name)
        pl.append(pers(-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0))
        rp.append(randint(1,100))
    for i in range(0,len(pu)):#群成员指针
        if msg.member.puid == pu[i]:
            tn = nm[i]
            si = i
    if (dt != (strftime("%Y{0}%m{1}%d{2}", localtime()).format('年','月','日'))):#jrrp更新
        for i in range(0,len(pu)):
            rp[i] = randint(1,100)
            dt = strftime("%Y{0}%m{1}%d{2}", localtime()).format('年','月','日')
    if ('.rd' in msg.text) | ('。rd' in msg.text):#将rd转化为。r1d
        if (len(msg.text) == 3) | (msg.text[3:4] == ' '):
            f = '.r1d100'+msg.text[3:]
        else:
            f = '.r1d'+msg.text[3:]
    if (randint(1,15) == 1) & (len(msg.text) <= 30) & (rpt == True):#随机复读
        if randint(1,2) == 1:
            group.send(WordStr.Repeat.format(msg.text,tn))
        else:
            group.send(WordStr.DRM[randint(0,len(WordStr.DRM)-1)] + '#梦话')
    if rgnm == True:#人物卡的注册
        if msg.member.puid == pu[rgid]:
            rgnm = False
            try:
                num = findall('\
攻击(.+)：(\d+)\n\
体质(.+)：(\d+)\n\
敏捷(.+)：(\d+)\n\
外貌(.+)：(\d+)\n\
意志(.+)：(\d+)\n\
经验(.+)：(\d+)\n\
感染(.+)：(\d+)\n\
幸运(.+)：(\d+)\n\
智力(.+)：(\d+)\n\
教育(.+)：(\d+)\n\
体型(.+)：(\d+)\
',msg.text)
                for i in range(0,11):
                    exec('pl['+str(rgid)+'].'+num[0][i*2]+'=int('+num[0][i*2+1]+')')
                pl[rgid].DUR = ceil((pl[rgid].CON + pl[rgid].SIZ) / 4)
                pl[rgid].SKL = (pl[rgid].INT + pl[rgid].EXP + pl[rgid].EDU) * 2
                pl[rgid].ART = floor(sqrt(pl[rgid].ORG + pl[rgid].INT + pl[rgid].EDU + pl[rgid].EXP)) - 10
                group.send(WordStr.RegSuc.format(str(pl[rgid].DUR),str(pl[rgid].SKL),str(pl[rgid].ART)))
            except:
                group.send(WordStr.Err)
            rgid = -1
    elif ennm == True:#敌方单位的注册
        if msg.member.puid == pu[enid]:
            ennm = False
            try:
                num = findall('\
名称：(.+)\n\
攻击(.+)：(\d+)\n\
体质(.+)：(\d+)\n\
闪避(.+)：(\d+)\n\
法抗(.+)：(\d+)\n\
生命(.+)：(\d+)\
',msg.text)
                en.append(enemy('',-1,-1,-1,0,-1,'',[],[]))
                en[-1].NAM = num[0][0]
                for i in range(1,6):
                    exec('en[-1].'+num[0][i*2-1]+'=int('+num[0][i*2]+')')
                group.send(WordStr.RegEnSuc.format(en[-1].NAM))
            except:
                group.send(WordStr.Err)
            enid = -1
    elif ('.reg' in msg.text) | ('。reg' in msg.text):#各种。reg
        try:
            x = msg.text[5:]
            if x == '':
                raise Exception
            if x == 'all':
                rgnm = True
                rgid = si
                group.send(WordStr.InputReg)
            elif x == 'del':
                pl[si] = pers(-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)
                group.send(WordStr.DelReg)
            elif x == 'list':
                if pl[si].ORG == -1:
                    group.send(WordStr.NotRegistered.format(tn))
                else:
                    group.send(WordStr.ListCRD.format(tn)+'\n\
攻击AGG：'+str(pl[si].AGG)+'\n\
体质CON：'+str(pl[si].CON)+'\n\
敏捷DEX：'+str(pl[si].DEX)+'\n\
外貌APP：'+str(pl[si].APP)+'\n\
意志POW：'+str(pl[si].POW)+'\n\
经验EXP：'+str(pl[si].EXP)+'\n\
感染ORG：'+str(pl[si].ORG)+'\n\
幸运LUK：'+str(pl[si].LUK)+'\n\
智力INT：'+str(pl[si].INT)+'\n\
教育EDU：'+str(pl[si].EDU)+'\n\
体型SIZ：'+str(pl[si].SIZ)+'\n\
耐力DUR：'+str(pl[si].DUR)+'\n\
法抗RES：'+str(pl[si].RES)+'\n\
技能点数SKL：'+str(pl[si].SKL)+'\n\
最大源石出力等级ART：'+str(pl[si].ART)+'\n')
            elif msg.text[5:8] == 'enm':
                if msg.text[9:] == 'all':
                    ennm = True
                    enid = si
                    group.send(WordStr.InputEnReg)
                elif msg.text[9:13] == 'list':
                    if len(en) == 0:
                        group.send(WordStr.NoEnemy)
                    elif msg.text[14:] == '':
                        s = WordStr.ListEnemyAll+'\n'
                        for i in range(0,len(en)):
                            s += str(i+1)+'：'+en[i].NAM+'\n'
                        group.send(s)
                    else:
                        y = -1
                        for i in range(0,len(en)):
                            if msg.text[14:] == en[i].NAM:
                                 y = i
                        if y != -1:
                            group.send(WordStr.ListEnemy.format(en[y].NAM)+'\n\
攻击AGG：'+str(en[y].AGG)+'\n\
体质CON：'+str(en[y].CON)+'\n\
闪避DEX：'+str(en[y].DEX)+'\n\
法抗RES：'+str(en[y].RES)+'\n\
生命DUR：'+str(en[y].DUR)+'\n')
                        else:
                            group.send(WordStr.EnNotFound.format(msg.text[14:]))
                elif msg.text[9:12] == 'del':
                    if msg.text[13:] == '':
                        raise Exception
                    else:
                        group.send(WordStr.DelEn.format(en[int(msg.text[13:])-1].NAM))
                        en.pop(int(msg.text[13:])-1)
                else:
                    y = -1
                    for i in range(0,len(en)):
                        if msg.text[9:].split(' ')[0] == en[i].NAM:
                            y = i
                            y1 = msg.text[9:].split(' ')[1].upper()
                    if y != -1:
                        if len(y1) == 3:
                            y2 = msg.text[9:].split(' ')[2]
                            exec('en['+str(y)+'].'+y1+'=int('+y2+')',globals(),locals())
                            group.send(WordStr.EnUpd.format(en[y].NAM,y1,str(int(y2))))
                        else:
                            exec('en['+str(y)+'].'+y1[0:3]+'=floor(en['+str(y)+'].'+y1+')',globals(),locals())
                            group.send(WordStr.EnChange.format(en[y].NAM,y1[0:3],y1,str(eval('en['+str(y)+'].'+y1[0:3]))))
                    else:
                        group.send(WordStr.EnNotFound.format(msg.text[9:].split(' ')[0]))
            elif msg.text[5:8].upper() in CRD:
                y = msg.text[5:8].upper()
                if len(msg.text) == 8:
                    group.send(WordStr.CRDStatus.format(tn,y,str(eval('pl['+str(si)+'].'+y))))
                elif msg.text[9] == ' ':
                    exec('pl['+str(si)+'].'+y+'=int('+msg.text[9:]+')',globals(),locals())
                    group.send(WordStr.CRDUpd.format(tn,y,str(int(msg.text[9:]))))
                else:
                    exec('pl['+str(si)+'].'+y+'=floor(pl['+str(si)+'].'+msg.text[5:].upper()+')',globals(),locals())
                    group.send(WordStr.CRDUpd.format(tn,y,msg.text[5:].upper(),str(eval('pl['+str(si)+'].'+y))))
        except:
            group.send(WordStr.Err)
    elif ('.atk' in msg.text) | ('。atk' in msg.text):#各种。atk
        try:
            x,y,n,t = msg.text[5:].split(' ')
            i1 = -1
            i2 = -1
            co = False
            enmy = False
            for i in range(0,len(nm)):
                if x == nm[i]:
                    i1 = i
                if y == nm[i]:
                    i2 = i
                    co = True
            for i in range(0,len(en)):
                if x == en[i].NAM:
                    i1 = i
                    enmy = True
                if y == en[i].NAM:
                    i2 = i
            if (i1 > -1) & (i2 > -1):
                if t == 'TDMG':
                    if co:
                        pl[i2].DUR -= int(n)
                        group.send(WordStr.Attack.format(y,x,n,'真实',str(pl[i2].DUR)))
                    else:
                        en[i2].DUR -= int(n)
                        z = int(n)
                        group.send(WordStr.Attack.format(y,x,n,'真实',str(en[i2].DUR)))
                elif t == 'PHYS':
                    if co:
                        z = max(int(n) - pl[i2].CON // 5,int(n) // 2)
                        z = 0 if z < 0 else z
                        pl[i2].DUR -= z
                        group.send(WordStr.Attack.format(y,x,str(z),'物理',str(pl[i2].DUR)))
                    else:
                        z = max(int(n) - en[i2].CON // 5,int(n) // 2)
                        z = 0 if z < 0 else z
                        en[i2].DUR -= z
                        group.send(WordStr.Attack.format(y,x,str(z),'物理',str(en[i2].DUR)))
                elif t == 'ARTS':
                    if co:
                        z = floor(int(n)*(100-pl[i2].RES)/100)
                        z = 0 if z < 0 else z
                        group.send(WordStr.Attack.format(y,x,str(z),'法术',str(pl[i2].DUR)))
                    else:
                        z = floor(int(n)*(100-en[i2].RES)/100)
                        z = 0 if z < 0 else z
                        group.send(WordStr.Attack.format(y,x,str(z),'法术',str(en[i2].DUR)))
                else:
                    raise Exception
                if (not co) & (not enmy):
                    if x in en[i2].DMS:
                        for i in range(0,len(en[i2].DMS)):
                            if x == en[i2].DMS[i]:
                                en[i2].DMG[i] += z
                    else:
                        en[i2].DMS.append(x)
                        en[i2].DMG.append(z)
                if enmy:
                    en[i1].LTN = y
            else:
                group.send(WordStr.UnitNotFound)
            co = False
        except:
            group.send(WordStr.Err)
    elif ('.jrrp' in msg.text) | ('。jrrp' in msg.text):#显示今日人品
        group.send(WordStr.Jrrp.format(tn,dt,str(rp[si])))
    elif ('.nn' in msg.text) | ('。nn' in msg.text):#更改昵称
        if ' ' in msg.text:
            if len(msg.text[4:]) > 30:
                group.send('@'+tn+' '+WordStr.RCG[randint(0,len(WordStr.RCG)-1)])
            else:
                nm[si] = msg.text[4:]
                group.send(WordStr.NN.format(nm[si]))
        else:
            nm[si] = msg.member.name
            group.send(WordStr.NNForget.format(tn))
    elif (msg.text == '*RPT OFF*'):#开关复读
        rpt = False
        group.send(WordStr.RPT.format('关闭'))
    elif (msg.text == '*RPT ON*'):
        rpt = True
        group.send(WordStr.RPT.format('开启'))
    elif ('.复读' in msg.text) | ('。复读' in msg.text):#手动复读
        if ' ' in msg.text:
            if len(msg.text[4:]) > 50:
                group.send('@'+tn+' '+WordStr.RCG[randint(0,len(WordStr.RCG)-1)])
            else:
                group.send(WordStr.Repeat.format(msg.text[4:],tn))
        else:
            group.send(WordStr.EmptyRpt[randint(0,1)])
    elif ('.tgt' in msg.text) | ('。tgt' in msg.text):#target
        try:
            num = msg.text[5:].split(' ')
            x = num[0]
            m = num[1]
            y = -1
            for i in range(0,len(en)):
                if en[i].NAM == x:
                    y = i
            if y != -1:
                j = False
                for i in range(0,len(pl)):
                    if pl[i].ORG != -1:
                        j = True
                if j:
                    if m == 'RAND':
                        k = randint(0,len(nm)-1)
                        while pl[k].ORG == -1:
                            k = randint(0,len(nm)-1)
                        k = nm[k]
                        group.send(WordStr.TGT.format('随机',k))
                    elif m == 'DUR':
                        mx = 999
                        lst = []
                        for i in range(0,len(pl)):
                            if (pl[i].DUR > -1) & (pl[i].DUR <= mx):
                                if pl[i].DUR == mx:
                                    lst.append(i)
                                else:
                                    lst = [i]
                                    mx = pl[i].DUR
                        k = nm[lst[randint(0,len(lst)-1)]]
                        group.send(WordStr.TGT.format('血量最低',k))
                    elif m == 'DMG':
                        if en[y].DMG != []:
                            mx = max(en[y].DMG)
                            lst = []
                            for i in range(0,len(en[y].DMG)):
                                if en[y].DMG[i] == mx:
                                    lst.append(en[y].DMS[i])
                            k = lst[randint(0,len(lst)-1)]
                            group.send(WordStr.TGT.format('对 '+x+' 造成伤害最高',k))
                        else:
                            group.send(WordStr.NODMG.format(x))
                    else:
                        raise Exception
                else:
                    group.send(WordStr.NOCRD)
            else:
                group.send(WordStr.UnitNotFound)
        except:
            group.send(WordStr.Err)
    elif ('.en' in msg.text) | ('。en' in msg.text):#成长
        x = msg.text[4:7]
        d = randint(1,100)
        try:
            if x.upper() not in CRD:
                raise Exception
            if pl[si].ORG == -1:
                raise NR
            d1 = eval('pl['+str(si)+'].'+x.upper())
            if d >= d1:
                group.send(WordStr.EN.format(tn,x.upper(),d1,d,WordStr.Suc))
            else:
                group.send(WordStr.EN.format(tn,x.upper(),d1,d,WordStr.Fail))
        except NR:
            group.send(WordStr.NotRegistered.format(tn))
        except:
            group.send(WordStr.Err)
    elif ('.rc' in msg.text) | ('。rc' in msg.text) | ('.ra' in msg.text) | ('。ra' in msg.text):#检定
        d = randint(1,100)
        k = msg.text[3:] if msg.text[3] != ' ' else msg.text[4:]
        if ' ' in k:
            x,y = k.split(' ')
        else:
            x = k
            y = ''
        try:
            x = int(x)
            if d > 95:
                t = WordStr.LFail
            elif d > x:
                t = WordStr.Fail
            elif d > x // 2:
                t = WordStr.Suc
            elif d > x // 5:
                t = WordStr.HardSuc
            else:
                t = WordStr.ExtremeSuc
            group.send(WordStr.RC.format(tn,y,d,t))    
        except:
            group.send(WordStr.Err)
    elif ('.art' in msg.text) | ('。art' in msg.text):#获取潜力信息
        x = 1
        s = WordStr.ART.format(tn)+'\n——————————\n'
        if ' ' in msg.text:
            num = findall(msg.text[0:4]+' (\d+)', msg.text)
            x = int(num[0][0])
        for j in range(0,x):
            zy = 0#卓越个数
            a = [[0] * 2  for i in range(6)]
            for i in range(6):
                a[i][0] = randint(1,5)
                if a[i][0] == 5:
                    zy += 1
            for i in range(5):
                if a[i][0] == 1:
                    a[i][1] = '缺陷 -1D10 = '+str(-randint(1,10))
                elif a[i][0] == 2:
                    a[i][1] = '普通 -1D6 = '+str(-randint(1,6))
                elif a[i][0] == 3:
                    a[i][1] = '标准 0'
                elif a[i][0] == 4:
                    a[i][1] = '优良 1D10 = '+str(randint(1,10))
                elif a[i][0] == 5:
                    a[i][1] = '卓越 2D10 = '+str(randint(1,10)+randint(1,10))
            if a[5][0] == 1:
                a[5][1] = '缺陷'
            elif a[5][0] == 2:
                a[5][1] = '普通'
            elif a[5][0] == 3:
                a[5][1] = '标准'
            elif a[5][0] == 4:
                a[5][1] = '优良'
            elif a[5][0] == 5:
                a[5][1] = '卓越'
            s += '物理强度：'+ a[0][1] +'\n'\
                 '生理耐受：'+ a[1][1] +'\n'\
                 '战场机动：'+ a[2][1] +'\n'\
                 '战术规划：'+ a[3][1] +'\n'\
                 '战斗技巧：'+ a[4][1] +'\n'\
                 '源石技术适应性：'+ a[5][1] +'\n'\
                 '“卓越”个数：'+str(zy)+'\n'\
                 '———————————\n'
        group.send(s) 
    elif ('.ark' in msg.text) | ('。ark' in msg.text):#人物卡生成
        x = 1
        s = WordStr.ARK.format(tn)
        if ' ' in msg.text:
            num = findall(msg.text[0:4]+' (\d+)', msg.text)
            x = int(num[0][0])
        for i in range(0,x):
            ax = [((randint(1,6)+randint(1,6)+randint(1,6))*5) for i in range(0,8)]\
                 + [((randint(1,6)+randint(1,6)+6)*5) for i in range (0,3)] + [0]
            for ii in range(0,11):
                ax[11] += ax[ii]
            s += \
            '攻击AGG：'+ str(ax[0]) + '\n'\
            '体质CON：'+ str(ax[1]) + '\n'\
            '敏捷DEX：'+ str(ax[2]) + '\n'\
            '外貌APP：'+ str(ax[3]) + '\n'\
            '意志POW：'+ str(ax[4]) + '\n'\
            '经验EXP：'+ str(ax[5]) + '\n'\
            '感染ORG：'+ str(ax[6]) + '\n'\
            '幸运LUK：'+ str(ax[7]) + '\n'\
            '智力INT：'+ str(ax[8]) + '\n'\
            '教育EDU：'+ str(ax[9]) + '\n'\
            '体型SIZ：'+ str(ax[10]) + '\n'\
            '总和SUM：'+ str(ax[11]) + '\n'
            if ax[11] >= 700:
                s += '★总和大于700！★\n'
            s += '———————————\n'
        group.send(s)
    elif ('.rb' in msg.text) | ('。rb' in msg.text) | ('.rp' in msg.text) | ('。rp' in msg.text):#奖励骰/惩罚骰
        x1 = randint(1,100)
        x2 = []
        y  = ''
        t  = 1
        if len(msg.text) > 3:
            if ' ' in msg.text:
                t = msg.text[3:].split(' ')[0]
                t = 1 if t == '' else int(t)
                if t > 100:
                    group.send('@'+tn+' '+WordStr.RCG[randint(0,len(WordStr.RCG)-1)])
                    t = -1
                y = msg.text[3:].split(' ')[1]
            else:
                t = int(msg.text[3:])
        for i in range(0,t):
            x2.append(randint(0,10))
        x3 = deepcopy(x2)
        x3.append(x1 // 10)
        if msg.text[2] == 'b':
            if x1 % 10 == 0:
                while min(x3) == 0:
                    for i in range(0,len(x3)):
                        x3[i] = 10 if x3[i] == 0 else x3[i]
            x = min(x3) * 10 + x1 % 10
            k = '奖励'
        elif msg.text[2] == 'p':
            if x1 % 10 != 0:
                while max(x3) == 10:
                    for i in range(0,len(x3)):
                        x3[i] = -1 if x3[i] == 10 else x3[i]
            elif min(x3) == 0:
                x3.append(10)
            x = max(x3) * 10 + x1 % 10
            k = '惩罚'
        if y == '':
            group.send(WordStr.RBP.format(tn,msg.text[2].upper(),x1,k,x2,x))
        else:
            group.send(WordStr.RBPn.format(y,tn,msg.text[2].upper(),x1,k,x2,x))
    elif ('.rhd' in msg.text) | ('。rhd' in msg.text):#暗骰
        group.send(WordStr.RHDGroup)
        fr = bot.friends().search('',puid=msg.member.puid)[0]
        if len(msg.text) == 4:
            fr.send(WordStr.RHD.format(randint(1,100)))
        else:
            fr.send(WordStr.RHDn.format(msg.text[6:],randint(1,100)))
        fr.send(WordStr.RHDLine)
    elif (msg.text[0:2] == '.r') | (msg.text[0:2] == "。r"):#普通骰子
        s = ''
        t = ''
        if f == '':
            f = msg.text
        if ' ' in f:
            xx = f.split(' ')[0][2:]
            z = f[len(xx)+3:]
            x,y = xx.split('d')
            if len(y) > 1:
                y,t = findall('(\d+)(.+)',y)[0]
                if len(t) <= 1:
                    y = y+t
                    t = ''
        else:
            x = f.split('d')[0][2:]
            y = f.split('d')[1]
            z = ''
            if len(y) > 1:
                y,t = findall('(\d+)(.+)',y)[0]
                if len(t) <= 1:
                    y = y+t
                    t = ''
        dc = 0
        if (int(x) > 100) | (int(y) > 100000):
            group.send('@'+tn+' '+WordStr.RCG[randint(0,len(WordStr.RCG)-1)])
        else:
            for i in range(1,int(x)+1):
                k = randint(1,int(y))
                s += str(k)
                if i != int(x):
                    s += '+'
                elif int(x) > 1:
                    if t != '':
                        s += ')' + t
                    s += '='
                else:
                    s = ''
                    if t != '':
                        s += str(k) + ')' + t + '='
                dc += k
                if (x == '1') & (y == '100'):
                    rp[si] = rp[si] - 1 if k <= 10 else rp[si]
                    rp[si] = rp[si] + 1 if k >= 90 else rp[si]
                    if (k<=10) | (k>=90):
                        group.send(WordStr.RPChange.format(tn,rp[si]))
            if (t != '') :
                y += t
                s = '(' + s
            if (z == ''):
                group.send(WordStr.ROLL.format(tn,x,y,s,eval('floor('+str(dc)+t+')')))
            else:
                group.send(WordStr.ROLLn.format(z,tn,x,y,s,eval('floor('+str(dc)+t+')')))
        f = ''
    sleep(2)
embed()
