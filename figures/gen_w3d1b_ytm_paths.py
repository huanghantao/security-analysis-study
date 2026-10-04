"""Week 3 第 0 章配图（0.4 节）：同样赚 25 元，两种拿钱方式的差别。

左：两张借条的"累计到手现金"。A（面值 100、票息 5 元）每年到手 5 元，一路有进账；
    B（面值 125、零票息）前四年一分没有，第 5 年一次拿到 125 元。终点都是 125 元。
右：两张借条的"基数路径"（每年年初在岗的本金）。A 生 5 发 5，基数平在 100；
    B 生出来的息全部留下，基数从 100 一路爬到 125。平均基数不同（100 对 109.55），
    这就是两者 YTM 不同（5.0000% 对 4.5640%）的原因。

正文（learning-guide/week3/00-债券是什么-一张放大了的借条.md 第 0.4 节）与此图数字一致。
"""
import sys, pathlib

import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import save, label, C_BLUE, C_ORANGE, C_GRAY

fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.4))
years = [0, 1, 2, 3, 4, 5]

# ---------------- 左：累计到手现金 ----------------
ax = axes[0]
cum_a = [0, 5, 10, 15, 20, 125]
cum_b = [0, 0, 0, 0, 0, 125]
ax.plot(years, cum_a, marker="o", ms=7, lw=2.4, color=C_BLUE, zorder=3,
        label="借条 A：面值 100、每年票息 5 元")
ax.plot(years, cum_b, marker="s", ms=7, lw=2.4, color=C_ORANGE, zorder=3,
        label="借条 B：面值 125、零票息")
ax.set_xlim(-0.35, 5.75)
ax.set_ylim(-8, 152)
ax.set_xticks(years)
ax.set_xlabel("年", fontsize=11)
ax.set_ylabel("累计到手的现金（元）", fontsize=11)
ax.set_title("累计到手现金：终点都是 125 元，路径不同", fontsize=12.5, pad=10)
ax.grid(ls=":", color="#cccccc", zorder=0)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(fontsize=10, loc="upper left", framealpha=0.95)
label(ax, 1.0, 26, "A 第 1 年就有 5 元到手\n（早到手的钱能再生钱）",
      color=C_BLUE, fontsize=10.5, ha="left")
label(ax, 2.0, 78, "B 前四年一分没有\n25 元全堆在第 5 年",
      color=C_ORANGE, fontsize=10.5, ha="center")

# ---------------- 右：基数路径 ----------------
ax = axes[1]
base_a = [100, 100, 100, 100, 100, 100]
base_b = [100, 104.564, 109.336, 114.326, 119.544, 125]
ax.plot(years, base_a, marker="o", ms=6, lw=2.4, ls="--", color=C_BLUE, zorder=3,
        label="借条 A 的基数：生 5、发 5、剩 0")
ax.plot(years, base_b, marker="s", ms=7, lw=2.6, color=C_ORANGE, zorder=3,
        label="借条 B 的基数：生息全留下")
ax.fill_between(years, base_a, base_b, color=C_ORANGE, alpha=0.10, zorder=1)
ax.axhline(100, color=C_GRAY, lw=1.0, ls=":", zorder=1)
ax.set_xlim(-0.35, 6.35)
ax.set_ylim(92, 134)
ax.set_xticks(years)
ax.set_xlabel("年", fontsize=11)
ax.set_ylabel("当年在岗的本金（基数，元）", fontsize=11)
ax.set_title("基数路径：A 停在 100，B 一路爬到面值 125", fontsize=12.5, pad=10)
ax.grid(ls=":", color="#cccccc", zorder=0)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(fontsize=10, loc="upper left", framealpha=0.95)
label(ax, 2.5, 96.6, "A 的基数平在 100，平均基数 = 100 = 买入价",
      color=C_BLUE, fontsize=10.5)
label(ax, 5.6, 128.6, "B 的平均基数 109.55\n大于买入价 100",
      color=C_ORANGE, fontsize=10.5, ha="right")
label(ax, 5.6, 118.0, "被迫复利的部分", color=C_ORANGE, fontsize=10, ha="right")

fig.subplots_adjust(wspace=0.26)
save(fig, "w3d1b_ytm_paths.png")
