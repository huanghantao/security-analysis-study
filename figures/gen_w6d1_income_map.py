"""Week 6 第 1 章配图：利润表逐行阅读地图。

左边一列：从收入到净利润的逐行结构（行名取 A股 利润表常见行名）；
右边一列：每一行可能"藏猫腻"的位置。
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from figures._common import OUT, save, fig_ax, box, arrow, label, C_BLUE, C_RED, C_GREEN, C_ORANGE, C_GRAY

fig, ax = fig_ax(width=12, height=11)

ROWS = [
    # (左侧行名, 右侧提示, 左框配色, 右框配色)
    ("① 营业收入",
     "猫腻：什么时候算\u201c赚到了\u201d？\n赊账、渠道压货、突击确认",
     "#eef4fb", C_BLUE, "#fdecea", C_RED),
    ("② 营业成本 → 毛利",
     "猫腻：存货计价口径一换\n毛利率立刻变形",
     "#eef4fb", C_BLUE, "#fdecea", C_RED),
    ("③ 期间费用\n（销售 / 管理 / 研发 / 财务）",
     "猫腻：费用被\u201c递延\u201d或塞进盈余\n当期利润凭空变好",
     "#eef4fb", C_BLUE, "#fdecea", C_RED),
    ("④ 折旧与减值",
     "猫腻：年限与减值时点都能调节利润\n警惕过度减记为来年\u201c洗大澡\u201d",
     "#eef4fb", C_BLUE, "#fdecea", C_RED),
    ("⑤ 营业利润",
     "重点：主业的真实答卷\n前四行的所有选择都汇总在这里",
     "#e8f6e8", C_GREEN, "#e9f7ec", C_GREEN),
    ("⑥ 营业外收支 / 投资收益\n/ 其他收益",
     "猫腻：非经常项目的主战场\n卖资产、政府补助、公允价值变动",
     "#fdf3e7", C_ORANGE, "#fdecea", C_RED),
    ("⑦ 所得税费用",
     "验钞机：报给税务局的利润\n与报给股东的差距过大要警惕",
     "#f2f2f2", C_GRAY, "#f7f7f7", C_GRAY),
    ("⑧ 净利润（归母）",
     "终点：先剔非经常、再看多年平均\n单年净利润不等于盈利能力",
     "#e8f6e8", C_GREEN, "#e9f7ec", C_GREEN),
]

BOX_H = 0.80          # 方框高度
PITCH = 1.15          # 行距
TOP = 8.75            # 第一行方框的底边 y
LX, LW = 0.15, 3.45   # 左列方框
RX, RW = 4.10, 5.72   # 右列方框

# 列标题
label(ax, LX + LW / 2, 9.85, "利润表：从收入到净利润", fontsize=13, weight="bold")
label(ax, RX + RW / 2, 9.85, "逐行扫描：可能藏猫腻的位置", fontsize=13, weight="bold", color=C_RED)

ys = [TOP - i * PITCH for i in range(len(ROWS))]
for i, (left_text, right_text, lfc, lec, rfc, rec) in enumerate(ROWS):
    y = ys[i]
    box(ax, LX, y, LW, BOX_H, left_text, fc=lfc, ec=lec,
        fontsize=11.5, weight="bold", tc="#1a1a1a")
    box(ax, RX, y, RW, BOX_H, right_text, fc=rfc, ec=rec,
        fontsize=10.5, tc="#333333")
    # 左列行与行之间的下行箭头
    if i < len(ROWS) - 1:
        arrow(ax, (LX + LW / 2, y), (LX + LW / 2, y - PITCH + BOX_H),
              color=C_GRAY, lw=1.8, shrinkA=2, shrinkB=2)

# 底部读法总结
label(ax, 5.0, 0.22,
      "读法总结：剔除非经常项目 → 取 5-10 年平均 → 才是可用来估值的\u201c盈利能力\u201d（下周展开）",
      fontsize=11, weight="bold")

save(fig, "w6d1_income_map.png")
