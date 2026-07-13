# Custom Settings Page

Combines `add_menu_page()` (or other menu API) + Settings API registration + Options API storage.

## Complete Example — Top-Level Settings Page

```php
add_action( 'admin_init', 'myplugin_register_settings' );
add_action( 'admin_menu', 'myplugin_add_settings_page' );

function myplugin_register_settings() {
    register_setting( 'myplugin_group', 'myplugin_options', array(
        'type'              => 'array',
        'sanitize_callback' => 'myplugin_sanitize_options',
    ) );

    add_settings_section(
        'myplugin_main',
        __( 'My Plugin Settings', 'text-domain' ),
        '__return_empty_string',
        'myplugin-page'
    );

    add_settings_field(
        'myplugin_color',
        __( 'Theme Color', 'text-domain' ),
        'myplugin_render_color_field',
        'myplugin-page',
        'myplugin_main',
        array( 'label_for' => 'myplugin_color' )
    );

    add_settings_field(
        'myplugin_enabled',
        __( 'Enable Feature', 'text-domain' ),
        'myplugin_render_toggle_field',
        'myplugin-page',
        'myplugin_main',
        array( 'label_for' => 'myplugin_enabled' )
    );
}

function myplugin_add_settings_page() {
    add_menu_page(
        __( 'My Plugin Settings', 'text-domain' ),
        __( 'My Plugin', 'text-domain' ),
        'manage_options',
        'myplugin-page',
        'myplugin_render_page',
        'dashicons-admin-generic',
        99
    );
}

function myplugin_render_page() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }

    // Show success/error messages
    if ( isset( $_GET['settings-updated'] ) && $_GET['settings-updated'] ) {
        add_settings_error( 'myplugin_messages', 'myplugin_message', __( 'Settings saved.', 'text-domain' ), 'updated' );
    }

    settings_errors( 'myplugin_messages' );
    ?>
    <div class="wrap">
        <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
        <form action="options.php" method="post">
            <?php settings_fields( 'myplugin_group' ); ?>
            <?php do_settings_sections( 'myplugin-page' ); ?>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

function myplugin_sanitize_options( $input ) {
    $sanitized = array();
    $sanitized['color']   = isset( $input['color'] ) ? sanitize_hex_color( $input['color'] ) : '#000000';
    $sanitized['enabled'] = isset( $input['enabled'] ) ? (bool) $input['enabled'] : false;
    return $sanitized;
}

function myplugin_render_color_field( $args ) {
    $options = get_option( 'myplugin_options' );
    $value   = isset( $options[ $args['label_for'] ] ) ? esc_attr( $options[ $args['label_for'] ] ) : '#000000';
    echo '<input type="color" id="' . esc_attr( $args['label_for'] ) . '" name="myplugin_options[' . esc_attr( $args['label_for'] ) . ']" value="' . $value . '" />';
}

function myplugin_render_toggle_field( $args ) {
    $options = get_option( 'myplugin_options' );
    $checked = isset( $options[ $args['label_for'] ] ) && $options[ $args['label_for'] ];
    echo '<input type="checkbox" id="' . esc_attr( $args['label_for'] ) . '" name="myplugin_options[' . esc_attr( $args['label_for'] ) . ']" value="1" ' . checked( $checked, true, false ) . ' />';
}
```

## Key Patterns

| Pattern | Implementation |
|---------|----------------|
| Array option storage | `register_setting()` with `'type' => 'array'` + sanitize callback returns array |
| Message display | `add_settings_error()` → `settings_errors()` in page callback |
| Success detection | Check `$_GET['settings-updated']` after form submission |
| Field naming | Use `$options[ $args['label_for'] ]` for array-style field names: `name="myplugin_options[color]"` |
