# REST API Overview

## Architecture

The WordPress REST API uses JSON over HTTP to expose WordPress data. Three core classes handle the request/response lifecycle:

| Class | Purpose |
|-------|---------|
| `WP_REST_Request` | Incoming/outgoing request data (routes, params, headers) |
| `WP_REST_Response` | Response data, status codes, headers, links |
| `register_rest_route()` | Function to register route definitions |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Namespace** | Grouping prefix for routes (e.g., `my-plugin/v1`). Must be unique. Never use `/wp/` unless contributing to core. |
| **Route** | URI path that maps to endpoints (e.g., `/my-namespace/v1/books`) |
| **Endpoint** | HTTP method + route combination with callbacks (GET, POST, PUT, DELETE) |
| **Schema** | JSON Schema definition for resource structure and argument validation |
| **Controller Class** | OOP pattern organizing routes, callbacks, schema, and permissions in one class |

## Base URL

All REST requests go through: `https://example.com/wp-json/`

The index at `/wp-json/` returns available namespaces, routes, and methods.

## HTTP Method Convention

| Method | Use Case | Idempotent? |
|--------|----------|-------------|
| GET | Retrieve data | Yes |
| POST | Create resource | No |
| PUT | Update resource | Yes |
| DELETE | Delete resource | Yes |
| OPTIONS | Get route metadata/schema | Yes |

> **Note:** For clients that can't send non-GET methods, use `?_method=DELETE` or `X-HTTP-Method-Override: DELETE` header with a POST request.
