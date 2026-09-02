"""Week 2 - 02 章：从收入到净利润的瀑布图（小满奶茶店第 1 年示意数字）。"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, C_BLUE, C_GREEN, C_ORANGE, C_PURPLE, C_RED, C_GRAY

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# (名称, 底部, 高度, 颜色, 顶部标注文字)
bars = [
    ("营业收入", 0,   100, C_BLUE,   "100"),
    ("营业成本", 70,  30,  C_RED,    "−30"),
    ("毛利",     0,   70,  C_GREEN,  "70"),
    ("期间费用", 30,  40,  C_RED,    "−40"),
    ("折旧",     22,  8,   C_ORANGE, "−8"),
    ("营业利润", 0,   22,  C_GREEN,  "22"),
    ("利息费用", 20,  2,   C_RED,    "−2"),
    ("净利润",   0,   20,  C_PURPLE, "20"),
]

fig, ax = plt.subplots(figsize=(12.5, 6.2))
xs = range(len(bars))
for i, (name, bottom, height, color, text) in enumerate(bars):
    ax.bar(i, height, bottom=bottom, width=0.62, color=color,
           edgecolor="white", zorder=3)
    ax.text(i, bottom + height + 2.2, text, ha="center", va="bottom",
            fontsize=11.5, color="#333333", zorder=5)

# 瀑布连接线（上一根柱的累计水平 → 下一根柱）
levels = [100, 70, 70, 30, 22, 22, 20]
for i, lv in enumerate(levels):
    ax.plot([i + 0.31, i + 1 - 0.31], [lv, lv], color=C_GRAY,
            lw=1.1, ls="--", zorder=2)

ax.set_xticks(list(xs))
ax.set_xticklabels([b[0] for b in bars], fontsize=11.5)
ax.set_ylim(0, 114)
ax.set_xlim(-0.55, len(bars) - 0.45)
ax.set_ylabel("金额（万元）", fontsize=11.5)
ax.set_title("小满奶茶店第 1 年：从收入到净利润的瀑布（示意数字，不考虑所得税）",
             fontsize=13.5, pad=12)
ax.grid(axis="y", alpha=0.28, zorder=0)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

# 右上角：两个比率
ax.text(5.55, 62,
        "毛利率 = 70 / 100 = 70%\n净利率 = 20 / 100 = 20%",
        ha="center", va="center", fontsize=11.5, color="#333333",
        linespacing=1.8, zorder=5,
        bbox=dict(boxstyle="round,pad=0.45", fc="#f7f7f2", ec="#cccccc"))

legend_items = [
    Patch(facecolor=C_BLUE, label="起点：营业收入"),
    Patch(facecolor=C_RED, label="减项：成本与费用"),
    Patch(facecolor=C_GREEN, label="小计：毛利 / 营业利润"),
    Patch(facecolor=C_PURPLE, label="终点：净利润"),
]
ax.legend(handles=legend_items, loc="upper right", fontsize=10.5, framealpha=0.95)

save(fig, "w2d3_income_waterfall.png")
