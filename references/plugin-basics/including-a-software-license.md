# Including a Software License

WordPress plugins are typically released under GPL. Include the license in your plugin header and optionally add a license block comment.

## Header Field

```php
/*
 * Plugin Name:       My Plugin
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 */
```

## License Block Comment

Place this near the top of your main plugin file:

```php
/*
{Plugin Name} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
any later version.

{Plugin Name} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with {Plugin Name}. If not, see https://www.gnu.org/licenses/gpl-2.0.html.
*/
```

## Common Licenses

| License | Slug | Description |
|---------|------|-------------|
| GPL v2 or later | `GPL v2 or later` | WordPress default, allows derivative works |
| GPL v3 or later | `GPL v3 or later` | Stronger copyleft requirements |
| MIT | `MIT` | Permissive, minimal restrictions |
| Apache 2.0 | `Apache-2.0` | Permissive with patent grant |

> **Note:** WordPress.org requires plugins to be GPL-compatible. The default choice (`GPL v2 or later`) is recommended for most plugins.
