#!/usr/bin/env python3
"""把本教程（mdBook 源文件）构建成一份排版好的 PDF。

流水线：
  1. 解析 SUMMARY.md，拿到全书的章节顺序与层级；
  2. 每章用 pandoc 把 Markdown 转成 HTML 片段（公式以 LaTeX 原样透传给 MathJax）；
  3. 配图内联为 data URI，MathJax 内联进 HTML（保证完全离线、单文件）；
  4. 组装成一册完整 HTML：封面 + 目录（带页码）+ 各周分卷页 + 正文；
  5. 用无头 Chrome 打印成 PDF（真实页码、PDF 书签、可点击目录）。

用法：
    python3 scripts/build_pdf.py                 # 输出到 dist/
    python3 scripts/build_pdf.py -o /tmp/x.pdf   # 指定输出路径
    python3 scripts/build_pdf.py --keep-html     # 保留中间 HTML 便于调试
"""

from __future__ import annotations

import argparse
import base64
import html
import mimetypes
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO / "dist" / "读懂证券分析-十周价值投资教程.pdf"

CHROME = Path(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)

# MathJax 3 的 TeX→CHTML 打包版；本地缓存，避免每次构建都联网
MATHJAX_URL = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
MATHJAX_CACHE = Path(tempfile.gettempdir()) / "security-analysis-pdf" / "tex-mml-chtml.js"

PANDOC_FROM = "gfm+tex_math_dollars+pipe_tables+footnotes+task_lists"
PANDOC_TO = "html5"
PANDOC_EXTRA = ["--mathjax", "--wrap=none", "--section-divs=false"]

WEEK_LABELS = {
    "week1": "Week 1：出发前的地图——证券分析是什么、不是什么",
    "week2": "Week 2：财报扫盲——三张表看懂一家公司",
    "week3": "Week 3：债券——借出去的钱怎么保本",
    "week4": "Week 4：优先股、可转债与条款的保护",
    "week5": "Week 5：普通股投资理论——股票是公司的一部分",
    "week6": "Week 6：利润表分析 I——看穿数字的游戏",
    "week7": "Week 7：利润表分析 II——盈利能力与市盈率",
    "week8": "Week 8：资产负债表分析——账面价值与清算价值",
    "week9": "Week 9：价格与价值——市场先生与安全边际",
    "week10": "Week 10：大结业——完整分析一家公司",
}

SUBTITLE = "十周吃透价值投资圣经"
AUTHOR = "为你定制的学习教程"


# --------------------------------------------------------------------------- #
# 1. 解析 SUMMARY.md
# --------------------------------------------------------------------------- #
class Entry:
    """目录里的一条：week 分卷标记，或一章正文。"""

    def __init__(self, kind: str, title: str, path: str | None, level: int = 0, anchor: str = ""):
        self.kind = kind          # "week" | "chapter"
        self.title = title
        self.path = path          # 相对仓库根的 md 路径
        self.level = level        # 0 = 周导读，1 = 周内章节
        self.anchor = anchor      # HTML 里的 id


def parse_summary(summary_path: Path) -> list[Entry]:
    """SUMMARY.md → Entry 列表（跳过前言/概述这类占位行）。"""
    entries: list[Entry] = []
    current_week: str | None = None
    used_anchors: dict[str, int] = {}

    for raw in summary_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# ") and not line.startswith("## "):
            heading = line[2:].strip()
            if re.match(r"^Week\s*\d+", heading):
                current_week = heading
                entries.append(Entry("week", heading, None))
            continue
        m = re.match(r"^-\s*\[(?P<title>[^\]]+)\]\((?P<path>[^)]+)\)", line)
        if not m:
            continue
        title, path = m.group("title"), m.group("path")
        if path.startswith("http") or not path.endswith(".md"):
            continue
        if path == "SUMMARY.md":
            continue
        level = 0 if Path(path).name == "README.md" else 1
        anchor = unique_anchor(path, used_anchors)
        entries.append(Entry("chapter", title, path, level, anchor))
    return entries


def unique_anchor(path: str, used: dict[str, int]) -> str:
    base = "ch-" + re.sub(r"[^0-9A-Za-z]+", "-", path.replace("/", "-")).strip("-").lower()
    if base in used:
        used[base] += 1
        base = f"{base}-{used[base]}"
    else:
        used[base] = 0
    return base


