# COTdicebot
CRISPY, the Call of Theresa DICEBOT, by ZTREN\
某一天，开发者终于明白把名字起的很好听没有一点卵用。
## 概述
COTdicebot是基于CallOfTheresa的跑团规则，由ZTREN独立编写的dicebot。
## 安装
### 1.安装python3
**注意：本程序可能并不兼容python2。（未经过测试）**\
官网链接如下。\
https://www.python.org/downloads/
### 2.安装wxpy
**WINDOWS用户需要安装pip。** \
参考如下教程安装：\
https://www.douban.com/note/696046743/ \
OSX、LINUX：
```
pip install wxpy
```
或者按照以下链接安装wxpy源代码。\
https://pypi.org/project/wxpy/
### 3.下载DICEBOT
https://github.com/ztren/COTdicebot/releases \
点击最新版本的zip下载并解压。
### 4.运行DICEBOT
用命令行或终端运行**DICE.py**，并根据提示操作。\
若扫描二维码之后未报错并出现">>>"字样（不含双引号），即说明登陆成功，可以使用。\
**注：wxpy并不会响应bot自身所在微信号发送的消息。**
## 功能介绍
### 1、一般功能
.rd [text] = [因为text]投掷1D100的一颗骰子\
.rXdY [text] = [因为text]投掷XDY的一颗骰子\
.rb/rp [n] = 投掷n个奖励骰/惩罚骰\
.ra/rc <x> [text] = [因为text]投掷以x为成功线的检定\
.en <XXX> 通过1D100检定人物卡中XXX数值的成成长（需要先注册人物卡！）\
.rhd [text] = [因为text]暗骰1D100\
.ark [x] = [x次重复]获取人物卡各项数值\
.art [x] = [x次重复]获取人物卡各项潜力信息\
.nn [name] = 将自己在骰子中显示的昵称改为name，若[name]为空则还原默认群昵称\
.复读 [msg] = 让骰子复读你的话//可以用来做语录\
.jrrp = 今日人品（1d100到10以下-1，90以上+1，不包含加减）\
.reg 详细见 .help reg\
.atk 详细见 .help atk\
.tgt 详细见 .help tgt\
\*MUTE(UNMUTE)\* = 将本bot禁言或解除禁言\
\*TIMER ON(OFF)\* = 开启或关闭自动唤醒，默认关闭\
\*EXIT\* = 关闭本bot\
**不使用\*EXIT\*关闭程序可能会导致程序在后台继续运行，造成不必要的麻烦**\
\*RPT ON(OFF)\* = 开启或关闭随机复读功能
### 2、REG功能
.reg [enm] all = 根据。ark填出来的卡读入[写入敌方单位数据]，第一行需为AGG\
.reg [enm] <XXX> <数据> = 人物卡[敌方单位]数据填写（如AGG 65）\
.reg [enm] <XXX+改变量> = 人物卡[敌方单位]数据改变（如AGG+1）\
.reg [enm] list = 显示你的人物卡[显示敌方单位列表]\
.reg enm <NAM> all = 显示名叫NAM敌方单位的详细信息
### 3、ATK功能
.atk <攻击者> <受击者> <伤害量> <攻击方式>\
攻击方式分为：\
PHYS = 物理攻击\
ARTS = 法术攻击\
TDMG = 真伤攻击
### 4、TGT功能
**注意！只有被.atk击中的单位才能被正确计算.tgt**\
.tgt <攻击者> <target方式>\
target方式分为：\
RAND = 完全随机\
DUR = 在生命值最低的单位中随机\
DMG = 对其造成伤害最高的单位中随机\

注：[]内为选填，<>内为必填，.和。通用\

## 常见问题解答
### 1、使用微信登陆失败，如何解决？
请进入[网页版微信网址](https://web.weixin.qq.com)并尝试登录网页版微信，检查自己的微信号是否可以使用网页版微信。若提示无法登录网页版微信，则需要更换使用时间更长，微信安全等级更高的微信号登录。
### 2、打开程序时显示IndexError: list index out of range错误，如何解决
退出网页版微信，在需要绑定骰子的群聊中发送几条消息并将其置顶再运行程序。等程序运行之后再将其取消置顶。
### 3、我该如何修改dicebot所说的台词？
修改WordStr文件即可。
