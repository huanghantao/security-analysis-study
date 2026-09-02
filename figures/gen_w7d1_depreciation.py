"""Week 7 第 0 章配图：直线折旧——年限-账面净值阶梯下降折线。

教学设计（手算与正文一致）：一台咖啡机 5 万元，预计用 5 年，报废时不值钱。
直线折旧：每年计提 = 5 ÷ 5 = 1 万元；第 t 年末净值 = 5 − t×1。
"计提不足 = 利润虚增"用文字框表达，不画第二条线，避免线条交叉。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, label, C_BLUE, C_ORANGE

import matplotlib.pyplot as plt

years = [0, 1, 2, 3, 4, 5]
net = [5, 4, 3, 2, 1, 0]   # 第 t 年末净值 = 5 − t

fig, ax = plt.subplots(figsize=(11, 6.6))
ax.set_xlim(-0.35, 5.7)
ax.set_ylim(-0.7, 7.0)

# 直线折旧的阶梯线：一年之内净值不变，年末跳降 1 万
ax.step(years, net, where="post", color=C_BLUE, lw=2.8, zorder=4)
ax.plot(0, net[0], "o", color=C_BLUE, ms=6.5, zorder=5)
label(ax, 0, net[0] + 0.44, "5", color="#1f4e79", fontsize=11.5, weight="bold")
# 第 1-5 年末的数值放在每个"下台阶"左下方的空白格里，避免压住竖直降线
for t in range(1, 6):
    v = net[t]
    ax.plot(t, v, "o", color=C_BLUE, ms=6.5, zorder=5)
    ax.text(t - 0.3, v + 0.32, f"{v}", ha="right", va="bottom", fontsize=11.5,
            color="#1f4e79", weight="bold", zorder=5)

ax.axhline(0, color="#bbbbbb", lw=1, zorder=1)

# 顶部左：方法框，箭头垂直落到第一段横线上（落点上方无任何元素）
ax.annotate(
    "直线折旧：每年计提 = 5 万 ÷ 5 年 = 1 万",
    xy=(0.68, 5.1), xytext=(0.62, 6.15), fontsize=11.5, color="#1f4e79",
    ha="left", va="center",
    bbox=dict(boxstyle="round,pad=0.4", fc="#eef4fb", ec=C_BLUE, lw=1.2),
    arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.5,
                    connectionstyle="arc3,rad=0"),
    zorder=6,
)
# 顶部右：结论框（不画线、不带箭头）
ax.text(
    2.95, 6.6,
    "若每年只提 0.5 万：\n5 年少提 2.5 万，每年利润虚增 0.5 万",
    fontsize=10.8, color="#a05a00", ha="left", va="top", linespacing=1.7,
    bbox=dict(boxstyle="round,pad=0.45", fc="#fdf3e7", ec=C_ORANGE, lw=1.2),
    zorder=6,
)
# 中部：第 3 年末净值（文字块整体左移，与"1"的数字标签拉开距离）
label(ax, 2.2, 1.42, "第 3 年末净值 = 5 − 3×1 = 2 万", color="#333333",
      fontsize=10.5)
ax.annotate("", xy=(2.95, 1.9), xytext=(2.78, 1.66),
            arrowprops=dict(arrowstyle="-|>", color="#555555", lw=1.4), zorder=6)
# 下部：第 5 年末归零（低处空白带纯文字说明，不画箭头）
label(ax, 2.4, 0.42, "第 5 年末净值 = 5 − 5×1 = 0（机器\u201c老\u201d完了）",
      color="#333333", fontsize=10.5)

ax.set_xticks(years)
ax.set_xticklabels(["购入时", "第 1 年末", "第 2 年末", "第 3 年末", "第 4 年末", "第 5 年末"],
                   fontsize=10.5)
ax.set_ylabel("账面净值（万元）", fontsize=11)
ax.set_xlabel("（示意数字，教学用：咖啡机购入价 5 万元，预计使用 5 年，残值 0）",
              fontsize=10)
ax.set_title("直线折旧：账面净值随年份阶梯下降（手算与正文一致）",
             fontsize=13, pad=12)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

save(fig, "w7d1_depreciation.png")
