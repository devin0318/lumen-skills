"""Install the local Lumen CBSA skill from a clone, or fast-forward that clone."""
import argparse
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
NAME = "lumen-cbsa"
SOURCE = ROOT / "plugins" / NAME / "skills" / NAME
LOCATIONS = {
    "codex": ".agents/skills",
    "claude-code": ".claude/skills",
    "cursor": ".cursor/skills",
    "gemini": ".gemini/skills",
    "deepseek-harness": ".dsh/skills",
}


def git(*args, env=None):
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], env=env, text=True
    ).strip()


def check_clone():
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT:
        raise ValueError("请在 lumen-skills 的独立 Git 克隆中运行。")
    url = git("remote", "get-url", "origin").removesuffix(".git")
    if url not in {
        "https://gitee.com/devin0318/lumen-skills",
        "git@gitee.com:devin0318/lumen-skills",
        "ssh://git@gitee.com/devin0318/lumen-skills",
        "https://github.com/devin0318/lumen-skills",
        "git@github.com:devin0318/lumen-skills",
        "ssh://git@github.com/devin0318/lumen-skills",
    }:
        raise ValueError("origin 需要指向 devin0318/lumen-skills。")
    if git("branch", "--show-current") != "main":
        raise ValueError("请使用跟踪正式发布内容的 main 分支。")


def update():
    if git("status", "--porcelain"):
        raise ValueError("仓库中有本地改动。请先自行处理，再更新。")
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    git("fetch", "--quiet", "origin", "refs/heads/main", env=env)
    target = git("rev-parse", "FETCH_HEAD")
    # Resolve the fetched revision once. Only an intact, forward release may replace it.
    if subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor",
                       "HEAD", target], check=False).returncode:
        raise ValueError("本地和远端版本有分歧，请人工核对。")
    relative = SOURCE.relative_to(ROOT).as_posix()
    for required in ("SKILL.md", "references/术语.md"):
        git("cat-file", "-e", f"{target}:{relative}/{required}")
    git("merge", "--ff-only", "--quiet", target)
    print("已同步正式发布分支；新开对话并引用 lumen-cbsa help 核对版本。")


def install(agent):
    if not (SOURCE / "SKILL.md").is_file():
        raise ValueError("当前克隆缺少 lumen-cbsa/SKILL.md，请检查下载来源。")
    dest = Path.home() / LOCATIONS[agent] / NAME
    if os.path.lexists(dest):
        if dest.resolve() == SOURCE:
            print(f"已连接 {dest}")
            return
        raise ValueError(f"目标已有另一份安装，请按使用指南先移出或卸载：{dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        # A junction needs no developer mode. Supply paths via environment variables.
        env = {**os.environ, "LUMEN_DEST": str(dest), "LUMEN_SOURCE": str(SOURCE)}
        subprocess.run(["cmd.exe", "/d", "/v:off", "/c",
                        'mklink /J "%LUMEN_DEST%" "%LUMEN_SOURCE%"'], env=env, check=True)
    else:
        dest.symlink_to(SOURCE, target_is_directory=True)
    if not (dest / "SKILL.md").is_file():
        raise ValueError(f"未能从 {dest} 读取 Skill。")
    print(f"已连接 {dest}。新开对话并引用 lumen-cbsa help。")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    actions.add_parser("install").add_argument("agent", choices=LOCATIONS)
    actions.add_parser("update")
    args = parser.parse_args()
    check_clone()
    if args.action == "update":
        update()
    else:
        install(args.agent)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(str(error))
