from random import randrange

from sanic import Sanic
from sanic.response import json, html

import json as jsons
import requests
import time
import asyncio

from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from bilibili_api import user,Credential

# 初始化 Sanic
# init_opts=opts.InitOpts(theme=ThemeType.LIGHT)
app = Sanic(__name__)

data1=[]
data2=[]
countryData=[]
credential = Credential(sessdata="", bili_jct="", buvid3="", dedeuserid="")

def checkvideoinfo():
    with open('./data/videolist.json', 'r',encoding='utf-8') as fcc_file:
        listinfo = jsons.load(fcc_file)
    for item in listinfo['videolist']:
        if ('bvid' in item):
            print('已存在数据')
        else:
            temp = getvideoinfo(item)
            # print('获取数据!')
            if(temp):
                item = temp 
            time.sleep(3)
    with open('./data/videolist.json',"w",encoding="utf-8") as f:
        jsons.dump(listinfo,f,indent=4, ensure_ascii=False)
        # print("加载入文件完成...")
        for item in listinfo['videolist']:
            if (item['country'] in data1):
                p = data1.index(item['country'])
                data2[p] +=1
            else:
                data1.append(item['country'])
                data2.append(1)
    return

def getvideoinfo(item):
    res = requests.get(url = 'https://tenapi.cn/v2/bilivideo?url='+item['url'])
    request = res.json()
    if (request['code']==200):
        item["url"] = item['url']
        item["bvid"] = request['data']['id']
        item["country"] = item['country']
        item["cover"] = request['data']['cover']
        item["title"] = request['data']['title']
        item["upname"] = request['data']['name']
        item["time"] = request['data']['time']
        return item
    else:
        print('接口出错')
        return
    
def bar_base() -> Map:
    countryData = list(zip(data1,data2))
    c = (
        Map()
            .add("稿件数", countryData, "world",name_map=name_map)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="可视化电子地图册"),
                visualmap_opts=opts.VisualMapOpts(max_=10),
            )
        )
    return c

async def checkupinfo():
    with open('./data/upinfo.json', 'r',encoding='utf-8') as fcc_file:
        listinfo = jsons.load(fcc_file)
    for item in listinfo['upinfo']:
        userinfo = user.User(uid=item['id'],credential=credential)
        request = await userinfo.get_user_info()
        print(request)
        if(request):
            item["name"] = request['name']
            item["avatar"] = request['face']
        time.sleep(3)
    with open('./data/upinfo.json',"w",encoding="utf-8") as f:
        jsons.dump(listinfo,f,indent=4, ensure_ascii=False)
    return

asyncio.get_event_loop().run_until_complete(checkupinfo())
checkvideoinfo()
# checkupinfo()

@app.route("/barChart", methods=["GET"])
async def draw_bar_chart(request):
    c = bar_base()
    return json(c.dump_options_with_quotes())

@app.route("/getData", methods=["GET"])
async def return_data(request):
    new_dict = json(open("./data/videolist.json",encoding='utf-8').read())
    return new_dict

@app.route("/getUpInfo", methods=["GET"])
async def return_upinfo(request):
    return json(open("./data/upinfo.json",encoding='utf-8').read())


@app.route("/", methods=["GET"])
async def index(request):
    return html(open("./templates/index.html",encoding='utf-8').read())

ssl = {
    "cert": "/usr/local/etc/xray/cert/sanicfullchain.cer",
    "key": "/usr/local/etc/xray/cert/sanicprivate.key",
}

if __name__ == '__main__':
    asyncio.run(app.run(host='0.0.0.0', port=443,fast=True,ssl=ssl))

