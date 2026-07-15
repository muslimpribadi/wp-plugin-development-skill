---
name: wordpress-plugin-development
description: >
  Expert WordPress plugin development skill. Guides the creation of secure,
  well-structured plugins following WP.org standards.
  PHP 8.2+ compatible — type declarations, strict types, constructor promotion,
  match expressions, and modern string functions throughout.
  Covers basic aspects (structure, hooks, security, admin menus, shortcodes, settings)
  and extends to advanced topics (CPTs, REST API, Cron, i18n, HTTP API, privacy,
  block editor/Gutenberg development).
license: GPL-2.0+
compatibility: Requires PHP 8.2+, WordPress 6.4+ environment
metadata:
  author: M. Pribadi, LUNA bot
  version: 1.3.0
  source: wp plugin handbook, wp block editor handbook
---

# WordPress Plugin Development Skill

## When to Use This Skill

Use when the user wants to create a new WordPress plugin, extend an existing one, or needs guidance on WordPress plugin development best practices. Always begin with **Basic Aspects** and add **Extended Aspects** only when the plugin's goals require them.

---

## Basic Aspects (Always Apply)

These steps form the foundation of every WordPress plugin. Implement these first before considering any Extended Aspect.

### 1. Plugin Structure & Naming Conventions

- Create a unique folder under `/wp-content/plugins/` using a lowercase-slug name with hyphens (e.g., `my-awesome-plugin`).
- The main plugin file must share the same slug and be placed at the root of the folder (e.g., `my-awesome-plugin.php`).
- Use a unique prefix (2–3 letters) for all functions, classes, hooks, and text domains to avoid collisions.
  ```php
  // Prefix example: MAP (My Awesome Plugin)
  function map_sanitize_input( string $value ): string {
      return sanitize_text_field( $value );
  }
  add_action( 'map_init', 'map_load_textdomain' );
  ```
- Organize additional code into a `/src/` directory with subfolders by concern.

### 2. Plugin Header & Metadata

Every main plugin file requires this header block:

```php
<?php
/**
 * Plugin Name:       My Awesome Plugin
 * Plugin URI:        https://example.com/my-awesome-plugin
 * Description:       A brief description of what this plugin does.
 * Version:           1.0.0
 * Author:            Your Name
 * Author URI:        https://example.com
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       my-awesome-plugin
 * Requires at least: 6.4
 * Requires PHP:      8.2
 */
declare(strict_types=1);
```

### 3. Hook Workflow (Actions & Filters)

All plugin logic must be attached to WordPress hooks — never execute code at the top level of the main file.

- **Activation**: Register with `register_activation_hook()`. Use for DB table creation, option defaults, rewrite flush.
- **Deactivation**: Register with `register_deactivation_hook()`. Clean up temporary data, do NOT delete user data or options.
- **Uninstall**: Provide an `uninstall.php` file in the plugin root. Runs only when the user deletes the plugin. Delete all options and temp data here.
- **Initialization**: Hook into `plugins_loaded` for text domain loading, `init` for CPTs/taxonomies registration, `admin_init` for settings registration.

```php
// Activation
register_activation_hook( __FILE__, 'map_activate' );
function map_activate(): void {
    // Create DB tables, set defaults
}

// Deactivation
register_deactivation_hook( __FILE__, 'map_deactivate' );
function map_deactivate(): void {
    // Flush rewrite rules, clear caches
}

// Init hook
add_action( 'init', 'map_init' );
function map_init(): void {
    load_plugin_textdomain( 'my-awesome-plugin', false, dirname( plugin_basename( __FILE__ ) ) . '/languages' );
}
```

### 4. PHP 8.2+ Compatibility Requirements

All generated code MUST comply with these rules:

- **`declare(strict_types=1);`** — Required at the top of every PHP file (after `<?php`).
- **Type declarations on all functions** — Every parameter and return type must be declared. Use `void` for functions that don't return a value.
  ```php
  // BAD: No types
  function my_function( $value ) { ... }
  
  // GOOD: PHP 8.2+
  function my_function( string $value ): string {
      return sanitize_text_field( $value );
  }
  ```
