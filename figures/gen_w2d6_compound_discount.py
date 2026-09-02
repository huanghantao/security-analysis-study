"""Week 2 - 05 章：复利与贴现双面板图。

左：1 万元按 10% 复利滚 30 年；右：贴现直觉——两年后的 121 万，10% 利率下今天只值 100 万。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, C_BLUE, C_ORANGE, C_RED, C_GRAY, C_GREEN

import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.6))

# ================= 左面板：复利 =================
ax = axes[0]
years = list(range(0, 31))
values = [1.0 * (1.10 ** t) for t in years]
ax.plot(years, values, color=C_BLUE, lw=2.4, zorder=3)

# 72 法则：10% 大约 7.2 年翻一倍（1.1^7.2 约等于 2）
ax.plot([7.2], [1.10 ** 7.2], "o", color=C_GREEN, ms=8, zorder=4)
ax.plot([0, 7.2], [2, 2], color=C_GRAY, lw=1.0, ls="--", zorder=2)
ax.plot([7.2, 7.2], [0, 2], color=C_GRAY, lw=1.0, ls="--", zorder=2)
ax.annotate("约 7.2 年翻一倍\n（72 法则：72 除以 10）",
            xy=(7.2, 2.0), xytext=(10.5, 1.15),
            fontsize=11, color="#2a6a2a", ha="center", va="center",
            linespacing=1.6, zorder=5,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="none", alpha=0.95),
            arrowprops=dict(arrowstyle="-|>", color=C_GREEN, lw=1.6))

# 30 年终点
end_y = 1.10 ** 30
ax.plot([30], [end_y], "o", color=C_RED, ms=8, zorder=4)
ax.annotate("30 年后约 17.4 万元\n1 万变 17 倍多",
            xy=(30, end_y), xytext=(20.5, 15.4),
            fontsize=11, color="#8a1a1a", ha="center", va="center",
            linespacing=1.6, zorder=5,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="none", alpha=0.95),
            arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.6))

ax.set_title("复利：1 万元按 10% 往前滚", fontsize=13, pad=10)
ax.set_xlabel("年数 t", fontsize=11.5)
ax.set_ylabel("金额（万元）", fontsize=11.5)
ax.set_xlim(0, 31.5)
ax.set_ylim(0, 19)
ax.grid(alpha=0.28)

# ================= 右面板：贴现 =================
ax = axes[1]
ts = [i / 20 for i in range(41)]
vs = [100 * (1.10 ** t) for t in ts]
ax.plot(ts, vs, color=C_ORANGE, lw=2.4, zorder=3)

# 三个锚点：今天 100、1 年后 110、2 年后 121
for t, v in [(0, 100), (1, 110), (2, 121)]:
    ax.plot([t], [v], "o", color=C_ORANGE, ms=8, zorder=4)
ax.text(1.06, 106.6, "110（1 年后）", fontsize=11, color="#7a4a10",
        ha="left", va="center", zorder=5,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.95))
ax.text(0.06, 96.9, "100（今天）", fontsize=11, color="#7a4a10",
        ha="left", va="center", zorder=5,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.95))

# 贴现两步算（放在曲线上方的空白区）
ax.text(0.72, 116.8,
        "折现两步算：\n121 ÷ 1.1 = 110（折回 1 年）\n110 ÷ 1.1 = 100（折回今天）",
        fontsize=11, color="#8a1a1a", ha="center", va="center",
        linespacing=1.7, zorder=5,
        bbox=dict(boxstyle="round,pad=0.4", fc="#fdf0ee", ec="#d62728", lw=1.2))
ax.annotate("",
            xy=(1.95, 120.6), xytext=(1.34, 118.2),
            arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.8))

ax.set_title("贴现：未来的钱往回折（10% 利率）", fontsize=13, pad=10)
ax.set_xlabel("年数 t", fontsize=11.5)
ax.set_ylabel("金额（万元）", fontsize=11.5)
ax.set_xticks([0, 0.5, 1, 1.5, 2])
ax.set_xlim(-0.15, 2.45)
ax.set_ylim(90, 127.5)
ax.grid(alpha=0.28)

fig.tight_layout()
save(fig, "w2d6_compound_discount.png")
