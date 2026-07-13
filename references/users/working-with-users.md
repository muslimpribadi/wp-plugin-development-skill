# Working with Users

## Creating Users

| Function | Use Case | Signature |
|----------|----------|-----------|
| `wp_create_user()` | Simple creation (username, password, email only) | `wp_create_user( string $username, string $password, string $email )` |
| `wp_insert_user()` | Full control (accepts array of user properties) | `wp_insert_user( array\|WP_User $userdata )` |

### Simple Creation

```php
$user_id = username_exists( $user_name );  // Check if username taken

if ( ! $user_id && ! email_exists( $user_email ) ) {
    $random_password = wp_generate_password( 12, false );
    $user_id = wp_create_user( $user_name, $random_password, $user_email );
}
```

### Full User Creation

```php
$user_data = array(
    'user_login'   => 'johndoe',
    'user_pass'    => 'securepassword',
    'user_email'   => 'john@example.com',
    'user_url'     => 'https://example.com',
    'first_name'   => 'John',
    'last_name'    => 'Doe',
    'display_name' => 'John Doe',
    'role'         => 'author',
);

$user_id = wp_insert_user( $user_data );

if ( is_wp_error( $user_id ) ) {
    // Handle error: $user_id->get_error_message()
} else {
    // Success: $user_id contains the new user ID
}
```

> **Note:** `wp_insert_user()` fires `user_register` on creation (ID doesn't exist) and `profile_update` on update (ID exists).

## Updating Users

| Function | Purpose | Signature |
|----------|---------|-----------|
| `wp_update_user()` | Update a user record | `wp_update_user( array\|WP_User $userdata )` |
| `update_user_meta()` | Update single metadata field | `update_user_meta( int $user_id, string $meta_key, mixed $meta_value )` |

```php
$user_id = wp_update_user( array(
    'ID'       => 42,
    'user_url' => 'https://newsite.com',
    'display_name' => 'New Name',
) );

if ( is_wp_error( $user_id ) ) {
    // Handle error
}
```

> **Warning:** If the user's password is being updated via `wp_update_user()`, all cookies for that user are cleared.

## Deleting Users

| Function | Purpose | Signature |
|----------|---------|-----------|
| `wp_delete_user()` | Delete a user and optionally reassign content | `wp_delete_user( int $id, int $reassign = null )` |

```php
// Delete user; all their posts are deleted too
$result = wp_delete_user( 42 );

// Delete user; reassign posts to user ID 1
$result = wp_delete_user( 42, 1 );

if ( is_wp_error( $result ) ) {
    // Handle error
} else {
    // Success: $result contains number of items reassigned/deleted
}
```

> **Warning:** If `$reassign` is not set to a valid user ID, all content associated with the deleted user (posts, comments, etc.) is permanently deleted.

## Helper Functions

| Function | Purpose | Signature |
|----------|---------|-----------|
| `username_exists()` | Check if username is taken | `username_exists( string $username )` → user ID or `null` |
| `email_exists()` | Check if email is registered | `email_exists( string $email )` → user ID or `null` |
| `wp_generate_password()` | Generate random password | `wp_generate_password( int $length = 12, bool $special_chars = true )` |

## Key Notes

| Consideration | Detail |
|---------------|--------|
| Validation | Always check `is_wp_error()` after create/update/delete operations |
| Passwords | Never store plaintext passwords; use `wp_create_user()` or let `wp_insert_user()` hash via `wp_hash_password()` |
| Role assignment | Set `'role'` in `$userdata` array for `wp_insert_user()` — defaults to site default role |
| Hooks | `user_register` fires on creation, `profile_update` fires on update, `deleted_user` fires after deletion |
