# Activation / Deactivation Hooks

## register_activation_hook()

Run code when a plugin is activated. Fires before any output is sent (safe for database operations, cache clearing).

```php
register_activation_hook( string $file, callable $callback )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$file` | string | Yes | Main plugin file path (usually `__FILE__`) |
| `$callback` | callable | Yes | Function to run on activation |

## register_deactivation_hook()

Run code when a plugin is deactivated. Fires before the plugin is removed from the active plugins list.

```php
register_deactivation_hook( string $file, callable $callback )
```

Same parameters as `register_activation_hook()`.

> **Note:** Deactivation hooks do NOT fire when deleting a plugin — use `uninstall.php` for that (see `uninstall-methods.md`).

## Example: CPT + Permalinks

Most common pattern: register CPT on activation and flush rewrite rules.

```php
add_action( 'init', 'myplugin_register_cpt' );

function myplugin_register_cpt() {
    register_post_type( 'book', array( 'public' => true ) );
}

register_activation_hook( __FILE__, 'myplugin_activate' );

function myplugin_activate() {
    myplugin_register_cpt(); // Ensure CPT is registered before flushing rules
    flush_rewrite_rules();
}

register_deactivation_hook( __FILE__, 'myplugin_deactivate' );

function myplugin_deactivate() {
    unregister_post_type( 'book' );
    flush_rewrite_rules();
}
```

## Common Activation Tasks

| Task | Function | Notes |
|------|----------|-------|
| Flush rewrite rules | `flush_rewrite_rules()` | Required after CPT/taxonomy registration |
| Create database tables | `dbDelta()` | See `database/creating-tables-with-plugins.md` |
| Set default options | `add_option()` / `update_option()` | Use `add_option()` to avoid overwriting existing values |
| Register cron events | `wp_schedule_event()` | See `cron/scheduling-wp-cron-events.md` |

## Common Deactivation Tasks

| Task | Function | Notes |
|------|----------|-------|
| Flush rewrite rules | `flush_rewrite_rules()` | Remove CPT/taxonomy rules from cache |
| Unschedule cron events | `wp_unschedule_event()` | See `cron/scheduling-wp-cron-events.md` |
| Delete temp files | `unlink()`, `rmdir()` | Do NOT delete options/tables — use uninstall.php for that |
