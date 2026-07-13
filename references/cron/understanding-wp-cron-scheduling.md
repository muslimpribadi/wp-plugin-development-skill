# Understanding WP-Cron Scheduling

WP-Cron runs on page load (not a true system daemon). Each request checks for overdue events and executes them.

## Default Intervals

| Interval | Seconds | Description |
|----------|---------|-------------|
| `hourly` | 3600 | Every hour |
| `twicedaily` | 43200 | Twice daily (every 12 hours) |
| `daily` | 86400 | Once per day |
| `weekly` | 604800 | Once per week (WP 5.4+) |

## Custom Intervals

Add custom intervals via the `cron_schedules` filter:

```php
add_filter( 'cron_schedules', 'myplugin_add_cron_intervals' );

function myplugin_add_cron_intervals( $schedules ) {
    $schedules['five_seconds'] = array(
        'interval' => 5,
        'display'  => esc_html__( 'Every Five Seconds' ),
    );
    $schedules['every_fifteen_minutes'] = array(
        'interval' => 900,
        'display'  => esc_html__( 'Every Fifteen Minutes' ),
    );
    return $schedules;
}
```

> **Note:** All intervals are in seconds. Use `wp_get_schedules()` to list all available schedules at runtime.

## Disabling WP-Cron (Use System Cron)

WP-Cron adds overhead on every page load. For high-traffic sites, disable it and trigger via a real system cron:

```php
// In wp-config.php
define( 'DISABLE_WP_CRON', true );
```

Then add to your server's crontab:

```bash
# Every 15 minutes
*/15 * * * * wget -q -O - http://your-site.com/wp-cron.php?doing_wp_cron >/dev/null 2>&1
```

Or via PowerShell (Windows):

```powershell
Invoke-WebRequest http://your-site.com/wp-cron.php?doing_wp_cron
```

> **Note:** Use `?doing_wp_cron` to prevent race conditions if multiple requests fire simultaneously.
