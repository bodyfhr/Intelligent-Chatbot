## 目录
- [Rasa版本](#Rasa版本)
- [在线测试地址](#在线测试地址)
- [效果图展示](#效果图展示)
- [系统说明](#系统说明)
- [环境配置](#环境配置)
- [数据库存储数据](#数据库存储数据)
- [训练模型](#训练模型)
- [测试模型](#测试模型)
- [运行服务](#运行服务)
- [系统参考](#系统参考)


## Rasa版本
- 此处为***Rasa==1.9.5***(其它Rasa版本请切换branch)


## 在线测试地址
- http://www.ylznwz.work:5000/

- 在线测试网址用的是腾讯云低配的服务器，加载速度慢，各位轻虐~~ >.<


## 效果图展示

![image](static/img/demo-1.gif)

![image](static/img/demo-2.gif)


## 系统说明
本系统是基于 [**Rasa-1.9.5**](https://rasa.com/) 版本及其支持的外部组件实现的智能聊天机器人系统，
具体包括闲聊和天气查询，智能问答等功能。

- Rasa的```Pipeline```配置如下：
    ```yaml
    pipeline:
      - name: "MitieNLP"
        model: "data/total_word_feature_extractor_zh.dat"
      - name: "JiebaTokenizer"
        dictionary_path: "data/dict"
      - name: "MitieEntityExtractor"
      - name: "EntitySynonymMapper"
      - name: "RegexFeaturizer"
      - name: "MitieFeaturizer"
      - name: "EmbeddingIntentClassifier"
    ```

- ***注意***： rasa-nlu和rasa-core已经合并成rasa


## 环境配置
1. python 3.6 +

2. 下载zip包或者git clone 

3. 进入Intelligent-Chatbot目录，conda记得activate环境

4. 安装Mitie其实很简单，具体步骤如下：
- conda activate激活你的python环境（或者venv激活）
- pip或者conda install cmake以及boost
- 终端或者cmd进入你的工作目录或者随便哪里，git clone https://github.com/mit-nlp/MITIE.git
- cd进MITIE的文件夹，python setup.py build
- 最后 python setup.py install

5. 然后在命令行使用命令安装项目需求的依赖包
    ```shell
   pip install -r requirements.txt
    ```
   
6. *提示*：

    - 国内推荐使用镜像加速（此命令是临时使用镜像，并非全局都用），比如：
        ```shell
        pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
        ```
   
    - 如果你有代理，可以在pip install命令后加上 --proxy=地址:端口


## 数据库存储数据
- 本系统是采用MySQL数据库,具体配置如下(系统配置文件：\Intelligent-Chatbot\chat\MyChannel\MyUtils.py):
 ```
 def get_record_db_cursor():
        db = pymysql.connect(
            host="localhost",
            port=端口号,
            user="用户名",
            passwd="密码",
            db="数据库名",
            charset="utf8",
    )
  ```
- 本系统主要存储的数据有:用户id,会话id,用户输入的内容,问答时间,用户ip地址。(系统配置文件：\Intelligent-Chatbot\chat\MyChannel\myio.py)
 ```
 用户id（user_id）：用于不同用户，就相当给定每个用户一个号码。因为同时访问该系统的用户非常多，我们要将区分开来。
 会话id（session_id）：用于解决用户每一轮的对话。用户输入对话有可能是单轮，也有可能是多轮，因此我们要将每一轮对话区分开来，也是为了解决这一轮对话结束，开启新一轮对话的标志。
 用户输入的内容（content）：用于记录用户每一轮输入对话的内容。
 问答时间（when）：用于记录用户每一轮提问的时间。
 用户ip地址（ip_address）：用于记录用户访问系统的用户IP地址。
 ```


## 训练模型
1. Rasa训练数据集的构造：使用到了 [**Chatito工具**](https://rodrigopivi.github.io/Chatito/) 

2. 下载用于mitie的模型文件放到```chat/data```文件夹下， [**百度网盘**](https://pan.baidu.com/s/1kNENvlHLYWZIddmtWJ7Pdg) ，密码：p4vx，
或者 [**Mega云盘**](https://mega.nz/#!EWgTHSxR!NbTXDAuVHwwdP2-Ia8qG7No-JUsSbH5mNQSRDsjztSA) 
 
3. 训练命令举例: 开启控制台,进入\Intelligent-Chatbot\chat目录下，然后输入命令，命令含义参照 [**Rasa文档**](https://rasa.com/docs/rasa/command-line-interface)
    ```shell
    rasa train --config config/zh_jieba_mitie_embeddings_config.yml --domain config/domain.yml --out models/medicalRasa2 --data data/ 
    ```

## 测试模型
1. 修改```endpoints.yml```中的```tracker_store```字段，将数据库连接信息换成你自己的（现成的db或新建db皆可，
我新建了一个db，Rasa会生成一个名为```events```的表），```dialect```字段是用了
 [**SQLAlchemy**](https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)
里的，这个链接是Rasa官方文档在 [**Tracker Store**](https://rasa.com/docs/rasa/api/tracker-stores/)
给出的，详情参考官方文档

2. 若要自己定制消息记录方式，请修改```MyChannel/MyUtils.py```中数据库连接信息，并确保你的MySQL数据库中
有```message_received```表，当然你可以取别的名字，记得在```myio.py```的```handle_message```函数里把对应代码改掉

3. 打开2个终端，记得在虚拟环境下。
- 一个终端（启动Action服务，无需切换到chat目录下）
    ```shell
   rasa run actions --actions actions --cors "*" -vv
    ```
- 另一个终端（Rasa Shell，需切换到chat目录下）
    ```shell
   rasa shell -m models/medicalRasa2/20210521-180159.tar.gz --endpoints config/endpoints.yml -vv
    ```

## 运行服务
打开3个终端控制台，记得在虚拟环境下。
- 第一个终端（启动Action服务，无需切换到chat目录下）
    ```shell
   rasa run actions --actions actions --cors "*" -vv
    ```
- 第二个终端（启动Rasa服务，需切换到chat目录下）
    ```shell
  rasa run --enable-api -m models/medicalRasa2/20210521-180159.tar.gz --port 5005 --endpoints config/endpoints.yml --credentials config/credentials.yml -vv
    ```
- 第三个终端（启动服务器，无需切换到chat目录下）
    ```shell
    python ask.py
    ```

## 系统参考
- 刘焕勇老师的 [**QABasedOnMedicalKnowledgeGraph**](https://github.com/liuhuanyong/QASystemOnMedicalKG)  

- 国内作者写的 [**Rasa_NLU_Chi**](https://github.com/crownpku/Rasa_NLU_Chi)，已经被rasa收入官方文档了，新版rasa已经有支持中文的方式了。
 
- 前端设计参考 [**WeatherBot**](https://github.com/howl-anderson/WeatherBot)，此项目采用的是nlu和core合并前的rasa。

- 所以前端使用了webchat.js， [**rasa-webchat**](https://github.com/mrbot-ai/rasa-webchat)

-  [**py2neo**](https://py2neo.org)

-  [**rasa-doc**](https://rasa.com/docs)或者旧版 [**legacy-rasa-doc**](https://legacy-docs.rasa.com/docs/)建议先看第一个
  
-  [**rasa-forum**](https://forum.rasa.com/)论坛上也会有很多问题的讨论，可以搜索  
