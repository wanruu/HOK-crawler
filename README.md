# 王者荣耀战绩爬虫

爬取并筛选游戏对局，拉取队友的游戏数据，汇总。自行根据个人需求修改数据处理方式。

## 使用组件库
requests, json, datetime, csv, sys


## 执行方法
1. 王者营地访问战绩抓包 (域名为 `kohcamp.qq.com` ), 获取request body中的参数: `gameOpenId`, `gameRoleId`, `openId`, `token`, `userId`。

    > 如果要查别人的战绩，需要对方的王者营地公开战绩显示，并且抓取对方的`userId`和`roleId`参数。

2. 执行文件。
    ```
    python main.py
    ```
    执行结果保存为 `data_[role_id]_[date]_[time].json` 以及 `summary.csv`。
    
    `summary.csv` 包含游戏场数、胜率、mvp率、平均评分、平均KDA、辅助伤害转换比、其他分路伤害转换比。

3. (可选) 可以对爬取到的json数据文件单独运行分析。
    ```
    python analyze.py [json_file]
    ```



## 涉及的URL
对局列表：https://kohcamp.qq.com/game/morebattlelist

对局详情：https://kohcamp.qq.com/game/battledetail