name_map = {
    'Singapore': '新加坡',
    'Dominican Rep.': '多米尼加共和国',
    'Dominica':'多米尼克',
    'Liechtenstein':'列支敦士登',
    'Isle of Man':'马恩岛',
    'Andorra':'安道尔',
    'Palestine': '巴勒斯坦',
    'Bahamas': '巴哈马',
    'Timor-Leste': '东帝汶',
    'Afghanistan': '阿富汗',
    'Guinea-Bissau': '几内亚比绍',
    "Côte d'Ivoire": '科特迪瓦',
    'Siachen Glacier': '锡亚琴冰川',
    "Br. Indian Ocean Ter.": '英属印度洋领土',
    'Angola': '安哥拉',
    'Albania': '阿尔巴尼亚',
    'United Arab Emirates': '阿联酋',
    'Argentina': '阿根廷',
    'Armenia': '亚美尼亚',
    'French Southern and Antarctic Lands': '法属南半球和南极领地',
    'Australia': '澳大利亚',
    'Austria': '奥地利',
    'Azerbaijan': '阿塞拜疆',
    'Burundi': '布隆迪',
    'Belgium': '比利时',
    'Benin': '贝宁',
    'Burkina Faso': '布基纳法索',
    'Bangladesh': '孟加拉国',
    'Bulgaria': '保加利亚',
    'The Bahamas': '巴哈马',
    'Bosnia and Herz.': '波斯尼亚和黑塞哥维那',
    'Belarus': '白俄罗斯',
    'Belize': '伯利兹',
    'Bermuda': '百慕大',
    'Bolivia': '玻利维亚',
    'Brazil': '巴西',
    'Brunei': '文莱',
    'Bhutan': '不丹',
    'Botswana': '博茨瓦纳',
    'Central African Rep.': '中非',
    'Canada': '加拿大',
    'Switzerland': '瑞士',
    'Chile': '智利',
    'China': '中国',
    'Ivory Coast': '象牙海岸',
    'Cameroon': '喀麦隆',
    'Dem. Rep. Congo': '刚果民主共和国',
    'Congo': '刚果',
    'Colombia': '哥伦比亚',
    'Costa Rica': '哥斯达黎加',
    'Cuba': '古巴',
    'N. Cyprus': '北塞浦路斯',
    'Cyprus': '塞浦路斯',
    'Czech Rep.': '捷克',
    'Germany': '德国',
    'Djibouti': '吉布提',
    'Denmark': '丹麦',
    'Algeria': '阿尔及利亚',
    'Ecuador': '厄瓜多尔',
    'Egypt': '埃及',
    'Eritrea': '厄立特里亚',
    'Spain': '西班牙',
    'Estonia': '爱沙尼亚',
    'Ethiopia': '埃塞俄比亚',
    'Finland': '芬兰',
    'Fiji': '斐济',
    'France': '法国',
    'Gabon': '加蓬',
    'United Kingdom': '英国',
    'Georgia': '格鲁吉亚',
    'Ghana': '加纳',
    'Guinea': '几内亚',
    'Gambia': '冈比亚',
    'Guinea Bissau': '几内亚比绍',
    'Eq. Guinea': '赤道几内亚',
    'Greece': '希腊',
    'Greenland': '格陵兰',
    'Guatemala': '危地马拉',
    'French Guiana': '法属圭亚那',
    'Guyana': '圭亚那',
    'Honduras': '洪都拉斯',
    'Croatia': '克罗地亚',
    'Haiti': '海地',
    'Hungary': '匈牙利',
    'Indonesia': '印度尼西亚',
    'India': '印度',
    'Ireland': '爱尔兰',
    'Iran': '伊朗',
    'Iraq': '伊拉克',
    'Iceland': '冰岛',
    'Israel': '以色列',
    'Italy': '意大利',
    'Jamaica': '牙买加',
    'Jordan': '约旦',
    'Japan': '日本',
    'Kazakhstan': '哈萨克斯坦',
    'Kenya': '肯尼亚',
    'Kyrgyzstan': '吉尔吉斯斯坦',
    'Cambodia': '柬埔寨',
    'Korea': '韩国',
    'Kosovo': '科索沃',
    'Kuwait': '科威特',
    'Lao PDR': '老挝',
    'Lebanon': '黎巴嫩',
    'Liberia': '利比里亚',
    'Libya': '利比亚',
    'Sri Lanka': '斯里兰卡',
    'Lesotho': '莱索托',
    'Lithuania': '立陶宛',
    'Luxembourg': '卢森堡',
    'Latvia': '拉脱维亚',
    'Morocco': '摩洛哥',
    'Moldova': '摩尔多瓦',
    'Madagascar': '马达加斯加',
    'Mexico': '墨西哥',
    'Macedonia': '马其顿',
    'Mali': '马里',
    'Myanmar': '缅甸',
    'Montenegro': '黑山',
    'Mongolia': '蒙古',
    'Mozambique': '莫桑比克',
    'Mauritania': '毛里塔尼亚',
    'Malawi': '马拉维',
    'Malaysia': '马来西亚',
    'Namibia': '纳米比亚',
    'New Caledonia': '新喀里多尼亚',
    'Niger': '尼日尔',
    'Nigeria': '尼日利亚',
    'Nicaragua': '尼加拉瓜',
    'Netherlands': '荷兰',
    'Norway': '挪威',
    'Nepal': '尼泊尔',
    'New Zealand': '新西兰',
    'Oman': '阿曼',
    'Pakistan': '巴基斯坦',
    'Panama': '巴拿马',
    'Peru': '秘鲁',
    'Philippines': '菲律宾',
    'Papua New Guinea': '巴布亚新几内亚',
    'Poland': '波兰',
    'Puerto Rico': '波多黎各',
    'Dem. Rep. Korea': '朝鲜',
    'Portugal': '葡萄牙',
    'Paraguay': '巴拉圭',
    'Qatar': '卡塔尔',
    'Romania': '罗马尼亚',
    'Russia': '俄罗斯',
    'Rwanda': '卢旺达',
    'W. Sahara': '西撒哈拉',
    'Saudi Arabia': '沙特阿拉伯',
    'Sudan': '苏丹',
    'S. Sudan': '南苏丹',
    'Senegal': '塞内加尔',
    'Solomon Is.': '所罗门群岛',
    'Sierra Leone': '塞拉利昂',
    'El Salvador': '萨尔瓦多',
    'Somaliland': '索马里兰',
    'Somalia': '索马里',
    'Serbia': '塞尔维亚',
    'Suriname': '苏里南',
    'Slovakia': '斯洛伐克',
    'Slovenia': '斯洛文尼亚',
    'Sweden': '瑞典',
    'Swaziland': '斯威士兰',
    'Syria': '叙利亚',
    'Chad': '乍得',
    'Togo': '多哥',
    'Thailand': '泰国',
    'Tajikistan': '塔吉克斯坦',
    'Turkmenistan': '土库曼斯坦',
    'East Timor': '东帝汶',
    'Trinidad and Tobago': '特里尼达和多巴哥',
    'Tunisia': '突尼斯',
    'Turkey': '土耳其',
    'Tanzania': '坦桑尼亚',
    'Uganda': '乌干达',
    'Ukraine': '乌克兰',
    'Uruguay': '乌拉圭',
    'United States': '美国',
    'Uzbekistan': '乌兹别克斯坦',
    'Venezuela': '委内瑞拉',
    'Vietnam': '越南',
    'Vanuatu': '瓦努阿图',
    'West Bank': '西岸',
    'Yemen': '也门',
    'South Africa': '南非',
    'Zambia': '赞比亚',
    'Zimbabwe': '津巴布韦',
    'Comoros': '科摩罗',
    'Fr. S. Antarctic Lands': '法属南半球和南极陆地',
    'Cayman Is.': '开曼群岛',
    'Faeroe Is.': '法罗群岛',
    'IsIe of Man': '马恩岛',
    'Malta': '马耳他共和国',
    'Jersey': '泽西',
    'Cape Verde': '佛得角共和国',
    'Turks and Caicos Is.': '特克斯和凯科斯群岛',
    'St. Vin. and Gren.': '圣文森特和格林纳丁斯',
    'Antigua and Barb.': '安提瓜和巴布达',
    'U.S. Virgin Is.': '美属维尔京群岛',
    'Falkland Is.': '马尔维纳斯群岛',
    'Grenada':'格林纳达',
    'Saint Lucia':'圣卢西亚',
     "S. Geo. and S. Sandw. Is.":'南乔治亚和南桑威奇群岛',
     'Palau':'帛琉',
     'Guam':'关岛',
     'Micronesia':'密克罗尼西亚联邦',
     'N. Mariana Is.':'北马里亚纳群岛',
     'Seychelles':'塞舌尔群岛',
     'Samoa':'萨摩亚',
     'American Samoa':'美属萨摩亚',
     'Tonga':'汤加',
     'Niue':'纽埃',
     'Fr. Polynesia':'法属波利尼西亚群岛',
     'Kiribati':'基里巴斯',
     'Heard I. and McDonald Is.':'赫克岛和麦克唐纳群岛',
     'Mauritius':'毛里求斯',
     'Saint Helena':'圣赫勒拿岛',
     'São Tomé and Principe':'圣多美和普林西比',
     'Bahrain':'巴林',
     'Montserrat':'蒙塞拉特岛',
     'Barbados':'巴巴多斯',
     'Curaçao':'库拉索'
}
