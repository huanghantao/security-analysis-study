"""Week 8 第 0 章配图：账面价值怎么算，以及它与市值、PB 的关系（概念图）。

左半幅：账面价值的计算链（总资产 − 无形 − 全部负债 = 账面价值，÷ 股本 = 每股净资产）；
右半幅：把市值和账面价值放在一起相除得到市净率 PB，以及 PB 三种水平的读法。
全部数字为教学示意数字。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    OUT, save, fig_ax, box, arrow, label,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_RED,
)

fig, ax = fig_ax(13, 9)

label(ax, 5.0, 9.55, "同一家公司，两种标价：账面价值 与 市值",
      fontsize=15.5, weight="bold")

# ---------- 左：账面价值怎么算 ----------
box(ax, 0.25, 1.5, 4.5, 7.35, "", fc="#f2f7fd", ec=C_BLUE, lw=1.2)
label(ax, 2.5, 8.45, "账面价值（book value）怎么算",
      color=C_BLUE, fontsize=13, weight="bold")

box(ax, 0.5, 7.3, 1.95, 0.8, "流动资产 7 亿\n（现金+应收+存货）",
    fc="white", ec=C_BLUE, fontsize=9.5)
box(ax, 2.55, 7.3, 1.95, 0.8, "非流动资产 5 亿\n（厂房 4 + 无形 1）",
    fc="white", ec=C_BLUE, fontsize=9.5)

box(ax, 0.5, 6.1, 4.0, 0.8, "减：全部负债 4 亿\n（流动 1.5 + 长期 2.5，足额扣）",
    fc="white", ec=C_GRAY, fontsize=9.5)

box(ax, 0.5, 4.9, 4.0, 0.9,
    "= 有形净资产（账面价值）7 亿\n总资产 12 − 无形 1 − 负债 4",
    fc="#e9f5ea", ec=C_GREEN, fontsize=10.5, weight="bold")

arrow(ax, (2.5, 4.85), (2.5, 4.4), color=C_GRAY)
label(ax, 3.55, 4.63, "÷ 总股本 2 亿股", fontsize=10, color=C_GRAY)

box(ax, 0.5, 3.55, 4.0, 0.8, "每股净资产 = 7 ÷ 2 = 3.5 元/股",
    fc="white", ec=C_BLUE, fontsize=11, weight="bold")

label(ax, 2.5, 2.95, "注：账面价值通常指有形口径——\n有商誉、品牌等无形资产时先剔除（本例 1 亿）",
      fontsize=9.5, color=C_GRAY)

box(ax, 0.6, 1.85, 3.8, 0.8,
    "直觉：这是家底的“账本价”，\n不问生意赚不赚钱",
    fc="white", ec=C_GRAY, fontsize=9.5, tc="#555555")

# ---------- 右：市净率 PB ----------
box(ax, 5.25, 1.5, 4.5, 7.35, "", fc="#fdf6ec", ec=C_ORANGE, lw=1.2)
label(ax, 7.5, 8.45, "市净率 PB：把两种标价放一起",
      color=C_ORANGE, fontsize=13, weight="bold")

box(ax, 5.55, 7.3, 3.9, 0.8, "市值 = 股价 × 总股本\n1.2 元 × 2 亿股 = 2.4 亿（示意）",
    fc="white", ec=C_ORANGE, fontsize=10)
arrow(ax, (7.5, 7.25), (7.5, 6.98), color=C_GRAY)
label(ax, 7.95, 7.11, "÷", fontsize=14, color=C_GRAY)

box(ax, 5.55, 6.1, 3.9, 0.8, "账面价值 7 亿\n（每股净资产 3.5 元）",
    fc="white", ec=C_BLUE, fontsize=10)
arrow(ax, (7.5, 6.05), (7.5, 5.65), color=C_GRAY)

box(ax, 5.55, 4.75, 3.9, 0.9, "PB = 市值 2.4 ÷ 账面 7 ≈ 0.34\n股价只有账面家底的 1/3 → 破净",
    fc="white", ec=C_RED, tc=C_RED, fontsize=10.5, weight="bold")

box(ax, 5.55, 3.5, 3.9, 0.68, "PB > 1：市场在为盈利能力付溢价",
    fc="white", ec=C_GRAY, fontsize=10, tc="#444444")
box(ax, 5.55, 2.62, 3.9, 0.68, "PB ≈ 1：市场只按家底出价",
    fc="white", ec=C_GRAY, fontsize=10, tc="#444444")
box(ax, 5.55, 1.74, 3.9, 0.68, "PB < 1：市场怀疑家底注水 / 盈利变差",
    fc="white", ec=C_RED, fontsize=10, tc=C_RED)

label(ax, 5.0, 0.85, "本周任务：把“破净”的折扣拆开看——哪些是真便宜，哪些是假便宜",
      fontsize=12, weight="bold", color="#444444")

save(fig, "w8d1_book_value.png")
