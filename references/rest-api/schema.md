# Schema

## Resource Schema

Define the structure of your API responses using JSON Schema. Register via the `'schema'` key in `register_rest_route()`:

```php
register_rest_route( 'my-plugin/v1', '/items/(?P<id>\d+)', [
    'methods'  => WP_REST_Server::READABLE,
    'callback' => 'myplugin_get_item',
    'schema'   => 'myplugin_get_item_schema',
] );

function myplugin_get_item_schema(): array {
    return [
        '$schema'    => 'http://json-schema.org/draft-04/schema#',
        'title'      => 'item',
        'type'       => 'object',
        'properties' => [
            'id' => [
                'description' => 'Unique identifier.',
                'type'        => 'integer',
                'context'     => [ 'view', 'edit', 'embed' ],
                'readonly'    => true,
            ],
            'title' => [
                'description' => 'The item title.',
                'type'        => 'string',
                'context'     => [ 'view', 'edit' ],
            ],
            'content' => [
                'description' => 'Full content.',
                'type'        => 'string',
                'format'      => 'html',
                'context'     => [ 'edit' ],
                'readonly'    => true,
            ],
        ],
    ];
}
```

### Schema Properties Reference

| Property | Type | Purpose |
|----------|------|---------|
| `$schema` | string | JSON Schema spec version (`draft-04`) |
| `title` | string | Resource identity name |
| `type` | string | Data type (`object`, `array`, `string`, `integer`, `number`, `boolean`) |
| `properties` | object | Field definitions keyed by field name |
| `required` | array | List of required property names |

### Property Schema Properties

| Property | Type | Purpose |
|----------|------|---------|
| `description` | string | Human-readable description |
| `type` | string | Data type |
| `format` | string | Format hint (`html`, `uri`, `date-time`, `email`) |
| `context` | array | When field is included: `view` (public), `edit` (logged-in), `embed` (with `_embed`) |
| `readonly` | bool | Field only appears in responses, never accepted in requests |
| `enum` | array | Allowed values |

### Context-Based Field Visibility

```php
// Only shown when context='view' (public API)
'id' => [ 'context' => [ 'view', 'embed' ] ],

// Hidden from public, only for logged-in users
'internal_status' => [ 'context' => [ 'edit' ] ],

// Always included
'name' => [ 'context' => [ 'view', 'edit', 'embed' ] ],
```

## Argument Schema

Define validation schemas for endpoint parameters (see `routes-endpoints.md` for full example):

```php
'args' => [
    'category' => [
        'description'       => 'Filter by category slug',
        'type'              => 'string',
        'enum'              => [ 'news', 'reviews', 'tutorials' ],
        'validate_callback' => 'rest_validate_request_arg',
        'sanitize_callback' => 'sanitize_key',
    ],
],
```

### Built-in Validation & Sanitization Functions

| Function | Validates/Sanitizes | Example |
|----------|-------------------|---------|
| `rest_validate_request_arg` | Type + enum matching | Default for most args |
| `sanitize_key` | Alphanumeric + hyphens/underscores | Category slugs, IDs |
| `absint` | Non-negative integer | Page numbers, counts |
| `sanitize_text_field` | Plain text | Freeform text input |
| `rest_sanitize_allowed_html` | Allowed HTML tags | Rich text fields |

> **Note:** Always specify both `validate_callback` and `sanitize_callback` when accepting user input. Validation rejects bad data; sanitization cleans good data.
