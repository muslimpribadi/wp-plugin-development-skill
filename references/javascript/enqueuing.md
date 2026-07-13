# Script Enqueuing

## wp_enqueue_script()

Register and enqueue a script on the page. Must be called from an action hook — never directly in plugin code.

```php
wp_enqueue_script( string $handle, string $src = '', array $deps = array(), string|false $ver = false, bool|array $args = array() )
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `$handle` | string | Yes | — | Unique name for the script (used as ID and in `wp_localize_script()`) |
| `$src` | string | No | `''` | Full URL or path to the script file. Use `plugins_url()` or `site_url()` |
| `$deps` | array | No | `array()` | Dependencies — scripts that must load first (e.g., `array('jquery')`) |
| `$ver` | string\|false | No | `false` | Version number for cache busting. `false` uses WordPress version |
| `$args` | bool\|array | No | `false` | If `true`: loads in footer. Array: supports `'in_footer' => true` and `'strategy' => 'defer'|'async'` (WP 6.3+) |

### Hook-Based Enqueuing

| Context | Hook | Parameter Passed |
|---------|------|-----------------|
| Admin pages | `admin_enqueue_scripts` | `$hook` (current page filename) — use to conditionally enqueue |
| Frontend pages | `wp_enqueue_scripts` | None — use template tags (`is_home()`, `is_single()`) |
| Login page | `login_enqueue_scripts` | None |

```php
add_action( 'admin_enqueue_scripts', 'myplugin_enqueue' );

function myplugin_enqueue( $hook ) {
    if ( 'edit.php' !== $hook && 'post.php' !== $hook ) {
        return;
    }
    wp_enqueue_script( 'my-script', plugins_url( '/js/script.js', __FILE__ ), array( 'jquery' ), '1.0', true );
}
```

## wp_register_script()

Register a script without enqueueing it. Use when another plugin/theme might also need to reference the same script:

```php
wp_register_script( string $handle, string $src = '', array $deps = array(), string|false $ver = false, bool|array $args = array() )
```

> **Note:** `wp_enqueue_script()` alone is sufficient for most cases. Only use `wp_register_script()` when you need to share a handle across multiple plugins or conditionally enqueue based on another plugin's decision.

## Script Loading Strategies (WP 6.3+)

Specify loading behavior via the `$args` array:

```php
wp_enqueue_script( 'my-script', plugins_url( '/js/script.js', __FILE__ ), array(), '1.0', array( 'strategy' => 'defer' ) );
```

| Strategy | Description | Execution Timing |
|----------|-------------|-----------------|
| `defer` | Execute after DOM parses, before `DOMContentLoaded` | In order of declaration |
| `async` | Execute as soon as downloaded, order not guaranteed | May execute before or after DOM ready |

> **Note:** WordPress resolves the final strategy based on the dependency tree. The chosen strategy will never be stricter than your intended one.

## wp_localize_script()

Pass PHP data to JavaScript by creating a global object:

```php
wp_localize_script( string $handle, string $object_name, array $l10n )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$handle` | string | Yes | The script handle this data belongs to |
| `$object_name` | string | Yes | Global JS object name (e.g., `my_ajax_obj`) |
| `$l10n` | array | Yes | Key-value pairs passed to JavaScript |

### Example — AJAX URL + Nonce

```php
wp_localize_script(
    'ajax-script',
    'my_ajax_obj',
    array(
        'ajax_url' => admin_url( 'admin-ajax.php' ),
        'nonce'    => wp_create_nonce( 'title_example' ),
    )
);
```

Access in JavaScript: `my_ajax_obj.ajax_url`, `my_ajax_obj.nonce`

> **Note:** The object is global to the page, not scoped to a specific script. Choose unique names to avoid collisions.

## wp_dequeue_script() / wp_deregister_script()

Remove or unregister scripts:

```php
wp_dequeue_script( string $handle );   // Remove from queue (prevents loading)
wp_deregister_script( string $handle ); // Unregister completely
```

```php
add_action( 'wp_enqueue_scripts', 'myplugin_remove_jquery_migrate' );

function myplugin_remove_jquery_migrate() {
    wp_dequeue_script( 'jquery-migrate' );
}
```
