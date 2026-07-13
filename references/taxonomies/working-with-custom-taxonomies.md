# Working with Custom Taxonomies

Register custom taxonomies via `register_taxonomy()` on the `init` hook. WordPress provides built-in `category` and `post_tag` — use this for any additional classification system.

## register_taxonomy()

```php
register_taxonomy( string $taxonomy, array|string $object_type, array $args = array() )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$taxonomy` | string | Yes | Taxonomy slug (lowercase, underscores for spaces). Must start with a letter. Max 32 characters in core. |
| `$object_type` | array\|string | Yes | Post types to associate (e.g., `array( 'post', 'product' )`) |
| `$args` | array | No | Configuration options (see below) |

## Arguments Reference

### Labels

Passed as an array. All labels are optional — WordPress provides defaults.

| Label Key | Purpose |
|-----------|---------|
| `name` | General name for the taxonomy (plural) |
| `singular_name` | Singular name |
| `search_items` | Search items text |
| `popular_items` | Popular items text (used in widget) |
| `all_items` | All items text |
| `parent_item` | Parent item text |
| `parent_item_colon` | Parent item colon text |
| `edit_item` | Edit item text |
| `view_item` | View item text |
| `update_item` | Update item text |
| `add_new_item` | Add new item text |
| `new_item_name` | New item name text |
| `separate_items_with_commas` | Separate items text |
| `add_or_remove_items` | Add or remove items text |
| `choose_from_most_used` | Choose from most used text |
| `not_found` | Not found text |
| `no_terms` | No terms text |
| `name_admin_bar` | Name displayed in admin bar |

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `hierarchical` | bool | `false` | Whether taxonomy is hierarchical (like categories) or flat (like tags) |
| `labels` | array | — | Label definitions |
| `show_ui` | bool | Auto | Whether to generate a default UI for managing terms |
| `show_admin_column` | bool | `false` | Display a column on the edit screen |
| `query_var` | bool\|string | `true` (slug) | Enable query variable (e.g., `?course=appetizer`) |
| `rewrite` | bool\|array | `array('slug' => $taxonomy)` | Permalink structure. Set `false` to disable |
| `capabilities` | array | — | Override default capabilities for this taxonomy |
| `default_term` | array | — | Default term: `array( 'name' => 'Uncategorized', 'description' => '' )` |
| `sort` | bool | `false` | Whether terms are sorted alphabetically |
| `public` | bool | Auto | Whether the taxonomy is publicly queryable |
| `publicly_queryable` | bool | Auto | Whether it's accessible via query vars |
| `show_in_rest` | bool | `false` | Enable REST API support |
| `show_tagcloud` | bool | Auto | Whether to show in tag cloud widget |
| `rest_controller_class` | string | — | Custom REST controller class name |

## Complete Example

```php
add_action( 'init', 'myplugin_register_course_taxonomy' );

function myplugin_register_course_taxonomy() {
    $labels = array(
        'name'              => _x( 'Courses', 'taxonomy general name', 'text-domain' ),
        'singular_name'     => _x( 'Course', 'taxonomy singular name', 'text-domain' ),
        'search_items'      => __( 'Search Courses', 'text-domain' ),
        'all_items'         => __( 'All Courses', 'text-domain' ),
        'parent_item'       => __( 'Parent Course', 'text-domain' ),
        'edit_item'         => __( 'Edit Course', 'text-domain' ),
        'update_item'     => __( 'Update Course', 'text-domain' ),
        'add_new_item'      => __( 'Add New Course', 'text-domain' ),
        'new_item_name'     => __( 'New Course Name', 'text-domain' ),
        'menu_name'         => __( 'Courses', 'text-domain' ),
    );

    $args = array(
        'hierarchical'      => true,
        'labels'            => $labels,
        'show_ui'           => true,
        'show_admin_column' => true,
        'query_var'         => true,
        'rewrite'           => array( 'slug' => 'course' ),
        'show_in_rest'      => true,
    );

    register_taxonomy( 'course', array( 'post' ), $args );
}
```

## Term Manipulation Functions

| Function | Purpose | Signature |
|----------|---------|-----------|
| `wp_insert_term()` | Create a new term | `wp_insert_term( string $term, string $taxonomy, array $args = array() )` |
| `get_term()` | Get a single term object | `get_term( int\|WP_Term $term, string $taxonomy = '' )` |
| `get_terms()` | Get multiple terms | `get_terms( array|string $args = array() )` |
| `edit_term()` | Hook fired when a term is edited | `add_action( 'edit_term', 'my_callback', 10, 3 )` |
| `edited_term_taxonomy_id()` | Hook fired after term + taxonomy edited | `add_action( 'edited_term_taxonomy_id', 'my_callback', 10, 2 )` |
| `create_term()` | Hook fired when a new term is created | `add_action( 'create_term', 'my_callback', 10, 3 )` |
| `delete_term()` | Hook fired when a term is deleted | `add_action( 'delete_term', 'my_callback', 10, 4 )` |
| `split_shared_term()` | Hook fired when a shared term is split (WP 4.2+) | `add_action( 'split_shared_term', 'my_callback', 10, 4 )` |

## Display Functions

| Function | Purpose | Signature |
|----------|---------|-----------|
| `the_terms()` | Display terms in a list | `the_terms( int $id, string $taxonomy, string $before = '', string $sep = '', string $after = '' )` |
| `wp_tag_cloud()` | Display a tag cloud | `wp_tag_cloud( array|string $args = array() )` |
| `get_the_term_list()` | Get terms as HTML (don't display) | `get_the_term_list( int $id, string $taxonomy, string $before = '', string $sep = '', string $after = '' )` |

## Archive URLs

| Taxonomy Type | Archive URL Pattern |
|---------------|-------------------|
| Hierarchical (`hierarchical => true`) | `/course/`, `/course/appetizer/`, `/course/appetizer/main-course/` |
| Flat (`hierarchical => false`) | `/course/chocolate/`, `/course/vanilla/` |

> **Note:** If `rewrite` is set to `false`, archive URLs are disabled. Use `?course=slug` query variable instead (if `query_var` is enabled).