- **Constructor property promotion** — Use PHP 8.0+ constructor shorthand:
  ```php
  // BAD (pre-8.0)
  class MyClass {
      public string $name;
      public int $count;
      public function __construct( string $name, int $count ) {
          $this->name = $name;
          $this->count = $count;
      }
  }
  
  // GOOD (PHP 8.0+)
  class MyClass {
      public function __construct(
          public string $name,
          public int $count,
      ) {}
  }
  ```
- **Match expressions** — Prefer `match()` over `switch()` or ternary chains:
  ```php
  // BAD: Nested ternary
  $status = $role === 'admin' ? 'full' : ($role === 'editor' ? 'partial' : 'none');
  
  // GOOD: Match expression (PHP 8.0+)
  $status = match( $role ) {
      'admin'   => 'full',
      'editor'  => 'partial',
      default   => 'none',
  };
  ```
- **Modern string functions** — Replace `strpos() === false` patterns:
  ```php
  // BAD: Pre-PHP 8.0
  if ( strpos( $haystack, 'needle' ) === false ) { ... }
  
  // GOOD: PHP 8.0+
  if ( ! str_contains( $haystack, 'needle' ) ) { ... }
  if ( str_starts_with( $haystack, 'prefix' ) ) { ... }
  if ( str_ends_with( $haystack, 'suffix' ) ) { ... }
  ```
- **Short array syntax** — Always use `[]` instead of `array()`.
- **Named arguments** — Use PHP 8.0+ named arguments for WordPress function calls with many parameters:
  ```php
  // GOOD: Named args for clarity
  add_menu_page(
      page_title: __( 'My Plugin', 'my-plugin' ),
      menu_title: __( 'My Plugin', 'my-plugin' ),
      capability: 'manage_options',
      menu_slug: 'my-plugin',
      callback: 'my_callback',
  );
  ```
- **Nullsafe operator** — Use `?->` for chained property access:
  ```php
  $title = $_GET['title']?->get( 'default' );
  ```
- **Null coalescing assignment** — Use `??=` for default value assignment:
  ```php
  $options['key'] ??= 'default_value';
  ```
- **Enums (PHP 8.1+)** — Use `enum` for fixed sets of values (WordPress 6.4+ supports PHP 8.1+):
  ```php
  enum PostStatus: string {
      case Draft = 'draft';
      case Publish = 'publish';
      case Pending = 'pending';
  }
  ```

> **Rule:** If a WordPress function has optional parameters, always use named arguments to document intent. Never leave parameter positions ambiguous.

### 5. Security Checklist (Non-Negotiable)

Every plugin MUST follow these security rules:

- [ ] **Sanitize input** — `sanitize_text_field()`, `absint()`, `sanitize_email()`, etc. — On every `$_GET`, `$_POST`, `$_COOKIE`, `$_FILES` value before use
- [ ] **Escape output** — `esc_html()`, `esc_attr()`, `esc_url()`, `wp_kses()` — On every value rendered to the browser
- [ ] **Verify nonces** — `wp_verify_nonce()`, `check_admin_referer()` — On all form submissions and AJAX requests
- [ ] **Check capabilities** — `current_user_can()`, `map_meta_cap` filter — Before any admin action or data modification
- [ ] **Prevent direct access** — `if ( ! defined( 'WP_USE_THEMES' ) || ! defined( 'ABSPATH' ) ) exit;` — At the top of every PHP file
- [ ] **Use prepared statements** — `$wpdb->prepare()` — On all SQL queries involving user data

## Validation Loop

After generating code, run this self-check:

1. **Scan for unsanitized input**: grep for `$_GET`, `$_POST`, `$_REQUEST` → ensure every instance is wrapped in a sanitization function
2. **Scan for unescaped output**: grep for `echo`, `print`, `?>` → ensure every instance uses an escaping function
3. **Verify nonces**: Check all form handlers and AJAX actions have `check_admin_referer()` or `verify_nonce()`
4. **Check capabilities**: Verify all admin pages use `current_user_can()` with appropriate capability strings
5. **Validate SQL**: Ensure `$wpdb->prepare()` is used on ALL database queries, even those without user input
6. **Confirm escaping in wp_die()**: Any `wp_die()` message must be escaped
7. **Verify PHP 8.2+ compliance**:
   - Every `.php` file starts with `<?php\ndeclare(strict_types=1);`
   - All functions have parameter types and return types declared
   - No `array()` literals — use `[]` everywhere
   - No `strpos() === false` — use `! str_contains()` instead
   - No bare `return;` in non-void functions (must be explicit `: void`)

