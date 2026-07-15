# Routes & Endpoints

## register_rest_route()

```php
register_rest_route( string $namespace, string $route, array $args = [], bool $override = false )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$namespace` | string | Yes | Route grouping prefix (e.g., `'my-plugin/v1'`). Format: `{vendor}/{version}` |
| `$route` | string | Yes | Resource path with optional path variables (e.g., `/books/(?P<id>\d+)`) |
| `$args` | array | No | Endpoint configuration (methods, callbacks, args, schema). PHP 8.2+ uses `[]` for empty arrays.
| `$override` | bool | No | If `true`, override existing route. Default: `false` |

### Hook

Must be called on the `rest_api_init` action hook:

```php
add_action( 'rest_api_init', 'myplugin_register_routes' );
```

## Basic Endpoint

```php
register_rest_route( 'my-plugin/v1', '/hello', [
    'methods'             => WP_REST_Server::READABLE,  // GET
    'callback'            => 'myplugin_hello_handler',
    'permission_callback' => '__return_true',           // Public endpoint
] );

function myplugin_hello_handler(): array {
    return rest_ensure_response( [ 'message' => 'Hello World!' ] );
}
```

## Multiple Methods on One Route

```php
register_rest_route( 'my-shop/v1', '/products', [
    [
        'methods'             => WP_REST_Server::READABLE,     // GET
        'callback'            => 'myshop_get_products',
        'permission_callback' => '__return_true',
    ],
    [
        'methods'             => WP_REST_Server::CREATABLE,    // POST
        'callback'            => 'myshop_create_product',
        'permission_callback' => 'myshop_check_edit_permission',
    ],
] );
```

### Method Constants

| Constant | HTTP Method |
|----------|-------------|
| `WP_REST_Server::READABLE` | GET, HEAD, OPTIONS |
| `WP_REST_Server::CREATABLE` | POST |
| `WP_REST_Server::EDITABLE` | PUT, PATCH |
| `WP_REST_Server::DELETABLE` | DELETE |

## Path Variables

Embed regex patterns in the route using named groups:

```php
register_rest_route( 'my-shop/v1', '/products/(?P<id>\d+)', [
    'methods'  => WP_REST_Server::READABLE,
    'callback' => 'myshop_get_product',
] );

function myshop_get_product( WP_REST_Request $request ): array {
    $id = (int) $request['id'];  // Access path variable by name
    $product = get_post( $id );

    if ( ! $product ) {
        return new WP_Error( 'rest_not_found', 'Product not found.', [ 'status' => 404 ] );
    }

    return rest_ensure_response( $product );
}
```

## Arguments

Define accepted parameters with JSON Schema:

```php
register_rest_route( 'my-plugin/v1', '/items', [
    'methods'             => WP_REST_Server::READABLE,
    'callback'            => 'myplugin_get_items',
    'permission_callback' => '__return_true',
    'args'                => [
        'filter' => [
            'description'       => 'Filter items by category',
            'type'              => 'string',
            'enum'              => [ 'red', 'green', 'blue' ],
            'validate_callback' => 'rest_validate_request_arg',
            'sanitize_callback' => 'sanitize_key',
        ],
        'page' => [
            'description'       => 'Page number',
            'type'              => 'integer',
            'default'           => 1,
            'minimum'           => 1,
            'validate_callback' => 'rest_validate_request_arg',
        ],
    ],
] );
```

### Argument Schema Properties

| Property | Type | Purpose |
|----------|------|---------|
| `description` | string | Human-readable description |
| `type` | string | Data type (`string`, `integer`, `array`, `object`) |
| `format` | string | Format modifier (`date-time`, `uri`, `email`) |
| `enum` | array | Allowed values |
| `default` | mixed | Default value if not provided |
| `required` | bool | Whether the argument is mandatory |
| `minimum` / `maximum` | int | Numeric bounds |
| `validate_callback` | callable | Validation function (returns true/WP_Error) |
| `sanitize_callback` | callable | Sanitization function |

### Validation & Sanitization Order

1. **Validate** (`validate_callback`) — Runs first, returns `true`/`WP_Error`
2. **Sanitize** (`sanitize_callback`) — Transforms the value if valid
3. **Callback** — Receives the sanitized value via `$request['param']`

> **Note:** Use `rest_validate_request_arg()` for standard validation or `sanitize_key()`, `absint()`, etc. as built-in sanitizers.

## Permissions Callback

```php
register_rest_route( 'my-plugin/v1', '/private', [
    'methods'             => WP_REST_Server::READABLE,
    'callback'            => 'myplugin_private_data',
    'permission_callback' => 'myplugin_check_permission',
] );

function myplugin_check_permission(): bool {
    return current_user_can( 'edit_posts' );
}
```

Return `true` for access, `false` or `WP_Error` to deny. Always check capability — never assume logged-in means authorized.

## Complete Pattern — CRUD Product Endpoint

```php
add_action( 'rest_api_init', 'myshop_register_routes' );

function myshop_register_routes(): void {
    register_rest_route( 'my-shop/v1', '/products', [
        [
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => 'myshop_get_products',
            'permission_callback' => '__return_true',
            'args'                => [
                'page'      => [ 'type' => 'integer', 'default' => 1 ],
                'per_page'  => [ 'type' => 'integer', 'default' => 10, 'maximum' => 100 ],
            ],
        ],
        [
            'methods'             => WP_REST_Server::CREATABLE,
            'callback'            => 'myshop_create_product',
            'permission_callback' => function() { return current_user_can( 'edit_products' ); },
            'args'                => [
                'title'   => [ 'type' => 'string', 'required' => true ],
                'price'   => [ 'type' => 'number', 'required' => true ],
            ],
        ],
    ] );

    register_rest_route( 'my-shop/v1', '/products/(?P<id>\d+)', [
        [
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => 'myshop_get_product',
            'permission_callback' => '__return_true',
        ],
        [
            'methods'             => WP_REST_Server::EDITABLE,
            'callback'            => 'myshop_update_product',
            'permission_callback' => function() { return current_user_can( 'edit_products' ); },
            'args'                => [
                'title' => [ 'type' => 'string' ],
                'price' => [ 'type' => 'number' ],
            ],
        ],
        [
            'methods'             => WP_REST_Server::DELETABLE,
            'callback'            => 'myshop_delete_product',
            'permission_callback' => function() { return current_user_can( 'delete_products' ); },
        ],
    ] );
}
```
