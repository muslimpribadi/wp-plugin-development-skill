# TinyMCE Enhanced Shortcodes

WordPress includes built-in shortcodes that render inline content in the Visual (TinyMCE) editor. Switching to the Text tab reveals the raw shortcode.

## Built-in Media Shortcodes

| Shortcode | Purpose |
|-----------|---------|
| `[audio]` | Embed a single audio file |
| `[video]` | Embed a single video file |
| `[gallery]` | Display multiple images in a gallery layout |
| `[playlist]` | HTML5 audio/video playlist with multiple media files |
| `[caption]` | Wrap an image in a div with `<p class="wp-caption-text">` caption |

> **Note:** These are handled by WordPress core. Custom shortcodes do not render in TinyMCE by default — use the [TinyMCE API](https://developer.wordpress.org/themes/advanced-tinymce/) to add custom visual support.
