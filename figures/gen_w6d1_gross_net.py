"""Week 6 第 1 章配图：总额法 vs 净额法——同一笔订单，两种记法。

设定：一笔 1000 元订单，平台留 100 元佣金，900 元货款转给商家。
总额法把 900 元"过路钱"同时记进收入和成本；净额法只记 100 元佣金。
两种记法毛利都是 100 元，营业收入却差 10 倍——所以先问口径，再谈规模。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import save, fig_ax, box, arrow, label, C_BLUE, C_RED, C_GREEN, C_ORANGE, C_GRAY

fig, ax = fig_ax(width=12, height=7.2)

# ── 顶部：订单设定 ─────────────────────────────────────────────
label(ax, 5.0, 9.55,
      "一笔 1000 元订单：平台留 100 元佣金，900 元货款转给商家",
      fontsize=12.5, weight="bold")

# ── 两行的纵向位置 ─────────────────────────────────────────────
ROW_A_Y = 7.05      # 总额法一行方框的底边
ROW_B_Y = 4.15      # 净额法一行方框的底边
H = 1.15            # 方框高度
COL = [             # (x, 宽度)
    (0.15, 1.80),   # 买家付款
    (2.40, 2.20),   # 营业收入
    (5.05, 2.35),   # 营业成本
    (7.85, 2.00),   # 毛利
]

label(ax, COL[0][0], 8.75,
      "总额法（主要责任人）：把自己当成卖方，900 元货款也记进自己的账",
      fontsize=12, weight="bold", color=C_RED, ha="left")
label(ax, COL[0][0], 5.85,
      "净额法（代理人）：只把 100 元佣金记成收入，900 元货款不进报表",
      fontsize=12, weight="bold", color=C_GREEN, ha="left")


def draw_row(y, texts, fills, edges, sizes=(12, 12, 12, 12), weights=("normal",) * 4):
    for (x, w), text, fc, ec, fs, wt in zip(COL, texts, fills, edges, sizes, weights):
        box(ax, x, y, w, H, text, fc=fc, ec=ec, fontsize=fs, weight=wt, lw=1.6)
    for i in range(3):
        x_from = COL[i][0] + COL[i][1]
        x_to = COL[i + 1][0]
        arrow(ax, (x_from, y + H / 2), (x_to, y + H / 2), color=C_GRAY, lw=1.8,
              shrinkA=1, shrinkB=1)


# 总额法：900 元同时进收入（被包在 1000 里）和成本
draw_row(
    ROW_A_Y,
    ["买家付款\n1000 元", "营业收入\n1000 元", "营业成本\n900 元（过路钱）", "毛利\n100 元"],
    ["#fdf3e7", "#eef4fb", "#fdecea", "#e8f6e8"],
    [C_ORANGE, C_BLUE, C_RED, C_GREEN],
)
label(ax, 5.0, 6.60,
      "900 元货款在收入里露一次面、在成本里再露一次面，一进一出正好抵掉，一分利润都不留",
      fontsize=10.5, color=C_RED)

# 净额法：900 元货款根本不进自己的收入
draw_row(
    ROW_B_Y,
    ["买家付款\n1000 元", "营业收入\n100 元（佣金）", "营业成本\n0 元（不碰货款）", "毛利\n100 元"],
    ["#fdf3e7", "#eef4fb", "#f5f5f5", "#e8f6e8"],
    [C_ORANGE, C_BLUE, C_GRAY, C_GREEN],
)
label(ax, 5.0, 3.70,
      "900 元货款由买家直接付给商家，收入、成本这两行都不经过",
      fontsize=10.5, color=C_GRAY)

# ── 结论 ──────────────────────────────────────────────────────
box(ax, 0.15, 1.45, 9.70, 1.30,
    "同一笔生意，毛利和净利润都是 100 元；差的是营业收入这一行：1000 对 100，差 10 倍\n"
    "所以比\u201c规模\u201d之前先问口径——比毛利额、营业利润、经营现金流，别拿营业收入直接比",
    fc="#fffbe6", ec=C_GRAY, fontsize=11.5, weight="bold", lw=1.4)

save(fig, "w6d1_gross_net.png")
