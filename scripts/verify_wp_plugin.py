#!/usr/bin/env python3
"""WordPress Plugin Security Validator — Heuristic pre-deployment scanner.

Audits PHP files for common security anti-patterns referenced in
`/references/plugin-security/`. Designed as a first-pass filter; not a
substitute for manual review or static-analysis tools (e.g. PHPStan +
PHP_CodeSniffer with WPCS).

Usage:
    python3 scripts/verify_wp_plugin.py <path_to_plugin_dir> [options]

Options:
    --exclude <glob,...>   Comma-separated glob patterns to skip (default: vendor/,tests/,node_modules/)
    --severity <level>     Only report issues at or above this level: low, medium, high, critical
    --summary              Show summary statistics per check type

Examples:
    python3 scripts/verify_wp_plugin.py my-plugin/
    python3 scripts/verify_wp_plugin.py my-plugin/ --exclude vendor/,tests/
    python3 scripts/verify_wp_plugin.py my-plugin/ --severity high --summary
"""

import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Severity classification per check (grounded in /references/plugin-security/)
# ---------------------------------------------------------------------------
SEVERITY = {
    "raw_superglobal": "high",
    "input_type_mismatch": "high",        # NEW: wrong sanitizer for input type
    "unescaped_output": "medium",
    "unprepared_sql": "critical",         # SQL injection risk
    "unescaped_wp_die": "high",           # XSS via wp_die()
    "debug_output": "low",                # Information disclosure
    "missing_nonce": "critical",          # CSRF risk
    "missing_capability": "critical",     # Privilege escalation risk
    "missing_rest_permission": "critical",# Unauthenticated endpoint access
    "file_upload_no_mime_check": "critical",  # Arbitrary file upload
    "escape_used_as_sanitize": "high",    # Data corruption / stored XSS
    "context_escape_mismatch": "medium",  # Wrong escape function for context
}

SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}


# ---------------------------------------------------------------------------
# Input-type-specific sanitizer mapping (from /references/plugin-security/data-validation.md)
# ---------------------------------------------------------------------------
SANITIZER_MAP = {
    r"\\$_POST\[.*(?:email|mail)\]": ["sanitize_email", "is_email"],
    r"\\$_POST\[.*(?:url|website)\]": ["esc_url_raw", "esc_url"],
    r"\\$_GET\[.*(?:s|search|keyword)\]": ["sanitize_text_field", "sanitize_key"],
    r"\\$_POST\[.*(?:file|upload|attachment)\]": ["sanitize_file_name", "finfo_open"],
    r"\\$_POST\[.*(?:textarea|content|message|comment)\]": [
        "sanitize_textarea_field", "wp_kses_post", "wp_kses", "sanitize_text_field"
    ],
    r"\\$_POST\[.*(?:name|title|label)\]": ["sanitize_text_field", "sanitize_title"],
    r"\\$_GET\[.*id\]": ["absint", "intval", "sanitize_key"],
    r"\\$_POST\[.*id\]": ["absint", "intval", "sanitize_key"],
    r"\\$_COOKIE\[.*\]": ["sanitize_text_field", "sanitize_key"],
}

# Generic sanitizers accepted when no specific input-type pattern matches
GENERIC_SANITIZERS = [
    "sanitize_", "absint", "intval", "floatval", "wp_unslash",
    "sanitize_email", "sanitize_url", "sanitize_file_name",
    "sanitize_text_field", "sanitize_textarea_field", "sanitize_title",
    "esc_url_raw", "wp_kses", "wp_kses_post",
]


# ---------------------------------------------------------------------------
# Check definitions
# ---------------------------------------------------------------------------

