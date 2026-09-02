"""Week 1 / 第 4 章：证券家族树 + 求偿顺序金字塔。

左图：按"法律身份"给证券分家——债主还是股东；
右图：公司散伙清算时，钱按什么顺序分给谁（求偿顺序金字塔）。
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import save, fig_multi, box, arrow, label, C_BLUE, C_ORANGE, C_GREEN, C_RED, C_GRAY, C_PURPLE

fig, axes = fig_multi(1, 2, width=14.5, height=7.2)
ax1, ax2 = axes
for ax in (ax1, ax2):  # fig_multi 不自动设 0~10 坐标范围，这里显式设置
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

# ---------------------------------------------------------------- 左图：证券家族树
ax1.set_title("① 证券家族树：一张纸，两种法律身份", fontsize=14, pad=14)

box(ax1, 3.1, 8.6, 3.8, 1.05, "证券（Security）\n代表某种权利的一张纸",
    fc="#fdf6e3", ec=C_PURPLE, fontsize=12, weight="bold")

box(ax1, 0.5, 6.3, 3.6, 1.1, "债券（Bond）\n你是债主：收固定利息",
    fc="#eef4fb", ec=C_BLUE, fontsize=11.5)
box(ax1, 5.9, 6.3, 3.6, 1.1, "股票（Stock）\n你是股东：分剩下的利润",
    fc="#fff2e8", ec=C_ORANGE, fontsize=11.5)

box(ax1, 5.0, 4.1, 2.6, 1.05, "优先股\n（Preferred）", fc="#fff2e8", ec=C_ORANGE, fontsize=11)
box(ax1, 8.0, 4.1, 2.0, 1.05, "普通股\n（Common）", fc="#fff2e8", ec=C_ORANGE, fontsize=11)

box(ax1, 1.9, 1.05, 6.2, 1.75,
    "混血儿：借条 + 换股权（Week 4 详谈）\n可转债（Convertible Bond）\n认股权证（Warrant）",
    fc="#eaf6ec", ec=C_GREEN, fontsize=10.5)

arrow(ax1, (5.0, 8.6), (2.3, 7.4), color=C_GRAY)
arrow(ax1, (5.0, 8.6), (7.7, 7.4), color=C_GRAY)
arrow(ax1, (7.7, 6.3), (6.3, 5.15), color=C_GRAY)
arrow(ax1, (7.7, 6.3), (9.0, 5.15), color=C_GRAY)
arrow(ax1, (2.3, 6.3), (4.0, 2.8), color=C_GREEN, ls="--")
arrow(ax1, (6.3, 4.1), (5.6, 2.8), color=C_GREEN, ls="--")

label(ax1, 5.0, 0.45, "先记大方向：买债券 = 借钱给人；买股票 = 成为公司的部分主人",
      color="#444444", fontsize=11.5)

# ---------------------------------------------------------------- 右图：求偿顺序金字塔
ax2.set_title("② 求偿顺序金字塔：公司散伙时，谁先拿钱？", fontsize=14, pad=14)

box(ax2, 3.0, 7.4, 4.0, 1.5, "第 1 顺位：债券持有人\n借出去的本金和利息\n最先拿，最有保障",
    fc="#eef4fb", ec=C_BLUE, fontsize=11.5)
box(ax2, 2.4, 5.2, 5.2, 1.5, "第 2 顺位：优先股股东\n有约定的股息，\n排在普通股前面",
    fc="#fff2e8", ec=C_ORANGE, fontsize=11.5)
box(ax2, 1.8, 3.0, 6.4, 1.5, "第 3 顺位：普通股股东\n分完剩下的才归你：\n风险最大，收益上限也最高",
    fc="#fdeaea", ec=C_RED, fontsize=11.5)

# 右侧向下的大箭头 + 左侧说明
arrow(ax2, (9.55, 8.4), (9.55, 3.3), color=C_GRAY, lw=2.4)
label(ax2, 0.25, 5.95, "清算分配\n从上往下\n依次进行", color="#444444",
      fontsize=11.5, ha="left")

label(ax2, 5.0, 1.55, "越靠上越安全，越靠下越有想象空间——这就是 Part II 先讲债券的原因",
      color="#444444", fontsize=11.5)

save(fig, "w1d5_security_map.png")
