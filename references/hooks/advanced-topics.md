# Advanced Hook Topics

## remove_action() / remove_filter()

Remove a previously registered callback. Parameters must match the original `add_action()`/`add_filter()` call exactly.

```php
remove_action( string $hook_name, callable $callback, int $priority = 10 )
remove_filter( string $hook_name, callable $callback, int $priority = 10 )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$hook_name` | string | Yes | The hook name |
| `$callback` | callable | Yes | The exact same function reference used in `add_action()`/`add_filter()` |
| `$priority` | int | No | Must match the original priority if set |

### Example

```php
// Original registration (e.g., in a theme)
add_action( 'template_redirect', 'theme_setup_slider', 9 );

// Removal — must happen AFTER original registration
add_action( 'after_setup_theme', 'myplugin_remove_slider' );

function myplugin_remove_slider() {
    remove_action( 'template_redirect', 'theme_setup_slider', 9 );
}
```

> **Note:** Removal must occur after the original callback is registered. Use a hook with later execution than the registration hook (e.g., `after_setup_theme` if the original was in `functions.php`).

## remove_all_actions() / remove_all_filters()

Remove all callbacks from a hook.

```php
remove_all_actions( string $hook_name, int $priority = false )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$hook_name` | string | Yes | Hook to clear |
| `$priority` | int\|false | No | If set, only remove callbacks at that priority. `false` = all priorities. |

### Example

```php
remove_all_actions( 'wp_head' ); // Remove all wp_head callbacks
```

## current_action() / current_filter()

Identify which hook is currently executing inside a shared callback.

```php
current_action() // Returns string|false — name of current action
current_filter() // Returns string|false — name of current filter
```

### Example

```php
add_filter( 'the_content', 'myplugin_modify_content' );
add_filter( 'the_excerpt', 'myplugin_modify_content' );

function myplugin_modify_content( $content ) {
    switch ( current_filter() ) {
        case 'the_content':
            return '<div class="full">' . $content . '</div>';
        case 'the_excerpt':
            return strip_tags( $content ) . '...';
        default:
            return $content;
    }
}
```

## did_action()

Count how many times a hook has been triggered. Useful for running code only once.

```php
did_action( string $hook_name ): int
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$hook_name` | string | Yes | Hook name to count |
| **Returns** | int | — | Number of times the hook has fired |

### Example

```php
add_action( 'save_post', 'myplugin_handle_save' );

function myplugin_handle_save( $post_id ) {
    if ( did_action( 'save_post' ) > 1 ) {
        return; // Skip recursive calls
    }
    // Process once
}
```

## All Hook ('all')

Fire a callback on every hook execution. Useful for debugging.

```php
add_action( 'all', 'myplugin_debug_hook' );

function myplugin_debug_hook() {
    error_log( current_action() . ' | ' . current_filter() );
}
```

> **Note:** The `all` hook fires on every action AND filter. Use with caution in production — it adds overhead to every hook call.
