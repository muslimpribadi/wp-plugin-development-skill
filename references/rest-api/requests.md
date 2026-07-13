# Requests

## WP_REST_Request

The `WP_REST_Request` class represents an incoming HTTP request or can be used to make internal requests.

### Constructor

```php
new WP_REST_Request( string $method = 'GET', string $route = '' )
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `$method` | string | HTTP method (`GET`, `POST`, `PUT`, `DELETE`, etc.) |
| `$route` | string | Route path (for internal requests only) |

### Accessing Parameters

The class implements `ArrayAccess` — access parameters by name:

```php
$id = $request['id'];         // Path variable
$page = $request['page'];     // Query parameter
$data = $request['data'];     // Body parameter
```

### Parameter Types

| Type | Source | Access Method | Example |
|------|--------|---------------|---------|
| **Path** | URL route variables (`/books/(?P<id>\d+)`) | `$request['id']` | From route matching |
| **Query** | Query string (`?page=2&sort=date`) | `$request['page']` | Same as `$_GET` |
| **Body** | Request body (POST/PUT) | `$request['data']` | Same as `$_POST` |
| **Files** | Multipart uploads | `$request->get_file_params()` | Same as `$_FILES` |

### Getting Parameters Explicitly

```php
$request->get_param( 'id' );           // Any parameter type (path + query + body)
$request->get_query_params();          // Only query string params (like $_GET)
$request->get_body_params();           // Only body params (like $_POST)
$request->get_url_params();            // Only path variables
$request->get_file_params();           // File uploads (like $_FILES)
$request->get_header( 'content-type' ); // Specific header value
$request->get_headers();               // All headers as array
```

> **Never access `$_GET`, `$_POST`, or `$_FILES` directly in REST endpoints.** Always use the `WP_REST_Request` methods.

### Request Attributes

Returns the registration options for the matched route:

```php
$attributes = $request->get_attributes();
// Returns: ['methods' => [...], 'args' => [...], 'callback' => [...], ...]
```

## Internal Requests

Use `rest_do_request()` to call endpoints internally without HTTP overhead:

```php
$request  = new WP_REST_Request( 'GET', '/my-namespace/v1/items/42' );
$response = rest_do_request( $request );  // Returns WP_REST_Response object

$data = $response->get_data();
```

### Batch Endpoint Pattern

```php
function myplugin_batch_handler( $request ) {
    $results = array();

    foreach ( $request['requests'] as $req_params ) {
        $inner_request = new WP_REST_Request(
            $req_params['method'],
            $req_params['route']
        );

        if ( isset( $req_params['params'] ) ) {
            foreach ( $req_params['params'] as $key => $value ) {
                $inner_request->set_param( $key, $value );
            }
        }

        $inner_response = rest_do_request( $inner_request );
        $results[] = $inner_response->get_data();
    }

    return rest_ensure_response( $results );
}
```

> **Note:** `rest_do_request()` returns a `WP_REST_Response` PHP object, NOT JSON-encoded data. Use `$response->get_data()` to access the response body.
