"""Week 8 第 2 章配图：清算瀑布图——各类资产清算时能收回几成账面价值。

数据照原书摘录：《证券分析》第 43 章（md 612）的清算折扣表（1930 年代美国经验）：
  现金类资产 100；应收账款 75~90（平均 80）；存货 50~75（平均 66 2/3）；
  固定及杂项资产 1~50（平均约 15）。
浅色条 = 原书给出的正常区间；实色条 = 原书给出的粗略平均。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, C_GREEN, C_BLUE, C_ORANGE, C_RED

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams["font.sans-serif"] = [
    "Arial Unicode MS", "PingFang SC", "Hiragino Sans GB", "STHeiti", "Songti SC",
]
plt.rcParams["axes.unicode_minus"] = False

rows = [
    # (名称, 区间下限, 区间上限, 平均, 颜色, 右侧说明)
    ("现金类资产\n（含按市价的证券）", 100, 100, 100, C_GREEN, "100%，一分不少"),
    ("应收账款\n（扣除常规坏账准备）", 75, 90, 80, C_BLUE, "75~90%（平均 80%）"),
    ("存货\n（成本与市价孰低）", 50, 75, 66.7, C_ORANGE, "50~75%（平均约 66.7%）"),
    ("固定资产及杂项\n（厂房、设备、无形资产等）", 1, 50, 15, C_RED, "1~50%（平均约 15%）"),
]

fig, ax = plt.subplots(figsize=(12.5, 7.2))
ax.set_xlim(0, 168)
ax.set_ylim(0, 5.6)

BAR_H = 0.52
ys = [4.3, 3.15, 2.0, 0.85]

for (name, lo, hi, avg, color, note), y in zip(rows, ys):
    if hi > lo:  # 浅色区间条
        ax.barh(y, hi - lo, left=lo, height=BAR_H, fc=color, alpha=0.22, zorder=2)
    ax.barh(y, avg, height=BAR_H, fc=color, zorder=3)  # 实色平均条
    ax.text(104, y, note, va="center", ha="left", fontsize=11.5, color="#333333")

ax.set_yticks(ys)
ax.set_yticklabels([r[0] for r in rows], fontsize=11.5)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=11)
ax.set_xlabel("清算时能收回的账面价值比例", fontsize=12)
ax.set_title("清算时，各类资产还能收回几成账面价值？", fontsize=15.5, pad=30)
ax.text(0, 5.28, "照原书摘录：《证券分析》第 43 章清算折扣表（1930 年代美国经验，md 612）",
        fontsize=11, color="#666666")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# 手动画图例（放在右下空白区）
legend_y = 0.12
ax.add_patch(mpatches.Rectangle((100, legend_y), 3.0, 0.3,
                                fc="#bbbbbb", alpha=0.25, ec="#999999", lw=0.8))
ax.text(104.5, legend_y + 0.15, "浅色 = 原书正常区间", va="center", fontsize=10.5, color="#555555")
ax.add_patch(mpatches.Rectangle((136, legend_y), 3.0, 0.3, fc="#666666"))
ax.text(140.5, legend_y + 0.15, "实色 = 粗略平均", va="center", fontsize=10.5, color="#555555")

fig.text(0.01, 0.005,
         "清算计算的第一规则：负债按面值足额扣除，资产才打折扣——《证券分析》第 43 章，md 612",
         fontsize=10.5, color="#666666")

OUT.mkdir(parents=True, exist_ok=True)
path = OUT / "w8d3_liquidation.png"
fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"  saved {path}")
