# Plugin Header Requirements

The main PHP file must include a header comment to be recognized as a WordPress plugin.

## Minimum Field

```php
/*
 * Plugin Name: YOUR PLUGIN NAME
 */
```

## Complete Header Fields

| Field | Required | Description |
|-------|----------|-------------|
| `Plugin Name` | Yes | Displayed in the Plugins list |
| `Plugin URI` | No | Unique URL for plugin info page (not wordpress.org) |
| `Description` | No | Short description (<140 chars) shown in admin |
| `Version` | No | Plugin version number |
| `Requires at least` | No | Minimum WordPress version |
| `Requires PHP` | No | Minimum PHP version |
| `Author` | No | Author name (comma-separated for multiple) |
| `Author URI` | No | Author website or profile |
| `License` | No | License slug (e.g., `GPL v2 or later`) |
| `License URI` | No | Full license text URL |
| `Text Domain` | No | gettext domain for translations |
| `Domain Path` | No | Path to translation files (e.g., `/languages`) |
| `Network` | No | Set to `true` for network-only plugins |
| `Update URI` | No | Prevents accidental overwrites from similar-named plugins |
| `Requires Plugins` | No | Comma-separated list of required plugin slugs |

## Complete Example

```php
/*
 * Plugin Name:       My Basics Plugin
 * Plugin URI:        https://example.com/plugins/the-basics/
 * Description:       Handle the basics with this plugin.
 * Version:           1.10.3
 * Requires at least: 5.2
 * Requires PHP:      7.2
 * Author:            John Smith
 * Author URI:        https://author.example.com/
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Update URI:        https://example.com/my-plugin/
 * Text Domain:       my-basics-plugin
 * Domain Path:       /languages
 * Requires Plugins:  my-plugin, yet-another-plugin
 */
```

## Version Numbering Note

WordPress uses `version_compare()` for version checks. Be aware of PHP's comparison behavior:

| Comparison | Result | Reason |
|------------|--------|--------|
| `1.02` > `1.1` | `true` | String comparison; "0" < "1" in position 2 |
| `1.1.0` > `1.1` | `false` | Equal (trailing zero ignored) |

> **Recommendation:** Use semantic versioning (`MAJOR.MINOR.PATCH`) and always include all three parts to avoid comparison surprises.
