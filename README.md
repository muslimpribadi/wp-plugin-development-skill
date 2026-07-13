# WordPress Plugin Development Skill

An expert AI agent skill for creating secure, well-structured WordPress plugins following WP.org standards.

## Overview

This skill package provides everything needed to develop production-ready WordPress plugins — from scaffolding and security checklists to advanced patterns like REST APIs, custom post types, and cron scheduling. It's designed for AI agents but can also serve as a reference guide for developers.

> **Source:** This skill is derived and optimized from the [WordPress.org official Plugin Handbook](https://developer.wordpress.org/plugins/) (Last updated December 14, 2023). Content has been restructured for AI agent consumption with progressive disclosure, actionable checklists, and automated validation patterns.

## Quick Start

1. **Review the `SKILL.md`** — This is the main instruction file that guides plugin creation step-by-step.
2. **Bootstrap from the skeleton** — Copy `assets/plugin-skeleton/` and rename to your plugin slug.
3. **Run the security validator** — Use `scripts/verify_wp_plugin.py` to scan generated code for common vulnerabilities.

## Structure

```
wp-plugin-development-skill/
├── SKILL.md                          # Main skill definition & instructions
├── assets/
│   └── plugin-skeleton/              # Working plugin template
│       ├── my-plugin.php             # Main file with full scaffolding
│       ├── uninstall.php             # Cleanup on deletion
│       └── README.md                 # Skeleton usage guide
├── references/                       # Extended topic guides (19 subdirs)
│   ├── custom-post-types/            # CPT registration patterns
│   ├── taxonomies/                   # Custom taxonomies
│   ├── rest-api/                     # REST endpoint creation
│   ├── cron/                         # Scheduled task patterns
│   ├── internationalization/         # Translation & i18n
│   ├── http-api/                     # External HTTP requests
│   ├── database/                     # $wpdb, $dbDelta, queries
│   ├── users/                        # Roles, capabilities
│   ├── javascript/                   # Asset enqueueing
│   ├── privacy/                      # Privacy/export hooks
│   ├── metadata/                     # readme.txt & WP.org prep
│   ├── plugin-security/              # Sanitization, nonces, escaping
│   ├── admin-menus/                  # Admin page creation
│   ├── hooks/                        # Action/filter workflows
│   ├── settings/                     # Settings API patterns
│   └── ...                           # (and more)
├── scripts/
│   └── verify_wp_plugin.py           # Automated security scanner
└── .gitignore
```

## What's Covered

### Basic Aspects (Every Plugin)
- Plugin structure & naming conventions
- WP plugin header & metadata
- Hook workflow (activation, deactivation, init)
- Security checklist with validation loop
- Admin menu creation
- Settings API implementation
- Shortcode development

### Extended Topics (As Needed)
- Custom post types & taxonomies
- REST API endpoints
- Cron scheduling
- Internationalization (i18n)
- HTTP API integration
- Custom database tables
- User roles & capabilities
- JavaScript/CSS enqueueing
- Privacy compliance
- WP.org submission prep

## Security Features

This skill enforces a security-first approach:

- **Non-negotiable checklist** — Sanitization, escaping, nonces, capability checks
- **Validation loop** — Self-check procedure before code delivery
- **Gotchas section** — Common WP pitfalls to avoid
- **Automated scanner** — `verify_wp_plugin.py` detects unsanitized input, unescaped output, missing nonces, and SQL injection risks

## Requirements

- PHP 7.4+
- WordPress 6.0+
- Python 3.8+ (for security validator script)

## License

GPL-2.0+ — Same license as WordPress itself.

## Authors

- [M.Pribadi](https://github.com/muslimpribadi)
- [LUNA bot](https://github.com/luna-bot-agent)

---

*For AI agent usage, the `SKILL.md` file is the entry point. Reference subdirectories are loaded on-demand based on plugin requirements.*
