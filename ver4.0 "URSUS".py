from wxpy import *
from random import *
from math import *
from time import *
from re import *
from json import *

bot = Bot(cache_path=True)
bot.enable_puid('wxpy_puid.pkl')
group = bot.groups().search('CallOfTheresa')[0]
CRD = ['AGG','CON','DEX','APP','POW','EXP','ORG','LUK','INT','EDU','SIZ','DUR','SKL','ART']#人物卡
RCG = ['cnm','sb','nmsl','傻逼','rnm','gck','爬','给爷爬']#random curse generator
YYY = ['干嘛戳我Q_Q','不要戳了啦！TAT','再戳就生气了！','干嘛QwQ','嘤','QwQ','TAT','呜呜呜他欺负我','坏人走开']#嘤嘤嘤
DRM = ['昂？','唔……','啥啊','唔嗯','啊？','#¥…#¥!@#','搜到有','……城市……压过来了……']#梦话
hlp = \
'——CRISPY酱使用指南——\n\
目前本机.和。通用，已经开发的功能有：\n\
.rd [text] = [因为text]投掷1D100的一颗骰子\n\
.rXdY [text] = [因为text]投掷XDY的一颗骰子\n\
.ark [x] = [x次重复]获取人物卡各项数值\n\
.art [x] = [x次重复]获取人物卡各项潜力信息\n\
.nn [name] = 将自己在骰子中显示的昵称改为name，若[name]为空则还原默认群昵称\n\
.复读 [msg] = 让骰子复读你的话//可以用来做语录\n\
.jrrp = 今日人品（1d100到10以下-1，90以上+1，不包含加减）\n\
.reg 详细见 .help reg\n\
.atk 详细见 .help atk\n\
.tgt 详细见 .help tgt\n\
*RPT ON(OFF)* = 开启或关闭随机复读功能\n\
目前随机复读状态为：\
'#帮助文本
reghlp = \
'——REG功能使用指南——\n\
.reg [enm] all = 根据。ark填出来的卡读入[写入敌方单位数据]\n\
.reg [enm] <XXX> <数据> = 人物卡[敌方单位]数据填写（如AGG 65）\n\
.reg [enm] <XXX+改变量> = 人物卡[敌方单位]数据改变（如AGG+1）\n\
.reg [enm] list = 显示你的人物卡[显示敌方单位列表]\n\
.reg enm <NAM> all = 显示名叫NAM敌方单位的详细信息\n\
'
atkhlp = \
'——ATK功能使用指南——\n\
.atk <攻击者> <受击者> <伤害量> <攻击方式>\n\
攻击方式分为：\n\
PHYS = 物理攻击\n\
ARTS = 法术攻击\n\
TDMG = 真伤攻击\n\
'
tgthlp = \
'——TGT功能使用指南——\n\
注意！只有被.atk击中的单位才能被正确计算.tgt！\n\
.tgt <攻击者> <target方式>\n\
target方式分为：\n\
RAND = 完全随机\n\
DUR = 在生命值最低的单位中随机\n\
DMG = 对其造成伤害最高的单位中随机\n\
'
rpt = True
pu = []
nm = []
pl = []
en = []
rp = []
dt = strftime("%Y年%m月%d日", localtime())
rgnm = False
rgid = -1
ennm = False
enid = -1
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

