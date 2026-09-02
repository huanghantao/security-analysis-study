"""Week 3 第 0 章配图：一张 5 年期借条的时间线现金流。

0 期借出 100 元，第 1~4 年每年收 5 元票息，第 5 年收 105 元（本金 + 利息）。
正文（learning-guide/week3/00-债券是什么-一张放大了的借条.md）与此图数字一致。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, fig_ax, box, arrow, label, C_BLUE, C_RED, C_GREEN, C_GRAY

fig, ax = fig_ax(width=11, height=5.8)

# ---------- 时间轴 ----------
ax_years = [1.0, 2.4, 3.8, 5.2, 6.6, 8.0]  # 第 0~5 年
arrow(ax, (0.55, 4.2), (9.35, 4.2), color=C_GRAY, lw=2.2)
for i, x in enumerate(ax_years):
    ax.plot([x], [4.2], marker="o", ms=7, color=C_BLUE, zorder=5)
    label(ax, x, 3.62, f"第 {i} 年", fontsize=11, color="#333333")

# ---------- 第 0 年：借出 100 元（向下箭头，左上方框） ----------
arrow(ax, (1.0, 6.6), (1.0, 4.45), color=C_RED, lw=2.2)
label(ax, 1.52, 5.35, "−100 元", fontsize=11.5, color=C_RED, ha="left")
box(ax, 0.05, 6.75, 2.35, 1.15,
    "第 0 年：借出 100 元\n（本金离开你）",
    fc="#fdecec", ec=C_RED, fontsize=11, weight="bold")

# ---------- 第 1~4 年：每年收 5 元票息（向上箭头，中上方框） ----------
for x in ax_years[1:5]:
    arrow(ax, (x, 4.4), (x, 5.6), color=C_GREEN, lw=2.2)
    label(ax, x, 5.98, "+5 元", fontsize=11.5, color=C_GREEN)
box(ax, 3.1, 6.75, 2.9, 1.15,
    "第 1~4 年：每年收 5 元\n（票面利率 5%）",
    fc="#eaf6ea", ec=C_GREEN, fontsize=11, weight="bold")

# ---------- 第 5 年：收 105 元（更高的向上箭头 + 右上方框） ----------
arrow(ax, (8.0, 4.4), (8.0, 6.55), color=C_GREEN, lw=2.4)
box(ax, 6.55, 6.75, 3.15, 1.15,
    "第 5 年：收 105 元\n（100 元本金 + 5 元利息）",
    fc="#eaf6ea", ec=C_GREEN, fontsize=11, weight="bold")

# ---------- 标题与脚注 ----------
label(ax, 5.0, 9.35, "一张 5 年期借条的现金流（面值 100 元，票面利率 5%，示意）",
      fontsize=14.5, weight="bold")
label(ax, 5.0, 2.45,
      "你（债主）把钱借出去，换来一串固定的小额回报，最后拿回本金：\n"
      "这就是债券的全部骨架——剩下的都只是在这串现金流上做文章。",
      fontsize=11.5, color="#444444")

save(fig, "w3d1_bond_cashflow.png")
