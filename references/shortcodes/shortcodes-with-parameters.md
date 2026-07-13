# Shortcodes with Parameters

Shortcodes can accept named attributes (parameters) and have a 3-parameter callback signature.

## Callback Signature

```php
function my_shortcode( $atts = array(), $content = null, $tag = '' )
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `$atts` | array | Shortcode attributes (e.g., `[wporg title="WP"]` → `array('title' => 'WP')`) |
| `$content` | string\|null | Enclosed content. `null` for self-closing tags. |
| `$tag` | string | The shortcode tag name (useful for a generic handler) |

## Parsing Attributes with Defaults

```php
function wporg_shortcode( $atts = array(), $content = null, $tag = '' ) {
    // Normalize keys to lowercase
    $atts = array_change_key_case( (array) $atts, CASE_LOWER );

    // Merge with defaults — only user-provided values override
    $wporg_atts = shortcode_atts(
        array(
            'title' => 'WordPress.org',
        ),
        $atts,
        $tag
    );

    // Build output
    $output = '<div class="wporg-box">';
    $output .= '<h2>' . esc_html( $wporg_atts['title'] ) . '</h2>';

    if ( ! is_null( $content ) ) {
        $output .= apply_filters( 'the_content', $content );
    }

    $output .= '</div>';
    return $output;
}
```

## shortcode_atts()

```php
shortcode_atts( array $pairs, array $atts, string $name = '' )
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `$pairs` | array | Default attribute key/value pairs |
| `$atts` | array | User-provided attributes (from callback) |
| `$name` | string | Shortcode tag name (for error messages) |

Returns an array with only the keys defined in `$pairs`, merged with user values. Extra user keys are silently dropped.

## Complete Example

```php
add_action( 'init', 'myplugin_register_shortcodes' );

function myplugin_register_shortcodes() {
    add_shortcode( 'wporg', 'myplugin_wporg_handler' );
}

/**
 * [wporg title="WordPress.org"]Content[/wporg]
 *
 * @param array  $atts    Shortcode attributes. Default empty.
 * @param string $content Shortcode content. Default null.
 * @param string $tag     Shortcode tag (name). Default empty.
 * @return string Shortcode output.
 */
function myplugin_wporg_handler( $atts = array(), $content = null, $tag = '' ) {
    // Normalize attribute keys to lowercase
    $atts = array_change_key_case( (array) $atts, CASE_LOWER );

    // Set defaults and merge with user attributes
    $wporg_atts = shortcode_atts(
        array(
            'title' => 'WordPress.org',
        ),
        $atts,
        $tag
    );

    // Build output — always escape
    $o = '<div class="wporg-box">';
    $o .= '<h2>' . esc_html( $wporg_atts['title'] ) . '</h2>';

    if ( ! is_null( $content ) ) {
        $o .= apply_filters( 'the_content', $content );
    }

    $o .= '</div>';
    return $o;
}
```

## Key Notes

| Consideration | Detail |
|---------------|--------|
| No enforcement | Shortcodes have no schema — users can provide any attributes or none at all |
| Defaults always set | Always call `shortcode_atts()` to establish defaults before using values |
| Case sensitivity | Use `array_change_key_case()` if you want case-insensitive attribute matching |
| Security | Escape all output (`esc_html()`, `esc_attr()`) before returning |
