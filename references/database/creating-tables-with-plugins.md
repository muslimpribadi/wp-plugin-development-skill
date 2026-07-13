# Creating Tables with Plugins

## When to Use a Custom Table vs Post Meta

| Approach | Best For | Example |
|----------|----------|---------|
| **Post Meta** | Data related to posts/pages/comments | Custom fields, user preferences per post |
| **Custom Table** | Large datasets, relational data, frequent queries | Statistics, logs, settings with many rows |

> **Default:** Use `update_post_meta()` / `get_post_meta()` when possible. Only create custom tables for performance-critical or relational data.

## Database Table Prefix

Always use `$wpdb->prefix` — never hardcode `wp_`:

```php
global $wpdb;
$table_name = $wpdb->prefix . 'myplugin_table';
```

## dbDelta Requirements

The `dbDelta()` function is **strict**. Your SQL must follow these rules:

| Rule | Example |
|------|---------|
| Each field on its own line | ✅ One field per line |
| Two spaces between `PRIMARY KEY` and definition | `` PRIMARY KEY  (id) `` |
| Use `KEY` not `INDEX` | `` KEY my_key (col) `` |
| Must include at least one `KEY` or `PRIMARY KEY` | Required |
| No backticks around field names | ✅ `id mediumint(9)` — NOT `` `id` mediumint(9) `` |
| Field types lowercase | ✅ `mediumint(9)` — NOT `MEDIUMINT(9)` |
| SQL keywords uppercase | ✅ `CREATE TABLE`, `NOT NULL`, `DEFAULT` |
| Specify length for numeric fields | ✅ `int(11)`, `varchar(255)` |

## Creating a Table

```php
function myplugin_create_table() {
    global $wpdb;

    $table_name = $wpdb->prefix . 'myplugin_table';
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        time datetime DEFAULT '0000-00-00 00:00:00' NOT NULL,
        name tinytext NOT NULL,
        text text NOT NULL,
        url varchar(255) DEFAULT '' NOT NULL,
        PRIMARY KEY  (id),
        KEY name_key (name(100))
    ) $charset_collate;";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );
}
```

> **Note:** `get_charset_collate()` requires WordPress 3.5+. For older versions, use: `"DEFAULT CHARACTER SET {$wpdb->charset} COLLATE {$wpdb->collate}"`

## Adding Initial Data

```php
function myplugin_add_initial_data() {
    global $wpdb;

    $table_name = $wpdb->prefix . 'myplugin_table';

    $wpdb->insert(
        $table_name,
        array(
            'time' => current_time( 'mysql' ),
            'name' => 'Welcome',
            'text' => 'Your table is ready.',
            'url'  => '',
        ),
        array( '%s', '%s', '%s' ) // format specifiers (optional)
    );
}
```

> **Note:** `$wpdb->insert()` automatically escapes values. For raw queries, use `$wpdb->prepare()`.

## Version Tracking

Store the schema version in `wp_options` to detect changes on updates:

```php
add_option( 'myplugin_db_version', '1.0' );
```

## Complete Activation Function

```php
$myplugin_db_version = '1.0';

function myplugin_install() {
    global $wpdb, $myplugin_db_version;

    $table_name = $wpdb->prefix . 'myplugin_table';
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        time datetime DEFAULT '0000-00:00:00' NOT NULL,
        name tinytext NOT NULL,
        text text NOT NULL,
        url varchar(255) DEFAULT '' NOT NULL,
        PRIMARY KEY  (id),
        KEY name_key (name(100))
    ) $charset_collate;";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );

    add_option( 'myplugin_db_version', $myplugin_db_version );
}

function myplugin_install_data() {
    global $wpdb;
    $table_name = $wpdb->prefix . 'myplugin_table';

    $wpdb->insert(
        $table_name,
        array(
            'time' => current_time( 'mysql' ),
            'name' => 'Welcome',
            'text' => 'Table created successfully.',
        )
    );
}

register_activation_hook( __FILE__, 'myplugin_install' );
register_activation_hook( __FILE__, 'myplugin_install_data' );
```

## Upgrading an Existing Table

`dbDelta()` handles schema changes automatically. Compare version and run when needed:

```php
function myplugin_update_db_check() {
    global $wpdb, $myplugin_db_version;

    $installed_ver = get_option( 'myplugin_db_version' );

    if ( $installed_ver !== $myplugin_db_version ) {
        myplugin_install(); // Re-run with new schema
        update_option( 'myplugin_db_version', $myplugin_db_version );
    }
}

// Runs on every page load — lightweight version check
add_action( 'plugins_loaded', 'myplugin_update_db_check' );
```

> **Note:** Since WordPress 3.1, `register_activation_hook()` is **not** called on plugin updates. Use `plugins_loaded` hook to detect schema changes.

## Common $wpdb Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `$wpdb->insert()` | Insert with auto-escaping | `$wpdb->insert( $table, $data, $format )` |
| `$wpdb->update()` | Update rows | `$wpdb->update( $table, $data, $where, $format, $where_format )` |
| `$wpdb->get_results()` | Fetch multiple rows | `$wpdb->get_results( "SELECT * FROM $table" )` |
| `$wpdb->get_row()` | Fetch single row | `$wpdb->get_row( "SELECT * FROM $table LIMIT 1" )` |
| `$wpdb->get_var()` | Fetch single value | `$wpdb->get_var( "SELECT COUNT(*) FROM $table" )` |
| `$wpdb->prepare()` | Sanitize query | `$wpdb->prepare( "SELECT * FROM $table WHERE id = %d", $id )` |
| `$wpdb->delete()` | Delete rows | `$wpdb->delete( $table, $where, $where_format )` |

> **Security:** Always use `$wpdb->prepare()` for queries with variables. Never concatenate user input into SQL strings.