If any check fails, fix the code before delivery.

```php
// Sanitize + Escape example
$input = sanitize_text_field( $_POST['my_field'] ?? '' );
echo esc_html( $input );

// Nonce verification example (PHP 8.0+ nullsafe operator)
$nonce = $_POST['my_nonce'] ?? null;
if ( ! $nonce || ! wp_verify_nonce( $nonce, 'my_action' ) ) {
    wp_die( esc_html__( 'Security check failed.', 'my-plugin' ) );
}

// Capability check example
if ( ! current_user_can( 'manage_options' ) ) {
    wp_die( esc_html__( 'You do not have sufficient permissions.', 'my-plugin' ) );
}
```

### 5. Administration Menu Creation

Use the WordPress Admin Menu API to create menu pages:

```php
add_action( 'admin_menu', 'map_admin_menu' );
function map_admin_menu(): void {
    // Top-level menu (PHP 8+ named arguments for clarity)
    add_menu_page(
        page_title: __( 'My Plugin', 'my-plugin' ),
        menu_title: __( 'My Plugin', 'my-plugin' ),
        capability: 'manage_options',
        menu_slug: 'my-plugin',
        callback: 'map_render_admin_page',
        icon_url: 'dashicons-admin-generic',
        position: 25,
    );

    // Submenu page
    add_submenu_page(
        parent_slug: 'my-plugin',
        page_title: __( 'Settings', 'my-plugin' ),
        menu_title: __( 'Settings', 'my-plugin' ),
        capability: 'manage_options',
        menu_slug: 'my-plugin-settings',
        callback: 'map_render_settings_page',
    );
}
```

### 6. Settings API Implementation

Use the Settings API for all admin option pages — never write raw `<form>` tags:

```php
add_action( 'admin_init', 'map_register_settings' );
function map_register_settings(): void {
    register_setting( 'map_settings_group', 'map_option_name', [
        'type'              => 'string',
        'sanitize_callback' => 'sanitize_text_field',
        'default'           => '',
    ] );
}

function map_render_settings_page(): void {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }
    ?>
    <div class="wrap">
        <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
        <form method="post" action="options.php">
            <?php
            settings_fields( 'map_settings_group' );
            do_settings_sections( 'map-settings' );
            submit_button();
            ?>
        </form>
    </div>
    <?php
}
```

### 7. Shortcode Implementation

Use the Shortcode API to add user-facing content blocks:

```php
add_shortcode( 'my_shortcode', 'map_my_shortcode' );
function map_my_shortcode( array $atts ): string {
    $atts = shortcode_atts( [
        'title'   => 'Default Title',
        'count'   => 5,
        'orderby' => 'date',
    ], $atts, 'my_shortcode' );

    // Sanitize attributes (PHP 8.2+ str_starts_with / str_contains examples)
    $title   = esc_html( sanitize_text_field( $atts['title'] ?? '' ) );
    $count   = absint( $atts['count'] ?? 0 );
    $orderby = in_array( $atts['orderby'] ?? 'date', ['date', 'title', 'rand'], true )
        ? $atts['orderby']
        : 'date';

    // Build output safely
    ob_start();
    ?>
    <div class="my-shortcode">
        <h2><?php echo $title; ?></h2>
        <p>Showing <?php echo $count; ?> items ordered by <?php echo $orderby; ?>.</p>
    </div>
    <?php
    return ob_get_clean();
}
```

---


## Gotchas

Common WordPress pitfalls that break plugins when overlooked:

