"""Week 8 第 1 章配图：净-净价值（net-net）的资产分层计算图（本周最重要的图）。

左列：流动资产逐项全额计入；非流动资产整体划掉、按 0 计；
右列：减去全部负债（足额、不打折），得到净-净价值，再与市价对照。
底部：账面价值 → 净-净口径 → 市价 的三级阶梯。
全部数字为教学示意数字。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import (
    OUT, save, fig_ax, box, arrow, label,
    C_BLUE, C_ORANGE, C_GREEN, C_GRAY, C_RED,
)

fig, ax = fig_ax(13, 9.2)

label(ax, 5.0, 9.55, "净-净价值（net-net）：只数流动资产，其余全部归零",
      fontsize=15, weight="bold")
label(ax, 5.0, 9.02, "示意公司：总股本 2 亿股，市价 1.2 元/股（教学示意数字，非真实公司）",
      fontsize=10.5, color=C_GRAY)

# ---------- 左列：数流动资产 ----------
label(ax, 2.45, 8.56, "第 1 步：数流动资产（按账面全额）",
      color=C_BLUE, fontsize=12, weight="bold")
box(ax, 0.45, 7.65, 4.0, 0.6, "✓  现金及等价物  3 亿",
    fc="#eef7ee", ec=C_GREEN, fontsize=11)
box(ax, 0.45, 6.9, 4.0, 0.6, "✓  应收账款  2 亿",
    fc="#eef7ee", ec=C_GREEN, fontsize=11)
box(ax, 0.45, 6.15, 4.0, 0.6, "✓  存货  2 亿",
    fc="#eef7ee", ec=C_GREEN, fontsize=11)
label(ax, 2.45, 5.8, "流动资产合计 7 亿", color=C_GREEN, fontsize=11.5, weight="bold")

label(ax, 2.45, 5.28, "非流动资产：整体划掉，按 0 计",
      color=C_RED, fontsize=12, weight="bold")
box(ax, 0.45, 4.22, 4.0, 0.6, "✗  厂房设备  4 亿  →  按 0 计",
    fc="#f0f0f0", ec=C_GRAY, tc="#777777", fontsize=11)
box(ax, 0.45, 3.47, 4.0, 0.6, "✗  商誉、品牌等无形  1 亿  →  按 0 计",
    fc="#f0f0f0", ec=C_GRAY, tc="#777777", fontsize=11)

# ---------- 右列：减全部负债 ----------
label(ax, 7.55, 8.56, "第 2 步：减去全部负债（足额，不打折）",
      color=C_RED, fontsize=12, weight="bold")
box(ax, 5.55, 7.65, 4.0, 0.6, "流动负债  1.5 亿", fc="white", ec=C_RED, fontsize=11)
box(ax, 5.55, 6.9, 4.0, 0.6, "长期借款  2.5 亿", fc="white", ec=C_RED, fontsize=11)
box(ax, 5.55, 6.15, 4.0, 0.6, "负债合计  4 亿", fc="#fdeeee", ec=C_RED,
    fontsize=11, weight="bold")
arrow(ax, (7.55, 6.1), (7.55, 5.85), color=C_RED)

box(ax, 5.55, 4.55, 4.0, 1.25,
    "净-净价值 = 7 − 4 = 3 亿\n每股 = 3 ÷ 2 = 1.5 元/股",
    fc="#e9f5ea", ec=C_GREEN, fontsize=12.5, weight="bold")

box(ax, 5.55, 3.05, 4.0, 1.1,
    "市价 1.2 元/股（示意）\n市值 2.4 亿 < 净流动资产 3 亿",
    fc="white", ec=C_ORANGE, fontsize=11)

# ---------- 底部：三级阶梯 ----------
box(ax, 0.45, 1.5, 2.8, 0.95, "账面价值口径\n每股 3.5 元",
    fc="#eef4fb", ec=C_BLUE, fontsize=11)
box(ax, 3.6, 1.5, 2.8, 0.95, "净-净口径\n每股 1.5 元",
    fc="#e9f5ea", ec=C_GREEN, fontsize=11, weight="bold")
box(ax, 6.75, 1.5, 2.8, 0.95, "市价\n1.2 元（示意）",
    fc="#fdf3e3", ec=C_ORANGE, fontsize=11)
arrow(ax, (3.28, 1.98), (3.57, 1.98), color=C_GRAY)
label(ax, 3.42, 2.72, "划掉\n非流动", fontsize=9, color=C_GRAY)
arrow(ax, (6.43, 1.98), (6.72, 1.98), color=C_GRAY)
label(ax, 6.57, 2.72, "市场\n再打折", fontsize=9, color=C_GRAY)

label(ax, 5.0, 0.75, "一句口诀：数现金，问应收，看存货；厂房、品牌、商誉，一概不信。",
      fontsize=12, weight="bold", color="#444444")

save(fig, "w8d2_netnet.png")
