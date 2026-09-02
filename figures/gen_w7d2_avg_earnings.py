"""Week 7 第 1 章配图：单年盈利 vs 10 年平均（周期股示意案例）。

教学设计（全部示意数字，非任何真实公司）：某强周期公司 10 年每股盈利
0.8 / 1.4 / 2.6 / 3.4 / 4.0 / 3.0 / 1.6 / 0.6 / 1.2 / 1.4 元，合计 20.0 元，
平均恰为 2.0 元。顶部年 EPS 4.0 元、谷底年 EPS 0.6 元（用颜色区分 + 图例）。
若股价 40 元：用顶部年算 PE = 10 倍（最"便宜"），用平均算 PE = 20 倍。
布局：全部说明用"框 + 图例"，不用箭头，杜绝线条交叉与文字遮挡。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, label, C_BLUE, C_GREEN, C_ORANGE, C_RED

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

eps = [0.8, 1.4, 2.6, 3.4, 4.0, 3.0, 1.6, 0.6, 1.2, 1.4]
years = list(range(1, 11))
avg = sum(eps) / len(eps)  # = 2.0

fig, ax = plt.subplots(figsize=(11.5, 6.8))
ax.set_xlim(0.2, 10.8)
ax.set_ylim(0, 7.0)

colors = [C_BLUE] * 10
colors[4] = C_ORANGE   # 顶部年（第 5 年）
colors[7] = C_RED      # 谷底年（第 8 年）
ax.bar(years, eps, width=0.62, color=colors, zorder=3)

# 每根柱顶标数值
for x, v in zip(years, eps):
    ax.text(x, v + 0.12, f"{v}", ha="center", va="bottom", fontsize=10.5,
            color="#333333", weight="bold", zorder=5)

# 10 年平均线 + 右侧标签（右侧第 9、10 年柱顶 1.2/1.4 低于线，上方空白）
ax.axhline(avg, color=C_GREEN, lw=2.2, ls="--", zorder=4)
label(ax, 8.9, 2.32, "10 年平均 = 20.0 ÷ 10 = 2.0 元", color=C_GREEN,
      fontsize=11.5, weight="bold")

# 左上：PE 陷阱框（三行，紧凑）
ax.text(
    0.28, 6.7,
    "陷阱预演（第 2 章展开）：若股价 40 元，\n用顶部年算 PE = 40 ÷ 4.0 = 10 倍——最\u201c便宜\u201d；\n用平均算 PE = 40 ÷ 2.0 = 20 倍",
    fontsize=10.2, color="#333333", ha="left", va="top", linespacing=1.55,
    bbox=dict(boxstyle="round,pad=0.4", fc="#eef7ee", ec=C_GREEN, lw=1.2),
    zorder=6,
)

# 右上：图例说明两种颜色（不再用箭头指向柱子）
legend_handles = [
    mpatches.Patch(color=C_ORANGE, label="顶部年（第 5 年）"),
    mpatches.Patch(color=C_RED, label="谷底年（第 8 年）"),
]
ax.legend(handles=legend_handles, loc="upper right", fontsize=11,
          framealpha=0.95, bbox_to_anchor=(1.0, 1.0))

ax.set_xticks(years)
ax.set_xticklabels([f"第 {i} 年" for i in years], fontsize=10)
ax.set_ylabel("每股盈利 EPS（元）", fontsize=11)
ax.set_xlabel("（示意数字，教学用：某强周期公司 10 年 EPS，非任何真实公司）",
              fontsize=10)
ax.set_title("周期股的单年盈利大起大落，10 年平均才是\u201c常态\u201d（示意数字）",
             fontsize=13, pad=12)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

save(fig, "w7d2_avg_earnings.png")
