"""Week 9 / 第 3 章：安全边际三段图——债券版 vs 股票版。

左（股票版）：0→15 买入价、15→20 安全边际、20→40 价值区间（示意数字，与 Week 1 呼应）；
右（债券版）：利息 1 元 vs 可付息利润 7 元，保障倍数 7 倍（Week 3 的形态）。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import save, box, label, C_BLUE, C_RED, C_GREEN, C_GRAY, C_BROWN

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.8, 5.9))

# ------------------------------------------------------------------ 左：股票版
Y0, YH = 3.9, 2.0  # 主条的底边与高度
ax1.add_patch(mpatches.Rectangle((0, Y0), 15, YH, fc="#dff0e5", ec=C_GREEN, lw=2.0, zorder=2))
ax1.add_patch(mpatches.Rectangle((15, Y0), 5, YH, fc="#fdeaea", ec=C_RED, lw=2.0, zorder=2))
ax1.add_patch(mpatches.Rectangle((20, Y0), 20, YH, fc="#e8f1fb", ec=C_BLUE, lw=2.0, zorder=2))

ax1.text(7.5, Y0 + YH / 2, "买入价 15 元", ha="center", va="center", fontsize=12.5,
         color="#1b5e38", weight="bold", zorder=4)
ax1.text(17.5, Y0 + YH + 1.0, "安全边际\n5 元", ha="center", va="bottom", fontsize=11.5,
         color=C_RED, weight="bold", linespacing=1.4, zorder=4)
ax1.text(30, Y0 + YH / 2, "价值区间 20~40 元\n（价值是一段，不是一个点）", ha="center",
         va="center", fontsize=11.5, color="#1a4d80", linespacing=1.5, zorder=4)

# 上方标注：价值区间本身不精确
ax1.annotate("", xy=(40, 9.2), xytext=(20, 9.2),
             arrowprops=dict(arrowstyle="<->", color=C_BLUE, lw=1.8), zorder=3)
label(ax1, 30, 9.75, "价值本身就不精确，所以只敢用保守的下沿", color=C_BLUE, fontsize=11)

# 下方标注：安全边际是两段距离的差
ax1.annotate("", xy=(20, 2.4), xytext=(15, 2.4),
             arrowprops=dict(arrowstyle="<->", color=C_RED, lw=1.8), zorder=3)
label(ax1, 17.5, 1.55, "下沿与买入价的差\n= 你的容错空间", color=C_RED, fontsize=11)

ax1.set_title("股票版：安全边际 = 买入价到价值下沿的距离（元，示意）", fontsize=13.5, pad=30)
ax1.set_xlabel("每股价格（元，示意数字）", fontsize=12)
ax1.set_xlim(0, 46)
ax1.set_ylim(0, 11)
ax1.set_xticks([0, 15, 20, 40])
ax1.set_xticklabels(["0", "15\n买入价", "20\n保守下沿", "40\n乐观上沿"])
ax1.set_yticks([])
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)

# ------------------------------------------------------------------ 右：债券版
ax2.axis("off")
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)

# 利润长条（7 元）与利息短条（1 元），长度按 0.82/元 缩放
ax2.add_patch(mpatches.Rectangle((1.0, 2.6), 5.74, 1.15, fc="#e8f1fb", ec=C_BLUE,
                                 lw=1.8, zorder=2))
ax2.text(1.2, 3.17, "可用于付息的利润 7 元", ha="left", va="center", fontsize=11.5,
         color="#1a4d80", zorder=4)
ax2.add_patch(mpatches.Rectangle((1.0, 5.9), 0.82, 1.15, fc="#f5e9d8", ec=C_BROWN,
                                 lw=1.8, zorder=2))
ax2.text(1.2, 7.4, "每年必须付的利息 1 元", ha="left", va="center", fontsize=11.5,
         color="#5d3a26", zorder=4)

# 倍数标注（虚线把利息水平引到箭头顶端，让"距离"有参照）
ax2.plot([1.82, 7.35], [6.47, 6.47], ls="--", lw=1.2, color=C_BROWN, alpha=0.8, zorder=1)
ax2.plot([6.74, 7.35], [3.17, 3.17], ls="--", lw=1.2, color=C_BLUE, alpha=0.8, zorder=1)
ax2.annotate("", xy=(7.35, 3.17), xytext=(7.35, 6.47),
             arrowprops=dict(arrowstyle="<->", color=C_GRAY, lw=1.6), zorder=3)
label(ax2, 8.55, 4.8, "利润是利息的\n7 倍\n（保障倍数）", color="#444444", fontsize=11)

box(ax2, 1.0, 0.35, 8.3, 1.35,
    "利润就算跌掉七分之六，利息照样付得起\n——这就是债券版的安全边际（Week 3 的老朋友）",
    fc="#f4f6f8", ec=C_GRAY, fontsize=11)

ax2.set_title("债券版：安全边际 = 保障倍数（倍数感）", fontsize=13.5, pad=12)
ax2.text(1.0, 8.6, "同一家公司：借条看『能不能一直付利息』，股票看『买得够不够便宜』",
         ha="left", va="center", fontsize=11, color="#555555")

fig.tight_layout(w_pad=2.6)
save(fig, "w9d4_margin.png")
