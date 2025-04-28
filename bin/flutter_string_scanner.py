import os
import re
import argparse
from typing import List, Tuple
from pathlib import Path

class FlutterStringScanner:
    def __init__(self, project_path: str, exclude_dirs: List[str], exclude_files: List[str]):
        self.project_path = Path(project_path)
        self.exclude_dirs = [Path(d) for d in exclude_dirs]
        self.exclude_files = [Path(f) for f in exclude_files]
        self.static_strings: List[Tuple[str, str, int]] = []

    def is_excluded(self, path: Path) -> bool:
        """Check if a file or directory should be excluded."""
        for excl_dir in self.exclude_dirs:
            if excl_dir in path.parents or path.name == excl_dir.name:
                return True
        return path.name in self.exclude_files

    def scan_dart_file(self, file_path: Path):
        """Scan a single .dart file for static strings."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.splitlines()

            # Regex to find static strings (e.g., "Hello" or 'World')
            string_pattern = r'(?<!\w)(?:\"(?:[^\"\\]|\\.)*\"|\'(?:[^\'\\]|\\.)*\')'
            strings = re.finditer(string_pattern, content)

            for match in strings:
                string = match.group(0)
                start_pos = match.start()

                # Calculate line number
                line_number = content[:start_pos].count('\n') + 1

                # Skip strings in comments or translation contexts
                line = lines[line_number - 1].strip()
                try:
                    comment_index = line.index('//') if '//' in line else len(line)
                    string_index = line.index(string) if string in line else len(line)
                    if (
                            comment_index < string_index or
                            '/*' in content[:start_pos] or
                            'AppLocalizations.of(context)' in line or
                            'S.of(context)' in line
                    ):
                        continue
                except ValueError:
                    # Skip if string spans multiple lines or not found in line
                    continue

                # Store the static string with file and line number
                self.static_strings.append((str(file_path), string, line_number))

    def scan_project(self):
        """Scan all .dart files in the project."""
        for root, _, files in os.walk(self.project_path):
            root_path = Path(root)
            if self.is_excluded(root_path):
                continue

            for file in files:
                file_path = root_path / file
                if file.endswith('.dart') and not self.is_excluded(file_path):
                    self.scan_dart_file(file_path)

    def generate_report(self) -> str:
        """Generate a report of found static strings."""
        if not self.static_strings:
            return "No untranslated static strings found."

        report = ["Untranslated Static Strings Report", "=" * 40]
        for file_path, string, line in self.static_strings:
            report.append(f"File: {file_path}")
            report.append(f"Line: {line}")
            report.append(f"String: {string}")
            report.append("-" * 40)
        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(
        description="Scan Flutter project for untranslated static strings."
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Path to the Flutter project directory (default: current directory)"
    )
    parser.add_argument(
        "--exclude-dirs",
        nargs="*",
        default=["build", ".dart_tool", "generated"],
        help="Directories to exclude from scanning"
    )
    parser.add_argument(
        "--exclude-files",
        nargs="*",
        default=["main.dart"],
        help="Files to exclude from scanning"
    )

    args = parser.parse_args()

    scanner = FlutterStringScanner(
        project_path=args.path,
        exclude_dirs=args.exclude_dirs,
        exclude_files=args.exclude_files
    )
    scanner.scan_project()
    print(scanner.generate_report())

if __name__ == "__main__":
    main()
