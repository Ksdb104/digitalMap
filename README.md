# digitalMap/可视化电子地图册

**所用地图仅为标识,不做任何划界参考,也不代表本人的任何立场,如果有的话我更想使用更抽象的地图,本项目的重点不在于此** 

将一些b站知识区up主讲解国家类的视频对应到地图上,能更直观的根据需求查询 ~~以及催更~~
![image](https://github.com/Ksdb104/digitalMap/assets/36178808/447c6306-b4d4-4a4d-aabd-6c07808888f1)
点选左侧地图能自动检索右侧视频,也可以自己搜索
主要使用了python pyecharts和sanic
```
apt install python3
pip3 install sanic
pip3 install pyecharts
```
前端依赖都是cdn引入,不需要安装
 ~~因为我一点后端也不会,python都是现学的,写的大概很烂~~

 目前还没有做移动端适配,使用网页端以获得更佳体验

## 关于数据
/data/upinfo.json 管理右侧up主列表
/data/videolist.json 管理视频信息
看哪些up很主观,我看的up也一般都是混更,不一定是国家类视频,所以目前数据装填都是手动的😭

对于up主所有的信息都需要手动填,包括uid,名字和头像,之后可以考虑加个自动拉取头像更新的功能
![image](https://github.com/Ksdb104/digitalMap/assets/36178808/7de589af-9ae8-4126-ad49-226f04f3d20c)
对于视频仅需要填入url和国别剩余信息能自动拉取
![image](https://github.com/Ksdb104/digitalMap/assets/36178808/d187d73f-b3c2-45ed-a914-e0bd81886fc5)
不过因此数据数据拓展能力很不错,可以接入任何up和视频
自己视情况修改app的端口和接口访问地址就可以运行
![image](https://github.com/Ksdb104/digitalMap/assets/36178808/0cb5e4b6-d1af-4610-aa5a-47b2b4fecec9)
![image](https://github.com/Ksdb104/digitalMap/assets/36178808/6e3ef7eb-f13f-4a91-b1c9-f5e00ebfbbde)
```
python app.py
```
或者直接访问

https://map.huan-yue.org