# --------------------------------------------------------------------------- #
# 2. Markdown → HTML（pandoc）
# --------------------------------------------------------------------------- #
def pandoc_available() -> None:
    if shutil.which("pandoc") is None:
        sys.exit("找不到 pandoc，请先安装：brew install pandoc")


def convert_chapter(md_path: Path) -> str:
    proc = subprocess.run(
        ["pandoc", "-f", PANDOC_FROM, "-t", PANDOC_TO, *PANDOC_EXTRA, str(md_path)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        sys.exit(f"pandoc 转换失败：{md_path}\n{proc.stderr}")
    if proc.stderr.strip():
        print(f"  ⚠ pandoc 提示 {md_path.name}: {proc.stderr.strip()[:200]}")
    return proc.stdout


def mark_tall_blocks(fragment: str, min_lines: int = 10, cpl: int = 34, stats: dict | None = None) -> str:
    """给超长引用块/代码块加 .tall，允许它们跨页。

    短块保持"不拆开"（版面更整齐），长块若也硬性不拆，就会被整块推到下一页，
    在上一页留下大片空白。

    cpl 是每行大致可容纳的字符数（引用块两侧有内边距，按 34 字估）。
    """
    def mark(tag: str):
        pattern = re.compile(rf"<{tag}(\s[^>]*)?>(.*?)</{tag}>", flags=re.S)

        def repl(m: re.Match) -> str:
            attrs = m.group(1) or ""
            inner = m.group(2)
            # 估算渲染行数：图片各算 2 行，其余文本按每行 cpl 字折行
            inner_no_img = re.sub(r"<img\b[^>]*>", "", inner)
            text = html.unescape(re.sub(r"<[^>]+>", "", inner_no_img))
            lines = sum(max(1, len(seg) // cpl + 1) for seg in text.splitlines())
            lines += inner.count("<img")
            if lines >= min_lines and "class=" not in attrs:
                if stats is not None:
                    stats["tall_blocks"] = stats.get("tall_blocks", 0) + 1
                return f'<{tag}{attrs} class="tall">{inner}</{tag}>'
            return m.group(0)

        return pattern.sub(repl, fragment)

    fragment = mark("blockquote")
    return mark("pre")


IMG_RE = re.compile(r'(<img\b[^>]*?\bsrc=")([^"]+)(")')
LINK_RE = re.compile(r'<a\b([^>]*?)\bhref="([^"]*)"([^>]*)>', flags=re.S)
EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:", "#")


def inline_images(fragment: str, md_path: Path, stats: dict) -> str:
    """把 <img src="../../figures/out/x.png"> 换成内联 data URI。"""
    base_dir = md_path.parent

    def repl(m: re.Match) -> str:
        src = m.group(2)
        if src.startswith(("data:", "http://", "https://")):
            return m.group(0)
        target = (base_dir / src).resolve()
        if not target.exists():
            stats.setdefault("missing", []).append(str(target))
            return m.group(0)
        mime = mimetypes.guess_type(target.name)[0] or "image/png"
        data = base64.b64encode(target.read_bytes()).decode("ascii")
        stats["images"] = stats.get("images", 0) + 1
        return f"{m.group(1)}data:{mime};base64,{data}{m.group(3)}"

    # 顺手把图片的 width/height 去掉，交给 CSS 控制版心内缩放
    fragment = re.sub(r'(<img\b[^>]*?)\s+width="[^"]*"', r"\1", fragment)
    return IMG_RE.sub(repl, fragment)


def rewrite_links(fragment: str, md_path: Path, path_anchor: dict[str, str], stats: dict) -> str:
    """把书内相对链接（xxx.md / ../weekN/yyy.md）改写成 PDF 内部跳转。

    PDF 里没有"另一个 .md 文件"可打开，所以跨章引用必须在同一份 PDF 内跳转：
    目标文件 → 该章正文的锚点 id（由 unique_anchor 生成，与目录一致）。
    """

    def repl(m: re.Match) -> str:
        pre, href, post = m.group(1), m.group(2), m.group(3)
        if href.startswith(EXTERNAL_SCHEMES) or href.endswith((".png", ".jpg", ".svg")):
            return m.group(0)
        target, _, frag = href.partition("#")
        if not target.endswith(".md"):
            return m.group(0)
        rel = (md_path.parent / target).resolve()
        try:
            key = rel.relative_to(REPO).as_posix()
        except ValueError:
            stats["dead_links"] = stats.get("dead_links", 0) + 1
            return f"<span{pre}{post}>"
        anchor = path_anchor.get(key)
        if anchor is None:
            stats["dead_links"] = stats.get("dead_links", 0) + 1
            return f"<span{pre}{post}>"
        new_href = f"#{anchor}" if frag else f"#{anchor}"
        stats["internal_links"] = stats.get("internal_links", 0) + 1
        return f'<a{pre}href="{new_href}"{post}>'

    return LINK_RE.sub(repl, fragment)


def strip_first_h1(fragment: str) -> tuple[str | None, str]:
    """摘出正文第一个 <h1>，用于自动生成页面标题；返回 (标题, 去掉 h1 的片段)。"""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", fragment, flags=re.S)
    if not m:
        return None, fragment
    title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return html.unescape(title), fragment[: m.start()] + fragment[m.end():]


# --------------------------------------------------------------------------- #
# 3. 组装 HTML
# --------------------------------------------------------------------------- #
CSS = r"""
@page {
  size: A4;
  margin: 20mm 18mm 18mm 18mm;
  @bottom-center {
    content: counter(page);
    font-family: "PingFang SC", "Heiti SC", sans-serif;
    font-size: 8.5pt;
    color: #999999;
  }
}
@page :first {
  margin: 0;
  @bottom-center { content: ""; }
}

html {
  font-size: 10.5pt;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
body {
  margin: 0;
  font-family: "Songti SC", "STSong", "SimSun", "Noto Serif CJK SC", serif;
  line-height: 1.75;
  color: #1a1a1a;
  text-align: justify;
  hyphens: none;
}

/* ---------- 封面 ---------- */
.cover {
  page: cover;
  break-after: page;
  height: 292mm;
  width: 210mm;
  box-sizing: border-box;
  padding: 42mm 24mm 24mm 24mm;
  text-align: center;
  background: linear-gradient(160deg, #f7f4ec 0%, #efe9dc 55%, #e6ddc9 100%);
  position: relative;
}
.cover .rule {
  width: 34mm;
  height: 1.6pt;
  background: #9c2b23;
  margin: 0 auto 12mm auto;
}
.cover h1 {
  font-family: "PingFang SC", "Heiti SC", "Microsoft YaHei", sans-serif;
  font-size: 30pt;
  line-height: 1.4;
  font-weight: 600;
  letter-spacing: 0.5pt;
  color: #14213d;
  margin: 0 0 8mm 0;
  border: none;
  padding: 0;
}
.cover .sub {
  font-size: 15pt;
  color: #9c2b23;
  letter-spacing: 3pt;
  margin-bottom: 22mm;
}
.cover .blurb {
  font-size: 11pt;
  line-height: 2;
  color: #3d3d3d;
  text-align: left;
  border-left: 2.5pt solid #9c2b23;
  padding: 2mm 0 2mm 6mm;
  margin: 0 4mm;
}
.cover .blurb p { margin: 0 0 2mm 0; }
.cover .meta {
  position: absolute;
  left: 24mm;
  right: 24mm;
  bottom: 30mm;
  font-size: 10.5pt;
  color: #4a4a4a;
  line-height: 2;
}
.cover .meta .author { font-size: 12pt; color: #14213d; }

/* ---------- 目录 ---------- */
.toc-page { break-after: page; }
.toc-page > h2 {
  font-family: "PingFang SC", "Heiti SC", sans-serif;
  font-size: 20pt;
  text-align: center;
  border: none;
  margin: 0 0 12mm 0;
  color: #14213d;
  letter-spacing: 4pt;
}
ul.toc { list-style: none; margin: 0; padding: 0; font-size: 10.5pt; }
ul.toc ul { list-style: none; margin: 0 0 3mm 0; padding: 0 0 0 6mm; }
ul.toc li { margin: 0 0 1.4mm 0; }
ul.toc li.week {
  font-family: "PingFang SC", "Heiti SC", sans-serif;
  font-weight: 600;
  font-size: 11.5pt;
  color: #9c2b23;
  margin: 5mm 0 2.5mm 0;
  padding-bottom: 1mm;
  border-bottom: 0.6pt solid #d8cfb8;
  break-after: avoid;
}
ul.toc a {
  color: #1a1a1a;
  text-decoration: none;
  display: block;
  position: relative;
  padding-right: 14mm;
}
/* 页码由构建脚本按第一遍渲染的真实分页回填（Chrome 不支持 target-counter） */
ul.toc a .pg {
  position: absolute;
  right: 0;
  top: 0;
  color: #8a8a8a;
  font-family: "PingFang SC", "Heiti SC", sans-serif;
  font-size: 9.5pt;
}
ul.toc li.week a { color: #9c2b23; }

/* ---------- 分卷页 ---------- */
.part {
  break-before: page;
  margin: 0 0 6mm 0;
  padding: 14mm 0 8mm 0;
  border-bottom: 1.6pt solid #9c2b23;
  break-after: avoid;
}
.part .label {
  font-family: "PingFang SC", "Heiti SC", sans-serif;
  font-size: 9.5pt;
  letter-spacing: 4pt;
  color: #9c2b23;
  margin-bottom: 4mm;
}
.part h2 {
  font-family: "PingFang SC", "Heiti SC", sans-serif;
  font-size: 20pt;
  line-height: 1.45;
  color: #14213d;
  border: none;
  margin: 0;
  padding: 0;
}

/* ---------- 章节 ---------- */
.chapter { break-before: page; }
/* 第一章紧接目录，下面还有正文；封面 → 目录的换页已由 .toc-page 负责 */
.chapter:first-of-type { break-before: auto; }
.chapter > .chapter-head {
  font-family: "PingFang SC", "Heiti SC", sans-serif;
  font-size: 19pt;
  line-height: 1.5;
  color: #14213d;
  margin: 0 0 7mm 0;
  padding-bottom: 3mm;
  border-bottom: 1.2pt solid #9c2b23;
  break-after: avoid;
}
.chapter > .chapter-head .cn {
  display: block;
  font-size: 10pt;
  letter-spacing: 3pt;
  color: #9c2b23;
  font-weight: 400;
  margin-bottom: 2mm;
}

h1, h2, h3, h4 {
  font-family: "PingFang SC", "Heiti SC", "Microsoft YaHei", sans-serif;
  color: #14213d;
  line-height: 1.5;
  break-after: avoid;
}
h2 {
  font-size: 14.5pt;
  margin: 8mm 0 3mm 0;
  padding-left: 3mm;
  border-left: 3pt solid #9c2b23;
}
h3 { font-size: 12pt; margin: 6mm 0 2.5mm 0; }
h4 { font-size: 11pt; margin: 5mm 0 2mm 0; }

p { margin: 0 0 3mm 0; orphans: 2; widows: 2; }
ul, ol { margin: 0 0 3.5mm 0; padding-left: 7mm; }
li { margin-bottom: 1.2mm; }
li > p { margin-bottom: 1.5mm; }

strong { color: #000; }

hr {
  border: none;
  border-top: 0.6pt dashed #c9c0a8;
  margin: 6mm 0;
}

/* 引用块（书里的 划重点 / 易踩坑 / 想一想 都用它） */
blockquote {
  margin: 4mm 0;
  padding: 3mm 5mm;
  background: #f7f4ec;
  border-left: 3pt solid #c9a227;
  border-radius: 0 1.5mm 1.5mm 0;
  break-inside: avoid;
  font-size: 10pt;
  color: #2e2e2e;
}
blockquote > :last-child { margin-bottom: 0; }
blockquote blockquote { background: #f2eede; }
/* 很长的引用块（金句原文 + 译文 + 点评）允许跨页：
   否则一整块被推到下一页，会留下一整页空白 */
blockquote.tall { break-inside: auto; }

/* 表格 */
table {
  border-collapse: collapse;
  width: 100%;
  margin: 4mm 0;
  font-size: 9.5pt;
  break-inside: auto;
}
thead { display: table-header-group; }
tr { break-inside: avoid; }
th, td {
  border: 0.5pt solid #cfc7b2;
  padding: 1.6mm 2.2mm;
  text-align: left;
  vertical-align: top;
}
th {
  background: #efe9dc;
  font-family: "PingFang SC", "Heiti SC", sans-serif;
  font-weight: 600;
  color: #14213d;
}
tbody tr:nth-child(even) { background: #faf8f3; }

/* 代码 */
code {
  font-family: "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.88em;
  background: #f2efe6;
  padding: 0.4mm 1mm;
  border-radius: 1mm;
}
pre {
  background: #f7f4ec;
  border: 0.5pt solid #ded5bd;
  border-radius: 1.5mm;
  padding: 3mm 4mm;
  margin: 4mm 0;
  break-inside: avoid;
  font-size: 9pt;
  line-height: 1.55;
  overflow-wrap: break-word;
  white-space: pre-wrap;
}
pre code { background: none; padding: 0; color: #23303f; }
/* 超长代码块同样允许跨页 */
pre.tall { break-inside: auto; }

/* 图片 */
img {
  max-width: 100%;
  max-height: 105mm;
  display: block;
  margin: 5mm auto;
  break-inside: avoid;
  border: 0.5pt solid #e2dccb;
  border-radius: 1.5mm;
}

/* 公式（MathJax CHTML 输出） */
mjx-container[jax="CHTML"] { outline: none; }
mjx-container[jax="CHTML"][display="true"] {
  margin: 4mm 0 !important;
  break-inside: avoid;
}
mjx-container[jax="CHTML"] mjx-math { font-size: 1.02em; }
"""

MATHJAX_CONFIG = """
window.MathJax = {
  tex: {
    inlineMath: [['\\\\(', '\\\\)']],
    displayMath: [['\\\\[', '\\\\]']],
    processEscapes: false,
    tags: 'none'
  },
  options: {
    enableMenu: false,
    ignoreHtmlClass: 'no-math'
  },
  chtml: { scale: 1.0, displayAlign: 'center' },
  startup: { typeset: true }
};
"""


def build_html(
    entries: list[Entry],
    stats: dict,
    mathjax_js: str,
    page_of: dict[str, int] | None = None,
) -> str:
    page_of = page_of or {}
    path_anchor = {e.path: e.anchor for e in entries if e.kind == "chapter" and e.path}
    chapters: list[tuple[Entry, str]] = []
    for entry in entries:
        if entry.kind != "chapter" or not entry.path:
            continue
        md_path = (REPO / entry.path).resolve()
        if not md_path.exists():
            stats.setdefault("missing_md", []).append(entry.path)
            continue
        frag = convert_chapter(md_path)
        h1, frag = strip_first_h1(frag)
        frag = mark_tall_blocks(frag, stats=stats)  # 先估行数，再内联图片（避免扫 base64）
        frag = inline_images(frag, md_path, stats)
        frag = rewrite_links(frag, md_path, path_anchor, stats)
        chapters.append((entry, frag))

    # ---- 目录 ----
    toc: list[str] = []
    for entry in entries:
        if entry.kind == "week":
            toc.append(f'<li class="week">{html.escape(entry.title)}</li>')
        else:
            if not any(c.path == entry.path for c, _ in chapters):
                continue
            pg = page_of.get(entry.anchor)
            pg_html = f'<span class="pg">{pg}</span>' if pg else ""
            toc.append(
                f'<li class="lvl{entry.level}">'
                f'<a href="#{entry.anchor}">{html.escape(entry.title)}{pg_html}</a></li>'
            )
    toc_html = (
        '<section class="toc-page"><h2>目 录</h2><ul class="toc">'
        + "\n".join(toc)
        + "</ul></section>"
    )

    # ---- 正文 ----
    body: list[str] = []
    for entry, frag in chapters:
        # 锚点直接放在 section 上：额外插一个空的 <a id> 会让 Chrome 多印一页空白
        body.append(f'<section class="chapter" id="{entry.anchor}">')
        body.append(
            f'<div class="chapter-head"><span class="cn">{html.escape(entry.title)}</span></div>'
        )
        body.append(frag)
        body.append("</section>")
    body_html = "\n".join(body)

    cover = f"""<section class="cover">
  <div class="rule"></div>
  <h1>读懂《证券分析》</h1>
  <div class="sub">{html.escape(SUBTITLE)}</div>
  <div class="blurb">
    <p>一套专为<strong>财务零基础</strong>读者定制的手把手教程：从"股票和债券有什么区别"讲起，
    三张报表、债券、可转债、利润表、资产负债表、市场先生、安全边际，
    直到<strong>亲手完整分析一家 A股 / 港股公司</strong>。</p>
    <p>主线教材：本杰明·格雷厄姆 &amp; 戴维·多德《证券分析》（<em>Security Analysis</em>，第六版英文版）。</p>
    <p>每一个概念都从零讲透，不需要会计基础、不需要金融基础、不需要会写代码。</p>
  </div>
  <div class="meta">
    <div class="author">{html.escape(AUTHOR)}</div>
    <div>{date.today():%Y 年 %m 月 %d 日} 编印</div>
  </div>
</section>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>读懂《证券分析》：{html.escape(SUBTITLE)}</title>
<style>{CSS}</style>
<script>{MATHJAX_CONFIG}</script>
<script>{mathjax_js}</script>
</head>
<body>
{cover}
{toc_html}
<main class="book-body">
{body_html}
</main>
</body>
</html>
"""


# --------------------------------------------------------------------------- #
# 4. Chrome 打印
# --------------------------------------------------------------------------- #
def ensure_mathjax() -> str:
    if not MATHJAX_CACHE.exists() or MATHJAX_CACHE.stat().st_size < 100_000:
        MATHJAX_CACHE.parent.mkdir(parents=True, exist_ok=True)
        print(f"  下载 MathJax → {MATHJAX_CACHE}")
        with urllib.request.urlopen(MATHJAX_URL, timeout=60) as resp:
            MATHJAX_CACHE.write_bytes(resp.read())
    return MATHJAX_CACHE.read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# 5. 目录页码：先渲染一遍量出真实页码，再回填重排
# --------------------------------------------------------------------------- #
CHAPTER_HEAD_RE = re.compile(
    r'<section class="chapter" id="(?P<anchor>[^"]+)">\s*'
    r'<div class="chapter-head"><span class="cn">(?P<title>[^<]*)</span></div>',
    flags=re.S,
)


def scan_chapters(html_doc: str) -> list[dict]:
    """从组装好的 HTML 里按出现顺序取出每章的 anchor 与章标题。"""
    return [
        {"anchor": m.group("anchor"), "title": html.unescape(m.group("title")).strip()}
        for m in CHAPTER_HEAD_RE.finditer(html_doc)
    ]


def page_texts(pdf_path: Path) -> list[str]:
    """取出每页的纯文本，并把所有空白压掉。

    PyMuPDF 抽 CJK 文本时常在字间插入空格（"第 0 章"），
    所以匹配前统一去空白，避免被排版空格干扰。
    """
    import fitz

    with fitz.open(pdf_path) as doc:
        return [re.sub(r"\s+", "", doc[i].get_text()) for i in range(doc.page_count)]


CHAPTER_MARK_RE = re.compile(r"第\d{1,2}章")
# 页脚页码（阿拉伯或全角数字）会被抽到页文本最前面，长度有限
PAGE_NO_PREFIX_RE = re.compile(r"^[0-9０-９]{1,4}")


def match_rule(title: str) -> str:
    """章标题 → 在页文本（已去空白）里做匹配的针。

    目录标题长这样：「第 0 章：总览——为什么值得认真读完这本书」，
    把它压成「总览——为什么值得认真读完这本书」；正文里章标记之后的文字形如
    「第0章：总览——…」，所以比对时要允许中间夹一个全角/半角冒号。
    """
    raw = re.sub(r"^第\s*\d+\s*章\s*[:：]?\s*", "", title).strip()
    if title.strip() == "本周导读" or not raw:
        return "本周导读"
    return re.sub(r"\s+", "", raw)[:18]


def is_chapter_start(page_text: str, needle: str) -> bool:
    """判断这一页是否是该章的起始页。

    页脚页码会被抽到页文本最前面（"253下一章：第 3 章…"），所以先把开头的页码
    剥掉，再看剩下的文本是不是正好以章标记开头。

    必须真正"以章标记开头"：像"下一章：第 3 章：粉饰手法…"这种章末指路句
    不能算命中（它出现的页不是该章起始页）。
    """
    body = PAGE_NO_PREFIX_RE.sub("", page_text, count=1)
    if needle == "本周导读":
        return body.startswith("本周导读")
    if not body.startswith("第"):
        return False
    m = CHAPTER_MARK_RE.match(body)
    if not m:
        return False
    rest = re.sub(r"^[:：]\s*", "", body[m.end() :])
    return rest.startswith(needle)


def measure_pages(pdf_texts: list[str], chapters: list[dict]) -> tuple[dict[str, int], list[dict]]:
    """按正文出现顺序定位每章标题，得到 {anchor: 页码}。

    顺序单调递增，所以每章只从上一章起始页之后开始找，
    同名条目（10 个"本周导读"、每周都有的"第 0 章…"）不会串位。
    """
    page_of: dict[str, int] = {}
    problems: list[dict] = []
    search_from = 0

    for ch in chapters:
        needle = match_rule(ch["title"])
        found = None
        for idx in range(search_from, len(pdf_texts)):
            if is_chapter_start(pdf_texts[idx], needle):
                found = idx + 1
                search_from = idx
                break
        if found is None:
            problems.append({**ch, "reason": f"正文中找不到「{needle}」"})
            continue
        page_of[ch["anchor"]] = found
    return page_of, problems


def validate_pages(pdf_texts: list[str], page_of: dict[str, int], chapters: list[dict]) -> list[str]:
    """复核：回填的页码处，是否确实是该章标题。"""
    bad: list[str] = []
    for ch in chapters:
        want = page_of.get(ch["anchor"])
        if not want or want > len(pdf_texts):
            bad.append(f"{ch['title']}：缺页码")
            continue
        if not is_chapter_start(pdf_texts[want - 1], match_rule(ch["title"])):
            bad.append(f"{ch['title']}：第 {want} 页开头是「{pdf_texts[want - 1][:24]}」")
    return bad


# --------------------------------------------------------------------------- #
# 6. PDF 书签（Chrome 不支持 CSS bookmark-level，生成后用 PyMuPDF 写）
# --------------------------------------------------------------------------- #
def add_bookmarks(pdf_path: Path, entries: list[Entry], page_of: dict[str, int]) -> int:
    """按「周 → 章」写入 PDF 大纲，返回写入的条目数。

    PyMuPDF 的大纲格式是嵌套列表：周条目为 [层级, 标题, 页码, 目标点, [子条目…]]。
    """
    import fitz

    def locate(page, title: str):
        """章标题在页面上的精确位置（找不到就退回页首）。"""
        head = re.sub(r"^(第\s*\d+\s*章|本周导读)\s*[:：]?\s*", "", title).strip() or title
        for query in (head[:24], head[:12]):
            hits = page.search_for(query)
            if hits:
                r = hits[0]
                return (r.x0, r.y0)
        return (40, 60)

    # 先在 entries 上按周分组
    groups: list[tuple[Entry, list[Entry]]] = []
    for entry in entries:
        if entry.kind == "week":
            groups.append((entry, []))
        elif entry.kind == "chapter" and entry.path:
            if not groups:
                groups.append((Entry("week", "正文", None), []))
            groups[-1][1].append(entry)

    count = 0
    with fitz.open(pdf_path) as doc:
        # 扁平 4 元组 [层级, 标题, 页码, 页内落点]，层级 1=周、2=章
        outline: list[list] = []
        for week, chapters in groups:
            placed = [c for c in chapters if page_of.get(c.anchor)]
            if not placed:
                continue
            first_page = page_of[placed[0].anchor]
            outline.append([1, week.title, first_page, locate(doc[first_page - 1], "本周导读")])
            count += 1
            for c in placed:
                pno = page_of[c.anchor]
                outline.append([2, c.title, pno, locate(doc[pno - 1], c.title)])
                count += 1
        doc.set_toc(outline)
        doc.save(pdf_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    return count


def find_chrome() -> Path:
    for candidate in (
        CHROME,
        Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
        Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
    ):
        if candidate.exists():
            return candidate
    found = shutil.which("chromium") or shutil.which("google-chrome") or shutil.which("chrome")
    if found:
        return Path(found)
    sys.exit("找不到 Chrome / Chromium，无法打印 PDF。")


def render_html(chrome: Path, html_doc: str, tmp_dir: Path, tag: str) -> tuple[Path, Path]:
    html_path = tmp_dir / f"book-{tag}.html"
    pdf_path = tmp_dir / f"book-{tag}.pdf"
    html_path.write_text(html_doc, encoding="utf-8")
    print_pdf(chrome, html_path, pdf_path)
    return html_path, pdf_path


def print_pdf(chrome: Path, html_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(chrome),
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=60000",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        sys.exit(f"Chrome 打印失败：\n{proc.stdout}\n{proc.stderr}")


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description="把教程构建成 PDF")
    ap.add_argument("-o", "--output", type=Path, default=DEFAULT_OUT, help="输出 PDF 路径")
    ap.add_argument("--keep-html", action="store_true", help="保留中间 HTML 便于调试")
    ap.add_argument("--max-passes", type=int, default=4, help="分页校准的最大遍数")
    args = ap.parse_args()

    pandoc_available()
    summary = REPO / "SUMMARY.md"
    if not summary.exists():
        sys.exit(f"找不到 {summary}")

    print("① 解析 SUMMARY.md …")
    entries = parse_summary(summary)
    n_ch = sum(1 for e in entries if e.kind == "chapter")
    n_wk = sum(1 for e in entries if e.kind == "week")
    print(f"   {n_wk} 个分卷、{n_ch} 章")

    print("② Markdown → HTML（pandoc）…")
    stats: dict = {}
    mathjax_js = ensure_mathjax()
    html_doc = build_html(entries, stats, mathjax_js, page_of=None)
    if "MathJax" not in html_doc:
        sys.exit("MathJax 未能注入 HTML，请检查构建脚本。")
    print(f"   内联配图 {stats.get('images', 0)} 张")
    print(f"   书内跨章链接改写 {stats.get('internal_links', 0)} 处"
          + (f"，其中 {stats['dead_links']} 处目标不在书内，已转为纯文本"
             if stats.get("dead_links") else ""))
    for m in stats.get("missing", []):
        print(f"   ⚠ 缺图：{m}")
    for m in stats.get("missing_md", []):
        print(f"   ⚠ 缺 md：{m}")

    chapters = scan_chapters(html_doc)
    print(f"   识别章节标题 {len(chapters)} 条")
    chrome = find_chrome()
    tmp_dir = Path(tempfile.mkdtemp(prefix="book-pdf-"))
    out_pdf = args.output.resolve()

    print("③ 分页实测：先渲染一遍，量出每章真实页码 …")
    _, probe_pdf = render_html(chrome, html_doc, tmp_dir, "probe")
    page_of, problems = measure_pages(page_texts(probe_pdf), chapters)
    for p in problems:
        print(f"   ⚠ {p['reason']}（{p['title']}）")
    print(f"   已定位 {len(page_of)}/{len(chapters)} 章")

    for attempt in range(1, args.max_passes + 1):
        html_doc = build_html(entries, stats, mathjax_js, page_of=page_of)
        _, pdf_path = render_html(chrome, html_doc, tmp_dir, f"pass{attempt}")
        new_pages, _ = measure_pages(page_texts(pdf_path), chapters)
        drift = {k: (page_of.get(k), v) for k, v in new_pages.items() if page_of.get(k) != v}
        print(f"④ 第 {attempt} 遍排版：{len(new_pages)} 章，页码漂移 {len(drift)} 处")
        page_of = new_pages
        if not drift:
            break
    else:
        print("   ⚠ 页码未完全收敛，采用最后一遍的实测值")

    html_path, final_tmp = render_html(chrome, html_doc, tmp_dir, "final")
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(final_tmp, out_pdf)

    bad = validate_pages(page_texts(out_pdf), page_of, chapters)
    if bad:
        print(f"   ⚠ 目录页码复核发现 {len(bad)} 处不一致：")
        for b in bad[:8]:
            print(f"     - {b}")
    else:
        print("   目录页码复核通过 ✓")

    try:
        n_bm = add_bookmarks(out_pdf, entries, page_of)
        print(f"   写入 PDF 书签 {n_bm} 条 ✓")
    except Exception as exc:  # 书签失败不影响正文
        print(f"   ⚠ 书签写入失败：{exc}")

    size_mb = out_pdf.stat().st_size / 1024 / 1024
    try:
        import fitz

        with fitz.open(out_pdf) as doc:
            pages = doc.page_count
        print(f"⑤ 完成：{out_pdf}（{pages} 页，{size_mb:.1f} MB）")
    except Exception:
        print(f"⑤ 完成：{out_pdf}（{size_mb:.1f} MB）")

    if args.keep_html:
        kept = out_pdf.with_suffix(".html")
        shutil.copy(html_path, kept)
        print(f"   中间 HTML 已保留（可自行调试排版）：{kept}")
    else:
        print("   提示：加 --keep-html 可保留中间 HTML，便于调试排版")
    shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
