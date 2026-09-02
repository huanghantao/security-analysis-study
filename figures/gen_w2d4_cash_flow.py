"""Week 2 - 03 章：经营 / 投资 / 筹资三类现金流方向示意图（小满奶茶店第 1 年）。"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    OUT, save, fig_ax, box, arrow, label,
    C_BLUE, C_GREEN, C_ORANGE, C_PURPLE, C_GRAY, C_RED, C_GOLD,
)

fig, ax = fig_ax(11, 7.8)

# ---- 标题 ----
label(ax, 5.0, 9.55, "现金流量表：钱从三类「门」进出——小满奶茶店第 1 年（示意，万元）",
      fontsize=13, weight="bold")

# ---- 中央：现金钱包 ----
box(ax, 4.05, 4.35, 1.9, 1.5, "现金钱包\n（货币资金）",
    fc="#fff7e0", ec=C_GOLD, fontsize=12.5, weight="bold")

# ---- 左：经营活动（净流入 +20）----
box(ax, 0.3, 3.7, 3.1, 2.8,
    "经营活动（Operating）\n卖奶茶收现    +90\n买原料付现    −30\n工资房租等    −40\n净流入  +20",
    fc="#eaf7ea", ec=C_GREEN, fontsize=11)
arrow(ax, (3.5, 5.1), (4.0, 5.1), color=C_GREEN, lw=2.6)

# ---- 右：投资活动（净流出 −40）----
box(ax, 6.6, 4.15, 3.1, 1.9,
    "投资活动（Investing）\n买设备付现    −40\n净流出  −40",
    fc="#fdeeea", ec=C_ORANGE, fontsize=11)
arrow(ax, (6.05, 5.1), (6.5, 5.1), color=C_ORANGE, lw=2.6)

# ---- 下：筹资活动（净流入 +48）----
box(ax, 2.95, 1.15, 4.1, 2.15,
    "筹资活动（Financing）\n股东投入 +20    银行借款 +40\n付利息 −2    还本金 −10\n净流入  +48",
    fc="#f0ecfa", ec=C_PURPLE, fontsize=11)
arrow(ax, (5.0, 3.4), (5.0, 4.3), color=C_PURPLE, lw=2.6)

# ---- 底部总账 ----
label(ax, 5.0, 0.45,
      "全年现金净增加 = +20 − 40 + 48 = +28：期初 0 → 期末 28，正好等于资产负债表里的货币资金",
      fontsize=10.5, color="#555555")

# ---- 三个门的小注（贴近各自的框）----
label(ax, 1.85, 6.85, "做日常生意\n进出后门", fontsize=9.5, color="#4a8a4a")
label(ax, 8.15, 6.5, "买设备、盖厂房\n进出侧门", fontsize=9.5, color="#b0611e")
label(ax, 8.62, 2.2, "找股东和银行\n进出前门", fontsize=9.5, color="#6a4fa3")

save(fig, "w2d4_cash_flow.png")
