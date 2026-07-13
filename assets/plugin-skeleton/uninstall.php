<?php
/**
 * WordPress Plugin Uninstall Script
 *
 * This file is executed when the user deletes the plugin from the WordPress admin.
 * It runs ONLY when the plugin is deleted (not deactivated).
 *
 * Use this file to:
 * - Delete all plugin options from wp_options
 * - Remove custom database tables
 * - Clean up any temporary files or data
 *
 * IMPORTANT: Do NOT delete user-generated content (posts, comments, etc.)
 * unless the plugin specifically manages that content and the user expects it.
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

/**
 * ---------------------------------------------------------------------------
 * Delete Plugin Options
 * ---------------------------------------------------------------------------
 */

// Single option
delete_option( 'my_plugin_option_a' );

// Array of options (use a loop or delete each individually)
delete_option( 'my_plugin_settings' );

// If you used add_options_page and stored settings as arrays,
// make sure to delete the full option key.

/**
 * ---------------------------------------------------------------------------
 * Delete Custom Database Tables
 * ---------------------------------------------------------------------------
 */
global $wpdb;

$tables = array(
    $wpdb->prefix . 'my_plugin_table',
);

foreach ( $tables as $table ) {
    if ( $wpdb->get_var( "SHOW TABLES LIKE '$table'" ) !== null ) {
        $wpdb->query( "DROP TABLE IF EXISTS `$table`" );
    }
}

/**
 * ---------------------------------------------------------------------------
 * Clean Up Transients & Cache
 * ---------------------------------------------------------------------------
 */

// Delete all transients with a common prefix
$transients = $wpdb->get_col( "SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE '%_transient_map_%'" );
foreach ( $transients as $transient ) {
    delete_transient( str_replace( '_transient_', '', $transient ) );
}

/**
 * ---------------------------------------------------------------------------
 * Remove Custom Rewrite Rules (if flushed on activation)
 * ---------------------------------------------------------------------------
 */

// If you added custom rewrite rules, flush them here
flush_rewrite_rules();
