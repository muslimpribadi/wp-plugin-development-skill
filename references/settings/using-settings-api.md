# Using Settings API

## Registration Flow

All registration functions (`register_setting()`, `add_settings_section()`, `add_settings_field()`) must be called on the `admin_init` action hook.

### Step 1 — Register Setting

```php
register_setting( string $option_group, string $option_name, array $args = array() )
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `$option_group` | string | Group name (used by `settings_fields()` and `options.php`) |
| `$option_name` | string | Database option key to store the value |
| `$args` | array | Optional: `type`, `sanitize_callback`, `default`, `show_in_rest` |

### Step 2 — Add Section

```php
add_settings_section( string $id, string $title, callable $callback, string $page, array $args = array() )
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `$id` | string | Unique section identifier (used in HTML `id`) |
| `$title` | string | Section heading (use `__()` for i18n) |
| `$callback` | callable | Function that outputs section description text |
| `$page` | string | Settings page slug (e.g., `'reading'`, `'my-page'`) |
| `$args` | array | Optional extra arguments passed to callback |

### Step 3 — Add Field

```php
add_settings_field( string $id, string $title, callable $callback, string $page, string $section = 'default', array $args = array() )
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `$id` | string | Unique field identifier (used in HTML `id`) |
| `$title` | string | Field label |
| `$callback` | callable | Function that outputs the form control |
| `$page` | string | Settings page slug |
| `$section` | string | Section to place field in (`'default'` if omitted) |
| `$args` | array | Optional: `label_for`, `class`, custom keys passed to callback |

### Step 4 — Render the Page

```php
// In your page callback function:
settings_errors();                              // Display messages
?>
<form action="options.php" method="post">
    <?php settings_fields( 'my_group' ); ?>     // Nonce + hidden fields
    <?php do_settings_sections( 'my-page' ); ?>  // Render all sections/fields
    <?php submit_button(); ?>
</form>
```

## Complete Minimal Example

```php
add_action( 'admin_init', 'myplugin_register_settings' );

function myplugin_register_settings() {
    register_setting( 'myplugin_group', 'myplugin_option', array(
        'sanitize_callback' => 'sanitize_text_field',
    ) );

    add_settings_section(
        'myplugin_section',
        __( 'My Plugin Settings', 'text-domain' ),
        '__return_empty_string',  // No description text
        'myplugin-page'
    );

    add_settings_field(
        'myplugin_key',
        __( 'API Key', 'text-domain' ),
        'myplugin_render_api_key_field',
        'myplugin-page',
        'myplugin_section'
    );
}

function myplugin_render_api_key_field() {
    $value = get_option( 'myplugin_option' );
    echo '<input type="text" name="myplugin_option" value="' . esc_attr( $value ) . '" />';
}
```

## Getting Settings

```php
$value = get_option( 'my_plugin_option', 'default_value' );
```

> **Note:** `get_option()` returns `false` if the option doesn't exist. Always provide a default value.
