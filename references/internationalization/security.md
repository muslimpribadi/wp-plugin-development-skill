# Internationalization Security

Translatable strings are untrusted input — always escape output and validate translations.

## Escape All Output

Never echo a translation function directly in HTML context:

```php
// INSECURE — translator could inject malicious code
_e( 'Click here', 'my-plugin' );

// SECURE — escaped for body content
echo esc_html__( 'Click here', 'my-plugin' );

// SECURE — escaped for attributes
echo esc_attr__( 'Tooltip text', 'my-plugin' );
```

### Escape Function Reference

| Context | Return | Echo |
|---------|--------|------|
| HTML body | `esc_html__()` | `esc_html_e()` |
| HTML attribute | `esc_attr__()` | `esc_attr_e()` |
| With context (body) | `esc_html_x()` | `esc_html_ex()` |
| With context (attr) | `esc_attr_x()` | `esc_attr_ex()` |

## Placeholders for URLs

Never include URLs in translatable strings — a malicious translator could redirect users:

```php
// INSECURE — URL embedded in translation
_e( 'Please <a href="https://login.wordpress.org/register">register</a>.', 'my-plugin' );

// SECURE — URL passed as separate variable
printf(
    esc_html__( 'Please %1$sregister%2$s.', 'my-plugin' ),
    '<a href="https://login.wordpress.org/register">',
    '</a>'
);
```

## Validate Translations

When receiving `.po`/`.mo` files from third parties:

| Check | Method |
|-------|--------|
| **Spam injection** | Use Google Translate to reverse-translate strings and compare with originals |
| **Malicious code** | Search `msgstr` entries for `<script>`, `javascript:`, backticks, `$(` patterns |
| **Compiled .mo mismatch** | Always recompile `.mo` from `.po` yourself — never trust pre-compiled binaries |

### Compile Your Own .mo

```bash
# Validate and compile (verbose output shows errors)
msgfmt -cv -o /path/to/output.mo /path/to/input.po
```

> **Note:** PoEdit may override `.po` headers during compilation. Command-line `msgfmt` preserves original metadata.

## Safe Translation Patterns Summary

| Pattern | Secure Version |
|---------|---------------|
| Simple text | `esc_html__( 'Text', 'domain' )` |
| Text with HTML tags | Pass HTML as separate variable via `printf()` |
| URLs | Always externalize via placeholders |
| User-facing output | Always use escape function (`esc_html__`, `esc_attr__`) |
| Attributes | Always use `esc_attr__()`, never `__()` |
