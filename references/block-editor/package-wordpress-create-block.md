# @wordpress/create-block

Official CLI tool for scaffolding WordPress block plugins. Generates PHP, JS, CSS, and `block.json` with a zero-config build setup (inspired by `create-react-app`).

## ⚠️ Constraints & Requirements (Strict)
- **Node.js:** v20.10.0 or above required.
- **npm:** v10.2.3 or above required.
- **Output Structure:** Generates a standalone WordPress plugin folder named after the `slug`.
- **Plugin vs Theme:** Strongly recommended to pair blocks with plugins (not themes) to ensure blocks remain functional when the theme changes.

## 🚀 Quick Start
```bash
npx @wordpress/create-block@latest [options] <slug>
cd <slug>
npm start
```
*Note: The generated plugin must be manually installed/activated in WordPress.*

## 🛠️ CLI Syntax & Options

### Base Command
`npx @wordpress/create-block@latest [options] [slug]`

| Flag | Description | Default / Notes |
|------|-------------|-----------------|
| `slug` | Block name, plugin name, and output folder. | Required for non-interactive mode. |
| `--namespace <value>` | Internal block namespace (e.g., `my-plugin`). | Default: `create-block` |
| `--title <value>` | Display title for the plugin/block. | - |
| `--short-description <value>` | Brief description for metadata. | - |
| `--category <name>` | Block category in WP editor. | e.g., `common`, `widgets` |
| `--textdomain <value>` | Text domain for internationalization. | Default: matches `slug` |
| `-t, --template <name>` | Select project template. | `standard` (default), `es5`, or external package/path |
| `--variant <name>` | Block variant type. | e.g., `dynamic` (server-side rendered) |
| `--target-dir <dir>` | Override output directory name. | Default: matches `slug` |
| `--wp-scripts` / `--no-wp-scripts` | Enable/disable `@wordpress/scripts` build integration. | Enabled by default |
| `--wp-env` | Enable `@wordpress/env` for local Docker testing. | Disabled by default |
| `--no-plugin` | Scaffold block files only (no `plugin.php`). | Useful for theme development |

## 🔄 Execution Modes

### 1. Interactive Mode
Run without arguments:
```bash
npx @wordpress/create-block@latest
```
Prompts sequentially for: `slug`, `title`, `namespace`, and other options.

### 2. Quick Start (Non-Interactive)
Provide `slug` to bypass prompts:
```bash
npx @wordpress/create-block@latest my-block --namespace=my-plugin
```
- **Block Name:** `my-plugin/my-block`
- **Output Folder:** `my-block/`
- All other fields use defaults unless overridden.

### 3. External Templates
Supports custom scaffolding via npm packages or local directories:
```bash
npx @wordpress/create-block@latest --template my-custom-template-package
# or
npx @wordpress/create-block@latest --template ./path/to/local/templates
```

## 📦 Generated Project Structure & Commands
The scaffolded folder is a complete Node.js package. It includes preconfigured `package.json` scripts derived from `@wordpress/scripts`.

**Standard Commands Available:**
- `npm start`: Starts development server with file watcher.
- `npm run build`: Production build.
- `npm test`: Runs unit tests (Jest).
- `npm run lint:js`, `lint:style`: Code quality checks.

*Note: No manual configuration of webpack, Babel, or ESLint is required.*
