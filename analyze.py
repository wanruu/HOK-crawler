import json
import csv

with open('result.json', encoding='utf-8') as f:
    data = json.load(f)


playerDict = {}
for game in data:
    try: 
        players = game['players']
        game_result = game['result']

        for player in players:
            name = player['name']
            score = float(player['score'])
            mvp = 1 if player['isMvp'] else 0
            win = 1 if game_result == '胜利' else 0
            kda = float(player['kda'])

            if name not in playerDict:
                playerDict[name] = {
                    'score': score, 
                    'kda': kda,
                    'mvp': mvp,
                    'game_num': 1,
                    'win_num': win
                }
            else:
                playerDict[name]['score'] += score
                playerDict[name]['kda'] += kda
                playerDict[name]['mvp'] += mvp
                playerDict[name]['game_num'] += 1
                playerDict[name]['win_num'] += win
    except KeyError:
        print("ERROR")
        print(game)


rows = []
for player in playerDict:
    player_data = playerDict[player]
    game_num = player_data['game_num']

    new_player_dict = {
        "玩家": player,
        "胜率": round(player_data['win_num'] / game_num, 2),
        "mvp率": round(player_data['mvp'] / game_num, 2),
        "平均评分": round(player_data['score'] / game_num, 1),
        "平均kda": round(player_data['kda'] / game_num, 1),
        "游戏场数": game_num
    }
    rows.append(new_player_dict)
rows = sorted(rows, key=lambda d: d['游戏场数'], reverse=True)

fields = ["玩家", "游戏场数", "胜率", "mvp率", "平均评分", "平均kda"]
with open("五排队友数据.csv", "w", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)


