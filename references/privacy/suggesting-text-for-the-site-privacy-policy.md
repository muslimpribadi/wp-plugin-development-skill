# Suggesting Text for the Site Privacy Policy

Use `wp_add_privacy_policy_content()` to provide suggested text for the privacy policy postbox. Called during `admin_init`.

## Function Signature

```php
wp_add_privacy_policy_content( string $plugin_name, string $policy_text )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `$plugin_name` | string | Yes | Plugin name (shown in the policy postbox) |
| `$policy_text` | string | Yes | HTML content with suggested privacy text |

## Complete Example

```php
add_action( 'admin_init', 'myplugin_add_privacy_policy_content' );

function myplugin_add_privacy_policy_content() {
    if ( ! function_exists( 'wp_add_privacy_policy_content' ) ) {
        return;
    }

    $content = '<p class="privacy-policy-tutorial">'
        . __( 'Some introductory content for the suggested text.', 'text-domain' )
        . '</p>'
        . '<strong class="privacy-policy-tutorial">'
        . __( 'Suggested Text:', 'my_plugin_textdomain' )
        . '</strong> '
        . sprintf(
            __( 'When you leave a comment on this site, we send your name, email address, IP address and comment text to example.com. Example.com does not retain your personal data. The example.com privacy policy is <a href="%1$s" target="_blank">here</a>.', 'text-domain' ),
            'https://example.com/privacy-policy'
        );

    wp_add_privacy_policy_content( 'Example Plugin', wp_kses_post( wpautop( $content, false ) ) );
}
```

## Tutorial CSS Class

Use `.privacy-policy-tutorial` class for instructional text that is **omitted** when the section is copied to the clipboard:

```php
// This text appears in the postbox but NOT in the exported policy
'<p class="privacy-policy-tutorial">' . __( 'Introductory context here', 'text-domain' ) . '</p>';

// This text appears in both the postbox AND the exported policy
'<strong>' . __( 'Suggested Text:', 'text-domain' ) . '</strong> Actual privacy text...';
```

## Applicable Questions to Address

| Question | Description |
|----------|-------------|
| What personal data we collect and why | Fields collected, purpose of collection |
| Who we share your data with | Third-party services, partners |
| How long we retain your data | Retention periods |
| What rights you have over your data | Access, correction, deletion requests |
| Where we send your data | Server locations, cross-border transfers |
| What automated decision making we do | Profiling, automated processing |

> **Note:** Call `wp_add_privacy_policy_content()` during `admin_init`. Calling outside a hook can cause issues.
