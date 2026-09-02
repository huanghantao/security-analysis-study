"""Week 7 第 2 章配图：市盈率的两把尺——同一股价、不同盈利口径下的 PE 对比。

教学设计（与 w7d2_avg_earnings.png 同一个示意案例）：
股价都是 40 元；EPS 分别取谷底年 0.6 元 / 10 年平均 2.0 元 / 顶部年 4.0 元，
对应 PE = 66.7 倍 / 20 倍 / 10 倍。
周期股的悖论：越在景气顶部，PE 看起来越"便宜"。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, label, C_BLUE, C_GREEN, C_ORANGE, C_RED

import matplotlib.pyplot as plt

cases = ["谷底年\nEPS 0.6 元", "10 年平均\nEPS 2.0 元", "顶部年\nEPS 4.0 元"]
pe = [66.7, 20.0, 10.0]
colors = [C_RED, C_GREEN, C_ORANGE]

fig, ax = plt.subplots(figsize=(10.5, 6.8))
ax.set_xlim(-0.6, 2.6)
ax.set_ylim(0, 82)

bars = ax.bar([0, 1, 2], pe, width=0.52, color=colors, zorder=3)

denoms = ["0.6", "2.0", "4.0"]
for x, v, d in zip([0, 1, 2], pe, denoms):
    ax.text(x, v + 1.6, f"{v} 倍", ha="center", va="bottom", fontsize=13,
            weight="bold", color="#333333", zorder=5)
    # 柱内标算式
    ax.text(x, v / 2, f"40 ÷ {d}", ha="center", va="center", fontsize=10.5,
            color="white", weight="bold", zorder=5)

ax.axhline(0, color="#999999", lw=1)

# 两个说明框放在两侧上部空白处
ax.text(
    -0.42, 79,
    "同一只股票、同一时刻，股价都是 40 元：\nPE = 股价 ÷ EPS",
    fontsize=11.2, color="#1f4e79", ha="left", va="top", linespacing=1.6,
    bbox=dict(boxstyle="round,pad=0.45", fc="#eef4fb", ec=C_BLUE, lw=1.2),
    zorder=6,
)
ax.text(
    0.52, 62,
    "周期股悖论：\n景气顶部 → EPS 高 → PE 最低（看似\u201c便宜\u201d）\n景气谷底 → EPS 低 → PE 最高（看似\u201c最贵\u201d）\n把尺子倒过来读，正好买错方向",
    fontsize=10.8, color="#333333", ha="left", va="top", linespacing=1.7,
    bbox=dict(boxstyle="round,pad=0.45", fc="#fdf3e7", ec=C_ORANGE, lw=1.2),
    zorder=6,
)

ax.set_xticks([0, 1, 2])
ax.set_xticklabels(cases, fontsize=11)
ax.set_ylabel("市盈率（倍）", fontsize=11)
ax.set_xlabel("（示意数字，教学用：与 w7d2_avg_earnings.png 同一个案例，股价统一按 40 元）",
              fontsize=10)
ax.set_title("市盈率的两把尺：用哪一年的盈利当分母，结论天差地别（示意数字）",
             fontsize=13, pad=12)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

save(fig, "w7d3_pe.png")
