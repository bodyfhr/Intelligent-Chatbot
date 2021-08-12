## 目录
- [Rasa版本](#Rasa版本)
- [Demo-Video-Here](#演示视频)
- [GIF动图展示](#GIF动图展示)
- [说明](#说明)
- [配置环境](#配置环境)
- [数据导入neo4j](#数据导入neo4j)
- [训练Rasa模型](#训练Rasa模型)
- [Shell方式测试模型](#Shell方式测试模型)
- [服务形式运行bot](#服务形式运行bot)
- [参考](#参考)
- [更新记录](#更新记录)
- [如有问题可以issue](#如有问题可以issue)

## [English ReadMe](/en-README.md)


## Rasa版本
- 此处为***Rasa==2.0.x***(其它Rasa版本请切换branch)


## 演示视频
- [**演示视频**](https://www.bilibili.com/video/av61715811/)

- 视频中的demo演示网址用的上海服务器，低配，加载速度慢，各位轻虐~~ >.<


## GIF动图展示
- 2020/05/20 聊天窗的颜色略有不同

![image](img/demo-1.gif)

![image](img/demo-2.gif)


## 说明
- 本程序实现的是基于中文的医疗知识图谱的问答机器人MedicalKBQA，
是基于 [**Rasa-2.0.x**](https://rasa.com/) 版本及其支持的外部组件实现的，
并使用了图数据库 [**Neo4j**](https://neo4j.com/) 构建知识图谱。

- Rasa的```Pipeline```配置如下：
    ```yaml
    pipeline:
      - name: "MitieNLP"
        model: "data/total_word_feature_extractor_zh.dat"
      - name: "JiebaTokenizer"
        dictionary_path: "jieba_userdict"
      - name: "MitieEntityExtractor"
      - name: "EntitySynonymMapper"
      - name: "RegexFeaturizer"
      - name: "MitieFeaturizer"
      - name: "SklearnIntentClassifier"
    ```

- ***注意***： rasa-nlu和rasa-core已经合并成rasa


## 配置环境
1. Python ≈ 3.8.5

1. 下载zip包或者git clone 

1. 进入Doctor-Friende目录，conda记得activate环境

1. 安装Mitie其实很简单，参考[安装Rasa所需的MITIE组件](https://blog.csdn.net/pengyou200902/article/details/109183361)

1. 然后在命令行使用命令安装依赖
    ```shell
   pip install -r requirements.txt
    ```
   
1. *提示*：

    - 国内推荐使用镜像加速（此命令是临时使用镜像，并非全局都用），比如：
        ```shell
        pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
        ```
   
    - 如果你有代理，可以在pip install命令后加上 --proxy=地址:端口


## 数据导入neo4j
- 前提是已经有了可以连接的neo4j graph

- 解压```MedicalSpider/data/data.tar.gz```，直接解压到```MedicalSpider/data```下，不要新建文件夹，则```medical.json```是所有数据的汇总，
将会被导入到你的知识图谱中

- 修改```MedicalSpider.process_data```下的```create_graph.py```，把neo4j数据库的链接信息改成你自己的，然后运行该文件
（为了防止路径问题，建议使用Pycharm打开本项目后运行）

- *关于爬虫*：爬虫实现是使用了 [**scrapy**](https://scrapy.org) 库，若想运行，可以在Doctor-Friende目录下运行```SpiderMain.py```

- 整体规模：
    - 13,635 nodes (5 labels)
    - 114,163 relationships (6 types)

![image](img/graphdb.png)

- 数据结构

| 实体类型 | 含义 | 数量 | 举例 |  
| :--- | :---: | :---: | :--- |  
| Disease | 疾病 | 6,143 |  百日咳\n头痛|  
| Department | 科室 | 54 |  儿科\n小儿内科|  
| Drug | 药品 | 1,124 |  硫辛酸片\n曲克芦丁片|  
| Food | 食物 | 378 |  蟹肉\n鱿鱼(干)|  
| Symptom | 疾病症状 | 5,936 |  角弓反张\n视网膜Roth斑|  
| Total | 总计 | 13,635 | 约1.3万实体量级|  


## 训练Rasa模型
1. Rasa训练数据集的构造：使用到了 [**Chatito工具**](https://rodrigopivi.github.io/Chatito/) 

1. 下载用于mitie的模型文件放到```chat/data```文件夹下， [**百度网盘**](https://pan.baidu.com/s/1kNENvlHLYWZIddmtWJ7Pdg) ，密码：p4vx，
或者 [**Mega云盘**](https://mega.nz/#!EWgTHSxR!NbTXDAuVHwwdP2-Ia8qG7No-JUsSbH5mNQSRDsjztSA) 

    <!--1. 第一次用此```Pipeline```训练时，输入训练命令后会自动下载模型，默认下载保存的目录见 [**Cache Models**](https://huggingface.co/transformers/installation.html#caching-models)-->
 
    <!--1. **重要：** 若出现模型加载报错问题，按如下改名
        - 将 ```bert-base-chinese-config.json``` 更名为 ```config.json```
        - 将 ```bert-base-chinese-vocab.txt``` 更名为 ```vocab.txt```
        - 将 ```bert-base-chinese-tf_model.h5``` 更名为 ```tf_model.h5```-->
 
1. 训练命令举例: 开启terminal/cmd进入chat目录，然后输入命令，命令含义参照 [**Rasa文档**](https://rasa.com/docs/rasa/command-line-interface)
    ```shell
    rasa train -c config/config_pretrained_embeddings_mitie_zh.yml --data data/medical/M3-training_dataset_1564317234.json data/medical/stories.md --out models/medicalRasa2 --domain config/domains.yml --num-threads 5 --augmentation 100 -vv
    ```

## Shell方式测试模型
1. 修改```endpoints.yml```中的```tracker_store```字段，将数据库连接信息换成你自己的（现成的db或新建db皆可，
我新建了一个db，Rasa会生成一个名为```events```的表），```dialect```字段是用了
 [**SQLAlchemy**](https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)
里的，这个链接是Rasa官方文档在 [**Tracker Store**](https://rasa.com/docs/rasa/api/tracker-stores/)
给出的，详情参考官方文档

1. 若要自己定制消息记录方式，请修改```MyChannel/MyUtils.py```中数据库连接信息，并确保你的MySQL数据库中
有```message_received```表，当然你可以取别的名字，记得在```myio.py```的```handle_message```函数里把对应代码改掉

1. ```chat/MyActions```下的```actions.py```中同样需要先把neo4j数据库的链接信息改成你自己的

1. 打开2个终端，都cd到chat目录下，conda记得activate环境  

1. 一个终端（启动Action Server）
    ```shell
   rasa run actions --actions MyActions.actions --cors "*" -vv  
    ```
   
1. 另一个终端（Rasa Shell）
    ```shell
   rasa shell -m models/medicalRasa2/20201108-200002.tar.gz --endpoints config/endpoints.yml -vv
    ```

## 服务形式运行bot
1. 参照上方除了最后一步其他都一样

1. 另一个终端（启动NLU & Core Server）
    ```shell
   rasa run --enable-api -m models/medicalRasa2/20201108-200002.tar.gz --port 5000 --endpoints config/endpoints.yml --credentials config/credentials.yml -vv
    ```
   
1. 前端页面位于： [**ChatHTML**](https://github.com/pengyou200902/ChatHTML)
   如果用了我写的自定义socketio接口，请把前端中的socketPath做对应修改，默认就改成```/mysocket.io/```

1. *提示*：

    - 部署在服务器推荐使用```nohup```等类似的方式在后台运行 ，并将控制台输出指向指定的文件。 


## 参考
- 刘焕勇老师的 [**QABasedOnMedicalKnowledgeGraph**](https://github.com/liuhuanyong/QASystemOnMedicalKG)  

- 国内作者写的 [**Rasa_NLU_Chi**](https://github.com/crownpku/Rasa_NLU_Chi)，已经被rasa收入官方文档了，新版rasa已经有支持中文的方式了。
 
- 前端设计参考 [**WeatherBot**](https://github.com/howl-anderson/WeatherBot)，此项目采用的是nlu和core合并前的rasa。

- 所以前端使用了webchat.js， [**rasa-webchat**](https://github.com/mrbot-ai/rasa-webchat)

-  [**Scrapy**](https://scrapy.org)

-  [**Neo4j**](https://neo4j.org)

-  [**py2neo**](https://py2neo.org)

-  [**rasa-doc**](https://rasa.com/docs)或者旧版 [**legacy-rasa-doc**](https://legacy-docs.rasa.com/docs/)建议先看第一个
  
-  [**rasa-forum**](https://forum.rasa.com/)论坛上也会有很多问题的讨论，可以搜索  
