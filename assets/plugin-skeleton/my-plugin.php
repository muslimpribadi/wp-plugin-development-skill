<?php
/**
 * Plugin Name:       My Plugin (Skeleton)
 * Plugin URI:        https://example.com/my-plugin
 * Description:       A minimal WordPress plugin skeleton demonstrating best practices. Replace all placeholder values with your own.
 * Version:           1.0.0
 * Author:            Your Name
 * Author URI:        https://example.com
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       my-plugin
 * Requires at least: 6.0
 * Requires PHP:      8.2
 */

// Prevent direct access.
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * ---------------------------------------------------------------------------
 * Plugin Constants & Configuration
 * ---------------------------------------------------------------------------
 */
define( 'MAP_VERSION', '1.0.0' );
define( 'MAP_PLUGIN_DIR', plugin_dir_path( __FILE__ ) );
define( 'MAP_PLUGIN_URL', plugin_dir_url( __FILE__ ) );

/**
 * ---------------------------------------------------------------------------
 * Activation Hook
 * ---------------------------------------------------------------------------
 */
register_activation_hook( __FILE__, 'map_activate' );

/**
 * Run on plugin activation.
 * Use for: creating database tables, setting default options, flushing rewrite rules.
 */
function map_activate(): void {
    // Example: set default options
    add_option( 'map_settings', [
        'option_a' => '',
        'option_b' => 0,
    ] );

    // Flush rewrite rules if using custom post types or permalinks
    flush_rewrite_rules();
}

/**
 * ---------------------------------------------------------------------------
 * Deactivation Hook
 * ---------------------------------------------------------------------------
 */
register_deactivation_hook( __FILE__, 'map_deactivate' );

/**
 * Run on plugin deactivation.
 * Use for: flushing rewrite rules, clearing caches. Do NOT delete user options.
 */
function map_deactivate(): void {
    flush_rewrite_rules();
}

/**
 * ---------------------------------------------------------------------------
 * Initialization Hooks
 * ---------------------------------------------------------------------------
 */
add_action( 'plugins_loaded', 'map_init' );

/**
 * Load text domain and initialize plugin components.
 */
function map_init(): void {
    load_plugin_textdomain( 'my-plugin', false, dirname( plugin_basename( __FILE__ ) ) . '/languages' );
}

/**
 * ---------------------------------------------------------------------------
 * Admin Menu
 * ---------------------------------------------------------------------------
 */
add_action( 'admin_menu', 'map_admin_menu' );

/**
 * Register admin menu pages.
 */
function map_admin_menu(): void {
    add_menu_page(
        __( 'My Plugin', 'my-plugin' ),
        __( 'My Plugin', 'my-plugin' ),
        'manage_options',
        'my-plugin',
        'map_render_main_page',
        'dashicons-admin-generic',
        25
    );

    add_submenu_page(
        'my-plugin',
        __( 'Settings', 'my-plugin' ),
        __( 'Settings', 'my-plugin' ),
        'manage_options',
        'my-plugin-settings',
        'map_render_settings_page'
    );
}

/**
 * Render the main admin page.
 */
function map_render_main_page(): void {
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( esc_html__( 'You do not have sufficient permissions to access this page.', 'my-plugin' ) );
    }

    echo '<div class="wrap">';
    echo '<h1>' . esc_html__( 'My Plugin', 'my-plugin' ) . '</h1>';
    echo '<p>' . esc_html__( 'Welcome to My Plugin. Configure settings below.', 'my-plugin' ) . '</p>';
    echo '</div>';
}

/**
 * ---------------------------------------------------------------------------
 * Settings API
 * ---------------------------------------------------------------------------
 */
add_action( 'admin_init', 'map_register_settings' );

/**
 * Register plugin settings.
 */
function map_register_settings(): void {
    register_setting( 'my_plugin_settings_group', 'my_plugin_option_a', [
        'type'              => 'string',
        'sanitize_callback' => 'sanitize_text_field',
        'default'           => '',
    ] );

    add_settings_section(
        'my_plugin_main_section',
        __( 'Main Settings', 'my-plugin' ),
        '__return_empty_string',
        'my-plugin-settings'
    );

    add_settings_field(
        'my_plugin_option_a',
        __( 'Option A', 'my-plugin' ),
        'map_render_option_a_field',
        'my-plugin-settings',
        'my_plugin_main_section'
    );
}

/**
 * Render the Option A input field.
 */
function map_render_option_a_field(): void {
    $value = get_option( 'my_plugin_option_a', '' );
    echo '<input type="text" name="my_plugin_option_a" value="' . esc_attr( $value ) . '" class="regular-text" />';
    echo '<p class="description">' . esc_html__( 'Enter a text value.', 'my-plugin' ) . '</p>';
}

/**
 * Render the Settings admin page.
 */
function map_render_settings_page(): void {
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( esc_html__( 'You do not have sufficient permissions to access this page.', 'my-plugin' ) );
    }

    echo '<div class="wrap">';
    echo '<h1>' . esc_html__( 'My Plugin Settings', 'my-plugin' ) . '</h1>';
    echo '<form method="post" action="options.php">';
    settings_fields( 'my_plugin_settings_group' );
    do_settings_sections( 'my-plugin-settings' );
    submit_button();
    echo '</form>';
    echo '</div>';
}

/**
 * ---------------------------------------------------------------------------
 * Shortcodes
 * ---------------------------------------------------------------------------
 */
add_shortcode( 'my_greeting', 'map_my_greeting_shortcode' );

/**
 * [my_greeting name="World"]
 * Outputs a personalized greeting message.
 */
function map_my_greeting_shortcode( array $atts ): string {
    $atts = shortcode_atts( [
        'name' => 'World',
    ], $atts, 'my_greeting' );

    $name = esc_html( $atts['name'] );

    ob_start();
    ?>
    <div class="my-greeting">
        <p><?php printf( esc_html__( 'Hello, %s!', 'my-plugin' ), $name ); ?></p>
    </div>
    <?php
    return ob_get_clean();
}

/**
 * ---------------------------------------------------------------------------
 * Example: AJAX Handler (with nonce + capability verification)
 * ---------------------------------------------------------------------------
 */
add_action( 'wp_ajax_map_do_action', 'map_ajax_handler' );

/**
 * Handle AJAX request. Only logged-in users with manage_options can access.
 */
function map_ajax_handler(): void {
    // Verify nonce
    if ( ! isset( $_POST['map_nonce'] ) || ! wp_verify_nonce( $_POST['map_nonce'], 'map_ajax_action' ) ) {
        wp_send_json_error( [ 'message' => __( 'Security check failed.', 'my-plugin' ) ] );
    }

    // Check capability
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_send_json_error( [ 'message' => __( 'Insufficient permissions.', 'my-plugin' ) ] );
    }

    // Process data
    $data = sanitize_text_field( $_POST['data'] ?? '' );

    wp_send_json_success( [ 'received' => $data ] );
}
