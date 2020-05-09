from random import *
from time import *
import os
import WordStr
import DiceConstant

def init():
    if not os.path.exists('groups/'+WordStr.GroupName):
        os.makedirs('groups/'+WordStr.GroupName)
    try:
        misc = open('groups/'+WordStr.GroupName+'/_misc',mode = 'x')
        initmisc = ['<cmd>\n/\n.\n。\n!\n！\n</cmd>\n',
        '<dt>\n'+strftime("%Y{0}%m{1}%d{2}", localtime()).format('年','月','日')+'\n</dt>\n',
        '<rule>\ncocrule 0\nsend off\njrrp on\nrpt off\nmute off\n</rule>\n',
        '<pu>\n</pu>\n<ob>\n</ob>\n']
        misc.writelines(initmisc)
        del initmisc
        misc.close()
    except:
        pass
        
def readpl(pl):
    pers = open('groups/'+WordStr.GroupName+'/'+pl,mode = 'r')
    a = pers.readlines()
    pers.close()
    return a

def writepl(pl,a):
    pers = open('groups/'+WordStr.GroupName+'/'+pl,mode = 'w')
    pers.writelines(a)
    pers.close()
    return

def readmisc(obj):
    misc = open('groups/'+WordStr.GroupName+'/_misc',mode = 'r')
    a = misc.readlines()
    misc.close()
    flag = False
    if obj == '':
        return a
    b = []
    for i in range(0,len(a)):
        if a[i] == '</'+obj+'>\n':
            flag = False
            return b
        if flag == True:
            b.append(a[i])
        if a[i] == '<'+obj+'>\n':
            flag = True
    raise IndexError

def writemisc(obj):
    misc = open('groups/'+WordStr.GroupName+'/_misc',mode = 'w')
    misc.writelines(obj)
    misc.close()
    return

def changemisc(obj,list):
    a = readmisc('')
    b,e = a.index('<'+obj+'>\n'),a.index('</'+obj+'>\n')
    a[b+1:e] = list
    writemisc(a)
    return

def readrule(obj):
    a = readmisc('rule')
    for i in range(0,len(a)):
        if a[i].split(' ')[0] == obj:
            return a[i][:-1].split(' ')[1]
        if i == len(a)-1:
            raise IndexError
    return

def changerule(obj,str):
    a = readmisc('rule')
    for i in range(0,len(a)):
        if a[i].split(' ')[0] == obj:
            a[i] = obj + ' ' + str + '\n'
            changemisc('rule',a)
            break
        if i == len(a)-1:
            raise IndexError
    return

def st(pl,nam,val):#更改数值
    val = str(val)
    a = readpl(pl)
    for i in range(0,len(a)):
        if a[i] == nam+'\n':
            a[i+1] = val+'\n'
            break
        elif i == len(a)-1:
            a += [nam+'\n',val+'\n']
    a[-1] = a[-1] + '\n' if '\n' not in a[-1] else a[-1]
    writepl(pl,a)
    return

def getvl(pl,nam):#获取数值
    a = readpl(pl)
    for i in range(0,len(a)-1):
        if a[i] == nam+'\n':
            return a[i+1][:-1]
    raise NameError

def syn(nam):
    for i in range(0,len(DiceConstant.syn)):
        if nam.upper() in DiceConstant.syn[i]:
            return DiceConstant.syn[i][0]
    return nam

def dice(expr):
    x,y = expr.split('d')
    if (int(x) > 100) | (int(y) > 100000):
        raise IndexError
    sum = ''
    for i in range(0,int(x)):
        sum += str(randint(1,int(y))) + '+'
    sum = sum[:-1]
    if int(x) > 1:
        sum = '(' + sum + ')'
    return sum

def calc(expr):
    opr = ['+','-','*','/','(',')']
    expr += '*'
    s = ''
    a = []
    li = 0
    for i in range(0,len(expr)):
        if expr[i] in opr:
            a += [expr[li:i],expr[i]]
            li = i + 1
    a.pop()
    for i in range(0,len(a)):
        if 'd' in a[i]:
            a[i] = dice(a[i])
        s += a[i]
    return s
