# Securing Input: Complete Workflow

## The Golden Rule

**Always sanitize on input, always escape on output.** Sanitization cleans data before storage; escaping formats data for safe display. They serve different purposes and both are required.

## Step-by-Step Input Security Workflow

### Step 1: Identify All Input Sources

```php
// Every one of these must be sanitized before use:
$_GET['param']      // Query string parameters
$_POST['param']     // Form submissions
$_COOKIE['name']    // Cookie values
$_FILES['upload']   // File uploads
$_SERVER['VAR']     // Server variables (use with extreme caution)
REST API request body
```

### Step 2: Sanitize Immediately on Receipt

```php
// WRONG: Using raw input anywhere
$name = $_POST['name'];
update_option('site_name', $name);

// CORRECT: Sanitize at the point of receipt
$name = sanitize_text_field($_POST['name']);
update_option('site_name', $name);
```

### Step 3: Validate Against Expected Format

```php
// Numeric validation
$count = absint($_GET['count']); // Forces integer, returns 0 if not numeric
if ($count < 1 || $count > 100) {
    wp_die('Invalid count.');
}

// Enumerated value validation
$status = sanitize_text_field($_POST['status']);
$allowed = array('draft', 'publish', 'pending');
if (!in_array($status, $allowed, true)) {
    $status = 'draft'; // Default to safe value
}

// Email validation
$email = sanitize_email($_POST['email']);
if (!is_email($email)) {
    wp_die('Invalid email address.');
}

// URL validation
$url = esc_url_raw($_POST['url']);
if (empty($url) || !filter_var($url, FILTER_VALIDATE_URL)) {
    wp_die('Invalid URL.');
}
```

### Step 4: Handle File Uploads Securely

```php
if (isset($_FILES['upload'])) {
    // Check for upload errors
    if ($_FILES['upload']['error'] !== UPLOAD_ERR_OK) {
        wp_die('Upload failed.');
    }
    
    // Validate MIME type (NOT just extension)
    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    $mime = finfo_file($finfo, $_FILES['upload']['tmp_name']);
    finfo_close($finfo);
    
    $allowed_types = array('image/jpeg', 'image/png', 'application/pdf');
    if (!in_array($mime, $allowed_types, true)) {
        wp_die('Invalid file type.');
    }
    
    // Sanitize filename
    $filename = sanitize_file_name($_FILES['upload']['name']);
    
    // Move to secure location (not web-accessible temp dir)
    $upload_dir = wp_upload_dir();
    $destination = $upload_dir['path'] . '/' . $filename;
    move_uploaded_file($_FILES['upload']['tmp_name'], $destination);
}
```

## Input Validation by Context

| Context | Required Checks | Example Function |
|---------|----------------|------------------|
| Admin settings form | Nonce + capability + sanitize | `check_admin_referer()` + `current_user_can()` + `sanitize_text_field()` |
| Front-end search | Sanitize + validate range | `sanitize_text_field()` + `absint()` for pagination |
| AJAX handler | Nonce + capability + sanitize | `wp_verify_nonce()` + `current_user_can()` + per-field sanitization |
| REST API callback | Capability check + sanitize | `permission_callback` + `sanitize_*()` in schema validation |
| Webhook receiver | Signature verify + sanitize | Custom signature check + strict type validation |

## Never Trust These Values

- Any value from `$_GET`, `$_POST`, `$_COOKIE`, `$_FILES`
- Values from external APIs (even your own) without validation
- Database values used in SQL queries without `$wpdb->prepare()`
- Transient/cached data that could be manipulated
