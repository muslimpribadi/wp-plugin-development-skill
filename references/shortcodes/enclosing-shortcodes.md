# Enclosing Shortcodes

Enclosing shortcodes wrap content that the callback can manipulate.

## Syntax

```
[wporg]Content to manipulate[/wporg]
```

The handler receives enclosed text in the `$content` parameter:

```php
function wporg_shortcode( array $atts = [], ?string $content = null ): string {
    // Process $content and return replacement
    return '<div class="box">' . $content . '</div>';
}
add_shortcode( 'wporg', 'wporg_shortcode' );
```

## Enclosing Content Detection

The `$content` parameter defaults to `null` for self-closing tags. Use `is_null()` to differentiate:

```php
function wporg_shortcode( array $atts = [], ?string $content = null ): string {
    if ( ! is_null( $content ) ) {
        // Enclosed content — manipulate it
        return '<div class="box">' . esc_html( $content ) . '</div>';
    } else {
        // Self-closing tag [wporg]
        return '<div class="box"></div>';
    }
}
```

## Shortcode-ception (Nested Shortcodes)

The shortcode parser performs a **single pass**. Nested shortcodes in `$content` are not automatically parsed. Call `do_shortcode()` to re-parse:

```php
function wporg_shortcode( array $atts = [], ?string $content = null ): string {
    if ( ! is_null( $content ) ) {
        $content = do_shortcode( $content );  // Re-parse nested shortcodes
    }
    return '<div class="box">' . $content . '</div>';
}
```

## Limitations

| Scenario | Behavior |
|----------|----------|
| `[wporg]text[/wporg]` | Standard enclosing — works correctly |
| `[wporg]non-enclosed [wporg]enclosed[/wporg]` | Parser treats entire string as one enclosing shortcode: `"non-enclosed [wporg]enclosed"` |
| Mixing same tag in self-closing + enclosing forms | **Not supported** — parser cannot distinguish |

## Key Notes

| Consideration | Detail |
|---------------|--------|
| Security | Always escape output (`esc_html()`, `esc_attr()`) before returning |
| Content filter | For post content, use `apply_filters( 'the_content', $content )` instead of `do_shortcode()` to apply full content pipeline |
| Single pass | Nested shortcodes require explicit `do_shortcode()` calls in the handler |
