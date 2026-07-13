# Managing Post Metadata

## Core Functions

| Function | Purpose | Signature |
|----------|---------|-----------|
| `add_post_meta()` | Add a new meta entry | `add_post_meta( $post_id, $meta_key, $meta_value, $unique = false )` |
| `update_post_meta()` | Update existing or create if missing | `update_post_meta( $post_id, $meta_key, $meta_value, $prev_value = '' )` |
| `delete_post_meta()` | Delete a meta entry | `delete_post_meta( $post_id, $meta_key, $meta_value = '' )` |
| `get_post_meta()` | Retrieve meta value(s) | `get_post_meta( $post_id, $meta_key = '', $single = false )` |

### add_post_meta() Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `$post_id` | int | Yes | — | ID of the post |
| `$meta_key` | string | Yes | — | Meta key name (prefix with plugin name, e.g., `myplugin_value`) |
| `$meta_value` | mixed | Yes | — | Value to store (string, int, array — arrays are serialized) |
| `$unique` | bool | No | `false` | If `true`, do not allow duplicate keys for the same post |

### update_post_meta() Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `$post_id` | int | Yes | — | ID of the post |
| `$meta_key` | string | Yes | — | The key to update |
| `$meta_value` | mixed | Yes | — | New value |
| `$prev_value` | mixed | No | `''` | If set, only update if current value matches. Empty = update all matching entries. |

### get_post_meta() Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `$post_id` | int | Yes | — | ID of the post |
| `$meta_key` | string | No | `''` | Specific key to retrieve. Empty = all keys for the post |
| `$single` | bool | No | `false` | `true` = return single value; `false` = return array of values |

### Examples

```php
// Add a new meta entry
add_post_meta( 123, '_myplugin_color', 'red', true );

// Update (creates if doesn't exist)
update_post_meta( 123, '_myplugin_color', 'blue' );

// Get single value
$color = get_post_meta( 123, '_myplugin_color', true ); // Returns string 'blue'

// Get all values for a key (if multiple entries allowed)
$values = get_post_meta( 123, '_myplugin_tags' ); // Returns array

// Get all meta keys and values
$all_meta = get_post_meta( 123 );

// Delete specific entry
delete_post_meta( 123, '_myplugin_color', 'blue' );

// Delete all entries with this key (regardless of value)
delete_post_meta( 123, '_myplugin_color' );
```

## Hidden Custom Fields

Meta keys starting with an underscore (`_`) are hidden from the Custom Fields UI and `the_meta()` template tag:

```php
add_post_meta( 123, '_myplugin_hidden', 'secret_value', true );
// Not visible in Custom Fields box or via the_meta()
```

## Character Escaping (JSON)

WordPress applies `stripslashes()` to meta values on storage. For JSON or escaped strings, use `wp_slash()`:

```php
$json = '{"key":"value with \"escaped quotes\""}';

// WRONG — slashes are stripped on retrieval
update_post_meta( $id, 'json', $json );

// CORRECT — wp_slash() adds extra layer that survives stripslashes()
update_post_meta( $id, 'json', wp_slash( $json ) );
```

## Meta Key Naming Conventions

| Rule | Example | Reason |
|------|---------|--------|
| Prefix with plugin name | `myplugin_color` | Avoids collisions with other plugins |
| Don't use `wp_` prefix | ❌ `wp_mykey` | Reserved by WordPress core |
| Use underscore prefix for hidden keys | `_myplugin_color` | Hidden from Custom Fields UI |

## When to Use Meta vs. Custom Tables

| Approach | Best For | Example |
|----------|----------|---------|
| **Post Meta** | Simple key-value data, low volume | Theme options per post, custom fields |
| **Custom Table** | Large datasets, relational queries, frequent reads | Statistics, logs, settings with many rows |

> **Default:** Use `update_post_meta()` / `get_post_meta()` when possible. Only create custom tables for performance-critical or relational data (see `database/creating-tables-with-plugins.md`).
