# Custom Hooks

Create extensible plugins by defining your own action and filter hooks. Prefix hook names with a unique identifier to avoid collisions.

## Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Action | `{prefix}_{description}` | `myplugin_after_settings` |
| Filter | `{prefix}_{target}_filter` | `myplugin_post_type_args` |

> **Note:** Use your plugin name or company prefix. Generic names like `email_body` risk collisions with other plugins.

## Creating an Action Hook

Use `do_action()` where another developer might want to inject behavior:

```php
// Trigger point in your plugin
do_action( 'myplugin_after_settings_page' );
```

Another plugin extends it:

```php
add_action( 'myplugin_after_settings_page', 'other_plugin_add_setting' );

function other_plugin_add_setting() {
    echo '<p>Additional setting injected here</p>';
}
```

## Creating a Filter Hook

Use `apply_filters()` to expose data for modification:

```php
// In your plugin
$settings = apply_filters( 'myplugin_export_settings', $settings );
return $settings;
```

Another plugin modifies it:

```php
add_filter( 'myplugin_export_settings', 'other_plugin_add_setting' );

function other_plugin_add_setting( $settings ) {
    $settings['include_logs'] = true;
    return $settings;
}
```

## Complete Example: Extensible Post Type Registration

```php
// Your plugin
add_action( 'init', 'myplugin_register_post_type' );

function myplugin_register_post_type() {
    $args = array(
        'public'      => true,
        'has_archive' => true,
        'supports'    => array( 'title', 'editor' ),
    );

    // Allow other plugins to modify arguments
    $args = apply_filters( 'myplugin_product_args', $args );

    register_post_type( 'product', $args );
}

// Another plugin modifies the CPT
add_filter( 'myplugin_product_args', function( $args ) {
    $args['supports'][] = 'thumbnail';
    $args['menu_icon']  = 'dashicons-cart';
    return $args;
} );
```

## Complete Example: Settings Form Extension

```php
// Your plugin renders settings form
function myplugin_render_settings() {
    // Your settings fields...

    // Allow other plugins to add fields after yours
    do_action( 'myplugin_after_settings_fields' );
}

// Another plugin adds a field
add_action( 'myplugin_after_settings_fields', 'other_plugin_add_field' );

function other_plugin_add_field() {
    echo '<tr><td>Other Plugin Setting</td></tr>';
}
```

## Best Practices

| Practice | Reason |
|----------|--------|
| Prefix all hook names | Prevents collisions with other plugins |
| Use filters for data, actions for side effects | Filters return values; actions execute behavior |
| Document your hooks | Other developers need to know which hooks exist and what they accept |
| Always pass context to filters | Include relevant data as additional arguments: `apply_filters( 'hook', $value, $context )` |