- **`$wpdb->prepare()` is mandatory for ALL queries** — Even queries with hardcoded values should use it. `$wpdb->get_results("SELECT * FROM {$wpdb->posts} WHERE post_status = 'publish'")` → WRONG. Use `$wpdb->get_results($wpdb->prepare("SELECT * FROM {$wpdb->posts} WHERE post_status = %s", 'publish'))`
- **`flush_rewrite_rules()` only on activation/deactivation** — Calling it on every request kills performance. Never put it in a hook that fires on page load.
- **Text domain must load on `plugins_loaded`** — Loading via `init` is too late for some translation functions. Use: `add_action('plugins_loaded', function() { load_plugin_textdomain('my-plugin', false, dirname(plugin_basename(__FILE__)) . '/languages'); });`
- **Nonces expire after 24 hours** — Always generate fresh nonces with each page load via `wp_create_nonce()`. Never cache nonce values.
- **`wp_die()` messages must be escaped** — `wp_die('Error: ' . $user_input)` → WRONG. Use `wp_die(esc_html('Error: ') . esc_html($user_input))`
- **`update_option()` triggers autoload changes** — Large options should use `'no'` autoload: `update_option('my_large_option', $data, 'no')`
- **Missing `declare(strict_types=1)`** — Every PHP file must start with `<?php\ndeclare(strict_types=1);`. Without it, type declarations are coerced, not enforced.
- **Missing return types on hooks** — WordPress hook callbacks that don't return values must declare `: void` to prevent accidental output.
- **Using `strpos() === false` instead of `! str_contains()`** — PHP 8.0+ provides `str_contains()`, `str_starts_with()`, and `str_ends_with()` for readable, bug-free string checks.

## Extended Aspects (Apply as Needed)

Reference these sections only when the plugin's goals require them. Use the lookup table below to find the relevant `references/` subdirectory.

| Plugin Goal | Reference Directory | Key Topics |
|-------------|-------------------|------------|
| Register new post types | `references/custom-post-types/` | `register_post_type()`, supports, capabilities |
| Register custom taxonomies | `references/taxonomies/` | `register_taxonomy()`, hierarchical vs flat |
| Create REST API endpoints | `references/rest-api/` | `register_rest_route()`, permissions, routing |
| Schedule periodic tasks | `references/cron/` | `wp_schedule_event()`, triggers, hooks |
| Make plugin translatable | `references/internationalization/` | `__()`, `_e()`, text domains, POT files |
| Make external HTTP requests | `references/http-api/` | `wp_remote_get()`, `wp_remote_post()`, error handling |
| Create custom database tables | `references/database/` | `$wpdb`, `$dbDelta`, data types, queries |
| Manage user roles & caps | `references/users/` | `add_role()`, `add_cap()`, capability mapping |
| Enqueue JS/CSS assets | `references/javascript/` | `wp_enqueue_script()`, `wp_localize_script()` |
| Handle privacy/export data | `references/privacy/` | Privacy policies, export/erase hooks |
| Create Gutenberg blocks | `references/block-editor/` | Blocks, block.json, editor UI, static/dynamic render |
| Plugin readme & WP.org prep | `references/metadata/` | `readme.txt` fields, WP.org guidelines |

### Block Editor Development

Gutenberg is the default WordPress editor as of WP 5.0+. Blocks are the fundamental unit — combining markup, styles, and behavior into reusable components.

#### Project Structure

```
my-plugin/
├── src/                  # Source files (never commit to production)
│   ├── my-block.js       # Block registration & behavior
│   ├── my-block.scss     # Editor + frontend styles
│   └── editor.scss       # Editor-only styles
├── build/                # Compiled output (deploy this)
│   ├── my-block.asset.php
│   ├── my-block.js
│   └── my-block.css
├── block.json            # Block metadata (auto-enqueues build files)
└── README.md
```

#### `block.json` — The Block Manifest

The single source of truth for block metadata. WordPress 5.0+ auto-registers blocks when this file is present.

```json
{
    "$schema": "https://schemas.wp.org/trunk/block.json",
    "apiVersion": 3,
    "name": "my-plugin/my-block",
    "title": "My Custom Block",
    "category": "design",
    "icon": "smiley",
    "description": "A custom block that does something useful.",
    "supports": {
        "html": false,
        "align": ["wide", "full"],
        "color": { "gradients": true, "link": true },
        "spacing": { "margin": true, "padding": true, "blockGap": true },
        "typography": { "fontSize": true, "lineHeight": true }
    },
    "attributes": {
        "content": { "type": "string", "source": "html" },
        "alignment": { "type": "string", "default": "left" }
    },
    "textdomain": "my-plugin",
    "editorScript": "file:./build/my-block.js",
    "script": "file:./build/my-block.asset.php",
    "style": "file:./build/my-block.css",
    "editorStyle": "file:./build/my-block.css"
}
```

