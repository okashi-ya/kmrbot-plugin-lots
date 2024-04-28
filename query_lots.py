import datetime
from typing import Tuple, Any
from protocol_adapter.adapter_type import AdapterGroupMessageEvent
from protocol_adapter.protocol_adapter import ProtocolAdapter
from nonebot import on_regex
from . import data
from nonebot.params import RegexGroup
from utils.permission import white_list_handle
from utils import group_only, get_time_zone

query_lots = on_regex(
    pattern=r"^(.*)抽签$",
    priority=5,
)


query_lots.__doc__ = """抽签"""
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
    pre_str = data.get_lots_pre(params[0])
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
        lots_info = data.get_lots_text_info((datetime_ymd * user_id) % 167342993)
        lots_str = f"抽到第{lots_info['value']}签\n" \
                   f"签名：{lots_info['name']}\n" \
                   f"签语：{lots_info['title']}\n" \
                   f"解签：{lots_info['meaning']}"
        msg = ProtocolAdapter.MS.reply(event) + ProtocolAdapter.MS.text(pre_str + lots_str)
        await query_lots.finish(msg)
