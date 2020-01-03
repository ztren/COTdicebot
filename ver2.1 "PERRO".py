from wxpy import *
from random import *
from time import *
from re import *

bot = Bot(cache_path=True)
bot.enable_puid('wxpy_puid.pkl')
group = bot.groups().search('CallOfTheresa')[0]
RCG = ['cnm','sb','nmsl','傻逼','rnm','gck','爬','给爷爬']#random curse generator
YYY = ['干嘛戳我Q_Q','不要戳了啦！TAT','再戳就生气了！','干嘛QwQ','嘤','QwQ','TAT','呜呜呜他欺负我','坏人走开']#嘤嘤嘤
DRM = ['昂？','唔……','啥啊','唔嗯','啊？','#¥…#¥!@#','搜到有']#梦话
hlp = \
'——CRISPY酱使用指南——\n\
目前本机.和。通用，已经开发的功能有：\n\
.rd [text] = [因为text]投掷1D100的一颗骰子\n\
.rXdY [text] = [因为text]投掷XDY的一颗骰子，支持在后面加入一位+-*/运算符\n\
.ark [x] = [x次重复]获取人物卡各项数值\n\
.art [x] = [x次重复]获取人物卡各项潜力信息\n\
.nn [name] = 将自己在骰子中显示的昵称改为name，若[name]为空则还原默认群昵称\n\
.复读 [msg] = 让骰子复读你的话//可以用来做语录\n\
*RPT ON(OFF)* = 开启或关闭随机复读功能\n\
'#帮助文本
pu = []#PUID
nm = []#PUID对应姓名
rpt = True

@bot.register(group,TEXT)       
def returner(msg):
    global RCG,YYY,pu,nm,rpt,DRM,hlp
    if msg.is_at:
        group.send(YYY[randint(0,len(YYY)-1)])
    f = ''
    if (msg.text == '.help') | (msg.text == '。help'):
        group.send(hlp)
    if pu.count(msg.member.puid) == 0:
        pu.append(msg.member.puid)
        nm.append(msg.member.name)
    if ('.rd' in msg.text):
        f = '.r1d100'
        if len(msg.text) > 3:
            if msg.text[3] == ' ':
                f += msg.text[3:]
    elif ('。rd' in msg.text):
        f = '。r1d100'
        if len(msg.text) > 3:
            if msg.text[3] == ' ':
                f += msg.text[3:]
    if ('.nn' in msg.text) | ('。nn' in msg.text):
        for i in range(0,len(pu)):
            if msg.member.puid == pu[i]:
                tn = nm[i]
                si = i
        if msg.text[0] == '.':
            s1 = '.nn'
        else:
            s1 = '。nn'
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
    if (randint(1,10) == 1) & (len(msg.text) <= 30) & (rpt == True):
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
        if msg.text[0] == '.':
            s1 = '.复读'
        else:
            s1 = '。复读'
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
        if msg.text[0] == '.':
            s1 = '.art'
        else:
            s1 = '。art'
        if ' ' in msg.text:
            num = findall(s1+' (\d+)', msg.text)
            x = int(num[0][0])
        for j in range(0,x):
            a = [[0] * 2  for i in range(6)]
            for i in range(6):
                a[i][0] = randint(1,5)
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
            s += '物理强度：'+ a[0][1]+'\n'\
                 '生理耐受：'+ a[1][1]+'\n'\
                 '战场机动：'+ a[2][1]+'\n'\
                 '战术规划：'+ a[3][1]+'\n'\
                 '战斗技巧：'+ a[4][1]+'\n'\
                 '源石技术适应性：'+ a[5][1]+'\n'\
                 '———————————\n'
        group.send(s) 
    if ('.ark' in msg.text) | ('。ark' in msg.text):
        x = 1
        for i in range(0,len(pu)):
            if msg.member.puid == pu[i]:
                tn = nm[i]
        s = '欢迎来到泰拉世界哦，'+tn+'酱\n'
        if msg.text[0] == '.':
            s1 = '.ark'
        else:
            s1 = '。ark'
        if ' ' in msg.text:
            num = findall(s1+' (\d+)', msg.text)
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
            '总和SUM：'+ str(ax[11]) + '\n'\
            '———————————\n'
        group.send(s)            
    elif (msg.text[0] == '.') | (msg.text[0:1] == "。"):
        for i in range(0,len(pu)):
            if msg.member.puid == pu[i]:
                tn = nm[i]
        if msg.text[0] == '.':
            s1 = '.'
        else:
            s1 = '。'
        s = ''
        if f == '':
            f = msg.text
        if ' ' in f:
            if ('+' in f)|('-' in f)|('*' in f)|('/' in f):
                num = findall(s1+'r(\d+)d(\d+)(.)(\d+) (.+)', f)
                x = num[0][0]
                y = num[0][1]
                z = num[0][4]
                t0 = num[0][2]
                t1 = num[0][3]
            else:
                num = findall(s1+'r(\d+)d(\d+) (.+)', f)
                x = num[0][0]
                y = num[0][1]
                z = num[0][2]
                t0 = ''
        else:
            if ('+' in f)|('-' in f)|('*' in f)|('/' in f):
                num = findall(s1+'r(\d+)d(\d+)(.)(\d+)', f)
                x = num[0][0]
                y = num[0][1]
                z = ''
                t0 = num[0][2]
                t1 = num[0][3]
            else:
                num = findall(s1+'r(\d+)d(\d+)', f)
                x = num[0][0]
                y = num[0][1]
                z = ''
                t0 = ''
        dc = 0
        f = ''
        if (int(x) > 100) | (int(y) > 100000):
            group.send('@'+tn+' '+RCG[randint(0,len(RCG)-1)])
        else:
            for i in range(1,int(x)+1):
                k = randint(1,int(y))
                s += str(k)
                if i != int(x):
                    s += '+'
                elif int(x) > 1:
                    if t0 != '':
                        s += ')' + t0 + t1
                    s += '='
                else:
                    s = ''
                    if t0 != '':
                        s += str(k) + ')' + t0 + t1 + '='
                dc += k
            if t0 == '+':
                dc += int(t1)
            elif t0 == '-':
                dc -= int(t1)
            elif t0 == '*':
                dc *= int(t1)
            elif t0 == '/':
                dc //= int(t1)
            if (t0 != '') :
                y += t0 + t1
                s = '(' + s
            if (z == ''):
                group.send(tn+' 骰出了 '+x+'d'+y+'='+s+str(dc))
            else:
                group.send('由于 '+z+' 检定，'+tn+'骰出了 '+x+'d'+y+'='+s+str(dc))
    sleep(2)
embed()
