"""Week 5 第 3 章配图：利润的两个去向——留存再投资 vs 派发股息（流向图）。

左侧是公司今年赚到的利润，右上 / 右下分别是两条去路与各自的价值逻辑：
  去向 A 留存再投资：用得好（未来利润更多）vs 用不好（利润蒸发，代理问题）；
  去向 B 派发股息：真金白银落袋，股东自己决定怎么用（回购是变相的派发）。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    OUT, save, fig_ax, box, arrow, label,
    C_BLUE, C_ORANGE, C_GREEN, C_RED, C_GRAY, C_PURPLE,
)

fig, ax = fig_ax(12.5, 8.2)

# ---------- 左：利润池 ----------
box(ax, 0.3, 3.9, 2.75, 2.3,
    "公司今年\n赚到的利润\n（净利润）",
    fc="#eef4fb", ec=C_BLUE, fontsize=12.5, weight="bold")

# ---------- 上路：留存再投资 ----------
arrow(ax, (3.1, 5.45), (4.0, 6.85), color=C_GREEN)
label(ax, 3.06, 6.42, "去向 A：留存", color=C_GREEN, fontsize=11, weight="bold")
box(ax, 4.0, 6.3, 2.8, 1.45,
    "留存再投资\n（利润留在公司里）",
    fc="#edf7ee", ec=C_GREEN, fontsize=11.5, weight="bold")

arrow(ax, (6.85, 7.35), (7.6, 8.6), color=C_GREEN)
arrow(ax, (6.85, 6.7), (7.6, 6.55), color=C_RED)
box(ax, 7.6, 8.35, 2.3, 1.5,
    "用得好\n未来利润更多\n（复利滚雪球）",
    fc="#edf7ee", ec=C_GREEN, fontsize=10.5)
box(ax, 7.6, 5.65, 2.3, 1.5,
    "用不好\n利润蒸发、乱扩张\n（代理问题）",
    fc="#fbeeee", ec=C_RED, fontsize=10.5)

# ---------- 下路：派发股息 ----------
arrow(ax, (3.1, 4.6), (4.0, 3.25), color=C_ORANGE)
label(ax, 3.06, 3.62, "去向 B：派发", color=C_ORANGE, fontsize=11, weight="bold")
box(ax, 4.0, 2.55, 2.8, 1.45,
    "派发给股东\n（现金股息 / 回购）",
    fc="#fdf3e3", ec=C_ORANGE, fontsize=11.5, weight="bold")

arrow(ax, (6.85, 3.27), (7.6, 3.27), color=C_ORANGE)
box(ax, 7.6, 2.55, 2.3, 1.45,
    "股东落袋\n自己决定怎么用\n（回报里最实的一笔）",
    fc="#fdf3e3", ec=C_ORANGE, fontsize=10.5)

# ---------- 底部：两句话总结 ----------
label(ax, 5.0, 1.35,
      "格雷厄姆：盈利能力相同时，分红慷慨的股票通常更值钱\n"
      "——利润是留在公司还是分出来，价值并不一样",
      color=C_GRAY, fontsize=11)
label(ax, 5.0, 0.42,
      "Part IV 导读·伯克维茨：自由现金流是股东一切回报的源头",
      color=C_PURPLE, fontsize=10.5)

save(fig, "w5d3_dividend_flow.png")
