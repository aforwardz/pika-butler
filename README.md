# pika-butler
## 说明
* 本项目基于[wukong-robot](https://github.com/wzpan/wukong-robot)项目3.5.3 版本（202307），感谢作者@wzpan 的开源
* 本项目目标：**完全离线版**wukong-robot，也是出于隐私保护的目的，主要计划在asr、tts等在线服务替换使用自己训练和组建的服务（跑在家庭服务器上）
* 因此本项目代码继续开源，主要修改在于接入模块以及定制化功能

## 优势
1. **注重个人隐私，不POST任何外网api**
2. 本地服务处理更快，大程度降低延时，提高体验
3. 高度定制化，方便加入自定义功能

## 劣势
1. 需要本地服务器，性能越高越好
2. 本地服务需要自己搭建

ps：以上对我来说不算劣势


## 功能&特性
保留一些基础功能，使用场景在家中室内，部署在~~树莓派上~~（硬件性能还是不够好）服务器上

目标计划：
1. 主要模型服务由内网服务器提供，尽量不使用其他厂商接口服务：更安全、更省钱、更定制化、更快速（需优化）
2. 训练自己和老婆的声音合成器，用于tts；当我说话时使用老婆声音对话，反之亦然；提升对话真实感
3. 其他个性任务如足球赛事播报等

### TODOS:
- [x] 训练生成自定义离线唤醒词
- [x] ~~本地化TTS服务（使用[vits-simple-api](https://github.com/Artrajz/vits-simple-api)解决）~~
- [x] 本地化TTS服务（使用[GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)解决）
- [x] ~~本地化ASR服务（使用[espnet](https://github.com/espnet/espnet)解决, 模型采用pengcheng_guo大佬基于wenetspeech数据集训练的[模型](https://huggingface.co/espnet/pengcheng_guo_wenetspeech_asr_train_asr_raw_zh_char)）~~
- [x] 本地化ASR服务（使用[FunASR](https://github.com/modelscope/FunASR)解决, 模型采用阿里达摩院的中文通用识别[模型](https://www.modelscope.cn/models/iic/speech_paraformer_asr_nat-zh-cn-16k-common-vocab8358-tensorflow1)）
- [x] ~~本地化Chat服务（接入ChatGLM2）~~
- [x] DeepSeek接入
- [ ] 本地化NLU服务（考虑使用大模型）
- [ ] 常用指令功能
- [ ] 多音箱就近唤醒、就近播放
- [ ] 说话对象识别（声纹识别）
- [ ] 使用自己的模型合成语音

### FEATURES:
- [ ] 更优雅的天气播报
- [ ] 更优雅的定时任务
- [ ] 赛事播报


## 开发日志
### 【2024.07】

[官方文档](https://wukong.hahack.com/#/README)对于大部分问题都有记录，很详细

### 训练唤醒词
按照文档使用snowboy离线训练服务训练一个自己的唤醒词模型，导出pdml文件放在指定目录即可

### ~~vits-simple-api~~
~~按照说明安装，模型只下了原神（**不玩原神！**）的模型，因为感觉雷电将军的御姐音好听，在config文件里配置好speaker id就行~~

### ~~espnet2~~
~~多种方式安装尝试发现直接pip安装也ok，不需要源码编译~~

~~pip install espnet~~

~~安装好后环境包里会有espnet2，另外需安装espnet-model-zoo~~

### ~~chatglm2~~
~~根据[ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)部署， 运行其open_api.py启动类似openai接口的服务~~

### 消除回声
测试时发现回答播放的语音又会被麦克风录入，导致自己无限对话，安装[消除回声](https://wukong.hahack.com/#/tips?id=_32%ef%bc%9a%e5%bc%80%e5%90%af%e5%9b%9e%e5%a3%b0%e6%b6%88%e9%99%a4)文档消除回声

### 声纹识别
使用[VoiceprintRecognition](https://github.com/yeyupiaoling/VoiceprintRecognition-Pytorch)进行声纹识别

### 人脸识别
使用[face_recognition](https://github.com/ageitgey/face_recognition/)进行人脸识别，经测试，效果很不错


### 【2025.02】
先略过语音部分，使用WIFI并支持TTS的喇叭进行流程实验

计划接入DeepSeek，替换ChatGLM2

### 【2025.02.27】
进行了TTS和ASR方案替换和接入，测试通过

本地部署DeepSeek R1 32B并接入，实测全流程效果达到初步预期，全服务均为本地

### GPT-SoVITS
按照说明安装，过程有部分坑，安装好后启动api服务

### FunASR
按照说明安装，并下载识别模型，代码里通过AutoModel调用

### DeepSeek
通过Ollama本地部署（需要再加两根内存条）

