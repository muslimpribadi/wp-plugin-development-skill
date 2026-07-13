# Best Practices

## Naming Collisions

All globally accessible code should be prefixed with a unique identifier (5+ characters) to avoid conflicts.

### Prefix Rules

| Must Prefix | Example |
|-------------|---------|
| Functions | `myplugin_init()` |
| Classes/Interfaces/Traits | `class MyPlugin_Core {}` |
| Namespaces | `namespace MyPlugin;` |
| Global variables | `$myplugin_options = array();` |
| Options/Transients | `update_option( 'myplugin_settings', $data );` |

### Reserved Prefixes (Do Not Use)

| Prefix | Reason |
|--------|--------|
| `__` (double underscore) | WordPress translation functions |
| `wp_` | Reserved by WordPress core |
| `_` (single underscore) | WordPress internal naming convention |
| `Woo` / `WC` | Reserved by WooCommerce |

### Existence Checks

```php
if ( ! function_exists( 'myplugin_init' ) ) {
    function myplugin_init() { /* ... */ }
}

if ( ! class_exists( 'MyPlugin_Core' ) ) {
    class MyPlugin_Core { /* ... */ }
}
```

> **Warning:** `function_exists()`/`class_exists()` guards should only be used for shared libraries. If another plugin's function loads first and has the same name, your plugin will silently break.

## File Organization

Root-level structure:

```
/plugin-name/
    plugin-name.php          # Main file (contains header)
    uninstall.php            # Cleanup on delete
    /languages/              # Translation files
    /includes/               # Core classes/functions
    /admin/                  # Admin-only code
        js/
        css/
    /public/                 # Frontend code
        js/
        css/
```

## Conditional Loading

Separate admin and frontend code:

```php
if ( is_admin() ) {
    require_once __DIR__ . '/admin/plugin-admin.php';
} else {
    require_once __DIR__ . '/public/plugin-public.php';
}
```

> **Note:** `is_admin()` only checks if the admin bar is shown, not user capability. Always add capability checks inside your code.

## Security: Prevent Direct File Access

At the top of every PHP file (except those meant to be directly accessed):

```php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
```

## Architecture Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Single file, functions | Small plugins, one-off scripts | Simple shortcode plugin |
| Single file, class | Medium plugins with multiple features | Plugin with admin page + frontend logic |
| Main file + class files | Large plugins, team projects | Full-featured plugin with separate admin/public modules |
