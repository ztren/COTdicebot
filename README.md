# COTdicebot
Call of Theresa DICEBOT
CRISPY ver4.1
## ——一般功能——
.rd [text] = [因为text]投掷1D100的一颗骰子\
.rXdY [text] = [因为text]投掷XDY的一颗骰子\
.rb/rp [n] = 投掷n个奖励骰/惩罚骰\
.rhd = 暗骰1D100\
.ark [x] = [x次重复]获取人物卡各项数值\
.art [x] = [x次重复]获取人物卡各项潜力信息\
.nn [name] = 将自己在骰子中显示的昵称改为name，若[name]为空则还原默认群昵称\
.复读 [msg] = 让骰子复读你的话//可以用来做语录\
.jrrp = 今日人品（1d100到10以下-1，90以上+1，不包含加减）\
.reg 详细见 .help reg\
.atk 详细见 .help atk\
.tgt 详细见 .help tgt\
*RPT ON(OFF)* = 开启或关闭随机复读功能
## ——REG功能使用指南——
.reg [enm] all = 根据。ark填出来的卡读入[写入敌方单位数据]\
.reg [enm] <XXX> <数据> = 人物卡[敌方单位]数据填写（如AGG 65）\
.reg [enm] <XXX+改变量> = 人物卡[敌方单位]数据改变（如AGG+1）\
.reg [enm] list = 显示你的人物卡[显示敌方单位列表]\
.reg enm <NAM> all = 显示名叫NAM敌方单位的详细信息
## ——ATK功能使用指南——
.atk <攻击者> <受击者> <伤害量> <攻击方式>\
攻击方式分为：\
PHYS = 物理攻击\
ARTS = 法术攻击\
TDMG = 真伤攻击
## ——TGT功能使用指南——
**注意！只有被.atk击中的单位才能被正确计算.tgt**\
.tgt <攻击者> <target方式>\
target方式分为：\
RAND = 完全随机\
DUR = 在生命值最低的单位中随机\
DMG = 对其造成伤害最高的单位中随机\

注：[]内为选填，<>内为必填，.和。通用\
