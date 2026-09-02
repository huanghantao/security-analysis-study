"""Week 9 / 第 0 章：价格钟摆——围绕价值的过度摆动。

价值是水平区间（20~40 元，示意），价格像钟摆一样围绕它过度摆动：
顶上标"贪婪的顶：夸大未来"，底下标"恐惧的底：忽视当下"（对应 ch50 的两大根源）。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, C_BLUE, C_RED, C_GREEN

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(13.2, 6.6))

t = np.linspace(0, 120, 900)
price = 30 + 16.5 * np.sin(t / 8.2 + 0.55) + 4.5 * np.sin(t / 3.05 + 1.4)

# 价值区间带 + 中枢
ax.axhspan(20, 40, color=C_BLUE, alpha=0.14, zorder=1, label="内在价值区间 20~40 元（示意）")
ax.axhline(30, color=C_BLUE, lw=1.2, ls=":", zorder=2, label="价值中枢 30 元")

# 越界区域的淡色填充：上方透支、下方捡货
ax.fill_between(t, 40, price, where=price > 40, color=C_RED, alpha=0.10, zorder=1.5,
                label="涨过头的部分（透支未来）")
ax.fill_between(t, price, 20, where=price < 20, color=C_GREEN, alpha=0.12, zorder=1.5,
                label="跌破价值的部分（安全边际出现）")

ax.plot(t, price, color=C_RED, lw=2.2, zorder=3, label="市场价（他的报价）")

# 找极值点做标注
i_high = int(np.argmax(price))
i_low = int(np.argmin(price))
x_high, y_high = t[i_high], price[i_high]
# 取后半段里最低的点做"恐惧的底"，避免与左端起手位置贴太近
mask = t > 30
i_low2 = int(np.argmin(np.where(mask, price, 999)))
x_low, y_low = t[i_low2], price[i_low2]

ax.annotate("贪婪的顶：夸大未来\n（Week 5 的『新时代』剧本）",
            xy=(x_high, y_high), xytext=(x_high - 26, y_high + 2.5),
            fontsize=12, color=C_RED, ha="center", va="bottom",
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=C_RED, lw=1.3),
            arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.6), zorder=5)
ax.annotate("恐惧的底：忽视当下\n（好公司被当成破烂卖）",
            xy=(x_low, y_low), xytext=(x_low + 21, y_low - 3.5),
            fontsize=12, color=C_GREEN, ha="center", va="top",
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=C_GREEN, lw=1.3),
            arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1.6), zorder=5)

ax.set_title("价格钟摆：围绕价值的过度摆动（数字为示意）", fontsize=15, pad=12)
ax.set_xlabel("时间", fontsize=12)
ax.set_ylabel("每股价格 / 每股价值（元，示意）", fontsize=12)
ax.set_xlim(0, 120)
ax.set_ylim(0, 60)
ax.set_xticks([])
ax.set_yticks([0, 10, 20, 30, 40, 50, 60])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# 图例放在图外下方，保证不与曲线打架
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3,
          fontsize=10.5, frameon=False)

fig.tight_layout()
save(fig, "w9d1_pendulum.png")