#### Block Registration (PHP + JS)

**PHP-side registration** (recommended for WP 6.8+):

```php
add_action('init', 'myplugin_register_blocks');
function myplugin_register_blocks(): void {
    register_block_type_from_registry('my-plugin/my-block', [
        'style'         => 'my-plugin-block-style',
        'editor_style'  => 'my-plugin-editor-style',
        'script'        => 'my-plugin-block-script',
        'editor_script' => 'my-plugin-editor-script',
    ]);
}
```

**JS-side registration** (traditional):

```js
// src/my-block.js
import { registerBlockType } from '@wordpress/blocks';
import './style.scss';
import metadata from './block.json';

registerBlockType(metadata.name, {
    edit: function Edit(props) { return <div>...</div>; },
    save: function Save() { return <p>Static output</p>; }, // omit for dynamic
});
```

#### The Block Wrapper

Every block is wrapped in a `<div>` by default. Use `useBlockProps` to merge attributes into the wrapper.

**JSX (edit mode):**

```js
import { useBlockProps } from '@wordpress/block-editor';

export function edit(props) {
    return (
        <div {...useBlockProps()}>
            <p>Hello World</p>
        </div>
    );
}
```

**PHP (dynamic render):**

```php
function myplugin_render_block( array $attributes, string $content ): string {
    $wrapperAttrs = get_block_wrapper_attributes();
    return "<div {$wrapperAttrs}>{$content}</div>";
}
```

#### Editor UI Components

**Block Toolbar** — context-sensitive actions above the block:

```js
import { BlockControls, InspectorControls } from '@wordpress/block-editor';
import { ToolbarGroup, ToolbarButton, ToggleControl } from '@wordpress/components';

function Edit(props) {
    const { attributes: { bold }, setAttributes } = props;
    return (
        <>
            <BlockControls>
                <ToolbarGroup>
                    <ToolbarButton
                        icon={bold ? 'editor-bold' : 'editor-italic'}
                        isActive={bold}
                        onClick={() => setAttributes({ bold: !bold })}
                    />
                </ToolbarGroup>
            </BlockControls>
            <InspectorControls>
                <PanelBody title="Settings">
                    <ToggleControl
                        label="Bold"
                        checked={bold}
                        onChange={(v) => setAttributes({ bold: v })}
                    />
                </PanelBody>
            </InspectorControls>
            <div {...useBlockProps()}>{/* block content */}</div>
        </>
    );
}
```

**Control Patterns:**
| Control | Use For |
|---------|----------|
| `TextControl` | Short text input |
| `TextareaControl` | Multi-line text |
| `SelectControl` | Dropdown selection |
| `ColorPalette` | Color picker |
| `PanelBody` | Collapsible sidebar sections |
| `RangeControl` | Slider with min/max/step |

#### Static vs Dynamic Rendering

| Approach | How It Works | Best For |
|----------|-------------|----------|
| **Static** (`save` returns JSX) | Rendered at edit time, stored in post content as HTML | Simple, predictable output |
| **Dynamic** (`render_callback`) | PHP renders on every page load | Personalized data, queries, API calls |
| **Hybrid** (static save + dynamic fallback) | Static for editor/preview, dynamic for final render | Complex blocks needing both |

**Dynamic block example:**

```php
function myplugin_render_dynamic( array $attributes, string $content ): string {
    $posts = get_posts(['post_type' => 'product', 'numberposts' => 3]);
    $output = '<ul>';
    foreach ($posts as $post) {
        // PHP 8.2+ str_contains for readability
        if ( str_starts_with($post->post_title, 'Featured') ) {
            continue; // Skip featured items
        }
        $output .= '<li>' . esc_html($post->post_title) . '</li>';
    }
    $output .= '</ul>';
    return $output;
}
```

#### JavaScript Execution Contexts

| Context | How It Runs | Use Case |
|---------|-------------|----------|
| **Build Process** (Webpack/Vite) | `npm run build` compiles JSX → JS + SCSS → CSS | Standard block development |
| **No Build** (`wp-scripts start`) | Live-reload dev server | Rapid prototyping |
| **Inline `<script>`** | Enqueued directly in admin page, no build step | Simple scripts, small plugins |

