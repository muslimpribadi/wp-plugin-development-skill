# Adding the Personal Data Exporter to Your Plugin

Register an exporter callback via `wp_privacy_personal_data_exporters` filter. Each exporter returns paginated data for a given email address.

## Exporter Callback Interface

```php
/**
 * @param string $email_address Email address to export data for
 * @param int    $page          Page number (1-based)
 * @return array {
 *     @type array  $data   Array of export items
 *     @type bool   $done   True if all data has been returned
 * }
 */
function myplugin_export_personal_data( string $email_address, int $page = 1 ): array
```

### Return Structure

| Key | Type | Description |
|-----|------|-------------|
| `$data` | array | Array of export item arrays (see structure below) |
| `$done` | bool | `true` when all data has been returned; WordPress increments page and calls again if `false` |

### Export Item Structure

```php
array(
    'group_id'    => 'myplugin-group',       // Required: unique group identifier
    'group_label' => __( 'My Plugin Data', 'text-domain' ),  // Optional: translated label
    'item_id'     => 'user-42',              // Required: unique item ID (format: type-id)
    'data'        => array(                  // Required: array of name/value pairs
        array( 'name' => 'Field Name', 'value' => 'field value' ),
    ),
)
```

### Pagination Pattern

Limit items per page to avoid timeouts. Check if there are more items:

```php
$number = 500; // Items per page
$page   = (int) $page;

// Fetch data with pagination
$results = get_comments( array(
    'author_email' => $email_address,
    'number'       => $number,
    'paged'        => $page,
    'order_by'     => 'comment_ID',
    'order'        => 'ASC',
) );

$done = count( $results ) < $number;
```

## Complete Exporter Example

```php
add_filter( 'wp_privacy_personal_data_exporters', 'myplugin_register_exporter' );

function myplugin_register_exporter( array $exporters ): array {
    $exporters['my-plugin'] = array(
        'exporter_friendly_name' => __( 'My Plugin', 'text-domain' ),
        'callback'               => 'myplugin_export_personal_data',
    );
    return $exporters;
}

function myplugin_export_personal_data( string $email_address, int $page = 1 ): array {
    $number = 500;
    $page   = (int) $page;

    $comments = get_comments( array(
        'author_email' => $email_address,
        'number'       => $number,
        'paged'        => $page,
        'order_by'     => 'comment_ID',
        'order'        => 'ASC',
    ) );

    $export_items = array();

    foreach ( $comments as $comment ) {
        $latitude  = get_comment_meta( $comment->comment_ID, 'latitude', true );
        $longitude = get_comment_meta( $comment->comment_ID, 'longitude', true );

        if ( ! empty( $latitude ) ) {
            $export_items[] = array(
                'group_id'    => 'comments',
                'group_label' => __( 'Comments', 'text-domain' ),
                'item_id'     => "comment-{$comment->comment_ID}",
                'data'        => array(
                    array( 'name' => __( 'Commenter Latitude', 'text-domain' ), 'value' => $latitude ),
                    array( 'name' => __( 'Commenter Longitude', 'text-domain' ), 'value' => $longitude ),
                ),
            );
        }
    }

    return array(
        'data' => $export_items,
        'done' => count( $comments ) < $number,
    );
}
```

## Key Notes

| Consideration | Detail |
|---------------|--------|
| Group IDs | Core provides `comments`, `posts`, etc. You can define custom group IDs |
| Item IDs | Format: `{type}-{id}` (e.g., `comment-133`). Use unique values if no natural ID exists |
| Caching | Exports are cached for 3 days then auto-deleted |
| Multiple exporters | A plugin can register multiple exporters, but most only need one |
