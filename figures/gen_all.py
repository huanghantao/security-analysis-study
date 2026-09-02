"""一键重新生成所有配图。"""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
scripts = sorted(HERE.glob("gen_w*.py"))

failed = []
for s in scripts:
    print(f"==> {s.name}")
    r = subprocess.run([sys.executable, str(s)])
    if r.returncode != 0:
        failed.append(s.name)

print()
if failed:
    print("以下脚本失败：")
    for f in failed:
        print("  ", f)
    sys.exit(1)
print(f"全部 {len(scripts)} 个脚本完成。图片在 figures/out/")
