"""Week 3 第 3 章配图：利息保障倍数（利润是利息的几倍）。

三家用示意数字的公司：甲 8 倍 / 乙 3 倍 / 丙 1.2 倍。
两条参考线：
  - 2 倍：格雷厄姆在本书正文提议的最低线（原书第 154 页脚注：平均盈利须达固定费用约 2 倍）；
  - 7 倍：更严的工业债参考线（格雷厄姆与梅雷迪思《财务报表解读》，1937，给工业债券的常用建议值）。
"""
import sys, pathlib

import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, C_BLUE, C_GREEN, C_GOLD, C_GRAY

fig, ax = plt.subplots(figsize=(10.5, 6))

names = [
    "丙公司（示意）\n利润 6 万 ÷ 利息 5 万",
    "乙公司（示意）\n利润 15 万 ÷ 利息 5 万",
    "甲公司（示意）\n利润 40 万 ÷ 利息 5 万",
]
ratios = [1.2, 3.0, 8.0]
colors = ["#d62728", "#1f77b4", "#2ca02c"]

bars = ax.barh([0, 1, 2], ratios, height=0.55, color=colors, alpha=0.85, zorder=2)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(names, fontsize=11)
ax.set_xlim(0, 9.8)
ax.set_ylim(-0.55, 4.15)
ax.set_xlabel("利息保障倍数 = 可用于付息的利润 ÷ 利息费用", fontsize=12)
ax.set_title("利息保障倍数：利润是利息的几倍？（示意数字）", fontsize=14.5, pad=14)
ax.grid(axis="x", ls=":", color="#cccccc", zorder=0)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="x", labelsize=11)

# 每根条末端的倍数标签
for y, r, c in zip([0, 1, 2], ratios, colors):
    ax.text(r + 0.15, y, f"{r:g} 倍", va="center", ha="left",
            fontsize=12.5, weight="bold", color=c)

# 参考线 1：格雷厄姆最低线 2 倍
ax.axvline(2, color=C_GRAY, ls="--", lw=1.8, zorder=3)
ax.text(2, 3.32, "最低线：2 倍\n（格雷厄姆在本书正文提议：\n平均盈利 ≥ 2 × 固定费用）",
        ha="center", va="bottom", fontsize=10.5, color="#444444",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_GRAY, lw=0.8))

# 参考线 2：更严的工业债参考线 7 倍
ax.axvline(7, color=C_GOLD, ls="--", lw=1.8, zorder=3)
ax.text(7, 3.32, "更严参考线：7 倍\n（工业债的常用建议值，\n格雷厄姆-梅雷迪思 1937）",
        ha="center", va="bottom", fontsize=10.5, color="#7a5c08",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_GOLD, lw=0.8))

fig.subplots_adjust(left=0.22, right=0.97, top=0.88, bottom=0.12)
save(fig, "w3d4_coverage.png")
