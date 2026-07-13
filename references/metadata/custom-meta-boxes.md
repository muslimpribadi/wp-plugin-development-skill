# Custom Meta Boxes

## Adding a Meta Box

```php
add_meta_box( string $id, string $title, callable $callback, string $screen, string $context = 'advanced', string $priority = 'default', array $callback_args = null )
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `$id` | string | Yes | — | Unique identifier for the meta box (use prefix: `myplugin_box_id`) |
| `$title` | string | Yes | — | Title displayed in the meta box header |
| `$callback` | callable | Yes | — | Function that outputs the HTML content of the box |
| `$screen` | string\|array | Yes | — | Post type(s) to show the box on (e.g., `'post'`, `['post', 'page']`) |
| `$context` | string | No | `'advanced'` | Where to render: `'normal'`, `'side'`, `'advanced'` |
| `$priority` | string | No | `'default'` | Ordering within context: `'high'`, `'core'`, `'default'`, `'low'` |

### Example

```php
add_action( 'add_meta_boxes', 'myplugin_add_meta_box' );

function myplugin_add_meta_box() {
    add_meta_box(
        'myplugin_meta_box',      // ID
        'My Plugin Settings',     // Title
        'myplugin_render_box',    // Callback
        'post',                   // Screen (post type)
        'normal',                 // Context
        'default'                 // Priority
    );
}

function myplugin_render_box( $post ) {
    ?>
    <label for="myplugin_field">Description</label>
    <select name="myplugin_field" id="myplugin_field">
        <option value="">Select...</option>
        <option value="a">Option A</option>
        <option value="b">Option B</option>
    </select>
    <?php
}
```

## Rendering Meta Box HTML

Meta box HTML is rendered inside the post edit form — no submit button needed. Pre-populate values with `get_post_meta()`:

```php
function myplugin_render_box( $post ) {
    // Nonce field for security
    wp_nonce_field( 'myplugin_save', 'myplugin_nonce' );

    $value = get_post_meta( $post->ID, '_myplugin_value', true );
    ?>
    <label for="myplugin_field">Description</label>
    <select name="myplugin_field" id="myplugin_field">
        <option value="">Select...</option>
        <option value="a" <?php selected( $value, 'a' ); ?>>Option A</option>
        <option value="b" <?php selected( $value, 'b' ); ?>>Option B</option>
    </select>
    <?php
}
```

### Key Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `get_post_meta()` | Retrieve saved meta value | `get_post_meta( $post->ID, '_key', true )` |
| `selected()` | Output `selected` attribute if values match | `<?php selected( $value, 'a' ); ?>` |
| `checked()` | Output `checked` attribute if values match | `<?php checked( $value, 1 ); ?>` |
| `disabled()` | Output `disabled` attribute if values match | `<?php disabled( $value, 1 ); ?>` |

## Saving Meta Box Values

Hook into `save_post` with nonce verification and capability check:

```php
add_action( 'save_post', 'myplugin_save_meta_box', 10, 2 );

function myplugin_save_meta_box( $post_id, $post ) {
    // 1. Verify nonce
    if ( ! isset( $_POST['myplugin_nonce'] ) ||
         ! wp_verify_nonce( $_POST['myplugin_nonce'], 'myplugin_save' ) ) {
        return;
    }

    // 2. Check autosave
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }

    // 3. Check user capability
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }

    // 4. Save the value
    if ( isset( $_POST['myplugin_field'] ) ) {
        update_post_meta(
            $post_id,
            '_myplugin_value',
            sanitize_text_field( $_POST['myplugin_field'] )
        );
    }
}
```

### save_post Hook Notes

| Consideration | Detail |
|---------------|--------|
| Fires multiple times | A single page update can trigger `save_post` more than once (revisions, autosave) |
| `$post` object passed | Available as second parameter since WP 2.7 — use it for post type checks |
| Always check nonce + capability | Required for security |

## Removing Meta Boxes

```php
remove_meta_box( string $id, string $screen, string $context )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$id` | string | Yes | The exact ID used when adding the box |
| `$screen` | string | Yes | Post type where it was added |
| `$context` | string | Yes | Context where it was added |

```php
add_action( 'add_meta_boxes', 'myplugin_remove_default_box' );

function myplugin_remove_default_box() {
    remove_meta_box( 'postcustom', 'post', 'normal' );
}
```

## Complete OOP Pattern

For complex plugins, use a class-based approach:

```php
class MyPlugin_Meta_Box {
    public static function register() {
        add_action( 'add_meta_boxes', [ self::class, 'add' ] );
        add_action( 'save_post', [ self::class, 'save' ], 10, 2 );
    }

    public static function add() {
        add_meta_box(
            'myplugin_meta_box',
            'My Plugin Settings',
            [ self::class, 'render' ],
            'post',
            'normal',
            'default'
        );
    }

    public static function render( $post ) {
        wp_nonce_field( 'myplugin_save', 'myplugin_nonce' );
        $value = get_post_meta( $post->ID, '_myplugin_value', true );
        // ... render HTML with selected() / checked() helpers
    }

    public static function save( $post_id, $post ) {
        if ( ! isset( $_POST['myplugin_nonce'] ) ||
             ! wp_verify_nonce( $_POST['myplugin_nonce'], 'myplugin_save' ) ) {
            return;
        }
        if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) return;
        if ( ! current_user_can( 'edit_post', $post_id ) ) return;

        update_post_meta( $post_id, '_myplugin_value', sanitize_text_field( $_POST['myplugin_field'] ) );
    }
}

MyPlugin_Meta_Box::register();
```
