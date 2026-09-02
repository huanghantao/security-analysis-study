"""Week 4 第 2 章配图：可转债价值线（示意数字）。

横轴：正股股价；纵轴：转债价值。
三条线：债券底价（水平线 100 元）、转换价值（斜线 = 2 × 股价）、
市价（取两者的较大者再加溢价，溢价随股价上涨收敛）。
教学例子与正文一致：面值 100 元、转股价 50 元、转换比率 2 股。

输出：figures/out/w4d3_convertible.png
"""

import sys, pathlib

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, C_GREEN, C_GRAY, C_ORANGE, C_RED

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(11.5, 6.8))

FACE = 100.0   # 面值 / 债底（示意）
CONV_P = 50.0  # 转股价（示意）
RATIO = FACE / CONV_P  # 转换比率：每张转债换 2 股

# 市价采样点（示意：底价与转换价值取大者，再加逐步收敛的溢价）
xs = np.array([30, 33, 36, 40, 43, 46, 50, 53, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 95])
mkt = np.array([101, 101.5, 102, 103.5, 104.8, 107, 115, 118, 120, 124,
                132, 140, 147, 154.5, 162, 169.8, 177.6, 185.6, 191])
lower = np.maximum(FACE, RATIO * xs)

# 转换溢价区（市价与"取大者"之间）
ax.fill_between(xs, lower, mkt, color=C_ORANGE, alpha=0.30, lw=0, zorder=2)

# 债券底价：水平线
ax.axhline(FACE, color=C_GRAY, lw=2.2, ls=(0, (6, 3)), zorder=3)
# 转换价值：斜线
ax.plot([30, 98], [RATIO * 30, RATIO * 98], color=C_GREEN, lw=2.4, zorder=3)
# 市价：曲线
ax.plot(xs, mkt, color=C_RED, lw=2.6, zorder=4)

# 转股价竖直参考线（画在底价以下，避免与线群纠缠）
ax.plot([CONV_P, CONV_P], [57, FACE], color=C_GRAY, lw=1.5, ls=":", zorder=2)
ax.plot([CONV_P], [FACE], marker="o", ms=7, color=C_RED, zorder=5)

ax.set_xlim(15, 100)
ax.set_ylim(55, 205)
ax.grid(alpha=0.22, ls=":")
ax.set_xlabel("正股股价（元）", fontsize=12)
ax.set_ylabel("转债价值（元）", fontsize=12)
ax.set_title("可转债价值地图：跌有底、涨跟涨（全部为示意数字）", fontsize=13.5, pad=10)

ax.annotate("债券底价 100 元（保底线）\n股价再跌，市价也贴着底价走",
            xy=(20, 93), fontsize=11, ha="left", va="top", color="#444444")
ax.annotate("转股价 50 元（示意）\n股价 = 50 时，转换价值恰好 = 面值",
            xy=(50, 68), fontsize=10.5, ha="center", va="top", color="#444444",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.9))
ax.annotate("转换价值 = 2 × 股价：涨跟涨",
            xy=(82, 135), fontsize=11, ha="center", va="top", color="#1a6b1a",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.9))
ax.annotate("阴影 = 转换溢价区\n（市价高出底价的部分）",
            xy=(31.5, 116), fontsize=10.5, ha="left", va="center", color="#7a4a00")

from matplotlib.lines import Line2D
from matplotlib.patches import Patch

handles = [
    Line2D([], [], color=C_GRAY, lw=2.2, ls=(0, (6, 3)), label="债券底价（保底）"),
    Line2D([], [], color=C_GREEN, lw=2.4, label="转换价值 = 2 × 股价"),
    Line2D([], [], color=C_RED, lw=2.6, label="转债市价（示意）"),
    Patch(facecolor=C_ORANGE, alpha=0.30, label="转换溢价区"),
]
ax.legend(handles=handles, loc="upper left", fontsize=10.5, framealpha=0.95)

fig.tight_layout()
save(fig, "w4d3_convertible.png")
