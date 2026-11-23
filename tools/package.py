"""Build the shareable release from the same skill files used by both marketplaces."""
import argparse
import json
from pathlib import Path
import re
import shutil
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/lumen-cbsa"
SKILL = PLUGIN / "skills/lumen-cbsa"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Release artifact directory")
    output = parser.parse_args().output
    version = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
    other = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
    if other != version or f'version: "{version}"' not in (SKILL / "SKILL.md").read_text(encoding="utf-8"):
        parser.error("版本不一致，请核对两个插件清单和 SKILL.md。")
    private_link = re.compile(r"(?:feishu\.cn|larksuite\.com|kdocs\.cn)/", re.I)
    for path in SKILL.rglob("*.md"):
        if private_link.search(path.read_text(encoding="utf-8")):
            parser.error(f"公开前请将内部原件链接替换为资料名及章节：{path.name}")
    output.mkdir(exist_ok=True, parents=True)
    archive = output / f"Lumen-CBSA-Skill-{version}.zip"
    with ZipFile(archive, "w") as bundle:
        for path in sorted(SKILL.rglob("*.md")):
            if path.is_symlink():
                raise ValueError(f"分发内容必须保存在包内：{path.name}")
            entry = ZipInfo(path.relative_to(SKILL.parent).as_posix())
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            bundle.writestr(entry, path.read_bytes())
    with ZipFile(archive) as bundle:
        for name in bundle.namelist():
            if bundle.read(name) != (SKILL.parent / name).read_bytes():
                raise ValueError(f"打包校验失败：{name}")
    guide = output / f"Lumen-CBSA-Guide-{version}.md"
    shutil.copyfile(ROOT / "使用指南.md", guide)
    print(archive, guide, sep="\n")


if __name__ == "__main__":
    main()
