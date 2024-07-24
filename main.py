import requests
import json
from datetime import datetime

from analyze import analyze

# ------------------------------------------------------
# TO MODIFY
# ------------------------------------------------------
SEARCH_FOR_ME = True # (Required)
USER_ID = ''  # Your user ID (Required)
ROLE_ID = ''  # Your role ID (Required)
FRIEND_USER_ID = '' # User ID of the player you want to query (Required if SEARCH_FOR_ME=False)
FRIEND_ROLE_ID = '' # Role ID of the player you want to query (Required if SEARCH_FOR_ME=False)
BATTLE_TYPE_DICT = {
    '排位赛 五排': True,
    '排位赛 三排': True,
    '排位赛 双排': True,
    '排位赛': False,
    '巅峰赛': False
}

GAME_OPEN_ID = ''  # (Required)
OPEN_ID = ''  # (Required)
TOKEN = ''  # (Required)
# ------------------------------------------------------

headers = {
    'gameOpenId': GAME_OPEN_ID,
    'openId': OPEN_ID,
    'token': TOKEN,
    'gameRoleId': ROLE_ID,
    'userId': USER_ID
}

target_user_id = USER_ID if SEARCH_FOR_ME else FRIEND_USER_ID
target_role_id = ROLE_ID if SEARCH_FOR_ME else FRIEND_ROLE_ID
target_battle_types = [key for (key, value) in BATTLE_TYPE_DICT.items() if value == True]

# ------------------------------------------------------

def get_battle_list(time_id):
    url = 'https://kohcamp.qq.com/game/morebattlelist'
    request_data = {
        "lastTime": f"{time_id}",
        "friendUserId": target_user_id,
        "friendRoleId": target_role_id
    }
    r = requests.post(url, headers=headers, json=request_data)
    data = r.json()['data']
    return (data['hasMore'], data['lastTime'], data['list']) if data else (False, None, [])



def get_battle_details(game_seq, relay_svr, game_svr, battle_type):
    url2 = 'https://kohcamp.qq.com/game/battledetail'
    request_data2 = {
        "relaySvr" : relay_svr,
        "gameSeq" : game_seq,
        "gameSvr" : game_svr,
        "targetRoleId" : target_role_id,
        "battleType" : battle_type
    }
    r2 = requests.post(url2, headers=headers, json=request_data2)
    data = r2.json()['data']

    def isTargetTeam(team):
        for player in team:
            if player['basicInfo']['roleId'] == target_role_id:
                return True
        return False

    result = { 'params': request_data2 }
    try:
        red = data['redRoles']
        blue = data['blueRoles']
        team = red if isTargetTeam(red) else blue

        result['players'] = [
            { 
                'name': p['basicInfo']['roleName'],
                'hero': p['battleRecords']['usedHero']['heroName'],
                'score': p['battleStats']['gradeGame'],
                'kda': p['battleStats']['kda'],
                'isMvp': p['battleStats']['mvp'],
                'money': p['battleStats']['money'], # 总经济
                'monsterCoin': p['battleStats']['monsterCoin'], # 野怪经济
                'totalHeroHurtCnt': p['battleStats']['totalHeroHurtCnt'], # 对英雄输出
                'hurtTransRate': p['battleStats']['hurtTransRate'], # 输出转化率
                'joinGamePercent': p['battleStats']['joinGamePercent'], # 参团率
                'ctrlTime': p['battleStats']['ctrlTime'], # 控制时长
                'healCnt': p['battleStats']['healCnt'], # 治疗量
                'totalBeheroHurtCnt': p['battleStats']['totalBeheroHurtCnt'], # 对英雄承伤
                'position': p['battleRecords']['position']
            } for p in team]
    except KeyError:
        print("ERROR: 无比赛详情（服务器端储存过期）")
        return (False, {})
    return (True, result)

# ------------------------------------------------------


if __name__ == '__main__':
    final_results = []

    nums = 0
    time_id = 0

    while True:
        nums += 1
        print(nums)

        (has_more, time_id, battle_list) = get_battle_list(time_id)
        
        for game in battle_list:
            try:
                if game['mapName'] in target_battle_types:
                    ret, details = get_battle_details(
                        game_seq=game['gameSeq'], 
                        relay_svr=game['relaySvrId'], 
                        game_svr=game['gameSvrId'],
                        battle_type=game['battleType']
                    )
                    if not ret:
                        has_more = False
                        break
                    details['result'] = '失败' if int(game['gameresult']) == 2 else '胜利'
                    details['time'] = game['gametime']
                    final_results.append(details)
                    print(f"{details['time']}, {details['result']}, {game['desc']}")
            except KeyError:
                print("ERROR: 获取对局列表失败")

        if not has_more:
            break
    
    # Save result
    cur_time = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f'data_{target_role_id}_{cur_time}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    analyze(final_results)
