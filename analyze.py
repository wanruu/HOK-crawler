import json
import csv
import sys


# position
# 对抗: 0
# 中路: 1
# 射手: 2
# 打野: 3
# 辅助: 4


def analyze(json_data):
    player_dict = {}
    for game in json_data:
        try: 
            players = game['players']
            game_result = game['result']

            for player in players:
                name = player['name']
                score = float(player['score'])
                mvp = 1 if player['isMvp'] else 0
                win = 1 if game_result == '胜利' else 0
                kda = float(player['kda'])
                hurt_trans_rate = float(player['hurtTransRate'])
                position = player['position']

                if name not in player_dict:
                    player_dict[name] = {
                        'score': score, 
                        'kda': kda,
                        'mvp': mvp,
                        'game_num': 1,
                        'sup_game_num': 1 if position == 4 else 0,
                        'win_num': win,
                        'sup_hurt_trans_rate': hurt_trans_rate if position == 4 else 0,
                        'other_hurt_trans_rate': hurt_trans_rate if position != 4 else 0
                    }
                else:
                    player_dict[name]['score'] += score
                    player_dict[name]['kda'] += kda
                    player_dict[name]['mvp'] += mvp
                    player_dict[name]['game_num'] += 1
                    player_dict[name]['sup_game_num'] += (1 if position == 4 else 0)
                    player_dict[name]['win_num'] += win
                    player_dict[name]['sup_hurt_trans_rate'] += (hurt_trans_rate if position == 4 else 0)
                    player_dict[name]['other_hurt_trans_rate'] += (hurt_trans_rate if position != 4 else 0)
        except KeyError:
            print("ERROR: 对局数据缺失")
            print(game)

    rows = []
    for player in player_dict:
        player_data = player_dict[player]
        game_num = player_data['game_num']
        sup_game_num = player_data['sup_game_num']
        other_game_num = game_num - sup_game_num

        player_summary_dict = {
            "玩家": player,
            "胜率": round(player_data['win_num'] / game_num, 2),
            "mvp率": round(player_data['mvp'] / game_num, 2),
            "平均评分": round(player_data['score'] / game_num, 1),
            "平均kda": round(player_data['kda'] / game_num, 1),
            "辅助伤害转换比": round(player_data['sup_hurt_trans_rate'] / sup_game_num, 1) if sup_game_num != 0 else '',
            "其他分路伤害转换比": round(player_data['other_hurt_trans_rate'] / other_game_num, 1) if other_game_num != 0 else '',
            "游戏场数": game_num
        }
        rows.append(player_summary_dict)
    rows = sorted(rows, key=lambda d: d['游戏场数'], reverse=True)

    fields = ["玩家", "游戏场数", "胜率", "mvp率", "平均评分", "平均kda", "辅助伤害转换比", "其他分路伤害转换比"]
    with open("summary.csv", "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def analyze_file(filename):
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)
        analyze(data)


if __name__ == '__main__':
    args = sys.argv

    if len(args) < 2:
        print("python analyze.py [json_file_name]")
        exit(0)

    analyze_file(args[1])