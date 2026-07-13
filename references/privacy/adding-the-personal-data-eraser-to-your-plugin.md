# Adding the Personal Data Eraser to Your Plugin

Register an eraser callback via `wp_privacy_personal_data_erasers` filter. Each eraser receives a paginated email address and returns deletion status.

## Eraser Callback Interface

```php
/**
 * @param string $email_address Email address to erase data for
 * @param int    $page          Page number (1-based)
 * @return array {
 *     @type bool   $items_removed  True if any items were removed
 *     @type bool   $items_retained True if any items could not be removed
 *     @type array  $messages       Messages explaining retained items
 *     @type bool   $done           True when all data has been erased
 * }
 */
function myplugin_erase_personal_data( string $email_address, int $page = 1 ): array
```

### Return Structure

| Key | Type | Description |
|-----|------|-------------|
| `$items_removed` | bool | `true` if any items containing personal data were removed |
| `$items_retained` | bool | `true` if any items could not be removed (e.g., legal hold) |
| `$messages` | array | Array of strings explaining why items were retained |
| `$done` | bool | `true` when all data has been erased; WordPress increments page and calls again if `false` |

### Pagination Pattern

Same pattern as exporters — limit per page to avoid timeouts:

```php
$number = 500; // Items per page
$page   = (int) $page;

$results = get_comments( array(
    'author_email' => $email_address,
    'number'       => $number,
    'paged'        => $page,
    'order_by'     => 'comment_ID',
    'order'        => 'ASC',
) );

$done = count( $results ) < $number;
```

## Complete Eraser Example

```php
add_filter( 'wp_privacy_personal_data_erasers', 'myplugin_register_eraser' );

function myplugin_register_eraser( array $erasers ): array {
    $erasers['my-plugin'] = array(
        'eraser_friendly_name' => __( 'My Plugin', 'text-domain' ),
        'callback'             => 'myplugin_erase_personal_data',
    );
    return $erasers;
}

function myplugin_erase_personal_data( string $email_address, int $page = 1 ): array {
    $number = 500;
    $page   = (int) $page;

    $comments = get_comments( array(
        'author_email' => $email_address,
        'number'       => $number,
        'paged'        => $page,
        'order_by'     => 'comment_ID',
        'order'        => 'ASC',
    ) );

    $items_removed = false;

    foreach ( $comments as $comment ) {
        $latitude  = get_comment_meta( $comment->comment_ID, 'latitude', true );
        $longitude = get_comment_meta( $comment->comment_ID, 'longitude', true );

        if ( ! empty( $latitude ) ) {
            delete_comment_meta( $comment->comment_ID, 'latitude' );
            $items_removed = true;
        }

        if ( ! empty( $longitude ) ) {
            delete_comment_meta( $comment->comment_ID, 'longitude' );
            $items_removed = true;
        }
    }

    return array(
        'items_removed'  => $items_removed,
        'items_retained' => false,
        'messages'       => array(),
        'done'           => count( $comments ) < $number,
    );
}
```

## Key Notes

| Consideration | Detail |
|---------------|--------|
| Destructive process | Erasure is irreversible — only run after request confirmation |
| Email as key | All erasers use email address (supports both registered users and unregistered commenters) |
| Pagination required | Always paginate to avoid timeouts on large datasets |
| Friendly name | Used for debugging; not shown to users in the admin UI |
