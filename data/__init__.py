import json
import os.path
from typing import Optional
from nonebot.log import logger

# emoji_key_data的数据是字典嵌套字典，每一层字典的key都可能是左emojiCode或右emojiCode
emoji_key_data = {}


def load_lots_data():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "lots_data.json"), encoding="utf-8") as f:
        return json.load(f)


def get_lots_pre(pre_name: str) -> Optional[str]:
    lots_data = load_lots_data()
    # 这里为了可以热更 就遍历了 反正也没多少
    for pre_info in lots_data.get("pre", []):
        if pre_info["name"] == pre_name:
            return pre_info["text"]
    return None


def get_lots_text_info(lots_key: int):
    lots_data = load_lots_data()
    if len(lots_data.get("lots_info", [])) == 0:
        logger.error(f"get_lots_text fail ! lots_info size invalid !")
        return "抽签错误"
    lots_id = lots_key % len(lots_data.get("lots_info", []))
    data = lots_data["lots_info"][lots_id]
    return {
        "value": data["lots_value"],
        "name": data["lots_name"],
        "title": data["lots_title"],
        "meaning": data["lots_meaning"],
    }
