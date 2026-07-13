# AJAX in WordPress

## Architecture

WordPress AJAX uses action hooks — not direct file access. All requests go through `admin-ajax.php`.

| Context | Hook Prefix | Example |
|---------|-------------|---------|
| Logged-in users | `wp_ajax_{action}` | `add_action('wp_ajax_my_action', 'my_handler')` |
| Public (non-logged-in) | `wp_ajax_nopriv_{action}` | `add_action('wp_ajax_nprv_my_action', 'my_handler')` |

## Server-Side Handler

```php
add_action( 'wp_ajax_my_action', 'myplugin_ajax_handler' );

function myplugin_ajax_handler() {
    // 1. Verify nonce
    check_ajax_referer( 'my_nonce_action', 'nonce' );

    // 2. Sanitize input
    $value = wp_unslash( sanitize_text_field( $_POST['value'] ) );

    // 3. Process logic
    $result = do_something( $value );

    // 4. Send response (JSON or plain text)
    wp_send_json_success( $result );
    // OR for plain text:
    echo esc_html( $result );
    wp_die();
}
```

### Response Functions

| Function | Purpose | JSON Callback |
|----------|---------|---------------|
| `wp_send_json()` | Send raw JSON response | Neither (raw) |
| `wp_send_json_success()` | Send 200 + success wrapper | JS `.done()` fires |
| `wp_send_json_error()` | Send 400 + error wrapper | JS `.fail()` fires |

```php
// wp_send_json_success() sends: { "success": true, "data": ... }
// wp_send_json_error() sends:  { "success": false, "data": null }
```

## Client-Side Request

### jQuery $.post()

```javascript
$.post(my_ajax_obj.ajax_url, {
    _ajax_nonce: my_ajax_obj.nonce,
    action: "my_action",
    value: $("#input").val()
}, function(response) {
    $(".result").html(response);
});
```

### jQuery $.ajax() with JSON Response

```javascript
$.ajax({
    url: my_ajax_obj.ajax_url,
    type: 'POST',
    data: {
        _ajax_nonce: my_ajax_obj.nonce,
        action: 'my_action',
        value: $('#input').val()
    },
    success: function(response) {
        if (response.success) {
            $(".result").html(response.data);
        } else {
            alert('Error: ' + response.data);
        }
    }
});
```

## Complete Pattern — Enqueue + Handler

```php
add_action( 'admin_enqueue_scripts', 'myplugin_setup_ajax' );

function myplugin_setup_ajax( $hook ) {
    if ( 'edit.php' !== $hook ) return;

    wp_enqueue_script(
        'my-ajax-script',
        plugins_url( '/js/myajax.js', __FILE__ ),
        array( 'jquery' ),
        '1.0',
        true
    );

    wp_localize_script( 'my-ajax-script', 'my_ajax_obj', array(
        'ajax_url' => admin_url( 'admin-ajax.php' ),
        'nonce'    => wp_create_nonce( 'my_nonce_action' ),
    ) );
}

add_action( 'wp_ajax_my_action', 'myplugin_ajax_handler' );

function myplugin_ajax_handler() {
    check_ajax_referer( 'my_nonce_action', 'nonce' );
    $value = wp_unslash( sanitize_text_field( $_POST['value'] ) );
    wp_send_json_success( strtoupper( $value ) );
}
```

## Nonce Verification

| PHP Function | Purpose |
|--------------|---------|
| `wp_create_nonce( string $action )` | Generate a nonce token |
| `check_ajax_referer( string $action, string $query_arg )` | Verify nonce and die on failure |

```php
// Create: wp_create_nonce( 'my_action' ) → stored in JS object as my_ajax_obj.nonce
// Verify: check_ajax_referer( 'my_action', 'nonce' );
// The second parameter matches the JS key name ('_ajax_nonce' or custom)
```

## Security Checklist

| Check | Function | Where |
|-------|----------|-------|
| Nonce verification | `check_ajax_referer()` | PHP handler (first line) |
| Capability check | `current_user_can()` | PHP handler (before logic) |
| Input sanitization | `sanitize_text_field()`, etc. | PHP handler (after nonce) |
| Output escaping | `esc_html__()`, etc. | Any HTML output |
| Die after response | `wp_die()` or via `wp_send_json_*` | End of handler |
