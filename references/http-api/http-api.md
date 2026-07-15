# HTTP API

WordPress provides wrapper functions for making HTTP requests. They abstract away `cURL`, `fsockopen`, and other transport methods.

## Making Requests

### wp_remote_get()

```php
wp_remote_get( string $url, array $args = array() ): array|WP_Error
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$url` | string | Yes | Resource URL to retrieve |
| `$args` | array | No | Request arguments (see defaults below) |
| **Returns** | array\|WP_Error | — | Response array on success, `WP_Error` on failure |

**Default args:**

| Arg | Type | Default | Description |
|-----|------|---------|-------------|
| `method` | string | `'GET'` | HTTP method |
| `timeout` | int | 5 | Seconds to wait for response |
| `redirection` | int | 5 | Max redirects to follow |
| `httpversion` | string | `'1.0'` | HTTP version |
| `blocking` | bool | `true` | Wait for response before continuing |
| `headers` | array | `[]` | Custom headers |
| `body` | mixed | `null` | Request body data |
| `cookies` | array | `[]` | Cookies to send |

### wp_remote_post()

```php
wp_remote_post( string $url, array $args = array() ): array|WP_Error
```

Same parameters as `wp_remote_get()`. The `'body'` arg is typically an associative array:

```php
$response = wp_remote_post( 'https://api.example.com/endpoint', [
    'body' => [
        'name'  => 'Jane Smith',
        'email' => 'jane@example.com',
    ],
] );
```

### wp_remote_head()

Check resource metadata without downloading content. Useful for rate-limit checks and cache validation:

```php
$response = wp_remote_head( 'https://api.example.com/resource' );
```

> **Note:** `body` is always empty in HEAD responses. Use for checking `last-modified`, `cache-control`, `content-length` headers.

### wp_remote_request()

For custom HTTP methods (PUT, DELETE, PATCH, etc.):

```php
wp_remote_request( string $url, array $args = array() ): array|WP_Error
```

```php
$response = wp_remote_request( 'https://api.example.com/resource/42', [
    'method' => 'DELETE',
] );

// PUT with body
$response = wp_remote_request( 'https://api.example.com/resource/42', [
    'method' => 'PUT',
    'body'   => json_encode( [ 'title' => 'Updated' ] ),
    'headers' => [ 'Content-Type' => 'application/json' ],
] );
```

## Response Helpers

All functions return an array with keys: `body`, `response`, `cookies`, `headers`, `filename`. Use helper functions to extract data:

| Function | Purpose | Example |
|----------|---------|---------|
| `wp_remote_retrieve_body()` | Get response body | `$body = wp_remote_retrieve_body( $response )` |
| `wp_remote_retrieve_response_code()` | Get HTTP status code | `$code = wp_remote_retrieve_response_code( $response )` |
| `wp_remote_retrieve_response_message()` | Get response message | `$msg = wp_remote_retrieve_response_message( $response )` |
| `wp_remote_retrieve_header()` | Get specific header | `$date = wp_remote_retrieve_header( $response, 'last-modified' )` |
| `wp_remote_retrieve_headers()` | Get all headers | `$headers = wp_remote_retrieve_headers( $response )` |

### Complete Example

```php
$response = wp_remote_get( 'https://api.github.com/users/octocat' );

if ( is_wp_error( $response ) ) {
    // Handle error
    return;
}

$body     = wp_remote_retrieve_body( $response );
$http_code = wp_remote_retrieve_response_code( $response );
$headers  = wp_remote_retrieve_headers( $response );

$data = json_decode( $body, true );
```

### Inline Usage (Body Only)

When only the body is needed:

```php
$body = wp_remote_retrieve_body( wp_remote_get( 'https://api.github.com/users/octocat' ) );
$data = json_decode( $body, true );
```

## Authentication

### Basic Auth

```php
$response = wp_remote_get( 'https://api.example.com/protected', [
    'headers' => [
        'Authorization' => 'Basic ' . base64_encode( 'username:password' ),
    ],
] );
```

### Custom Headers / API Keys

```php
$response = wp_remote_get( 'https://api.example.com/data', [
    'headers' => [
        'X-API-Key'    => 'your-api-key-here',
        'Accept'       => 'application/json',
        'Content-Type' => 'application/json',
    ],
] );
```

## Response Codes Reference

| Code | Meaning |
|------|---------|
| 200 | OK — Success |
| 301 | Moved Permanently |
| 302 | Found (Temporary Redirect) |
| 403 | Forbidden — Auth failure or insufficient permissions |
| 404 | Not Found |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

## Caching with Transients

Cache API responses to reduce external requests and improve performance.

### Set a Transient

```php
set_transient( string $transient, mixed $value, int $expiration ): bool
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$transient` | string | Yes | Unique name for the cached data |
| `$value` | mixed | Yes | Data to cache (must be serializable) |
| `$expiration` | int | No | Seconds until expiration. Use constants like `HOUR_IN_SECONDS` (3600), `DAY_IN_SECONDS` (86400) |

### Get a Transient

```php
get_transient( string $transient ): mixed|false
```

Returns cached value, or `false` if not found/expired.

### Delete a Transient

```php
delete_transient( string $transient ): bool
```

### Complete Cache Pattern

```php
function myplugin_get_github_user( string $username ): ?array {
    // Try cache first
    $cached = get_transient( 'myplugin_github_' . md5( $username ) );
    if ( false !== $cached ) {
        return $cached;
    }

    // Fetch from API
    $response = wp_remote_get( "https://api.github.com/users/{$username}" );
    if ( is_wp_error( $response ) ) {
        return null;
    }

    $data = json_decode( wp_remote_retrieve_body( $response ), true );

    // Cache for 1 hour
    set_transient( 'myplugin_github_' . md5( $username ), $data, HOUR_IN_SECONDS );

    return $data;
}
```

> **Note:** Use `md5()` or similar on dynamic data in the transient name to ensure uniqueness. Prefer site-wide transients (`set_site_transient()`) for multisite compatibility.
