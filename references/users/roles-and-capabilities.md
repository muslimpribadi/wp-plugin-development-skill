# Roles and Capabilities

Roles define sets of capabilities for a user. WordPress stores them in the `{$wpdb->prefix}_options` table under the `user_roles` key.

## Built-in Roles

| Role | Description |
|------|-------------|
| `super_admin` | Network-level administrator (multisite) |
| `administrator` | Full site administration |
| `editor` | Manage and publish posts, including other users' posts |
| `author` | Publish and manage own posts |
| `contributor` | Write and manage own posts but cannot publish |
| `subscriber` | Read only, no publishing |

## Functions — Role Management

| Function | Purpose | Signature |
|----------|---------|-----------|
| `add_role()` | Register a new role | `add_role( string $role, string $name, array $capabilities )` |
| `remove_role()` | Delete an existing role | `remove_role( string $role )` |
| `get_role()` | Get a role object | `get_role( string $role )` → `WP_Role` instance |
| `add_cap()` | Add capability to a role | `$role->add_cap( string $cap, bool $grant = true )` |
| `remove_cap()` | Remove capability from a role | `$role->remove_cap( string $cap )` |

## Role Object Methods

```php
$role = get_role( 'author' );

// Add a capability
$role->add_cap( 'edit_others_posts', true );

// Remove a capability
$role->remove_cap( 'delete_posts' );

// Get all capabilities
$capabilities = $role->capabilities;  // Array of cap => bool
```

## Capability Check Functions

| Function | Purpose | Signature |
|----------|---------|-----------|
| `current_user_can()` | Check current user's capability | `current_user_can( string $cap, mixed ...$args )` |
| `user_can()` | Check any user's capability | `user_can( int\|WP_User $user, string $cap, mixed ...$args )` |
| `current_user_can_for_blog()` | Multisite: check on specific blog | `current_user_can_for_blog( int $blog_id, string $cap )` |

> **Note:** `$args` (third argument) can pass an object ID for context-aware capability checks (e.g., post-specific permissions).

## Adding a Custom Role — Example

```php
add_action( 'init', 'myplugin_add_custom_role' );

function myplugin_add_custom_role() {
    add_role(
        'content_reviewer',
        __( 'Content Reviewer', 'text-domain' ),
        array(
            'read'         => true,
            'edit_posts'   => true,
            'upload_files' => true,
            'read_private_posts' => true,
        )
    );
}
```

> **Warning:** After the first `add_role()` call, the role is stored in the database. Subsequent calls do nothing — they won't alter capabilities. To modify a role: `remove_role()` then `add_role()` again. Only do this if capabilities actually differ to avoid performance degradation.

## Modifying an Existing Role

```php
// Must run AFTER initial add_role() (higher priority)
add_action( 'init', 'myplugin_modify_role_caps', 11 );

function myplugin_modify_role_caps() {
    $role = get_role( 'content_reviewer' );
    $role->add_cap( 'edit_others_posts' );
}
```

## Key Notes

| Consideration | Detail |
|---------------|--------|
| Multisite default role | If removing the `subscriber` role, run `update_option('default_role', 'new_role')` |
| Never remove admin/super_admin | Core may re-add these in future updates; removing breaks functionality |
| Capabilities without UI | Custom capabilities have no effect on the default admin dashboard but can be checked programmatically for custom areas |
