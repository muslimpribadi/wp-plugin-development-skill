# Working with Custom Post Types

## Template Files

WordPress uses template hierarchy for custom post types. Create these files in your theme:

| Template | Use Case |
|----------|----------|
| `single-{post_type}.php` | Single post view |
| `archive-{post_type}.php` | Archive listing |
| `taxonomy-{taxonomy}.php` | Custom taxonomy term archive |

**Example:** For CPT slug `product`, create `single-product.php` and `archive-product.php`.

### Conditional Check

```php
is_post_type_archive( 'product' );   // Returns true on product archive page
post_type_archive_title();           // Echoes/archive title of the current post type archive
```

## Querying by Post Type

Use `WP_Query` with the `post_type` parameter:

```php
$args = array(
    'post_type'      => 'product',
    'posts_per_page' => 10,
);
$loop = new WP_Query( $args );

if ( $loop->have_posts() ) {
    while ( $loop->have_posts() ) {
        $loop->the_post();
        ?>
        <div class="entry-content">
            <?php the_title(); ?>
            <?php the_content(); ?>
        </div>
        <?php
    }
    wp_reset_postdata();
}
```

### Query Multiple Post Types

```php
$args = array(
    'post_type'      => array( 'product', 'service' ),
    'posts_per_page' => 20,
);
```

## Altering the Main Query

Use `pre_get_posts` to modify queries before they run. This is more efficient than multiple `WP_Query` calls.

```php
add_action( 'pre_get_posts', 'myplugin_add_cpts_to_home' );

function myplugin_add_cpts_to_home( $query ) {
    if ( is_home() && $query->is_main_query() ) {
        $query->set( 'post_type', array( 'post', 'page', 'product' ) );
    }
}
```

### Key Conditions for `pre_get_posts`

| Condition | Purpose |
|-----------|---------|
| `$query->is_main_query()` | Ensure you're modifying the primary query, not a sidebar/widget query |
| `is_home()` | Target the blog posts page |
| `is_admin()` | Admin area queries (use sparingly) |
| `! is_admin()` | Frontend only |

### Exclude Post Types from Main Query

```php
add_action( 'pre_get_posts', 'myplugin_exclude_cpts' );

function myplugin_exclude_cpts( $query ) {
    if ( ! is_admin() && $query->is_main_query() && is_home() ) {
        $query->set( 'post_type', array( 'post' ) );
    }
}
```

## Template Hierarchy Order

When WordPress renders a custom post type template, it checks in this order:

**Single post:**
1. `single-{post_type}.php`
2. `single.php`
3. `singular.php`
4. `index.php`

**Archive:**
1. `archive-{post_type}.php`
2. `archive.php`
3. `index.php`
