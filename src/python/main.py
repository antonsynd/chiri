#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

from pathlib import Path
from typing import AbstractSet, Mapping, Optional, Sequence

import pyjson5

CHIRI_VERSION: str = "0.1.0"
PACKAGE_ALIASES: AbstractSet[str] = {"build", "pkg"}


def main() -> None:
    parser: argparse.ArgumentParser = create_parser()
    args, rest = parser.parse_known_args()

    command: str = args.command

    if command == "package" or command in PACKAGE_ALIASES:
        package(args=args, rest=rest)
    elif command == "help":
        parser.print_help()
    elif command == "version":
        print(f"Chiri v{CHIRI_VERSION}")
    else:
        print(f'Unknown command "{command}"', file=sys.stderr)
        sys.exit(1)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Chiri build system.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("package", aliases=["pkg", "build"])
    subparsers.add_parser("help")
    subparsers.add_parser("version")

    return parser


def package(args: argparse.Namespace, rest: Sequence[str]) -> None:
    config_path: Optional[Path] = try_find_config()

    if not config_path:
        print(f"Cannot find chiri_config.json5", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as config_file:
        config_data = pyjson5.decode_io(config_file)
        build_system_name: str = config_data["build_system"]

        repo_root: Path = config_path.parent
        build_tools_dir: Path = repo_root / "build_tools"
        build_system_entry_point: Path = build_tools_dir / "bin" / build_system_name
        build_system_lib_dir: Path = build_tools_dir / "lib"

        if not build_system_entry_point.is_file():
            print(
                f"Build system {build_system_entry_point.name} does not exist",
                file=sys.stderr,
            )
            sys.exit(1)

        env: Mapping[str, str] = os.environ.copy()
        existing_ld_library_path: str = env.get("LD_LIBRARY_PATH", "")
        env["LD_LIBRARY_PATH"] = f"{existing_ld_library_path}:{build_system_lib_dir}"

        try:
            subprocess.run(
                args=[str(build_system_entry_point), *rest], env=env, check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Build failed with error {e}", file=sys.stderr)
            sys.exit(1)


def try_find_config() -> Optional[Path]:
    current_dir: Path = Path.cwd()

    config_path: Path = current_dir / "chiri_config.json5"

    if config_path.is_file():
        return config_path

    parent_dir: Optional[Path] = get_parent_dir_stop_at_root(p=current_dir)

    while parent_dir:
        config_path: Path = parent_dir / "chiri_config.json5"

        if config_path.is_file():
            return config_path

        parent_dir: Optional[Path] = get_parent_dir_stop_at_root(p=parent_dir)

    return None


def get_parent_dir_stop_at_root(p: Path) -> Optional[Path]:
    if p == Path("/"):
        return None

    return p.parent


if __name__ == "__main__":
    main()
