# 王者荣耀爬虫

筛选五排游戏局，拉取队友的游戏数据，汇总。

自行根据个人需求修改数据处理方式。

## 使用组件库
requests


## 执行方法
1. 王者营地访问战绩抓包: gameOpenId, gameRoleId, openId, token, userId。

    > 如果要查别人的战绩，需要对方的王者营地公开战绩显示，并且抓取对方的userId和roleId参数。

2. `python main.py` 执行结果保存为 `result.json`。

3. `python analyze.py` 读取 `result.json` 中的数据, 输出文件 `五排队友数据.csv`, 包含游戏场数、胜率、mvp率、平均评分、平均KDA。



## 涉及的URL
访问战绩列表：https://kohcamp.qq.com/game/morebattlelist

访问对局详情：https://kohcamp.qq.com/game/battledetail