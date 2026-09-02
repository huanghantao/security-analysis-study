"""Week 10 第 1 章配图：价值投资五步法流程总图（每步标注用到了第几周的什么）。"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, fig_ax, box, arrow, label, C_BLUE, C_GREEN, C_ORANGE, C_PURPLE, C_GRAY, C_BROWN, C_GOLD

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(11.0, 13.6))
ax.set_xlim(0, 10)
ax.set_ylim(-1.2, 13)
ax.axis("off")

# ---------- 标题 ----------
label(ax, 5, 12.55, "价值投资五步法：把九周的零件装成一条流水线",
      fontsize=15.5, weight="bold", color="#222222")

# ---------- 五个主步骤（左侧）----------
BX, BW, BH = 0.55, 4.55, 1.72          # 左列方框：x、宽、高
ys = [10.30, 7.75, 5.20, 2.65, 0.10]   # 每个方框左下角 y
step_colors = [C_BLUE, C_GREEN, C_GOLD, C_PURPLE, C_ORANGE]

steps = [
    "第①步 · 理解生意（定性）\n它靠什么赚钱？钱好不好赚？能赚多久？\n输出：一句话生意描述 + 能力圈判定",
    "第②步 · 读三表（体检）\n结构 → 勾稽 → 异常信号\n输出：三张表的“体检结论”",
    "第③步 · 调利润（提纯）\n剔非经常、验口径、看现金、查折旧\n输出：扣非的、可比的盈利能力",
    "第④步 · 双锚估值（称重）\n盈利能力 × 保守倍数 + 资产锚对照\n输出：一段价值区间（不是目标价）",
    "第⑤步 · 安全边际与纪律（出手）\n保守下沿 → 折扣判定 → 分批与检查\n输出：观察价 / 买入价 / 卖出信号",
]

for (y, text, color) in zip(ys, steps, step_colors):
    box(ax, BX, y, BW, BH, text, fc="#f4f8fd", ec=color, fontsize=11.5,
        weight="normal", lw=2.0)

# 步骤之间的向下箭头
for i in range(4):
    arrow(ax, (BX + BW / 2, ys[i]), (BX + BW / 2, ys[i + 1] + BH),
          color=C_GRAY, lw=2.2)

# ---------- 右侧：每一步用到了哪几周的什么 ----------
week_notes = [
    "用到：Week 1 第 3 章\n（定量 vs 定性、能力圈）\nWeek 5 第 2 章（盈利能力）",
    "用到：Week 1 第 5 章（查年报）\nWeek 2 全周（三表 + 勾稽）",
    "用到：Week 6（非经常项目、\n粉饰手法、利润表四问）\nWeek 7（折旧、平均盈利）",
    "用到：Week 5 第 2 章（两个锚）\nWeek 7（PE 尺度与倍数纪律）\nWeek 8（账面价值、net-net）",
    "用到：Week 4 第 4 章（定期检查）\nWeek 9（市场先生、安全边际、\n逆向三前提）",
]

NOTE_X = 7.45
for (y, note, color) in zip(ys, week_notes, step_colors):
    cy = y + BH / 2
    # 连接小箭头：从主方框右缘指向右侧注释
    arrow(ax, (BX + BW + 0.08, cy), (NOTE_X - 0.42, cy), color=color, lw=1.4)
    label(ax, NOTE_X + 1.05, cy, note, fontsize=10.5, color="#333333")

# ---------- 底部说明 ----------
label(ax, 5, -0.75, "任何一步没走完，就不进入下一步——“跳步”是散户亏损的第一大来源。",
      fontsize=11, color=C_GRAY)

save(fig, "w10d2_flow.png")
