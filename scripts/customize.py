#!/usr/bin/env python3
"""Customize a freshly cloned template-mbt-module project."""

import argparse
import json
import sys
from pathlib import Path


def update_json_file(path: Path, updates: dict):
    data = json.loads(path.read_text())
    data.update(updates)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Customize MoonBit module template")
    parser.add_argument("project_dir", help="Path to the project directory")
    parser.add_argument("--module-name", required=True, help="MoonBit module name (e.g. user/my-module)")
    parser.add_argument("--npm-name", required=True, help="npm package name (e.g. my-module)")
    parser.add_argument("--author", default="elzup", help="Author name")
    parser.add_argument("--description", default="", help="Package description")
    parser.add_argument("--license", default="MIT", help="License type")
    parser.add_argument("--github-repo", default="", help="GitHub repo (e.g. elzup/my-module)")
    args = parser.parse_args()

    root = Path(args.project_dir).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)

    # 1. moon.mod.json
    moon_mod = root / "moon.mod.json"
    if moon_mod.exists():
        data = json.loads(moon_mod.read_text())
        data["name"] = args.module_name
        data["version"] = "0.0.1"
        data["license"] = args.license
        moon_mod.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print(f"  Updated {moon_mod.name}")

    # 2. package.json
    pkg = root / "package.json"
    if pkg.exists():
        data = json.loads(pkg.read_text())
        data["name"] = args.npm_name
        data["version"] = "0.0.0"
        data["description"] = args.description
        data["author"] = args.author
        data["license"] = args.license
        if args.github_repo:
            data["repository"] = args.github_repo
            data["bugs"] = {"url": f"https://github.com/{args.github_repo}/issues"}
            data["homepage"] = f"https://github.com/{args.github_repo}#readme"
        pkg.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print(f"  Updated {pkg.name}")

    # 3. Clean sample source code
    lib_mbt = root / "src" / "lib" / "lib.mbt"
    if lib_mbt.exists():
        lib_mbt.write_text("")
        print(f"  Cleaned {lib_mbt.relative_to(root)}")

    # 4. Clean moon.pkg.json exports
    moon_pkg = root / "src" / "lib" / "moon.pkg.json"
    if moon_pkg.exists():
        data = {"link": {"js": {"exports": [], "format": "esm"}}}
        moon_pkg.write_text(json.dumps(data, indent=2) + "\n")
        print(f"  Cleaned {moon_pkg.relative_to(root)}")

    # 5. Clean type definitions
    types_dts = root / "types" / "index.d.ts"
    if types_dts.exists():
        types_dts.write_text("")
        print(f"  Cleaned {types_dts.relative_to(root)}")

    # 6. Clean test file
    test_file = root / "test" / "index.test.ts"
    if test_file.exists():
        test_file.write_text(
            "import { describe, expect, it } from 'vitest'\n\n"
            "// import { } from '../lib/esm/index.js'\n\n"
            "describe('TODO', () => {\n"
            "  it.todo('implement tests')\n"
            "})\n"
        )
        print(f"  Cleaned {test_file.relative_to(root)}")

    # 7. Update readme.md
    readme = root / "readme.md"
    if readme.exists():
        readme.write_text(
            f"# {args.npm_name}\n\n"
            f"> {args.description}\n\n"
            "## Install\n\n"
            "```\n"
            f"$ npm install {args.npm_name}\n"
            "```\n\n"
            "## Usage\n\n"
            "```js\n"
            f"import {{ }} from '{args.npm_name}'\n"
            "```\n\n"
            f"## License\n\n"
            f"{args.license}\n"
        )
        print(f"  Updated {readme.name}")

    print("\nDone! Next steps:")
    print("  1. Write MoonBit code in src/lib/lib.mbt")
    print("  2. Update exports in src/lib/moon.pkg.json")
    print("  3. Add type definitions in types/index.d.ts")
    print("  4. pnpm install && pnpm build && pnpm test")


if __name__ == "__main__":
    main()
