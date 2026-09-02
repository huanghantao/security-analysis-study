"""Week 4 第 0 章配图：资本结构层叠图。

同一公司的三层资本结构（债券 / 优先股 / 普通股）：
- 位置：上层的求偿顺位靠前；
- 每层标注收益特征与风险特征；
- 左侧箭头表示"公司清算时排队领钱的顺序"。

输出：figures/out/w4d1_pref_stack.png
"""

import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, fig_ax, box, arrow, label, C_BLUE, C_ORANGE, C_GREEN, C_GRAY

fig, ax = fig_ax(width=12.5, height=7)

# 顶部说明
label(ax, 5.0, 9.72, "同一家公司的资本结构：三层楼", fontsize=14, weight="bold")

# 左侧：清算顺序大箭头
arrow(ax, (1.7, 9.0), (1.7, 3.35), color=C_GRAY, lw=2.2)
label(ax, 1.02, 6.2, "公司清算时\n排队领钱的\n顺序（自上而下）", fontsize=10.5, color=C_GRAY)

# 三层方框（x, y 为左下角）
box(ax, 2.6, 7.55, 4.7, 1.55,
    "【债券】求偿顺位 ①\n收益：票息固定 + 到期还本（封顶）\n风险：三层中最低，但公司赚再多也拿不到",
    fc="#eef4fb", ec=C_BLUE, fontsize=11, weight="normal")
box(ax, 2.6, 5.45, 4.7, 1.55,
    "【优先股】求偿顺位 ②\n收益：股息固定、没有到期日（封顶）\n风险：股息说停就停，还没有到期日兜底",
    fc="#fdf3e0", ec=C_ORANGE, fontsize=11, weight="normal")
box(ax, 2.6, 3.35, 4.7, 1.55,
    "【普通股】求偿顺位 ③\n收益：分红不固定，上不封顶\n风险：三层中最高，前面分剩的才是它的",
    fc="#eef8ee", ec=C_GREEN, fontsize=11, weight="normal")

# 右侧：每层一句话定位
label(ax, 8.75, 8.32, "像债：\n拿固定利息", fontsize=10.5, color=C_BLUE)
label(ax, 8.75, 6.22, "像债地拿息\n像股地担风险", fontsize=10.5, color=C_ORANGE)
label(ax, 8.75, 4.12, "像股：\n赚多赚少全看它", fontsize=10.5, color=C_GREEN)

# 底部：利润分配顺序
label(ax, 5.0, 1.75,
      "同一笔利润的分配顺序：先付债券利息 → 再付优先股股息 → 剩下的全归普通股股东",
      fontsize=12, weight="bold")
label(ax, 5.0, 0.85,
      "位置越靠上，求偿越靠前、拿钱越稳；位置越靠下，风险越大、但上限越高",
      fontsize=10.5, color=C_GRAY)

save(fig, "w4d1_pref_stack.png")
