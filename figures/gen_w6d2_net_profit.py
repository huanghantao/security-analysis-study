"""Week 6 第 2 章配图：净利润 vs 扣非净利润 对比柱状图。

教学设计（示意数字，非任何真实公司）：某公司连续 5 年报表净利润"稳定"在 10 亿，
但扣除非经常性损益后大幅波动，甚至有一年扣非亏损——
"年年异常的一次性项目"把主业亏损藏进了非经常科目。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, C_BLUE, C_ORANGE, C_RED

import matplotlib.pyplot as plt

years = ["第 1 年\n卖子公司股权", "第 2 年\n卖厂房 + 补助", "第 3 年\n补助 + 退税",
         "第 4 年\n理财浮盈", "第 5 年\n资产处置"]
net_profit = [10, 10, 10, 10, 10]        # 报表净利润（含非经常）
deducted = [5, -1, 2, 7, 8]              # 扣非净利润

x = range(len(years))
fig, ax = plt.subplots(figsize=(10.5, 6.4))
ax.axhline(0, color="#999999", lw=1)

b1 = ax.bar([i - 0.2 for i in x], net_profit, width=0.38, color=C_BLUE,
            label="净利润（报表口径）")
b2 = ax.bar([i + 0.2 for i in x], deducted, width=0.38, color=C_ORANGE,
            label="扣非净利润（剔一次性）")

# 数值标签
for i, v in enumerate(net_profit):
    ax.text(i - 0.2, v + 0.25, f"{v}", ha="center", va="bottom",
            fontsize=10.5, color="#1f4e79", weight="bold")
for i, v in enumerate(deducted):
    if v >= 0:
        ax.text(i + 0.2, v + 0.25, f"{v}", ha="center", va="bottom",
                fontsize=10.5, color="#a05a00", weight="bold")
    else:
        ax.text(i + 0.2, v - 0.35, f"{v}", ha="center", va="top",
                fontsize=10.5, color=C_RED, weight="bold")

# 结论标注：框放在最上方空白区，箭头垂直落到第 2 年扣非柱的正上方，
# 全程走在两根柱子之间的空隙里，不穿过任何柱子和数字。
ax.annotate(
    "报表净利 5 年都是 10 亿，\n其中 3 年靠\u201c一次性\u201d收益撑住——\n主业其实赚 2 亿、亏 1 亿",
    xy=(1.2, 0.35), xytext=(0.02, 14.7), fontsize=11, color="#333333",
    ha="left", va="top",
    bbox=dict(boxstyle="round,pad=0.4", fc="#fdecea", ec=C_RED, lw=1.2),
    arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.6,
                    connectionstyle="arc3,rad=0"),
    zorder=6,
)

ax.set_xticks(list(x))
ax.set_xticklabels(years, fontsize=10)
ax.set_ylim(-3, 15)
ax.set_ylabel("亿元", fontsize=11)
ax.set_title("净利润 vs 扣非净利润：\u201c年年异常\u201d的一次性项目如何托住净利润（示意数字，教学用）",
             fontsize=12.5, pad=12)
ax.set_xlabel("（年份、公司、事件均为教学示意；一次性项目类型写在横轴第二行）", fontsize=10)
ax.legend(loc="upper right", fontsize=10.5, framealpha=0.95)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

save(fig, "w6d2_net_profit.png")
