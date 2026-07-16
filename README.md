# WordPress Plugin Development Skill

An expert AI agent skill for creating secure, well-structured WordPress plugins following WP.org standards.

## Overview

> 🔗 **New to AI Agent Skills?** If you're unfamiliar with how `SKILL.md` files work, how agents discover and load them, or want to learn more about building your own skills — start at **[agentskills.io/home](https://agentskills.io/home)**. It's the central hub for understanding the skill ecosystem, from installation to advanced customization.

This skill package provides everything needed to develop production-ready WordPress plugins — from scaffolding and security checklists to advanced patterns like REST APIs, custom post types, and cron scheduling. It's designed for AI agents but can also serve as a reference guide for developers.

> **Source:** This skill is derived and optimized from the:
> - [WordPress.org official Plugin Handbook](https://developer.wordpress.org/plugins/) (Last updated June 12, 2024).
> - [WordPress.org official Fundamentals of Block Development - Block Editor Handbook](https://developer.wordpress.org/block-editor/getting-started/fundamentals/) (Last updated December 14, 2023).
> Content has been restructured for AI agent consumption with progressive disclosure, actionable checklists, and automated validation patterns.

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
│   ├── block-editor/                 # Block editor & custom blocks
│   ├── hooks/                        # Action/filter workflows
│   ├── settings/                     # Settings API patterns
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
- Block Editor & Custom Blocks

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

- **PHP 8.2+** — All code examples use modern PHP syntax (short arrays, typed parameters)
- WordPress 6.0+
- Python 3.8+ (optional for security validator script)

## Acknowledgements

This skill was built with assistance from [Qwen3.6-35B-A3B](https://qwen.ai/blog?id=qwen3.6-35b-a3b):

```bibtex
@misc{qwen36_35b_a3b,
    title = {{Qwen3.6-35B-A3B}: Agentic Coding Power, Now Open to All},
    url = {https://qwen.ai/blog?id=qwen3.6-35b-a3b},
    author = {{Qwen Team}},
    month = {April},
    year = {2026}
}
```

## License

GPL-2.0+ — Same license as WordPress itself.

## Authors

- [M.Pribadi](https://github.com/muslimpribadi)
- [LUNA bot](https://github.com/luna-bot-agent)

---

*For AI agent usage, the `SKILL.md` file is the entry point. Reference subdirectories are loaded on-demand based on plugin requirements.*
