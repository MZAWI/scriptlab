import sys
from pathlib import Path
import shutil

if len(sys.argv) < 4:
    sys.exit(f"{sys.argv[0]}: insufficient arguments")

src: Path = Path(sys.argv[1])
dst: Path = Path(sys.argv[2])
ext: str = sys.argv[3]
count: int = 0
skipped: list = []

if not src.exists():
    sys.exit(f"{sys.argv[0]}: {src} does not exist")

dst.mkdir(parents=True, exist_ok=True)

for file in src.iterdir():
    if not file.suffix.lower() == f".{ext.lower()}":
        continue
    dst_file = Path(dst / file.name)
    if dst_file.exists():
        skipped.append(dst_file)
        continue
    try:
        shutil.copy2(file, dst/file.name)
        count += 1
    except Exception as e:
        print(f"Failed to copy {file.name}: {e}")

print(f"Copied {count} files")
print(f"Skipped files: {[file.name for file in skipped]}")
