# Sub-Menus

## add_submenu_page()

Register a submenu item under an existing top-level menu.

**Hook:** `admin_menu` (priority: 999)
**Returns:** `$hook_suffix` string (for form processing)

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| $parent_slug | string | Yes | — | Slug of the parent menu |
| $page_title | string | Yes | — | Title displayed in browser tab |
| $menu_title | string | Yes | — | Text displayed in submenu |
| $capability | string | Yes | — | Minimum capability required |
| $menu_slug | string | Yes | — | Unique identifier for the page |
| $function | callable | No | `''` | Callback that renders page HTML |

### Example

```php
add_action( 'admin_menu', 'myplugin_register_submenus' );

function myplugin_register_submenus() {
    add_submenu_page(
        'edit.php',           // parent slug (Posts)
        'My Plugin Settings', // page_title
        'Settings',           // menu_title
        'manage_options',     // capability
        'my-plugin-settings', // menu_slug
        'myplugin_render_settings' // callback
    );
}

function myplugin_render_settings() {
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

## Predefined Sub-Menu Helpers

WordPress provides helper functions for built-in top-level menus. Each returns `$hook_suffix`.

| Function | Parent Slug | Parent Menu |
|----------|-------------|-------------|
| `add_dashboard_page()` | `index.php` | Dashboard |
| `add_posts_page()` | `edit.php` | Posts |
| `add_media_page()` | `upload.php` | Media |
| `add_pages_page()` | `edit.php?post_type=page` | Pages |
| `add_comments_page()` | `edit-comments.php` | Comments |
| `add_theme_page()` | `themes.php` | Appearance |
| `add_plugins_page()` | `plugins.php` | Plugins |
| `add_users_page()` | `users.php` | Users |
| `add_management_page()` | `tools.php` | Tools |
| `add_options_page()` | `options-general.php` | Settings |

### Custom Post Type Parent Slugs

```php
// For a CPT registered with 'menu_slug' => 'edit.php?post_type=product'
add_submenu_page(
    'edit.php?post_type=product',  // parent slug
    'Product Settings',             // page_title
    'Settings',                     // menu_title
    'manage_options',               // capability
    'product-settings',             // menu_slug
    'myplugin_render_product_settings'
);
```

## add_*_page() Helpers

Use these for common cases instead of `add_submenu_page()` directly:

```php
// Adds submenu under "Posts"
add_posts_page(
    'My Post Tools',      // page_title
    'Tools',              // menu_title
    'edit_posts',         // capability
    'my-post-tools',      // menu_slug
    'myplugin_render_tools'
);

// Adds submenu under "Settings"
add_options_page(
    'My Plugin Options',  // page_title
    'My Plugin',          // menu_title
    'manage_options',     // capability
    'my-plugin-options',  // menu_slug
    'myplugin_render_options'
);
```

## remove_submenu_page()

Remove a registered submenu item.

**Hook:** `admin_menu` (priority: 99)

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| $parent_slug | string | Yes | Parent menu slug |
| $menu_slug | string | Yes | Submenu slug to remove |

### Example

```php
add_action( 'admin_menu', 'myplugin_remove_submenus', 99 );

function myplugin_remove_submenus() {
    remove_submenu_page( 'edit.php', 'edit.php?post_format=aside' );
}
```

## Form Submission

Capture `$hook_suffix` from `add_submenu_page()` and use `load-$hook_suffix`:

```php
add_action( 'admin_menu', 'myplugin_register_submenus' );

function myplugin_register_submenus() {
    $hook_suffix = add_submenu_page(
        'tools.php',
        'My Plugin Tools',
        'Tools',
        'manage_options',
        'my-plugin-tools',
        'myplugin_render_tools'
    );

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

    wp_redirect( admin_url( 'admin.php?page=my-plugin-tools&settings-updated=true' ) );
    exit;
}
```

### Form Action Attribute

```php
<form action="<?php echo esc_url( menu_page_url( 'my-plugin-tools' ) ); ?>" method="post">
    <?php wp_nonce_field( 'myplugin_save', 'myplugin_nonce' ); ?>
    <!-- form fields -->
</form>
```

> **Note:** `menu_page_url()` escapes and echoes by default. Use `menu_page_url( 'slug', false )` to return without echoing.
