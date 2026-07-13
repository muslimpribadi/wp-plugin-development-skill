# Top-Level Menus

## add_menu_page()

Register a new top-level menu item in the WordPress admin sidebar.

**Hook:** `admin_menu` (priority: 999)
**Returns:** `$hook_suffix` string (for form processing)

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| $page_title | string | Yes | — | Title displayed in browser tab |
| $menu_title | string | Yes | — | Text displayed in menu |
| $capability | string | Yes | — | Minimum capability required |
| $menu_slug | string | Yes | — | Unique identifier for the page |
| $function | callable | No | `''` | Callback that renders page HTML |
| $icon_url | string | No | `''` | URL or Dashicons CSS (`dashicons-icon`) |
| $position | int | No | `null` | Menu position (10=Posts, 20=Media, etc.) |

### Example

```php
add_action( 'admin_menu', 'myplugin_register_menu' );

function myplugin_register_menu() {
    add_menu_page(
        'My Plugin',          // page_title
        'My Plugin',          // menu_title
        'manage_options',     // capability
        'my-plugin',          // menu_slug
        'myplugin_render_page', // callback
        'dashicons-admin-generic', // icon
        20                    // position
    );
}

function myplugin_render_page() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }
    ?>
    <div class="wrap">
        <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
        <?php myplugin_render_content(); ?>
    </div>
    <?php
}
```

### Menu Position Reference

| Position | Menu Item |
|----------|-----------|
| 5 | Dashboard |
| 10 | Posts |
| 15 | Media |
| 20 | Pages |
| 25 | Comments |
| 59 | (separator) |
| 60 | First custom item |

### Using a Separate PHP File for HTML

```php
add_action( 'admin_menu', 'myplugin_register_menu' );

function myplugin_register_menu() {
    add_menu_page(
        'My Plugin',
        'My Plugin',
        'manage_options',
        plugin_dir_path( __FILE__ ) . 'admin/view.php',
        null,
        'dashicons-admin-generic',
        20
    );
}
```

## remove_menu_page()

Remove a registered top-level menu item.

**Hook:** `admin_menu` (high priority, e.g. 99)

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| $menu_slug | string | Yes | The slug of the menu to remove |

### Example

```php
add_action( 'admin_menu', 'myplugin_remove_menus', 99 );

function myplugin_remove_menus() {
    remove_menu_page( 'tools.php' );
}
```

> **Note:** Use high priority (e.g. 99) to ensure the menu is registered before removal. This does not prevent direct URL access — use capability checks for security.

## Form Submission

### Pattern

1. Capture `$hook_suffix` from `add_menu_page()` return value
2. Hook into `load-$hook_suffix` for form processing (runs before HTML output)
3. Verify nonce, sanitize, and redirect on success

```php
add_action( 'admin_menu', 'myplugin_register_menu' );

function myplugin_register_menu() {
    $hook_suffix = add_menu_page(
        'My Plugin',
        'My Plugin',
        'manage_options',
        'my-plugin',
        'myplugin_render_page',
        'dashicons-admin-generic',
        20
    );

    // Process form before page renders
    add_action( "load-{$hook_suffix}", 'myplugin_handle_form' );
}

function myplugin_handle_form() {
    if ( ! isset( $_POST['myplugin_nonce'] ) ||
         ! wp_verify_nonce( $_POST['myplugin_nonce'], 'myplugin_save' ) ) {
        return;
    }

    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( 'Insufficient permissions.' );
    }

    // Process sanitized data
    $value = sanitize_text_field( $_POST['myplugin_setting'] );
    update_option( 'myplugin_setting', $value );

    wp_redirect( admin_url( 'admin.php?page=my-plugin&settings-updated=true' ) );
    exit;
}
```

### Form Action Attribute

```php
<form action="<?php echo esc_url( menu_page_url( 'my-plugin' ) ); ?>" method="post">
    <?php wp_nonce_field( 'myplugin_save', 'myplugin_nonce' ); ?>
    <!-- form fields -->
</form>
```

> **Note:** Use `esc_url()` when outputting the action attribute. `menu_page_url()` escapes and echoes by default, so use `menu_page_url( 'slug', false )` if you need the raw URL.
