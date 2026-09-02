"""Week 9 / 第 1 章：市场先生情绪循环。

左侧：环形情绪轮（狂喜→不安→恐慌→绝望→平静→乐观→回到狂喜），中心是"每天来报价的市场先生"；
右侧："报价 vs 价值"对照卡（寓言的两个推论）。纯概念图，box/arrow/label。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import save, box, label, C_BLUE, C_RED, C_GREEN, C_ORANGE, C_GRAY, C_GOLD

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12.8, 7.0))
ax.set_xlim(0, 15.6)
ax.set_ylim(0, 10)
ax.axis("off")

# ------------------------------------------------------------------ 左侧：情绪轮
cx, cy, r = 4.5, 5.1, 2.75
BW, BH = 1.85, 0.92

# 顺时针：顶部狂喜 → 右上不安 → 右下恐慌 → 底部绝望 → 左下平静 → 左上乐观
moods = [
    ("狂喜",   90,  C_RED,    "#fdecea"),
    ("不安",   30,  C_GOLD,   "#fdf6e3"),
    ("恐慌",  -30,  C_ORANGE, "#fff0e0"),
    ("绝望",  -90,  C_GRAY,   "#eef0f2"),
    ("平静", -150,  C_BLUE,   "#e8f1fb"),
    ("乐观",  150,  C_GREEN,  "#e7f5ea"),
]

centers = []
for name, ang, ec, fc in moods:
    a = np.deg2rad(ang)
    x = cx + r * np.cos(a)
    y = cy + r * np.sin(a)
    centers.append((name, ang, ec, fc, x, y))
    box(ax, x - BW / 2, y - BH / 2, BW, BH, name, fc=fc, ec=ec,
        fontsize=13, weight="bold", tc="#333333")

# 沿圆弧连接相邻情绪（箭头画在两个方框之间的弧线上，不压字）
for i in range(len(centers)):
    name, ang, ec, fc, x, y = centers[i]
    nxt = centers[(i + 1) % len(centers)]
    a_from = np.deg2rad(ang - 19)
    a_to = np.deg2rad(nxt[1] + 19)
    p_from = (cx + r * np.cos(a_from), cy + r * np.sin(a_from))
    p_to = (cx + r * np.cos(a_to), cy + r * np.sin(a_to))
    ax.annotate(
        "", xy=p_to, xytext=p_from,
        arrowprops=dict(arrowstyle="-|>", color=C_GRAY, lw=1.7,
                        connectionstyle="arc3,rad=-0.28",
                        shrinkA=2, shrinkB=2, mutation_scale=15),
        zorder=1,
    )

# 中心：市场先生本人
box(ax, cx - 1.55, cy - 0.78, 3.1, 1.56,
    "市场先生\n每天来敲门，报一个价", fc="#ffffff", ec=C_BLUE, fontsize=12.5, weight="bold")

label(ax, cx, cy + 4.35, "他的情绪循环（一圈一圈转下去）", fontsize=12.5, color="#333333")

# ------------------------------------------------------------------ 右侧：报价 vs 价值对照卡
label(ax, 12.35, 9.45, "报价 vs 价值：别把两者混在一起", fontsize=13.5, weight="bold")

box(ax, 9.6, 6.35, 5.5, 2.05,
    "他兴高采烈、报出高价时\n公司还是那家公司\n→ 别跟着他一起高兴",
    fc="#fdf2f2", ec=C_RED, fontsize=11.5)
box(ax, 9.6, 3.75, 5.5, 2.05,
    "他垂头丧气、报出低价时\n公司还是那家公司\n→ 想想是不是你的机会",
    fc="#f0f7f1", ec=C_GREEN, fontsize=11.5)
box(ax, 9.6, 1.15, 5.5, 2.05,
    "他的报价是给你的服务\n不是给你的命令\n（寓言的两个推论）",
    fc="#f4f6fb", ec=C_BLUE, fontsize=11.5)

save(fig, "w9d2_mr_market.png")
