# Filters

Filters modify data during execution. Callbacks must return a value and should never have side effects (no echo, no global variable mutation).

## add_filter()

```php
add_filter( string $hook_name, callable $callback, int $priority = 10, int $accepted_args = 1 )
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `$hook_name` | string | Yes | — | Name of the filter hook |
| `$callback` | callable | Yes | — | Function that receives and returns modified data |
| `$priority` | int | No | 10 | Execution order (same as `add_action`) |
| `$accepted_args` | int | No | 1 | Number of arguments passed to callback |

### Example

```php
add_filter( 'the_title', 'myplugin_prefix_title' );

function myplugin_prefix_title( $title ) {
    return 'Featured: ' . $title;
}
```

### Modifying Arrays

```php
add_filter( 'body_class', 'myplugin_add_body_class' );

function myplugin_add_body_class( $classes ) {
    if ( ! is_admin() ) {
        $classes[] = 'myplugin-theme';
    }
    return $classes;
}
```

> **Note:** Filters must always return the modified value. Forgetting `return` causes data loss.

## apply_filters()

Apply a filter to modify a value.

```php
apply_filters( string $hook_name, mixed $value, mixed ...$args )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$hook_name` | string | Yes | Name of the filter hook |
| `$value` | mixed | Yes | The value to be modified by callbacks |
| `...$args` | mixed | No | Additional arguments passed to callbacks |

### Example

```php
$output = apply_filters( 'myplugin_settings', $settings );

$post_type_args = array( /* ... */ );
$post_type_args = apply_filters( 'myplugin_post_type_args', $post_type_args );
register_post_type( 'custom_type', $post_type_args );
```

> **Note:** The first argument after `$hook_name` is always the value being filtered. Additional args follow for context.
