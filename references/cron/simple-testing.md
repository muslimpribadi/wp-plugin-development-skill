# Testing WP-Cron Events

## WP-CLI

```bash
# List all scheduled events
wp cron event list

# Run a specific event immediately
wp cron event run myplugin_cron_hook

# Delete a scheduled event
wp cron event delete myplugin_cron_hook

# Delete all scheduled events
wp cron event delete --all
```

## Programmatic Inspection

```php
// View all scheduled cron events (raw data)
$crons = _get_cron_array();
print_r( $crons );

// View available schedules
$schedules = wp_get_schedules();
print_r( $schedules );
```

## Third-Party Plugins

Several plugins provide UI for managing cron events:
- **WP Crontrol** — View, edit, and run scheduled events from admin UI
- **Event Monitor** — Log cron event executions with timestamps and results
