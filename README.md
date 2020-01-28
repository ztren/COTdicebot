# COTdicebot
Call of Theresa DICEBOT

# ——CRISPY使用指南——\n\
### CRISPY ver4.1\n\
目前本机.和。通用，已经开发的功能有：\n\
.rd [text] = [因为text]投掷1D100的一颗骰子\n\
.rXdY [text] = [因为text]投掷XDY的一颗骰子\n\
.rb/rp [n] = 投掷n个奖励骰/惩罚骰\n\
.rhd = 暗骰1D100\n\
.ark [x] = [x次重复]获取人物卡各项数值\n\
.art [x] = [x次重复]获取人物卡各项潜力信息\n\
.nn [name] = 将自己在骰子中显示的昵称改为name，若[name]为空则还原默认群昵称\n\
.复读 [msg] = 让骰子复读你的话//可以用来做语录\n\
.jrrp = 今日人品（1d100到10以下-1，90以上+1，不包含加减）\n\
.reg 详细见 .help reg\n\
.atk 详细见 .help atk\n\
.tgt 详细见 .help tgt\n\
注：[]内为选填，<>内为必填\n\
*RPT ON(OFF)* = 开启或关闭随机复读功能\n\
## ——REG功能使用指南——\n\
.reg [enm] all = 根据。ark填出来的卡读入[写入敌方单位数据]\n\
.reg [enm] <XXX> <数据> = 人物卡[敌方单位]数据填写（如AGG 65）\n\
.reg [enm] <XXX+改变量> = 人物卡[敌方单位]数据改变（如AGG+1）\n\
.reg [enm] list = 显示你的人物卡[显示敌方单位列表]\n\
.reg enm <NAM> all = 显示名叫NAM敌方单位的详细信息\n\
## ——ATK功能使用指南——\n\
.atk <攻击者> <受击者> <伤害量> <攻击方式>\n\
攻击方式分为：\n\
PHYS = 物理攻击\n\
ARTS = 法术攻击\n\
TDMG = 真伤攻击\n\
## ——TGT功能使用指南——\n\
注意！只有被.atk击中的单位才能被正确计算.tgt！\n\
.tgt <攻击者> <target方式>\n\
target方式分为：\n\
RAND = 完全随机\n\
DUR = 在生命值最低的单位中随机\n\
DMG = 对其造成伤害最高的单位中随机\n\
