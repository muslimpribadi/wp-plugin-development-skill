# Settings API

The Settings API (added in WordPress 2.7) manages admin settings pages with form fields, sections, and validation. Called on the `admin_init` hook.

## Registration Functions

| Function | Purpose | Hook |
|----------|---------|------|
| `register_setting()` | Register a setting for validation/sanitization | `admin_init` |
| `unregister_setting()` | Remove a previously registered setting | `admin_init` |
| `add_settings_section()` | Add a section (group) to a settings page | `admin_init` |
| `add_settings_field()` | Add a field to a section on a page | `admin_init` |

## Form Rendering Functions

| Function | Purpose |
|----------|---------|
| `settings_fields()` | Output form fields + nonce for the registered setting group |
| `do_settings_sections()` | Output all sections/fields for the given page |
| `submit_button()` | Output the "Save Changes" button |

## Error Handling Functions

| Function | Purpose | Signature |
|----------|---------|-----------|
| `add_settings_error()` | Register a settings message | `add_settings_error( string $slug, string $code, string $message, string $type = 'error' )` |
| `get_settings_errors()` | Get all registered messages | `get_settings_errors( string $slug = '', bool $reset = true )` |
| `settings_errors()` | Display registered messages | `settings_errors( string $slug = '' )` |

## `$args` Keys for `add_settings_field()`

| Key | Purpose |
|-----|---------|
| `label_for` | Sets the `<label for="">` attribute on the field ID |
| `class` | CSS class applied to the `<tr>` wrapping the field |
| Any custom key | Passed through to your field callback as `$args['key']` |

## Error Types

| Type | Admin Color | Use Case |
|------|-------------|----------|
| `'error'` | Red border | Validation failure, save rejected |
| `'updated'` | Green border | Success message |
| `'warning'` | Yellow border | Non-critical notice |

## Quick Reference — Registration Flow

```php
// 1. Register setting (enables validation + auto-save)
register_setting( 'my_group', 'my_option', array(
    'type'              => 'string',
    'sanitize_callback' => 'sanitize_text_field',
) );

// 2. Add section (group heading + description)
add_settings_section( 'my_section', 'My Section Title', 'my_section_cb', 'my-page' );

// 3. Add field (individual input within section)
add_settings_field( 'my_field', 'Field Label', 'my_field_cb', 'my-page', 'my_section', array(
    'label_for' => 'my_field_input',
) );
```

## Form Template — Settings Page HTML

```php
<div class="wrap">
    <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>

    <?php settings_errors(); ?>

    <form action="options.php" method="post">
        <?php
        settings_fields( 'my_group' );      // Nonce + hidden fields
        do_settings_sections( 'my-page' );  // Sections and fields
        submit_button();
        ?>
    </form>
</div>
```

## Key Notes

| Consideration | Detail |
|---------------|--------|
| Form action | Always `options.php` — WordPress handles validation, sanitization, and saving automatically |
| Capability | Users need `manage_options` to submit settings (enforced by `options.php`) |
| Security | Nonces are auto-included via `settings_fields()` |
| Hook | Registration functions must run on `admin_init`, not directly in plugin load |
