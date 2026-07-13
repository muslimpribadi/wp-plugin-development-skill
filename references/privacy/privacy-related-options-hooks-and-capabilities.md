# Privacy Options, Hooks and Capabilities

## Options

| Option | Type | Description |
|--------|------|-------------|
| `wp_page_for_privacy_policy` | int | Page ID of the site's privacy policy page |

## Actions

| Hook | Purpose |
|------|---------|
| `user_request_action_confirmed` | Fires when a user confirms a privacy request |
| `wp_privacy_delete_old_export_files` | Scheduled action to prune old exports from personal data folder |
| `wp_privacy_personal_data_erased` | Fires after the last page of the last eraser is complete |
| `wp_privacy_personal_data_export_file` | Used during export flow to create a personal data export file |
| `wp_privacy_personal_data_export_file_created` | Fires after a personal data export file has been created |

## Filters — Export/Eraser Registration

| Hook | Purpose |
|------|---------|
| `wp_privacy_personal_data_erasers` | Register plugin eraser callbacks (key => array with `eraser_friendly_name` + `callback`) |
| `wp_privacy_personal_data_exporters` | Register plugin exporter callbacks (key => array with `exporter_friendly_name` + `callback`) |
| `wp_privacy_anonymize_data` | Filter anonymous data for each type |

## Filters — Export Data Flow

| Hook | Purpose |
|------|---------|
| `wp_privacy_personal_data_export_page` | Filter a page of exporter data; build export report |
| `wp_privacy_personal_data_erasure_page` | Filter a page of eraser data; consume erasure response |
| `wp_privacy_additional_user_profile_data` | Extend user profile data for the privacy exporter |

## Filters — Email Notifications (Export)

| Hook | Purpose |
|------|---------|
| `wp_privacy_personal_data_email_content` | Modify email body sent with personal data export link |
| `wp_privacy_personal_data_email_headers` | Filter email headers for export completion notification |
| `wp_privacy_personal_data_email_subject` | Filter email subject for export completion notification |
| `wp_privacy_personal_data_email_to` | Filter recipient of export email (use with caution) |

## Filters — Email Notifications (Erasure)

| Hook | Purpose |
|------|---------|
| `user_erasure_complete_email_subject` | Filter subject of erasure completion email |
| `user_confirmed_action_email_content` | Filter body of erasure fulfillment notification |
| `user_erasure_complete_email_headers` | Filter headers of erasure notification |
| `user_erasure_fulfillment_email_to` | Filter recipient of erasure fulfillment notification |

## Filters — Request Confirmation Emails

| Hook | Purpose |
|------|---------|
| `user_request_confirmed_email_content` | Filter body of request confirmation email |
| `user_request_confirmed_email_headers` | Filter headers of request confirmation email |
| `user_request_confirmed_email_subject` | Filter subject of request confirmation email |
| `user_request_confirmed_email_to` | Filter recipient of request confirmation notification |

## Filters — General Privacy

| Hook | Purpose |
|------|---------|
| `privacy_policy_url` | Filter the privacy policy page URL |
| `the_privacy_policy_link` | Filter the privacy policy page link HTML |
| `wp_get_default_privacy_policy_content` | Filter default content for privacy policy guide |
| `user_request_action_confirmed_message` | Modify action confirmation message displayed to user |
| `user_request_action_description` | Filter user action description |
| `user_request_key_expiration` | Filter expiration time of confirmation keys (seconds) |
| `wp_privacy_export_expiration` | Control how long export files are kept (default: 3 days) |
| `wp_privacy_exports_dir` | Filter directory used to store personal data exports |
| `wp_privacy_exports_url` | Filter URL of personal data exports directory |

## Capabilities

| Capability | Controls |
|------------|----------|
| `erase_others_personal_data` | Availability of Erase Personal Data sub-menu under Tools |
| `export_others_personal_data` | Availability of Export Personal Data sub-menu under Tools |
| `manage_privacy_options` | Availability of Privacy sub-menu under Settings |

> **Note:** Administrators have all three capabilities by default on single-site installs.
