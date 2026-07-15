# Securing Output: Complete Guide

## The Golden Rule

**Escape data at the point of output**, not before storage. Store raw (sanitized) data; escape when rendering to browser, email, or API response.

## Function Selection Guide

| Output Context | Escape Function | Why |
|----------------|-----------------|-----|
| Inside HTML element content | `esc_html()` | Converts `<`, `>`, `&`, `"`, `'` to entities |
| Inside HTML attribute | `esc_attr()` | Same as esc_html but for attribute values |
| URLs (href, src, action) | `esc_url()` | Validates protocol, strips dangerous chars |
| URLs in query strings | `esc_url_raw()` | For database storage of URLs |
| Rich text with allowed HTML | `wp_kses_post()` or `wp_kses()` | Allows safe HTML tags while stripping others |
| JSON output | `wp_json_encode()` | Properly escapes for JavaScript contexts |
| Database output in SQL | `$wpdb->prepare()` | Prevents SQL injection |

## Context-Aware Escaping Examples

### Inside HTML Content

```php
// WRONG: Raw echo
echo $user_input;

// CORRECT: Escape HTML content
echo esc_html($user_input);

// CORRECT: With translation
echo esc_html(__('Hello', 'my-plugin') . ' ' . esc_html($username));
```

### Inside Attributes

```php
// WRONG: Attribute injection via unescaped value
echo '<input type="text" value="' . $user_value . '" />';

// CORRECT: Escape attribute values
echo '<input type="text" value="' . esc_attr($user_value) . '" />';

// CORRECT: With data attributes (safe if you control the key)
echo '<div class="widget" data-id="' . absint($id) . '"></div>';
```

### URLs

```php
// WRONG: Protocol-relative or unvalidated URL
echo '<a href="' . $user_url . '">Link</a>';

// CORRECT: Validate and escape
echo '<a href="' . esc_url($user_url) . '">Link</a>';

// CORRECT: With fallback
$url = !empty($user_url) ? esc_url($user_url) : esc_url(home_url('/'));
```

### Rich Text Output

```php
// User-submitted content with allowed HTML
$content = get_post_meta($post_id, 'custom_content', true);
echo wp_kses_post($content); // Allows p, br, a, strong, em, etc.

// Strict allowlist for specific use case
$allowed_tags = [
    'a'      => ['href' => true, 'title' => true],
    'strong' => [],
    'em'     => [],
];
echo wp_kses($user_content, $allowed_tags);
```

## Common Output Mistakes

```php
// WRONG: Assuming stored data is safe to echo
echo get_option('my_option'); // May contain raw HTML/JS

// CORRECT: Always escape on output regardless of source
echo esc_html(get_option('my_option'));

// WRONG: Using print_r or var_dump in production
print_r($data); // Exposes internal structure, unescaped

// CORRECT: Use proper formatting with escaping
echo '<pre>' . esc_html(print_r($data, true)) . '</pre>';

// WRONG: Unescaped wp_die message
wp_die('Error: ' . $user_error); // XSS vulnerability

// CORRECT: Escaped wp_die message
wp_die(esc_html('Error: ') . esc_html($user_error));
```

## Special Cases

### JavaScript Contexts

```php
// NEVER output PHP variables directly into JS strings
// WRONG:
echo '<script>var data = "' . $js_data . '";</script>';

// CORRECT: Use wp_localize_script() or wp_add_inline_script()
wp_localize_script('my-script', 'myData', [
    'value' => $safe_value, // Automatically JSON-encoded
]);

// For inline echo in PHP-generated JS:
echo '<script>var data = ' . wp_json_encode($safe_data) . ';</script>';
```

### Email Output

```php
// Emails should use plain text escaping for safety
$to      = sanitize_email($recipient);
$subject = esc_html($email_subject);
$message = wp_kses_post($email_body); // If HTML email, use proper headers
wp_mail($to, $subject, $message, $headers);
```

### REST API Responses

```php
// Always set proper content type and escape response data
rest_ensure_response([
    'status'  => 'success',
    'data'    => array_map('esc_html', $results), // Escape each string
    'count'   => absint($total),
]);
```

## Quick Reference: Escape or Die

If you're unsure which escape function to use, default to `esc_html()`. It is the safest catch-all for text output. When in doubt: **escape early, escape often**.
