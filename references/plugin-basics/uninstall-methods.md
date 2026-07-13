# Uninstall Methods

When a user deletes a plugin (not just deactivates), use one of these methods to clean up data permanently.

## Method 1: uninstall.php (Recommended)

Create `uninstall.php` in your plugin root. WordPress executes it automatically when the plugin is deleted.

```php
// if uninstall.php is not called by WordPress, die
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    die;
}

// Delete single-site options
delete_option( 'myplugin_options' );

// Delete site-wide options in Multisite
delete_site_option( 'myplugin_options' );

// Drop custom database table
global $wpdb;
$wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}myplugin_table" );
```

> **Note:** `WP_UNINSTALL_PLUGIN` is defined only when uninstall.php runs directly. It is NOT defined when using `register_uninstall_hook()`.

## Method 2: register_uninstall_hook()

For multisite-compatible cleanup or programmatic control:

```php
register_uninstall_hook( __FILE__, 'myplugin_uninstall' );

function myplugin_uninstall() {
    delete_option( 'myplugin_options' );
    // Note: $wpdb->query() won't work in multisite without switching blogs
}
```

> **Note:** `register_uninstall_hook()` is NOT supported for network-activated plugins. Use `uninstall.php` for multisite.

## Deactivation vs Uninstall

| Action | Deactivation Hook | Uninstall Hook / uninstall.php |
|--------|-------------------|-------------------------------|
| Flush cache/temp files | ✅ Yes | ❌ No |
| Flush permalinks | ✅ Yes | ❌ No |
| Remove options from `{$wpdb->prefix}_options` | ❌ No | ✅ Yes |
| Drop custom database tables | ❌ No | ✅ Yes |

## Multisite Considerations

Looping through all sites in a multisite network is resource-intensive:

```php
if ( is_multisite() ) {
    $blogs = get_sites();
    foreach ( $blogs as $blog ) {
        switch_to_blog( $blog->blog_id );
        delete_option( 'myplugin_options' );
        restore_current_blog();
    }
}
```

> **Warning:** Only loop through sites if absolutely necessary. Consider deleting data only for the current site or using a batch process.
