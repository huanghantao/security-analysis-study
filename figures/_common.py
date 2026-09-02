"""生图脚本公共设施：中文字体、输出目录、概念图常用的方框/箭头/标注函数。

每个 gen_*.py 脚本开头：

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from figures._common import OUT, save, fig_ax, box, arrow, label, ...

脚本可以独立运行，也可以被 gen_all.py 统一运行。

图片质量硬要求（每次交付前必须自查）：
  1. 文字不遮挡文字、文字不遮挡线条、线条不遮挡文字、线条不遮挡线条；
  2. 标注一律带白色衬底（本文件的 box/label 已内置）；
  3. 多个元素之间留足间距，放不下就加 figsize 或缩小字号；
  4. 生成后用 read_image 亲自看一遍，发现遮挡就改脚本重跑。
"""

import pathlib

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "out"

plt.rcParams["font.sans-serif"] = [
    "Arial Unicode MS",
    "PingFang SC",
    "Hiragino Sans GB",
    "STHeiti",
    "Songti SC",
]
plt.rcParams["axes.unicode_minus"] = False

# 统一的配色
C_BLUE = "#1f77b4"
C_ORANGE = "#ff7f0e"
C_GREEN = "#2ca02c"
C_RED = "#d62728"
C_GRAY = "#7f7f7f"
C_PURPLE = "#9467bd"
C_BROWN = "#8c564b"
C_GOLD = "#b8860b"


def save(fig, name: str, dpi: int = 150):
    """保存图片到 figures/out/，并关闭画布。"""
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved {path}")


def fig_ax(width=10, height=6):
    """新建一幅白底画布，返回 (fig, ax)。"""
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    return fig, ax


def fig_multi(rows, cols, width=12, height=6):
    """新建多子图画布，返回 (fig, axes)。axes 为按行展平的列表。"""
    fig, axes = plt.subplots(rows, cols, figsize=(width, height))
    flat = list(axes.flat) if hasattr(axes, "flat") else [axes]
    for ax in flat:
        ax.axis("off")
    return fig, flat


def box(ax, x, y, w, h, text, fc="#eef4fb", ec=C_BLUE, fontsize=12,
        tc="#222222", lw=1.6, style="round,pad=0.02,rounding_size=0.15",
        weight="normal", zorder=3):
    """画一个带文字的圆角方框（x, y 为左下角，w/h 为宽高）。"""
    import matplotlib.patches as mpatches

    rect = mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle=style, fc=fc, ec=ec, lw=lw, zorder=zorder
    )
    ax.add_patch(rect)
    ax.text(
        x + w / 2, y + h / 2, text, ha="center", va="center",
        fontsize=fontsize, color=tc, weight=weight, zorder=zorder + 2,
        linespacing=1.5,
    )
    return rect


def arrow(ax, xy_from, xy_to, color=C_GRAY, lw=1.8, style="-|>",
          connectionstyle=None, ls="-", zorder=2, shrinkA=6, shrinkB=6):
    """画一支箭头（默认两端各留 6pt 空隙，避免戳进方框里）。"""
    ax.annotate(
        "",
        xy=xy_to,
        xytext=xy_from,
        arrowprops=dict(
            arrowstyle=style,
            color=color,
            lw=lw,
            linestyle=ls,
            shrinkA=shrinkA,
            shrinkB=shrinkB,
            mutation_scale=16,
            connectionstyle=connectionstyle or "arc3,rad=0",
        ),
        zorder=zorder,
    )


def label(ax, x, y, text, color="#222222", fontsize=12, ha="center",
          va="center", weight="normal", zorder=6, alpha=0.9):
    """放一段带白色衬底的文字（衬底把压在下面的线条垫掉，避免糊成一团）。"""
    ax.text(
        x, y, text, color=color, fontsize=fontsize, ha=ha, va=va,
        weight=weight, zorder=zorder, linespacing=1.5,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=alpha),
    )
