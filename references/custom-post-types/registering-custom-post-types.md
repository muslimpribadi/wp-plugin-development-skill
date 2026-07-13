# Registering Custom Post Types

Register a custom post type using `register_post_type()`. Must be called on the `init` hook (after `after_setup_theme`, before `admin_init`).

## Basic Registration

```php
add_action( 'init', 'myplugin_register_product_cpt' );

function myplugin_register_product_cpt() {
    register_post_type( 'product', array(
        'labels'      => array(
            'name'          => __( 'Products', 'myplugin' ),
            'singular_name' => __( 'Product', 'myplugin' ),
        ),
        'public'      => true,
        'has_archive' => true,
    ) );
}
```

## register_post_type() Parameters

```php
register_post_type( string $post_type, array|string $args = array() )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$post_type` | string | Yes | Machine-readable slug (max 20 chars). Must be lowercase, no spaces. Prefix to avoid conflicts (e.g., `myplugin_product`). |
| `$args` | array | No | Configuration arguments (see below). |

### Key Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `labels` | array | — | UI labels (`name`, `singular_name`, `add_new`, `edit_item`, etc.) |
| `public` | bool | `false` | Makes CPT visible in admin, REST API, and frontend |
| `has_archive` | bool/string | `false` | Enable archive page. String sets custom archive slug. |
| `supports` | array | `['title', 'editor']` | Features: `'title'`, `'editor'`, `'excerpt'`, `'thumbnail'`, `'custom-fields'`, `'page-attributes'` |
| `menu_icon` | string | — | Dashicon CSS (`dashicons-admin-post`) or image URL. Position in admin menu. |
| `menu_position` | int | `null` | Menu order (see Menu Position Reference below) |
| `show_in_rest` | bool | `false` | Enable Gutenberg REST API support |
| `rewrite` | array\|bool | `true` | Permalink structure. `array('slug' => 'products')` or `false` to disable. |

### Menu Position Reference

| Position | Menu Item |
|----------|-----------|
| 5 | Dashboard |
| 10 | Posts |
| 15 | Media |
| 20 | Pages |
| 25 | Comments |
| 59 | (separator) |
| 60+ | First custom item |

## Naming Best Practices

- **Max 20 characters** — `post_type` column in the database is VARCHAR(20)
- **Prefix your slug** — use plugin/theme namespace (e.g., `myplugin_product`) to avoid conflicts
- **Do not use `wp_` prefix** — reserved by WordPress core
- **Avoid generic names** — `product`, `event`, `movie` are likely already used

> **Conflict resolution:** Duplicate post type slugs cannot be resolved without disabling one of them. Always use a unique, prefixed name.

## Custom Permalink Slug

```php
add_action( 'init', 'myplugin_register_product_cpt' );

function myplugin_register_product_cpt() {
    register_post_type( 'product', array(
        'labels'      => array(
            'name'          => __( 'Products', 'myplugin' ),
            'singular_name' => __( 'Product', 'myplugin' ),
        ),
        'public'      => true,
        'has_archive' => true,
        'rewrite'     => array( 'slug' => 'shop/products' ),
    ) );
}
```

URL structure: `http://example.com/shop/products/product-slug/`

> **Note:** After changing rewrite rules, flush permalinks by visiting Settings → Permalinks.

## Complete Example with All Common Options

```php
add_action( 'init', 'myplugin_register_product_cpt' );

function myplugin_register_product_cpt() {
    $labels = array(
        'name'               => __( 'Products', 'myplugin' ),
        'singular_name'      => __( 'Product', 'myplugin' ),
        'add_new'            => __( 'Add New', 'myplugin' ),
        'add_new_item'       => __( 'Add New Product', 'myplugin' ),
        'edit_item'          => __( 'Edit Product', 'myplugin' ),
        'new_item'           => __( 'New Product', 'myplugin' ),
        'view_item'          => __( 'View Product', 'myplugin' ),
        'search_items'       => __( 'Search Products', 'myplugin' ),
        'not_found'          => __( 'No products found.', 'myplugin' ),
        'not_found_in_trash' => __( 'No products found in trash.', 'myplugin' ),
    );

    register_post_type( 'product', array(
        'labels'          => $labels,
        'public'          => true,
        'has_archive'     => true,
        'supports'        => array( 'title', 'editor', 'excerpt', 'thumbnail' ),
        'menu_icon'       => 'dashicons-cart',
        'menu_position'   => 20,
        'show_in_rest'    => true,
        'rewrite'         => array( 'slug' => 'shop/products' ),
    ) );
}
```
