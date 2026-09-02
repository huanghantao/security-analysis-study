"""Week 7 第 3 章配图：杠杆双刃剑——无债 vs 高债，好年景/坏年景的 ROE 对比。

教学设计（手算与正文一致，全部示意数字，忽略所得税）：
甲公司（无债）：总资产 1000 万 = 股东权益 1000 万，无借款。
乙公司（高债）：总资产 1000 万 = 借款 800 万（年利率 6%，利息 48 万/年）+ 股东权益 200 万。
总资产息前回报（EBIT）：好年景 100 万（10%），坏年景 30 万（3%）。
ROE：甲好 = 100/1000 = 10%；乙好 = (100-48)/200 = 26%；
     甲坏 = 30/1000 = 3%； 乙坏 = (30-48)/200 = -9%。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, label, C_BLUE, C_ORANGE, C_RED

import matplotlib.pyplot as plt

roe_a_good, roe_b_good = 10.0, 26.0
roe_a_bad, roe_b_bad = 3.0, -9.0

x = [0, 1]                      # 好年景 / 坏年景 两组
w = 0.3

fig, ax = plt.subplots(figsize=(11, 6.8))
ax.set_xlim(-0.55, 2.0)
ax.set_ylim(-16, 36)
ax.axhline(0, color="#888888", lw=1.2, zorder=2)

b1 = ax.bar([i - w / 2 for i in x], [roe_a_good, roe_a_bad], width=w,
            color=C_BLUE, label="甲公司（无债：权益 1000 万）", zorder=3)
b2 = ax.bar([i + w / 2 for i in x], [roe_b_good, roe_b_bad], width=w,
            color=C_ORANGE, label="乙公司（高债：借款 800 万 + 权益 200 万）", zorder=3)

vals = [roe_a_good, roe_a_bad, roe_b_good, roe_b_bad]
pos = [0 - w / 2, 1 - w / 2, 0 + w / 2, 1 + w / 2]
for p, v in zip(pos, vals):
    if v >= 0:
        ax.text(p, v + 0.8, f"{v:g}%", ha="center", va="bottom", fontsize=12.5,
                weight="bold", color="#333333", zorder=5)
    else:
        ax.text(p, v - 0.8, f"{v:g}%", ha="center", va="top", fontsize=12.5,
                weight="bold", color=C_RED, zorder=5)

# 说明框：左上放假设，右上放结论，互不重叠
ax.text(
    -0.5, 34.5,
    "假设（示意数字，忽略所得税）：两家总资产都是 1000 万；\n甲全用自有资金；乙借 800 万（年利率 6%，每年利息 = 800×6% = 48 万）+ 自有 200 万。\n好年景总资产息前回报 100 万（10%）；坏年景 30 万（3%）",
    fontsize=9.8, color="#444444", ha="left", va="top", linespacing=1.7,
    bbox=dict(boxstyle="round,pad=0.4", fc="#f4f4f4", ec="#999999", lw=1),
    zorder=6,
)
ax.text(
    1.02, 26.5,
    "杠杆放大一切：\n好年景乙的 ROE = 26% 完胜甲的 10%；\n坏年景乙 = -9%，比甲多亏 12 个点。\n乙的利息覆盖：好年景 100 ÷ 48 ≈ 2.1 倍，\n坏年景 30 ÷ 48 ≈ 0.6 倍（入不敷出）",
    fontsize=10.5, color="#333333", ha="left", va="top", linespacing=1.7,
    bbox=dict(boxstyle="round,pad=0.45", fc="#fdf3e7", ec=C_ORANGE, lw=1.2),
    zorder=6,
)

ax.set_xticks(x)
ax.set_xticklabels(["好年景（息前回报 10%）", "坏年景（息前回报 3%）"], fontsize=11.5)
ax.set_ylabel("净资产收益率 ROE（%）", fontsize=11)
ax.set_xlabel("（示意数字，教学用：非任何真实公司；乙公司 ROE =（息前利润 − 48 万利息）÷ 200 万）",
              fontsize=9.8)
ax.set_title("杠杆双刃剑：同样的生意，借钱多少决定 ROE 的放大与坠落（示意数字）",
             fontsize=13, pad=12)
ax.legend(loc="lower left", fontsize=10, framealpha=0.95)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

save(fig, "w7d4_leverage.png")
