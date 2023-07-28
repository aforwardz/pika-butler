# pika-butler
## 说明
* 本项目基于[wukong-robot](https://github.com/wzpan/wukong-robot)项目3.5.3 版本（202307），感谢作者@wzpan 的开源
* 因家庭需求以及个人职业相关，主要计划在asr、tts等engine模块使用自己训练和组建的服务（跑在家庭服务器上13900KF+4090）
* 因此本项目代码继续开源，主要修改在于接入模块

## 优势
1. **注重个人隐私，不POST任何外网api**
2. 本地服务处理更快，大程度降低延时，提高体验
3. 高度定制化，方便加入自定义功能

## 劣势
1. 需要本地服务器，性能越高越好
2. 本地服务需要自己搭建，没有调API 

ps：以上对我来说不算劣势


## 功能&特性
保留一些基础功能，使用场景在家中室内，部署在树莓派上

计划更新：
1. 主要模型服务由内网服务器提供，尽量不使用其他厂商接口服务：更安全、更省钱、更定制化、更快速（需优化）
2. 训练自己和老婆的声音合成器，用于tts；当我说话时使用老婆声音对话，反之亦然；提升对话真实感
3. 其他个性任务如足球赛事播报等

### TODOS:
- [x] 训练生成自定义离线唤醒词
- [x] 本地化TTS服务（使用[vits-simple-api](https://github.com/Artrajz/vits-simple-api)解决）
- [x] 本地化ASR服务（使用[espnet](https://github.com/espnet/espnet)解决, 模型采用pengcheng_guo大佬基于wenetspeech数据集训练的[模型](https://huggingface.co/espnet/pengcheng_guo_wenetspeech_asr_train_asr_raw_zh_char)）
- [ ] 本地化NLU服务
- [x] 本地化Chat服务（接入ChatGLM2）
- [ ] ASR识别说话对象
- [ ] 使用自己的模型合成语音

### FEATURES:
- [ ] 更优雅的天气播报
- [ ] 更优雅的定时任务
- [ ] 赛事播报


## 记录
[官方文档](https://wukong.hahack.com/#/README)对于大部分问题都有记录，很详细

### 训练唤醒词
按照文档使用snowboy离线训练服务训练一个自己的唤醒词模型，导出pdml文件放在指定目录即可

### vits-simple-api
按照说明安装，模型只下了原神（**不玩原神！**）的模型，因为感觉雷电将军的御姐音好听，在config文件里配置好speaker id就行

### espnet2
多种方式安装尝试发现直接pip安装也ok，不需要源码编译
```shell
pip install espnet
```
安装好后环境包里会有espnet2，另外需安装espnet-model-zoo

### chatglm2
根据[ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)部署， 运行其open_api.py启动类似openai接口的服务

### 消除回声
测试时发现回答播放的语音又会被麦克风录入，导致自己无限对话，安装[消除回声](https://wukong.hahack.com/#/tips?id=_32%ef%bc%9a%e5%bc%80%e5%90%af%e5%9b%9e%e5%a3%b0%e6%b6%88%e9%99%a4)文档消除回声

