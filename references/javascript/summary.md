# JavaScript Summary — AJAX Example

## Complete PHP Handler

Place in your plugin file:

```php
add_action( 'admin_enqueue_scripts', 'myplugin_enqueue_ajax' );

function myplugin_enqueue_ajax( $hook ) {
    if ( 'myplugin_settings.php' !== $hook ) {
        return;
    }

    wp_enqueue_script(
        'ajax-script',
        plugins_url( '/js/myjquery.js', __FILE__ ),
        array( 'jquery' ),
        '1.0.0',
        true
    );

    wp_localize_script(
        'ajax-script',
        'my_ajax_obj',
        array(
            'ajax_url' => admin_url( 'admin-ajax.php' ),
            'nonce'    => wp_create_nonce( 'title_example' ),
        )
    );
}

add_action( 'wp_ajax_my_tag_count', 'myplugin_ajax_handler' );

function myplugin_ajax_handler() {
    check_ajax_referer( 'title_example' );

    $title = wp_unslash( $_POST['title'] );
    update_user_meta( get_current_user_id(), 'title_preference', sanitize_text_field( $title ) );

    $args     = array( 'tag' => $title );
    $the_query = new WP_Query( $args );

    echo esc_html( $title ) . ' (' . $the_query->post_count . ') ';
    wp_die();
}
```

## Complete jQuery Handler

Place in `js/myjquery.js`:

```javascript
jQuery(document).ready(function($) {
    $(".pref").change(function() {
        var this2 = this;
        $.post(my_ajax_obj.ajax_url, {
            _ajax_nonce: my_ajax_obj.nonce,
            action: "my_tag_count",
            title: this.value
        }, function(data) {
            this2.nextSibling.remove();
            $(this2).after(data);
        });
    });
});
```
