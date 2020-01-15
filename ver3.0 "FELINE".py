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
DRM = ['昂？','唔……','啥啊','唔嗯','啊？','#¥…#¥!@#','搜到有']#梦话
hlp = \
'——CRISPY酱使用指南——\n\
目前本机.和。通用，已经开发的功能有：\n\
.rd [text] = [因为text]投掷1D100的一颗骰子\n\
.rXdY [text] = [因为text]投掷XDY的一颗骰子\n\
.ark [x] = [x次重复]获取人物卡各项数值\n\
.art [x] = [x次重复]获取人物卡各项潜力信息\n\
.nn [name] = 将自己在骰子中显示的昵称改为name，若[name]为空则还原默认群昵称\n\
.复读 [msg] = 让骰子复读你的话//可以用来做语录\n\
.reg all = 根据。ark填出来的卡读入（记录不保存！）\n\
.reg <XXX+改变量> 人物卡数据改变（如AGG+1）\n\
.jrrp 今日人品（1d100到10以下-1，90以上+1，不包含加减）\n\
*RPT ON(OFF)* = 开启或关闭随机复读功能\n\
目前随机复读状态为：\
'#帮助文本
rpt = True
pu = []
nm = []
pl = []
rp = []
dt = strftime("%Y年%m月%d日", localtime())
rgnm = False
rgid = -1
class pers:
    def __init__(self,AGG,CON,DEX,APP,POW,EXP,ORG,LUK,INT,EDU,SIZ,DUR,SKL,ART):
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

@bot.register(group,TEXT)       
def returner(msg):
    global RCG,YYY,pl,rpt,DRM,hlp,rgnm,rgid,CRD,rp,dt
    if msg.is_at:
        group.send(YYY[randint(0,len(YYY)-1)])
    f = ''
    if (msg.text == '.help') | (msg.text == '。help'):
        temp = hlp+'ON' if rpt else hlp+'OFF'
        group.send(temp)
    if pu.count(msg.member.puid) == 0:
        pu.append(msg.member.puid)
        nm.append(msg.member.name)
        pl.append(pers(-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1))
        rp.append(randint(1,100))
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
                k = '人物卡注册成功了的说，您其他数据是：\n\
耐力DUR：'+str(pl[rgid].DUR)+'\n\
技能点数SKL：'+str(pl[rgid].SKL)+'\n\
最大源石出力等级ART：'+str(pl[rgid].ART)+'\n'
                group.send(k)
            except:
                group.send('输入格式好像不太对的说')
            rgid = -1
    if ('.reg' in msg.text) | ('。reg' in msg.text):
        for i in range(0,len(pu)):
            if msg.member.puid == pu[i]:
                tn = nm[i]
                si = i
        try:
            x = ''
            x = msg.text[5:]
            group.send
            if x == '':
                raise Exception
            if x == 'all':
                rgnm = True
                rgid = si
                group.send('告诉我你的人物卡数据吧(o^^o)')
            elif x == 'del':
                pl[si] = pers(-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1)
                group.send('人物卡数据被清空了！')
            elif msg.text[5:8].upper() in CRD:
                if len(msg.text) == 8:
                    group.send(tn+'，你的'+msg.text[5:8].upper()+'目前的数值为：'+str(eval('pl['+str(si)+'].'+msg.text[5:8].upper())))
                else:
                    exec('pl['+str(si)+'].'+msg.text[5:8].upper()+'=floor(pl['+str(si)+'].'+msg.text[5:].upper()+')',globals(),locals())
                    group.send(tn+'的'+msg.text[5:8].upper()+'数值要改变？唔好的：\n'+msg.text[5:].upper()+' → '+str(eval('pl['+str(si)+'].'+msg.text[5:8].upper())))
        except:
            group.send('输入格式好像不太对的说')
    if ('.rd' in msg.text) | ('。rd' in msg.text):
        f = '.r1d100'+msg.text[3:]
    if ('.jrrp' in msg.text) | ('。jrrp' in msg.text):
        for i in range(0,len(pu)):
            if msg.member.puid == pu[i]:
                tn = nm[i]
                si = i
        group.send(tn+'，你在'+dt+'的人品为：'+str(rp[si])+'！\n试试。rd提升人品吧！')
        if (dt != (strftime("%Y年%m月%d日", localtime()))):
            for i in range(0,len(pu)):
                rp[i] = randint(1,100)
                dt = strftime("%Y年%m月%d日", localtime())
    if ('.nn' in msg.text) | ('。nn' in msg.text):
        for i in range(0,len(pu)):
            if msg.member.puid == pu[i]:
                tn = nm[i]
                si = i
        if ' ' in msg.text:
            if len(msg.text[4:]) > 30:
                group.send('@'+tn+' '+RCG[randint(0,len(RCG)-1)])
            else:
                nm[si] = msg.text[4:]
                group.send('啊，那之后就把你叫做' + nm[si] + '了昂')
        else:
            nm[si] = msg.member.name
            group.send('让我忘掉' + tn + '这个称号？好啊')
    if (msg.text == '*RPT OFF*'):
        rpt = False
        group.send('已关闭随机对话！')
    if (msg.text == '*RPT ON*'):
        rpt = True
        group.send('已开启随机对话！')
    if (randint(1,15) == 1) & (len(msg.text) <= 30) & (rpt == True):
        for i in range(0,len(pu)):
            if msg.member.puid == pu[i]:
                tn = nm[i]
        if randint(1,2) == 1:
            group.send(msg.text + '\n——' + tn)
        else:
            group.send(DRM[randint(0,len(DRM)-1)] + '#梦话')
    if ('.复读' in msg.text) | ('。复读' in msg.text):
        for i in range(0,len(pu)):
            if msg.member.puid == pu[i]:
                tn = nm[i]
        if ' ' in msg.text:
            if len(msg.text[4:]) > 50:
                group.send('@'+tn+' '+RCG[randint(0,len(RCG)-1)])
            else:
                group.send(msg.text[4:] + '\n——' + tn)
        else:
            group.send('耍我啊？')
    if ('.art' in msg.text) | ('。art' in msg.text):
        x = 1
        for i in range(0,len(pu)):
            if msg.member.puid == pu[i]:
                tn = nm[i]
        s = tn+'，想获取自己的潜力信息吗？啊(哈欠)，等我roll一下..\n——————————\n'
        if ' ' in msg.text:
            num = findall(msg.text[0]+' (\d+)', msg.text)
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
    if ('.ark' in msg.text) | ('。ark' in msg.text):
        x = 1
        for i in range(0,len(pu)):
            if msg.member.puid == pu[i]:
                tn = nm[i]
        s = '欢迎来到泰拉世界哦，'+tn+'酱\n'
        if ' ' in msg.text:
            num = findall(msg.text[0]+' (\d+)', msg.text)
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
    elif (msg.text[0] == '.') | (msg.text[0:1] == "。"):
        for i in range(0,len(pu)):
            if msg.member.puid == pu[i]:
                tn = nm[i]
                si = i
        s = ''
        if f == '':
            f = msg.text
        if ' ' in f:
            xx = f.split(' ')[0][2:]
            z = f[len(xx)+3:]
            x = xx.split('d')[0]
            y = xx.split('d')[1]
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
                if (f[1:7] == 'r1d100'):
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
