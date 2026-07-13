# Working with User Metadata

User metadata is stored in the `{$wpdb->prefix}_usermeta` table. Use it for any data beyond what's in the `wp_users` table (`ID`, `user_login`, `user_pass`, `user_nicename`, `user_email`, `user_url`, `user_registered`, `user_activation_key`, `user_status`, `display_name`).

## Functions — CRUD Operations

| Function | Purpose | Signature |
|----------|---------|-----------|
| `add_user_meta()` | Add new metadata | `add_user_meta( int $user_id, string $meta_key, mixed $meta_value, bool $unique = false )` |
| `update_user_meta()` | Update existing metadata | `update_user_meta( int $user_id, string $meta_key, mixed $meta_value, mixed $prev_value = '' )` |
| `delete_user_meta()` | Delete metadata | `delete_user_meta( int $user_id, string $meta_key, mixed $meta_value = '' )` |
| `get_user_meta()` | Retrieve metadata | `get_user_meta( int $user_id, string $key = '', bool $single = false )` |

### Get All Metadata for a User

```php
$all_meta = get_user_meta( $user_id );  // Returns associative array of all keys
```

## Profile Form Hooks

| Hook | Fires When | Capability Required |
|------|-----------|---------------------|
| `show_user_profile` | User edits **own** profile | None (any logged-in user) |
| `edit_user_profile` | User edits **another** user's profile | `edit_users` or specific user edit capability |
| `personal_options_update` | Own profile is saved | Capability to edit own profile |
| `edit_user_profile_update` | Another user's profile is saved | Capability to edit that user |

## Complete Profile Field Example

```php
add_action( 'show_user_profile', 'myplugin_add_birthday_field' );
add_action( 'edit_user_profile', 'myplugin_add_birthday_field' );

function myplugin_add_birthday_field( $user ) {
    ?>
    <h3><?php _e('Personal Information', 'text-domain'); ?></h3>
    <table class="form-table">
        <tr>
            <th><label for="birthday"><?php _e('Birthday', 'text-domain'); ?></label></th>
            <td>
                <input type="date"
                       id="birthday"
                       name="birthday"
                       value="<?php echo esc_attr( get_user_meta( $user->ID, 'birthday', true ) ); ?>" />
                <p class="description"><?php _e('Please use YYYY-MM-DD format.', 'text-domain'); ?></p>
            </td>
        </tr>
    </table>
    <?php
}

add_action( 'personal_options_update', 'myplugin_save_birthday_field' );
add_action( 'edit_user_profile_update', 'myplugin_save_birthday_field' );

function myplugin_save_birthday_field( $user_id ) {
    if ( ! current_user_can( 'edit_user', $user_id ) ) {
        return false;
    }

    if ( isset( $_POST['birthday'] ) ) {
        update_user_meta( $user_id, 'birthday', sanitize_text_field( $_POST['birthday'] ) );
    }
}
```

## Programmatic Usage — Example

```php
// Add metadata
add_user_meta( $user_id, 'favorite_color', 'blue' );

// Update metadata
update_user_meta( $user_id, 'favorite_color', 'red' );

// Get single value
$color = get_user_meta( $user_id, 'favorite_color', true );  // Returns string

// Get multiple values (if not unique)
$colors = get_user_meta( $user_id, 'favorite_color' );  // Returns array

// Delete metadata
delete_user_meta( $user_id, 'favorite_color' );
```

## Key Notes

| Consideration | Detail |
|---------------|--------|
| Unique flag | `add_user_meta()` `$unique = true` prevents duplicate keys on the same user |
| Prev_value for update | `update_user_meta()` `$prev_value` only updates if current value matches (prevents race conditions) |
| Sanitization | Always sanitize input (`sanitize_text_field()`, etc.) before calling `update_user_meta()` |
| Escaping | Always escape output (`esc_attr()`, `esc_html()`) when rendering metadata |
