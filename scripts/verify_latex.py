"""LaTeX 转换规范性检查（全仓库正文）。

检查 learning-guide/ 与根 README.md：
  1. 剥离代码围栏 / 行内代码 / 图片 / 链接文字之后，剩余正文中的 $ 必须成对
     （行内 $...$ 同行闭合；$$ 成对）；
  2. 正文（同上剥离后）不得残留 Unicode 数学字符；
  3. 正文不得残留制表符矩阵边框。

用法：python scripts/verify_latex.py
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# 正文不允许残留的 Unicode 数学字符（代码块/行内代码/图片 alt 中豁免）
BANNED = set("×·≈≠≤≥√∑∏λθαβγεΣΠΔ¹²³⁰ᵀ⁻½⅓⅔¼₁₂⇔−")


def strip_protected(text: str) -> str:
    """去掉代码围栏、行内代码、图片、链接显示文字，返回"纯正文"。"""
    # 1) 三反引号围栏（含语言标签）
    text = re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.DOTALL)
    # 2) 图片 ![alt](path)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    # 3) 链接文字 [text](path) —— 保留 text 本身（链接文字里的数学算正文）
    #    只去掉 URL 部分以免误判
    text = re.sub(r"\]\([^)]*\)", "]", text)
    # 4) 行内代码 `...`
    text = re.sub(r"`[^`]*`", "", text)
    return text


def check_file(path: pathlib.Path) -> list:
    problems = []
    text = path.read_text(encoding="utf-8")
    prose = strip_protected(text)

    # 换行反斜杠检查：公式换行在 md 源里必须写 \\\\（四个反斜杠），
    # 否则 Markdown 吃掉一层后 MathJax 收不到换行，多行公式挤成一行。
    # 代码围栏外、行尾反斜杠数量 >0 且不是 4 的倍数 → 告警。
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.search(r"(\\+)\s*$", line)
        if m and len(m.group(1)) % 4 != 0:
            problems.append(f"  第 {lineno} 行行尾反斜杠数 {len(m.group(1))} 会被 Markdown 吃掉一层：{line.strip()[:60]}")

    # $ 成对（$$ 也满足偶数个 $）；行内必须同行闭合
    for lineno, line in enumerate(prose.splitlines(), 1):
        n = line.count("$")
        if n % 2 == 1:
            problems.append(f"  第 {lineno} 行 $ 数量为奇数：{line.strip()[:60]}")
    if prose.count("$$") % 2 == 1:
        problems.append("  $$ 不配对")

    # 制表符矩阵残留
    if re.search(r"[┌┐└┘│]", prose):
        problems.append("  残留制表符矩阵边框（┌┐└┘│）")

    # 单反斜杠 + ASCII 标点（\; \, \: \| \{ \} \! \~）：mdBook 的 Markdown 解析器
    # 会把它们当转义符吃掉标点前的反斜杠，MathJax 收到的公式已被破坏
    # （\| → | 范数变单竖线；\, → , 冒出多余逗号；\{ → { 集合括号消失）。
    # 安全写法：\, \; → "\ "（反斜杠空格）；\| → \Vert；\{ \} → \lbrace \rbrace。
    eaten = sorted(set(re.findall(r"(?<!\\)\\[;,:|{}!~]", prose)))
    if eaten:
        problems.append(
            f"  会被 Markdown 吃掉反斜杠的写法：{' '.join(eaten)}"
            "（间距请用 \\ ，范数请用 \\Vert，集合括号请用 \\lbrace \\rbrace）")

    # }_{ ：下划线紧跟在标点 } 后面会被 Markdown 当成强调（渲染出 <em>），
    # 必须转义成 }\_{。
    if "}_{" in prose:
        problems.append("  出现 }_{：会被 Markdown 当成下划线强调，请写 }\\_{")

    # Unicode 数学字符残留
    leftover = sorted({c for c in prose if c in BANNED})
    if leftover:
        problems.append(f"  残留 Unicode 数学字符：{''.join(leftover)}")

    return problems


def main():
    files = sorted(ROOT.glob("learning-guide/**/*.md")) + [ROOT / "README.md"]
    total = 0
    for f in files:
        problems = check_file(f)
        if problems:
            total += len(problems)
            print(f"✗ {f.relative_to(ROOT)}")
            for p in problems:
                print(p)
    if total == 0:
        print(f"✅ 全部 {len(files)} 个文件 LaTeX 规范检查通过")
        return 0
    print(f"❌ 共 {total} 个问题")
    return 1


if __name__ == "__main__":
    sys.exit(main())
