# Basic Shortcodes

The Shortcode API allows registering custom tags that WordPress replaces with callback output.

## register_shortcode()

```php
add_shortcode( string $tag, callable $callback )
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `$tag` | string | The shortcode tag (e.g., `'wporg'`). Used in content as `[wporg]`. |
| `$callback` | callable | Function that returns the replacement text. |

### Hook Timing

Must be registered on the `init` action hook:

```php
add_action( 'init', 'myplugin_register_shortcodes' );

function myplugin_register_shortcodes(): void {
    add_shortcode( 'wporg', 'myplugin_wporg_handler' );
}

function myplugin_wporg_handler( array $atts = [], ?string $content = null ): string {
    return '<p>WordPress.org</p>';
}
```

## remove_shortcode()

```php
remove_shortcode( string $tag )
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `$tag` | string | The shortcode tag to remove. Must match exactly. |

> **Note:** Ensure the shortcode has been registered before removing. Use a higher priority number in `add_action()` or hook into a later action.

## shortcode_exists()

```php
shortcode_exists( string $tag )
```

Returns `true` if the shortcode is registered, `false` otherwise.

## Complete Example — Self-Closing Tag

```php
add_action( 'init', 'myplugin_register_shortcodes' );

function myplugin_register_shortcodes(): void {
    add_shortcode( 'wporg', 'myplugin_wporg_handler' );
}

function myplugin_wporg_handler( array $atts = [], ?string $content = null ): string {
    return '<p>WordPress.org</p>';
}

// Remove a shortcode (e.g., from another plugin)
remove_shortcode( 'wporg' );

// Check if registered
if ( shortcode_exists( 'wporg' ) ) {
    // Do something
}
```

## Key Notes

| Consideration | Detail |
|---------------|--------|
| Return value | Callback must always `return` — never `echo` |
| Hook timing | Register on `init`, not in plugin load |
| Multiple shortcodes | Call `add_shortcode()` multiple times for different tags |
