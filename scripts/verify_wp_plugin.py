#!/usr/bin/env python3
"""
WordPress Plugin Security Validator

Scans PHP files for common security anti-patterns:
- Unsanitized $_GET/$_POST/$_COOKIE/$_FILES usage
- Unescaped echo/print output
- Missing nonce verification on form/AJAX handlers
- Missing capability checks on admin pages
- SQL queries without $wpdb->prepare()

Usage: python3 verify_wp_plugin.py <path_to_plugin_dir>
"""

import re
import sys
from pathlib import Path


def check_file(filepath: Path) -> list[str]:
    """Run all security checks on a single PHP file."""
    issues = []
    content = filepath.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Skip comments and strings that are just examples
        if stripped.startswith("//") or stripped.startswith("*"):
            continue

        # Check 1: Raw superglobal usage without sanitization
        raw_access = re.findall(
            r'\$_(GET|POST|COOKIE|FILES)\[', line
        )
        if raw_access and "sanitize_" not in line and "absint" not in line:
            issues.append(
                f"  ⚠ Line {line_num}: Raw superglobal access "
                f"($_{raw_access[0]}) without sanitization"
            )

        # Check 2: echo/print without escaping (simplified heuristic)
        if re.search(r'\b(?:echo|print)\s+', line):
            if not any(
                esc in line for esc in [
                    "esc_html", "esc_attr", "esc_url",
                    "wp_kses", "printf", "sprintf"
                ]
            ):
                # Skip if it's inside a function that returns (ob_start pattern)
                if "ob_start" not in content[:content.find(line)] if line else True:
                    issues.append(
                        f"  ⚠ Line {line_num}: echo/print without escaping function"
                    )

        # Check 3: SQL queries without $wpdb->prepare()
        if re.search(r'\$wpdb->(get_)?(result|row|col|var)\s*\(', line):
            if "$wpdb->prepare" not in content[max(0, content.find(line)-200):content.find(line)+200]:
                issues.append(
                    f"  ⚠ Line {line_num}: $wpdb query without $wpdb->prepare()"
                )

        # Check 4: Form/AJAX handler without nonce check
        if re.search(r'function\s+\w*ajax\w*', line, re.IGNORECASE):
            func_match = re.search(r'function\s+(\w+)', line)
            if func_match:
                func_name = func_match.group(1)
                # Check if function has nonce verification
                func_body_start = content.find(f"function {func_name}")
                if func_body_start >= 0:
                    # Get next 50 lines of function body
                    func_snippet = content[func_body_start:func_body_start+2000]
                    if "wp_verify_nonce" not in func_snippet and \
                       "check_admin_referer" not in func_snippet:
                        issues.append(
                            f"  ⚠ Function {func_name}: AJAX handler without nonce check"
                        )

        # Check 5: Admin page callback without capability check
        if re.search(r'function\s+\w*render\w*admin', line, re.IGNORECASE):
            func_match = re.search(r'function\s+(\w+)', line)
            if func_match:
                func_name = func_match.group(1)
                func_body_start = content.find(f"function {func_name}")
                if func_body_start >= 0:
                    func_snippet = content[func_body_start:func_body_start+500]
                    if "current_user_can" not in func_snippet:
                        issues.append(
                            f"  ⚠ Function {func_name}: Admin callback without capability check"
                        )

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verify_wp_plugin.py <plugin_directory>")
        print("Scans all .php files for common WordPress security issues.")
        sys.exit(1)

    plugin_dir = Path(sys.argv[1])
    if not plugin_dir.is_dir():
        print(f"Error: '{plugin_dir}' is not a valid directory.")
        sys.exit(1)

    php_files = list(plugin_dir.rglob("*.php"))
    if not php_files:
        print(f"No .php files found in '{plugin_dir}'.")
        sys.exit(0)

    total_issues = 0
    for php_file in sorted(php_files):
        issues = check_file(php_file)
        if issues:
            print(f"\n{php_file.relative_to(plugin_dir)}:")
            for issue in issues:
                print(issue)
            total_issues += len(issues)

    print(f"\n{'='*50}")
    if total_issues > 0:
        print(f"Found {total_issues} potential issue(s).")
        print("Review and fix before deploying.")
    else:
        print("No issues found. Plugin passes basic security checks.")


if __name__ == "__main__":
    main()
