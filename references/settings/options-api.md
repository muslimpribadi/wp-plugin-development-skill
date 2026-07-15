# Options API

The Options API provides functions to store, retrieve, update, and delete WordPress options from the `{$wpdb->prefix}_options` table.

## Functions — Single Site

| Function | Purpose | Signature |
|----------|---------|-----------|
| `add_option()` | Add new option | `add_option( string $option, mixed $value, string $deprecated = '', bool $autoload = 'yes' )` |
| `get_option()` | Get option value | `get_option( string $option, mixed $default = false )` |
| `update_option()` | Update existing option | `update_option( string $option, mixed $value )` |
| `delete_option()` | Delete an option | `delete_option( string $option )` |

## Functions — Multisite (Site-Level)

| Function | Purpose | Signature |
|----------|---------|-----------|
| `add_site_option()` | Add site-level option | `add_site_option( string $option, mixed $value )` |
| `get_site_option()` | Get site-level option | `get_site_option( string $option, mixed $default = false )` |
| `update_site_option()` | Update site-level option | `update_site_option( string $option, mixed $value )` |
| `delete_site_option()` | Delete site-level option | `delete_site_option( string $option )` |

> **Note:** Site options are shared across all sites in a multisite installation. Use single-site options for per-site settings.

## Storage Patterns

### Single Value

```php
add_option( 'my_plugin_key', 'hello world' );
$value = get_option( 'my_plugin_key' );
```

### Array of Values (Recommended for Related Options)

```php
// Store as a single array option
update_option( 'my_plugin_settings', [
    'title'   => 'My Plugin',
    'enabled' => true,
    'count'   => 42,
] );

// Retrieve and access
$settings = get_option( 'my_plugin_settings' );
echo esc_html( $settings['title'] );
```

> **Best Practice:** Store related options as a single array. This reduces database transactions — one `SELECT`/`UPDATE` instead of many individual option queries.

## Key Notes

| Consideration | Detail |
|---------------|--------|
| Autoload | Third argument to `add_option()` / `update_option()`: `'yes'` (default, loaded on every page) or `'no'` (loaded only when explicitly fetched). Use `'no'` for large options not needed on every request. |
| Default value | `get_option()` returns `false` if option doesn't exist — always provide a default: `get_option( 'my_option', 'default_value' )` |
| Sanitization | Always sanitize output (`esc_html()`, `esc_attr()`) and validate/sanitize input on save |
| Transient alternatives | For temporary data, consider `set_transient()` instead of options |
