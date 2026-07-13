# My Plugin (Skeleton)

A minimal WordPress plugin skeleton demonstrating best practices for security, structure, and hook usage.

## Quick Start

1. Copy this entire directory to `/wp-content/plugins/my-plugin/`
2. Edit `my-plugin.php` — replace all placeholder values:
   - **Plugin Name**: Your plugin's display name
   - **Text Domain**: Replace `my-plugin` with your unique slug
   - **Prefix**: Replace all `MAP_` prefixes with your own 2–3 letter prefix
3. Activate the plugin in WordPress admin

## What's Included

| File | Purpose |
|------|---------|
| `my-plugin.php` | Main plugin file with header, hooks, admin menu, settings, shortcode, and AJAX example |
| `uninstall.php` | Runs on plugin deletion — cleans options, tables, transients |

## Sections in `my-plugin.php`

1. **Plugin Header** — Valid WP.org header block
2. **Constants** — Version, directory paths
3. **Activation Hook** — Default options, rewrite flush
4. **Deactivation Hook** — Rewrite flush (no data deletion)
5. **Initialization** — Text domain loading
6. **Admin Menu** — Top-level + submenu pages with capability checks
7. **Settings API** — Registration, sections, fields, validation
8. **Shortcode** — `[my_greeting name="World"]` example with sanitization/escaping
9. **AJAX Handler** — Nonce verification + capability check pattern

## Security Checklist (Already Implemented)

- [x] Sanitize all input (`sanitize_text_field()`)
- [x] Escape all output (`esc_html()`, `esc_attr()`, `esc_url()`)
- [x] Verify nonces on forms and AJAX
- [x] Check capabilities (`current_user_can()`)
- [x] Prevent direct file access
- [x] Use Settings API (never raw form handling)

## Next Steps

After using this skeleton:

1. Add your plugin's specific functionality
2. Register custom post types or taxonomies if needed (see `references/custom-post-types/` and `references/taxonomies/`)
3. Create REST API endpoints (see `references/rest-api/`)
4. Add internationalization strings (`__()`, `_e()`) throughout
5. Create a `readme.txt` for WP.org submission

## License

GPL-2.0+ — Same license as WordPress core.
