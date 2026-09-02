"""Week 1 / 第 2 章：价格围绕价值区间波动 + 安全边际示意。

左图：市场价像钟摆一样围绕"价值区间"上下摆动；
右图：只有当买入价低于价值区间下沿时，中间的差才是安全边际。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, label, C_BLUE, C_RED, C_GREEN, C_GRAY

import numpy as np
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.6))

# ---------------------------------------------------------------- 左图：价格围绕价值波动
t = np.linspace(0, 120, 600)
price = 30 + 17 * np.sin(t / 9.0) + 5 * np.sin(t / 3.3 + 1.2)

ax1.axhspan(20, 40, color=C_BLUE, alpha=0.15, zorder=1)
ax1.axhline(30, color=C_BLUE, lw=1.2, ls=":", zorder=2)
ax1.plot(t, price, color=C_RED, lw=2.2, zorder=3)

# 价值区间说明（放在价格线下方的空白区，用小箭头指向蓝色区间）
label(ax1, 16, 9.3, "内在价值区间（示意）\n20~40 元\n虚线 = 中枢 30 元",
      color=C_BLUE, fontsize=10)
ax1.annotate("", xy=(16, 18.6), xytext=(16, 13.1),
             arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.6), zorder=4)

# 找出前半段最低点与最高点做标注（坐标由数据决定）
i_low = int(np.argmin(price[:250]))
i_high = int(np.argmax(price[:120]))
x_low, y_low = t[i_low], price[i_low]
x_high, y_high = t[i_high], price[i_high]

ax1.annotate("跌得远低于价值：\n机会出现（安全边际大）",
             xy=(x_low, y_low), xytext=(x_low + 16, y_low - 9),
             fontsize=11, color=C_GREEN, ha="center", va="top",
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_GREEN, lw=1.2),
             arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1.6), zorder=5)
ax1.annotate("涨得远高于价值：\n危险（透支未来）",
             xy=(x_high, y_high), xytext=(x_high + 12, y_high + 4.5),
             fontsize=11, color=C_RED, ha="center", va="bottom",
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_RED, lw=1.2),
             arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.6), zorder=5)

label(ax1, 121, 45.8, "市场价", color=C_RED, fontsize=12, ha="right")
ax1.set_title("价格像钟摆：围绕价值上下波动", fontsize=14, pad=12)
ax1.set_xlabel("时间 →", fontsize=12)
ax1.set_ylabel("每股价格 / 每股价值（元，示意）", fontsize=12)
ax1.set_xlim(0, 122)
ax1.set_ylim(0, 60)
ax1.set_xticks([])
ax1.set_yticks([0, 10, 20, 30, 40, 50, 60])
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# ---------------------------------------------------------------- 右图：安全边际
ax2.axvspan(20, 40, color=C_BLUE, alpha=0.18, zorder=1)
ax2.vlines(15, 0, 3.4, color=C_GREEN, lw=3.2, zorder=3)
ax2.vlines(45, 0, 3.4, color=C_GRAY, lw=2.2, ls="--", zorder=3)

ax2.annotate("", xy=(20, 2.0), xytext=(15, 2.0),
             arrowprops=dict(arrowstyle="<->", color=C_RED, lw=2.0), zorder=4)
label(ax2, 17.5, 2.45, "安全边际 5 元\n（示意数字）", color=C_RED, fontsize=11.5)
label(ax2, 30, 3.05, "内在价值区间 20~40 元", color=C_BLUE, fontsize=12.5, weight="bold")
label(ax2, 13.6, 3.7, "买入价 15 元", color=C_GREEN, fontsize=12, ha="right")
label(ax2, 46.2, 3.7, "市场先生报价 45 元\n（比价值上限还高，太贵）",
      color=C_GRAY, fontsize=11, ha="left")

ax2.set_title("安全边际：买得比价值低，才有缓冲垫", fontsize=14, pad=12)
ax2.set_xlabel("每股价格（元，示意数字）", fontsize=12)
ax2.set_xlim(0, 54)
ax2.set_ylim(0, 4.4)
ax2.set_xticks([0, 15, 20, 30, 40, 45, 50])
ax2.set_yticks([])
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)

fig.tight_layout(w_pad=3.0)
save(fig, "w1d2_price_value.png")
