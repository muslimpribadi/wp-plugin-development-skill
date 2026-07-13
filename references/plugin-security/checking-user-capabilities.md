# Checking User Capabilities

Always verify user capabilities before executing privileged operations or exposing functionality.

## Role Hierarchy

| Role | Capabilities Inherited From | Key Unique Capabilities |
|------|---------------------------|------------------------|
| Administrator | All below | `manage_options`, `edit_users` |
| Editor | Author, Contributor, Subscriber | Edit/publish any post |
| Author | Contributor, Subscriber | Publish own posts |
| Contributor | Subscriber | Write own posts (no publish) |
| Subscriber | — | Profile management only |

## Checking Capabilities

```php
current_user_can( string $capability ): bool
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$capability` | string | Yes | Capability to check (e.g., `'manage_options'`, `'edit_posts'`) |
| **Returns** | bool | — | `true` if user has capability, `false` otherwise |

### Common Capabilities Reference

| Capability | Description | Minimum Role |
|------------|-------------|-------------|
| `read` | Basic read access | Subscriber |
| `edit_posts` | Edit own posts | Author |
| `edit_others_posts` | Edit any post | Editor |
| `publish_posts` | Publish own posts | Author |
| `manage_options` | Plugin/theme settings | Administrator |
| `manage_categories` | Manage post categories | Editor |
| `delete_posts` | Delete own posts | Author |
| `edit_users` | Edit other users | Administrator |

### Example: Conditional UI Rendering

```php
if ( current_user_can( 'edit_others_posts' ) ) {
    ?>
    <a href="<?php echo esc_url( add_query_arg( array( 'action' => 'delete', 'post' => get_the_ID() ), home_url() ) ); ?>">
        <?php esc_html_e( 'Delete Post', 'my-plugin' ); ?>
    </a>
    <?php
}
```

### Example: Protecting Logic

```php
add_action( 'init', 'myplugin_handle_delete' );

function myplugin_handle_delete() {
    if ( ! isset( $_GET['action'] ) || 'delete' !== $_GET['action'] ) {
        return;
    }

    // Capability check — blocks all unauthorized requests
    if ( ! current_user_can( 'edit_others_posts' ) ) {
        wp_die( esc_html__( 'Insufficient permissions.', 'my-plugin' ) );
    }

    $post_id = isset( $_GET['post'] ) ? absint( $_GET['post'] ) : 0;
    if ( ! get_post( $post_id ) ) {
        wp_die( esc_html__( 'Post not found.', 'my-plugin' ) );
    }

    wp_trash_post( $post_id );
    wp_redirect( admin_url( 'edit.php' ) );
    exit;
}
```

> **Note:** Capability checks must be paired with nonce verification for form submissions and AJAX requests. See `nonces.md`.
