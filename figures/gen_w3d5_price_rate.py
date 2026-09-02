"""Week 3 第 4 章配图：市场利率上行 → 同一张借条的价格下跌（双柱对比）。

左：5 年期借条（票息 5 元/年、面值 100）：利率 5% → 6%，价格 100 → 约 96（快捷公式反解的近似值）。
右：无期限借条（每年付 5 元、永不还本，示意）：利率 5% → 6%，价格 100 → 约 83（价格 = 票息 ÷ 利率）。
期限越长，同幅度加息跌得越狠——这就是"久期"的一句话直觉。
说明文字一律放在绘图区下方，避免压住柱体。
"""
import sys, pathlib

import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, C_BLUE, C_ORANGE

fig, axes = plt.subplots(1, 2, figsize=(11, 6.4), sharey=True)

panels = [
    {
        "ax": axes[0],
        "title": "5 年期借条（每年付 5 元利息）",
        "prices": [100.0, 95.7],
        "labels": ["100 元", "约 96 元"],
        "drop": "跌约 4%",
    },
    {
        "ax": axes[1],
        "title": "无期限借条（每年付 5 元，永不还本，示意）",
        "prices": [100.0, 83.3],
        "labels": ["100 元", "约 83 元"],
        "drop": "跌约 17%",
    },
]

for p in panels:
    ax = p["ax"]
    ax.bar([0, 1], p["prices"], width=0.5,
           color=[C_BLUE, C_ORANGE], alpha=0.88, zorder=2)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["市场利率 5%", "市场利率 6%"], fontsize=12)
    ax.set_ylim(60, 116)
    ax.set_xlim(-0.6, 1.6)
    ax.set_title(p["title"], fontsize=12.5, pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", ls=":", color="#cccccc", zorder=0)
    ax.set_xlabel("市场利率（假设）", fontsize=11)
    # 柱顶价格标签
    ax.text(0.0, 101.5, p["labels"][0], ha="center", fontsize=12, weight="bold", color=C_BLUE)
    ax.text(1.0, p["prices"][1] + 1.6, p["labels"][1], ha="center", fontsize=12,
            weight="bold", color=C_ORANGE)
    # 跌幅标注（两柱之间上方，下方无柱体）
    ax.text(0.5, 108.0, p["drop"], ha="center", fontsize=12.5, weight="bold", color="#c0392b",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none"))

axes[0].set_ylabel("借条价格（面值 = 100 元）", fontsize=12)
fig.suptitle("市场利率上行 → 同一张借条变便宜（近似估算的示意数字）", fontsize=14.5, y=0.98)

# 说明文字统一放在绘图区下方，不压柱体
notes = [
    "为什么跌得不一样：5 年期借条快到期、价格被“到期拿回 100 元”拽住，只跌约 4%；",
    "无期限借条只能靠“票息 ÷ 利率”重新定价，跌约 17% —— 期限越长，同幅度加息跌得越狠（“久期”的一句话直觉）。",
    "估算法：无期限借条价格 = 票息 ÷ 利率（5 ÷ 6% ≈ 83）；5 年期借条用第 0 章的快捷公式反解（约 96）；精确值要用 Week 2 数学小灶的贴现公式逐笔折现。",
]
for i, t in enumerate(notes):
    fig.text(0.5, 0.098 - i * 0.043, t, ha="center", fontsize=10, color="#555555")

fig.subplots_adjust(left=0.08, right=0.98, top=0.87, bottom=0.26, wspace=0.12)
save(fig, "w3d5_price_rate.png")
