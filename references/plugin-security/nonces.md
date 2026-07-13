# Nonces (Number Used Once)

## What Is a Nonce?

A nonce in WordPress is a one-time use token that prevents CSRF (Cross-Site Request Forgery) attacks. It is NOT encryption — it proves the request came from your site and from an authorized user.

## Creating Nonces

```php
// In admin pages:
$nonce = wp_create_nonce('my_action');
// Store in hidden form field:
echo '<input type="hidden" name="my_nonce" value="' . esc_attr($nonce) . '" />';

// For AJAX requests:
wp_localize_script('my-script', 'myAjax', array(
    'nonce' => wp_create_nonce('my_ajax_action'),
    'url'   => admin_url('admin-ajax.php'),
));
```

## Verifying Nonces

### In Form Handlers

```php
// Option 1: check_admin_referer (exits on failure)
check_admin_referer('my_action', 'my_nonce');

// Option 2: wp_verify_nonce (returns bool, lets you handle manually)
if (!isset($_POST['my_nonce']) || !wp_verify_nonce($_POST['my_nonce'], 'my_action')) {
    wp_die(esc_html__('Security check failed.', 'my-plugin'));
}
```

### In AJAX Handlers

```php
add_action('wp_ajax_my_action', 'handle_my_ajax');
function handle_my_ajax() {
    // Check nonce for logged-in users
    if (!isset($_POST['nonce']) || !wp_verify_nonce($_POST['nonce'], 'my_ajax_action')) {
        wp_die('Security check failed.');
    }
    
    // Process request...
    wp_send_json_success();
}

// For non-logged-in users (public AJAX):
add_action('wp_ajax_nopriv_my_action', 'handle_my_ajax_public');
function handle_my_ajax_public() {
    if (!isset($_POST['nonce']) || !wp_verify_nonce($_POST['nonce'], 'my_ajax_action')) {
        wp_die(0);
    }
    // Process request...
}
```

## Best Practices

1. **Always use unique nonce strings** — Use a descriptive action name: `wp_create_nonce('my-plugin_save-settings')` not `wp_create_nonce('nonce')`.
2. **Nonces expire after 24 hours** — Always generate fresh nonces on each page load via `wp_create_nonce()`. Never cache or reuse nonce values.
3. **Include the nonce field name in verification** — `check_admin_referer($action, $query_arg)` where `$query_arg` is the `$_POST` key containing the nonce.
4. **Never trust a request without nonce verification** — Every form submission and AJAX action must check a nonce.
5. **Use `wp_nonce_field()` for forms** — It generates both the hidden input and the nonce field automatically:
   ```php
   wp_nonce_field('my_action', 'my_nonce');
   // Outputs: <input type="hidden" id="my_nonce" name="my_nonce" value="..." />
   ```

## Common Mistakes

```php
// WRONG: Using the same nonce for multiple actions
wp_create_nonce('generic'); // Too vague, vulnerable to replay

// WRONG: Verifying with wrong action string
wp_verify_nonce($_POST['nonce'], 'different_action'); // Always fails

// WRONG: Checking capability but not nonce (or vice versa)
// You need BOTH:
if (!current_user_can('manage_options')) wp_die('No access.');
if (!wp_verify_nonce($_POST['nonce'], 'my_action')) wp_die('Nonce failed.');

// WRONG: Using md5() or hash() instead of nonces for security
$token = md5($user_id . time()); // Not a WordPress nonce, not recommended
```
