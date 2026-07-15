# @wordpress/scripts

Official build tool and CLI for WordPress block development. Provides a zero-config webpack setup with optimized defaults for production and development.

## ⚠️ Constraints & Requirements (Strict)
- **Node.js:** Long-term support (LTS) version required.
- **ESLint v10:** Flat config (`eslint.config.*`) is now default. Legacy `.eslintrc.*` fallback is deprecated.
- **E2E Testing:** Uses Playwright by default. Test files must be in `/specs` with `.test` or `.spec` suffix.
- **Entry Point Resolution:** 
  1. Scans `src/` for `block.json` files → uses `script`, `editorScript`, etc. fields as entry points.
  2. Fallback: `src/index.js` (supports `.jsx`, `.ts`, `.tsx`).
  3. Manual override: Pass file paths directly to CLI.

## 🛠️ Master Command Reference

| Category | Command | Alias | Description & Usage |
|----------|---------|-------|---------------------|
| **Build** | `build` | - | Production build. Exits after single run. Supports incremental builds via `start`. |
| | `start` | - | Development build with file watcher. Auto-reloads on changes. |
| | `plugin-zip` | - | Creates a distributable `.zip` for WordPress plugins. |
| | `build-blocks-manifest` | - | Generates `blocks-manifest.php` from all `block.json` files for performance optimization (WP 6.7+). |
| **Linting** | `lint:js` | - | ESLint check for `.js`, `.jsx`, `.ts`, `.tsx`. |
| | `lint:style` | `lint-css` | Stylelint check for CSS, PCSS, SCSS. |
| | `lint:pkg-json` | - | Validates `package.json` against WP standards. |
| | `lint:md:docs` | - | Markdownlint check for `.md` files. |
| **Formatting** | `format` | - | Prettier formatting for JS, JSON, TS, YAML. Ignores `build/`, `node_modules/`. |
| **Testing** | `test-unit-js` | `test:unit` | Jest runner. Looks in `__tests__/`, `test/`, or `.test.js` files. |
| | `test-e2e` | `test-playwright` | Playwright runner for end-to-end tests. |
| **Utility** | `check-engines` | - | Validates Node/npm versions against `package.json`. |
| | `check-licenses` | - | Validates dependency licenses (GPLv2 compatible). |
| | `packages-update` | - | Updates all `@wordpress/*` packages to latest. Use `--dist-tag=wp-X.X` for specific WP versions. |

## 🔧 CLI Flags & Options

### Build & Start Flags
| Flag | Description | Default / Notes |
|------|-------------|-----------------|
| `--source-path <dir>` | Override source directory. | `.` (root) if files passed, otherwise `src/` |
| `--output-path <dir>` | Override build output directory. | `build/` |
| `--webpack-copy-php` | Copies all PHP files from source to output. | Default: only copies files referenced in `block.json` |
| `--blocks-manifest` | Generates PHP blocks manifest during build. | Useful for `wp_register_block_types_from_metadata_collection()` |
| `--webpack-no-externals` | Disables asset generation & default externals list. | Use for non-plugin builds |
| `--hot` | Enables Fast Refresh (Dev only). | Requires `SCRIPT_DEBUG` in WP & Gutenberg plugin installed |
| `--webpack-bundle-analyzer` | Visualizes bundle size via treemap. | - |

### Test Flags
| Flag | Description |
|------|-------------|
| `--watch` | Runs tests in watch mode (auto-re-run on change). |
| `--help` | Prints Jest/Playwright CLI options. |
| `--debug` / `--inspect-brk` | Enables Node inspector for debugging in Chrome/VS Code. |

### Plugin-Zip Flags
| Flag | Description |
|------|-------------|
| `--root-folder <name>` | Sets root directory name inside the zip. |
| `--no-root-folder` | Extracts files directly to target directory (no wrapper folder). |

## 📦 Entry Point & Asset Handling

### CSS Import Behavior
When importing styles in JS (e.g., `import './index.scss'`):
- **Editor Styles:** Bundled into `[entry-name].css` (used only in Gutenberg editor).
- **Frontend/Global Styles:** Imported via `style.css` → bundled into `[entry-name]-style-index.css`.
- ⚠️ **Constraint:** Do not name entry points using the word `style` to avoid build conflicts.

### Static Assets (Fonts & Images)
- Webpack automatically handles fonts (`woff`, `woff2`, `eot`, `ttf`, `otf`) and images (`png`, `jpg`, `gif`, `svg`, `webp`).
- Reference paths relative to the CSS/JS file processing them.

### SVG Handling
- Import as URL: `import starUrl from './star.svg'`
- Import as React Component: `import { ReactComponent as Star } from './star.svg'`

## ⚙️ Advanced Configuration (Webpack)
To override defaults, create `webpack.config.js` in the project root.
```javascript
const defaultConfig = require('@wordpress/scripts/config/webpack.config');

module.exports = {
    ...defaultConfig,
    module: {
        ...defaultConfig.module,
        rules: [
            ...defaultConfig.module.rules,
            // Add custom rules here (e.g., TOML parser)
        ],
    },
};
```
- ⚠️ Always use `wp-scripts build/start` commands. Never run `webpack` directly to ensure environment variables and defaults remain consistent.
