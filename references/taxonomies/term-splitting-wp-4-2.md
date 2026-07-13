# Term Splitting (WordPress 4.2+)

## Background

Prior to WordPress 4.2, terms in different taxonomies with the same slug shared a single term ID (e.g., a tag and category with slug "news" had the same term ID). Starting with 4.2, updating one of these shared terms triggers a split — the updated term receives a new term ID.

## Hook: `split_shared_term`

Fired when a shared term is assigned a new term ID. Use this to update stored references.

```php
add_action( 'split_shared_term', 'myplugin_update_stored_term_ids', 10, 4 );

function myplugin_update_stored_term_ids( int $term_id, int $new_term_id, int $term_taxonomy_id, string $taxonomy ): void {
    // Check if this taxonomy matters to your plugin
    if ( 'post_tag' !== $taxonomy ) {
        return;
    }

    // Update stored option/array with new term ID
    $featured_tags = get_option( 'featured_tags', array() );
    $found_key = array_search( $term_id, $featured_tags, true );

    if ( false !== $found_key ) {
        $featured_tags[ $found_key ] = $new_term_id;
        update_option( 'featured_tags', $featured_tags );
    }
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `$term_id` | int | ID of the formerly shared term |
| `$new_term_id` | int | ID of the new term created for this taxonomy |
| `$term_taxonomy_id` | int | Term_taxonomy row affected by the split |
| `$taxonomy` | string | Taxonomy name |

## Updating Post Meta References

```php
add_action( 'split_shared_term', 'myplugin_update_post_meta_term_ids', 10, 4 );

function myplugin_update_post_meta_term_ids( int $term_id, int $new_term_id, int $term_taxonomy_id, string $taxonomy ): void {
    $page_ids = get_posts( array(
        'post_type'   => 'page',
        'fields'      => 'ids',
        'meta_key'    => '_related_term_id',
        'meta_value'  => $term_id,
    ) );

    if ( $page_ids ) {
        foreach ( $page_ids as $id ) {
            update_post_meta( $id, '_related_term_id', $new_term_id, $term_id );
        }
    }
}
```

## Utility Functions

| Function | Purpose | Signature |
|----------|---------|-----------|
| `wp_get_split_term()` | Get new term ID for a split term | `wp_get_split_term( int $old_term_id, string $taxonomy )` |
| `wp_get_split_terms()` | Get all split terms for an old term ID | `wp_get_split_terms( int $old_term_id )` |

### Usage Example — Validation on Plugin Update

```php
function myplugin_validate_stored_term_ids() {
    $tag_ids = get_option( 'featured_tags', array() );

    foreach ( $tag_ids as $index => $tag_id ) {
        $new_id = wp_get_split_term( $tag_id, 'post_tag' );
        if ( $new_id ) {
            $tag_ids[ $index ] = $new_id;
        }
    }

    update_option( 'featured_tags', $tag_ids );
}
```

## Key Notes

| Consideration | Detail |
|---------------|--------|
| Preferred method | Use the `split_shared_term` hook for real-time updates |
| Fallback method | Use `wp_get_split_term()` to check and fix stored IDs (e.g., on plugin update) |
| Scope | Only affects terms that shared an ID across taxonomies — most installations are unaffected |
| Best practice | Avoid storing raw term IDs in options/meta when possible; use slugs or term taxonomy combinations instead |