#### Standalone Block Editor

Use the Block Editor in custom admin pages or frontend:

```php
add_action('admin_menu', 'myplugin_add_editor_page');
function myplugin_add_editor_page(): void {
    add_menu_page(
        page_title: 'My Editor',
        menu_title: 'My Editor',
        capability: 'manage_options',
        menu_slug: 'my-editor-page',
        callback: 'myplugin_render_editor',
    );
}

function myplugin_render_editor(): void {
    ?>
    <div id="my-custom-editor"></div>
    <?php
}

add_action('admin_enqueue_scripts', 'myplugin_enqueue_editor_assets');
function myplugin_enqueue_editor_assets( string $hook ): void {
    if ( $hook !== 'toplevel_page_my-editor-page' ) {
        return;
    }
    wp_enqueue_script(
        'my-editor-script',
        plugins_url('build/editor.js', __FILE__),
        ['wp-block-editor', 'wp-blocks', 'wp-components'],
        filemtime(plugin_dir_path(__FILE__) . 'build/editor.js')
    );
}
```

```js
// src/editor.js
import { createRoot } from '@wordpress/element';
import { BlockEditorProvider, BlockEditorKeyboardShortcuts } from '@wordpress/block-editor';
import { __ } from '@wordpress/i18n';

const root = createRoot(document.getElementById('my-custom-editor'));
root.render(
    <BlockEditorProvider
        contentInitial={{ blocks: [], blockNamespaces: {} }}
        settings={{ title: __('My Editor', 'my-plugin') }}
    >
        <BlockEditorKeyboardShortcuts />
    </BlockEditorProvider>
);
```

> **Tip:** Use `@wordpress/block-editor` exports like `RichText`, `MediaUpload`, `InspectorControls`, and `useBlockProps` for building custom editor experiences.

---

## Reference Lookup Guide

When the user specifies what their plugin should do, map it to the appropriate reference directory:

```
User says: "I want a plugin that manages events"
→ Basic Aspects (structure, hooks, security, admin menu, settings)
→ Extended: custom-post-types (events as CPT), taxonomies (event categories), cron (reminders), rest-api (event listings)

User says: "I need a plugin that sends weekly email reports"
→ Basic Aspects
→ Extended: cron (weekly schedule), http-api (sending emails), javascript (admin dashboard)

User says: "I want a plugin with a custom shortcode and settings page"
→ Basic Aspects only (shortcodes + settings are covered in Basic)

User says: "I need to create a REST API for my custom data"
→ Basic Aspects
→ Extended: rest-api, database, users (permissions)
```

---

## Skeleton Usage

Bootstrap your plugin from the template at `assets/plugin-skeleton/`:

1. Copy the `assets/plugin-skeleton/` directory and rename it to your plugin slug.
2. Edit the plugin header in the main PHP file with your plugin's name, description, and author info.
3. Replace all instances of the placeholder prefix (`MAP_`) with your own 2–3 letter prefix.
4. Replace `my-plugin` text domain with your plugin slug.
5. Add your specific hooks, shortcodes, admin pages, and settings.

The skeleton includes:
- Valid WP plugin header
- Activation/deactivation/uninstall hooks
- Admin menu + submenu structure
- Settings API registration
- A working shortcode example
- Proper security scaffolding (nonce checks, capability checks)
- Text domain loading

---

## Quick Reference: Security Functions

| Purpose | Function |
|---------|----------|
| Sanitize text | `sanitize_text_field()` |
| Sanitize integer | `absint()`, `intval()` |
| Sanitize email | `sanitize_email()` |
| Sanitize URL | `esc_url_raw()` |
| Sanitize textarea | `sanitize_textarea_field()` |
| Escape HTML | `esc_html()` |
| Escape attribute | `esc_attr()` |
| Escape URL output | `esc_url()` |
| Escape with allowed tags | `wp_kses()` |
| Verify nonce | `wp_verify_nonce()` |
| Check capability | `current_user_can()` |
| Prepare SQL | `$wpdb->prepare()` |

Full sanitization/escaping reference: see `references/plugin-security/`
