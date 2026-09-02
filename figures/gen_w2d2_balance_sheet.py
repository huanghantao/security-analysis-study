"""Week 2 - 01 章：资产负债表左右结构图（小满奶茶店年末示意数字）。"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    OUT, save, fig_ax, box, arrow, label,
    C_BLUE, C_GREEN, C_ORANGE, C_PURPLE, C_GRAY, C_RED, C_GOLD,
)

fig, ax = fig_ax(11, 7.6)

# ---- 标题与恒等式 ----
label(ax, 5.0, 9.55, "小满奶茶店 · 年末资产负债表（示意数字，单位：万元）",
      fontsize=13.5, weight="bold")
label(ax, 5.0, 9.02, "资产 70  =  负债 30  +  所有者权益 40",
      fontsize=12.5, weight="bold", color="#333333")

# ---- 左侧容器：资产（资金用途）----
box(ax, 0.35, 1.9, 4.3, 6.6, "", fc="#f3f8fd", ec=C_BLUE, lw=1.8, zorder=1)
label(ax, 2.5, 8.08, "资产（Assets）", fontsize=13, weight="bold", color=C_BLUE)
label(ax, 2.5, 7.62, "钱去哪儿了？——资金的用途", fontsize=10, color="#555555")

box(ax, 0.7, 6.32, 3.6, 0.95, "货币资金（Cash）    28", fontsize=12)
box(ax, 0.7, 5.07, 3.6, 0.95, "应收账款（Receivables）    10", fontsize=12)
box(ax, 0.7, 3.82, 3.6, 0.95, "固定资产·净值（Fixed）    32", fontsize=12)

label(ax, 2.5, 3.32, "前两项：流动资产（一年内能变成现金）", fontsize=9.5, color="#666666")
label(ax, 2.5, 2.84, "第三项：非流动资产（设备装修花了 40，扣掉折旧 8）",
      fontsize=9.5, color="#666666")

# ---- 右侧容器：负债 + 权益（资金来源）----
box(ax, 5.35, 1.9, 4.3, 6.6, "", fc="#fdf6ec", ec=C_GOLD, lw=1.8, zorder=1)
label(ax, 7.5, 8.08, "负债 + 所有者权益（L + E）", fontsize=13, weight="bold", color="#8a6100")
label(ax, 7.5, 7.62, "钱从哪儿来？——资金的来源", fontsize=10, color="#555555")

box(ax, 5.7, 5.72, 3.6, 1.5,
    "负债（Liabilities）\n银行贷款    30",
    fc="#fbeee6", ec=C_ORANGE, fontsize=12)
box(ax, 5.7, 3.12, 3.6, 2.1,
    "所有者权益（Equity）\n老板投入    20\n这一年赚下的利润    20",
    fc="#eaf7ea", ec=C_GREEN, fontsize=12)

label(ax, 7.5, 2.6, "权益 40 = 总资产 70 − 负债 30", fontsize=9.5, color="#666666")
label(ax, 7.5, 2.16, "负债到期要还；权益不用还，分剩下的", fontsize=9.5, color="#666666")

# ---- 底部流向箭头：资金从右边来，花在左边 ----
arrow(ax, (7.5, 1.5), (2.5, 1.5), color=C_GRAY, lw=2.0,
      connectionstyle="arc3,rad=-0.22")
label(ax, 5.0, 0.38, "资金流向：从右边的「来源」流到左边的「用途」",
      fontsize=10.5, color="#555555")

save(fig, "w2d2_balance_sheet.png")
