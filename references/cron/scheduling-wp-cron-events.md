# Scheduling WP-Cron Events

## Adding the Hook

Create a custom hook and assign a callback function:

```php
add_action( 'myplugin_cron_hook', 'myplugin_cron_exec' );

function myplugin_cron_exec() {
    // Task logic here
}
```

> **Note:** Prefix all function names with your plugin namespace to avoid conflicts.

## Scheduling a Recurring Event

```php
wp_schedule_event( int $timestamp, string $recurrence, string $hook, array $args = array() )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$timestamp` | int | Yes | UNIX timestamp of first execution |
| `$recurrence` | string | Yes | Interval name (`'hourly'`, `'daily'`, or custom) |
| `$hook` | string | Yes | Name of the action hook to trigger |
| `$args` | array | No | Arguments passed to the callback function |

### Example

```php
add_action( 'myplugin_init', 'myplugin_schedule_task' );

function myplugin_schedule_task() {
    if ( ! wp_next_scheduled( 'myplugin_cron_hook' ) ) {
        wp_schedule_event( time(), 'hourly', 'myplugin_cron_hook' );
    }
}
```

### Scheduling with Arguments

```php
if ( ! wp_next_scheduled( 'myplugin_send_emails' ) ) {
    wp_schedule_event( time(), 'daily', 'myplugin_send_emails', array( 'user_id' => 42 ) );
}

add_action( 'myplugin_send_emails', 'myplugin_send_to_user', 10, 1 );

function myplugin_send_to_user( $args ) {
    $user_id = $args['user_id'];
    // Send email to user
}
```

## Unscheduling a Task

```php
wp_unschedule_event( int $timestamp, string $hook )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$timestamp` | int | Yes | Timestamp of the event to unschedule |
| `$hook` | string | Yes | Hook name associated with the event |

### Example

```php
$timestamp = wp_next_scheduled( 'myplugin_cron_hook' );
wp_unschedule_event( $timestamp, 'myplugin_cron_hook' );
```

## Checking if a Task is Scheduled

```php
wp_next_scheduled( string $hook )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$hook` | string | Yes | Hook name to check |
| **Returns** | int\|false | — | UNIX timestamp of next run, or `false` if not scheduled |

### Example

```php
if ( wp_next_scheduled( 'myplugin_cron_hook' ) ) {
    // Task is already scheduled
}
```

## Cleanup on Deactivation

Always unschedule tasks when your plugin deactivates:

```php
register_deactivation_hook( __FILE__, 'myplugin_deactivate' );

function myplugin_deactivate() {
    $timestamp = wp_next_scheduled( 'myplugin_cron_hook' );
    if ( $timestamp ) {
        wp_unschedule_event( $timestamp, 'myplugin_cron_hook' );
    }
}
```

> **Note:** Without cleanup, orphaned cron events continue to run even after plugin deactivation.

## Listing Scheduled Events

```php
// List all scheduled cron events (raw array)
$crons = _get_cron_array();

// List available schedules
$schedules = wp_get_schedules();
```
