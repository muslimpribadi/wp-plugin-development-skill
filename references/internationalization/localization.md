# Localization Files and Workflow

## File Types

| Extension | Name | Description |
|-----------|------|-------------|
| `.pot` | Portable Object Template | Original strings (usually English). Sent to translators. |
| `.po` | Portable Object | Translated file with `msgid` (original) and `msgstr` (translation). One per language. |
| `.mo` | Machine Object | Binary compiled from `.po`. This is what WordPress actually loads. |

### File Naming Convention

```
{text-domain}-{locale}.mo
```

| Locale | Language | Example Filename |
|--------|----------|-----------------|
| `de_DE` | German (Germany) | `my-plugin-de_DE.mo` |
| `fr_FR` | French (France) | `my-plugin-fr_FR.mo` |
| `es_ES` | Spanish (Spain) | `my-plugin-es_ES.mo` |
| `zh_CN` | Chinese (China) | `my-plugin-zh_CN.mo` |

> **Note:** Language codes come from [WordPress locale list](https://developer.wordpress.org/apis/wordpress.org/other-translations/). Use country-specific codes (`de_DE`) when available for proper formatting.

## Generating POT Files

### WP-CLI (Recommended)

```bash
# Generate POT from source files
wp i18n make-pot . languages/my-plugin.pot --domain=my-plugin

# Update existing POT with new strings
wp i18n make-pot . languages/my-plugin.pot --merge
```

### Poedit

1. Open Poedit → File → New catalog from PO/File
2. Set project info (name, version, language)
3. Add source files or directories to scan
4. Save as `.pot` in `languages/` folder

## Translating a PO File

### Manual Edit (PO file format)

```po
#: plugin.php:42
msgid "Hello World"
msgstr ""
```

Fill in `msgstr`:

```po
#: plugin.php:42
msgid "Hello World"
msgstr "Hola Mundo"
```

### Poedit

1. Open the `.pot` file (or create from it)
2. Translate each `msgid` into `msgstr`
3. Save as `{domain}-{locale}.po`
4. Build → Compile to MO (generates `.mo` file)

## Compiling .mo Files

### Command Line

```bash
# Single file
msgfmt -o my-plugin-de_DE.mo my-plugin-de_DE.po

# Batch — all PO files in a directory
for file in *.po; do msgfmt -o "${file%.po}.mo" "$file"; done
```

> **Note:** Always compile your own `.mo` files from received `.po` files. Never trust pre-compiled `.mo` files from third parties.

### Poedit

Build → Compile to MO (or Ctrl+Shift+B)

## Translation File Locations

| Location | WordPress Version | Use Case |
|----------|-------------------|----------|
| `wp-content/languages/plugins/{domain}-{locale}.mo` | 3.7+ | Shared translations across plugins |
| `{plugin}/languages/{domain}-{locale}.mo` | All | Plugin-specific translations |

## Tips for Good Translations

| Practice | Reason |
|----------|--------|
| Translate organically, not literally | Languages have different structures and rhythms |
| Maintain consistent formality | Match the tone of the target audience |
| Avoid slang and region-specific terms | Keep content universally understandable |
| Read other software translations | Maintain consistency with common UI terminology |

## Resources

- [WordPress Codex: I18n for WordPress Developers](https://developer.wordpress.org/plugins/internationalization/)
- [translate.wordpress.org](https://translate.wordpress.org) — Official translation platform
- [GlotPress](https://glotpress.wordpress.org) — Open-source translation management tool
- [Poedit](https://poedit.net) — Free .po/.mo editor for Windows, macOS, Linux
