# System Cron Integration

WP-Cron runs on page load, which can cause delays or missed executions for time-sensitive tasks. For production sites, replace WP-Cron with a real system scheduler.

## Step 1: Disable WP-Cron

Add to `wp-config.php` before `require_once( ABSPATH . 'wp-settings.php' );`:

```php
define( 'DISABLE_WP_CRON', true );
```

## Step 2: Configure System Cron

### Linux / macOS (crontab)

```bash
# Edit crontab
crontab -e

# Add entry — runs every 15 minutes
*/15 * * * * wget -q -O - http://your-site.com/wp-cron.php?doing_wp_cron >/dev/null 2>&1
```

**Crontab syntax:** `minute hour day-of-month month day-of-week command`

| Field | Value Range | Example |
|-------|-------------|---------|
| Minute | 0–59 | `*/15` = every 15 min |
| Hour | 0–23 | `2` = at 2 AM |
| Day of month | 1–31 | `*` = every day |
| Month | 1–12 | `*` = every month |
| Day of week | 0–7 (0,7=Sunday) | `1-5` = weekdays |

**Common examples:**

```bash
# Every 15 minutes
*/15 * * * * wget -q -O - http://example.com/wp-cron.php?doing_wp_cron >/dev/null 2>&1

# Daily at midnight
0 0 * * * wget -q -O - http://example.com/wp-cron.php?doing_wp_cron >/dev/null 2>&1

# Every hour on the hour
0 * * * * wget -q -O - http://example.com/wp-cron.php?doing_wp_cron >/dev/null 2>&1
```

### Windows (Task Scheduler)

Create a Basic Task and use PowerShell:

```powershell
Invoke-WebRequest http://your-site.com/wp-cron.php?doing_wp_cron
```

### Alternative HTTP Tools

| Tool | Command | Notes |
|------|---------|-------|
| `wget` | `wget -q -O - URL` | `-q` quiet, `-O -` no file output |
| `curl` | `curl -s URL` | `-s` silent mode |
| `lynx` | `lynx -dump URL` | Text browser |

> **Note:** Use `?doing_wp_cron` to prevent race conditions. Without it, concurrent requests may trigger multiple simultaneous cron runs.
