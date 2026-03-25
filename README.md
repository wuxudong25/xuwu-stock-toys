# xuwu-stock-toys
some stock analysis toys based on tushare

## AllTick 黄金日K脚本

新增脚本：`alltick_gold_kline.py`，用于调用 AllTick 的 `/quote-b-api/kline` 接口，查询黄金（默认 `GOLD`）最近2根日K并输出“昨日”那根K线。

用法：

```bash
python3 alltick_gold_kline.py --token '<你的token>'
# 或者
ALLTICK_TOKEN='<你的token>' python3 alltick_gold_kline.py
```
