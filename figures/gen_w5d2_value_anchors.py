"""Week 5 第 2 章配图：普通股估值的两个锚——盈利能力锚与资产价值锚（概念图）。

这张图是 Week 7 / Week 8 / Week 9 的预告地图：
  锚 1（盈利能力锚：平均盈利 乘以 合理倍数）→ Week 7 展开；
  锚 2（资产价值锚：账面价值 / 流动资产价值）→ Week 8 展开；
  两个锚合成价值区间，再留安全边际 → Week 9 收束。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    OUT, save, fig_ax, box, arrow, label,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_PURPLE,
)

fig, ax = fig_ax(12, 8.6)

# 顶部问题框
box(ax, 3.05, 8.72, 3.9, 1.0,
    "一只普通股\n它到底值多少钱？",
    fc="#fdf3e3", ec=C_ORANGE, fontsize=13.5, weight="bold")

# 顶部框分别引出两支箭头，指向左右两个锚
arrow(ax, (4.1, 8.7), (2.5, 8.12), color=C_GRAY)
arrow(ax, (5.9, 8.7), (7.5, 8.12), color=C_GRAY)

# ---------- 左：锚 1 盈利能力锚 ----------
box(ax, 0.3, 4.0, 4.4, 4.1, "", fc="#eef4fb", ec=C_BLUE)
label(ax, 2.5, 7.72, "锚 1：盈利能力锚（earning power）",
      color=C_BLUE, fontsize=12.5, weight="bold")
box(ax, 0.62, 6.5, 3.76, 0.9,
    "平均盈利：\n近 5~10 年利润的平均值",
    fc="white", ec=C_BLUE, fontsize=11)
arrow(ax, (2.5, 6.44), (2.5, 5.8), color=C_BLUE, zorder=4)
label(ax, 3.6, 6.1, "乘以合理倍数", color=C_BLUE, fontsize=10.5)
box(ax, 0.62, 4.72, 3.76, 1.02,
    "得到一个估值\n（年均利润 10 亿 × 15 倍 = 150 亿）",
    fc="white", ec=C_BLUE, fontsize=10.5)
label(ax, 2.5, 4.34, "→ Week 7 展开：折旧、平均盈利、市盈率",
      color=C_GRAY, fontsize=10)

# ---------- 右：锚 2 资产价值锚 ----------
box(ax, 5.3, 4.0, 4.4, 4.1, "", fc="#edf7ee", ec=C_GREEN)
label(ax, 7.5, 7.72, "锚 2：资产价值锚（asset value）",
      color=C_GREEN, fontsize=12.5, weight="bold")
box(ax, 5.62, 6.55, 3.76, 1.0,
    "账面价值：每股净资产（家底）\n更保守口径：流动资产价值（net-net）",
    fc="white", ec=C_GREEN, fontsize=10.5)
arrow(ax, (7.5, 6.49), (7.5, 5.78), color=C_GREEN, zorder=4)
label(ax, 8.6, 6.1, "打折看\n（资产不等于价值）", color=C_GREEN, fontsize=10)
box(ax, 5.62, 4.72, 3.76, 0.95,
    "得到一条估值底线\n（公司散伙也能值多少）",
    fc="white", ec=C_GREEN, fontsize=10.5)
label(ax, 7.5, 4.34, "→ Week 8 展开：账面价值、清算价值",
      color=C_GRAY, fontsize=10)

# ---------- 底部：两锚合一 + 安全边际 ----------
arrow(ax, (2.5, 3.96), (3.95, 3.14), color=C_GRAY)
arrow(ax, (7.5, 3.96), (6.05, 3.14), color=C_GRAY)
box(ax, 1.5, 1.05, 7.0, 2.05,
    "两个锚各给一个数 → 合成一段价值区间\n"
    "出价 = 价值区间下沿再打一个折扣\n"
    "这条折扣，就是安全边际（margin of safety，Week 9）",
    fc="#f4effa", ec=C_PURPLE, fontsize=12, weight="normal")

label(ax, 5.0, 0.42,
      "估值不是算出一个精确数，而是圈出一段合理范围",
      color=C_GRAY, fontsize=10.5)

save(fig, "w5d2_value_anchors.png")
