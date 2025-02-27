import os
import json
import requests
import logging
from robot import constants

logger = logging.getLogger(__name__)

INTENT_LIST = []
ENTITY_LIST = []


def getNLU(query, api_base, model):
    examples = open(os.path.join(constants.DATA_PATH, "intent_examples.json"), "a+")

    def make_prompt(user_query):
        nlu_prompt = (f"""# 背景 #
你是一个优秀的语言学家，数据标注员。
# 目标 #
你的任务是在家庭语音助手的情景下，标注并提取用户对话中的意图和实体，主要包括{'、'.join(INTENT_LIST)}这{len(INTENT_LIST)}种意图，以及{'、'.join(ENTITY_LIST)}等类型实体。
需要注意不要捏造答案，所有结果均需来自用户输入的原文。如果句子中没有任何上述意图或相关实体，则不标注，不提取意图或实体。

# 响应 #
JSON格式的数据

<<<
下面是一些意图识别和实体识别的例子：
{examples}
>>>

输入：{user_query}
输出："""
        )

        return nlu_prompt

    msg = make_prompt(query)

    logger.info("msg: " + msg)

    header = {
        "Content-Type": "application/json",
    }

    data = {"model": model, "prompt": msg, "stream": False}
    logger.info("开始意图实体识别")
    url = api_base + "/api/generate"
    # 请求接收流式数据
    try:
        response = requests.request(
            "POST",
            url,
            headers=header,
            json=data,
            stream=False,
        )

        message = response.message
        respond = message.content
        return respond
    except Exception:
        logger.critical(
            "llm nlu failed to response for %r", msg, exc_info=True
        )
        return "抱歉，LLM 回答失败"


def getIntent(parsed):
    return ""


def hasIntent(parsed, intent):
    return True


def getSlots(parsed, intent=""):
    return []


def getSlotWords(parsed, intent, name):
    return []


def getSlotOriginalWords(parsed, intent, name):
    return []


def getSayByConfidence(parsed):
    return ""


def getSay(parsed, intent=""):
    return ""


if __name__ == "__main__":
    parsed = getNLU(
        "今天的天气",
        "S13442",
        "w5v7gUV3iPGsGntcM84PtOOM",
    )
    print(parsed)

