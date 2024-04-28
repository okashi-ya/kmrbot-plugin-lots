import datetime
from typing import Tuple, Any
from protocol_adapter.adapter_type import AdapterGroupMessageEvent
from protocol_adapter.protocol_adapter import ProtocolAdapter
from nonebot import on_command, on_regex
from .data.lots_data import lots_data
from nonebot.params import RegexGroup
from utils.permission import white_list_handle
from utils import group_only, get_time_zone

query_lots = on_regex(
    pattern=r"^(.*)抽签$",
    priority=5,
)

lots_pre = {
    "古守": "",
    "AA": "",
    "钢板": "",
    "平板": "",
    "墙壁": "",
    "-8000": "",
    "砧板": "",
    "空港": "",
    "古宝": "",
    "nano": "切り抜かないで～\n\n",
    "土豆": "切り抜かないで～\n\n",
    "小森": "小森是FCup哦！\n\n",
    "绝壁": "夏诺雅：你才绝壁，你全家都绝壁，花Q！\n\n",
    "夏小姐": "夏诺雅：nya~\n\n",
    "夏诺雅": "夏诺雅：nya~\n\n",
    "白菜": "白菜：ねえ、今どんな気持ち？\n\n",
    "uru": "",
    "giaogiao": "星熊uru：no giao\n\n",
    "gaugau": "星熊uru：gaugau~\n\n",
    "熊熊": "",
    "橘子": "橘子前辈：快进字幕组！\n\n",
    "mimo": "mimo：已经不是橘子的mimo了！\n\n",
    "114514": "哼！哼！哼！啊啊啊啊啊啊啊啊！！！！！\n\n",
    "1919810": "哼！哼！哼！啊啊啊啊啊啊啊啊！！！！！\n\n",
    "1145141919810": "哼！哼！哼！啊啊啊啊啊啊啊啊！！！！！\n\n",
}

query_lots.__doc__ = """古守抽签"""
query_lots.__help_type__ = None

query_lots.handle()(white_list_handle("lots"))
query_lots.handle()(group_only)

# 当前抽签对应的时间 及所有抽签人数
# 隔天判断query_date就行
query_lots_data = {
    "query_date_ymd": 0,
    "query_user_id": set()
}


@query_lots.handle()
async def _(
        event: AdapterGroupMessageEvent,
        params: Tuple[Any, ...] = RegexGroup(),
):
    # 一个彩蛋
    pre_str = lots_pre.get(params[0])
    if pre_str is None:
        return await query_lots.finish()

    # 根据QQ号和今日时间决定一个唯一的签
    datetime_ymd = int(datetime.datetime.now(get_time_zone()).strftime('%Y%m%d'))
    user_id = int(event.get_user_id())
    # 如果是新的一天 就清空query_user_id的数据
    if query_lots_data["query_date_ymd"] != datetime_ymd:
        query_lots_data["query_user_id"].clear()
        query_lots_data["query_date_ymd"] = datetime_ymd
    if user_id in query_lots_data["query_user_id"]:
        # 已经抽签了不能再重复抽
        msg = ProtocolAdapter.MS.reply(event) + ProtocolAdapter.MS.text(pre_str + "今日已进行抽签，无法再次抽签！")
        await query_lots.finish(msg)
    else:
        query_lots_data["query_user_id"].add(user_id)
        # 增加一个无理数用来保证尽可能不会让结果相同
        # 因167342993是一个无理数 且datetime_ymd 比 167342993大的多
        # 所以不可能出现因时间原因导致大范围抽签结果相同的情况出现
        # 在几年内是不会出现重复问题的，够用
        lots_key = (datetime_ymd * user_id) % 167342993 % len(lots_data)
        lots_str = f"抽到第{lots_data[lots_key]['lots_value']}签\n" \
                   f"签名：{lots_data[lots_key]['lots_name']}\n" \
                   f"签语：{lots_data[lots_key]['lots_title']}\n" \
                   f"解签：{lots_data[lots_key]['lots_meaning']}"
        msg = ProtocolAdapter.MS.reply(event) + ProtocolAdapter.MS.text(pre_str + lots_str)
        await query_lots.finish(msg)
