# WP Plugin Development Skill

A comprehensive AI agent skill for building secure, production-ready WordPress plugins.

## Requirements

- **PHP 8.2+** — All code examples use modern PHP syntax (short arrays, typed parameters, strict types)
- WordPress 6.0+
- Python 3.8+ (for security validator script)

## What's Covered

### Basic Aspects (Every Plugin)
- Plugin structure & naming conventions
- WP plugin header & metadata
- Hook workflow (activation, deactivation, init)
- Security checklist with validation loop
- Admin menu creation
- Settings API implementation
- Shortcode development

### PHP 8.2+ Modern Patterns (Enforced)
- **Short array syntax** — `[]` instead of `array()`
- **Typed parameters** — Type hints on all function parameters
- **Return type declarations** — `: void`, `: string`, `: array`, etc.
- **Strict types mode** — `declare(strict_types=1)` recommended
- **Match expressions** — Where appropriate for cleaner conditionals
- **Named arguments** — For improved readability in complex function calls

### Advanced Topics
- REST API endpoints & controllers
- Custom post types & taxonomies
- Database operations & table creation
- HTTP API integration
- Internationalization (i18n)
- Cron job scheduling

## Security Features

This skill enforces a security-first approach:

- **Non-negotiable checklist** — Sanitization, escaping, nonces, capability checks
- **Validation loop** — Self-check procedure before code delivery
- **Gotchas section** — Common WP pitfalls to avoid
- **Automated scanner** — `verify_wp_plugin.py` detects unsanitized input, unescaped output, missing nonces, and SQL injection risks

## Project Structure

```
wp-plugin-development-skill/
├── SKILL.md          # Main skill instructions (enforces all rules)
├── README.md         # This file
├── references/       # Topic-specific reference guides with code examples
│   ├── admin-menus/
│   ├── block-editor/
│   ├── cron/
│   ├── custom-post-types/
│   ├── database/
│   ├── hooks/
│   ├── http-api/
│   ├── internationalization/
│   ├── javascript/
│   ├── metadata/
│   ├── plugin-basics/
│   ├── plugin-security/
│   ├── privacy/
│   ├── rest-api/
│   ├── settings/
│   ├── shortcodes/
│   ├── taxonomies/
│   └── users/
├── assets/           # Plugin skeleton template with full implementation examples
│   └── plugin-skeleton/
└── verify_wp_plugin.py  # Automated security & PHP linting scanner
```

## Usage

1. Install the skill in your AI agent configuration
2. Reference `SKILL.md` for all development rules and enforcement policies
3. Use reference guides in `references/` for topic-specific examples
4. Use `assets/plugin-skeleton/` as a starting template for new plugins
5. Run `verify_wp_plugin.py <file.php>` to check security compliance

## Security Checklist (Enforced)

Every plugin MUST include:
- [ ] Sanitize ALL input (`sanitize_text_field`, `absint`, etc.)
- [ ] Escape ALL output (`esc_html`, `esc_attr`, `esc_url`)
- [ ] Verify nonces on all form submissions
- [ ] Check user capabilities before admin actions
- [ ] Use `$wpdb->prepare()` for all SQL queries
- [ ] No direct database access without proper escaping
