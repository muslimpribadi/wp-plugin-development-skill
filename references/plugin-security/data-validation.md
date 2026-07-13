# Data Validation & Sanitization

## Decision Tree: Which Function to Use?

| Input Type | Sanitize Function | Escape Function | Example |
|------------|-------------------|-----------------|---------|
| Plain text (no HTML) | `sanitize_text_field()` | `esc_html()` | `$name = sanitize_text_field($_POST['name']); echo esc_html($name);` |
| Integer | `absint()`, `intval()` | N/A (auto-safe) | `$count = absint($_GET['count']);` |
| Float | `floatval()` | N/A (auto-safe) | `$price = floatval($_POST['price']);` |
| Email | `sanitize_email()` | `esc_attr()` | `$email = sanitize_email($_POST['email']); echo esc_attr($email);` |
| URL | `esc_url_raw()` (save), `esc_url()` (display) | `esc_url()` | `$url = esc_url_raw($_POST['url']); echo esc_url($url);` |
| Textarea (no HTML) | `sanitize_textarea_field()` | `esc_html()` | `$desc = sanitize_textarea_field($_POST['desc']); echo esc_html($desc);` |
| Rich text (allowed HTML) | `wp_kses_post()`, `wp_kses()` | N/A (already escaped) | `$content = wp_kses_post($_POST['content']); echo $content;` |
| File upload | `sanitize_file_name()` | N/A | `$filename = sanitize_file_name($_FILES['upload']['name']);` |
| Array of values | Loop + per-value sanitization | Per-value escaping | `foreach ($_POST['items'] as $item) { $clean[] = absint($item); }` |

## Common Mistakes

```php
// WRONG: Using esc_html() for sanitization (it escapes, doesn't sanitize)
$safe = esc_html($_POST['input']); // Dangerous — raw data stored in DB

// WRONG: Sanitizing on output instead of input
update_option('my_option', $_POST['raw_input']); // Unsanitized storage!
echo esc_html(get_option('my_option')); // Too late — bad data already saved

// CORRECT: Sanitize on input, escape on output
$sanitized = sanitize_text_field($_POST['input']);
update_option('my_option', $sanitized);
echo esc_html(get_option('my_option'));
```

## When to Use `wp_kses()` vs `wp_kses_post()`

- **`wp_kses_post()`**: Uses WordPress's default allowed HTML tags (same as the visual editor). Use for user-generated content that may include basic formatting.
- **`wp_kses($data, $allowed_html)`**: Custom allowlist. Use when you need precise control over which HTML tags/attributes are permitted.

```php
// Custom allowlist example — only <strong>, <em>, and <a> with href
$allowed = array(
    'strong' => array(),
    'em'     => array(),
    'a'      => array('href' => true, 'title' => true),
);
$safe_content = wp_kses($user_input, $allowed);
```
