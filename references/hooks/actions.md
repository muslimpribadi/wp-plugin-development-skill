# Actions

Actions execute a callback at a specific point in WordPress execution. Callbacks do not return values.

## add_action()

```php
add_action( string $hook_name, callable $callback, int $priority = 10, int $accepted_args = 1 )
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `$hook_name` | string | Yes | — | Name of the action hook to attach to |
| `$callback` | callable | Yes | — | Function or method to execute |
| `$priority` | int | No | 10 | Execution order (lower = earlier). Typical range: 1–20. Default priority callbacks run first, then higher numbers. |
| `$accepted_args` | int | No | 1 | Number of arguments to pass from `do_action()` to callback |

### Example

```php
add_action( 'init', 'myplugin_init_callback' );

function myplugin_init_callback(): void {
    // Runs on WordPress init
}
```

### Priority Order

| Callback | Priority | Execution Order |
|----------|----------|-----------------|
| `mycallback_early` | 9 | 1st (before default) |
| `mycallback_default` | 10 (default) | 2nd |
| `mycallback_late` | 11 | 3rd (after default) |

When priority is equal, execution order follows registration order.

### Passing Arguments

If the action passes multiple arguments, specify `$accepted_args`:

```php
// Hook receives: $post_id, $post object
add_action( 'save_post', 'myplugin_save_handler', 10, 2 );

function myplugin_save_handler( int $post_id, WP_Post $post ): void {
    // Process post data
}
```

> **Note:** The callback function must declare the same number of parameters as `$accepted_args`.

## do_action()

Trigger an action hook.

```php
do_action( string $hook_name, mixed ...$args )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$hook_name` | string | Yes | Name of the action to trigger |
| `...$args` | mixed | No | Arguments passed to callback functions |

### Example

```php
do_action( 'myplugin_before_export' );

do_action( 'myplugin_user_registered', $user_id, $userdata );
```
