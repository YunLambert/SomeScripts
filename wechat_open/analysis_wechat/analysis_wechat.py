import itchat
import codecs
import json
from pyecharts import Map,Pie,Bar
from collections import Counter

def login_wx():
    sexList = {'0': 'unknown', '1': 'male', '2': "female"}  # 将itchat接口获取到的0,1,2转换为相应的性别
    itchat.auto_login()
    try:
        friends = itchat.get_friends(update=True)
        friendsList = []

        for friend in friends:
            item = {}
            item['NickName'] = friend['NickName']
            item['Sex'] = sexList[str(friend['Sex'])]
            item['Province'] = friend['Province']
            item['Signature'] = friend['Signature']
            item["UserName"] = friend['UserName']
            friendsList.append(item)

        return friendsList
    except Exception as e:
        print(e)


def save_friends_to_json(friendsList):
    output = "./result/friends.json"
    with codecs.open(output, "w", encoding="utf-8") as jsonFile:
        jsonFile.write(json.dumps(friendsList, ensure_ascii=False))

def get_friends_from_json():
    with codecs.open("./result/friends.json", encoding = "utf-8") as f:
        friendsList = json.load(f)
        return friendsList

def get_pie(friend_list):
    sexDict = {'男':0, '女':0, '未知':0}
    sexMap = {'male':'男', 'female':'女', 'unknown': '未知'}
    for item in friend_list:
        sexDict[sexMap[item["Sex"]]] += 1

    sexList = []
    numList = []

    for key, value in sexDict.items():
        sexList.append(key)
        numList.append(value)

    if len(sexList) and len(numList) and len(numList)==len(sexList):
        outputFile = './result/sex_proportion.html'
        pie = Pie('性别比例图', width=1200, height=600, title_pos='center')
        pie.add(
            '',
            sexList, numList,
            is_label_show=True,  # 是否显示标签
            label_text_color=None,  # 标签颜色
            legend_orient='vertical',  # 图例是否垂直
            legend_pos='left'
        )
        pie.render(outputFile)
    else:
        print("Empty list!")


def get_province(friendList):
    provinceCounter = Counter()
    for item in friendList:
        if item['Province'] != "":
            provinceCounter[item["Province"]] += 1

    nameList = []
    numList = []
    for counter in provinceCounter.most_common(11):
        nameList.append(counter[0])
        numList.append(counter[1])

    return nameList, numList


def get_bar(nameList, numList):
    outputFile = './result/省份柱状图.html'
    bar = Bar(title='省份分布柱状图', width=1200, height=600, title_pos='center')
    bar.add(
        '',  # 注解label属性
        nameList,  # 横
        numList  # 纵
    )
    bar.show_config()
    bar.render(outputFile)


def get_map(nameList, numList):
    pass
    outputFile = './result/区域分布图.html'
    map = Map(title='微信好友区域分布图', width=1200, height=600, title_pos='center')
    map.add(
        '', nameList, numList,
        maptype='china',  # 地图范围
        is_visualmap=True,  # 是否开启鼠标缩放漫游等
        is_label_show=True  # 是否显示地图标记
    )
    map.render(outputFile)


if __name__ == "__main__":
    # friendsList = login_wx()
    # save_friends_to_json(friendsList)
    analysis_friend_list = get_friends_from_json()
    nameList, numList = get_province(analysis_friend_list)
    get_bar(nameList, numList)
    # get_map(nameList, numList)   pyecharts关掉了map系统，需另外导入地图或在options中进行设置
    print("已在result文件夹中生成html文件")
