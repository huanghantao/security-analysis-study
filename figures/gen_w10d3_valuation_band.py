"""Week 10 第 2 章配图：福耀玻璃（示意数字）估值区间与安全边际判定带。"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, label, C_BLUE, C_RED, C_GREEN, C_GRAY, C_BROWN, C_GOLD

import matplotlib.pyplot as plt

# ---------- 示意数字（与第 2 章正文一致，全部为教学示意口径） ----------
ASSET_ANCHOR = 260    # 资产锚：账面净资产（示意）
PESS, NEUT, OPT = 390, 510, 585   # 悲观/中性/乐观三档（盈利能力锚 39 亿 × 10/13/15 倍）
FLOOR = PESS          # 保守下沿 = 悲观档
BUY_LINE = 330        # 买入判定线：保守下沿再打约 8.5 折
NOW = 1200            # 当前示意市值

fig, ax = plt.subplots(figsize=(12.6, 7.4))
ax.set_xlim(0, 1330)
ax.set_ylim(0, 10)
ax.axis("off")

Y0, Y1 = 1.1, 9.3     # 判定带的上下边
AX_Y = 1.1            # 横轴位置

# ---------- 四段判定带（先画色带，再画竖线） ----------
ax.fill_between([0, BUY_LINE], Y0, Y1, color=C_GREEN, alpha=0.16, zorder=1)
ax.fill_between([BUY_LINE, FLOOR], Y0, Y1, color=C_GOLD, alpha=0.18, zorder=1)
ax.fill_between([FLOOR, OPT], Y0, Y1, color=C_BLUE, alpha=0.13, zorder=1)
ax.fill_between([OPT, 1330], Y0, Y1, color=C_RED, alpha=0.09, zorder=1)

# ---------- 底部横轴 ----------
ax.plot([0, 1330], [AX_Y, AX_Y], color="#444444", lw=2.2, zorder=2)
label(ax, 300, 0.42, "市值（示意口径，单位：亿元）→", fontsize=11, color="#444444")

# ---------- 竖线：资产锚 / 买入判定线 / 三档价值 / 当前价格 ----------
for x, color, lw, ls in [
    (ASSET_ANCHOR, C_BROWN, 2.0, ":"),
    (BUY_LINE, C_GOLD, 2.2, "--"),
    (PESS, C_BLUE, 2.4, "--"),
    (NEUT, C_GRAY, 2.0, "--"),
    (OPT, C_GREEN, 2.0, "--"),
    (NOW, C_RED, 2.8, "-"),
]:
    ax.plot([x, x], [Y0, Y1], color=color, lw=lw, ls=ls, zorder=2)

# ---------- 标签：每个标签占一条独立的“高度层”，横向再错开，保证互不遮挡 ----------
# 高度层从上到下：8.5 / 6.8 / 5.3 / 3.9 / 2.4
label(ax, 165, 8.5, "① 买入判定区\n≤ 330 亿：安全边际充足\n到点按计划分批",
      fontsize=10.5, color="#1b6b2a")
label(ax, 360, 6.8, "② 边缘区：330~390 亿\n折扣不足，再等",
      fontsize=10.5, color="#8a6508")
label(ax, 487, 8.5, "③ 价值区间\n390~585 亿\n合理，但不便宜",
      fontsize=10.5, color="#17537d")
label(ax, 930, 8.5, "④ 区间之外\n> 585 亿：市场先生在讲增长故事\n不买，写进观察清单持续跟踪",
      fontsize=10.5, color="#9c2b2b")

label(ax, 330, 5.3, "买入判定线 330 亿\n（保守下沿再打约 8.5 折）",
      fontsize=10.5, color=C_GOLD)
label(ax, 245, 3.9, "资产锚 260 亿（安全网）", fontsize=10.5, color=C_BROWN)
label(ax, 510, 3.9, "中性档 510 亿", fontsize=10.5, color=C_GRAY)
label(ax, 390, 2.4, "悲观档 390 亿\n= 保守下沿", fontsize=10.5, color=C_BLUE)
label(ax, 585, 2.4, "乐观档 585 亿", fontsize=10.5, color=C_GREEN)
label(ax, 1200, 5.9, "当前示意市值\n约 1200 亿", fontsize=11, color=C_RED, weight="bold")

ax.set_title("福耀玻璃示意估值带：三档价值 → 保守下沿 → 当前价格的落点（全部为教学示意数字）",
             fontsize=13.5, pad=14, color="#222222")

save(fig, "w10d3_valuation_band.png")