@bot.register(group,TEXT)       
def returner(msg):
    global RCG,YYY,pl,en,rpt,DRM,hlp,rgnm,rgid,CRD,rp,dt,ennm,enid
    if msg.is_at:
        group.send(YYY[randint(0,len(YYY)-1)])
    f = ''
    if ('.help' in msg.text) | ('。help' in msg.text):
        if len(msg.text) == 5:
            temp = hlp+'ON' if rpt else hlp+'OFF'
            group.send(temp)
        else:
            exec('group.send('+msg.text[6:]+'hlp)')
    if msg.member.puid not in pu:
        pu.append(msg.member.puid)
        nm.append(msg.member.name)
        pl.append(pers(-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0))
        rp.append(randint(1,100))
    for i in range(0,len(pu)):
        if msg.member.puid == pu[i]:
            tn = nm[i]
            si = i
    if (dt != (strftime("%Y年%m月%d日", localtime()))):
        for i in range(0,len(pu)):
            rp[i] = randint(1,100)
            dt = strftime("%Y年%m月%d日", localtime())
    if ('.rd' in msg.text) | ('。rd' in msg.text):
        if (len(msg.text) == 3) | (msg.text[3:4] == ' '):
            f = '.r1d100'+msg.text[3:]
        else:
            f = '.r1d'+msg.text[3:]
    if (randint(1,15) == 1) & (len(msg.text) <= 30) & (rpt == True):
        if randint(1,2) == 1:
            group.send(msg.text + '\n——' + tn)
        else:
            group.send(DRM[randint(0,len(DRM)-1)] + '#梦话')
    if rgnm == True:
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
                group.send('人物卡注册成功了的说，您其他数据是：\n\
耐力DUR：'+str(pl[rgid].DUR)+'\n\
技能点数SKL：'+str(pl[rgid].SKL)+'\n\
最大源石出力等级ART：'+str(pl[rgid].ART)+'\n')
            except:
                group.send('输入格式好像不太对的说')
            rgid = -1
    elif ennm == True:
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
                en[enid].NAM = num[0][0]
                for i in range(1,6):
                    exec('en['+str(enid)+'].'+num[0][i*2-1]+'=int('+num[0][i*2]+')')
                group.send('敌方单位 '+en[enid].NAM+' 注册成功了的说')
            except:
                group.send('输入格式好像不太对的说')
            enid = -1
    elif ('.reg' in msg.text) | ('。reg' in msg.text):
        try:
            x = msg.text[5:]
            if x == '':
                raise Exception
            if x == 'all':
                rgnm = True
                rgid = si
                group.send('告诉我你的人物卡数据吧(o^^o)')
            elif x == 'del':
                pl[si] = pers(-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)
                group.send('人物卡数据被清空了！')
            elif x == 'list':
                if pl[si].ORG == -1:
                    group.send(tn+'，你好像并没有注册人物卡呀(･_･;')
                else:
                    group.send('以下是 '+tn+' 的人物卡数据！\n\
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
                    group.send('告诉我敌方单位的数据吧o(∩_∩)o')
                elif msg.text[9:13] == 'list':
                    if len(en) == 0:
                        group.send('目前好像没有敌方单位呀(･_･;')
                    elif msg.text[14:] == '':
                        s = '以下是敌方单位名单哦：\n'
                        for i in range(0,len(en)):
                            s += str(i+1)+'：'+en[i].NAM+'\n'
                        group.send(s)
                    else:
                        y = -1
                        for i in range(0,len(en)):
                            if msg.text[14:] == en[i].NAM:
                                y = i
                        if y != -1:
                            group.send('以下是 '+en[y].NAM+' 的数据：\n\
攻击AGG：'+str(en[y].AGG)+'\n\
体质CON：'+str(en[y].CON)+'\n\
闪避DEX：'+str(en[y].DEX)+'\n\
法抗RES：'+str(en[y].RES)+'\n\
生命DUR：'+str(en[y].DUR)+'\n')
                        else:
                            group.send('并没有找到名叫 '+msg.text[14:]+' 的敌方单位(>﹏<)')
                elif msg.text[9:12] == 'del':
                    if msg.text[13:] == '':
                        raise Exception
                    else:
                        group.send('敌方单位 '+en[int(msg.text[13:])-1].NAM+' 被删除了！')
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
                            group.send('敌方单位 '+en[y].NAM+' 的'+y1+'数值已经更新为'+str(int(y2))+'啦_(:з」∠)_')
                        else:
                            exec('en['+str(y)+'].'+y1[0:3]+'=floor(en['+str(y)+'].'+y1+')',globals(),locals())
                            group.send('敌方单位 '+en[y].NAM+' 的'+y1[0:3]+'数值要改变？唔好的：\n'+y1+' → '+str(eval('en['+str(y)+'].'+y1[0:3])))
                    else:
                        group.send('并没有找到名叫 '+msg.text[9:].split(' ')[0]+' 的敌方单位(>﹏<)')
            elif msg.text[5:8].upper() in CRD:
                y = msg.text[5:8].upper()
                if len(msg.text) == 8:
                    group.send(tn+'，你的'+y+'目前的数值为：'+str(eval('pl['+str(si)+'].'+y)))
                elif msg.text[9] == ' ':
                    exec('pl['+str(si)+'].'+y+'=int('+msg.text[9:]+')',globals(),locals())
                    group.send(tn+'的'+y+'数值已经更新为'+str(int(msg.text[9:]))+'啦_(:з」∠)_')
                else:
                    exec('pl['+str(si)+'].'+y+'=floor(pl['+str(si)+'].'+msg.text[5:].upper()+')',globals(),locals())
                    group.send(tn+'的'+y+'数值要改变？唔好的：\n'+msg.text[5:].upper()+' → '+str(eval('pl['+str(si)+'].'+y)))
        except:
            group.send('输入格式好像不太对的说')
    elif ('.atk' in msg.text) | ('。atk' in msg.text):
        try:
            num = msg.text[5:].split(' ')
            x = num[0]
            y = num[1]
            n = num[2]
            t = num[3]
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
                        group.send(y+' 受到了来自 '+x+' 的'+n+'点真实伤害！还剩下'+str(pl[i2].DUR)+'点血量！')
                    else:
                        en[i2].DUR -= int(n)
                        z = int(n)
                        group.send(y+' 受到了来自 '+x+' 的'+n+'点真实伤害！还剩下'+str(en[i2].DUR)+'点血量！')
                elif t == 'PHYS':
                    if co:
                        z = int(n) * 2 - floor(pl[i2].CON / 5)
                        z = 0 if z < 0 else z
                        pl[i2].DUR -= z
                        group.send(y+' 受到了来自 '+x+' 的'+str(z)+'点物理伤害！还剩下'+str(pl[i2].DUR)+'点血量！')
                    else:
                        z = int(n) * 2 - floor(en[i2].CON / 5)
                        z = 0 if z < 0 else z
                        en[i2].DUR -= z
                        group.send(y+' 受到了来自 '+x+' 的'+str(z)+'点物理伤害！还剩下'+str(en[i2].DUR)+'点血量！')
                elif t == 'ARTS':
                    if co:
                        z = floor(int(n)*(100-pl[i2].RES)/100)
                        z = 0 if z < 0 else z
                        group.send(y+' 受到了来自 '+x+' 的'+str(z)+'点法术伤害！还剩下'+str(pl[i2].DUR)+'点血量！')
                    else:
                        z = floor(int(n)*(100-en[i2].RES)/100)
                        z = 0 if z < 0 else z
                        group.send(y+' 受到了来自 '+x+' 的'+str(z)+'点法术伤害！还剩下'+str(en[i2].DUR)+'点血量！')
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
                group.send('并没有找到你所说的单位啊(･_･;')
            co = False
        except:
            group.send('输入格式好像不太对的说')
    elif ('.jrrp' in msg.text) | ('。jrrp' in msg.text):
        group.send(tn+'，你在'+dt+'的人品为：'+str(rp[si])+'！\n试试。rd提升人品吧！')
    elif ('.nn' in msg.text) | ('。nn' in msg.text):
        if ' ' in msg.text:
            if len(msg.text[4:]) > 30:
                group.send('@'+tn+' '+RCG[randint(0,len(RCG)-1)])
            else:
                nm[si] = msg.text[4:]
                group.send('啊，那之后就把你叫做' + nm[si] + '了昂')
        else:
            nm[si] = msg.member.name
            group.send('让我忘掉' + tn + '这个称号？好啊')
    elif (msg.text == '*RPT OFF*'):
        rpt = False
        group.send('已关闭随机对话！')
    elif (msg.text == '*RPT ON*'):
        rpt = True
        group.send('已开启随机对话！')
    elif ('.复读' in msg.text) | ('。复读' in msg.text):
        if ' ' in msg.text:
            if len(msg.text[4:]) > 50:
                group.send('@'+tn+' '+RCG[randint(0,len(RCG)-1)])
            else:
                group.send(msg.text[4:] + '\n——' + tn)
        else:
            group.send('耍我啊？')
    elif ('.tgt' in msg.text) | ('。tgt' in msg.text):
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
                        group.send('target出随机目标为：'+k+'！')
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
                        group.send('target出血量最低目标为：'+k+'！')
                    elif m == 'DMG':
                        if en[y].DMG != []:
                            mx = max(en[y].DMG)
                            lst = []
                            for i in range(0,len(en[y].DMG)):
                                if en[y].DMG[i] == mx:
                                    lst.append(en[y].DMS[i])
                            k = lst[randint(0,len(lst)-1)]
                            group.send('target出对 '+x+' 造成伤害最高的目标为：'+k+'！')
                        else:
                            group.send(x+' 并没有受到任何伤害(･_･;')
                    else:
                        raise Exception
                else:
                    group.send('并没有任何人注册了人物卡(･_･;')
            else:
                group.send('并没有找到你所说的单位啊(･_･;')
        except:
            group.send('输入格式好像不太对的说')
    elif ('.art' in msg.text) | ('。art' in msg.text):
        x = 1
        s = tn+'，想获取自己的潜力信息吗？啊(哈欠)，等我roll一下..\n——————————\n'
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
    elif ('.ark' in msg.text) | ('。ark' in msg.text):
        x = 1
        s = '欢迎来到泰拉世界哦，'+tn+'酱\n'
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
    elif (msg.text[0:2] == '.r') | (msg.text[0:2] == "。r"):
        s = ''
        t = ''
        if f == '':
            f = msg.text
        if ' ' in f:
            xx = f.split(' ')[0][2:]
            z = f[len(xx)+3:]
            x = xx.split('d')[0]
            y = xx.split('d')[1]
            if len(y) > 1:
                num = findall('(\d+)(.+)',y)
                y = num[0][0]
                t = num[0][1]
                if len(t) <= 1:
                    y = y+t
                    t = ''
        else:
            x = f.split('d')[0][2:]
            y = f.split('d')[1]
            z = ''
            if len(y) > 1:
                num = findall('(\d+)(.+)',y)
                y = num[0][0]
                t = num[0][1]
                if len(t) <= 1:
                    y = y+t
                    t = ''
        dc = 0
        if (int(x) > 100) | (int(y) > 100000):
            group.send('@'+tn+' '+RCG[randint(0,len(RCG)-1)])
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
                        group.send(tn+'的今日人品变动！现在是：'+str(rp[si])+'！')
            if (t != '') :
                y += t
                s = '(' + s
            if (z == ''):
                group.send(tn+' 骰出了 '+x+'d'+y+'='+s+str(eval('floor('+str(dc)+t+')')))
            else:
                group.send('由于 '+z+' 检定，'+tn+'骰出了 '+x+'d'+y+'='+s+str(eval('floor('+str(dc)+t+')')))
        f = ''
    sleep(2)
embed()
