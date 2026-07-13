# Controller Classes

## Overview

Controller classes organize REST endpoint logic (routes, callbacks, schema, permissions) into a single reusable class. This is the recommended pattern for plugins with multiple endpoints.

## Base Pattern

```php
class My_REST_Controller {
    protected $namespace = 'my-plugin/v1';

    public function register_routes() {
        register_rest_route( $this->namespace, '/items', array(
            array(
                'methods'             => WP_REST_Server::READABLE,
                'callback'            => array( $this, 'get_items' ),
                'permission_callback' => array( $this, 'get_items_permissions_check' ),
                'args'                => $this->get_collection_params(),
            ),
            'schema' => array( $this, 'get_item_schema' ),
        ) );

        register_rest_route( $this->namespace, '/items/(?P<id>\d+)', array(
            array(
                'methods'             => WP_REST_Server::READABLE,
                'callback'            => array( $this, 'get_item' ),
                'permission_callback' => array( $this, 'get_item_permissions_check' ),
            ),
            'schema' => array( $this, 'get_item_schema' ),
        ) );
    }

    public function get_items( $request ) {
        // Return collection of items
    }

    public function get_item( $request ) {
        $id = (int) $request['id'];
        // Return single item
    }

    public function get_items_permissions_check( $request ) {
        return current_user_can( 'read' );
    }

    public function get_item_permissions_check( $request ) {
        return current_user_can( 'read' );
    }

    public function prepare_item_for_response( $item, $request ) {
        $data = array(
            'id'    => (int) $item->ID,
            'title' => $item->post_title,
        );
        return rest_ensure_response( $data );
    }

    public function get_item_schema() {
        return array(
            '$schema'    => 'http://json-schema.org/draft-04/schema#',
            'title'      => 'item',
            'type'       => 'object',
            'properties' => array(
                'id'    => array( 'description' => 'ID', 'type' => 'integer', 'context' => array( 'view', 'edit' ), 'readonly' => true ),
                'title' => array( 'description' => 'Title', 'type' => 'string', 'context' => array( 'view', 'edit' ) ),
            ),
        );
    }

    protected function get_collection_params() {
        return array(
            'page'     => array( 'description' => 'Page number', 'type' => 'integer', 'default' => 1 ),
            'per_page' => array( 'description' => 'Items per page', 'type' => 'integer', 'default' => 10, 'maximum' => 100 ),
        );
    }
}

// Register the controller
add_action( 'rest_api_init', function() {
    ( new My_REST_Controller() )->register_routes();
} );
```

## Key Methods

| Method | Purpose |
|--------|---------|
| `register_routes()` | Called on `rest_api_init` — defines all routes |
| `get_items()` / `get_item()` | Main callbacks for collection and single resource |
| `get_items_permissions_check()` / `get_item_permissions_check()` | Permission callbacks |
| `prepare_item_for_response($item, $request)` | Transform raw data into response format |
| `get_item_schema()` | JSON Schema definition |
| `get_collection_params()` | Query parameters for collection endpoints (`page`, `per_page`, `search`, etc.) |

## Inheritance Best Practices

Do NOT extend controller classes directly (e.g., `class My_CPT_Controller extends My_REST_Posts_Controller`). Instead:

1. **Create separate controllers** for each resource type
2. **Use an abstract base class** or shared trait for common logic (schema structure, permission checks)
3. **Copy the core `WP_REST_Controller` pattern** — WordPress is moving toward this as a core class

> **Note:** The WordPress core team is developing `WP_REST_Controller` as a base class for inclusion in core. Monitor the REST API feature plugin for updates.
