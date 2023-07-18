import datetime
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.log import logger
from nonebot import on_command
from haruka_bot.utils import (
    group_only,
)
from .data.lots_data import lots_data
from plugins import while_list_handle
from plugins.common_plugins_function import get_time_zone

query_lots = on_command(
    "古守抽签", aliases={
        "AA抽签",
        "钢板抽签",
        "铁板抽签",
        "平板抽签",
        "墙壁抽签",
        "小森抽签",
        "绝壁抽签",
        "夏小姐抽签",
        "夏诺雅抽签",
        "-8000抽签",
        "砧板抽签",
        "空港抽签",
        "古宝抽签",
        "白菜抽签",
        "uru抽签",
        "giaogiao抽签",
        "gaugau抽签",
        "熊熊抽签",
        "橘子抽签",
        "114514抽签",
        "1919810抽签",
        "1145141919810抽签"},
    priority=5,
)
query_lots.__doc__ = """诸葛抽签"""
query_lots.__help_type__ = None

query_lots.handle()(while_list_handle("lots"))
query_lots.handle()(group_only)

# 当前抽签对应的时间 及所有抽签人数
# 隔天判断query_date就行
query_lots_data = {
    "query_date_ymd": 0,
    "query_user_id": set()
}


@query_lots.handle()
async def _(
    event: GroupMessageEvent
):
    event_msg_extra_str = {
        "小森抽签": "小森是FCup哦！\n\n",
        "绝壁抽签": "夏诺雅：你才绝壁，你全家都绝壁，花Q！\n\n",
        "夏小姐抽签": "夏诺雅：nya~\n\n",
        "夏诺雅抽签": "夏诺雅：nya~\n\n",
        "白菜抽签": "白菜：ねえ、今どんな気持ち？\n\n",
        "giaogiao抽签": "星熊uru：no giao！yes gau！\n\n",
        "gaugau抽签": "星熊uru：gaugau~\n\n",
        "橘子抽签": "橘子前辈：快进字幕组！\n\n",
        "114514抽签": "哼！哼！哼！啊啊啊啊啊啊啊啊！！！！！\n\n",
        "1919810抽签": "哼！哼！哼！啊啊啊啊啊啊啊啊！！！！！\n\n",
        "1145141919810抽签": "哼！哼！哼！啊啊啊啊啊啊啊啊！！！！！\n\n",
    }
    # 一个彩蛋
    pre_str = event_msg_extra_str.get(str(event.message), "")

    # 根据QQ号和今日时间决定一个唯一的签
    datetime_ymd = int(datetime.datetime.now(get_time_zone()).strftime('%Y%m%d'))
    user_id = event.user_id
    # 如果是新的一天 就清空query_user_id的数据
    if query_lots_data["query_date_ymd"] != datetime_ymd:
        query_lots_data["query_user_id"].clear()
        query_lots_data["query_date_ymd"] = datetime_ymd
    if user_id in query_lots_data["query_user_id"]:
        # 已经抽签了不能再重复抽
        msg = Message(f"[CQ:reply,id={event.message_id}]") + Message(pre_str + "今日已进行抽签，无法再次抽签！")
        await query_lots.finish(msg)
    else:
        query_lots_data["query_user_id"].add(user_id)
        lots_key = (datetime_ymd * user_id) % len(lots_data)
        lots_str = f"抽到第{lots_key}签\n" \
                   f"签名：{lots_data[lots_key]['lots_name']}\n" \
                   f"签语：{lots_data[lots_key]['lots_title']}\n" \
                   f"解签：{lots_data[lots_key]['lots_meaning']}"
        msg = Message(f"[CQ:reply,id={event.message_id}]") + Message(pre_str + lots_str)
        await query_lots.finish(msg)
