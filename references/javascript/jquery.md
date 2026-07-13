# jQuery in WordPress

## NoConflict Mode

WordPress loads jQuery in `noConflict()` mode. Always use the full `jQuery` name or pass `$` as a parameter:

```javascript
// WRONG — $ is not available globally
$(document).ready(function() { ... });

// CORRECT — wrapper pattern
jQuery(document).ready(function($) {
    // $ is available inside this scope
    $(".my-class").hide();
});

// ALTERNATIVE — shorthand (not recommended for readability)
(function($) {
    $(".my-class").hide();
})(jQuery);
```

## Common Selectors

| Selector | Example | Purpose |
|----------|---------|---------|
| Class | `$(".classname")` | Elements with class |
| ID | `$("#idname")` | Single element with ID |
| Tag | `$("p")` | All paragraph elements |
| Attribute | `$("[data-field='value']")` | Elements with specific attribute |

## Common Events

| Event | Triggered By | Example |
|-------|-------------|---------|
| `click` | Mouse click | `$(".btn").click(function() { ... })` |
| `change` | Input value changes | `$("input").change(function() { ... })` |
| `submit` | Form submission | `$("#form").submit(function(e) { e.preventDefault(); ... })` |
| `keyup` | Key pressed and released | `$("input").keyup(function() { ... })` |
| `ready` | DOM fully loaded | `jQuery(document).ready(function($) { ... })` |

## AJAX with jQuery

### $.post() — Simple POST Request

```javascript
$.post( url, data, callback, dataType )
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | Endpoint URL (use `my_ajax_obj.ajax_url`) |
| `data` | object | Yes | Key-value pairs sent to server |
| `callback` | function | No | Function receiving response data |
| `dataType` | string | No | Expected response type (`'json'`, `'html'`, etc.) |

```javascript
$.post(my_ajax_obj.ajax_url, {
    _ajax_nonce: my_ajax_obj.nonce,
    action: "my_action",
    field: $("#input").val()
}, function(response) {
    $(".result").html(response);
});
```

### $.ajax() — Full Control

```javascript
$.ajax({
    url: my_ajax_obj.ajax_url,
    type: 'POST',
    data: {
        _ajax_nonce: my_ajax_obj.nonce,
        action: 'my_action',
        value: $('#input').val()
    },
    success: function(response) {
        // Handle success
    },
    error: function(xhr, status, error) {
        // Handle error
    }
});
```

## Variable Scope in Closures

When using jQuery callbacks, `this` refers to the callback element, not the original trigger. Store it first:

```javascript
$(".pref").change(function() {
    var self = this;  // Preserve reference to original element
    $.post(my_ajax_obj.ajax_url, {
        action: 'my_action',
        value: $(this).val()
    }, function(response) {
        // $() here refers to callback context
        // Use self for the original trigger element
        $(self).after(response);
    });
});
```
