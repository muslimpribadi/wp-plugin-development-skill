# Rendering Post Metadata

## Template Tags and Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `get_post_meta()` | mixed\|array | Core function — get meta by post ID and key |
| `get_post_custom()` | array | All custom fields for a post (key => values array) |
| `get_post_custom_values()` | array | All values for a specific meta key |
| `the_meta()` | void (echoes) | Template tag — outputs all custom fields as an HTML list |

## Usage Examples

### Get Single Value

```php
$value = get_post_meta( $post->ID, '_myplugin_value', true );
if ( ! empty( $value ) ) {
    echo esc_html( $value );
}
```

### Get All Values for a Key

```php
$values = get_post_custom_values( '_myplugin_tags', $post->ID );
// Returns array of all values stored under this key
foreach ( $values as $tag ) {
    echo '<span>' . esc_html( $tag ) . '</span>';
}
```

### Get All Custom Fields

```php
$custom = get_post_custom( $post->ID );
// Returns: [ '_myplugin_value' => ['red'], 'name' => ['John'] ]

foreach ( $custom as $key => $values ) {
    foreach ( $values as $value ) {
        echo '<p>' . esc_html( $key ) . ': ' . esc_html( $value ) . '</p>';
    }
}
```

### the_meta() Template Tag

Outputs an unordered list of all non-hidden custom fields:

```php
the_meta();
// Outputs: <ul class="post-meta"><li><span>Key:</span> Value</li></ul>
```

> **Note:** Hidden keys (prefixed with `_`) are excluded by `the_meta()`.

## Escaping Output

Meta values are stored as-is and retrieved as-is — always escape on output:

| Context | Escape Function | Example |
|---------|----------------|---------|
| HTML body | `esc_html()` | `echo esc_html( get_post_meta( $id, '_key', true ) );` |
| HTML attribute | `esc_attr()` | `echo esc_attr( get_post_meta( $id, '_key', true ) );` |
| URL attribute | `esc_url()` | `<a href="<?php echo esc_url( $url ); ?>">` |
