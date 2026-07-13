# Plugin and Content Directory Functions

Always use WordPress functions — never hardcode `wp-content` paths. Users can rename or relocate `wp-content`.

## URL Functions (for enqueueing, linking)

| Function | Returns | Example |
|----------|---------|---------|
| `plugins_url( $path, $file )` | Full URL to file in plugin directory | `plugins_url( 'js/script.js', __FILE__ )` → `example.com/wp-content/plugins/myplugin/js/script.js` |
| `plugin_dir_url( $file )` | URL of the plugin's directory | `plugin_dir_url( __FILE__ )` → `example.com/wp-content/plugins/myplugin/` |

## Path Functions (for file includes)

| Function | Returns | Example |
|----------|---------|---------|
| `plugin_dir_path( $file )` | Server path to plugin directory | `plugin_dir_path( __FILE__ )` → `/var/www/html/wp-content/plugins/myplugin/` |
| `plugin_basename( $file )` | Plugin slug (relative path) | `plugin_basename( __FILE__ )` → `myplugin/myplugin.php` |

## Theme Functions

| Function | Returns | Example |
|----------|---------|---------|
| `get_template_directory_uri()` | URL of parent theme directory | `example.com/wp-content/themes/twentytwentyfour/` |
| `get_stylesheet_directory_uri()` | URL of child/active theme | Same as above (different for child themes) |
| `get_theme_root_uri()` | URL of themes directory | `example.com/wp-content/themes/` |

## Site & WordPress Functions

| Function | Returns | Example |
|----------|---------|---------|
| `site_url()` | WordPress core URL | `example.com` or `example.com/wordpress/` |
| `home_url()` | Frontend URL (as set in Settings) | `example.com` |
| `admin_url()` | Admin directory URL | `example.com/wp-admin/` |
| `content_url()` | wp-content URL | `example.com/wp-content/` |
| `includes_url()` | wp-includes URL | `example.com/wp-includes/` |
| `wp_upload_dir()` | Array with upload paths and URLs | `wp_upload_dir()['basedir']`, `wp_upload_dir()['baseurl']` |

## Multisite Functions

| Function | Returns | Example |
|----------|---------|---------|
| `get_admin_url( $blog_id )` | Admin URL for specific site | `get_admin_url( 2 )` → site #2 admin |
| `get_site_url( $blog_id )` | Site URL for specific site | `get_site_url( 2 )` → site #2 frontend |
| `network_admin_url()` | Network admin URL | `example.com/wp-admin/network/` |
| `network_site_url()` | Network site URL | `example.com/site2/` |

## Common Patterns

```php
// Enqueue a script
wp_enqueue_script( 'my-script', plugins_url( '/js/script.js', __FILE__ ), array(), '1.0' );

// Include another PHP file
require_once plugin_dir_path( __FILE__ ) . 'includes/helper.php';

// Get upload directory URL
$upload_dir = wp_upload_dir();
$image_url  = $upload_dir['baseurl'] . '/2024/01/image.jpg';
```

## Constants (Do Not Use Directly)

These are available but should not be used directly in plugins:

| Constant | Description |
|----------|-------------|
| `WP_CONTENT_DIR` | Full server path to wp-content |
| `WP_CONTENT_URL` | Full URL to wp-content |
| `WP_PLUGIN_DIR` | Full server path to plugins directory |
| `WP_PLUGIN_URL` | Full URL to plugins directory |
| `UPLOADS` | Relative path to uploads folder (multisite only) |

> **Note:** These constants may not be set in all environments. Always use the functions above instead.
