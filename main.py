import requests
import json
# import time


# def getHeroDict():
#     url = 'https://pvp.qq.com/web201605/js/herolist.json'
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
#     }
#     r = requests.get(url, headers=headers)
#     r.encoding = r.apparent_encoding
#     msgs = r.json()
#     dict = {}
#     for item in msgs:
#         dict[item['ename']] = item['cname']
#     return dict


# heroDict = getHeroDict()


headers = {
    'gameOpenId': '',
    'gameRoleId': '',
    'openId': '',
    'token': '',
    'userId': '',
}

userId = headers['userId']
roleId = headers['gameRoleId']


def getGameDetails(gameSeq, relaySvr, gameSvr, battleType):
    url2 = 'https://kohcamp.qq.com/game/battledetail'
    request_data2 = {
        "relaySvr" : relaySvr,
        "gameSeq" : gameSeq,
        "gameSvr" : gameSvr,
        "targetRoleId" : roleId,
        "battleType" : battleType
    }
    r2 = requests.post(url2, headers=headers, json=request_data2)
    data = r2.json()['data']

    def isMyTeam(team):
        for player in team:
            if player['basicInfo']['isMe'] == True:
                return True
        return False

    result = { 'params': request_data2 }
    try:
        red = data['redRoles']
        blue = data['blueRoles']
        team = red if isMyTeam(red) else blue

        result['players'] = [
            { 
                'name': p['basicInfo']['roleName'],
                'hero': p['battleRecords']['usedHero']['heroName'],
                'score': p['battleStats']['gradeGame'],
                'kda': p['battleStats']['kda'],
                'isMvp': p['battleStats']['mvp']
            } for p in team]
    except KeyError:
        pass
    return result


final_results = []

nums = 0
time_id = 0
url = 'https://kohcamp.qq.com/game/morebattlelist'

while True:
    nums += 1
    print(nums)

    request_data = {
        "lastTime": f"{time_id}",
        "friendUserId": userId,
        "friendRoleId": roleId
    }
    r = requests.post(url, headers=headers, json=request_data)

    data = r.json()['data']
    if not data:
        print('ERROR')
        exit(0)
    time_id = data['lastTime']
    
    for game in data['list']:
        # desc = game['desc'] if game['desc'] else ''
        try:
            if '五排' in game['mapName']:
                details = getGameDetails(
                    gameSeq=game['gameSeq'], 
                    relaySvr=game['relaySvrId'], 
                    gameSvr=game['gameSvrId'],
                    battleType=game['battleType']
                )
                details['result'] = '失败' if int(game['gameresult']) == 2 else '胜利'
                details['time'] = game['gametime']
                # details['rank'] = game['roleJobName'] + f"{game['stars']}星"
                final_results.append(details)
                print(f"{details['time']}, {details['result']}")
                # time.sleep(0.5)
        except KeyError:
            print("ERROR")

    # time.sleep(1)
    if not data['hasMore']:
        break


with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(final_results, f, ensure_ascii=False, indent=4)


