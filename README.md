# 王者荣耀爬虫

## 使用组件库
requests


## 执行方法
王者营地访问战绩抓包: gameOpenId, gameRoleId, openId, token, userId
`python main.py`执行结果保存为`result.json`
`python analyze.py`读取`result.json`, 输出`五排队友数据.csv`, 包含游戏场数、胜率、mvp率、平均评分、平均KDA。


## 涉及的URL
访问战绩列表：https://kohcamp.qq.com/game/morebattlelist
访问对局详情：https://kohcamp.qq.com/game/battledetail