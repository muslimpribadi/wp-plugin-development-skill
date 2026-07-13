# Internationalizing Your Plugin

## Text Domain

A text domain is a unique identifier for your plugin's translations. It must match the plugin slug (lowercase, dashes, no spaces).

```php
/*
 * Plugin Name: My Plugin
 * Text Domain: my-plugin
 */
```

### Domain Path

Define where translation files live:

```php
/*
 * Plugin Name: My Plugin
 * Text Domain: my-plugin
 * Domain Path: /languages
 */
```

> **Note:** `Domain Path` defaults to the plugin root. Only specify if translations are in a subdirectory (e.g., `/languages`).

## Loading Translations

```php
add_action( 'init', 'myplugin_load_textdomain' );

function myplugin_load_textdomain() {
    load_plugin_textdomain( 'my-plugin', false, dirname( plugin_basename( __FILE__ ) ) . '/languages' );
}
```

> **Note:** Since WordPress 4.6, `load_plugin_textdomain()` is optional for plugins on wordpress.org (translations are loaded automatically). Include it only if you ship your own `.mo` files.

To prevent WordPress.org translation override:

```php
add_filter( 'load_textdomain_mofile', 'myplugin_override_translations' );

function myplugin_override_translations( $mofile, $domain ) {
    if ( 'my-plugin' === $domain && false !== strpos( $mofile, WP_LANG_DIR . '/plugins/' ) ) {
        $locale = apply_filters( 'plugin_locale', determine_locale(), $domain );
        $mofile = WP_PLUGIN_DIR . '/' . dirname( plugin_basename( __FILE__ ) ) . '/languages/' . $domain . '-' . $locale . '.mo';
    }
    return $mofile;
}
```

## Translation Functions

### Basic Translation

| Function | Returns/Echoes | Parameters | Example |
|----------|---------------|------------|---------|
| `__()` | Returns translated string | `$text`, `$domain` | `$title = __( 'Hello', 'my-plugin' )` |
| `_e()` | Echoes translated string | `$text`, `$domain` | `_e( 'Hello', 'my-plugin' )` |

### Escaping Translation Functions

Use these when outputting HTML attributes or text:

| Function | Purpose | Example |
|----------|---------|---------|
| `esc_html__()` | Escape for HTML body content | `<h1><?php echo esc_html__( 'Title', 'my-plugin' ); ?></h1>` |
| `esc_html_e()` | Echo + escape for HTML body | `<h1><?php esc_html_e( 'Title', 'my-plugin' ); ?></h1>` |
| `esc_attr__()` | Escape for HTML attribute | `<div title="<?php echo esc_attr__( 'Tooltip', 'my-plugin' ); ?>">` |
| `esc_attr_e()` | Echo + escape for attribute | `<div title="<?php esc_attr_e( 'Tooltip', 'my-plugin' ); ?>">` |
| `esc_html_x()` | Escape + context (returns) | `echo esc_html_x( 'Post', 'noun', 'my-plugin' )` |
| `esc_attr_x()` | Escape + context (returns) | `echo esc_attr_x( 'Post', 'verb', 'my-plugin' )` |

## Variables in Strings

Use placeholders with `printf()`/`sprintf()`. Never concatenate variables into translatable strings.

### Single Placeholder

```php
printf(
    /* translators: %s: City name */
    __( 'Your city is %s.', 'my-plugin' ),
    esc_html( $city )
);
```

### Multiple Placeholders (Argument Swapping)

Use `%1$s`, `%2$s` for languages that reorder words:

```php
printf(
    /* translators: 1: City name, 2: ZIP code */
    __( 'City: %1$s, ZIP: %2$s', 'my-plugin' ),
    esc_html( $city ),
    esc_html( $zipcode )
);
```

> **Warning:** Never do this — variables must not be in the translatable string:
> ```php
> // WRONG — translators see literal $city
> _e( "Your city is $city.", 'my-plugin' );
> ```

## Pluralization

### Basic Plurals

```php
printf(
    /* translators: %s: Comment count */
    _n(
        '%s comment',
        '%s comments',
        get_comments_number(),
        'my-plugin'
    ),
    number_format_i18n( get_comments_number() )
);
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `$single` | string | Singular form (use `%s`, not `'One comment'`) |
| `$plural` | string | Plural form |
| `$count` | int | Number determining which form to use |
| `$domain` | string | Text domain |

> **Note:** Some languages have 3+ plural forms. Always use `%s` or `%d`, never `'One item'`.

### Deferred Pluralization

Use `_n_noop()` + `translate_nooped_plural()` for deferred translation (e.g., storing strings in options):

```php
$comments_text = _n_noop( '%s comment', '%s comments', 'my-plugin' );

printf(
    translate_nooped_plural( $comments_text, get_comments_number(), 'my-plugin' ),
    number_format_i18n( get_comments_number() )
);
```

### Context-Based Translation

Use when a word has different meanings in different contexts:

```php
// As a noun
$post_label = _x( 'Post', 'noun', 'my-plugin' );

// As a verb
$post_action = _x( 'Post', 'verb', 'my-plugin' );
```

| Function | Returns/Echoes | Parameters | Example |
|----------|---------------|------------|---------|
| `_x()` | Returns | `$text`, `$context`, `$domain` | `_x( 'Post', 'noun', 'my-plugin' )` |
| `_ex()` | Echoes | `$text`, `$context`, `$domain` | `_ex( 'Post', 'verb', 'my-plugin' )` |

## Translator Comments

Add hints for translators using `/* translators: ... */` comments immediately before the function call:

```php
/* translators: draft saved date format, see http://php.net/date */
$saved_date_format = __( 'g:i:s a', 'my-plugin' );

/* translators: 1: WordPress version, 2: number of bugs fixed */
_n_noop(
    '<strong>Version %1$s</strong> addressed %2$s bug.',
    '<strong>Version %1$s</strong> addressed %2$s bugs.',
    'my-plugin'
);
```

## Best Practices

| Practice | Reason |
|----------|--------|
| Use full sentences | Word order varies across languages |
| Split at paragraphs | Don't bundle entire pages into one string |
| No leading/trailing whitespace | Causes translation mismatches |
| Assume 2x expansion length | UI may break with long translations |
| Avoid HTML in translatable strings | Breaks in other languages; use placeholders instead |
| Use argument swapping (`%1$s`) | Allows reordering for different languages |
| Add context hints | Helps translators choose correct meaning |

## JavaScript Translations

Use `wp_localize_script()` to pass translatable strings to JS:

```php
wp_enqueue_script( 'myplugin-script', plugins_url( 'js/script.js', __FILE__ ) );

wp_localize_script( 'myplugin-script', 'mypluginL10n', array(
    'confirmDelete' => __( 'Are you sure?', 'my-plugin' ),
    'loading'       => __( 'Loading...', 'my-plugin' ),
) );
```

Then access in JavaScript:

```javascript
alert( mypluginL10n.confirmDelete );
```