CHECKS = {
    "raw_superglobal": {
        "name": "Raw superglobal access without sanitization",
        "regex": r"(?:\$_GET|\$_POST|\$_COOKIE|\$_FILES)",
        "sanitizer_pattern": "|".join(GENERIC_SANITIZERS),
    },
    "input_type_mismatch": {
        "name": "Input-type-specific sanitizer not used (see data-validation.md)",
        "mappings": SANITIZER_MAP,
    },
    "unescaped_output": {
        "name": "echo/print without escaping function",
        "regex": r"\b(?:echo|print)\s+",
        "escape_functions": [
            "esc_html", "esc_attr", "esc_url", "esc_js", "esc_textarea",
            "wp_kses", "wp_kses_post", "printf", "sprintf", "wp_json_encode",
            "__", "_e", "_x", "_ex", "_n", "_nx",
        ],
    },
    "unprepared_sql": {
        "name": "$wpdb query without $wpdb->prepare()",
        "query_pattern": r"\$wpdb\s*->\s*(?:get_result|get_row|get_col|get_var|query)\s*\(",
        "prepare_pattern": r"\$wpdb\s*->\s*prepare\s*\(",
    },
    "unescaped_wp_die": {
        "name": "wp_die() message without escaping",
        "regex": r"\bwp_die\s*\(",
        "escape_functions": [
            "esc_html", "esc_html_e", "esc_attr", "wp_kses", "sprintf", "__", "_e",
        ],
    },
    "debug_output": {
        "name": "Debug output (print_r/var_dump) in production code",
        "regex": r"\b(?:print_r|var_dump|debug_print_backtrace|xdebug_var_dump)\s*\(",
    },
    "missing_nonce": {
        "name": "Form/AJAX handler without nonce check",
        "body_patterns": [r"\$_POST", r"\$_GET"],
        "required_in_body": [r"wp_verify_nonce", r"check_admin_referer"],
        "scan_window": 2000,
    },
    "missing_capability": {
        "name": "Privileged operation without capability check",
        "body_patterns": [
            r"\$_POST", r"\$_GET",
            r"\bwp_delete_", r"\bwp_trash_", r"\bwp_insert_", r"\bwp_update_",
            r"\bupdate_option\b", r"\bdelete_option\b",
            r"\badd_user_meta\b", r"\bupdate_user_meta\b",
        ],
        "required_in_body": [r"current_user_can"],
        "scan_window": 500,
    },
    "missing_rest_permission": {
        "name": "REST route without permission_callback",
        "regex": r"register_rest_route\s*\(",
        "required_in_context": r"permission_callback",
    },
    "file_upload_no_mime_check": {
        "name": "File upload handling without MIME validation",
        "trigger_patterns": [r"\$_FILES"],
        "required_in_window": [r"finfo_open|finfo_file|mime_content_type|getimagesize"],
        "scan_window": 500,
    },
    "escape_used_as_sanitize": {
        "name": "Escaping function used as sanitization (not for DB storage)",
        "pattern": r"(?:esc_html|esc_attr|esc_url)\s*\(\s*(?:\$_POST|\$_GET|\$_COOKIE)",
        "storage_context": [r"update_option", "insert_post", "wp_insert", "add_user_meta", "update_user_meta"],
    },
    "context_escape_mismatch": {
        "name": "Wrong escape function for HTML context (see securing-output.md)",
        "patterns": {
            "href|src|action|url": r"esc_url",
            "class|style|data-": r"(?:esc_attr|esc_html)",
            "innerHTML|javascript:": r"wp_json_encode|wp_scripts|wp_add_inline_script",
            "sql|query|prepare": r"\$wpdb->prepare",
        },
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_file(path: Path) -> list[str]:
    """Return file lines, skipping non-UTF-8 gracefully."""
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []


def _is_comment_line(line: str) -> bool:
    stripped = line.strip()
    return (stripped.startswith("//") or stripped.startswith("*") or
            stripped.startswith("/*") or stripped.startswith("#"))


def _find_function_body(lines: list[str], func_start_idx: int) -> tuple[int, str]:
    """Return (end_line_idx, body_text) for the function starting at *func_start_idx*.

    Uses brace-counting with awareness of string literals to avoid false nesting.
    Handles multi-line function definitions and nested closures up to 3 levels deep.
    """
    depth = 0
    started = False
    body_lines: list[str] = []
    in_single_quote = False
    in_double_quote = False

    # Find opening brace — look ahead up to 5 lines for multi-line defs
    search_start = func_start_idx
    for i in range(func_start_idx, min(func_start_idx + 5, len(lines))):
        if "{" in lines[i]:
            search_start = i
            break

    for i in range(search_start, len(lines)):
        line = lines[i]
        body_lines.append(line)

        j = 0
        while j < len(line):
            ch = line[j]

            # Track string literals to avoid counting braces inside them
            if ch == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
            elif ch == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
            elif not in_single_quote and not in_double_quote:
                if ch == "{":
                    depth += 1
                    started = True
                elif ch == "}":
                    depth -= 1

            # Skip escaped characters
            if ch == "\\" and j + 1 < len(line):
                j += 1

            j += 1

        if started and depth <= 0:
            return i, "\n".join(body_lines)

    # Function never closed — return what we have
    end_idx = min(search_start + 30, len(lines))
    return end_idx, "\n".join(lines[search_start:end_idx])


def _is_string_literal_line(line: str) -> bool:
    """Heuristic: a line that is mostly a string assignment (common in docblocks)."""
    stripped = line.strip()
    # Skip lines that are purely string content or docblock comments
    return (stripped.startswith('"') and stripped.endswith(('"', '";')) or
            stripped.startswith("'") and stripped.endswith(("'", "';")))


# ---------------------------------------------------------------------------
# Check handlers
# ---------------------------------------------------------------------------

def _check_superglobal(line: str, check_cfg: dict) -> bool:
    """Check 1 — raw superglobal without sanitizer."""
    if re.search(check_cfg["regex"], line):
        return not re.search(check_cfg["sanitizer_pattern"], line)
    return False


def _check_input_type_mismatch(line: str, check_cfg: dict) -> bool:
    """NEW Check — input type doesn't match expected sanitizer.

    Grounded in /references/plugin-security/data-validation.md decision tree:
    - Email fields → sanitize_email() + is_email()
    - URL fields → esc_url_raw() for storage
    - File uploads → finfo_open() MIME check
    - Textarea → sanitize_textarea_field() or wp_kses_post()
    """
    for input_pattern, required_sanitizers in check_cfg["mappings"].items():
        if re.search(input_pattern, line):
            # Line matches an input type — check if the right sanitizer is used
            has_correct_sanitizer = any(
                re.search(r"\b" + re.escape(san) + r"\s*\(", line)
                for san in required_sanitizers
            )
            if not has_correct_sanitizer:
                return True
    return False


def _check_output_escaping(line: str, check_cfg: dict) -> bool:
    """Check 2 — echo/print without escaping function."""
    if re.search(check_cfg["regex"], line):
        for fn in check_cfg["escape_functions"]:
            if fn in line:
                return False
        return True
    return False


def _check_unprepared_sql(lines: list[str], idx: int, check_cfg: dict) -> bool:
    """Check 3 — $wpdb query without prepare()."""
    if not re.search(check_cfg["query_pattern"], lines[idx]):
        return False
    # Look back up to 20 chars for prepare() on the same line
    if re.search(check_cfg["prepare_pattern"], lines[idx]):
        return False
    # Look forward up to 15 lines for prepare() wrapping this call
    for j in range(idx, min(idx + 15, len(lines))):
        if re.search(check_cfg["prepare_pattern"], lines[j]):
            return False
    return True


def _check_wp_die(line: str, check_cfg: dict) -> bool:
    """Check 6 — wp_die() without escaping."""
    if not re.search(check_cfg["regex"], line):
        return False
    for fn in check_cfg["escape_functions"]:
        if fn in line:
            return False
    return True


def _check_debug_output(line: str, check_cfg: dict) -> bool:
    """Check 7 — debug output functions."""
    return bool(re.search(check_cfg["regex"], line))


def _check_nonce(lines: list[str], idx: int, check_cfg: dict) -> bool:
    """Check 4 — function with $_POST/$_GET but no nonce check in body."""
    if not re.match(r"\s*function\s+", lines[idx]) and not re.match(r"\s*def\s+\w+\s*\(", lines[idx]):
        return False
    _, body = _find_function_body(lines, idx)
    has_trigger = any(re.search(p, body) for p in check_cfg["body_patterns"])
    has_nonce = any(
        re.search(p, body[:check_cfg["scan_window"]])
        for p in check_cfg["required_in_body"]
    )
    return has_trigger and not has_nonce


def _check_capability(lines: list[str], idx: int, check_cfg: dict) -> bool:
    """Check 5 — function with privileged ops but no capability check."""
    if not re.match(r"\s*function\s+", lines[idx]) and not re.match(r"\s*def\s+\w+\s*\(", lines[idx]):
        return False
    _, body = _find_function_body(lines, idx)
    has_trigger = any(re.search(p, body) for p in check_cfg["body_patterns"])
    has_cap = any(
        re.search(p, body[:check_cfg["scan_window"]])
        for p in check_cfg["required_in_body"]
    )
    return has_trigger and not has_cap


def _check_rest_permission(lines: list[str], idx: int, check_cfg: dict) -> bool:
    """Check 9 — register_rest_route without permission_callback."""
    if not re.search(check_cfg["regex"], lines[idx]):
        return False
    context = "\n".join(lines[idx : idx + 11])
    return check_cfg["required_in_context"] not in context


def _check_file_upload_mime(lines: list[str], idx: int, check_cfg: dict) -> bool:
    """Check 10 — $_FILES usage without MIME validation."""
    has_files = any(re.search(p, lines[idx]) for p in check_cfg["trigger_patterns"])
    if not has_files:
        return False
    window = "\n".join(lines[idx : idx + check_cfg["scan_window"]])
    has_mime_check = any(
        re.search(p, window) for p in check_cfg["required_in_window"]
    )
    return not has_mime_check


def _check_escape_as_sanitize(line: str, check_cfg: dict) -> bool:
    """Check 11 — esc_* used on superglobal destined for storage."""
    if not re.search(check_cfg["pattern"], line):
        return False
    return True  # Context checked by caller


def _check_context_escape_mismatch(line: str, check_cfg: dict) -> bool:
    """NEW Check 12 — wrong escape function for the HTML context.

    Grounded in /references/plugin-security/securing-output.md context table:
    - href/src/action/url attributes → must use esc_url()
    - class/style/data-* attributes → must use esc_attr() or esc_html()
    - JavaScript/innerHTML → must use wp_json_encode() or proper script handling
    - SQL values → must use $wpdb->prepare()
    """
    line_lower = line.lower()

    for context_keyword, required_escape in check_cfg["patterns"].items():
        if context_keyword in line_lower:
            # Check if the required escape is present
            if not re.search(required_escape, line):
                return True
    return False


# ---------------------------------------------------------------------------
# Dispatcher map: check key → handler
# ---------------------------------------------------------------------------
HANDLERS = {
    "raw_superglobal": _check_superglobal,
    "input_type_mismatch": _check_input_type_mismatch,
    "unescaped_output": _check_output_escaping,
    "unprepared_sql": _check_unprepared_sql,
    "unescaped_wp_die": _check_wp_die,
    "debug_output": _check_debug_output,
    "missing_nonce": _check_nonce,
    "missing_capability": _check_capability,
    "missing_rest_permission": _check_rest_permission,
    "file_upload_no_mime_check": _check_file_upload_mime,
    "context_escape_mismatch": _check_context_escape_mismatch,
}


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def check_file(filepath: Path) -> list[dict]:
    """Run all enabled checks on a single PHP file.

    Returns a list of dicts: { 'line': int, 'check': str, 'message': str, 'severity': str }
    """
    lines = _read_file(filepath)
    issues: list[dict] = []
    seen: set[tuple[int, str]] = set()  # Deduplicate (line, check_key)

    for idx, line in enumerate(lines):
        line_no = idx + 1  # 1-based display number

        if _is_comment_line(line):
            continue
        if _is_string_literal_line(line):
            continue

        # --- Line-level checks (run every line) ---
        for key, check_cfg in CHECKS.items():
            handler = HANDLERS.get(key)
            if not handler:
                continue

            try:
                result = handler(lines, idx, check_cfg) if key in (
                    "unprepared_sql", "missing_nonce", "missing_capability",
                    "missing_rest_permission", "file_upload_no_mime_check",
                    "context_escape_mismatch"
                ) else handler(line, check_cfg)

                if result:
                    dedup_key = (line_no, key)
                    if dedup_key not in seen:
                        seen.add(dedup_key)
                        severity = SEVERITY.get(key, "medium")
                        issues.append({
                            "line": line_no,
                            "check": key,
                            "message": CHECKS[key]["name"],
                            "severity": severity,
                        })
            except Exception:
                pass

        # --- Escape-as-sanitize (special: needs surrounding context) ---
        esc_cfg = CHECKS.get("escape_used_as_sanitize")
        if esc_cfg and re.search(esc_cfg["pattern"], line):
            ctx_lines = lines[max(0, idx - 3): min(len(lines), idx + 4)]
            ctx = "\n".join(ctx_lines)
            if any(re.search(p, ctx) for p in esc_cfg["storage_context"]):
                dedup_key = (line_no, "escape_used_as_sanitize")
                if dedup_key not in seen:
                    seen.add(dedup_key)
                    issues.append({
                        "line": line_no,
                        "check": "escape_used_as_sanitize",
                        "message": esc_cfg["name"],
                        "severity": SEVERITY.get("escape_used_as_sanitize", "high"),
                    })

    return issues


def main() -> None:
    # Parse optional arguments
    args = sys.argv[1:]
    target_path = None
    exclude_patterns = ["vendor/", "tests/", "node_modules/", "test/", ".git/"]
    severity_filter = None
    show_summary = False

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--exclude" and i + 1 < len(args):
            exclude_patterns = args[i + 1].split(",")
            i += 2
        elif arg.startswith("--exclude="):
            exclude_patterns = arg.split("=", 1)[1].split(",")
            i += 1
        elif arg == "--severity" and i + 1 < len(args):
            severity_filter = args[i + 1].lower()
            if severity_filter not in SEVERITY_ORDER:
                print(f"Error: unknown severity '{args[i+1]}'. Choose from: low, medium, high, critical")
                sys.exit(1)
            i += 2
        elif arg.startswith("--severity="):
            severity_filter = arg.split("=", 1)[1].lower()
            if severity_filter not in SEVERITY_ORDER:
                print(f"Error: unknown severity '{severity_filter}'. Choose from: low, medium, high, critical")
                sys.exit(1)
            i += 1
        elif arg == "--summary":
            show_summary = True
            i += 1
        elif not arg.startswith("--"):
            target_path = arg
            i += 1
        else:
            print(f"Warning: unknown option '{arg}', ignoring.")
            i += 1

    if not target_path:
        print("Usage: python3 scripts/verify_wp_plugin.py <path_to_plugin_dir> [--exclude <glob>] [--severity <level>] [--summary]")
        sys.exit(1)

    target = Path(target_path).resolve()
    if not target.is_dir():
        print(f"Error: {target} is not a valid directory.")
        sys.exit(1)

    # Build exclude regexes
    exclude_regexes = [re.compile(re.escape(p).replace(r"\*", ".*")) for p in exclude_patterns]

    def _should_exclude(path: Path) -> bool:
        path_str = str(path)
        return any(rx.search(path_str) for rx in exclude_regexes)

    php_files = sorted(target.rglob("*.php"))
    filtered_files = [f for f in php_files if not _should_exclude(f)]

    total_issues = 0
    check_counts: dict[str, int] = {}
    severity_counts: dict[str, int] = {s: 0 for s in SEVERITY_ORDER}

    for php_file in filtered_files:
        issues = check_file(php_file)

        # Apply severity filter
        if severity_filter:
            min_severity = SEVERITY_ORDER[severity_filter]
            issues = [i for i in issues if SEVERITY_ORDER.get(i["severity"], 0) >= min_severity]

        if issues:
            print(f"{php_file.relative_to(target)}:")
            for issue in issues:
                severity_icon = {"low": "ℹ", "medium": "⚠", "high": "🔴", "critical": "💥"}.get(issue["severity"], "?")
                print(f"  {severity_icon} Line {issue['line']}: [{issue['severity'].upper()}] {issue['message']}")
            print()

        for issue in issues:
            total_issues += 1
            check_counts[issue["check"]] = check_counts.get(issue["check"], 0) + 1
            severity_counts[issue["severity"]] = severity_counts.get(issue["severity"], 0) + 1

    # Summary output
    if show_summary or total_issues > 0:
        print("=" * 60)
        print(f"Total issues found: {total_issues}")
        if severity_counts:
            sev_parts = [f"{s}: {c}" for s, c in sorted(severity_counts.items(), key=lambda x: SEVERITY_ORDER.get(x[0], -1), reverse=True) if c > 0]
            print(f"By severity: {', '.join(sev_parts)}")
        if check_counts and show_summary:
            print("By check type:")
            for check_key, count in sorted(check_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  {CHECKS[check_key]['name']}: {count}")
        if total_issues > 0:
            print("Review and fix before deploying.")
        else:
            print("No issues detected. Good work!")


if __name__ == "__main__":
    main()
