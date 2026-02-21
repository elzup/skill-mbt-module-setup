---
name: mbt-module-setup
description: "Set up a new MoonBit module project for npm publishing from the elzup/template-mbt-module template. Use when the user wants to create a new MoonBit module, start a new MBT project, scaffold a MoonBit-to-JavaScript package, or says 'mbt-module-setup', 'new moonbit module', 'create mbt project'. Template source is at ~/.ghq/github.com/elzup/template-mbt-module (GitHub elzup/template-mbt-module)."
---

# MoonBit Module Setup

Set up a new MoonBit module project from `elzup/template-mbt-module`. The template provides:

- MoonBit source compiled to ESM + CJS via `scripts/build.js`
- TypeScript type definitions
- Vitest test suite + MoonBit inline tests
- GitHub Actions CI (MoonBit test → Node matrix build)
- pnpm, Prettier, Renovate, Codecov

## Workflow

1. Gather project info from the user
2. Create the project (GitHub template or local copy)
3. Customize files (edit directly, no external script needed)
4. Install dependencies and verify

### Step 1: Gather Project Info

Ask the user for:

- **Module name**: MoonBit module name (e.g. `username/my-lib`)
- **npm name**: npm package name (e.g. `my-lib`)
- **GitHub repo**: e.g. `username/my-lib`
- **Description**: one-line description
- **Author**: defaults to `elzup`
- **License**: defaults to `MIT`

### Step 2: Create the Project

**Option A: GitHub template** (recommended when user wants a new GitHub repo)

```bash
gh repo create <github-repo> --template elzup/template-mbt-module --public --clone
# Then move to ghq-managed path if needed:
ghq get <github-repo>
```

**Option B: Local copy** (when user wants offline setup or no GitHub repo yet)

```bash
cp -r ~/.ghq/github.com/elzup/template-mbt-module <target-dir>
cd <target-dir>
rm -rf .git _build target node_modules .mooncakes .claude .serena
git init
```

### Step 3: Customize

Edit the following files directly in the project directory. The template uses `TODO` as placeholders.

#### 3-1. `moon.mod.json`

Set `name` to the MoonBit module name, `version` to `0.0.1`, `license` to the chosen license.

#### 3-2. `package.json`

Replace the following fields:

- `name` → npm name
- `version` → `0.0.0`
- `description` → description
- `author` → author
- `license` → license
- `repository` → `<github-repo>`
- `bugs.url` → `https://github.com/<github-repo>/issues`
- `homepage` → `https://github.com/<github-repo>#readme`

#### 3-3. `src/lib/lib.mbt`

Clear the file (empty). User will write their own code here.

#### 3-4. `src/lib/moon.pkg.json`

Replace with:

```json
{
  "link": {
    "js": {
      "exports": [],
      "format": "esm"
    }
  }
}
```

#### 3-5. `types/index.d.ts`

Clear the file (empty). User will add type definitions.

#### 3-6. `test/index.test.ts`

Replace with:

```ts
import { describe, expect, it } from 'vitest'

// import { } from '../lib/esm/index.js'

describe('TODO', () => {
  it.todo('implement tests')
})
```

#### 3-7. `readme.md`

Replace with:

```md
# <npm-name>

> <description>

## Install

\`\`\`
$ npm install <npm-name>
\`\`\`

## Usage

\`\`\`js
import { } from '<npm-name>'
\`\`\`

## License

<license>
```

#### 3-8. `.gitignore`

Ensure the file contains at least:

```
node_modules
coverage
/lib
target
_build
.mooncakes
```

### Step 4: Verify Setup

```bash
cd <project-dir>
pnpm install
moon check
```

Build will fail until the user adds actual MoonBit functions and exports. Inform the user of next steps:

1. Write MoonBit code in `src/lib/lib.mbt`
2. Add export names in `src/lib/moon.pkg.json` under `link.js.exports`
3. Add TypeScript declarations in `types/index.d.ts`
4. Write tests in `test/index.test.ts`
5. Run `pnpm build && pnpm test` to verify

## Key Files Reference

| File                         | Purpose                                          |
| ---------------------------- | ------------------------------------------------ |
| `moon.mod.json`              | MoonBit module metadata (name, version, license) |
| `src/lib/moon.pkg.json`      | JS export config (`link.js.exports` + `format`)  |
| `src/lib/lib.mbt`            | MoonBit source code                              |
| `scripts/build.js`           | Builds ESM + CJS from MoonBit source             |
| `types/index.d.ts`           | TypeScript type definitions                      |
| `test/index.test.ts`         | Vitest test suite                                |
| `package.json`               | npm package config (dual ESM/CJS exports)        |
| `.github/workflows/node.yml` | CI pipeline                                      |
