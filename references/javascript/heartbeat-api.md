# Heartbeat API

The Heartbeat API provides periodic, low-overhead server communication for near-real-time updates (used by WordPress dashboard auto-save, post locking, etc.).

## How It Works

| Step | Direction | Event/Filter | Description |
|------|-----------|-------------|-------------|
| 1 | Client → Server | `heartbeat-send` (JS) | Add custom data to heartbeat payload |
| 2 | Server → Filter | `heartbeat_received` (PHP) | Detect sent data, add response data |
| 3 | Server → Client | (automatic JSON) | Response passed back to JS |
| 4 | Client ← Server | `heartbeat-tick` (JS) | Process server response |

## Sending Data to the Server

```javascript
jQuery(document).on('heartbeat-send', function(event, data) {
    data.myplugin_customfield = 'some_data';
});
```

## Receiving and Responding on the Server

```php
add_filter( 'heartbeat_received', 'myplugin_handle_heartbeat', 10, 2 );

function myplugin_handle_heartbeat( array $response, array $data ) {
    if ( empty( $data['myplugin_customfield'] ) ) {
        return $response;
    }

    $response['myplugin_customfield_hashed'] = sha1( $data['myplugin_customfield'] );
    return $response;
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `$response` | array | Current heartbeat response (add your data here) |
| `$data` | array | Data sent from client (unslashed) |

## Processing the Response on Client

```javascript
jQuery(document).on('heartbeat-tick', function(event, data) {
    if ( data.myplugin_customfield_hashed ) {
        alert('Hash: ' + data.myplugin_customfield_hashed);
    }
});
```

## Heartbeat Events Reference

| Event | Direction | Handler | Purpose |
|-------|-----------|---------|---------|
| `heartbeat-send` | Client → Server | `jQuery(document).on('heartbeat-send', ...)` | Add custom data to payload |
| `heartbeat-received` (PHP) | Server filter | `add_filter('heartbeat_received', ...)` | Detect sent data, prepare response |
| `heartbeat-tick` | Server → Client | `jQuery(document).on('heartbeat-tick', ...)` | Process server response |

## Controlling Heartbeat Interval

Heartbeat fires every 15–120 seconds. Reduce frequency for low-activity pages:

```javascript
jQuery(document).ready(function($) {
    // Set interval to 60 seconds (default is ~15-120)
    wp.heartbeat.interval('60s');
});
```

> **Note:** Heartbeat runs on all admin pages by default. Disable it entirely if not needed:
> ```php
> add_action('admin_enqueue_scripts', 'myplugin_disable_heartbeat');
> function myplugin_disable_heartbeat() {
>     wp_deregister_script('heartbeat');
> }
> ```
