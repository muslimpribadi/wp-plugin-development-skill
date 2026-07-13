# Responses

## WP_REST_Response

Represents an HTTP response. Created via `rest_ensure_response()` which wraps data and auto-encodes to JSON.

### Creating a Response

```php
// Preferred — automatically handles array/object wrapping
$response = rest_ensure_response( $data );

// Manual construction
$response = new WP_REST_Response( $data, $status_code = 200, $headers = array() );
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `$data` | mixed | — | Response body (array, object, or scalar) |
| `$status_code` | int | 200 | HTTP status code |
| `$headers` | array | `array()` | Response headers |

### Accessing Response Data

```php
$response->get_data();              // Response body
$response->get_status();            // HTTP status code (e.g., 200, 404)
$response->get_headers();           // All headers as array
$response->get_matched_route();     // The matched route string
$response->get_matched_handler();   // Registered endpoint options
```

### Setting Data and Headers

```php
$response->set_data( $new_data );
$response->set_status( 201 );
$response->header( 'X-Custom-Header', 'value' );
$response->headers()->set( 'Content-Type', 'application/json' );
```

## Error Handling

Return a `WP_Error` from your callback — the REST server automatically converts it to an HTTP error response:

```php
return new WP_Error(
    'rest_error_code',        // Error code (machine-readable)
    'Human readable message', // Error message (user-facing)
    array( 'status' => 400 )  // HTTP status code
);
```

### Common Error Codes

| Code | Meaning | HTTP Status |
|------|---------|-------------|
| `rest_forbidden` | Authentication/authorization failure | 401 or 403 |
| `rest_not_found` | Resource not found | 404 |
| `rest_invalid_param` | Invalid request parameter | 400 |
| `rest_unknown_route` | Route does not exist | 404 |

## Response Linking (HAL)

Add links to responses for resource relationships:

```php
$response->add_links( array(
    'replies' => array(
        'href'       => rest_url( 'my-namespace/v1/comments?post=' . $post_id ),
        'embeddable' => true,
    ),
) );
```

| Link Property | Type | Description |
|---------------|------|-------------|
| `href` | string | URL to the linked resource |
| `embeddable` | bool | If `true`, link data is included with `?_embed` query param |

### Embedding Linked Resources

Clients can request embedded data by adding `?_embed` to their request:

```
GET /wp-json/my-namespace/v1/comments/3?_embed
```

The response will include the linked post data inline, reducing HTTP round-trips.

## Response for Collection

When returning multiple items, prepare each for collection:

```php
function myplugin_prepare_for_collection( $response ) {
    if ( ! ( $response instanceof WP_REST_Response ) ) {
        return $response;
    }

    $data = (array) $response->get_data();
    $server = rest_get_server();

    if ( method_exists( $server, 'get_compact_response_links' ) ) {
        $links = call_user_func( array( $server, 'get_compact_response_links' ), $response );
    } else {
        $links = call_user_func( array( $server, 'get_response_links' ), $response );
    }

    if ( ! empty( $links ) ) {
        $data['_links'] = $links;
    }

    return $data;
}
```

> **Note:** WordPress core now includes `WP_REST_Controller::prepare_response_for_collection()`. Use the parent method instead of this manual implementation.
